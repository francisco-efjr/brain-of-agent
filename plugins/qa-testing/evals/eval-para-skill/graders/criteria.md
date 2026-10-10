---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Propõe pelo menos 3 casos no layout `evals/<caso>/prompt.md` mais `graders/*.md`, com frontmatter nos arquivos.
2. Inclui um caso que deve disparar (usando a migração do pedido dentro do prompt, sem citar o nome `revisar-migracao-sql`), um caso negativo (pedido não relacionado) com grader `tool_used` de `min: 0` e `max: 0`, um grader sobre o resultado e um sobre os passos.
3. Usa grader `llm` somente para saída curta, com PASS if e FAIL if concretos e binários, e sugere juiz de modelo diferente do gerador; começa por graders determinísticos.
4. Menciona 3 execuções por caso, comparação com baseline sem o plugin (ablação), leitura das transcrições e que `tool_used: Skill` é indicador de disparo.
5. Avisa custo de modelo por execução e por juiz, a versão mínima do Claude Code (2.1.269 ou superior) e que no Windows nativo suítes com Bash exigem WSL2, e marca os casos como `designed_not_executed`.
6. Recomenda partir de falhas reais da skill; sinaliza como «a confirmar na documentação da versão instalada» qualquer flag ou campo de que não tenha certeza.
FAIL if qualquer um ocorrer: inventa flags, campos ou resultados de execução; afirma que rodou os casos; escreve grader `llm` vago («a resposta está boa?»); cita o nome da skill dentro dos prompts dos casos; ignora o caso negativo.
