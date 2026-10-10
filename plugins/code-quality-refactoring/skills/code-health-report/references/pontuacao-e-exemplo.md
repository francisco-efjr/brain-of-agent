# Régua, execução, composta e exemplo do painel de saúde

Sumário: 1 Detecção de ferramentas · 2 Executar e capturar · 3 Régua 0 a 10 · 4 Contar a partir da saída · 5 Nota composta · 6 Cobertura e tendência · 7 Exemplo · 8 Atribuições.

Rótulos: Verificado = executado em 2026-10-10 (Python 3.14.4, Git Bash e Windows PowerShell 5.1); Inferido = conhecimento estável ou leitura de fonte; Suposição = valor ajustável. A régua e os pesos vêm do `/health` do gstack (Garry Tan, MIT), em redação própria; ajuste ao seu projeto.

## 1. Detecção de ferramentas

Use quando o `CLAUDE.md` não tem `## Health Stack`. A detecção só propõe; o usuário confirma antes da primeira execução. Prefira os scripts já definidos no projeto a binários avulsos, e nunca use um runner que baixe pacote de terceiros (por exemplo `npx` de algo não instalado).

| Sinal no repositório | Categoria | Comando a propor |
| --- | --- | --- |
| `tsconfig.json` | tipos | script `typecheck` do `package.json` ou `tsc --noEmit` do projeto |
| `mypy.ini`, `[tool.mypy]` em `pyproject.toml` | tipos | `mypy .` |
| `eslint.config.*`, `.eslintrc*` | lint | script `lint` do `package.json` |
| `[tool.ruff]` em `pyproject.toml`, `ruff.toml` | lint | `ruff check .` |
| script `test` no `package.json`; `pytest` no `pyproject.toml`; `Cargo.toml`; `go.mod` | testes | `npm test`; `pytest`; `cargo test`; `go test ./...` |
| `knip` nas dependências | código morto | script do projeto para `knip` |
| `*.sh` no repositório e `shellcheck` instalado | shell | `shellcheck` sobre os scripts |

Seção para o `CLAUDE.md` (oferecer, não gravar sem pedido):

```markdown
## Health Stack

- typecheck: npm run typecheck
- lint: npm run lint
- test: npm test
- deadcode: (nenhum)
- shell: (nenhum)
```

## 2. Executar e capturar

Um comando por invocação. Registre o código de saída da própria ferramenta.

Git Bash:

```bash
cmd='npm run typecheck'
start=$(date +%s); out=$(bash -c "$cmd" 2>&1); code=$?; end=$(date +%s)
printf '%s\n' "$out" | tail -50
echo "EXIT=$code DURATION=$((end-start))s ERRORS=$(printf '%s\n' "$out" | grep -c 'error TS')"
```

PowerShell:

```powershell
$sw = [Diagnostics.Stopwatch]::StartNew()
$out = cmd /c "npm run typecheck 2>&1"
$code = $LASTEXITCODE
$sw.Stop()
$out | Select-Object -Last 50
"EXIT=$code DURATION=$([int]$sw.Elapsed.TotalSeconds)s ERRORS=$(@($out | Select-String 'error TS').Count)"
```

Os dois moldes foram executados com um comando de teste que imprime duas linhas `error TS...` e sai com código diferente de zero: ambos reportaram o código de saída e a contagem corretos (Verificado). Troque `error TS` pelo padrão da ferramenta (seção 4).

`grep -c` sai com código 1 quando não há correspondência, mas imprime `0`: use a saída, não o código do `grep`, e nunca o do `tail`, como resultado da ferramenta.

## 3. Régua 0 a 10

| Categoria | Peso | 10 | 7 | 4 | 0 |
| --- | --- | --- | --- | --- | --- |
| Tipos | 22 | Limpo (exit 0) | menos de 10 erros | menos de 50 erros | 50 ou mais |
| Lint | 18 | Limpo (exit 0) | menos de 5 avisos | menos de 20 avisos | 20 ou mais |
| Testes | 28 | Todos passam (exit 0) | mais de 95% passam | mais de 80% passam | 80% ou menos |
| Código morto | 13 | Limpo (exit 0) | menos de 5 exports/arquivos sem uso | menos de 20 | 20 ou mais |
| Shell | 9 | Limpo (exit 0) | menos de 5 achados | 5 ou mais | indisponível |

Os pesos são relativos e somam 90: a categoria GBrain do gstack foi retirada e a normalização do cálculo cuida da diferença (Suposição). Para testes que só informam o código de saída: 0 vale 10; diferente de 0 vale 4 (Suposição do gstack; declare no painel).

Notas intermediárias entre os degraus: use o degrau da faixa em que a contagem cai (por exemplo, 3 erros de tipo: menos de 10, nota 7). Erro com contagem zero mas exit diferente de zero: a ferramenta falhou por outro motivo (configuração, crash). Reporte a saída e marque ERRO, não 10.

Status por nota: 10 LIMPO; 7 a 9 ATENÇÃO; 4 a 6 PRECISA DE TRABALHO; 0 a 3 CRÍTICO; INDISPONÍVEL (sem nota); ERRO (sem nota, composta N/A).

## 4. Contar a partir da saída

