# Verificação por execução (jogos)

Base: V-01, V-04, V-05, V-10, V-12, V-29, V-30 (VALIDATED, 2026-10-10). Transposição de artigos web e de compilador para jogos é **Inferido**. Nenhum comando abaixo foi executado pelos autores deste plugin (regra de não executar); rode no seu ambiente e cole a saída.

## Sumário

- [Por que executar](#por-que-executar)
- [Contrato de pronto](#contrato-de-pronto)
- [Camadas de verificação](#camadas-de-verificação)
- [Sondas no próprio jogo](#sondas-no-próprio-jogo)
- [Check curto](#check-curto)
- [Oráculos e referência](#oráculos-e-referência)
- [Harness de sessões longas](#harness-de-sessões-longas)
- [Avaliador cético](#avaliador-cético)
- [Critério de aceite por execução](#critério-de-aceite-por-execução)
- [Evidência: o que vale](#evidência-o-que-vale)
- [Armadilhas](#armadilhas)

## Por que executar

A documentação oficial do Claude Code pede dar ao agente algo que ele rode (build, teste, captura de tela) antes de dizer "pronto" (V-01). Em jogos isso vira: comandos headless da engine, sondas dentro do jogo e captura de evidência. O agente não enxerga o jogo rodando; "compila sem erro" não é prova (V-29). O que a execução **não** prova: aparência, animação, áudio e sensação (limite do modo headless, confirmado em V-12 por fornecedor, classe C, e pelo autor do port Amiga em V-30). Isso é pendência humana em todo relatório.

## Contrato de pronto

Escreva antes de codar (`assets/templates/contrato-de-pronto.md`). Cada linha tem comando ou sonda e limiar.

```markdown
Funcionalidade: spawner de inimigos (Godot 4.3, GDScript)
1. Funciona: com --level test_spawn, 10 inimigos instanciados; o limite de 10 é respeitado ao tentar o 11o.
   Prova: godot --headless --path . -- --probe  -> linha "spawned=10 cap_hit=true"; exit 0; 0 linhas ERROR.
2. Regressão: a cena main.tscn carrega sem erro (check de todos os níveis).
3. Orçamento: 300 inimigos mantêm <= 16,67 ms de CPU no hardware-alvo [só se o projeto definiu esse orçamento].
4. Humano: sensação do ritmo de spawn, áudio do spawn, legibilidade dos inimigos -> NÃO AVALIADO (pendência humana).
```

Regras: o limiar é fixado antes de medir; reduzir critério para esconder falha é proibido (V-05); critério sem comando vira pendência humana, não "ok".

## Camadas de verificação

| Camada | O que prova | O que não prova | Godot | Unity / Unreal |
| --- | --- | --- | --- | --- |
| Importar/compilar | recursos e scripts carregam | comportamento | `godot --headless --path . --import` (em checkout limpo) | o comando que o CLAUDE.md fixar |
| Sintaxe de script | um `.gd` analisa | lógica | `godot --headless --path . --check-only -s res://scripts/x.gd` (combinação Inferido; confirme com `godot --help`) | n/a |
| Testes de lógica | fórmulas, transições, limiares | jogabilidade | GUT: `godot --headless --path . -s addons/gut/gut_cmdln.gd -gdir=res://test/unit -gexit` (somente se o projeto adotou GUT; exit 0 passa, 1 falha) | Unity: Test Runner (EditMode/PlayMode); `Unity.exe -runTests -batchmode -projectPath <pasta> -testPlatform EditMode -testResults <xml>` (opções Verificadas na doc do Test Framework 1.4; não executado pelo plugin). Unreal: o que o projeto fixar |
| Sonda em cena de teste | comportamento observável na engine | sensação, áudio | flags do jogo (abaixo) | idem |
| Captura/clipe | estado visual no instante | persistência, sensação | `--screenshot <arquivo>` | idem |
| Humano joga | sensação, áudio, legibilidade | n/a | n/a | n/a |

Escolha **um** framework de teste por projeto (GUT ou GdUnit4); dois confundem o agente (V-32). GUT 9 exige Godot 4 (V-12).

## Sondas no próprio jogo

O caso do port Amiga para Godot (V-30, classe B, relato individual) expõe flags para o modelo testar sem humano. Adicione-as **antes** de pedir mecânicas novas, como tarefa pequena e aprovada (`assets/templates/spec-de-sondas.md`):

| Flag | Efeito | Exemplo |
| --- | --- | --- |
| `--level <id>` | carrega direto a cena de teste | `-- --level test_spawn` |
| `--drive <script>` | injeta input a partir de arquivo (por exemplo `0:right,30:jump,60:attack`) | `-- --drive tests/dash.drive` |
| `--probe` | imprime estado interno em texto (posição, vida, contagem de nós) | `probe t=61 player.x=312.0 stamina=40` |
| `--screenshot <arquivo>` | salva captura e sai | `-- --screenshot out/dash.png` |

Em Godot, argumentos do jogo vêm depois de `--` e são lidos com `OS.get_cmdline_user_args()` (conhecimento estável, **Inferido**: confirme na versão). Dois checks headless de projeto (V-30): compilar todos os scripts e carregar todos os níveis relatando falhas.

## Check curto

Do compilador C (V-10, analogia a jogos: Inferido): o comando `check` do projeto imprime no máximo 20 linhas (resumo mais caminho do log), etiqueta erros como `ERROR[sistema]` (para `grep`), aceita `--quick` (amostra determinística de cenas ou níveis) e `--full`; detalhe vai para arquivo. Saída longa consome contexto e esconde a linha que importa.

```text
check --quick  (seed=7, 6/42 níveis)
OK   import        0 erros
OK   scripts       58/58 compilam
FAIL levels        ERROR[level] level_07.tscn: nó 'Spawner' sem cena atribuída
OK   gut           31 passaram, 0 falharam
resultado: FAIL (1)   log: build/check.log   exit=1
```

## Oráculos e referência

Quando existe referência (captura de versão aprovada, saída de build anterior, binário original), compare em vez de "olhar" (V-10, V-30). No port Amiga a comparação pixel a pixel foi dos níveis de 1993 renderizados contra capturas de 2020, não do port moderno, que o autor revisou a olho (correção do validador em V-30). Jogo novo não tem oráculo: só sondas. Triagem de regressão: ache o último build bom, rode o mesmo `--drive` nos dois, compare a saída de `--probe` linha a linha, bisseccione os commits.

## Harness de sessões longas

Fonte: Anthropic Engineering, 26/11/2025 (V-04). Transposição a jogos é Inferido. Lista de funcionalidades em JSON porque o modelo o sobrescreve menos que Markdown.

```json
{"id": "dash-01", "categoria": "gameplay",
 "descricao": "Dash consome stamina e respeita colisão com paredes",
 "passos": ["abrir a cena de teste", "acionar dash via sonda de input", "ler stamina e posição no log"],
 "passes": false}
```

Regras: só o campo `passes` muda, e só depois de rodar os `passos`; nunca apagar nem editar passos; uma funcionalidade por sessão.

Rotina de início (comando `/game-development:init-session`): confirmar diretório; ler `git log` e o arquivo de progresso; ler `features.json` e escolher o primeiro `passes: false`; rodar o init (abre o jogo ou editor e executa o check headless); rodar o teste mínimo antes de codar. Fim: commit descritivo (só se o usuário pediu commit), atualizar progresso com o que ficou quebrado e o próximo item.

Script de init no Windows (o ambiente do usuário é Windows, Inferido pelos caminhos). Escreva o arquivo, **execute só com confirmação**:

```powershell
# init.ps1 - roda da raiz do projeto Godot; ajuste godot ao seu PATH
$ErrorActionPreference = "Stop"
godot --version
godot --headless --path . --import
if ($LASTEXITCODE -ne 0) { Write-Error "import falhou"; exit 1 }
Write-Output "init ok"
```

## Avaliador cético

Fonte: Anthropic Engineering, 24/03/2026 (V-05). Agentes elogiam o próprio trabalho; é mais viável calibrar um avaliador cético do que fazer o gerador se criticar. Custo relatado pelo autor para um app web: solo cerca de 20 min e US$ 9; harness completo 6 h e US$ 200; versão atualizada US$ 124,70. Com o Opus 4.6 ele removeu o sprint e passou a rodar o avaliador uma vez no fim: use o avaliador **só** em funcionalidade difícil, no fim, ou a pedido (agente `game-evaluator`). Calibre com 2 a 3 exemplos de notas comentadas do próprio projeto. O prompt do avaliador é Inferido (a fonte não o publica); a rubrica de jogo é Suposição até testar em projeto real. Ele é da mesma família de modelo: declare que não é validação externa.

## Critério de aceite por execução

Padrão do godogen (V-29, classe B; não instale nem execute o projeto: gera assets com chaves pagas e roda código): a cada iteração, rodar o jogo, capturar evidência (captura ou clipe curto), listar defeitos visíveis e só então marcar a tarefa como feita. O agente julga **itens objetivos do contrato** (sem erro no log, valor na sonda, nó contado); sensação, áudio e legibilidade ficam NÃO AVALIADO (conflito K4 do SYNTHESIS). Guia por engine em `engines/<nome>.md` com comandos de build, check e captura é um formato útil no repositório do jogo.

## Evidência: o que vale

| Vale | Não vale |
| --- | --- |
| Comando, exit code e trecho do log gerados nesta sessão | "Rodei e passou" sem saída |
| Linha de `--probe` com o valor lido | Descrição de como o código deveria se comportar |
| Caminho de captura gerado agora | Captura antiga reaproveitada depois de mudança no código |
| Teste que falhou antes da correção e passou depois | Teste escrito já verde |

Status por item: OK / PENDENTE / FALHOU / N/A. "Testado" sem evidência conta como PENDENTE (convenção do `checklist-release` do brain, adaptada). Uma mudança posterior invalida a evidência anterior afetada: refaça só o afetado.

## Armadilhas

- Testar só no menu: use a cena de teste com o contexto real.
- Falha em 0% das tentativas em muitas execuções costuma indicar tarefa ou teste quebrado, não dificuldade (V-06).
- Retry que transforma a primeira falha em verde esconde intermitência: mantenha a primeira falha no relatório.
- Constantes ajustadas à mão no tick original (V-30) não se "normalizam" para parecer limpas.
- Nunca instale nem execute godogen, hooks de catálogos ou scripts do skill-creator sem ler antes e sem decisão do responsável.
