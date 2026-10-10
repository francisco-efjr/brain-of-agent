# Design de ferramentas, MCP e tool use

Conferido em 2026-10-10 · Rótulos: Verificado, Inferido, Suposição, Não verificável · Itens `V-nn` de `docs/dev-segments/research/llm-ai-agents/VALIDATED.md` · O protocolo MCP evolui: confira a versão da especificação (páginas de segurança lidas na revisão 2025-11-25; a página de ferramentas cita 2026-07-28) antes de citar campos.

## Sumário

1. Checklist de ferramenta em 10 itens
2. Exemplo antes/depois
3. Definição de ferramenta MCP
4. Orçamento de tokens com MCP e execução de código
5. Tool use na API Claude
6. Segurança e autorização de servidor MCP
7. Construir um servidor MCP: quatro fases
8. Gotchas

## 1. Checklist de ferramenta (V-05, Verificado)

Fontes: Anthropic, "Writing tools for agents" (2025-09-11) e Apêndice 2 de "Building effective agents" (caminhos absolutos e tempo gasto em tools). Números do artigo vêm de casos internos.

| # | Item | Critério verificável |
| --- | --- | --- |
| 1 | Descrição | Diz quando usar, quando não usar e qual tool usar no lugar; escrita para um colega novo |
| 2 | Escopo | Cobre uma tarefa de alto nível; wrappers crus de endpoint são consolidados |
| 3 | Parâmetros | Nomes inequívocos (`user_id`, não `user`); termos de nicho definidos; um exemplo de chamada correta |
| 4 | Caminhos | Quando o caminho é fonte de erro, exigir caminho absoluto ou outro formato canônico |
| 5 | Saída | Campos legíveis, sem UUID opaco; `response_format` `concise`/`detailed` quando útil (no exemplo do artigo o conciso usou cerca de um terço dos tokens) |
| 6 | Volume | Paginação, filtro e limite de tamanho com padrões sensatos (o Claude Code limita respostas de tool a 25.000 tokens por padrão) |
| 7 | Erro | Diz o que corrigir e mostra a forma correta |
| 8 | Namespace | Por serviço ou recurso; testar prefixo contra sufixo com a avaliação |
| 9 | Avaliação | Tarefas realistas com muitas chamadas; ler transcrições; medir tempo, nº de chamadas, tokens e erros |
| 10 | Escrita | Tools de escrita ou externas pedem confirmação |

## 2. Exemplo antes/depois (ilustrativo)

Antes:

```json
{ "name": "get_data", "description": "Gets data", "input_schema": { "type": "object", "properties": { "user": {"type": "string"}, "q": {"type": "string"} } } }
```

Problemas: nome e descrição genéricos (itens 1, 8), `user` ambíguo (3), sem limite (6), sem orientação de erro (7).

Depois:

```json
{
  "name": "crm_search_orders",
  "description": "Busca pedidos de UM cliente no CRM. Use quando o usuário citar um pedido, uma compra ou um e-mail de cliente. Não use para perguntas de política (responda com a base de conhecimento) nem para listar todos os clientes (use crm_list_customers). Retorna até `limit` pedidos, mais recentes primeiro, com status legível. Se `customer_email` não existir, retorna erro com 'customer_not_found: confira o e-mail ou use crm_list_customers'.",
  "input_schema": {
    "type": "object",
    "properties": {
      "customer_email": { "type": "string", "description": "E-mail exato do cliente, ex.: ana@exemplo.com" },
      "status": { "type": "string", "enum": ["open", "shipped", "delivered", "cancelled"], "description": "Filtro opcional" },
      "limit": { "type": "integer", "description": "1 a 20; padrão 5" },
      "response_format": { "type": "string", "enum": ["concise", "detailed"], "description": "concise: id, status, total; detailed: itens e histórico" }
    },
    "required": ["customer_email"]
  }
}
```

Uma ferramenta de escrita ao lado (`crm_send_email`) deve exigir confirmação humana antes de executar e mostrar a entrada completa antes da chamada (itens 10 e seção 3).

## 3. Definição de ferramenta MCP (V-18, Verificado; página de conceito de tools)

- Dois canais de erro: erro de protocolo e erro de execução com `isError: true` (este é para o modelo se corrigir).
- Nome de 1 a 128 caracteres com letras, dígitos, `_`, `-` e `.` (formulado como SHOULD, não MUST). Nome curto e único; descrição com propósito e limites.
- `inputSchema` é objeto JSON Schema válido; `additionalProperties: false` é recomendado para tool sem parâmetros.
- `structuredContent` acompanhado de texto serializado.
- Ordem de listagem determinística (ajuda cache); sem identificadores opacos na saída.
- Tool com estado: handle explícito, autorização verificada a cada chamada, expiração descrita.
- Tool de escrita: confirmação e exibição da entrada antes de chamar (humano no loop).

