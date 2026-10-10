# Checklist de design e revisão de API

Sumário: 1. Checklist numerado · 2. Mapa de status HTTP · 3. Mudanças quebrantes e aditivas · 4. Versionamento e depreciação · 5. Paginação por cursor em detalhe · 6. Segurança no contrato · 7. Gotchas

Validado em 2026-10-10 (modelos Claude 4.x/5.x). Fontes: V-39 (Web API design, Azure Architecture Center, ms.date 2025-03-27, atualizado 2026-06-03; leitura parcial por tópicos), V-40 (api-designer, MIT; RFC 9457 em lugar de 7807), V-41 (system-design-skills, MIT), N-02 (RFC 9457, julho de 2023, Standards Track, obsoleta a RFC 7807), N-03 (rascunho Idempotency-Key, expirado), N-04 (Parallel Change). Semântica de métodos e códigos HTTP vem de conhecimento estável (RFC 9110); a página da Microsoft não foi lida inteira e não se afirma o que ela diz sobre RFC 9457 (V-39). Itens marcados Inferido não foram reabertos em fonte nesta execução.

Responda cada item: sim, não ou Não aplicável (motivo).

## 1. Checklist numerado

**Recursos e nomes**
- [ ] A-01 Coleções com substantivos no plural; hierarquia de até 2 níveis; sem verbos em caminhos CRUD.
- [ ] A-02 Identificadores opacos, estáveis e não sequenciais quando a enumeração for um risco.
- [ ] A-03 Ações fora do CRUD modeladas como recurso (`/orders/{id}/cancellation`) ou sub-recurso, de forma consistente.
- [ ] A-04 Nomes e formatos consistentes: um estilo de caixa em JSON, datas em ISO 8601 UTC, valores monetários sem ponto flutuante (inteiro em centavos ou string decimal), enums documentados.

**Métodos, status e idempotência**
- [ ] A-05 GET sem efeito colateral; PUT e DELETE idempotentes; POST descreve quando cria e quando executa ação.
- [ ] A-06 Criação responde 201 com `Location`; remoção bem-sucedida 204 (ou 200 com corpo, documentado).
- [ ] A-07 POST com efeito (pagamento, pedido) aceita `Idempotency-Key`, com escopo, TTL e comportamento de reuso documentados (convenção, N-03).
- [ ] A-08 Operação demorada responde 202 Accepted com `Location` de um recurso de status (estados, resultado, erro final); polling com `Retry-After` ou webhook.
- [ ] A-09 PATCH: formato declarado (merge patch ou JSON Patch) e semântica de campos ausentes e nulos.

**Coleções**
- [ ] A-10 Paginação por cursor opaco em coleção grande ou volátil; `limit` com padrão e máximo; ordenação estável com desempate por id.
- [ ] A-11 Filtros e ordenação por parâmetros nomeados e documentados; campos sensíveis não filtráveis sem autorização.
- [ ] A-12 Respostas parciais (`fields=`) ou expansão (`expand=`) declaradas, se existirem.
- [ ] A-13 Total de itens opcional ou estimado em coleção grande.

**Erros**
- [ ] A-14 `application/problem+json` (RFC 9457) com `type`, `title`, `status`, `detail`, `instance` e extensões para campos inválidos.
- [ ] A-15 Catálogo de `type` estável e documentado; mensagens não vazam stack trace, SQL nem dados de outros usuários.
- [ ] A-16 Mapeamento de status consistente (seção 2); 429 com `Retry-After`.
- [ ] A-17 Erros de validação listam todos os campos inválidos de uma vez, com ponteiro para o campo.

**Evolução**
- [ ] A-18 Política: mudanças aditivas sem nova versão; quebra exige versão nova ou expand/contract (N-04).
- [ ] A-19 Estratégia de versão escolhida (URI, cabeçalho, tipo de mídia) e implicações de cache registradas (V-39).
- [ ] A-20 Depreciação com aviso, data de remoção e meio de comunicação (seção 4).
- [ ] A-21 Clientes tolerantes: ignoram campos desconhecidos (documentado); enums com valor desconhecido tratados.

**Concorrência e segurança**
- [ ] A-22 Concorrência otimista com `ETag` e `If-Match` (412 em conflito; 428 se o cabeçalho for obrigatório).
- [ ] A-23 Autorização por objeto em todo acesso por id (o usuário pode ver este recurso), não só por rota (OWASP API Security: broken object level authorization; Inferido, lista não reaberta).
- [ ] A-24 Multi-tenant: o tenant vem das credenciais, não de parâmetro livre (V-39 trata APIs multi-tenant).
- [ ] A-25 Nenhum segredo, token ou dado pessoal em URL ou query string (logs e proxies os guardam).
- [ ] A-26 `traceparent` (W3C Trace Context) aceito e propagado; identificador de requisição devolvido.

**Contrato**
- [ ] A-27 Contrato OpenAPI como fonte de verdade, com exemplos de sucesso, erro e página; o usuário roda o lint (comando em `ferramentas-e-mcp.md` do playbook; Não verificável aqui).
- [ ] A-28 Limites declarados: tamanho máximo de corpo, de `limit`, timeouts esperados, rate limit com cabeçalhos informados (a implementação do limite é do backend-api).

