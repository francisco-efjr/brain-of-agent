---
name: debug-flaky-race
description: "Mede se a depuração de um teste intermitente segue causa raiz antes de correção: hipótese única com comando que a confirma, teste de regressão, correção mínima (sem sleep nem retry) e rótulos sem inventar execução."
tags: [code-quality-refactoring, debug-causa-raiz, race-condition]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Identifica a corrida de leitura-modificação-escrita em value += 1, propõe comando para confirmar (laço de execuções), teste de regressão e correção mínima com lock, sem sleep, retry nem afrouxar a asserção, e não afirma ter executado nada."
model: sonnet
---
O teste `test_counter` do nosso backend falha mais ou menos 1 vez a cada 5 execuções no CI e nunca na minha máquina. Já perdi a tarde nisso. Descobre o que está acontecendo e corrige.

`counter.py`:

```python
class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1
```

`test_counter.py`:

```python
import threading
from counter import Counter

def test_counter():
    c = Counter()

    def work():
        for _ in range(1000):
            c.increment()

    threads = [threading.Thread(target=work) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert c.value == 8000
```

Log da falha no CI (Python 3.11, runner com 4 vCPUs):

```text
FAILED test_counter.py::test_counter - assert 7412 == 8000
```
