---
name: readme-landing-page
description: Mede se o README da biblioteca pyslug abre com frase de valor e exemplo funcional, usa só fatos do pyproject colado, não inventa PyPI, badges nem URLs e marca a instalação como não executada.
tags: [technical-writing-docs, readme, escrever-readme]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega um README com frase de valor e exemplo funcional nas primeiras linhas, Quick Start copiável, instalação via pip install . a partir do repositório, licença MIT e comando slug vindos do pyproject, sem badges nem URLs inventados e com instalação marcada como não executada."
model: sonnet
---
Escreva o README da minha lib `pyslug`, que converte títulos em slugs para URL. O código está no GitHub, mas ainda não publiquei no PyPI: quem quer usar clona o repositório e roda `pip install .` na raiz. Não tenho site nem badges, é só o repositório.

Este é o `pyproject.toml`:

```toml
[project]
name = "pyslug"
version = "0.3.1"
description = "Convert titles into URL slugs"
requires-python = ">=3.9"
license = { text = "MIT" }
authors = [{ name = "Marina Duarte" }]

[project.scripts]
slug = "pyslug.cli:main"
```

O comando `slug` recebe o título como argumento e imprime o slug. Em Python o uso é assim:

```python
from pyslug import slugify
slugify('Olá Mundo')  # 'ola-mundo'
```

Pode entregar o README completo aqui na resposta.
