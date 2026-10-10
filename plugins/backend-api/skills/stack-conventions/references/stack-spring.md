# Spring Security (resource server JWT) e Spring Boot

Fontes: documentação do Spring Security, "OAuth 2.0 Resource Server JWT" (V-20, https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html, série 7.1.1 estável, Verificado em 2026-10-10); OWASP (V-09, V-10); RFC 8725 (V-13). Código abaixo é adaptação própria dos padrões descritos na documentação; **confirme assinaturas na versão do projeto** (`mvn dependency:tree | grep spring-security` ou `gradle dependencies`). **Lacunas declaradas**: `ProblemDetail`, Bean Validation, Actuator e Spring Data não foram pesquisados (lacunas registradas em `fontes.md` do playbook); o que consta sobre eles abaixo é Inferido.

## Sumário

1. Checklist
2. Configuração do resource server
3. Validação de audiência
4. Escopos e autoridades
5. Autorização por objeto
6. Erros e validação (Inferido)
7. Verificação por busca

## 1. Checklist

- [ ] `issuer-uri` configurado: descobre as chaves e valida `iss`. `jwk-set-uri` sozinho **não** valida `iss` (V-20).
- [ ] Algoritmo: por padrão só RS256 é aceito (V-20); outro algoritmo exige configuração explícita e consciente.
- [ ] `exp`, `nbf` e `iss` validados por padrão, com tolerância de 60 s (V-20).
- [ ] **`aud` não é validado por padrão** (V-20): configure `audiences` (propriedade) ou `JwtClaimValidator` próprio.
- [ ] Escopos `scope`/`scp` viram autoridades `SCOPE_<valor>` (V-20); regras de rota usam esses nomes.
- [ ] Cadeia de filtros com **negação por padrão** (`anyRequest().authenticated()` ou `denyAll()` no fim).
- [ ] Sessão `STATELESS` para API com bearer; decisão sobre CSRF explícita (API sem cookie de sessão costuma desabilitar CSRF; com cookie, não).
- [ ] Autorização por **objeto** no service/repositório: escopo não substitui filtro de dono.
- [ ] Erros 401/403 no mesmo formato de erro do projeto (RFC 9457), sem detalhes internos.
- [ ] Rate limit em login/reset; segredos em variáveis de ambiente/cofre.

## 2. Configuração do resource server

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://idp.exemplo.com.br/       # valida iss e descobre as chaves
          audiences: orders-api                         # V-20: propriedade audiences
```

```java
@Configuration
@EnableMethodSecurity
class SecurityConfig {

  @Bean
  SecurityFilterChain api(HttpSecurity http) throws Exception {
    http
      .authorizeHttpRequests(a -> a
        .requestMatchers("/actuator/health").permitAll()
        .requestMatchers(HttpMethod.GET, "/orders/**").hasAuthority("SCOPE_orders:read")
        .requestMatchers(HttpMethod.POST, "/orders/**").hasAuthority("SCOPE_orders:write")
        .anyRequest().denyAll())                         // negar por padrão
      .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
      .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS));
    return http.build();
  }
}
```

Em Spring Boot, a propriedade `audiences` configura o decoder autoconfigurado; se o projeto define o próprio bean `JwtDecoder`, a autoconfiguração recua e a propriedade não o configura: valide a audiência no bean (próxima seção). (Inferido; confirme na documentação do Spring Boot da versão.)

## 3. Validação de audiência

Padrão da documentação para validar `aud` num `JwtDecoder` próprio (adaptado; confirme tipos e métodos na versão):

```java
@Bean
JwtDecoder jwtDecoder(@Value("${spring.security.oauth2.resourceserver.jwt.issuer-uri}") String issuer,
                      @Value("${app.audience}") String audience) {
  NimbusJwtDecoder decoder = JwtDecoders.fromIssuerLocation(issuer);
  OAuth2TokenValidator<Jwt> withIssuer = JwtValidators.createDefaultWithIssuer(issuer);
  OAuth2TokenValidator<Jwt> withAudience = new JwtClaimValidator<List<String>>(
      JwtClaimNames.AUD, aud -> aud != null && aud.contains(audience));
  decoder.setJwtValidator(new DelegatingOAuth2TokenValidator<>(withIssuer, withAudience));
  return decoder;
}
```

Teste: token válido de **outra audiência** deve ser recusado com 401. Sem esse teste, "a configuração parece certa" não prova nada.

## 4. Escopos e autoridades

Por padrão `scope`/`scp` viram `SCOPE_<valor>` (V-20). Para papéis em outra claim (`roles`, `realm_access`), configure um `JwtAuthenticationConverter` com `JwtGrantedAuthoritiesConverter` (`setAuthoritiesClaimName`, `setAuthorityPrefix`); confirme a classe na versão. Evite misturar `ROLE_` e `SCOPE_` sem decisão: o prefixo errado faz `hasAuthority` nunca casar e a rota ficar negada (ou, mal configurada, aberta).

```java
@PreAuthorize("hasAuthority('SCOPE_orders:write')")
public Order cancelar(UUID id, Jwt jwt) { ... }
```

## 5. Autorização por objeto

```java
public Order obter(UUID id, @AuthenticationPrincipal Jwt jwt) {
  UUID dono = UUID.fromString(jwt.getSubject());
  return repo.findByIdAndOwnerId(id, dono)                 // dono vem do token
             .orElseThrow(OrderNotFoundException::new);    // alheio = inexistente (404)
}
```

Alternativa: `@PostAuthorize`/`@PreAuthorize` com expressão que consulta o dono, ou `AuthorizationManager` próprio. O essencial é que a consulta nunca aceite um ID sem o dono.

## 6. Erros e validação (Inferido; fora das fontes)

- Spring 6+ traz a classe `ProblemDetail` para o formato de erro do tipo RFC 7807/9457, com suporte em `ResponseEntityExceptionHandler` e propriedade para ativar a resposta; confirme o nome exato da propriedade e a versão da RFC implementada na documentação do Spring Framework do projeto.
- Bean Validation (`@Valid`, `@NotNull`, `@Size`): valide DTOs na borda; traduza `MethodArgumentNotValidException` para o formato de erro do projeto sem ecoar valores sensíveis.
- Actuator: exponha apenas `health`/`info` necessários; `management.endpoints.web.exposure.include=*` em produção é achado de configuração (OWASP API8).

## 7. Verificação por busca

```bash
grep -rEn "jwk-set-uri|issuer-uri|audiences" src/main/resources
grep -rEn "JwtDecoder|JwtClaimValidator|JwtValidators" src/main/java
grep -rEn "permitAll|anyRequest\(\)" src/main/java        # a regra final deve ser authenticated()/denyAll()
grep -rEn "csrf|sessionCreationPolicy" src/main/java
grep -rEn "ROLE_|SCOPE_|hasRole|hasAuthority" src/main/java
grep -rEn "findById\(" src/main/java                       # BOLA: ID sem dono (candidato)
```

Um achado "`aud` não validado" exige ler `application.yml`/`properties` **e** os beans de `JwtDecoder`; a ausência de `audiences` sem validador próprio é o achado (V-20).
