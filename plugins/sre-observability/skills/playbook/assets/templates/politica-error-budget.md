# Política de error budget — [SERVIÇO]

Template T-02. Estrutura de V-02 (SRE Workbook, "Implementing SLOs"; redação própria). As ações listadas como exemplo são ilustrativas: cada organização define as suas. Todos os stakeholders aprovam; sem acordo, revise SLIs e metas.

```text
Serviço:             [serviço]         SLO: [meta]% em [janela] dias (documento: T-01)
Orçamento de erro:   100% − [meta]% = [x]%  ≈ [conta e equivalente em tempo/requisições]
Consumo verificado:  [diário/semanal], dono: [papel/nome]
Revisão gerencial:   [mensal/trimestral]

Quando o orçamento estiver em [50]% consumido:   [ex.: revisar as 3 maiores causas em reunião de confiabilidade]
Quando estiver em  [75]% consumido:              [ex.: priorizar bugs de confiabilidade no próximo ciclo]
Quando esgotado:     [ ] prioriza confiabilidade   [ ] pausa features   [ ] congela deploys não essenciais
                     Duração da medida: até o orçamento se recuperar até [x]% ou decisão dos aprovadores
Executa as ações:    [papel responsável]
Falha originada em dependência de outro time: [decisão registrada: congelar ou não, e por quê]
Exceções permitidas: [ex.: correção de segurança, reversão de mudança que causou o consumo]
Escalonamento (divergência de cálculo ou de aplicação): [papel/fórum, prazo para decidir]

Autores:     [..]    Revisores: [..]
Aprovadores: produto [..] / desenvolvimento [..] / operação [..]   Data: [..]
Próxima revisão da política: [data]
```

Verificação antes de publicar: (1) a conta do orçamento está feita para a meta e janela deste serviço; (2) existe dono do acompanhamento e cadência; (3) as ações no esgotamento têm executor nomeado; (4) há caminho de escalonamento; (5) os três aprovadores assinaram.
