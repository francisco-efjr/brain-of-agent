# MLOps, governança e notebooks

Validado em 2026-10-10. Fontes: V-22, V-23, V-24, V-25, V-30, V-31, V-32, V-33 (ver `fontes.md`). Este plugin **não faz deploy**: produz plano, checklist e decisão; ações de registro e deploy são instruções ao humano. Infra e CI/CD ficam em `devops-cloud-infra`; SLO e alertas de plataforma em `sre-observability`; ETL e lineage em `data-engineering`. Lacunas: serving oficial (FastAPI/BentoML/MLflow serving), persistência segura (sklearn `model_persistence`, skops), pandera e Great Expectations não lidos. Os trechos de código são de redação própria e **não foram executados** (confira API na versão instalada).

## Sumário
1. Registro de runs (checklist por run)
2. Registro e promoção de modelos
3. Checklist de serving e regra de pickle
4. Training-serving skew e prontidão de ML
5. Monitoramento de drift
6. Decisão de promoção
7. Model card e moldura de risco
8. Notebooks e estrutura de projeto
9. Roteiro único de validação (sem comando nesta versão)

## 1. Registro de runs (V-22)

Por run: **hash dos dados · commit + flag de diretório sujo · lockfile · seed · parâmetros (hiperparâmetros) · métricas por fold e finais · artefatos · ambiente**. Logue sempre dentro de um contexto de run (Inferido de listagens de terceiros).

```python
import subprocess, mlflow

def git_state():
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], text=True).strip())
    return sha, dirty

with mlflow.start_run():
    sha, dirty = git_state()
    mlflow.set_tags({"git_sha": sha, "git_dirty": str(dirty), "data_hash": DATA_SHA256})
    mlflow.log_params({"seed": SEED, **hyperparams})
    mlflow.log_metrics({"auc_val_mean": auc_mean, "auc_val_std": auc_std})
```
O exemplo MLflow da skill de terceiros registrava só o SHA, sem a flag de diretório sujo; o exemplo W&B omitia dados e ambiente. `mlflow --version` primeiro: a API muda (a alegação de que `artifact_path` está obsoleto é Não verificada).

## 2. Registro e promoção de modelos (V-22)

- Registre com `registered_model_name` em `log_model` ou `mlflow.register_model`; cada registro incrementa a **versão**.
- Aponte produção por **alias** (ex.: `champion`) e carregue por URI `models:/<nome>@<alias>` ou `models:/<nome>/<versão>`; **nunca por `run_id`** em código de produção.
- Assinatura: `set_signature()` pode ser adicionada depois; a **exigência** de assinatura é do Unity Catalog (Databricks), não do MLflow OSS.
- A página de registry ainda cita stages no trecho OSS e **não** declara stages obsoletos: não afirme obsolescência.
- Controle quem promove (permissão no registry); a decisão é humana (modelo `decisao-de-promocao.md`).

## 3. Checklist de serving (V-23, fonte classe C corrigida)

- [ ] Salvar o **pipeline completo** (pré-processamento + modelo), não só o estimador.
- [ ] Carregar o modelo **uma vez** na inicialização, não por requisição.
- [ ] Validar o payload (esquema, tipos, faixas); erro 422 com mensagem clara.
- [ ] Devolver `model_version` na resposta.
- [ ] Endpoints de **health** e **readiness** (a fonte original pedia readiness mas só implementava `/health`).
- [ ] Timeouts e limite de tamanho de entrada.
- [ ] Pré-processamento **idêntico** ao do treino (mesmo código).
- [ ] Autenticação e limite de taxa em endpoint público.
- [ ] Monitorar latência p50/p95/p99, erros e drift.
- [ ] **Nunca carregar `pickle`/`joblib` de origem não confiável:** a desserialização pode executar código arbitrário. Vale também para `torch.load` sem `weights_only=True` (Inferido). O artefato vem de um registro próprio, com acesso controlado e integridade verificável; nunca de bucket gravável por terceiros (cenário do caso E-07).
- [ ] Segredos por variável de ambiente ou cofre, nunca no artefato ou na imagem.
Alegações de benchmark da fonte ("ONNX + quantização dá 2 a 4 vezes") não têm medição: não as repita; o snippet ONNX da fonte ignorava o pré-processamento.

## 4. Training-serving skew e prontidão de ML (V-31)

Checklist (guia *Rules of Machine Learning*, Google, atualizado em 2025-08-25, e Sculley et al., 2015):
- [ ] Métrica definida **antes** do modelo; heurística como baseline (lance sem ML se bastar).
- [ ] Modelo simples; infraestrutura testada independentemente do ML.
- [ ] Corte temporal no teste (Regra 33): treine até uma data, teste depois.
- [ ] **Mesmo código de features** em treino e serving; **logue as features no serving** e compare com as do treino (skew; regras 29 a 32 e 37).
- [ ] Dono e documentação por coluna; frescor dos dados e falhas silenciosas monitorados.
- [ ] Laços de realimentação identificados (o modelo muda os dados futuros).
- [ ] Dívida técnica: fronteiras erodidas, entrelaçamento, consumidores não declarados, dependências de dados e de configuração, mudanças no mundo externo.
O guia tem partes específicas de ranking e recomendação.

## 5. Monitoramento de drift (V-24)

