# Treino, tuning e depuração de modelos

Validado em 2026-10-10 (documentação do PyTorch 2.14, LightGBM e XGBoost stable). Fontes: V-19, V-20, V-21 (ver `fontes.md`); trechos de terceiros foram corrigidos pelo validador e **os snippets abaixo são de redação própria e não foram executados** (Suposição quanto à execução; confira nomes de API na versão instalada, por exemplo `torch.amp.GradScaler` e `lgb.early_stopping`). Lacunas: PyTorch AMP e checkpoint oficiais não lidos; CatBoost não pesquisado.

## Sumário
1. Isolar a camada do problema
2. Árvore sintoma → causa
3. Ordem do passo de treino em PyTorch
4. Teste de sobreajustar um batch (indício)
5. Reprodutibilidade
6. Checkpoint completo
7. Tuning em 9 itens
8. Gradient boosting
9. Registro das mudanças

## 1. Isolar a camada

Bugs de ML são falhas silenciosas: o código roda e o número parece plausível. Pergunte, nesta ordem: o problema está em **dados** (rótulos, vazamento, normalização, pipeline de carga), em **otimização** (lr, loss, gradiente, inicialização, modo train/eval) ou em **generalização** (capacidade, regularização, distribuição)? Mude **uma coisa por vez** e registre.

## 2. Árvore sintoma → causa (roteiro, não verdade; fonte classe C corrigida)

| Sintoma | Causas candidatas (várias; teste cada uma) | Primeiro teste |
| --- | --- | --- |
| Loss vira NaN | lr alto; log/divisão de zero; dado com NaN/inf; AMP sem escala; gradiente explosivo | `torch.isfinite` em entrada e loss; clipping; reduzir lr |
| Loss não cai | lr baixo demais; `zero_grad` ausente; rótulos embaralhados; dropout/augmentation fortes; poucos passos; otimizador sem parâmetros | Sobreajustar um batch (seção 4); conferir `optimizer.param_groups` |
| Treino bom, validação ruim | overfitting; vazamento invertido (validação com distribuição diferente); `model.eval()` esquecido; normalização diferente | Comparar estatísticas treino × validação; conferir `eval()` |
| Métrica alta demais | vazamento; duplicatas; rótulo na feature | `ds-leakage-audit` |
| Métrica no nível do acaso | rótulos desalinhados com as features; bug de indexação; lr; dados constantes | Conferir alinhamento em um exemplo manual |
| Loss estabiliza acima de zero | ruído de rótulo, capacidade, regularização | Esperado em dados ruidosos; não é bug por si |
Afirmação do tipo "LR errada causa a maioria das falhas" não tem fonte: não use.

## 3. Ordem do passo de treino em PyTorch (V-20)

```python
model.train()
for xb, yb in train_loader:
    xb, yb = xb.to(device), yb.to(device)
    optimizer.zero_grad(set_to_none=True)
    with torch.autocast(device_type="cuda", dtype=torch.float16):
        loss = loss_fn(model(xb), yb)
    scaler.scale(loss).backward()
    scaler.unscale_(optimizer)                       # antes do clipping
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    scaler.step(optimizer)
    scaler.update()
    scheduler.step()                                  # se o scheduler for por passo

model.eval()
with torch.no_grad():
    ...  # validação; nunca ajustar nada aqui
```
Pontos: `scaler = torch.amp.GradScaler("cuda")` criado antes do loop (namespace `torch.amp`; confira a versão). Sem GPU/AMP, o loop é `zero_grad` → forward → `backward` → clipping → `step`. Validação sempre com `eval()` e `no_grad()`. Dados e modelo no mesmo device.

## 4. Teste de sobreajustar um batch (~200 passos): é indício

Treine só em um batch pequeno por cerca de 200 passos com regularização desligada. Interpretação:
- **Não sobreajusta**: suspeite de fiação de modelo/loss/rótulos, **mas também** de lr baixo, poucos passos, dropout/augmentation ligados ou capacidade pequena.
- **Sobreajusta, mas não generaliza**: pode ser otimização ou regularização, mas também ruído de rótulo, capacidade ou qualidade dos dados.
A perda pode estabilizar acima de zero. Nunca declare causa única sem um experimento que a confirme ou refute (V-19).

## 5. Reprodutibilidade (V-20)

Critério de aceite: reexecutar com a mesma configuração reproduz a métrica **dentro de uma tolerância declarada** (ex.: |Δ AUC| ≤ 0,005 entre 3 reexecuções), não "exatamente" em hardware diferente. O PyTorch não garante resultados totalmente reprodutíveis entre versões, commits, plataformas ou entre CPU e GPU.

