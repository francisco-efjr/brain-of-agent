# Modelo: handoff de sessão (cinco campos)

Use ao concluir uma tarefa, antes de trocar de sessão ou de contexto (skill [context-engineering](../../../context-engineering/SKILL.md), seção Restartable Session Boundaries). Salve em [CAMINHO, ex.: `docs/handoff.md`]. A fronteira segura é uma **tarefa concluída**, não uma contagem de tokens. Commite só se o usuário ou o fluxo do repositório autorizar; senão deixe a árvore intacta e registre "não commitado".

```markdown
# Handoff: [PROJETO / TAREFA] · [AAAA-MM-DD HH:MM]

Autor: [agente e modelo] · Branch: [nome] · Base: [hash curto ou "não commitado"]

## 1. Escopo e decisões
- Escopo aceito: [link ou resumo da spec e da seção do plano]
- Decisões e razões: [D1: escolhi X porque Y; alternativa rejeitada: Z]
- Anotado e não feito (fora do pedido): [item e onde]

## 2. Status e próxima tarefa
- Feito: [T001 ✓ ...]
- Em andamento: [tarefa, o que falta]
- **Próxima tarefa:** [ID e nome, com o critério de aceite]

## 3. Arquivos e git
- Alterados: [caminho: o que mudou]
- Árvore: [commitado em <hash> | NÃO commitado: lista de arquivos]
- Remoto: [só local, sem push]

## 4. Verificação
| Comando | Resultado | Rótulo |
| --- | --- | --- |
| [comando exato] | [N testes verdes, 0 falhas] | Verificado, [HH:MM] |
| [comando que não rodou] | [motivo] | Não verificado |

Baseline registrado: [sim | não]. O que depende dele: [próxima tarefa que precisa refazer a verificação].

## 5. Abertos
- Perguntas ao humano: [...]
- Riscos: [...]
- Aprovações pendentes: [o quê, de quem]
- Aprovações dadas: [o quê, onde está registrado]. Só valem se estiverem registradas aqui ou na spec.

## Para a próxima sessão
Leia antes de agir: [regras: `CLAUDE.md`, `CONSTRAINTS.md`], [spec], [plano], este arquivo e o `git status` real. Refaça a verificação se o baseline não está registrado, se o código andou ou se a próxima tarefa depende dele. Não infira aprovação de uma conversa anterior.
```

## Checagem rápida

- [ ] Os cinco campos estão preenchidos; a próxima tarefa tem nome e critério de aceite.
- [ ] Cada comando de verificação tem resultado e rótulo; o que não rodou está como Não verificado.
- [ ] O estado do git é o real (`git status` conferido), não o lembrado.
- [ ] Nenhum segredo, valor de variável de ambiente ou dado pessoal no arquivo.
