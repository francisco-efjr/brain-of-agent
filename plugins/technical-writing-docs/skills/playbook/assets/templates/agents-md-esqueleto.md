# Template: AGENTS.md (cinco seções)

Fontes: AGENTS.md, formato aberto (https://agents.md/, repositório MIT; V-06) e V-48 (carregamento no Claude Code). Markdown puro. O AGENTS.md mais próximo do arquivo editado vence; o pedido explícito do usuário prevalece. O Claude Code (2.1.277 ou superior) lê AGENTS.md sozinho só quando não existe `CLAUDE.md`, `.claude/CLAUDE.md` nem `CLAUDE.local.md`; para usar os dois, crie `CLAUDE.md` com `@AGENTS.md` mais o que for específico do Claude. Mantenha só o que o agente não descobre lendo o repo.

````markdown
# AGENTS.md

## Visão geral

[Propósito do projeto em duas frases e as pastas que importam.]

## Comandos de build e teste

- Instalar: `[COMANDO]`
- Build: `[COMANDO]`
- Testes: `[COMANDO]`; um teste só: `[COMANDO COM EXEMPLO]`

## Estilo de código e documentação

- [CONVENÇÃO QUE DIVERGE DO PADRÃO]. Use [ALTERNATIVA] em vez de [PROIBIDO].
- Documentação: [GUIA DE ESTILO, linters: Vale, markdownlint, lychee e seus comandos].

## Testes

- [Onde ficam, como rodar o subconjunto relevante, o que não mockar.]

## Segurança

- Nunca commitar segredos; variáveis de ambiente em `[ARQUIVO DE EXEMPLO]`.
- [Ações que exigem confirmação humana: deploy, migração, publicação.]

## Pull requests

- Título no padrão [CONVENÇÃO]. Antes de abrir: `[COMANDOS]`. Documentação e CHANGELOG no mesmo PR quando o comportamento público muda.
````

## CLAUDE.md que importa o AGENTS.md

````markdown
@AGENTS.md

## Específico do Claude Code
<!-- motivo: [O QUE SÓ O CLAUDE CODE PRECISA] | revisada: AAAA-MM -->
- [REGRA]
````

Limite de saltos de `@imports`: quatro (V-01).
