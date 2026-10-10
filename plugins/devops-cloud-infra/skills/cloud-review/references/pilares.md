# Well-Architected: uma pergunta de revisão por pilar

Base: V-23 e V-40 (classe B: as páginas lidas são hubs; as práticas por pilar **não** foram lidas). Conferido em 2026-10-10. As perguntas abaixo são autoria desta síntese (decisão de design), não afirmações dos frameworks. Uso correto: conduzir a revisão como conversa sobre trade-offs, como a própria AWS descreve (V-23), e registrar "sem evidência" quando o material recebido não responde. Nunca invente uma prática atribuída a um pilar.

## O que foi verificado

| Framework | Verificado | Fonte |
| --- | --- | --- |
| AWS Well-Architected | seis pilares nas páginas de Security e Cost Optimization; Security (6 nov 2024) sem princípios de design nem implementação; Cost Optimization (27 jun 2024) com cinco metas: Practice Cloud Financial Management, Expenditure and usage awareness, Cost effective resources, Manage demand and supply resources, Optimize over time; ferramenta Well-Architected Tool gratuita | V-23, V-40 |
| Google Cloud Well-Architected Framework | seis pilares: operational excellence; security, privacy and compliance; reliability; cost optimization; performance optimization; sustainability; perspectivas de AI/ML e de serviços financeiros. O nome oficial atual é "Well-Architected Framework" (a URL ainda usa `architecture/framework`) | V-40 |
| Azure Well-Architected Framework | cinco pilares: Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency; cargas (Fabric, AI, SaaS, mission-critical, HPC, sustentabilidade); ferramenta de assessment; `ms.date` 2026-09-11 | V-40 |

Os nomes dos seis pilares da AWS fora dos dois lidos (Operational Excellence, Reliability, Performance Efficiency, Sustainability) são conhecimento estável: Inferido.

## Perguntas por pilar

Responda cada uma com evidência (`arquivo:linha`, saída de comando, documento) ou escreva "sem evidência: Não verificável". As colunas de nuvem mostram como o pilar se chama em cada framework.

| Pilar (AWS / GCP / Azure) | Pergunta de revisão | Evidência típica no que você recebeu |
| --- | --- | --- |
| Operational excellence (AWS, GCP, Azure) | Como a equipe sabe que uma mudança funcionou e como a desfaz? Quem é acionado quando falha? | pipeline com verificação pós-deploy, plano de rollback, runbook, alarmes com dono |
| Security (AWS), Security privacy and compliance (GCP), Security (Azure) | Quem acessa o quê, com qual privilégio, e como o acesso é auditado? Onde os dados estão cifrados? | IAM sem wildcard, segredos em cofre, rede privada, logs de auditoria, chaves KMS |
| Reliability (AWS, GCP, Azure) | O que acontece quando uma dependência, uma instância ou uma zona cai? O backup foi restaurado alguma vez? | multi-AZ, retries com backoff, DLQ, teste de restauração, health checks |
| Performance efficiency (AWS), Performance optimization (GCP), Performance Efficiency (Azure) | O dimensionamento foi medido com carga representativa? O que escala sozinho e o que não? | teste de carga, autoscaling, limites, métricas de saturação |
| Cost optimization (AWS, GCP, Azure) | Quem é o dono do custo? Há estimativa antes do PR e alarme de anomalia depois? | tags de dono, orçamento, estimativa de custo no PR, desligamento de ambientes ociosos |
| Sustainability (AWS, GCP) | Os recursos são proporcionais ao uso real? | dimensionamento, desligamento fora de horário, regiões |

As cinco metas de custo da AWS viram perguntas diretas: existe prática de gestão financeira de nuvem (responsável, revisão periódica)? o gasto e o uso são visíveis por time? os recursos escolhidos são os de custo-benefício adequado? a oferta acompanha a demanda? há revisão contínua?

## Uso na revisão

1. Escolha o framework da nuvem do projeto; não misture.
2. Percorra os pilares; para cada um, 1 a 3 linhas: pergunta, evidência, lacuna.
3. Priorize lacunas pelo impacto (perda de dados, exposição, indisponibilidade) e pelo custo de corrigir.
4. Classifique como **Verificado** só o que está nos arquivos. O que depende da conta (backup configurado, quotas, regiões, Well-Architected Tool preenchida) é **Não verificável**.
5. Topologia, multi-região e decisão entre monólito e serviços ficam com `architecture-design`: registre o ponteiro, não decida aqui. Decisões relevantes viram ADR de infra (`${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/adr-infra.md`).
