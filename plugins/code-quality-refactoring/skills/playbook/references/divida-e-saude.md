# Dívida técnica, auditoria de testes, análise estática e painel de saúde

Sumário: 1 Quadrantes de dívida · 2 Prioridade por frequência x dor (com comandos) · 3 Registro de dívida · 4 Auditoria de testes que custam mais do que protegem · 5 Análise estática no fluxo · 6 Métricas como guia de onde olhar · 7 Painel de saúde somente leitura · 8 Exemplo de nota composta · 9 Lacunas · 10 Gotchas

Fontes: V-20 (Fowler: Technical Debt e Debt Quadrant), V-21 (Strangler), V-30 (auditoria de testes, ideia do gstack `/test-audit`), V-39 (Ruff, Tricorder, Sonar), BR-24 (ideia do `/health` do gstack, MIT, redação própria). Skills: `tech-debt-triage` e `code-health-report` (só por comando).

## 1. Quadrantes (V-20, redação própria)

Dois eixos: a dívida foi **deliberada** ou **inadvertida**, e a decisão foi **prudente** ou **imprudente**.

| Quadrante | Descrição | Ação típica |
| --- | --- | --- |
| Deliberada e imprudente | A equipe sabe que está criando bagunça e ignora as consequências | Parar de acumular; registrar e corrigir onde há frequência de mudança |
| Deliberada e prudente | Atalho consciente para entregar agora, com plano de pagar | Registrar dono e prazo; cobrar o prazo |
| Inadvertida e imprudente | Falta de conhecimento de práticas básicas; a equipe nem percebe o dano | Treinamento, revisão, regras no CLAUDE.md |
| Inadvertida e prudente | Só depois de entregar se aprende o desenho melhor | Refatorar quando a área voltar a mudar |

A metáfora de juros tem um limite: o juro vem do **uso**, não do tempo. Gasta-se mais tempo removendo "cruft" nas áreas modificadas com frequência; áreas feias mas estáveis podem ficar como estão (V-20).

## 2. Prioridade por frequência de mudança x dor

Prioridade = frequência de alteração na janela x dor ao mexer (Inferido de V-20; sem fonte para método quantitativo além de Fowler).

**Frequência** (somente leitura). Janela padrão 6 meses (Suposição), ajustável:

```bash
# Bash (Git Bash)
git log --since="6 months ago" --name-only --pretty=format: | grep -v '^$' | sort | uniq -c | sort -rn | head -20
```

```powershell
# PowerShell
git log --since="6 months ago" --name-only --pretty=format: | Where-Object { $_ } | Group-Object | Sort-Object Count -Descending | Select-Object -First 20 Count,Name
```

Sem histórico git: escreva "frequência não medida" e ordene só por dor (Inferido).

**Dor** (1 a 5, Suposição): 1 entende-se em minutos; 3 exige ler vários arquivos; 5 incidentes ou bugs ligados ao arquivo e ninguém ousa mexer. Fontes de dor: bugs com o arquivo no diff da correção (`git log --grep="fix" -- [ARQUIVO]`), tempo para entender, incidentes citados pelo usuário.

**Regra**: ordene por frequência x dor; código estável e feio vai para o fim da fila; dívida deliberada exige dono e prazo. Bugs recorrentes nos mesmos arquivos indicam debt arquitetural: encaminhe a `architecture-design`.

Exemplo (dados colados pelo usuário):

| Arquivo | Commits em 6 meses | Dor (1–5) | Prioridade | Quadrante |
| --- | --- | --- | --- | --- |
| `billing/invoice.py` | 41 | 5 | 205 | inadvertida e imprudente |
| `api/routes.py` | 28 | 3 | 84 | deliberada e prudente (atalho com prazo vencido) |
| `legacy/report_v1.py` | 2 | 5 | 10 | estável e feio: fim da fila |

## 3. Registro de dívida

Use `assets/templates/tech-debt-register.md`: ID, local, quadrante, frequência (com comando), dor, ação proposta, tamanho do passo, skill que a executa (`refactor-seguro`, `migration-parity`), dono e prazo se deliberada, evidência, rótulo. A skill de triagem **não corrige** nada.

## 4. Auditoria de testes que custam mais do que protegem (V-30, Classe C)

Modo somente relatório; nenhuma remoção sem aprovação. Critérios:

| # | Critério | Como achar (exemplos; adapte à linguagem) |
| --- | --- | --- |
| 1 | Testa o código-fonte em vez do comportamento | Teste que lê arquivos de `src` como texto, `inspect.getsource`, grep no fonte |
| 2 | Duplica outro teste | Mesmas entradas e mesmas asserções em arquivos diferentes |
| 3 | Executa sem asserção | Teste sem `assert`/`expect`, só chama a função |
| 4 | Depende de export criado só para o teste | Símbolo exportado apenas por causa do teste |
| 5 | Mock confirma a chamada e não o efeito | Asserção só de `called`/`toHaveBeenCalled` para regra de atomicidade ou persistência |

Cartão de evidência por item: arquivo:linha do teste, critério violado, comando ou trecho que prova, o que protege hoje, risco de remover, ação proposta (manter, reescrever, remover), rótulo. A decisão é do usuário. O dono desta auditoria (aqui ou em `qa-testing`) ficou em aberto no design: este plugin trata como método de dívida; estratégia de testes é de `qa-testing`.

## 5. Análise estática no fluxo (V-39)

