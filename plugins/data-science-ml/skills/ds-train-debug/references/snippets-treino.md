# Snippets de treino PyTorch: seeds, DataLoader, loop com AMP, checkpoint

Validado em 2026-10-10 contra a documentação do PyTorch 2.14 (notas de reprodutibilidade) e o padrão de skills lidas em V-20. Os snippets são esqueletos: variáveis como `model`, `train_ds`, `criterion`, `cfg`, `device` vêm do projeto. Não foram executados (Não verificado). Confira `torch.__version__`: namespaces `torch.amp.*` são os atuais; `torch.cuda.amp.*` está em desuso nas versões recentes (Inferido).

## Sumário
1. Seeds e determinismo
2. DataLoader reprodutível
3. Loop com AMP, clipping e validação
4. Checkpoint completo e retomada
5. Teste de sobreajustar um batch
6. Comandos de ambiente

## 1. Seeds e determinismo

```python
import os, random
import numpy as np
import torch

def seed_everything(seed: int, deterministic: bool = True) -> torch.Generator:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)                 # cobre CPU e CUDA
    if deterministic:
        torch.use_deterministic_algorithms(True)   # erro em operações sem versão determinística
        torch.backends.cudnn.benchmark = False
        # torch.backends.cudnn.deterministic = True  # afeta só o cuDNN; redundante com a linha acima
    g = torch.Generator()
    g.manual_seed(seed)
    return g
```

`PYTHONHASHSEED` não se define aqui: precisa existir no ambiente **antes** de iniciar o interpretador.

```bash
# bash
PYTHONHASHSEED=0 python train.py --config configs/base.yaml
# PowerShell
$env:PYTHONHASHSEED = "0"; python train.py --config configs/base.yaml
```

Em GPU, algumas operações exigem uma variável de ambiente adicional para serem determinísticas (`CUBLAS_WORKSPACE_CONFIG`). A página de randomness do PyTorch 2.14 consultada em V-20 não a cita: confirme na documentação de CUDA/`use_deterministic_algorithms` da sua versão antes de depender dela (Não verificado).

Declare no relatório: `torch`, CUDA, driver, GPU e a tolerância de reprodução (por exemplo, "AUC de validação dentro de ±0,002 entre três execuções").

## 2. DataLoader reprodutível

```python
from torch.utils.data import DataLoader

def seed_worker(worker_id: int):
    s = torch.initial_seed() % 2**32
    np.random.seed(s)
    random.seed(s)

g = seed_everything(cfg.seed)
train_loader = DataLoader(train_ds, batch_size=cfg.batch_size, shuffle=True,
                          num_workers=4, worker_init_fn=seed_worker, generator=g,
                          pin_memory=(device.type == "cuda"))
```

Sem `generator` e `worker_init_fn`, a ordem e a augmentation por worker variam entre execuções (V-20, Verificado na documentação).

## 3. Loop com AMP, clipping e validação

```python
use_amp = device.type == "cuda"
scaler = torch.amp.GradScaler("cuda", enabled=use_amp)   # fp16; para bf16 não é necessário (Inferido)

for epoch in range(start_epoch, cfg.epochs):
    model.train()
    for x, y in train_loader:
        x, y = x.to(device, non_blocking=True), y.to(device, non_blocking=True)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type=device.type, dtype=torch.float16, enabled=use_amp):
            loss = criterion(model(x), y)
        scaler.scale(loss).backward()
        scaler.unscale_(opt)                                   # antes do clipping
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        scaler.step(opt)
        scaler.update()
    scheduler.step()          # scheduler por época; OneCycleLR e afins avançam por lote, dentro do loop

    model.eval()
    val_loss, n = 0.0, 0
    with torch.no_grad():
        for x, y in val_loader:
            x, y = x.to(device), y.to(device)
            val_loss += criterion(model(x), y).item() * len(y)
            n += len(y)
    print(f"epoch {epoch} val_loss {val_loss / n:.4f}")
```

Pontos de revisão: `zero_grad` a cada passo; `train()`/`eval()` alternados; `no_grad()` na validação; `unscale_` antes do clipping; métrica de validação calculada em modo `eval()`.

## 4. Checkpoint completo e retomada

```python
def save_checkpoint(path, epoch, model, opt, scheduler, scaler, generator, cfg, extra=None):
    torch.save({
        "epoch": epoch,
        "model": model.state_dict(),
        "optimizer": opt.state_dict(),
        "scheduler": scheduler.state_dict(),
        "scaler": scaler.state_dict(),
        "generator": generator.get_state(),
        "rng": {
            "python": random.getstate(),
            "numpy": np.random.get_state(),
            "torch": torch.get_rng_state(),
            "cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None,
        },
        "config": cfg,
        **(extra or {}),          # ex.: hash dos dados, commit, lockfile
    }, path)

def load_checkpoint(path, model, opt, scheduler, scaler, generator, device):
    # weights_only=False porque o arquivo guarda estados de RNG de Python/NumPy: carregue SÓ checkpoints próprios.
    ckpt = torch.load(path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"]); opt.load_state_dict(ckpt["optimizer"])
    scheduler.load_state_dict(ckpt["scheduler"]); scaler.load_state_dict(ckpt["scaler"])
    generator.set_state(ckpt["generator"])
    random.setstate(ckpt["rng"]["python"]); np.random.set_state(ckpt["rng"]["numpy"])
    torch.set_rng_state(ckpt["rng"]["torch"].cpu())
    if ckpt["rng"]["cuda"] is not None:
        torch.cuda.set_rng_state_all([s.cpu() for s in ckpt["rng"]["cuda"]])
    return ckpt["epoch"] + 1
```

Salvar só `state_dict` do modelo não permite retomar o treino de forma equivalente: faltam otimizador, scheduler, scaler e RNG. `torch.load` com `weights_only=False` usa pickle e executa código na desserialização: nunca para arquivo de origem não confiável.

## 5. Teste de sobreajustar um batch

```python
model.train()
x, y = next(iter(train_loader))
x, y = x.to(device), y.to(device)
opt = torch.optim.AdamW(model.parameters(), lr=1e-3)    # lr razoável; sem dropout/augmentation neste teste
for step in range(200):
    opt.zero_grad(set_to_none=True)
    loss = criterion(model(x), y)
    loss.backward()
    opt.step()
    if step % 20 == 0:
        print(step, loss.item())
```

Desligue dropout (`model.eval()` desliga dropout mas também congela BatchNorm; se o modelo tem BN, zere `p` dos dropouts em vez de usar `eval()`). Resultado é indício: a loss pode estabilizar acima de zero e não cair por causas além do wiring (lr, passos, capacidade, ruído de rótulo).

## 6. Comandos de ambiente (registre a saída no relatório)

```bash
python -c "import sys, numpy, torch; print(sys.version); print(torch.__version__, torch.version.cuda, torch.cuda.is_available(), numpy.__version__)"
pip freeze > reports/pip-freeze.txt     # ou o lockfile do projeto (uv.lock, poetry.lock, conda-lock)
git rev-parse HEAD && git status --porcelain
```

Lockfile completo vale mais que `requirements.txt` direto; registre hash dos dados (`sha256sum data/processed/train.parquet` ou equivalente).
