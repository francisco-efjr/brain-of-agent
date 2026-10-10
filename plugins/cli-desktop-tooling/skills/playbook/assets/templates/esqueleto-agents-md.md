# Esqueleto de AGENTS.md (e CLAUDE.md que o importa)

Baseado nas seções sugeridas pelo formato aberto (V-10) e nas regras de CLAUDE.md (V-06). Mantenha abaixo de 200 linhas e apague toda linha que o agente descobre lendo o repositório. Substitua os `[CMD]`; nenhum pode sobrar. Em monorepo, um arquivo por subprojeto (o mais próximo do arquivo editado vence); instrução explícita no chat sobrepõe o arquivo.

```markdown
# [NOME DO PROJETO]

## Visão geral
[Uma ou duas frases: o que é, quem usa, plataformas.]

## Setup (Windows/PowerShell)
- Shell: Windows PowerShell 5.1 (`$PSVersionTable`). Use cmdlets, não comandos Linux; bash só para `.sh` (Git Bash).
- Instalar dependências: `[CMD]`

## Comandos exatos
- Build: `[CMD]`
- Testes: `[CMD]` · um teste: `[CMD com filtro]`
- Lint: `[CMD]`
- Rode lint e testes antes de commitar e corrija até passar. Cole comando e saída ao dizer "pronto".

## Estilo e convenções que divergem do padrão
- [Somente o que o agente não infere do código.]

## Testes
- [Onde ficam; contrato da CLI (stdout, stderr, exit code) ou fluxo headless da TUI; como atualizar snapshots.]

## Segurança
- Segredos nunca em código, flags ou logs: [LOCAL DOS SEGREDOS].
- Não editar: [PASTAS GERADAS].
- Instalar ferramentas, assinar, notarizar, publicar e abrir PR só com confirmação do usuário.

## PR
- [Convenção de branch, commit e revisão.]
```

Ponte para o Claude Code: se o repositório tem `AGENTS.md`, o `CLAUDE.md` contém `@AGENTS.md` mais só o que é exclusivo do Claude (V-06). Sem `CLAUDE.md`, o Claude Code lê o `AGENTS.md` a partir da v2.1.277. Link simbólico no Windows é frágil: prefira o import.
