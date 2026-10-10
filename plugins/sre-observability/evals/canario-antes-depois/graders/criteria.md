---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final e no transcript:
1. Aponta que a comparação hoje contra ontem no mesmo horário (antes e depois) é frágil porque padrões de tráfego e dependências mudam, e recomenda comparar o canário com um controle concorrente (instâncias da versão atual servindo tráfego comparável ao mesmo tempo).
2. Recomenda poucas métricas (no máximo cerca de uma dúzia), de preferência os SLIs (erro e latência da busca) e desaconselha CPU como critério por ser ruidosa.
3. Explica a necessidade de separar as séries do canário e do controle, com o exemplo de que 20% de erro numa fatia de 5% do tráfego aparece como cerca de 1% no agregado.
4. Pede baseline capturado antes do deploy e não sobrescrito durante a comparação, e critérios de interrupção e rollback definidos antes de começar, tratando os 10% do plano como Suposição a calibrar.
5. Sugere alertar apenas se o mesmo padrão aparecer em duas checagens seguidas (antes disso, observação), com estados quebrado, degradado ou saudável, e evidência por alerta; indica que 2 checagens é escolha do autor e deve ser calibrada.
6. Diz que o rollback é decisão humana (a automação apenas recomenda) e que reverter o binário não desfaz efeitos já produzidos (dados migrados, e-mails, cobranças); verifica compatibilidade entre versões.
7. Menciona o comando explícito /sre-observability:release-health para conduzir a verificação, sem executar consultas nem reversões.
FAIL if qualquer um ocorrer: aprova o plano antes e depois; usa CPU como critério principal; propõe 30 ou mais métricas; automatiza o rollback sem decisão humana; ignora a separação entre canário e controle.
