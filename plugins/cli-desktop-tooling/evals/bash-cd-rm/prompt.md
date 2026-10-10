---
name: bash-cd-rm
description: Mede se a revisão de um script sh aponta SC2086, SC2164 antes de rm -rf, SC2155, local e dupla de colchetes fora do POSIX, erro em stdout e trata set -e como rede parcial, sem executar o script.
tags: [cli-desktop-tooling, shell-script-review, bash, scripts]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: Achados com cenário, correção por item, nota sobre dialeto e set -e, e declaração de que o ShellCheck e o script não foram executados.
model: sonnet
---

Esse script de limpeza e build roda no CI e também no Git Bash dos devs. Pode revisar? Está no clean_build.sh:

```sh
#!/bin/sh
cd $1
rm -rf build/*
local out=$(make all)
[[ -f out.txt ]] && echo ok
echo "erro"
```
