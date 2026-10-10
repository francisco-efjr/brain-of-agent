# Checklists de promoção: registro, serving, skew, drift, rollback

Validado em 2026-10-10. Redação própria a partir de V-22 (MLflow, param087 MIT classe C), V-23 (serving, param087 com correções do validador), V-24 (AWS MLOPS01-BP03; timwukp Apache-2.0; Evidently de versão não declarada), V-31 (Rules of ML, Sculley et al.). Cada linha: ID · severidade · como verificar · status epistêmico esperado. Marque cada item com Verificado (visto no código ou documento), Inferido, ou NÃO VERIFICÁVEL (sem acesso).

## Sumário
1. Critérios de decisão (antes do teste)
2. Registro e rastreabilidade
3. Serving
4. Skew treino-serving
5. Drift e monitoramento
6. Rollback
7. Perguntas ao dono do modelo

## 1. Critérios de decisão (antes do teste)

| ID | Item | Sev. | Como verificar |
| --- | --- | --- | --- |
| P-01 | Métrica de decisão e meta com origem da meta | BLOCK | doc de critérios com data anterior à avaliação no teste |
| P-02 | Baseline (heurística ou modelo atual) na mesma partição | BLOCK | relatório de avaliação com ambos |
| P-03 | Fatias que não podem piorar, definidas antes | BLOCK se relevantes | tabela por fatia com n e intervalo |
| P-04 | Teste usado uma vez, sem escolhas nele | BLOCK | histórico do notebook/runs |
| P-05 | Meta de latência, custo e capacidade | WARN | doc do serviço |
| P-06 | Calibração medida quando a probabilidade é usada | WARN | curva e Brier |

## 2. Registro e rastreabilidade

| ID | Item | Sev. | Como verificar |
| --- | --- | --- | --- |
| R-01 | Hash dos dados de treino e avaliação no run | BLOCK se ausente | tags/params do run |
| R-02 | Commit **e** flag de diretório sujo | BLOCK se ausente | `git rev-parse HEAD` e `git status --porcelain` registrados |
| R-03 | Lockfile completo e versões (Python, bibliotecas, CUDA) | BLOCK se ausente | arquivo anexado ao run |
| R-04 | Seed e parâmetros; métricas **por fold** | WARN | params/metrics do run |
| R-05 | Artefatos: pipeline completo (pré-processamento + modelo), relatório | BLOCK se só o modelo | lista de artefatos |
| R-06 | Promoção por alias ou versão; controle de quem promove | WARN | política do registro |
| R-07 | Produção carrega por `models:/<nome>@<alias>` ou `/<versão>`, nunca por `run_id` | BLOCK | grep no código de serving |
| R-08 | Logging dentro do contexto de run (`with mlflow.start_run()`), sem runs órfãos | WARN | listagem de runs (Inferido de listagens de terceiros) |

## 3. Serving

| ID | Item | Sev. | Como verificar |
| --- | --- | --- | --- |
| S-01 | **Sem `pickle`/`joblib`/`torch.load(weights_only=False)` de origem não confiável** | BLOCK | grep `pickle\.load|joblib\.load|torch\.load`; origem do arquivo |
| S-02 | Modelo carregado uma vez no start, não por requisição | WARN | código do handler |
| S-03 | Payload validado (schema, tipos, faixas); erro 422 com mensagem | WARN | modelo de dados do endpoint |
| S-04 | `model_version` na resposta | BLOCK se sem rastreio | contrato da resposta |
| S-05 | `/health` (vivo) e `/ready` (modelo carregado) | WARN | rotas |
| S-06 | Timeouts e limite de tamanho de requisição | WARN | configuração |
| S-07 | Pré-processamento idêntico ao treino (mesmo objeto/biblioteca) | BLOCK se divergente | diff de código treino vs serving |
| S-08 | Autenticação e limite de taxa em endpoint público | BLOCK se público e aberto | configuração |
| S-09 | Latência p50/p95/p99, taxa de erro e drift monitorados | WARN | dashboards (NÃO VERIFICÁVEL se sem acesso) |
| S-10 | Segredos fora do código e dos artefatos; sem PII em artefato | BLOCK | grep de padrões de credencial; inspeção de artefatos |

Observação: um "checklist" que pede readiness mas cujo código só expõe `/health`, ou que pede `model_version` mas não o devolve, é um achado típico (V-23); confira o código, não o checklist. Alegações de ganho de velocidade com ONNX/quantização sem benchmark e com pré-processamento ignorado não são evidência.

## 4. Skew treino-serving

| ID | Item | Sev. | Como verificar |
| --- | --- | --- | --- |
| K-01 | Mesma implementação de features em treino e serving (biblioteca compartilhada) | BLOCK se cópia manual divergente | diff / imports |
| K-02 | Features logadas no serving | WARN | schema de logs |
| K-03 | Comparação de distribuição treino vs serving por feature | WARN | relatório de skew |
| K-04 | Dados do serving chegam no mesmo formato, unidade e fuso | WARN | amostras e contrato |
| K-05 | Corte temporal no teste (treinar até uma data, testar depois) | BLOCK se ausente com dado temporal | partição |

## 5. Drift e monitoramento

| ID | Item | Sev. | Como verificar |
| --- | --- | --- | --- |
| D-01 | Baseline de features e predições salvo antes do deploy | WARN | artefato |
| D-02 | Janelas de referência e atual definidas por tempo | WARN | config |
| D-03 | Tipos de coluna declarados (numérica, categórica) | WARN | `DataDefinition` ou equivalente |
| D-04 | Teste por tipo (PSI/KS numéricas; qui-quadrado categóricas) com **limiares documentados como convenção** | WARN | doc de limiares |
| D-05 | Drift de entrada, de predição e de qualidade separados | WARN | painéis |
| D-06 | Tamanho de efeito além do p-valor; correção de múltiplos testes | WARN | método |
| D-07 | Cada alerta com dono e ação; protocolo de resposta | WARN | runbook |
| D-08 | Retreino automático **somente com revisão humana** | BLOCK se automático sem revisão | pipeline |
| D-09 | Revisão periódica, mesmo sem alerta | WARN | cadência |
| D-10 | Versão da biblioteca de drift fixada e API conferida | WARN | lockfile |
| D-11 | Métrica de negócio monitorada | WARN | painéis |

Antipadrões (AWS, Verificado): sem métrica de negócio; sem plano de ação; monitoramento irregular; sem limiar. Rótulos que chegam com atraso exigem monitoramento de qualidade com defasagem declarada (Inferido).

## 6. Rollback

Plano mínimo:
1. **Versão de retorno**: alias/versão anterior identificado e ainda disponível no registro.
2. **Gatilhos**: métrica de qualidade (com limiar), guardrail de negócio, taxa de erro/latência; com janela de observação.
3. **Dono da decisão** e canal de acionamento.
4. **Procedimento**: mover o alias de volta; invalidar caches; verificar `model_version` nas respostas; registrar o evento.
5. **Dados**: o que fazer com predições já servidas e com dados gravados pelo modelo novo.
6. **Teste do rollback** feito antes (ao menos em ambiente de teste).
Sem plano de rollback: BLOCK.

## 7. Perguntas ao dono do modelo

1. "Quem escreve no local de onde o modelo é carregado?"
2. "O código de features do serving importa a mesma função que o treino?"
3. "Os critérios de promoção foram escritos antes de olhar o teste? Onde está o registro com data?"
4. "O que acontece com a decisão de negócio se o modelo ficar indisponível ou for revertido?"
5. "Quem recebe o alerta de drift e qual é a primeira ação?"
