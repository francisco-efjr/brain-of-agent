# Handoff e checkpoint de documentação

Adaptado de `brains/fullstack/assets/templates/handoff-checkpoint.md` do repositório francisco-efjr/brain-of-agent (conteúdo do próprio usuário, licença MIT, Copyright (c) 2026 Brain of Agent contributors). Alteração: o campo "Dados/integrações usados" virou "Fontes de fatos e documentos lidos". Use em sessão longa, troca de contexto ou antes de uma janela encher. Sem segredos nem dados pessoais desnecessários.

```markdown
# Handoff e checkpoint

Objetivo/escopo autorizado:
Revisão atual e ambiente:
Estado do workspace e mudanças preservadas:
Leituras completas/parciais/ausentes e retomada:
Fontes de verdade e decisões:

| Item | Estado | Alteração | Evidência | Limitação/próxima ação |
| --- | --- | --- | --- | --- |

Comandos executados, resultados e primeira falha:
Fontes de fatos e documentos lidos (código, contratos, ADRs, tickets colados):
Checks invalidados por mudanças posteriores:
Pendências, riscos e impedimentos:
Dívida de documentação:
Próxima ação concreta:

Ao retomar, confirme revisão e workspace antes de assumir que este estado
continua válido. Não incluir segredos ou dados pessoais desnecessários.
```

## Uso no modo DOCS-COMPLETO

Preencha "Leituras completas/parciais/ausentes" com os 12 arquivos de `references/` (lote A, B, C) e liste em "Checks invalidados" qualquer linter, link ou exemplo revalidado antes de uma mudança posterior.
