# Grade OWASP API Security Top 10 (2023) para revisão

Fonte dos 10 títulos: https://api-security.owasp.org/editions/2023/en/0x11-t10 (V-09, Verificado em 2026-10-10; a página não cita edição mais nova que 2023). Hardening complementar: OWASP REST Security Cheat Sheet (V-10, Verificado). As colunas "o que procurar", "candidatos de busca" e "correção" são redação própria a partir de conhecimento estável do domínio e dos textos de V-10; os textos de prevenção por risco do OWASP não foram lidos por inteiro na pesquisa: **Inferido**. Confira a edição vigente em https://owasp.org antes de citar.

Os candidatos de busca são **heurísticas** para achar onde ler; nunca reporte sem confirmar o fluxo. Ajuste caminhos e extensões ao projeto.

## Sumário

- API1 a API10 (seções abaixo)
- Como registrar a resposta
- Candidatos de busca consolidados

## Como registrar a resposta

Para cada risco, escreva uma linha: `APIn · Aplicável? · Evidência (arquivo:linha) ou "Não verificado" · Achado (ID) ou "sem achado"`. Risco que não se aplica leva "Não aplicável" com motivo (ex.: sem upload de arquivo).

## API1:2023 Broken Object Level Authorization (BOLA)

- **Pergunta (V-09):** todo acesso a objeto por ID checa o dono?
- **Procurar:** consultas por `id` vindo da rota/corpo sem filtro por `owner_id`/`tenant_id`; ORM `get(id)`/`findById` direto no handler; agregações e exportações que ignoram o filtro; IDs sequenciais.
- **Busca:** `grep -rEn "find(ById|One)\(|\.get\(|filter\(.*\.id ==" src/` e então ler se há condição de dono; rotas com `:id`/`{id}` sem guard de propriedade.
- **Correção:** filtro de dono/tenant em toda consulta, vindo da identidade autenticada (dependência/guard), nunca do corpo; recurso alheio responde 404 idêntico ao inexistente (status e formato de corpo iguais). IDs não sequenciais ajudam, mas não substituem a checagem.

```python
# vulnerável: qualquer usuário autenticado lê qualquer pedido
order = db.query(Order).filter(Order.id == order_id).first()
# seguro: o dono vem da identidade, e a ausência é indistinguível de inexistente
order = db.query(Order).filter(Order.id == order_id, Order.owner_id == user.id).first()
if order is None:
    raise NotFound()
```

## API2:2023 Broken Authentication

- **Pergunta:** a autenticação de tokens, senhas e chaves resiste a forjamento, força bruta e vazamento?
- **Procurar:** JWT mal validado (ver [jwt-oauth.md](jwt-oauth.md)); login/reset sem rate limit; senha com hash fraco; credencial ou token em URL/log; troca de e-mail/senha sem reautenticação; autenticação própria no lugar de biblioteca; tutorial que "extrai" o token sem validar (V-21).
- **Busca:** `grep -rEn "jwt\.(decode|verify)|get_unverified|algorithms|verify_signature|md5|sha1\(|password" src/`; `grep -rEn "login|reset" src/` e verificar limitador.
- **Correção:** biblioteca padrão para JWT e hash de senha (Argon2 ou bcrypt, V-27 classe C corroborada por V-10), rate limit por conta e por IP em login/reset, mensagens de erro iguais para "usuário inexistente" e "senha errada", MFA quando o produto exigir.

## API3:2023 Broken Object Property Level Authorization

- **Pergunta:** o chamador pode ler ou alterar **propriedades** que não deveria (exposição excessiva e atribuição em massa)?
- **Procurar:** retorno direto de entidade/modelo do ORM; `**request.json`/`Object.assign(entity, body)`/`model_dump()` aplicado à entidade; DTO de entrada com `role`, `is_admin`, `price`, `owner_id`, `tenant_id`; `response_model_exclude` usado como proteção (não muda o OpenAPI, V-21).
- **Busca:** `grep -rEn "\*\*(request|body|payload|data)|Object\.assign\(|setattr\(|\.update\(.*(body|data)" src/`.
- **Correção:** DTOs de entrada e de saída separados e fechados (lista de campos permitidos, `extra="forbid"` / `additionalProperties: false` / `whitelist` + `forbidNonWhitelisted` no Nest); campos sensíveis nunca no DTO de saída; escrita de propriedade privilegiada exige função própria.

## API4:2023 Unrestricted Resource Consumption

- **Pergunta:** há limite de tamanho, quantidade, tempo e frequência?
- **Procurar:** listas sem `limit` máximo; corpo sem limite (413); upload sem teto; consulta/agregação sem timeout; operação em lote sem teto de itens; chamadas caras (SMS, e-mail, IA) sem cota; falta de rate limit em endpoints sensíveis.
- **Regra de modo:** em design é achado; em diff, só se o diff remove/omite limite em endpoint sensível com cenário concreto (ver SKILL.md).
- **Correção:** `page_size` com máximo; limites de corpo/arquivo/profundidade; timeouts; rate limit com chave de **credencial validada**, 429 com `Retry-After`; cota por plano; política de falha do armazenamento do limite por rota (aberta em formulário de baixo risco, fechada em login/pagamento: heurística de fonte classe C, V-33).

## API5:2023 Broken Function Level Authorization (BFLA)

