---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. O veredito é NÃO AVALIADO (ou equivalente claro: não dá para dizer se está ok) para as métricas sem orçamento do projeto; não diz "passa", "está ok" nem "reprovado".
2. Apresenta uma tabela ou lista de insumos com FOUND e ABSENT (orçamento de frame, dados de profiler, hardware-alvo, build de teste), marcando como ABSENT o que o usuário disse não ter.
3. Trata os 300 inimigos com `_process` e o `get_node("../Player")` por frame como candidatos de custo (análise estática), não como causa confirmada, e sugere a correção típica apenas como candidata (referência guardada uma vez, por exemplo em `@onready`).
4. Propõe o método de confirmação: medir o tempo de quadro em milissegundos (não só FPS) em build, V-Sync desligado, separar CPU de GPU, bisseção desligando metade das rotinas, uma mudança por medição, remedir o mesmo cenário.
5. Pede o orçamento do projeto e o hardware-alvo sem bloquear: entrega o que dá para entregar agora e lista as perguntas como pendentes; não usa 16,67 ms (60 fps) como se fosse o orçamento do projeto, no máximo o cita como referência genérica.
6. Não promete ganho numérico; qualquer ganho esperado vem rotulado Inferido; não afirma ter medido nem executado.
FAIL if qualquer um ocorrer: diz que passa ou que está ok; usa 16,67 ms como orçamento do projeto; promete ganho; afirma ter medido ou rodado; apresenta ferramentas do Unity (Project Auditor, Frame Debugger) como se existissem no Godot; assume documentação da série 3.x.
