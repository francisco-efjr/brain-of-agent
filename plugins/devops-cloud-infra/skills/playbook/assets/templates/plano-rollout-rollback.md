# Plano de rollout e rollback

<!--
Defina TUDO antes do deploy. Valores numéricos que você propuser são Suposição até a equipe aprovar;
nenhum limiar é norma. Base: Google SRE Workbook (canarying; CC BY-NC-ND, só destilação), Argo Rollouts,
Flagger e o brain-of-agent (entrega-e-operacao). Este plano não promove, não aborta e não aplica nada.
-->

| Campo | Valor |
| --- | --- |
| Serviço e versões | [SERVIÇO] · de [VERSÃO ATUAL] para [VERSÃO NOVA] |
| Artefato promovido (imagem por digest, commit, config) | [IDENTIFICADOR] |
| Estratégia | [blue-green / canary / rolling] · motivo: [convive com duas versões? há métricas confiáveis? há traffic manager?] |
| Ferramenta | [Argo Rollouts / Flagger / Deployment] |
| Dono · quem decide · janela | [NOMES] · [DATA, FUSO] |

## Compatibilidade entre versões

- A versão anterior lê o schema e os dados que a nova grava? [sim / não / Suposição]
- Migração envolvida: [descrição]. Se quebrar a versão anterior: expandir, migrar, contrair, ou correção para frente com decisão do responsável.
- Flags envolvidas: [NOME · dono · valor seguro · data de remoção]

## As cinco linhas de critérios

| # | Critério | Definição | Rótulo |
| --- | --- | --- | --- |
| 1 | Métricas (poucas, percebidas pelo usuário, atribuíveis à mudança) | [ex.: taxa de erro 5xx; latência p95 do checkout] | |
| 2 | Comparação: controle em paralelo + limiar absoluto (SLO), nunca só antes/depois | [ex.: erro do canário não excede o do controle por mais de [X] pontos; SLO [Y]] | Suposição |
| 3 | Duração e tamanho representativos, incluindo pico; janela da métrica menor ou igual à duração; um canário por vez | [ex.: [N]% do tráfego por [T] min, cobrindo o pico das [HORA]] | Suposição |
| 4 | Gatilho automático (métrica fora do controle ou do SLO) e gatilho humano (sinal ambíguo) | Automático: [REGRA]. Humano: [SINAL]. Decide: [NOME] | |
| 5 | Rollback e o que não reverte | Rollback: [commit a reverter / abort do rollout]. Não reverte: [schema, state, dados gravados, e-mails, cobranças] | |

## Passos do rollout

| Passo | Peso ou ação | Pausa ou análise | Critério para avançar |
| --- | --- | --- | --- |
| 1 | [ex.: setWeight 10] | [pause com `duration` ou até `promote`] | [métrica dentro do critério 2] |

Notas de campo (conferir na versão instalada): Argo Rollouts, `pause` sem `duration` espera `promote`; `setCanaryScale` só com traffic router; sem `steps` age como rolling update; falha de análise aborta; confira `analysis` nas páginas de Analysis antes de escrever YAML. Flagger: `interval` (60 s), `threshold`, `maxWeight`, `stepWeight`, `iterations`, `metrics`, `webhooks`.

## Verificação por etapa

- Prova de que a revisão certa recebe o tráfego: [COMO]
- Fluxo de negócio verificado: [COMO]

## Pendências de decisão humana

- [DECISÃO · responsável]
