# Checklist de design de CLI (IDs CLI-nn)

Verificado em 2026-10-10 contra V-11, V-12, V-13, V-64. Os IDs e as severidades padrão são os do `checklist-completo.md` do playbook (`${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/checklist-completo.md`); aqui eles aparecem agrupados nos blocos A a F da revisão, com a evidência a procurar. Severidade padrão é da fábrica (Inferido): ajuste ao contexto (versão publicada, público, reversibilidade) e justifique quando mudar. As expressões de busca também são da fábrica (Inferido): adapte ao idioma do projeto e registre os arquivos pesquisados.

Sumário: [Bloco A](#bloco-a-contrato-de-máquina) · [Bloco B](#bloco-b-humano) · [Bloco C](#bloco-c-agente) · [Bloco D](#bloco-d-segurança-e-destrutivo) · [Bloco E](#bloco-e-nomes-verbos-e-estabilidade) · [Bloco F](#bloco-f-distribuição-e-teste-inferido) · [Padrões de busca](#padrões-de-busca-por-linguagem)

## Bloco A: contrato de máquina

| ID | Sev. | Como detectar | Fonte | Correção |
| --- | --- | --- | --- | --- |
| CLI-01 | Média | Logs e progresso impressos no mesmo stream do resultado (`print`, `console.log`, `fmt.Println`, `println!`, `Write-Output`) | V-13, V-64 | Resultado em stdout; log, progresso e aviso em stderr |
| CLI-02 | Alta | `exit(0)` incondicional, um único código de falha, códigos não documentados | V-13 | 0 só em sucesso; tabela de códigos no `--help` e no README |
| CLI-03 | Alta | Mensagem de erro em stdout, ou erro com exit 0 | V-13, V-64 | Erro em stderr e exit diferente de zero |
| CLI-04 | Alta | Leitura interativa (`input(`, `readline`, `inquirer`, `Read-Host`, `Console.ReadLine`) sem teste de TTY | V-12, V-13, V-64 | Flag para toda pergunta; sem TTY e sem a flag, falhar rápido listando o que faltou; `--no-input` |
| CLI-05 | Alta | Sem `--json`, ou JSON que devolve string, booleano solto ou texto misturado | V-13, V-64 | `--json` com objeto estável; mensagens fora do stdout |
| CLI-06 | Baixa | Sem `--plain` para saída em tabela | V-13 | Uma linha por registro, campos separados por tab |
| CLI-07 | Média | Cor ou spinner sem checar TTY e `NO_COLOR` | V-13, V-64 | Desligar sem TTY ou com `NO_COLOR`; `--no-color` |
| CLI-19 | Média | Operação longa que só existe bloqueante | V-64 | `--no-wait` e comando `wait` |
| CLI-20 | Média | Parâmetro que recebe JSON bruto; unidade no nome do argumento (`--timeout-seconds`) | V-64 | Propriedades como flags; aceitar sufixos como `30s`, `1h` |
| CLI-25 | Baixa | Imports ou rede no startup antes de tratar `--help` e `--version` | V-13, V-12 | Carregamento preguiçoso (meta citada pelo clig.dev: 100 ms) |

## Bloco B: humano

| ID | Sev. | Como detectar | Fonte | Correção |
| --- | --- | --- | --- | --- |
| CLI-08 | Média | `--help` sem exemplos ou com exemplos no fim | V-13 | Exemplos primeiro |
| CLI-09 | Baixa | Flag ou comando sem descrição | V-64 | Descrição curta em toda flag |
| CLI-10 | Média | Erro sem causa, correção ou uso correto (`Error: failed`) | V-11, V-13, V-64 | Problema, causa, correção e exemplo de uso |
| CLI-12 | Média | Configuração lida em ordem arbitrária | V-13 | Precedência: flags, ambiente, projeto, usuário, sistema; XDG é convenção Unix (no Windows, escolha do projeto, Inferido) |
| CLI-17 | Alta | Comando que apaga, move ou publica sem flag explícita nem confirmação | V-13 | Confirmação proporcional ao risco; `--yes`/`--force` para script |
| CLI-26 | Baixa | Instalação documentada sem desinstalação | V-13 | Instrução de desinstalar ao fim da de instalar |

## Bloco C: agente

| ID | Sev. | Como detectar | Fonte | Correção |
| --- | --- | --- | --- | --- |
| CLI-21 | Média | Listas sem limite, paginação ou filtro; saída gigante; sem modo `concise`/`detailed` | V-11, V-12 | Limite padrão, paginação, dica de filtro, verbosidade opcional |
| CLI-22 | Baixa | Segundo processo do mesmo serviço sobe sem aviso (`make dev` duplicado) | V-12 | Pidfile ou lock e mensagem "já rodando" |
| CLI-23 | Baixa | Log de serviço só no terminal | V-12 (parcial) | Sugestão da fábrica (Inferido): log em arquivo de caminho fixo, documentado no `CLAUDE.md`, para o agente ler depois. O Ronacher não trata de caminho nem de timeout |
| CLI-29 | Baixa | Nenhuma evidência de teste com tarefa real de vários passos | V-11 | Rodar a tarefa com um agente e ler a transcrição, com conjunto de tarefas separado para não superajustar (autorização do usuário) |

Itens C transversais que reaproveitam IDs de outros blocos: subcomando que faz uma coisa com nome inequívoco (CLI-15), saída curta (CLI-21), erro com correção (CLI-10), nunca prompt sem TTY (CLI-04), idempotência (CLI-16).

## Bloco D: segurança e destrutivo

| ID | Sev. | Como detectar | Fonte | Correção |
| --- | --- | --- | --- | --- |
| CLI-13 | Crítica | Flags `--password`, `--token`, `--api-key`, `--secret`; leitura de segredo de variável de ambiente nas CLIs que escrevemos | V-13 | Arquivo com permissão restrita (`--token-file`), stdin ou store do sistema. Variável de ambiente só como exceção documentada de CI (por exemplo, a chave do updater do Tauri, V-20), e então a severidade cai para Alta |
| CLI-14 | Alta | Segredo ou cabeçalho de autorização em log, `--verbose` ou mensagem de erro | V-13 (Inferido) | Mascarar valores sensíveis |
| CLI-17 | Alta | (ver Bloco B) apagar sem flag explícita | V-13 | `--yes`/`--force` |
| CLI-18 | Média | Destrutivo de efeito amplo sem simulação | V-25, V-28 (padrão), V-13 | `--dry-run` que lista o que mudaria |

Caso especial de caminho (crítica, conhecimento estável, relacionado a SC2164 de V-61): `rm -rf "$dir/"*` ou equivalente com variável possivelmente vazia. Valide que o alvo não é vazio nem a raiz antes de apagar; em scripts, veja `shell-script-review`.

## Bloco E: nomes, verbos e estabilidade

| ID | Sev. | Como detectar | Fonte | Correção |
| --- | --- | --- | --- | --- |
| CLI-15 | Baixa | Mistura de `verbo substantivo` e `substantivo verbo`; subcomando que faz várias coisas | V-64, V-11 | `[substantivo] [verbo]` em todo lugar; uma ação por subcomando |
| CLI-16 | Média | Mesmo verbo com semântica diferente; `create` que falha se já existe; `show` com 1 para "não encontrado" | V-64 | `create` idempotente que devolve o recurso; `update` tipo PATCH; `set` substitui tudo; `show`; `list` num comando só; `delete` sem retorno; código próprio para não encontrado (Azure CLI: 3) |
| CLI-24 | Alta (com versão publicada) | Flag, exit code ou campo JSON renomeado sem nota depois de GA | V-64 (Heroku, sinal C) | Mudança só em versão maior, com nota de migração |

## Bloco F: distribuição e teste (Inferido)

Sem item V validado; conhecimento estável do domínio (lacuna 17).

| ID | Sev. | Como detectar | Fonte | Correção |
| --- | --- | --- | --- | --- |
| CLI-11 | Baixa | `--version` ausente ou diferente da versão publicada | V-13 (Inferido) | Versão gerada de uma única fonte (manifesto ou tag) |
| CLI-27 | Média | Nenhum teste fixa stdout, stderr e exit code | Inferido | Teste de contrato por caminho e snapshot de `--help` e dos erros (exemplo em [contrato-proposto.md](contrato-proposto.md)) |
| CLI-28 | Baixa | README sem canal de instalação nem completions de shell | Inferido (lacuna 17) | Declarar canal (winget, gerenciador da linguagem, binário único) e completions quando o framework gerar. Não citar ferramenta sem fonte |

## Padrões de busca por linguagem

Ponto de partida para o `Grep` (Inferido).

| Verificação | Python | Node | Go | Rust | .NET | PowerShell |
| --- | --- | --- | --- | --- | --- | --- |
| Saída de erro | `sys.stderr`, `print(` | `console.error`, `console.log` | `os.Stderr`, `fmt.Println` | `eprintln!`, `println!` | `Console.Error`, `Console.WriteLine` | `Write-Error`, `Write-Output` |
| Saída e códigos | `sys.exit(`, `SystemExit` | `process.exit(`, `process.exitCode` | `os.Exit(` | `std::process::exit` | `Environment.Exit`, retorno de `Main` | `exit `, `$LASTEXITCODE` |
| TTY e cor | `isatty`, `NO_COLOR` | `isTTY`, `NO_COLOR` | `IsTerminal`, `NO_COLOR` | `is_terminal`, `NO_COLOR` | `Console.IsOutputRedirected` | `$Host.UI.SupportsVirtualTerminal` |
| Prompt | `input(`, `getpass` | `readline`, `inquirer`, `prompts` | `bufio.NewReader(os.Stdin)` | `read_line` | `Console.ReadLine` | `Read-Host`, `-Confirm` |
| Segredo por flag | `--password`, `--token` | idem | idem | idem | idem | `[string]$Password`, `[string]$Token` |