## 4. Orçamento de tokens com MCP (V-17, Verificado; Anthropic 2025-11-04)

Conte as definições de tools carregadas; meça os resultados intermediários que passam pelo modelo; filtre e agregue no ambiente de execução; marque campos sensíveis para tokenização antes de chegarem ao modelo; guarde estado em arquivo; execute código gerado somente em sandbox com limites e monitoramento; mantenha poucos servidores MCP. O exemplo de 150.000 para 2.000 tokens (98,7%) é um caso específico: não extrapole. O plugin não fornece o sandbox.

## 5. Tool use na API Claude (V-37, Verificado; conferir página atual)

| Tema | Regra |
| --- | --- |
| Tipos | Tools de cliente (seu app executa; `stop_reason: "tool_use"` e depois `tool_result`) e de servidor (web_search, web_fetch, code_execution, tool_search) |
| `tool_choice` | `auto`, `any`, `tool`, `none`. Para ação obrigatória use `tool_choice`, não só o prompt (instrução aumenta uso, não garante). `any`/`tool` retornam 400 em Opus 5.5, Sonnet 5.5, Fable 5.1 e Mythos 5.1 e com thinking manual: usar `auto` + `strict: true` (Verificado, "Define tools", 2026-10-10) |
| Paralelismo | `disable_parallel_tool_use` em tool de escrita: uma chamada por vez |
| `strict: true` | Garante conformidade ao schema da tool |
| Parâmetro faltante | O Opus tende a pedir o valor; o Sonnet pode inferir ("comportamento não garantido"): valide no código |
| Sobrecarga | O prompt de sistema de tools adiciona 286 a 675 tokens conforme o modelo |

## 6. Segurança e autorização de servidor MCP (V-44, Verificado; especificação 2025-11-25)

Checklist antes de habilitar ou publicar:

- Origem confiável; comando exibido por inteiro, sem truncar, com aprovação; stdio para uso local.
- HTTP: OAuth 2.1 (rascunho) com metadados de recurso protegido (RFC 9728) e 401 com `WWW-Authenticate`; cliente usa PKCE `S256`, recusa continuar se `code_challenge_methods_supported` faltar, envia `resource` (RFC 8707); servidor valida audiência do token.
- Registro de cliente, em ordem: pré-registro, Client ID Metadata Document, registro dinâmico (RFC 7591), pedir ao usuário. (Corrige a ordem do pesquisador.)
- Sem token repassado a APIs de terceiros (token passthrough proibido); token nunca na query string; 403 `insufficient_scope` com repetição limitada.
- Proxy MCP com ID de cliente estático: consentimento por cliente antes de encaminhar (confused deputy); cookie `__Host-` `Secure` `HttpOnly` `SameSite=Lax`; `redirect_uri` por correspondência exata; `state` aleatório, de uso único.
- SSRF na descoberta de metadados: HTTPS fora de loopback, bloquear faixas privadas e link-local (inclui endpoints de metadados de nuvem); a página recomenda não validar IP à mão (encodings alternativos escapam) e considerar proxy de saída; atenção a DNS rebinding.
- Sessões: ID aleatório, vinculado ao usuário, nunca usado como autenticação. URL de autorização: só http/https; rejeitar javascript, data, file, vbscript.
- Escopos: inicial mínimo, elevação incremental, sem coringa. Logs sem segredos. Descrições de tools sem instruções ocultas.
- Plugin que documenta um servidor: informar URL do recurso, escopos mínimos e como revogar; nenhuma credencial embutida.

Servidores de referência (Everything, Fetch, Filesystem, Git, Memory, Sequential Thinking, Time): o README os declara exemplos educativos, não produção; vários antigos foram arquivados; o código não foi lido (91.101 estrelas, commit 2026-10-04). Licença: arquivo LICENSE presente, Apache-2.0/MIT não confirmado.

## 7. Construir um servidor MCP: quatro fases (V-23, destilado do mcp-builder, Verificado)

1. Pesquisa e plano (APIs, tarefas de ponta a ponta, tools de alto nível).
2. Implementação (schemas tipados, erros acionáveis, paginação).
3. Revisão e teste (chamar cada tool; ler a saída).
4. Avaliações: 10 perguntas independentes, somente leitura, com resposta estável, em XML `<evaluation>`/`<qa_pair>`.

A skill `mcp-builder` não tem licença confirmada por arquivo: só destilar. A construção prática pertence a `/automation-integrations:playbook`; aqui ficam os critérios.

## 8. Gotchas

- Wrapper cru de endpoint em vez de tarefa de alto nível.
- Descrição que contém instruções ocultas ao modelo (vetor de injeção).
- Token em query string; confiar nos servidores de referência como produção.
- Esquecer que mudar nome ou descrição de tool invalida o cache de prompt adiante (`rag-custo-observabilidade.md`).
- Citar campos MCP sem conferir a revisão da especificação.
