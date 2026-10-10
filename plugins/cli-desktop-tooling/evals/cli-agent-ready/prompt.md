---
name: cli-agent-ready
description: Mede se a revisão de uma CLI Python aponta prompt bloqueante, destrutivo sem flag, erro em stdout com exit 0 e falta de contrato para agente e CI, sem executar a CLI.
tags: [cli-desktop-tooling, cli-design-review, cli]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: Relatório com achados e evidência, proposta de flags, stderr e tabela de exit codes, rótulos epistêmicos e declaração de que a CLI não foi executada.
model: sonnet
---

Vou colocar essa CLI de backup para ser usada por um agente de IA e por um job de CI. Revisa o design dela pra mim antes de eu publicar? O arquivo é o mytool.py:

```python
import os
import shutil
import sys


def delete_old(dest):
    for f in os.listdir(dest):
        if f.endswith(".bak"):
            os.remove(os.path.join(dest, f))


def main():
    dest = input("Destino do backup: ")
    resp = input("Apagar backups antigos? (s/n) ")
    try:
        shutil.copytree("data", os.path.join(dest, "data"))
        if resp == "s":
            delete_old(dest)
        print("Backup ok!!!")
    except Exception as e:
        print("Erro:", e)
    sys.exit(0)


if __name__ == "__main__":
    main()
```
