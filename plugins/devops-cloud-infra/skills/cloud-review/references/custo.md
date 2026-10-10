# Custo, FinOps e plataforma interna

Base: V-53 (Infracost, classe B), V-40 (AWS Cost Optimization, metas), V-48 (Cost Anomaly Detection no Lambda), V-51 (CNCF Platforms White Paper, classe A), V-52 (Backstage Software Templates, classe B), P-23. Conferido em 2026-10-10. Destilação com redação própria. Lacuna: o FinOps Framework (finops.org) não foi lido (403); não cite práticas dele como verificadas.

## Custo

### Estimativa no PR

Fatos de V-53: Infracost cobre Terraform, CloudFormation e AWS CDK (AWS, Azure, Google Cloud); `infracost setup` e `infracost scan` mostram custo por recurso, violações de política FinOps e tags; comenta no PR; a estimativa parte do JSON do plano; a ferramenta declara que credenciais e segredos de nuvem não são enviados à API. `breakdown` e `diff` **não** foram confirmados nas páginas lidas. É estimativa, não garantia.

Fluxo para o PR (leitura e geração local, sem aplicar):

1. O usuário (ou o CI) gera o plano: `terraform plan -out=tfplan` e `terraform show -json tfplan > plan.json`. Você não roda `plan`.
2. Com `infracost` instalado e autorização para enviar o JSON do plano: `infracost scan` e leitura do resultado (confira os argumentos na `--help` da versão instalada).
3. Registre: custo mensal estimado, delta contra a base, premissas de volume (ex.: invocações, GB trafegados), recursos sem preço (uso variável).
4. Revisão humana acima do limite **definido pela equipe**; você não inventa limite. Até haver um, escreva "limite: pendente de decisão".

Template de estimativa sem inventar preço:

```markdown
| Recurso | Premissa de uso | Preço unitário (fonte, data) | Custo mensal | Rótulo |
| aws_lambda_function.worker | N invocações/mês, M MB, T ms | [página oficial de preços, data da consulta] | N x ... | Suposição |
```

Sem consulta à página de preços nesta sessão, o preço fica "pendente" e o rótulo é Suposição.

### Checklist CO-nn

| ID | Verificar | Sev. | Fonte |
| --- | --- | --- | --- |
| CO-01 | tags de dono e ambiente em todo recurso que gera custo (`default_tags` no provider) | Médio | V-53 |
| CO-02 | estimativa de custo no PR com premissas explícitas | Médio | V-53 |
| CO-03 | alarme de anomalia de custo ligado (no caso da AWS, o Cost Anomaly Detection pode atrasar até 24 h) | Médio | V-48 |
| CO-04 | recursos com custo contínuo decididos com dado: provisioned concurrency, instâncias mínimas, NAT gateways, volumes ociosos (os dois últimos: Inferido) | Médio | V-48, V-50 |
| CO-05 | ambientes efêmeros com criação, expiração e limite de custo | Alto | brain `dados-ambientes-ci` |
| CO-06 | as cinco metas de custo da AWS têm responsável: gestão financeira, visibilidade de gasto e uso, recursos adequados, oferta e demanda, otimização contínua | Informativo | V-40 |
| CO-07 | recursos de teste com `command = apply` em `terraform test` só em conta descartável e com orçamento | Alto | V-37 |

## Plataforma interna (CNCF)

Fatos de V-51 (CNCF TAG App Delivery, v1.0, sem data): sete atributos (plataforma como produto; experiência do usuário; documentação e onboarding; self-service; carga cognitiva reduzida; opcional e composável; secure by default); "golden path" aparece no atributo de documentação e na lista de 13 capacidades; métricas NPS, SPACE e as quatro métricas DORA; começar pelo esforço viável mínimo ("thinnest viable platform"), com capacidades pouco diferenciadas e poucos times.

Checklist de maturidade PL-nn:

| ID | Pergunta | Evidência |
| --- | --- | --- |
| PL-01 | Existe **uma** capacidade em self-service (por exemplo, criar um serviço novo, provisionar um banco) sem ticket? | template, portal ou pipeline documentado |
| PL-02 | Há um golden path com exemplo funcional e documentação de onboarding? | repositório-modelo, guia |
| PL-03 | A plataforma tem dono e é tratada como produto (usuários, feedback)? | backlog, canal de suporte |
| PL-04 | As métricas DORA (frequência de deploy, tempo de entrega de mudança, taxa de falha de mudança, tempo de restauração) são medidas por time? | dashboard (os nomes das quatro: conhecimento estável, Inferido) |
| PL-05 | O template já nasce seguro (permissões mínimas, segredos fora do repo, pins)? | template revisado contra `iac-review` e `gha-hardening-review` |
| PL-06 | Usar a plataforma é opcional e composável, ou obrigatório sem saída? | política |

Backstage Software Templates (V-52) servem como exemplo de golden path: carregam esqueleto de código, preenchem variáveis e publicam em GitHub ou GitLab, em steps com entradas próprias. A página **não** usa o termo "golden path" (o conceito vem do white paper da CNCF). Detalhes verificados: `scaffolder.registerComponent: false` em `app.routes.bindings` oculta "Register Existing Component"; IDs de ação em camelCase (hífen vira subtração e resulta em `NaN`).

Armadilhas: portal sem capacidade de self-service real é vitrine; metas de DORA sem medição por time viram slogan; plataforma obrigatória e rígida aumenta a carga cognitiva, o contrário do objetivo.
