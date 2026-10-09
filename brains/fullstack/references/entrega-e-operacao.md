# Entrega, observabilidade, desempenho e recuperação

## Entrega começa no artefato

Identificar o que será promovido: commit, build, imagem, configuração, schema e flags. Preferir promover artefato testado quando o pipeline permite; rebuild pode produzir dependência diferente. Registrar lockfile, runtime e variáveis exigidas sem expor segredos.

Uma feature pronta localmente não equivale a implantada. Distinguir preparar release, publicar artefato, implantar, habilitar e verificar produção. Respeitar autorização para cada ação externa; keyword de desenvolvimento não amplia acesso ou permissão.

## Critério de serviço

Definir indicador do usuário: proporção de operações concluídas corretamente dentro de prazo, disponibilidade da jornada ou frescor de dado. Escolher janela e denominador; média esconde cauda e sucesso HTTP pode esconder erro de negócio. SLO orienta decisão e custo conforme necessidade do produto, não meta universal de 99,99%. [Fonte: Google SRE Service Level Objectives](https://sre.google/sre-book/service-level-objectives/).

Exemplo: pedido HTTP 202 é aceito rapidamente, mas processamento fica parado. Medir tempo até conclusão e idade da fila, além de latência HTTP. Identificar responsável e ação de resposta ao alerta.

## Observabilidade acionável

Correlacionar logs, métricas e traces com operação, sem dados sensíveis. OpenTelemetry descreve sinais de telemetria; coleta sozinha não fornece diagnóstico. [Fonte: OpenTelemetry Signals](https://opentelemetry.io/docs/concepts/signals/).

Definir cardinalidade e custo: ID de usuário como label pode explodir séries e expor dado. Separar evento de auditoria, log de diagnóstico e métrica agregada. Testar se uma falha simulada permitida gera sinal e se o runbook explica o próximo passo.

## Desempenho com hipótese

Definir workload (volume, mistura, concorrência, tamanho), baseline, ambiente, warmup e critério. Medir gargalo: CPU, memória, IO, pool, filas e dependências. Não chamar benchmark local de capacidade de produção. Carga externa exige escopo e limite acordados.

Antes: endpoint lento ganha cache sem invalidação. Depois: identificar query N+1, medir query/latência, ajustar acesso e revalidar no mesmo workload; se cache necessário, definir chave por tenant/permissão, TTL, invalidação e tolerância a dado antigo. Otimização que altera correção é regressão.

## Plano de rollout e reversão

Considerar canário/flag quando impacto e infraestrutura justificam. Definir sinais de interrupção antes de iniciar: erros, inconsistência, latência, saturação. Flag precisa de dono, valor seguro e plano de remoção; flags antigas criam combinações pouco testadas.

Rollback deve considerar schema e efeitos já produzidos. Reverter binário não desfaz envio de email, cobrança ou conversão de dado. Registrar compatibilidade entre versão anterior e migração; preferir correção para frente quando reversão não é segura, com decisão explícita do responsável.

## Checklist

- [ ] Artefato, versões e configuração rastreáveis.
- [ ] Build e dependências reproduzíveis na medida suportada pelo projeto.
- [ ] Migrações e coexistência de versões verificadas.
- [ ] Sinais representam sucesso do usuário e falha de negócio.
- [ ] Alerta tem dono, severidade e ação útil.
- [ ] Performance possui workload, baseline e limite acordado.
- [ ] Rollout, interrupção e reversão descritos antes de publicar.
- [ ] Verificação pós-entrega confirma fluxo e dado, não apenas healthcheck.
- [ ] Runbook e pendências acompanham entrega.

Falhas frequentes: readiness igual a liveness sem análise; retry amplificando incidente; log completo de payload; “zero downtime” sem versão antiga/nova concorrentes; deploy feito sem comparar artefato ao que passou testes.

Fontes consultadas em 2026-10-09. Estratégias são adaptáveis à infraestrutura existente; não executar implantação por inferência de autorização.
