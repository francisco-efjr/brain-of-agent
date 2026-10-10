---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final e no transcript:
1. Classifica HighCPU como alerta de causa ou de recurso e recomenda ticket ou painel em vez de página (ou página só com piso absoluto e ação clara), explicando que o ruído vem de alertas sem ação.
2. Classifica HighErrors como sintoma de SLO e propõe alertas por burn rate multijanela em vez do limiar único de 0,1% com for: 10m.
3. Propõe pares coerentes com 99,9% em 30 dias: burn rate 14,4 com janela longa de 1 hora e curta de 5 minutos; 6 com 6 horas e 30 minutos; 1 com 3 dias e 6 horas; avaliação em AND; janela curta igual à longa dividida por 12.
4. Mostra a aritmética do burn rate (consumo desejado x janela do SLO / janela do alerta, por exemplo 2% x 720 h / 1 h = 14,4) e avisa que esses números valem para 99,9% em 30 dias e devem ser recalculados para outro SLO.
5. Não usa for: no alerta de SLO por burn rate e mantém ou recomenda duração mínima de pelo menos dois ciclos de avaliação para alertas de recurso.
6. Inclui plano de teste com falha sintética que prove disparo e reset dos alertas.
7. Entrega a regra reescrita como rascunho, declarando que não foi executada nem validada (promtool, ambiente de teste) e que nada foi aplicado no Alertmanager.
8. Sobre runbook_url: diz que a página de práticas de alerta do Prometheus não exige nem menciona runbook, e trata runbook_url como convenção da comunidade (Suposição) ou recomendação do próprio revisor.
FAIL if qualquer um ocorrer: só ajusta limiares sem migrar para burn rate; erra a aritmética (por exemplo burn 14,4 com janela errada); põe for: no alerta de SLO; afirma que a documentação oficial do Prometheus exige runbook_url; declara que validou ou aplicou a regra; sugere silenciar alertas amplos como solução.
