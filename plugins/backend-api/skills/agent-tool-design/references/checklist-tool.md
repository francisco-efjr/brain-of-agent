# Checklist de tool/endpoint para agente

Fontes (Verificado em 2026-10-10 salvo indicação): Anthropic Engineering "Writing tools for agents" (V-01, https://www.anthropic.com/engineering/writing-tools-for-agents, 11/09/2025); Claude API "Define tools" (V-02, https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) e "Strict tool use" (V-03, .../strict-tool-use); `mcp-builder` de anthropics/skills (V-06, LICENSE da skill Apache-2.0; destilado, não copiado); Armin Ronacher, "Agentic coding" (V-28, classe C, opinião de autor). A licença do texto de V-01/V-02/V-03 não é declarada: tudo aqui é redação própria.

## Sumário

1. Checklist
2. Descrição em quatro frases
3. Schema, strict e exemplos
4. Padrões antes e depois
5. Anotações MCP
6. Avaliação de 10 perguntas
7. Scripts e CLIs para agentes
8. Itens que mudam com o tempo

## 1. Checklist

```
[ ] uma operação por fluxo de negócio, não por tabela
[ ] nome com prefixo de serviço/recurso; parâmetros sem ambiguidade (customer_id, não user)
[ ] resposta enxuta; modo concise por padrão, detailed sob pedido (mantendo IDs para a chamada seguinte)
[ ] paginação + limite padrão; ao truncar, dizer como refinar a busca
[ ] erro diz o que corrigir e mostra um exemplo de entrada válida
[ ] descrição de 3 a 4 frases (o que faz, quando usar, quando não usar, parâmetros e limites)
[ ] tool que muda estado: strict, additionalProperties:false, enum fechado, required explícito
[ ] avaliação: tarefas realistas de várias chamadas; medir acerto, nº de chamadas, tokens, erros; ler as transcrições
```

(Os seis primeiros itens são o checklist de V-01; os dois últimos somam V-02, V-03.)

## 2. Descrição em quatro frases

Modelo (V-02): (1) o que faz e o que retorna; (2) quando usar; (3) quando **não** usar; (4) efeito de cada parâmetro e limitações. A descrição é o fator mais importante do desempenho da tool, com pelo menos 3 a 4 frases.

Exemplo, tool de cancelamento (muta estado):

> Cancela um pedido ainda não enviado e devolve o pedido atualizado (id, status, valor estornado). Use quando o cliente pedir cancelamento explícito e o status for PENDING ou PAID. Não use para pedidos SHIPPED (retorna erro `not_cancellable`; oriente devolução) nem para consultar status (use `orders_get`). `order_id` é o UUID do pedido; `reason` é obrigatório, até 200 caracteres, e fica no histórico; a operação é idempotente por `order_id`.

## 3. Schema, strict e exemplos

- `strict: true` fica no nível da tool, ao lado de `name`, `description` e `input_schema` (V-03). A amostragem é restrita por gramática; schemas compilados ficam em cache por até 24 h desde o último uso.
- Não coloque PHI em nomes de propriedade, enum, const ou regex (V-03).
- Toolsets de computer use e browser use não aceitam `strict` (V-03).
- O subconjunto de JSON Schema suportado em modo estrito está na página de structured outputs, **não lida**: não presuma suporte a `minimum`, `maximum`, `pattern` ou `default`; declare limites também na descrição e valide no servidor.
- `input_examples` precisam validar contra o schema, senão a API devolve 400; custam cerca de 20 a 50 tokens (simples) ou 100 a 200 (aninhados) (V-02). Campo complexo sem exemplo válido é suspeito.
- Consolide ações com um parâmetro `action` somente quando o fluxo é um só; ações com efeitos muito diferentes ficam em tools separadas (anotações diferentes).
- Identificadores estáveis e legíveis (`order_id`, nome do recurso) em vez de índices posicionais.

## 4. Padrões antes e depois

| Antes | Depois | Por quê |
| --- | --- | --- |
| `list_all_orders()` devolve 5 MB | `orders_search(customer_id, status, created_after, page_size, cursor)` com `concise` | o agente nunca precisa da base inteira; contexto é finito |
| `get_user(user)` | `customers_get(customer_id)` | `user` ambíguo: nome? e-mail? id? |
| erro `Error 500` | `{"error":"invalid_customer_id","message":"... UUID (ex.: ...); use customers_search para obter o id"}` | o agente se corrige sozinho |
| três tools encadeadas sempre | uma tool que resolve o fluxo | menos chamadas, menos erros de encadeamento |
| resposta com 40 campos | 5 campos em `concise`, todos em `detailed`, IDs sempre presentes | alto sinal por token; IDs permitem a próxima chamada |
| truncar em silêncio | `"truncated": true, "hint": "refine com status ou created_after"` | sem a dica o agente repete a mesma busca |

## 5. Anotações MCP

Em servidores MCP, cada tool declara `readOnlyHint`, `destructiveHint`, `idempotentHint` e `openWorldHint` (V-06). Leitura: `readOnlyHint: true`. Cancelamento: `readOnlyHint: false`, `destructiveHint: true` (se irreversível), `idempotentHint: true` (se repetir é seguro). `openWorldHint: true` quando interage com sistemas externos abertos (web, e-mail). As anotações são **dicas** para o host; não são controle de acesso: a autorização continua no servidor.

Fluxo de trabalho do `mcp-builder` em 4 fases (V-06, destilado): (1) pesquisa e plano (APIs a expor, fluxos); (2) implementação com utilitários compartilhados e anotações; (3) revisão e teste com um inspetor/cliente; (4) avaliações. A stack segue o projeto.

## 6. Avaliação de 10 perguntas

Critérios (V-06): perguntas **independentes** entre si, **somente leitura**, **complexas** (várias chamadas), **realistas**, **verificáveis por comparação de string**, **estáveis** no tempo. Modelo em XML (`${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/avaliacao-10-perguntas.md`):

```xml
<evaluation>
  <qa_pair>
    <question>Qual o status do pedido mais recente do cliente 7f6c2a1e-0000-4000-8000-000000000001 e o total?</question>
    <answer>PAID, 49.90</answer>
  </qa_pair>
  <!-- ... mais 9 pares, todos com dados semeados e estáveis ... -->
</evaluation>
```

Execução: rode o agente com as tools antigas e novas sobre o mesmo conjunto; registre acerto, nº de chamadas, tokens e erros; leia as transcrições (a nota esconde o motivo). Conjunto de avaliação separado do usado para ajustar as descrições. Várias execuções por pergunta (uma não prova nada). Sem execução, declare "avaliação desenhada, não executada".

## 7. Scripts e CLIs para agentes

Opinião de autor (V-28, classe C), útil como heurística: ferramentas rápidas e com pouca saída; travar é pior que falhar (timeout); erro que orienta o próximo passo; pidfile/lock contra segunda execução; log em arquivo de caminho fixo além do terminal; comandos críticos como alvos de Makefile; MCP só quando o script não resolve. Sem métrica publicada.

## 8. Itens que mudam com o tempo

- Tabela de compatibilidade de `tool_choice` por modelo (V-02): conferir na hora.
- IDs e nomes de modelo; limites de tamanho de resposta (25.000 tokens é padrão do Claude Code, não regra geral, V-01).
- Subconjunto de JSON Schema em modo estrito; ferramentas sem suporte a `strict`.
- Campos novos de definição de tool: leia a doc atual antes de usar qualquer campo que este arquivo não cita.