## 2. Mapa de status HTTP (convenção; escolha e documente)

| Situação | Status | Observação |
| --- | --- | --- |
| Sucesso com corpo | 200 | |
| Criado | 201 + `Location` | |
| Aceito para processamento assíncrono | 202 + `Location` do status | |
| Sem conteúdo | 204 | DELETE ou PUT sem corpo |
| Requisição malformada (JSON inválido, parâmetro ilegível) | 400 | |
| Não autenticado | 401 | `WWW-Authenticate` quando aplicável |
| Autenticado sem permissão | 403 | Ver política de 404 vs 403 |
| Recurso inexistente | 404 | |
| Método não permitido | 405 | `Allow` |
| Conflito de estado (duplicata, transição inválida, chave de idempotência em andamento) | 409 | |
| Pré-condição falhou (`If-Match`) | 412 | |
| Pré-condição ausente exigida | 428 | |
| Validação semântica (campo inválido) | 422 (ou 400, se a equipe preferir um só) | Convenção; uma regra para toda a API |
| Excesso de requisições | 429 + `Retry-After` | |
| Falha do servidor | 500 | Sem detalhes internos |
| Dependência indisponível | 503 + `Retry-After` | |

Semântica geral dos códigos: RFC 9110 (conhecimento estável; não reaberta nesta execução, Inferido).

## 3. Mudanças quebrantes e aditivas

| Aditiva (sem nova versão) | Quebrante (exige versão ou expand/contract) |
| --- | --- |
| Novo endpoint | Remover ou renomear campo, parâmetro ou endpoint |
| Novo campo opcional na resposta (clientes toleram desconhecidos) | Mudar tipo, formato ou unidade de campo |
| Novo parâmetro opcional de requisição | Tornar obrigatório um campo antes opcional |
| Novo valor de enum **somente** se o contrato já avisa que o conjunto pode crescer | Apertar validação (rejeitar o que era aceito) |
| Novo código de erro documentado no catálogo | Mudar a semântica de um status ou de um `type` de erro |
| | Mudar a ordenação padrão ou o tamanho de página padrão de forma que quebre clientes |

Aditiva só é segura se os clientes forem tolerantes (A-21). Em API pública, assuma que há clientes rígidos.

## 4. Versionamento e depreciação

- Estratégias (V-39): URI (`/v2/orders`), query string, cabeçalho personalizado, tipo de mídia. Cada uma afeta cache, roteamento e facilidade para o cliente; decida uma vez e registre em ADR.
- Expand/contract (N-04): ofereça o novo campo ao lado do antigo; migre clientes; remova o antigo só depois do prazo.
- Sinalização de depreciação: cabeçalho `Sunset` (RFC 8594, conhecimento estável) para a data de desligamento e `Deprecation` (RFC 9745, publicada em 2025; Inferido, não reaberta aqui: confira em rfc-editor.org) mais aviso na documentação e comunicação direta aos consumidores conhecidos.
- Política mínima: duração do suporte (Suposição: defina com o negócio), um ponto de contato, métrica de uso por versão antes de desligar.

## 5. Paginação por cursor em detalhe (conhecimento estável)

Por que não offset em dados vivos: o custo cresce com o deslocamento e, se linhas são inseridas ou removidas entre duas páginas, itens se repetem ou somem.

Cursor: ordenação total por `(created_at DESC, id DESC)`; a página seguinte filtra `(created_at, id) < (último_created_at, último_id)` (comparação de tupla suportada por PostgreSQL e MySQL; adapte em outros SGBDs) e usa índice composto `(created_at, id)`. O cursor devolvido codifica esses dois valores de forma opaca (por exemplo base64 de um JSON), nunca exposto como contrato. Resposta: `{ "items": [...], "next_cursor": "..." | null }`; último item da última página devolve `next_cursor: null`.

Limitações: não permite "ir para a página 50"; o cursor pode expirar se a ordenação mudar; assine ou valide o cursor para impedir adulteração (não é fronteira de segurança, apenas robustez).

## 6. Segurança no contrato

- Autorização por objeto é item de revisão do design; auditoria de segurança detalhada (pentest, SAST) fica com o segmento de segurança.
- Erros iguais para "não existe" e "não tem acesso" quando a existência é sensível.
- Parâmetros de busca nunca recebem dados pessoais (e-mail, CPF) em URL; use POST de busca ou corpo.
- Limite de tamanho de corpo e de `limit` para impedir abuso.

## 7. Gotchas

- O checklist do api-designer (V-40) usava listas MUST/MUST NOT e RFC 7807: foram reescritos em forma positiva e com RFC 9457.
- Lint e mock via `npx` baixam código de terceiros: o plugin só documenta.
- "Como o cliente atual usa" não é contrato: leia o contrato e os logs de uso antes de mudar (Não verificável sem acesso a logs).
- Pagamentos em ponto flutuante e fusos horários implícitos são as duas falhas de formato mais caras; A-04 existe por isso.
