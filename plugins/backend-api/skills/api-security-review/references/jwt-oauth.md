# JWT e OAuth 2.0: checklist de revisão e código

Fontes (Verificado em 2026-10-10, redação própria): RFC 8725 JWT BCP (V-13, https://www.rfc-editor.org/rfc/rfc8725), RFC 9700 OAuth 2.0 Security BCP (V-12, https://datatracker.ietf.org/doc/html/rfc9700), OWASP REST Security Cheat Sheet (V-10), Spring Security 7.1.1 (V-20), FastAPI (V-21), NestJS guards (V-19). Trechos de código são exemplos escritos aqui, não cópias; confira a API na versão instalada (bibliotecas mudam). Cerca de 35% da RFC 9700 (seções finais) não foi lida na pesquisa.

## Sumário

1. Checklist JWT
2. Checklist OAuth 2.0
3. Código vulnerável x seguro (Python PyJWT, Node jose)
4. Spring e Nest em uma linha
5. Sessão, refresh e revogação
6. Lacunas

## 1. Checklist JWT

Cada linha vira uma pergunta com evidência (`arquivo:linha`) ou "Não verificado".

- [ ] **Algoritmo fixado no servidor** (lista explícita, ex.: `RS256`/`ES256`); o `alg` do header do token nunca decide como verificar (V-13).
- [ ] `none` rejeitado; HMAC (HS256) só com segredo de alta entropia e nunca com chave pública usada como segredo (confusão RS/HS).
- [ ] `iss` validado contra o emissor esperado; a chave de verificação pertence a esse emissor (V-13).
- [ ] `aud` validado quando o emissor atende várias partes (V-13). Em Spring, **não vem ligado** por padrão (V-20).
- [ ] `exp` (e `nbf` quando usado) validados, com tolerância pequena e documentada (Spring usa 60 s, V-20). RFC 8725 não trata `exp`/`nbf`; a exigência vem do OWASP (V-10) e da biblioteca.
- [ ] `typ` explícito quando houver tipos de token diferentes (access x ID token) (V-13).
- [ ] `kid` sanitizado (injeção SQL/LDAP/caminho) e usado só para escolher entre chaves já conhecidas; `jku`/`x5u` só de allowlist (SSRF) ou ignorados (V-13).
- [ ] JWKS buscado do emissor com cache e rotação; falha de busca não vira "aceitar".
- [ ] `jti` + lista de revogação quando o produto exige revogação antes do `exp` (V-10).
- [ ] Token fora da query string, fora de log e de mensagem de erro; resposta de login com `Cache-Control: no-store`.
- [ ] Dados sensíveis não vão no payload (JWT assinado é legível por qualquer um).

## 2. Checklist OAuth 2.0 (RFC 9700)

- [ ] **Authorization Code + PKCE** para clientes públicos (MUST); recomendado para confidenciais; o servidor de autorização deve suportar PKCE (V-12).
- [ ] Redirect URI com **comparação exata de string** (exceção: porta em loopback para apps nativos) (V-12).
- [ ] Password grant: **proibido** (MUST NOT). Implicit: **desencorajado** (SHOULD NOT; correção ao que as lentes diziam) (V-12).
- [ ] Token de acesso nunca na query string; use header `Authorization` (V-12, V-10).
- [ ] Refresh token de cliente público: sender-constraint (mTLS/DPoP) **ou rotação** (V-12).
- [ ] Escopos mínimos e audiência restrita por token (Inferido a partir da RFC 9700; seção não relida).
- [ ] Parâmetro `state`/PKCE e verificação de `iss` na resposta para mitigar mix-up (item da pesquisa, não reconferido: **Inferido**).
- [ ] O resource server valida o token em **toda** requisição e autoriza por escopo e por objeto; escopo não substitui checagem de dono.
- [ ] Segredo de cliente confidencial fora do código e do front; rotação documentada.

## 3. Código vulnerável x seguro

### Python (PyJWT; confira a versão instalada)

```python
import jwt  # PyJWT

# VULNERÁVEL: o algoritmo vem do próprio token; aud não é verificada
def current_user_bad(token: str) -> dict:
    header = jwt.get_unverified_header(token)
    return jwt.decode(token, SECRET, algorithms=[header["alg"]], options={"verify_aud": False})

# SEGURO: algoritmo, emissor, audiência e claims obrigatórias fixados no servidor
def current_user(token: str) -> dict:
    return jwt.decode(
        token,
        key=PUBLIC_KEY,                 # obtida do JWKS do emissor, com cache
        algorithms=["RS256"],
        audience="orders-api",
        issuer="https://idp.exemplo.com.br/",
        options={"require": ["exp", "iss", "aud", "sub"]},
        leeway=30,                      # segundos de tolerância de relógio
    )
```

Em FastAPI a dependência usa `OAuth2PasswordBearer(tokenUrl=...)` apenas para extrair o header; **a validação acima é por conta do projeto** (V-21). `python-jose` e `passlib` têm manutenção fraca (Inferido a partir do comentário da leitura de V-29); prefira PyJWT e bcrypt/pwdlib/argon2 e confira o estado atual.

### Node (biblioteca jose; confira a versão instalada)

```typescript
import { createRemoteJWKSet, jwtVerify } from 'jose';

const jwks = createRemoteJWKSet(new URL('https://idp.exemplo.com.br/.well-known/jwks.json'));

export async function verificar(token: string) {
  const { payload } = await jwtVerify(token, jwks, {
    issuer: 'https://idp.exemplo.com.br/',
    audience: 'orders-api',
    algorithms: ['RS256'],        // fixado no servidor
    clockTolerance: 30,           // segundos
  });
  return payload;                  // sub, scope etc. já com exp/nbf checados pela biblioteca
}
```

A URL do JWKS vem de configuração do servidor, nunca do `jku`/`x5u` do token (SSRF, V-13).

## 4. Spring e Nest em uma linha

- **Spring (V-20, série 7.1.1):** `issuer-uri` descobre as chaves e valida `iss`; `jwk-set-uri` sozinho **não** valida `iss`; só RS256 por padrão; `exp`/`nbf`/`iss` com tolerância de 60 s; `aud` só com a propriedade `audiences` ou `JwtClaimValidator`; `scope`/`scp` viram `SCOPE_<valor>`. Detalhe e código em `${CLAUDE_PLUGIN_ROOT}/skills/stack-conventions/references/stack-spring.md`.
- **NestJS (V-19):** guard de autenticação anexa `request.user`; guard de papel lê metadata (`Reflector.createDecorator`/`@SetMetadata`); `APP_GUARD` permite injeção de dependências e `useGlobalGuards()` fora de módulo não; guard que devolve `false` gera 403. Detalhe em `stack-nestjs-node.md`.

## 5. Sessão, refresh e revogação

- Access token de vida curta; refresh com rotação e detecção de reuso (Inferido). Logout/revogação precisam de ponto de consulta (lista de `jti`, versão de sessão) se o requisito exigir efeito imediato; JWT puro não revoga sozinho.
- Cookie de sessão: `HttpOnly`, `Secure`, `SameSite` conforme o fluxo; CSRF tratado quando houver cookie (Inferido; fora do escopo de V).
- Senhas: Argon2 ou bcrypt por biblioteca (V-27 classe C, corroborada por V-10); nunca registrar senha ou token em log.

## 6. Lacunas declaradas

OIDC Core (validação de ID token, `nonce`), ABAC/ReBAC, multi-tenancy com RLS e DPoP em detalhe não têm fonte validada neste plugin (lacuna registrada em `fontes.md` do playbook). Declare "Não verificado" ou delegue a `security-appsec`.
