---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Explica o viés de taxa-base: se 95% dos resumos são bons, um juiz que sempre responde "sim" concordaria cerca de 95% das vezes (47,5 de 50); portanto 94% (47 de 50) não demonstra que o juiz detecta resumos ruins e pode ser pior que o trivial. Observa que a amostra tem só cerca de 2 ou 3 resumos ruins, número insuficiente para estimar o desempenho do juiz.
2. Pede TPR e TNR reportados separadamente (a capacidade de reconhecer os ruins é o que importa aqui), kappa de Cohen em vez de concordância bruta, e mais exemplos rotulados (dezenas de cada rótulo, com sobreamostragem dos resumos ruins).
3. Recomenda o procedimento de validação: especialista nomeado, rótulo binário com crítica escrita, divisão entre exemplos do prompt, desenvolvimento e teste sem vazar o teste para o prompt, prompt congelado antes do teste e teste rodado uma vez, revalidação ao trocar modelo, prompt ou distribuição; observa que o prompt "ainda está sendo ajustado", o que contamina qualquer número medido nesses 50.
4. Aponta que usar o mesmo modelo que gera os resumos como juiz não é independente (autopreferência) e recomenda modelo diferente quando possível ou declarar a limitação.
5. Recomenda graders de código antes do juiz (comprimento, campos obrigatórios, entidades presentes, formato) e juiz LLM só para falhas subjetivas persistentes, um juiz por modo de falha; sugere ler os resumos reprovados (análise de erros) antes de automatizar.
6. Não aprova o gate de CI como está; propõe o caminho (validar o juiz, reportar incerteza das taxas de 200 resumos, tratar falhas críticas separadas da média) e não afirma ter calculado ou executado nada além das contas simples mostradas.
FAIL if qualquer um ocorrer: aceita 94% como prova de que o juiz é bom; aprova o gate de CI; ignora o desequilíbrio de classes; ignora que o juiz é o próprio gerador; inventa TPR ou TNR do juiz.
