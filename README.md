# Brain of Agent

Conhecimento por segmento combinado com workflows de agentes. Os segmentos próprios são **QA** e **desenvolvedor fullstack**. O projeto inclui uma cópia completa dos fontes do
[gstack](https://github.com/garrytan/gstack), com licenças e créditos preservados.

```text
brain-of-agent/
├── SKILL.md                 # entrada para selecionar recursos
├── brains/qa/               # qualidade, oráculos, risco, templates e helpers
├── brains/fullstack/        # desenvolvimento, arquitetura, implementação e validação
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

## Ativar o protocolo QA completo

Em um chat com acesso ao repositório, envie:

> QA-COMPLETO. Leia SKILL.md e aplique o protocolo ao projeto [caminho/objeto].
> Meu escopo é [auditar / implementar correções]. Entregue inventário de leitura,
> checklist de análise, implementação e revalidação, evidências e riscos pendentes.

A keyword exige leitura integral da base própria, cobertura de todas as áreas
e justificativa do que não se aplica. Não concede autorização para deploy ou
instalações. Sem acesso aos arquivos, anexe a base ou aceite cobertura parcial.

- [Protocolo](brains/qa/references/protocolo-qa-completo.md)
- [Checklist operacional](brains/qa/assets/templates/checklist-qa-completo.md)
- [Benchmark e avaliação](brains/qa/evals/README.md)
- [Validação operacional de integração](docs/runtime-validation.md)

As avaliações comportamentais são registradas separadamente dos testes de
helpers. Casos preparados e checks estruturais não equivalem a execuções de IA.

## Desenvolvedor fullstack e qualidade integrada

> FULLSTACK-COMPLETO. Leia SKILL.md e aplique o protocolo ao projeto [caminho].
> Implemente [objetivo] preservando [contratos]. Analise criticamente, corrija
> e revalide dentro do escopo. Entregue checklist, evidências e pendências.

- [Skill fullstack](brains/fullstack/SKILL.md)
- [Protocolo integral](brains/fullstack/references/protocolo-completo.md)
- [Checklist](brains/fullstack/assets/templates/checklist-fullstack-completo.md)
- [Pesquisa em fontes primárias](docs/research/agentes-desenvolvimento.md)
- [Benchmark fullstack](brains/fullstack/evals/README.md)

FULLSTACK-COMPLETO lê as bases próprias fullstack e QA em lotes, avalia todas
as áreas e aplica as pertinentes. A keyword não cria permissões nem impõe
stack. QA-COMPLETO continua adequado à avaliação; em pedido só de auditoria,
nenhum dos modos autoriza alterar o produto. Padrão Apple é referência de
acabamento adaptada à plataforma, não requisito de migrar para SwiftUI.

A exportação inclui todos os brains próprios e contexto compartilhado.
Casos de benchmark preparados, testes de ferramentas e revisão por IA
são evidências diferentes; não provam superioridade a QA ou a outro modelo.

Evidências iniciais: [forward-tests e limites](docs/validation/fullstack-forward-tests.md).