Checklist:
- [ ] **Baseline** de features e predições salvo antes do deploy.
- [ ] Janelas de referência e atual **por tempo**.
- [ ] Colunas numéricas e categóricas **declaradas**.
- [ ] Testes por tipo: PSI/KS para numéricas, qui-quadrado para categóricas, com limiares documentados como **convenção** (PSI 0,1/0,2 são convenção, não verdade).
- [ ] Separar drift de **entrada**, de **predição** e de **qualidade** (esta quando os rótulos chegam). Drift estatístico não prova perda de desempenho.
- [ ] Amostras grandes: olhar o **tamanho de efeito** além do p-valor e corrigir múltiplos testes.
- [ ] Cada alerta tem **dono e ação**; revisão periódica mesmo sem alerta (AWS ML Lens, MLOPS01-BP03).
- [ ] Retreino automático **só com revisão humana**.
- [ ] Versão da biblioteca fixada e API conferida.
Antipadrões da AWS: sem métrica de negócio, sem plano de ação, monitoramento irregular, sem limiar. Evidently (versão não declarada na página lida; V-24 cita 0.7+): `Dataset.from_pandas` com `DataDefinition` explícito, `Report([DataDriftPreset()])`, `report.run(current, reference)` — confira a API instalada.

```python
import numpy as np

def psi(ref, cur, bins=10, eps=1e-6):
    edges = np.unique(np.quantile(ref, np.linspace(0, 1, bins + 1)))   # quantis podem duplicar: deduplicar
    edges[0], edges[-1] = -np.inf, np.inf
    e = np.histogram(ref, edges)[0] / len(ref) + eps
    a = np.histogram(cur, edges)[0] / len(cur) + eps
    return float(np.sum((a - e) * np.log(a / e)))
```
PSI com quantis pode gerar bins degenerados em variáveis com muitos valores repetidos; a função da skill de terceiros ainda assumia acurácia 0,9 quando faltava dado e ignorava `min_days_since_last_train`: não copie lógica de retreino automático.

## 6. Decisão de promoção (V-25; modelo `assets/templates/decisao-de-promocao.md`)

**BLOCK** se houver: vazamento plausível; split sem tempo/grupo quando deveria; feature indisponível na decisão; promoção não reproduzível; critérios definidos depois de ver o teste; serving divergente do treino; sem plano de rollback; segredo ou PII em artefato; avaliação sem baseline ou sem fatias relevantes. **WARN**: calibração não medida, latência ou custo sem meta, monitoramento sem dono, documentação incompleta. **APPROVE** exige: nenhum bloqueador, critérios declarados antes da seleção, baseline e modelo atual comparados. Itens inacessíveis ao revisor: NÃO VERIFICÁVEL. O agente `ds-model-promotion-reviewer` aplica isto em contexto novo e somente leitura.

## 7. Model card e moldura de risco (V-32)

Campos **propostos pelo validador (Inferido; a lista oficial de seções de Mitchell et al. não foi lida)**: uso pretendido e não recomendado; dados de treino e avaliação com datas e janelas; métricas **por fatia** com intervalos; calibração; limitações conhecidas; riscos e mitigação; responsável, versão e data; link do run de origem (`assets/templates/model-card.md`). NIST AI RMF 1.0 (2023-01-26): as funções **Govern, Map, Measure, Manage** servem de moldura; os nomes só foram confirmados no texto alternativo de uma imagem da página, e o documento completo não foi lido: não gere requisitos específicos do NIST. Conformidade jurídica (LGPD, AI Act) está fora do escopo: `security-appsec` e assessoria jurídica.

## 8. Notebooks e estrutura de projeto (V-33, V-10)

Checklist de notebook:
- [ ] Rodar **do início ao fim em ambiente limpo** antes de confiar no resultado; ordem das células verificada (contador de execução monotônico).
- [ ] Seções claras; lógica estável em módulos (`src/`); o notebook importa.
- [ ] Dependências registradas em lockfile.
- [ ] Notebook versionado (considere pareamento com `.py`, por exemplo com jupytext) para diffs legíveis.
- [ ] Dados brutos imutáveis; saídas rastreáveis (caminho e hash).
- [ ] **Regra para o agente:** ele edita o notebook; o resultado só vale após execução completa pelo usuário ou por comando do projeto. A alegação "o Claude Code não executa células" veio de fornecedor e é Não verificada; trate como regra de processo, sem alegação técnica sobre Jupyter.
Estrutura (Cookiecutter Data Science v2): `data/{raw,interim,processed,external}`, pacote de código com `dataset.py`, `features.py`, `modeling/`, notebooks numerados com iniciais, `Makefile`; `data/raw` imutável. As "dez regras" de Rule et al. (arXiv 1810.08055) não foram lidas: não as atribua.

## 9. Roteiro único de validação (V-30) (comando `ds-validate` planejado, não incluído nesta versão)

Uma definição de tarefa do projeto (ex.: `make validate`), igual local, em hook e em CI, que roda tipos, lint (com `select` explícito), testes, varredura de segredos e de dependências, e valida DataFrames (pandera). Falha se qualquer etapa falhar. O comando do plugin lê o `CLAUDE.md`/Makefile, **pergunta antes de executar** se o comando for desconhecido, executa uma vez, cola a saída e não instala nada. Stack do autor da fonte (Python 3.14, uv, mise) é específico: não presuma. `TRIVY_CONFIG` exportado pode sobrescrever a política: passe `--config`. Autoverificação mínima (lista do plugin, não da fonte), 7 itens: tipos, lint, testes, segredos, dependências, formato dos dados, e o estado do `git` (sem arquivos não rastreados indevidos).
