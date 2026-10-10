# Decisões e trade-offs

Para cada escolha: quando usar, custo, sinal para reconsiderar e fonte. Onde as fontes divergem, a resolução do plugin vem com justificativa (C1 a C15). Decisão material vira ADR curto (`assets/templates/adr-api.md`); decisão pequena vira uma linha no PR. Rótulos: **Verificado** (lido em fonte), **Inferido**, **Suposição**.

## Sumário

- [1. Protocolo: REST, GraphQL, gRPC, tRPC](#1-protocolo-rest-graphql-grpc-trpc)
- [2. Paginação: cursor x offset](#2-paginação-cursor-x-offset)
- [3. Códigos: 400 x 422 e 403 x 404](#3-códigos-400-x-422-e-403-x-404)
- [4. Versionamento e deprecação](#4-versionamento-e-deprecação)
- [5. Síncrono x 202 (operação longa)](#5-síncrono-x-202-operação-longa)
- [6. Teste de contrato: Pact x schema](#6-teste-de-contrato-pact-x-schema)
- [7. Política de idempotência](#7-política-de-idempotência)
- [8. Rate limit: falha aberta x fechada](#8-rate-limit-falha-aberta-x-fechada)
- [9. OpenAPI 3.0, 3.1 ou 3.2](#9-openapi-30-31-ou-32)
- [10. Monólito modular x serviços](#10-monólito-modular-x-serviços)
- [11. Autonomia do agente x migração de dados](#11-autonomia-do-agente-x-migração-de-dados)
- [12. Conflitos entre fontes e resolução](#12-conflitos-entre-fontes-e-resolução)

## 1. Protocolo: REST, GraphQL, gRPC, tRPC

| Opção | Escolha quando | Custo | Reconsidere quando | Fonte |
| --- | --- | --- | --- | --- |
| REST + OpenAPI | API pública ou de parceiros; consumidores diversos; cache HTTP útil; ferramentas de spec, mock e fuzz | Muitas rotas; over/under-fetching; versionamento explícito | Clientes precisam compor dados muito variados por tela | V-11, V-35 |
| GraphQL | Vários clientes (web, mobile) com necessidades de dados diferentes; BFF de produto | Complexidade de autorização por campo, N+1, limites de profundidade e custo; cache HTTP perde força; erro vem com HTTP 200 | Só um cliente, modelo simples | V-30, brain |
| gRPC | Serviço-a-serviço interno, baixa latência, streaming, contrato Protobuf rígido | Navegadores precisam de proxy; depuração exige ferramenta; evolução de `.proto` disciplinada | API pública para terceiros sem toolchain gRPC | V-17, brain |
| tRPC | Cliente e servidor TypeScript no mesmo repositório, sem consumidores externos | Acopla cliente ao servidor; não é contrato para terceiros ou outras linguagens (*Inferido*, sem fonte V) | Surge consumidor não TypeScript | Lacuna declarada |

Regra do plugin: não impor migração de protocolo. Respeite o que o projeto já usa e justifique mudança por problema demonstrado.

## 2. Paginação: cursor x offset

| Opção | Use em | Evite em | Detalhe |
| --- | --- | --- | --- |
| Cursor opaco (`page_token`) | Listas grandes ou mutáveis; feeds; API pública | — | Mesmos filtros entre páginas; token vazio indica fim; token não concede autorização; base64 transparente não é proteção (V-34) |
| Offset/limit | Listas pequenas ou administrativas com ordenação estável e desempate | Lista mutável grande | Offset pula ou duplica itens sob inserção concorrente; custo cresce com o deslocamento (*Inferido*) |

Em qualquer caso: limite padrão e máximo desde o primeiro dia; adicionar depois quebra clientes (V-34). `total_size` é opcional e pode ser estimativa.

## 3. Códigos: 400 x 422 e 403 x 404

- **400 x 422:** o defeito é a inconsistência. Default sugerido: 400 para sintaxe ou tipo malformado, 422 para regra semântica violada. Se o framework já emite 422 para validação, mantenha e documente (*Inferido*; brain). Registre a tabela no OpenAPI.
- **403 x 404 para recurso alheio:** com ID previsível ou existência sensível, a resposta de "existe mas não é seu" deve ser indistinguível de "não existe" (mesmo status, mesmo formato, mesmo tempo aproximado). Use 403 só quando a existência não é segredo (V-09 API1, brain).
- **401 x 403:** 401 é "não sei quem é você" (com `WWW-Authenticate`); 403 é "sei quem é, não pode".

## 4. Versionamento e deprecação

| Estratégia | Característica | Observação |
| --- | --- | --- |
| Versão no caminho (`/v2/...`) | Visível, simples de rotear | Prática comum |
| `api-version` na query, sem versão no caminho | Convenção específica da Azure (V-35), data-versionada | Não é regra geral |
| Cabeçalho de versão | Limpa a URL | Pior para cache e depuração (*Inferido*) |

O plugin exige: **uma única estratégia por API, declarada no ADR**; nenhuma quebra dentro de uma versão; descontinuação sinalizada (`Deprecation`, `Sunset`) com data e substituto (`assets/templates/aviso-de-deprecacao.md`); depreciar antes de remover, também em GraphQL (V-30) e `reserved` em Protobuf (brain). Não prescreve caminho x query (conflito C3).

## 5. Síncrono x 202 (operação longa)

Responda de forma síncrona quando a operação termina dentro do orçamento do cliente (a convenção Azure usa p99 abaixo de ~1 s como limite, V-35). Acima disso: `202 Accepted` com URL de monitoramento e `Retry-After`; o monitor persiste por tempo documentado (Azure: no mínimo 24 h); estados terminais (`succeeded`, `failed`, `canceled`); a criação do job é idempotente. 202 nunca significa concluído (AB-19).

## 6. Teste de contrato: Pact x schema

| Situação | Escolha |
| --- | --- |
| Serviços internos, os dois lados sob seu controle, consumidores usando partes diferentes da API | Pact: mostra quem usa o quê e bloqueia o deploy que quebraria alguém |
| API pública ou de parceiros, consumidores desconhecidos | OpenAPI como fonte da verdade + Schemathesis/Prism + diff de spec |
| Time sem disciplina de broker e versionamento | Comece por schema; Pact mal operado vira contrato velho que ninguém verifica |

Os dois se complementam: conformidade com schema não diz quais campos os consumidores usam; o Pact não cobre consumidor que não escreveu contrato (brain, MIT). Dredd foi arquivado em 08/11/2024 (Verificado em 2026-10-10 no GitHub): não use em projeto novo.

## 7. Política de idempotência

Não há padrão publicado vencedor: o draft do header expirou em 18/04/2026 (V-16). Escolha e documente (`assets/templates/politica-de-idempotencia.md`).

| Família | Comportamento | Quando |
| --- | --- | --- |
| Stripe v1 (V-15) | Chave do cliente; salva a primeira resposta (inclusive 500); erro se parâmetros diferem; validação que falha e conflito concorrente não são salvos; retenção mínima de 24 h | API de pagamentos; compatibilidade com clientes Stripe-like |
| AIP-155 (V-15) | `request_id` no corpo (UUID, 36 caracteres); duplicata devolve o sucesso anterior ou o estado atual | APIs no estilo Google/gRPC |
| Draft-07 (V-16, expirado) | 400 se a chave exigida falta; 422 se corpo diverge; 409 se em processamento | Referência para códigos |
| Azure (V-35) | `Repeatability-Request-ID` + `Repeatability-First-Sent`; janela mínima 5 min; 501 se não suporta | Ecossistema Azure |

Default do plugin (PR-04, conflito C5): header `Idempotency-Key`, hash do corpo, 422 se corpo diverge, 409 se em processamento, 400 se ausente ou malformado, falha de validação não consome a chave. Sempre rotule como **Suposição** quando o usuário não decidiu.

## 8. Rate limit: falha aberta x fechada

Quando o armazenamento do limite (por exemplo Redis) cai: **fail-open** (deixa passar) em rotas de baixo risco como formulário de contato; **fail-closed** (bloqueia) em login, reset e pagamento. A fonte é um blog (classe C, V-33): trate como heurística e decida por rota com o dono do produto. A chave do limite vem de credencial validada (identidade + plano + endpoint), nunca de header livre.

## 9. OpenAPI 3.0, 3.1 ou 3.2

3.1.x segue a base mais suportada por ferramentas (*Inferido*) e alinha com JSON Schema; existem 3.2.0 e 3.2.1 (V-11, correção 8). Default: 3.1.x, salvo se Spectral, Redocly, gerador de cliente ou gateway do projeto exigir outra; confira a versão suportada antes de atualizar "por ser a mais recente" (brain). O prompt original da GitHub gerava 3.0.3 (V-32): diferença consciente, não erro.

## 10. Monólito modular x serviços

Fora do escopo profundo deste plugin: use `/architecture-design:playbook`. Regra mínima daqui: comece pelo padrão existente; separar serviço exige problema demonstrado (escala, equipe, ciclo de deploy); sem microsserviços por moda e sem números de capacidade inventados (A2 `backend-architect`).

## 11. Autonomia do agente x migração de dados

O brain permite implementar e testar com autonomia dentro do escopo; V-38 manda o humano executar migrações. Resolução (C13): o agente **escreve** a migração e a roda **somente contra banco de teste local**; staging e produção são do humano, com autorização concreta. Backup e restauração são verificados em ambiente isolado, nunca por cima do banco ativo (brain). Modelagem física, índices e expand/contract detalhado: `/database-data-modeling:playbook`.

## 12. Conflitos entre fontes e resolução

| # | Conflito | Resolução |
| --- | --- | --- |
| C1 | 400 x 422 | Seção 3 |
| C2 | 403 x 404 | Seção 3 |
| C3 | Versionamento por query (Azure) x caminho | Seção 4 |
| C4 | Rate limit: o security-review exclui "DoS genérico"; OWASP API4 inclui | Em **design/revisão de serviço** é achado API4. Em **revisão de diff**, só quando o diff remove ou omite limite em endpoint sensível com cenário concreto (V-08 x V-09) |
| C5 | Política de idempotência | Seção 7 |
| C6 | OpenAPI 3.0.3 x 3.1 x 3.2 | Seção 9 |
| C7 | Regras sempre carregadas de ~1.000 linhas x CLAUDE.md curto | Checklists longos viram `references/` sob demanda; CLAUDE.md abaixo de 200 linhas (bloco do plugin até 60) |
| C8 | Tom absoluto (CAPS, "Iron Law") x tom calmo | Reescrever com o porquê e a alternativa; ênfase só em invariante de segurança |
| C9 | Subagentes sem `tools` x `tools` mínimos | `tools` explícitos; revisores sem Write/Edit; não depender de `permissionMode`, que é ignorado em plugin (V-05) |
| C10 | Offset x cursor | Seção 2 |
| C11 | Fail-open x fail-closed | Seção 8 |
| C12 | HATEOAS como critério | Fora; só vocabulário |
| C13 | Autonomia x migração | Seção 11 |
| C14 | mcp-builder recomenda TypeScript | Usar só o workflow de 4 fases e as 10 perguntas; a stack segue o projeto |
| C15 | Limites numéricos (400/600 linhas, 80% de confiança, "45 endpoints") | Excluídos: opinião ou não verificados; confiança vira escala 1 a 10 do relatório (`assets/templates/relatorio-de-revisao-api.md`), sem limiar mágico |

Ressalvas sem conflito: RFC 9700 define implicit como SHOULD NOT (só password grant é MUST NOT); AIP-155 não obriga documentar a retenção (documentar é boa prática, *Inferido*); RFC 8725 não trata `exp`/`nbf`; Spring não valida `aud` por padrão.

Validado em 2026-10-10.
