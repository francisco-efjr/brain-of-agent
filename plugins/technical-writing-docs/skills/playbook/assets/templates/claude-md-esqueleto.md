# Template: CLAUDE.md (WHY / WHAT / HOW)

Fontes: V-15 (estrutura WHY/WHAT/HOW e `agent_docs/`), V-01 (limite de 200 linhas, comentários HTML removidos antes do contexto), V-18 (motivo e data), V-16 (cada proibição com alternativa). Regra do arquivo: só entra o que o agente **não descobre lendo o repositório**; abaixo de 200 linhas (preferência do plugin: 100 a 150). Este esqueleto é ponto de partida: apague seções vazias em vez de preenchê-las com conselho genérico. Em auditoria de arquivo existente, proponha diff (skill `auditar-claude-md`) em vez de sobrescrever.

````markdown
# [NOME DO PROJETO]

[WHY: propósito em uma frase.]

## Mapa

<!-- motivo: o agente não deduz a fronteira entre pacotes só pelo ls | revisada: AAAA-MM -->
- `[PASTA]`: [o que contém]
- `[PASTA]`: [o que contém]

## Comandos

<!-- motivo: comandos exatos evitam tentativa e erro | revisada: AAAA-MM -->
- Instalar: `[COMANDO]`
- Build: `[COMANDO]`
- Testes: `[COMANDO]` · um teste só: `[COMANDO COM EXEMPLO]`
- Lint e docs: `[COMANDO]`

## Convenções que divergem do padrão

<!-- motivo: [ERRO REPETIDO QUE ISTO EVITA] | revisada: AAAA-MM -->
- [CONVENÇÃO]. Use [ALTERNATIVA] em vez de [PROIBIDO].

## Armadilhas

<!-- motivo: [INCIDENTE OU ERRO OBSERVADO] | revisada: AAAA-MM -->
- [ARMADILHA NÃO DESCOBRÍVEL LENDO O CÓDIGO]. Ponteiro: `[arquivo:linha]`.

## Pronto quando

- [CRITÉRIO OBSERVÁVEL: teste, linter, build].

## Documentação de tarefa (sob demanda)

- `agent_docs/[ARQUIVO].md`: [descrição de uma linha de quando ler]
````

## Checklist

- [ ] Menos de 200 linhas; sem árvore de diretórios nem conselho genérico.
- [ ] Todo comando existe no manifesto/Makefile (Grep).
- [ ] Toda proibição traz alternativa; toda regra, motivo e data.
- [ ] Sem segredos.
- [ ] Depois de editar: `/doctor prompt-audit` e `/context` (recursos do produto; confira na sua versão).
