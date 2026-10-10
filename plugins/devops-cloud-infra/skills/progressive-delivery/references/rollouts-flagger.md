# Argo Rollouts, Flagger e plano de rollout preenchido

Base: V-44 (Argo Rollouts), V-45 (Flagger), V-46 (SRE Workbook, canarying), V-47 (OpenFeature), V-31 (Argo CD), P-17 (nota 85), brain `entrega-e-operacao` e `checklist-release`. Conferido em 2026-10-10. Destilação com redação própria; o SRE Workbook é CC BY-NC-ND 4.0 e não foi copiado. Todo número abaixo é **Suposição** até a equipe aprovar. Confirme campos e defaults na versão instalada do controller (`kubectl api-resources`, `kubectl explain rollout.spec.strategy --recursive` quando o CRD estiver instalado).

## Sumário

- [Plano preenchido (exemplo)](#plano-preenchido-exemplo)
- [Argo Rollouts](#argo-rollouts)
- [Flagger](#flagger)
- [O que não reverte](#o-que-não-reverte)
- [Verificação pós-mudança](#verificação-pós-mudança)
- [Feature flags](#feature-flags)

## Plano preenchido (exemplo)

Serviço fictício `checkout-api`, Kubernetes com Argo CD e Argo Rollouts, ingress com divisão por peso. Perguntas de entrada: convive com duas versões (sim, contrato de API retrocompatível), há métricas por versão (sim, Prometheus), traffic manager (sim).

```markdown
## Estratégia: canário, porque a API é retrocompatível e há métricas por versão
## Critérios (decididos antes do deploy)
| # | Critério | Definição | Quem decide | Rótulo |
| 1 | Métricas | taxa de respostas 5xx e latência p95 de `/checkout`, por versão (canário e estável) | dono do serviço | Suposição |
| 2 | Comparação | canário vs. versão estável em paralelo; e SLO absoluto de erro definido pela equipe (valor: pendente) | SRE de plantão | Pendente |
| 3 | Duração e tamanho | 10% por 15 min, 50% por 15 min; deve cruzar um período de pico; janela das métricas de 5 min (menor que a duração) | dono do serviço | Suposição |
| 4 | Gatilhos | automático: análise falha (erro do canário acima do controle ou do SLO); humano: latência piora sem passar o limiar, quem decide é o dono do serviço | SRE de plantão | Suposição |
| 5 | Rollback | novo commit revertendo o manifest; não reverte: migração `orders.add_column` já aplicada e e-mails de confirmação enviados pelo canário | dono + DBA | Suposição |
## Compatibilidade: versão N e N+1 usam o mesmo schema (coluna nova nula por padrão); cache com chave versionada
## Flags: `novo-calculo-frete` (dono: time de pagamentos; valor seguro: desligada; remoção: 2 sprints após 100%)
## Verificação pós-mudança: imagem do Pod ativo = digest aprovado; taxa de pedidos concluídos igual ou melhor que a semana anterior no mesmo horário
## Pendências de decisão humana: valor do SLO; quem aprova promoção fora do horário comercial
```

O exemplo mostra o formato; os números não são recomendação (a fonte não dá limiares, V-46).

## Argo Rollouts

Fatos verificados em V-44: o `Rollout` substitui o `Deployment` quando se precisa de entrega avançada; blue-green e canário; roteamento avançado (por exemplo, cabeçalhos HTTP) só com traffic manager; `setWeight`, `pause` (com `duration`, ou sem `duration` até `promote`), `setCanaryScale` (só com traffic router); sem `steps` o canário age como rolling update; `maxSurge` e `maxUnavailable` com padrão de 25%; falha de análise aborta o rollout; promoção ou rollback automáticos por métricas.

Canário (esqueleto; ajuste ao serviço):

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: checkout-api
spec:
  replicas: 5
  selector:
    matchLabels:
      app: checkout-api
  template:
    metadata:
      labels:
        app: checkout-api
    spec:
      containers:
        - name: api
          image: registry.example.com/checkout-api@sha256:<digest-real>
  strategy:
    canary:
      canaryService: checkout-api-canary
      stableService: checkout-api-stable
      trafficRouting:
        nginx:
          stableIngress: checkout-api
      steps:
        - setWeight: 10
        - pause: { duration: 15m }
        - setWeight: 50
        - pause: { duration: 15m }
        - pause: {}                 # espera `promote` humano antes de 100%
```

`trafficRouting` depende do traffic manager escolhido (nginx, Istio, ALB e outros): consulte a página de traffic management da versão instalada e não copie o bloco acima sem ajustar. Análise automática (`AnalysisTemplate`, `analysis`): **não foi lida nesta cadeia**; leia as páginas de Analysis do Argo Rollouts antes de escrever esse bloco.

Blue-green:

```yaml
  strategy:
    blueGreen:
      activeService: checkout-api-active
      previewService: checkout-api-preview
      autoPromotionEnabled: false   # promoção manual após teste no preview
```

Quando escolher: troca atômica, aplicação que não convive com duas versões, ou ausência de métricas confiáveis. Custo: duplica réplicas durante a troca.

## Flagger

Fatos verificados em V-45: estratégias canário, A/B e blue-green com mirroring; tráfego via service mesh ou ingress; provedores de métricas Prometheus, InfluxDB, Datadog, New Relic, CloudWatch, Stackdriver, Graphite; alertas em Slack, Teams, Discord e Rocket; `interval` padrão de 60 s; `threshold` é o número máximo de checagens com falha antes do rollback; `maxWeight`, `stepWeight`, `iterations` (A/B e blue-green), `metrics`, `webhooks`; promoção com falha vira `Promoted=false` com motivo `Failed`; projeto graduado na CNCF.

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: checkout-api
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: checkout-api
  service:
    port: 80
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
        interval: 1m
```

As métricas embutidas (`request-success-rate`, `request-duration`) dependem do provedor de métricas e do mesh/ingress configurados no Flagger; confirme na página do provedor. `min: 99` é exemplo (Suposição). Versão de API (`v1beta1`) e campos: confira na versão instalada.

## O que não reverte

Antes do deploy, percorra a lista e escreva "reverte", "não reverte" ou "não aplicável" para cada item:

| Item | Por que importa | Alternativa se não reverte |
| --- | --- | --- |
| migração de schema aplicada | o código antigo pode não ler o schema novo | expandir/migrar/contrair em fases (plugin `database-data-modeling`); correção para a frente |
| state do Terraform/Pulumi | reverter o código não reverte recursos já criados | novo `plan` revisado; nunca editar state à mão |
| dados já gravados ou convertidos | rollback do binário não restaura dados | backup/restauração testado; script de correção |
| e-mail, SMS, cobrança, webhook emitidos | efeito externo irreversível | comunicação, estorno, idempotência no reenvio |
| mensagens já consumidas de fila | pode haver perda ou duplicação | dead-letter, reprocessamento idempotente |
| flag ligada para usuários | estado do usuário mudou | desligar a flag e tratar os afetados |

Regra do brain: quando reverter não é seguro, prefira correção para a frente com decisão explícita do responsável. Em GitOps o rollback é um novo commit; com Argo CD e sync automático, o rollback pela UI é bloqueado (V-31).

## Verificação pós-mudança

Prove a revisão no ar e o fluxo, não só o alcance (um 200 prova alcance, não qual release está no ar; gstack `land-and-deploy`, MIT, Garry Tan, como inspiração):

- Qual imagem está ativa: `kubectl get rollout checkout-api -o jsonpath='{.spec.template.spec.containers[0].image}'` e a lista de ReplicaSets/Pods ativos (`kubectl get pods -l app=checkout-api -o wide`) comparados ao digest aprovado.
- O fluxo de negócio: indicador do usuário (pedidos concluídos, não só HTTP 2xx), comparado ao mesmo horário da semana anterior (Suposição quanto à janela).
- Logs de erro da versão nova no período do canário.

Esses comandos são de leitura; o usuário (ou `deploy-infra`) os roda no contexto aprovado.

## Feature flags

- Acesso pela API do OpenFeature (Evaluation API, contexto de avaliação, providers, hooks; V-47).
- Nasce com dono, valor seguro e data de remoção no PR que a cria (Inferido; OpenFeature não trata do ciclo de vida).
- Testar com a flag ligada e desligada (brain `checklist-release`).
- Remover o código morto quando a flag chega a 100% e estabiliza: flags antigas geram combinações pouco testadas (brain).
