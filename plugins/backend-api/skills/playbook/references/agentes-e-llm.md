# Tools para agentes e integração com a API de um modelo

Referência para `agent-tool-design`. Recorte: tools e endpoints **do lado do serviço** (expor um backend existente a um agente; endpoints que chamam um modelo). Arquitetura de agentes, RAG, evals de modelo e memória ficam em `/llm-ai-agents:playbook`. Fontes: V-01, V-02, V-03, V-06, V-07, V-28 (`fontes.md`). Tabelas de compatibilidade por modelo, IDs de modelo e limites mudam: **confira a doc oficial atual** (`https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools`) antes de afirmar. Se o projeto usa outro provedor, não adicione chamadas Anthropic (V-07).

## Sumário

- [1. Checklist de tool ou endpoint para agente](#1-checklist-de-tool-ou-endpoint-para-agente)
- [2. Descrição em quatro frases](#2-descrição-em-quatro-frases)
- [3. Schema estrito e exemplos](#3-schema-estrito-e-exemplos)
- [4. Resposta enxuta e erro acionável](#4-resposta-enxuta-e-erro-acionável)
- [5. Anotações MCP](#5-anotações-mcp)
- [6. Avaliação de dez perguntas](#6-avaliação-de-dez-perguntas)
- [7. Endpoint que chama a API do modelo](#7-endpoint-que-chama-a-api-do-modelo)
- [8. Scripts e ferramentas para agentes](#8-scripts-e-ferramentas-para-agentes)

## 1. Checklist de tool ou endpoint para agente

Destilado de V-01 (Anthropic Engineering, 11/09/2025):

- [ ] Uma operação por **fluxo de negócio**, não por tabela ou por endpoint REST espelhado.
- [ ] Nome com prefixo de serviço/recurso (`orders_search`); decida prefixo x sufixo por avaliação, o texto original não prescreve um. Parâmetros sem ambiguidade (`user_id`, não `user`).
- [ ] Resposta enxuta; modo conciso por padrão e detalhado sob pedido, mantendo os IDs necessários para a chamada seguinte.
- [ ] Paginação, filtros e **limite padrão**; ao truncar, a resposta diz como refinar a busca.
- [ ] Erro diz o que corrigir e mostra um exemplo de entrada válida.
- [ ] Avaliação com tarefas realistas de várias chamadas; medir acerto, número de chamadas, tokens e erros; ler as transcrições.
- [ ] O limite de 25.000 tokens vale **por padrão no Claude Code**; não é regra geral de outros clientes.

## 2. Descrição em quatro frases

V-02: a descrição é "o fator mais importante" do desempenho de uma tool, com pelo menos 3 a 4 frases. Molde:

1. O que faz e o que retorna.
2. Quando usar.
3. Quando **não** usar (e qual tool usar nesse caso).
4. Efeito de cada parâmetro e limitações.

Antes e depois:

```text
Antes:  "Busca pedidos."
Depois: "Busca pedidos do cliente autenticado e devolve até `limit` itens com id, status e total
         (use response_format=detailed para incluir itens). Use para localizar pedidos por status ou
         período. Não use para ler um pedido já conhecido (use orders_get) nem para alterar pedidos.
         `status` aceita apenas os valores do enum; `limit` padrão 20, máximo 100; datas em ISO 8601."
```

O nome segue `^[a-zA-Z0-9_-]{1,128}$` (V-02). Consolidar ações com um parâmetro `action` é uma opção documentada.

## 3. Schema estrito e exemplos

Verificado em V-03: `strict: true` no nível da tool (ao lado de `name`, `description`, `input_schema`); o exemplo oficial usa `additionalProperties: false`; amostragem restrita por gramática; schemas compilados ficam em cache por até 24 h desde o último uso; **não coloque PHI** em nomes de propriedade, enum, const ou regex; toolsets de computer use e browser use não aceitam `strict`. O subconjunto de JSON Schema suportado fica na página de structured outputs (não lida: *Não verificado*).

Regra do plugin: tools que **mutam estado** usam `strict: true`, `additionalProperties: false`, enums fechados e `required` explícito. `input_examples` precisam **validar contra o schema** (senão a API devolve 400) e custam tokens (V-02: cerca de 20 a 50 para exemplos simples, 100 a 200 para aninhados); campo complexo sem exemplo válido é suspeito.

```json
{
  "name": "orders_cancel",
  "description": "Cancela um pedido do cliente autenticado e devolve o pedido com status 'canceled'. Use quando o cliente pedir cancelamento explícito de um pedido ainda não enviado. Não use para devolução (orders_return) nem para pedidos já enviados; nesse caso responde erro 'not_cancelable' com o próximo passo. 'order_id' é o UUID do pedido; 'reason' é opcional, até 200 caracteres.",
  "strict": true,
  "input_schema": {
    "type": "object",
    "properties": {
      "order_id": { "type": "string", "format": "uuid" },
      "reason": { "type": "string", "maxLength": 200 }
    },
    "required": ["order_id"],
    "additionalProperties": false
  },
  "input_examples": [{ "order_id": "7f6c2a1e-0000-4000-8000-000000000001", "reason": "comprei por engano" }]
}
```

Confirme os nomes de campos na doc atual antes de publicar; palavras-chave como `format` e `maxLength` podem não fazer parte do subconjunto aceito com `strict` (*Não verificado*): se a API recusar o schema, remova-as e valide no servidor. **`tool_choice`:** segundo V-02, `any` e `tool` retornam 400 em Opus 5.5, Sonnet 5.5, Fable 5.1 e Mythos 5.1 (use `auto` com `strict`); a tabela muda por modelo, confira na hora. Peça "explicação", não "raciocínio", no texto da tool (risco de recusa `reasoning_extraction`, V-02).

## 4. Resposta enxuta e erro acionável

```json
{
  "type": "https://api.exemplo.com.br/erros/not-cancelable",
  "title": "Pedido não pode ser cancelado",
  "status": 409,
  "detail": "O pedido 7f6c... já foi enviado. Para devolver, use orders_return com este order_id. Exemplo de entrada válida: {\"order_id\": \"7f6c2a1e-0000-4000-8000-000000000001\"}."
}
```

O erro orienta o agente a corrigir a chamada; nunca devolve stack trace nem dado sensível (os agentes decidem retry pelo erro). Respostas truncadas indicam como refinar (`filtre por status ou período`). Mantenha IDs na resposta concisa para encadear chamadas.

## 5. Anotações MCP

Do workflow do mcp-builder (V-06, Apache-2.0 na skill, destilado): `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint` descrevem o efeito da tool para o cliente; nomes de ação com prefixo; quatro fases: (1) pesquisa e plano, (2) implementação com utilitários compartilhados e anotações, (3) revisão e teste com inspetor, (4) avaliações. A skill original recomenda TypeScript; no seu projeto a stack segue o projeto (C14). O servidor MCP de **terceiros** é supply chain: ver `ferramentas-e-mcp.md`.

## 6. Avaliação de dez perguntas

Molde de V-06 (`assets/templates/avaliacao-10-perguntas.md`): dez pares pergunta-resposta, cada um **independente**, **somente leitura**, **complexo** (várias chamadas), **realista**, **verificável por comparação de string** e **estável** no tempo. Execute o agente com as tools, meça acerto, número de chamadas, tokens e erros, e **leia as transcrições** para achar tools confusas. Separe um conjunto de teste para não ajustar descrições ao conjunto de avaliação (V-01). Sem execução, rotule "avaliação desenhada, não executada".

## 7. Endpoint que chama a API do modelo

Checklist (V-07, anthropics/skills `claude-api`; a skill é amplamente aplicável mas o repositório não tem licença única, então destile):

- [ ] Use o **SDK oficial da linguagem**; não invente assinatura de método; confira na versão instalada.
- [ ] **ID de modelo** da tabela oficial atual (sem sufixo de data quando a doc assim indicar); IDs envelhecem, não os fixe no plugin.
- [ ] Verifique `stop_reason` (`max_tokens`, `refusal`) **antes** de executar tools.
- [ ] Devolva **todos** os `tool_result` de um turno numa **única** mensagem.
- [ ] **Valide cada entrada de tool** contra o schema antes de executar (saída do modelo é dado não confiável: nunca vire SQL, shell ou URL sem validação — AB-25).
- [ ] **Streaming** para saídas longas ou entradas grandes (evita timeouts).
- [ ] Cache por prefixo do prompt; confira `usage.cache_read_input_tokens` para saber se funcionou.
- [ ] Segredo da API só em variável de ambiente ou cofre; nunca no cliente nem em log.
- [ ] Timeout, tentativas limitadas e idempotência no seu endpoint (o cliente repete; o modelo cobra tokens a cada tentativa).
- [ ] Limite de entrada e rate limit **por usuário** no seu endpoint (API4): o custo é seu.
- [ ] Antes de adicionar chamada Anthropic a arquivo de outro provedor: pare e pergunte.

## 8. Scripts e ferramentas para agentes

V-28 (Armin Ronacher, 12/06/2025; classe C, opinião de autor): ferramentas rápidas e de saída curta; travar é pior que falhar (timeout); erro que orienta o próximo passo; pidfile/lock contra segunda execução; log em arquivo de caminho fixo além do terminal; comandos críticos como alvos de Makefile; MCP só quando o script não resolve.

```make
# Exemplo de alvo para agente: verificação em ordem, falha rápida, saída curta
verify:
	@echo "== tipos ==" && timeout 120 mypy app 2>&1 | tail -n 20
	@echo "== testes ==" && timeout 300 pytest -q -x 2>&1 | tail -n 30
	@echo "== lint ==" && timeout 60 ruff check app 2>&1 | tail -n 20
	@echo "== spec ==" && timeout 60 spectral lint openapi.yaml 2>&1 | tail -n 20 || echo "spectral ausente: spec NÃO verificada"
```

Substitua pelos comandos reais do projeto (*Inferido*; Spectral só se instalado). Prefira o script do repositório a instalar ferramenta nova.

Validado em 2026-10-10 · modelo-alvo: claude-sonnet-5-5.
