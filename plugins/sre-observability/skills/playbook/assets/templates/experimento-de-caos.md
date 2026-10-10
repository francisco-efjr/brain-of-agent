# Experimento de caos — [NOME]

Template T-08. Base: quatro passos de principlesofchaos.org (V-29): estado estável mensurável, hipótese, eventos reais, tentativa de refutar. Redação própria. **O plugin planeja o experimento; não injeta falha.** Experimento em produção só com autorização humana explícita, raio de explosão mínimo e critério de aborto definidos.

```text
Experimento:                 [nome]           Serviço: [serviço]        Ambiente: [staging / produção]
Estado estável               (métrica, janela, limiar): [ex.: taxa de sucesso do checkout ≥ [x]% e p95 < [y] ms, janela de [z] min]
Hipótese:                    o estado estável se mantém com a falha [descrição da falha]
Grupo de controle:           [o que permanece sem a falha, para comparação concorrente]
Variável injetada            (evento realista): [ex.: perda de 1 de 3 réplicas; latência de +300 ms na dependência X]
Ferramenta:                  [ex.: Chaos Mesh (exige Kubernetes), ou procedimento manual] · Quem opera: [papel]
Raio de explosão             (quem é afetado, como limitar): [% do tráfego, região, tenants excluídos]
Critério de aborto:          [ex.: SLI abaixo de [x] por [y] min, ou qualquer alerta de página; quem aborta e como: [comando/botão]]
Pré-condições:               [monitoramento ligado, runbook de rollback testado, janela comunicada, plantão ciente]
Autorização humana           (obrigatória em produção): aprovador [nome/papel] · data [..] · registro [link]
Resultado                    (hipótese refutada ou não, com evidência): [preencher após a execução; "não executado" até lá]
Ação de acompanhamento:      [dono, prazo, ticket]
```

Verificação antes de executar: (1) hipótese ligada a métrica mensurável; (2) evento injetado é realista e prioriza impacto e frequência; (3) o grupo de controle existe; (4) aborto testado em ambiente não produtivo; (5) autorização registrada. Resultado só é Verificado com consulta executada e saída colada.
