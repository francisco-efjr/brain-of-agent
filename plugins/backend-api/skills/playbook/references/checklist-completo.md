# Checklist completo de backend e APIs

Use como grade de revisão e de teste. Cada tabela traz o critério verificável; o ID `V-nn` aponta para `fontes.md`. Tabelas 1 a 3 vêm do brain-of-agent (conteúdo próprio do usuário, MIT), enriquecidas com as fontes validadas. Rótulos: **Verificado** (lido na fonte), **Inferido** (conhecimento estável ou leitura sua), **Suposição**, **Não verificável**.

## Sumário

- [1. Checklist por endpoint](#1-checklist-por-endpoint)
- [2. Status HTTP esperados e confusões](#2-status-http-esperados-e-confusões)
- [3. Checklist de serviço (nove itens)](#3-checklist-de-serviço-nove-itens)
- [4. Grade OWASP API Top 10 (2023)](#4-grade-owasp-api-top-10-2023)
- [5. Hardening REST por tópico](#5-hardening-rest-por-tópico)
- [6. Checklist de contrato OpenAPI](#6-checklist-de-contrato-openapi)
- [7. Gates por fase](#7-gates-por-fase)

## 1. Checklist por endpoint

Status 200 não prova nada: `200 {"erro": "..."}` e dado gravado errado passam nesse teste. Priorize pelo risco (dinheiro, dado de terceiros, operação irreversível).

| Aspecto | O que verificar |
| --- | --- |
| Status e corpo | Status exato, não "2xx". Valores de negócio conferidos contra oráculo independente (total calculado à parte, dado semeado), nunca copiados da resposta |
| Schema | Na resposta, aceitar campo novo (não é quebra), mas conferir que campo sensível não vaza (`senha_hash`, CPF completo, dado interno). Dinheiro como string decimal ou centavos inteiros, nunca float; datas ISO 8601 com fuso |
| Headers | `Content-Type` correto (`application/problem+json` nos erros); `Cache-Control: no-store` em dado pessoal; `Location` no 201; `Allow` no 405; sem versão em `Server`/`X-Powered-By`; HSTS e `X-Content-Type-Options: nosniff` |
| CORS | Só origens da lista; nunca refletir qualquer `Origin` com `Access-Control-Allow-Credentials: true`; preflight `OPTIONS` coerente |
| Erro (RFC 9457) | `type` (URI que identifica o erro), `title`, `status` igual ao HTTP, `detail`, `instance` e extensões (campos inválidos). Mesmo formato em todos os endpoints; sem stack trace, SQL ou hostname. JSON malformado vira 400 nesse formato, não 500 |
| Idempotência | `PUT`/`DELETE` repetidos deixam o mesmo estado (o 2º `DELETE` pode dar 204 ou 404, conforme o contrato). `POST` com chave: mesma chave e corpo, mesma resposta, sem novo efeito. Códigos para chave reutilizada com outro corpo (422), original em curso (409) e chave ausente (400) são opção do draft expirado (V-16): o projeto decide e documenta |
| Paginação | `limit` padrão, máximo, 0, negativo, máximo+1, 10^9 (recusar com 400 ou limitar; nunca 500 nem "tudo"); última página sem "próximo"; página além do fim devolve lista vazia com 200; cursor adulterado devolve 400; ordenação com desempate (`criado_em, id`), senão itens repetem ou somem |
| Filtros e ordenação | Combinações; sem resultado devolve lista vazia; acento e caixa ("joão" x "Joao"); fim de intervalo de data inclusivo e no fuso certo; campo de ordenação fora da lista permitida devolve 400 (vetor de injeção) |
| Validação | Obrigatório ausente; `null` x ausente (em `PATCH`, `null` limpa e ausente não mexe); tipo errado; tamanhos; Unicode; corpo enorme devolve 413. Campo extra: o contrato diz se rejeita ou ignora, nunca aplica (`{"papel": "admin"}` ou `{"preco": 0}` é atribuição em massa) |
| AuthN x AuthZ | Sem token, expirado, assinatura inválida, `alg: none`, token de outro ambiente: 401. Válido sem o escopo: 403. Recurso de outro usuário ou tenant: 404 (ou 403 se a existência não for segredo); listagens não trazem itens alheios |
| Rate limit | Acima do limite: 429 com `Retry-After`; limite por cliente, não global. Testar só em ambiente isolado |
| Versionamento | Versão anterior funciona enquanto houver consumidor; descontinuação sinalizada com `Deprecation` e `Sunset` (RFCs 9745 e 8594, Verificado em 2026-10-10). Quebras: remover ou renomear campo, mudar tipo, tornar obrigatório campo de entrada, **novo valor de enum na resposta** (quebra `switch` exaustivo no consumidor) |
| Concorrência otimista | `GET` devolve `ETag`; `If-Match` desatualizado devolve 412; ausência quando exigido devolve 428; conflito de regra (transição inválida, chave única) devolve 409. Nunca atualização perdida em silêncio |
| Tempo de resposta | Teto folgado (por exemplo 2 s) só para pegar travamento; percentis ficam no teste de performance, porque teto apertado gera intermitência |
| Efeito colateral | Depois do `POST`, o `GET` devolve o mesmo dado; a linha certa está no banco; o evento saiu **uma vez** com o payload certo. E o inverso: requisição recusada não deixa registro pela metade |

## 2. Status HTTP esperados e confusões

| Status | Esperado quando | Confusão comum |
| --- | --- | --- |
| 200 | leitura; atualização que devolve o recurso; ação que não cria nada | `200` com erro no corpo |
| 201 | `POST`/`PUT` que criou recurso, com `Location` | `200` na criação; falta `Location` |
| 202 | processamento assíncrono aceito e ainda não feito; indica onde consultar | tratar 202 como concluído |
| 204 | sucesso sem corpo (`DELETE`, `PUT` sem retorno) | 204 com corpo |
| 400 | requisição malformada: JSON inválido, tipo errado | ver 422 |
| 401 | sem credencial ou credencial inválida/expirada, com `WWW-Authenticate` | 401 para "sem permissão" |
| 403 | autenticado, sem permissão | 403 para token expirado |
| 404 | não existe, ou existe e o chamador não pode saber | 403 em ID alheio revela que o ID existe |
| 405 / 406 / 415 | método não suportado (com `Allow`) / `Accept` impossível / `Content-Type` não suportado | 500 ou 400 genérico |
| 409 | conflito com o estado atual: duplicidade, transição inválida | 409 para erro de validação |
| 412 / 428 | `If-Match` desatualizado / pré-condição exigida e ausente | 409 genérico para os dois |
| 413 | corpo acima do limite | 500 por estouro de memória |
| 422 | sintaxe válida, regra violada (fim antes do início, CPF com dígito errado) | ver abaixo |
| 429 | limite de taxa, com `Retry-After` | 503 sem dizer quando voltar |
| 500 | nunca é o esperado para entrada do cliente | "aceitável porque o dado era inválido" |
| 502 / 503 / 504 | falha de dependência ou gateway; 503 com `Retry-After` em manutenção | — |

**400 x 422:** o defeito é a inconsistência, não a escolha (FastAPI usa 422 para validação por padrão; Spring usa 400). Siga a tabela do projeto e cobre a mesma regra em todos os endpoints. **404 x 403 para recurso alheio:** com ID previsível ou existência sensível (pedido, paciente), "existe mas não é seu" deve ser indistinguível de "não existe": mesmo status, mesmo formato de corpo. Métodos HTTP têm propriedades distintas; idempotência de método não substitui chave de operação de negócio; nunca use `GET` para ação destrutiva (MDN, consultado pelo brain em 2026-10-09).

## 3. Checklist de serviço (nove itens)

- [ ] Consumidores e contratos existentes identificados.
- [ ] Schemas cobrem erro, sucesso, vazio e limites; serializers reais verificados.
- [ ] Autorização por objeto, tenant e ação ocorre no servidor.
- [ ] Chave idempotente tem escopo, fingerprint, atomicidade e política de expiração.
- [ ] Timeouts e retries têm limite e classificação de erro.
- [ ] Webhook ou fila suporta duplicação, ordem e falha de processamento.
- [ ] Mudança compatível, ou migração de consumidores planejada.
- [ ] Integração real em ambiente permitido difere de mock explicitamente.
- [ ] Evidência mostra regra correta, e não apenas HTTP 200.

Revalidar: payload antigo e novo, chamada duplicada concorrente, perda de resposta após aceitação, tenant errado, limite de paginação, fornecedor lento, evento repetido. Não executar carga ou mutação contra sistema externo sem escopo autorizado.

## 4. Grade OWASP API Top 10 (2023)

Fonte: V-09 (títulos *Verificado*; textos de prevenção por risco não foram lidos em detalhe, então a coluna "Procure por" é heurística *Inferida*). Responda cada linha com evidência `arquivo:linha` ou "Não verificado". Regex acha candidato, só leitura confirma achado.

| ID | Risco | Pergunta de revisão | Procure por |
| --- | --- | --- | --- |
| API1 | Autorização quebrada em nível de objeto (BOLA) | Todo acesso a objeto por ID checa o dono ou o tenant? | consulta `WHERE id = ?` sem `owner_id`/`tenant_id`; ID vindo de path, query ou corpo usado direto |
| API2 | Autenticação quebrada | O token é validado de verdade (assinatura, `iss`, `aud`, `exp`)? Login tem limite de tentativas? | `verify=False`, `algorithms` vindo do header, segredo fixo, ausência de rate limit em login e reset de senha |
| API3 | Autorização quebrada em nível de propriedade (BOPLA) | A resposta devolve só as propriedades permitidas e a entrada só aceita as permitidas? | retorno do modelo ORM inteiro, `**request.json` em `update`, ausência de DTO de saída |
| API4 | Consumo irrestrito de recursos | Há limite de taxa, de tamanho de corpo, de página e de custo? | listas sem `limit`, upload sem teto, consulta GraphQL sem profundidade máxima, ausência de timeout |
| API5 | Autorização quebrada em nível de função (BFLA) | Rotas administrativas exigem papel no servidor? | rota `/admin` só escondida no front, guard ausente em método `DELETE`/`PUT` |
| API6 | Acesso irrestrito a fluxos de negócio sensíveis | O fluxo (compra, cupom, cadastro) resiste a automação e repetição? | cupom sem limite por conta, fluxo sem verificação de etapa anterior |
| API7 | SSRF | Toda URL remota controlada pelo cliente passa por allowlist e proteção de rede? | `requests.get(url_do_usuario)`, webhooks de saída, importação por URL, redirects seguidos |
| API8 | Configuração incorreta de segurança | Headers, CORS, erros, debug e TLS estão corretos? | `Access-Control-Allow-Origin` refletido, stack trace em resposta, `DEBUG=true`, métodos HTTP supérfluos |
| API9 | Gestão inadequada de inventário | Versões antigas, endpoints de teste e hosts de homologação estão catalogados e desativados? | `/v0`, `/internal`, `/debug`, spec fora de sincronia com as rotas reais |
| API10 | Consumo inseguro de APIs | Respostas de terceiros são validadas como entrada não confiável? | `response.json()` usado sem schema, seguir redirect de fornecedor, confiar em campo de preço vindo de parceiro |

Em **revisão de diff de PR**, reporte API4 só quando o diff remove ou omite limite em endpoint sensível (login, pagamento, envio) com cenário concreto; "DoS genérico" sem impacto fica de fora (V-08 x V-09, conflito C4 em `decisoes-e-tradeoffs.md`).

## 5. Hardening REST por tópico

Fonte principal: V-10 (*Verificado*), com RFC 9700/8725 em `autenticacao-seguranca.md`.

| Tópico | Regra |
| --- | --- |
| Transporte | Apenas HTTPS; HSTS; endpoints de gestão fora da internet pública |
| Controle de acesso | Em cada endpoint, no servidor; allowlist de métodos com 405 |
| JWT | Nunca `alg: none`; algoritmo fixado no servidor, não pelo header do token; validar `iss`, `aud`, `exp` (e `nbf` quando necessário); `jti` para revogação |
| API key | Em toda requisição, sobre TLS; 429 em excesso; sozinha não protege recurso sensível |
| Validação | Tipo, tamanho, faixa e formato; limite de corpo (413); `Content-Type` (415) e `Accept` (406) verificados |
| Fluxos | Impedir execução fora de ordem em fluxo de várias etapas |
| Erros | Genéricos para o cliente; detalhes só em log protegido; sem stack trace |
| Headers | `Cache-Control: no-store` em resposta sensível; `X-Content-Type-Options: nosniff`; HSTS |
| CORS | Origens explícitas; nunca refletir `Origin` com credenciais |
| Segredos | Nunca credenciais em URL; nunca segredo em log, teste ou resposta |

## 6. Checklist de contrato OpenAPI

Fonte: V-11, V-14, V-32, V-35. Versão-alvo 3.1.x salvo ferramenta do projeto que exija outra; existem 3.2.0 e 3.2.1 (confirme o que o validador do projeto suporta, *Inferido*).

- [ ] `openapi` e `info` presentes, mais ao menos um entre `paths`, `components`, `webhooks`.
- [ ] `security` explícita por operação: `security` global é lista de alternativas (basta satisfazer uma; `{}` torna opcional); a da operação substitui a global; `[]` remove. Operação pública sem `security: []` herda a global por engano.
- [ ] Respostas de sucesso e de erro por operação; erro em `application/problem+json` com componente reutilizável.
- [ ] Exemplos realistas conferidos contra os serializers reais.
- [ ] Parâmetros tipados com limites (`maximum`, `maxLength`, `enum` fechado); paginação documentada.
- [ ] Regra que o código não mostra marcada como "a confirmar", sem inventar regra de negócio.
- [ ] Handlers com tipo genérico (`any`) listados em vez de inferidos.
- [ ] Validador de spec do projeto executado e saída colada; sem validador instalado, declarar **Não verificado**.

## 7. Gates por fase

| Fase | Saída necessária para avançar |
| --- | --- |
| Entendimento | Stack e versão confirmadas, consumidores listados, fontes de requisito e contrato identificadas, conflitos expostos |
| Plano | Fatia vertical, contrato, riscos e oráculos definidos (`assets/templates/plano-de-incremento-api.md`) |
| Implementação | Mudança no escopo; validação, autorização, erro, idempotência e paginação tratados pelo risco; APIs conferidas na versão instalada |
| Validação | Tipos, testes, lint e validação da spec executados; negativos de authz, validação, duplicata e concorrência; saída colada |
| Revalidação | Reprodução original repetida; regressões por impacto; evidência anterior invalidada por mudança nova foi refeita |
| Entrega | Artefatos, comandos, rótulos, limitações, riscos residuais e próximo passo (`assets/templates/handoff-checkpoint.md`) |

Resultado: **concluído no escopo**, **parcial** (falta leitura, acesso, execução ou revalidação material) ou **impedido** (condição e próximo passo descritos). Falha crítica impede recomendação favorável; média de notas não a compensa.

Validado em 2026-10-10. Confira versões e flags na versão instalada antes de copiar comandos.