- **Pergunta:** funções administrativas e de outro papel estão protegidas por papel/escopo no servidor?
- **Procurar:** rotas `/admin`, `/internal`, métodos DELETE/PUT sem guard; checagem de papel só no front; troca de método HTTP que contorna regra (GET protegido, POST aberto); guard registrado só em algumas rotas.
- **Busca:** listar todas as rotas e cruzar com guards: `grep -rEn "@(app|router)\.(get|post|put|patch|delete)|@(Get|Post|Put|Patch|Delete)\(" src/` e `grep -rEn "Depends\(|UseGuards|PreAuthorize|\[Authorize" src/`.
- **Correção:** negar por padrão (guard global, ex.: Nest `APP_GUARD`, V-19; Spring `authorizeHttpRequests` com `anyRequest().authenticated()`/`denyAll()` no fim); escopos `SCOPE_*` mapeados (V-20); teste por perfil.

## API6:2023 Unrestricted Access to Sensitive Business Flows

- **Pergunta:** fluxos de negócio valiosos (compra, cadastro, cupom, reserva, envio) resistem a uso automatizado em escala?
- **Procurar:** criação de conta/cupom/reserva sem limite por identidade; ausência de controle de repetição; sem detecção de padrão anômalo; promoções sem cota.
- **Correção:** limite por identidade e por fluxo, idempotência, desafio/verificação em etapas de risco, cota; decisão de produto: registre como "a confirmar" quando a regra for de negócio.

## API7:2023 Server Side Request Forgery (SSRF)

- **Pergunta:** toda URL remota fornecida pelo cliente passa por allowlist (V-09)?
- **Procurar:** `requests.get(url)`, `fetch(url)`, `http.Get(url)`, `HttpClient` com URL vinda de corpo/query/webhook/imagem remota/importação; `jku`/`x5u` em JWT (V-13); redirects seguidos automaticamente.
- **Busca:** `grep -rEn "(requests|httpx)\.(get|post)\(|fetch\(|http\.(Get|NewRequest)\(|WebClient|RestTemplate" src/` e rastrear a origem do argumento.
- **Correção:** allowlist de hosts/esquemas resolvida após DNS, bloqueio de faixas internas e metadados de nuvem, desligar seguimento de redirect ou revalidar cada salto, timeout, sem devolver o corpo bruto da resposta remota ao cliente.

## API8:2023 Security Misconfiguration

- **Pergunta:** transporte, cabeçalhos, CORS, erros e ambientes estão configurados com segurança?
- **Procurar (V-10):** HTTP sem TLS/HSTS; `Cache-Control: no-store` ausente em dado sensível; `X-Content-Type-Options` ausente; CORS com `*` ou refletindo `Origin` junto de `Allow-Credentials: true`; stack trace/SQL/hostname em erro; modo debug em produção; docs/Swagger/introspecção GraphQL abertos; métodos HTTP não necessários habilitados (405 com `Allow`); endpoints de gestão expostos; segredos em código.
- **Busca:** `grep -rEn "allow_origins|Access-Control-Allow|cors\(|DEBUG\s*=\s*True|debug:\s*true|traceback|printStackTrace" src/ config/`.
- **Correção:** configuração por ambiente, CORS com lista explícita, handler central de erros (RFC 9457) sem detalhes internos, endpoints de gestão fora da internet, segredos por variável de ambiente/cofre.

## API9:2023 Improper Inventory Management

- **Pergunta:** versões antigas, endpoints de teste e ambientes paralelos estão inventariados e protegidos ou desligados?
- **Procurar:** rotas `/v1` ainda ativas sem dono; `/test`, `/debug`, `/beta`; spec que não bate com o código; ambiente de homologação com dado real; documentação desatualizada.
- **Correção:** inventário de versões e hosts, deprecação com data (`Deprecation`/`Sunset`, ver `api-contract-design`), diff entre rotas registradas e spec, remoção do que não tem dono.

## API10:2023 Unsafe Consumption of APIs

- **Pergunta:** respostas de APIs de terceiros são tratadas como dado não confiável?
- **Procurar:** resposta externa gravada sem validação; redirects seguidos cegamente; sem timeout/limite de tamanho; confiança em campo do fornecedor para decisão de autorização; webhook sem assinatura verificada (CRITICAL, V-24 AP4); saída de LLM usada como comando ou consulta.
- **Correção:** validar schema e tamanho de toda resposta externa, timeouts e limites, TLS verificado, assinatura HMAC sobre o corpo cru e dedupe de eventos (ver `idempotency-and-resilience`), tratar saída de modelo como dado.

## Candidatos de busca consolidados

```bash
# Rotas e guards (compare as duas listas)
grep -rEn "@(app|router)\.(get|post|put|patch|delete)|@(Get|Post|Put|Patch|Delete)\(|mux\.Handle(Func)?\(" src/
grep -rEn "Depends\(|UseGuards|PreAuthorize|\[Authorize|RequireAuthorization" src/
# Segredos e credenciais em texto (heurística; não imprima valores encontrados no relatório)
grep -rEIn "(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}" src/ config/
# Algoritmo e verificação de JWT
grep -rEn "get_unverified|verify_signature.*False|verify_aud.*False|algorithms\s*=|ignoreExpiration|alg.*none" src/
```

Ao relatar um segredo encontrado, cite `arquivo:linha` e o **tipo**, nunca o valor.
