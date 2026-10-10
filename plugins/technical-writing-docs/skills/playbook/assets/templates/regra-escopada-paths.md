# Template: regra escopada em `.claude/rules/` com `paths:`

Fontes: V-01 (regras por caminho carregam quando o Claude trabalha com arquivos que casam; formato `paths:` do Claude Code), V-29 (estrutura bom/ruim e validação, do awesome-copilot, MIT; `applyTo` é do Copilot e não se transfere), V-18 (motivo e data). Use quando a regra só vale para um tipo de arquivo (por exemplo, documentação em `docs/`). Comece com poucas regras e adicione depois de falhas observadas.

Arquivo `.claude/rules/docs.md`:

````markdown
---
paths:
  - "docs/**/*.md"
  - "README.md"
---
# Regras para documentação

<!-- motivo: um quadrante por página evita texto misto | revisada: AAAA-MM -->
Cada documento tem um quadrante (tutorial, how-to, referência ou explicação). Declare-o no topo.

<!-- motivo: exemplo quebrado é pior que nenhum | revisada: AAAA-MM -->
Cada comando traz o resultado esperado. Se você não o executou, escreva "não executado".

## Exemplos

Bom:
- Título em caixa de frase: "Configurar o ambiente de desenvolvimento".

Ruim:
- Título genérico: "Informações".

## Validação

Abra um arquivo em `docs/` com a ferramenta Read e confira que a regra aparece no contexto; abra um arquivo fora do glob e confira que ela não aparece. Registre a versão do Claude Code usada no teste.
````

## Checklist

- [ ] O glob de `paths:` casa os arquivos certos (Glob) e nenhum outro.
- [ ] Cada regra tem motivo e data; cada proibição, alternativa.
- [ ] Teste feito com a ferramenta Read (regras aninhadas tiveram falhas de carregamento corrigidas nas versões 2.1.290 a 2.1.293; V-26).
