# Template: handoff e checkpoint

Adaptado de `brains/fullstack/assets/templates/handoff-checkpoint.md` do brain-of-agent (conteúdo próprio do autor, MIT), com campos de git. Gere antes de a janela de contexto encher ou antes de pausar.

Objetivo/escopo autorizado:
Ações externas já autorizadas (push, PR, merge, tag, release) e as que ainda dependem de confirmação:
Revisão atual (`git rev-parse HEAD`), branch, base e ambiente (`git --version`, `gh auth status`):
Estado do workspace (`git status --short`), stashes, worktrees e mudanças preservadas:
Leituras completas/parciais/ausentes e retomada:
Fontes de verdade e decisões (estilo de commit, método de merge, política de versão):

| Item | Estado | Alteração | Evidência | Limitação/próxima ação |
| --- | --- | --- | --- | --- |

Comandos executados, resultados e primeira falha:
Dados/integrações usados e limpeza necessária (branches de segurança, worktrees temporários):
Checks invalidados por mudanças posteriores (CI de SHA antigo, testes anteriores à última edição):
Pendências, riscos e impedimentos:
Próxima ação concreta:

Ao retomar, confirme revisão e workspace antes de assumir que este estado continua válido. Não incluir segredos ou dados pessoais desnecessários.
