---
name: pytorch-overfit-um-batch
description: Caso de disparo e de robustez. Mede se o plugin diagnostica uma loss PyTorch parada em ln(10) listando várias causas candidatas no código (zero_grad ausente, modelo preso em eval depois da validação, taxa de aprendizado 1e-7, poucas épocas), propõe sobreajustar um batch como indício e não declara causa única como certa.
tags: [data-science-ml, ds-train-debug, pytorch, debugging, training-loop]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Isola a camada de otimização, lista causas candidatas observáveis no código (sem zero_grad, evaluate deixa o modelo em eval e o loop não volta a train, learning rate 1e-7, poucas épocas, dropout 0,5 quando em modo de treino), propõe sobreajustar um único batch como indício com causas alternativas e uma mudança por vez, e não declara uma causa única como certa nem afirma ter rodado."
model: sonnet
---
Meu classificador de 10 classes não aprende: a loss fica em 2,30 nas 3 épocas e a acurácia de validação em torno de 10%. Já conferi que os dados carregam certo (imagens achatadas em vetores de 64 posições e rótulos de 0 a 9). Estou perdido, o que há de errado com o loop?

```python
import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(64, 128), nn.ReLU(), nn.Dropout(0.5), nn.Linear(128, 10)
)
opt = torch.optim.Adam(model.parameters(), lr=1e-7)
loss_fn = nn.CrossEntropyLoss()

def evaluate(model, loader):
    model.eval()
    correct = 0
    with torch.no_grad():
        for x, y in loader:
            correct += (model(x).argmax(1) == y).sum().item()
    return correct / len(loader.dataset)

for epoch in range(3):
    acc = evaluate(model, val_loader)
    for x, y in train_loader:
        loss = loss_fn(model(x), y)
        loss.backward()
        opt.step()
    print(epoch, loss.item(), acc)
# saída: 0 2.3031 0.101 / 1 2.3028 0.099 / 2 2.3026 0.100
```

Não consigo rodar nada agora; me diga o que você enxerga no código e o que eu deveria testar, em ordem.
