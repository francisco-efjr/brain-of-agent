# Decisões e trade-offs

Tabelas de decisão para as escolhas recorrentes do segmento. Cada uma traz critérios, recomendação padrão, quando inverter e o rótulo epistêmico. Fontes por ID em [fontes.md](fontes.md). Quando a decisão afeta a equipe, registre-a em ADR curto (plugin `architecture-design`) e linke no PR.

## Sumário

1. Fluxo de branching
2. Método de merge
3. Desfazer: revert, reset ou rebase
4. Estilo de commit
5. Changelog: humano ou gerado
6. Versão: MAJOR, MINOR, PATCH, 0.y.z, pré-release
7. Release: manual, release-please ou changesets
8. Monorepo: um changelog por pacote?
9. Worktree ou branch
10. PR único ou empilhado
11. Hook, `deny`, CLAUDE.md ou skill: onde colocar a regra
12. Revisão: quando acionar revisor LLM

## 1. Fluxo de branching (V-26, V-39; conflito C2)

| Critério | GitHub flow | Trunk-based |
| --- | --- | --- |
| Tamanho do time | Qualquer | Pequeno a médio |
| Deploy | Com janela ou sob demanda | Frequente (integração a cada 24 h) |
| Flags | Opcionais | Praticamente necessárias |
| CI | Por PR | Rápida, em toda integração |
| Revisão | Obrigatória por branch | Pode ser pós-merge ou em pares |

Padrão: **GitHub flow** com branches de horas a poucos dias. Inverta para trunk-based se há flags, CI rápida e deploy frequente. Em ambos: sem force push na principal e CI em toda integração. Rótulo: Inferido (fonte do trunk-based é classe C; sem dados DORA, G1). GitFlow com várias branches longas: sem fonte contrária pesquisada; trate release branches como lacuna G2.

## 2. Método de merge (V-27, V-33; conflito C7)

| Método | Vantagem | Custo | Quando |
| --- | --- | --- | --- |
| Squash | Histórico limpo; recomendado pelo release-please; indicado para branches curtas | Perde granularidade interna do PR | **Padrão** com PRs pequenos |
| Merge commit | Preserva todos os commits e o contexto | Histórico ramificado; cada commit precisa ser bom | Série longa de commits atômicos já conformes |
| Rebase and merge | Linear; SHAs novos | Descarta commits vazios; cada commit precisa ser Conventional | Time aceita histórico linear |

Rótulo: método por critério é Inferido; fatos de cada método são Verificados (V-27).

## 3. Desfazer (V-19, V-23, V-24, V-27)

| Situação | Ferramenta | Por quê |
| --- | --- | --- |
| Só local | `rebase`, `commit --amend` é evitado (use `--fixup`) | Ninguém depende do histórico |
| Publicada só por mim | Rebase + `--force-with-lease --force-if-includes` | Reescrita controlada; confirmação |
| Compartilhada ou protegida | `git revert` | Acrescenta histórico, não remove |
| Merge a desfazer | `git revert -m 1` | O pai 1 é a linha principal |
| Reaplicar merge revertido | Reverter o revert | Senão o Git considera as mudanças "nunca desejadas" |
| Trabalho não commitado a descartar | Pedir confirmação; preferir `git stash` ou branch | Descarte é irreversível |

## 4. Estilo de commit (V-18; conflito C1)

Padrão **Conventional Commits** (alimenta SemVer e release-please). Alternativa: regras curtas (Sanglard, classe C) sem integração de versão. Regra: detectar o estilo do histórico e do CLAUDE.md; **nunca misturar**. Mudar de estilo exige decisão do time e de um marco claro no histórico.

## 5. Changelog (V-32, V-33; conflito C6)

Humano (KaC) se o público é externo e as mudanças merecem narrativa; gerado (release-please) se há muitos commits regulares e disciplina de Conventional Commits. Nunca dois geradores no mesmo arquivo.

## 6. Versão (V-31)

| Pergunta | Resposta |
| --- | --- |
| Quebrou a API pública declarada? | MAJOR |
| Adicionou funcionalidade compatível? | MINOR |
| Só corrigiu compatível? | PATCH |
| É candidata? | `-rc.N` |
| Está em `0.y.z`? | Qualquer mudança pode quebrar; decida e documente o que isso significa para o projeto |
| Mudou só doc/CI/teste? | Sem release (com release-please) |

Pergunta-chave para o usuário quando a API pública não está declarada: "o que consumidores externos dependem de, exatamente?". Peça confirmação em MINOR e MAJOR.

## 7. Release: manual, release-please ou changesets (V-33, V-35)

| Opção | Escolha se | Cuidado |
| --- | --- | --- |
| Manual (skill `release-cut`) | Poucos releases, controle total, sem Conventional Commits disciplinado | Mais passos humanos |
| release-please | Conventional Commits + squash; um pacote ou manifesto | Não publica em pacotes; commits fora do padrão invisíveis; manifesto não lido (G3) |
| Changesets | Monorepo com versionamento por pacote | Comandos não confirmados (V-35) |

## 8. Monorepo (V-13, V-35; G3)

Um CHANGELOG por pacote publicado externamente; um CHANGELOG na raiz se há versão única. Prefixo de pacote nos commits; CODEOWNERS por caminho; CLAUDE.md por pacote. Rótulo: Inferido (a doc oficial não cobre release de monorepo).

## 9. Worktree ou branch

| Cenário | Escolha |
| --- | --- |
| Uma tarefa por vez | Branch simples |
| Duas ou mais sessões do Claude em paralelo, arquivos disjuntos | Worktrees (até 3, Suposição) |
| Bisect sem mexer no trabalho em andamento | Worktree temporário |
| Escopos que se sobrepõem | Não paralelizar: conflito certo |

## 10. PR único ou empilhado (V-29)

Empilhado se as partes dependem umas das outras e cada uma é revisável sozinha; único se cabe em ~100–400 linhas e um assunto. Se o time faz squash, use `--fixup` para tratar revisão. Rótulo: limiares Suposição.

## 11. Onde colocar a regra (PP-26, PP-38)

1. Precisa valer sempre? Regra `deny` ou hook (garantia).
2. Fato universal e curto do repositório? CLAUDE.md (< 200 linhas).
3. Fluxo de uma tarefa? Skill (com `disable-model-invocation` se tem efeito).
4. Papel isolado, somente leitura? Subagente.
5. Dado externo? MCP (documentado, desativado).

## 12. Revisão: quando acionar revisor LLM

| Diff | Revisão |
| --- | --- |
| Trivial (documentação, renome) | Dispensar o revisor; verificação basta |
| Funcional pequeno | `revisor-diff` (limiar 80) |
| Com plano ou critérios | `revisor-plano` (até 2 rodadas) |
| Segurança, dinheiro, dados | Humano obrigatório; `security-appsec` |
| Release | `auditor-release` (go/no-go) |