- Rode o linter e o typechecker do projeto antes da revisão; o que eles pegam não entra no relatório do agente.
- Aplique só correções automáticas **seguras** (no Ruff, `ruff check --fix` aplica só as seguras; as inseguras exigem opt-in). Correção insegura exige teste antes e depois e aprovação.
- Não suprima aviso (`noqa`, `ts-ignore`) para fazer passar; justifique ou corrija. Procure supressões inúteis (no Ruff, a regra RUF100).
- Complexidade serve para escolher onde olhar, não como meta. Cite a ferramenta e a versão. Regras de complexidade cognitiva do Sonar não foram lidas (página protegida): Não verificado.
- Tricorder (Google, ICSE 2015) confirma a existência de uma plataforma de análise; seus princípios não foram lidos nesta pesquisa.

## 6. Métricas como guia

Número de linhas, complexidade, cobertura e duplicação indicam onde olhar. Nenhuma é meta; otimizar o número esconde o problema (AA-24). Cobertura alta com asserções fracas não prova nada.

## 7. Painel de saúde somente leitura (skill `code-health-report`, ideia do `/health` do gstack)

Regras (redação própria):
1. **Envolva, não substitua**: rode as ferramentas do projeto e mostre a saída; nunca troque o relatório da ferramenta pela análise do agente.
2. **Somente leitura**: nada é corrigido; o usuário decide.
3. **Respeite o CLAUDE.md**: se existir `## Health Stack` (snippet S-08), use exatamente aqueles comandos.
4. **Indisponível não é falha**: verifique a disponibilidade antes de pular; comando que rodou e falhou nunca vira "pulado".
5. **Mostre a saída bruta** (final) das falhas para o usuário agir sem reexecutar.
6. **Tendência só entre rodadas com a mesma cobertura**; se mudou, escreva "cobertura mudou, notas não comparáveis". Primeira rodada: "sem tendência ainda".
7. **Seja honesto**: 100 erros de tipo com testes verdes não é saudável; a nota deve refletir isso.
8. Gravar histórico só a pedido, em arquivo do projeto.

Régua 0–10 e pesos (exemplos, Suposição: valores vêm da ideia do gstack e são configuráveis; contagens vêm da saída completa capturada):

| Categoria | Peso | 10 | 7 | 4 | 0 |
| --- | --- | --- | --- | --- | --- |
| Tipos | 22% | saída limpa (exit 0) | menos de 10 erros | menos de 50 | 50 ou mais |
| Lint | 18% | limpo | menos de 5 avisos | menos de 20 | 20 ou mais |
| Testes | 28% | todos passam | mais de 95% passam | mais de 80% | 80% ou menos |
| Código morto | 13% | limpo | menos de 5 exports sem uso | menos de 20 | 20 ou mais |
| Shell | 9% | limpo | menos de 5 achados | 5 ou mais | indisponível: não pontua |

Se o executor de testes só informa o código de saída: exit 0 = 10; diferente de 0 = 4 (assume falhas) e marque como estimativa. Um checador com saída diferente de 0 nunca é "limpo", mesmo que a contagem seja zero.

Cálculo da nota composta em código, não de cabeça (Python stdlib; entra JSON por stdin, `null` = indisponível):

```python
import json, sys
W = {"typecheck": 0.22, "lint": 0.18, "test": 0.28, "deadcode": 0.13, "shell": 0.09}
scores = json.load(sys.stdin)                       # {"typecheck": 7, "lint": 4, "test": null}
scored = {k: v for k, v in scores.items() if k in W and v is not None}
if not scored:
    print("COMPOSITE: N/A - nenhuma checagem rodou")
else:
    total = sum(W[k] for k in scored)
    comp = sum(W[k] * v for k, v in scored.items()) / total
    partial = len(scored) < len(W)
    print(f"COMPOSITE: {comp:.1f}" + (" (cobertura parcial)" if partial else ""))
```

Nenhuma checagem rodou: "N/A, nenhuma checagem rodou", nunca 10/10. Recomendações ordenadas por peso x (10 - nota). Template: `assets/templates/health-dashboard.md`.

## 8. Exemplo de nota composta (cobertura parcial)

Entradas coladas: `tsc --noEmit` com 3 erros (nota 7), `eslint` com 7 avisos (nota 4), sem executor de testes.

- Cálculo: (0,22 x 7 + 0,18 x 4) / (0,22 + 0,18) = 2,26 / 0,40 = 5,65, reportado como "cerca de 5,7 (cobertura parcial: tipos e lint)".
- Indisponíveis com motivo: testes (sem runner informado), código morto (sem ferramenta), shell (sem scripts).
- Recomendações por peso x déficit: lint 0,18 x 6 = 1,08; tipos 0,22 x 3 = 0,66. Primeiro lint, depois tipos; mostrar o final da saída bruta de cada um.
- Nada foi corrigido.

## 9. Lacunas declaradas

- Sem método quantitativo de dívida além de Fowler.
- ESLint, SonarQube (regras), Semgrep, mypy e o artigo completo do Tricorder não foram lidos.
- Nenhuma fonte primária de métrica de manutenibilidade foi lida.

## 10. Gotchas

- Métrica de complexidade guia, não é meta (V-39).
- A nota composta é guia de priorização, não métrica de equipe (Inferido).
- Dívida deliberada sem dono e prazo vira dívida permanente.
- Frequência vem de comando mostrado; sem comando, é "não medida".
- Teste que "não protege nada" hoje pode proteger uma regra que ninguém lembra: proponha, não remova.
