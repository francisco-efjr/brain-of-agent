# Procedimento de gravação de ADR

Sumário: 1. Regras de nome e número · 2. Índice · 3. Supersessão passo a passo · 4. Diálogo de aprovação · 5. Casos de borda · 6. Gotchas

Validado em 2026-10-10. Fontes: V-12, V-13 (imutabilidade, supersessão), V-14 (numeração em 4 dígitos), V-15 (ADR existente só muda por proposta de diff), V-16 (pergunta antes de criar pasta, descarta se recusar), N-05 (MADR 4.0.0). Exemplos fictícios.

## 1. Regras de nome e número

| Regra | Detalhe | Exemplo |
| --- | --- | --- |
| Prefixo | `adr-` + número de 4 dígitos | `adr-0004-...` |
| Número | maior número presente + 1; nunca preencher buracos | existem 0001, 0002, 0005 -> próximo 0006 |
| Slug | ASCII minúsculo, hífens, sem acentos, até 60 caracteres, título nominal | "Fila de eventos para pedidos" -> `fila-de-eventos-para-pedidos` |
| Colisão | se o arquivo existe, parar e perguntar | nunca sobrescrever |
| Convenção local | se o projeto já usa `0004-titulo.md` ou outra pasta, seguir | avisar ao usuário |

Cálculo do maior número (com as ferramentas da skill): `Glob` em `<pasta>/adr-*.md`, extrair os 4 dígitos de cada nome, tomar o máximo. Se existir também um índice com número maior (ADR apagado depois de listado), use o maior dos dois.

## 2. Índice (`README.md` da pasta)

```markdown
# Architecture Decision Records

| Nº | Título | Status | Data | Confiança | Relação |
| --- | --- | --- | --- | --- | --- |
| [0001](<adr-0001-postgresql-banco-pedidos.md>) | PostgreSQL como banco do serviço de pedidos | substituído por 0004 | 2026-10-10 | média | |
| [0004](<adr-0004-banco-de-pedidos-particionado.md>) | Banco de pedidos particionado por tenant | proposto | 2026-11-02 | baixa | substitui 0001 |
```

Regras: uma linha por ADR, ordenada por número; status igual ao do arquivo; confiança igual ao campo do ADR; ao superseder, as duas linhas mudam no mesmo passo. Se o índice não existir, mostre-o inteiro no passo de aprovação.

## 3. Supersessão passo a passo

Cenário: ADR-0001 (aceito) será substituído por ADR-0004.

1. Verifique que o ADR-0001 está `aceito`. Se estiver `proposto`, é rascunho: edição normal, com permissão.
2. ADR novo: inclui no topo `Substitui: [ADR-0001](<adr-0001-postgresql-banco-pedidos.md>)` e, em Contexto, o que mudou desde a decisão antiga (gatilho de reavaliação atingido, requisito novo).
3. ADR antigo: troque somente a linha de status. Diff mostrado ao usuário antes:

```diff
- Status: aceito
+ Status: substituído por [ADR-0004](<adr-0004-banco-de-pedidos-particionado.md>)
```

4. Índice: duas linhas alteradas (0001 e 0004).
5. Releia os três arquivos; confirme que o corpo do ADR-0001 não mudou (`Grep` de uma frase do Contexto e da Decisão).

Caso inverso (descontinuado sem substituto): status `descontinuado`, com uma frase de motivo no próprio campo de status e data. Diga ao usuário que isso também é uma decisão e deve ter dono.

## 4. Diálogo de aprovação (modelo)

```text
Vou criar:
- docs/adr/adr-0004-banco-de-pedidos-particionado.md (conteúdo abaixo)
- docs/adr/README.md (+1 linha, diff abaixo)
- docs/adr/adr-0001-postgresql-banco-pedidos.md (só a linha de status, diff abaixo)
A pasta docs/adr/ já existe. Gravo estes arquivos? (sim/não)
```

Se a resposta for "sim, mas troque X", aplique a alteração, mostre de novo e pergunte de novo: aprovação vale para o conteúdo que o usuário viu.

## 5. Casos de borda

| Situação | Conduta |
| --- | --- |
| Pasta inexistente | Perguntar se pode criar `docs/adr/`; se não, descartar |
| Dois rascunhos aprovados de uma vez | Gravar na ordem apresentada, numerando em sequência; um diálogo de aprovação cobrindo todos |
| Rascunho com `[NEEDS CLARIFICATION]` | Gravar como `proposto` só se o usuário aprovar com os marcadores; senão devolver à skill `adr` |
| Usuário pede status `aceito` sem dizer quem decidiu | Perguntar o nome; sem nome, gravar `proposto` |
| ADR antigo não encontrado (`NNNN` inexistente) | Informar e não criar ADR novo com `Substitui:` quebrado |
| Repositório com ADRs em outro idioma | Manter o idioma e o formato do repositório |
| Falha ao gravar (permissão, disco) | Relatar o erro literal e não afirmar que gravou |

## 6. Gotchas

- Marcar `aceito` por conta própria transforma o assistente em decisor; a skill só registra o que o usuário afirmou.
- Link de supersessão sempre relativo e com nome de arquivo real; links quebrados passam despercebidos até alguém seguir a cadeia.
- Em monorepos com vários serviços, pergunte se os ADRs são por serviço ou globais antes de numerar.
- Não rode `git add` ou `git commit` aqui; o usuário decide o versionamento.
