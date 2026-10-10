# Ficha de tool MCP

Preencha uma ficha por tool **antes** de implementar (fase 1–2 do fluxo de V-12). Se duas fichas respondem à mesma tarefa do usuário, consolide (T-01).

| Campo | Preenchimento |
| --- | --- |
| Intenção do usuário (uma frase: "quando o usuário quer…") | |
| Nome (`servico_verbo_objeto`, T-02) | |
| Descrição (o que faz · quando usar · quando **não** usar e a tool vizinha · o que retorna) | |
| Parâmetros (nome sem ambiguidade, tipo, restrições, exemplo; T-03) | |
| Retorno `concise` (campos de alto sinal, IDs traduzidos para nomes) | |
| Retorno `detailed` (opcional) | |
| Limite padrão e paginação (T-05) | |
| Erros previstos e mensagem acionável (causa · correção · exemplo válido; T-06) | |
| Anotações: `readOnlyHint` / `destructiveHint` / `idempotentHint` / `openWorldHint` (T-07) | |
| Efeito colateral e confirmação exigida no servidor (S-04) | |
| Traz conteúdo externo/da web? (injeção, trifecta; S-06) | |
| Autorização/escopo necessário (credencial mínima; S-03) | |
| Tarefa de avaliação que exercita esta tool (várias chamadas, resposta verificável) | |
| Teste: válido · inválido · vazio · grande · erro de autenticação | |

Nota: não ponha na descrição o que o servidor deve **impor** (autorização, limites): isso é código. Fonte: V-09, V-12, V-27. Verificado em 2026-10-10.
