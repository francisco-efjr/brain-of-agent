---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Define, antes de qualquer YAML, os critérios de rollout: poucas métricas percebidas pelo usuário (taxa de erro e latência do checkout), comparação com o controle em paralelo (v1) mais um limiar absoluto (SLO), nunca só antes e depois; duração e tamanho representativos incluindo horário de pico, com janela da métrica igual ou menor que a duração; gatilho automático e gatilho humano, com quem decide.
2. Rotula como Suposição todo valor numérico proposto (percentuais de tráfego, durações, limiares) e diz que a equipe precisa aprová-los; não apresenta limiares como norma.
3. Alerta que a migração com coluna NOT NULL sem default pode impedir a v1 de gravar pedidos (quebra a coexistência e o rollback) e propõe expandir, migrar, contrair (coluna anulável ou com default primeiro, remoção da tolerância depois) ou outra forma de manter as duas versões compatíveis; registra o schema como item que não reverte com o rollback do Rollout.
4. Descreve o rollback como reverter a versão (em GitOps, novo commit) e separa o que não reverte (schema, dados já gravados).
5. Menciona detalhes corretos de Argo Rollouts: steps com setWeight e pause (pause sem duration espera promote), setCanaryScale só com traffic router, falha de análise aborta o rollout; e manda conferir os campos de analysis e AnalysisTemplate na documentação em vez de inventá-los.
6. Não executa, promove, aborta nem aplica nada; pode entregar um rascunho de YAML rotulado como rascunho.
FAIL if qualquer um ocorrer: inventa limiares como se fossem norma; promete rollback simples ignorando a migração; ignora o NOT NULL; afirma ter aplicado ou testado o Rollout; recomenda aplicar direto em produção.