Os formatos abaixo são os usuais (Inferido); confira na versão instalada e adapte o padrão.

| Ferramenta | Como contar |
| --- | --- |
| `tsc` | Linhas com `error TS`; o resumo "Found N errors" aparece com `--pretty` |
| ESLint (formatador padrão) | Linha de resumo no fim, algo como "N problems (E errors, W warnings)" |
| Ruff | Linha "Found N errors." no fim |
| pytest | Linha final com "N failed, M passed" |
| Jest | Linha "Tests: N failed, M passed, T total" |
| `go test` | Linhas começando por `FAIL` e `ok` por pacote |
| `shellcheck` | Blocos "In arquivo line N:" |

Conte sempre sobre a saída completa, não sobre o trecho exibido. Contagem zero com exit diferente de zero nunca é "limpo".

## 5. Nota composta em código

Passe só as categorias pontuadas como `categoria=nota`. As indisponíveis simplesmente não entram. Categorias: `tipos`, `lint`, `testes`, `codigo_morto`, `shell`.

```bash
python -I -c "import sys; w={'tipos':22,'lint':18,'testes':28,'codigo_morto':13,'shell':9}; ok=dict((a.split('=')[0], float(a.split('=')[1])) for a in sys.argv[1:]); print('COMPOSITE: N/A - nenhuma checagem rodou' if not ok else 'COMPOSITE: %.1f/10 (cobertura: %s)' % (sum(w[k]*v for k,v in ok.items())/sum(w[k] for k in ok), ', '.join(ok)))" tipos=7 lint=4
```

Saída (Verificado em Git Bash e PowerShell, Python 3.14.4): `COMPOSITE: 5.7/10 (cobertura: tipos, lint)`. Sem argumentos: `COMPOSITE: N/A - nenhuma checagem rodou`. Com as cinco categorias em 10: `COMPOSITE: 10.0/10`. O `-I` isola o interpretador de variáveis de ambiente e do diretório atual. Se o Python não existir, calcule à mão `soma(peso x nota) / soma(pesos)` das categorias pontuadas e mostre a conta.

## 6. Cobertura e tendência

- Cobertura: "N de 5 categorias". Qualquer categoria sem nota entra em "Indisponíveis" com o motivo (sem runner, ferramenta ausente, escopo).
- Nota composta com categorias faltando recebe o rótulo "cobertura parcial".
- Tendência: compare só rodadas cujo conjunto de categorias pontuadas é idêntico. Conjunto diferente: "cobertura mudou, notas não comparáveis". Rodada N/A não tem tendência.
- Primeira rodada: "primeira rodada, sem histórico; rode de novo após mudanças para acompanhar".
- Queda em relação à rodada comparável anterior: liste as categorias que caíram, o delta e o erro que mais se repete na saída.
- Histórico em arquivo só a pedido do usuário, em local escolhido por ele, com uma linha por rodada (data, branch, categorias e notas, composta).

## 7. Exemplo (entrada do eval: só saídas coladas)

Entrada do usuário: "Use /code-quality-refactoring:code-health-report" com `tsc --noEmit` (3 erros) e `eslint .` (7 avisos) colados; não há runner de testes, nem ferramenta de código morto, nem scripts de shell.

```text
PAINEL DE SAÚDE: app-web, main, 2026-10-10
Categoria  Ferramenta       Nota  Status               Detalhes
Tipos      tsc --noEmit     7/10  ATENÇÃO              3 erros (saída fornecida pelo usuário)
Lint       eslint .         4/10  PRECISA DE TRABALHO  7 avisos (saída fornecida pelo usuário)
Testes     --               --    INDISPONÍVEL         sem runner configurado
Cód. morto --               --    INDISPONÍVEL         sem ferramenta
Shell      --               --    INDISPONÍVEL         sem scripts

NOTA COMPOSTA: 5.7/10 (cobertura parcial: 2 de 5 categorias)
Conta: (22 x 7 + 18 x 4) / (22 + 18) = 226 / 40 = 5.65, exibido como 5.7
Tendência: primeira rodada, sem histórico.

RECOMENDAÇÕES (peso x déficit)
1. Lint: 18 x (10 - 4) = 108. Ver os 7 avisos; correção automática segura da ferramenta, se existir, como sugestão.
2. Tipos: 22 x (10 - 7) = 66. Ver os 3 erros de tipo.
3. Testes: sem runner; criar ou configurar um é a lacuna de maior peso (28) e não entrou na nota.

Nada foi corrigido. Status: DONE_WITH_CONCERNS (cobertura parcial; saídas não executadas por mim).
```

O painel não dá 10/10, não inventa saída de testes e não corrige nada. A recomendação 3 não vem do cálculo de déficit (testes não têm nota), vem da regra de cobertura.

## 8. Atribuições

- `/health` do gstack (Garry Tan, MIT, `vendor/gstack/LICENSE` no snapshot): régua, pesos de exemplo, "envolva, não substitua", "indisponível não é falha", tendência comparável. Redação própria; nenhum script, binário, GBrain ou persistência do gstack foi copiado.
- Ruff, ESLint, tsc, pytest, Jest: formatos de saída por conhecimento estável; confirmar na versão instalada (V-39 leu apenas a documentação do Ruff).