```python
import os, random, numpy as np, torch

def seed_everything(seed: int) -> torch.Generator:
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)   # manual_seed cobre CPU e CUDA
    torch.use_deterministic_algorithms(True)                            # erro em ops sem versão determinística
    g = torch.Generator(); g.manual_seed(seed)
    return g

def seed_worker(worker_id: int):
    s = torch.initial_seed() % 2**32
    np.random.seed(s); random.seed(s)

# loader = DataLoader(ds, batch_size=64, shuffle=True, num_workers=4,
#                     worker_init_fn=seed_worker, generator=g)
```
Checklist:
- [ ] Seeds em `random`, NumPy e torch.
- [ ] `PYTHONHASHSEED` definido **no ambiente antes de iniciar o Python** (`PYTHONHASHSEED=0 python train.py`); atribuí-lo dentro do processo não tem efeito.
- [ ] `use_deterministic_algorithms(True)`; em GPU, `CUBLAS_WORKSPACE_CONFIG` (Não verificado: a página de randomness lida não a menciona; conferir na doc do PyTorch/CUDA da sua versão). `cudnn.deterministic` afeta só o cuDNN.
- [ ] `generator` e `worker_init_fn` no DataLoader.
- [ ] Seed inteira nos splitters e no sampler de tuning.
- [ ] Lockfile **completo** (não só `requirements.txt` direto), hash dos dados e commit registrados.
- [ ] Tolerância declarada e 3 reexecuções medidas, se o orçamento permitir.

## 6. Checkpoint completo

Para retomar treino exatamente: estado do **modelo, otimizador, scheduler, scaler de AMP, época/passo e estado dos RNGs** (`torch.get_rng_state()`, `torch.cuda.get_rng_state_all()`, `np.random.get_state()`, `random.getstate()`). A skill de terceiros lida salvava só modelo, otimizador e época. Nunca carregue checkpoint de origem não confiável: `torch.load` usa pickle (use `weights_only=True` quando o conteúdo for só tensores; Inferido, confirme na doc da versão).

## 7. Tuning em 9 itens (V-21)

1. O **Pipeline inteiro** está dentro da CV.
2. Escala logarítmica para taxa de aprendizado e regularização.
3. Espaço largo primeiro; depois estreitar.
4. `n_estimators` por early stopping em **validação separada do teste**.
5. Seeds no sampler e no splitter.
6. `n_trials` e `timeout` limitados.
7. Apenas 3 a 5 parâmetros.
8. Mesma CV ao comparar com e sem tuning.
9. Teste tocado **uma vez**, ao fim.
Poda no Optuna exige `trial.report()` e `trial.should_prune()` **durante** o treino; `cross_val_score` devolve só a média final e não suporta poda.

```python
def objective(trial):
    lr = trial.suggest_float("lr", 1e-4, 1e-1, log=True)
    model, opt = build(lr)
    for epoch in range(max_epochs):
        train_one_epoch(model, opt)
        val = evaluate(model, val_loader)      # validação, nunca teste
        trial.report(val, epoch)
        if trial.should_prune():
            raise optuna.TrialPruned()
    return val
```
Não prometa "ganho de X%" com tuning (a alegação "5 a 15%" não tinha fonte).

## 8. Gradient boosting (LightGBM e XGBoost, docs stable)

| Biblioteca | Parâmetros-chave | Notas verificadas |
| --- | --- | --- |
| LightGBM | `num_leaves` (abaixo de `2^max_depth`), `min_data_in_leaf`, `feature_fraction`, `bagging_fraction`, `learning_rate` | `min_data_in_leaf` é guarda contra overfitting; early stopping exige conjunto de validação |
| XGBoost | `max_depth`, `min_child_weight`, `gamma`, `subsample`, `eta` | Desbalanceamento: `scale_pos_weight` (AUC) ou, se probabilidades importam, não rebalancear e usar `max_delta_step` finito |
Early stopping: o conjunto de validação do `eval_set` **não pode ser o teste**. Com muitas dobras, fixe `n_estimators` pela mediana do early stopping nas dobras e retreine, ou use early stopping dentro de cada dobra com validação interna.

## 9. Registro das mudanças

Para cada hipótese: o experimento que a confirma ou refuta, o resultado e a decisão. Nenhuma alegação de ganho sem comparar com a **mesma CV**. Saída da skill `ds-train-debug`: diagnóstico ranqueado (hipótese · evidência · teste · correção) + checklist de reprodutibilidade preenchido. Execução de treino só com confirmação do usuário (custo, GPU, tempo).
