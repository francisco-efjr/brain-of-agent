# Brain of Agent

Conhecimento por segmento combinado com workflows de agentes. O primeiro
segmento é **QA**. O projeto inclui uma cópia completa dos fontes do
[gstack](https://github.com/garrytan/gstack), com licenças e créditos preservados.

```text
brain-of-agent/
├── SKILL.md                 # entrada para selecionar recursos
├── brains/qa/               # nossa skill, referências, templates, scripts e testes
├── vendor/gstack/           # snapshot integral dos arquivos do fornecedor
├── registry/                # catálogo e origem/hashes do snapshot
├── tools/                   # catálogo, integridade, importação e exportação
├── tests/                   # regressões da integração
└── docs/                    # arquitetura, uso e atualização
```

**QA** reúne técnica, risco, oráculos e evidência. **gstack** fornece workflows
de planejamento, revisão, investigação, execução de QA, documentação e entrega.
Nossa skill se chama `qa`; instale os workflows com prefixo `gstack-*` para
separar `qa` de `gstack-qa`.

Ferramentas próprias: Python 3.10+, com biblioteca padrão. Para usar o
conhecimento em qualquer IA, forneça
[brains/qa/SKILL.md](brains/qa/SKILL.md) e as referências pertinentes. Não é
necessário instalar ferramentas para ler a base.

```bash
python3 tools/catalog.py --list
python3 tools/export_project.py --host claude --target /caminho/do/projeto
# Alternativa para outro projeto:
python3 tools/export_project.py --host codex --target /outro/projeto
```

A exportação copia fontes e imprime a próxima etapa. Não executa setup nem
sobrescreve skills existentes. Veja [a integração](docs/integration.md).
O pacote gstack importado exige Bun **>= 1.4.0** para seu runtime.

```bash
python3 tools/verify.py
python3 -m unittest discover -s brains/qa/tests -v
python3 -m unittest discover -s tests -v
```

As verificações próprias cobrem a integração e os helpers QA. A conferência
do snapshot não significa execução da suíte inteira ou do runtime gstack.

Importação em **05/10/2026**: gstack **1.91.27**, commit
[`c285d88b90d39116ccfa2b901f80ea0fce0b26eb`](https://github.com/garrytan/gstack/commit/c285d88b90d39116ccfa2b901f80ea0fce0b26eb),
**3.133 arquivos versionados**, incluindo skills, fontes, testes, fixtures,
documentação e licenças. É um snapshot completo dos arquivos, sem a pasta
`.git` e o histórico upstream; não depende de submódulo ou novo clone para
obter os fontes. Novos segmentos entram em `brains/<segmento>/`.

Leia [a arquitetura](docs/architecture.md) e
[o procedimento de atualização](docs/upstream.md). Licença própria:
[MIT](LICENSE). Créditos externos: [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
