# Layout de evals, flags e receita de CI

Apoio da skill `eval-design`. Leia ao montar a pasta `evals/`, escrever `prompt.md` e graders, escolher flags do `claude plugin eval` ou configurar CI.

Rótulos: tipos de grader, flags, códigos de saída, padrões (3 execuções, `--threshold` 1.0), restrição do Windows e requisitos de versão vêm de V-02 (documentação oficial de plugin evals, lida em 2026-10-10: Verificado). A lista de chaves aceitas em `prompt.md`, os campos de cada tipo de grader, a regra de concessão de ferramentas e a exclusão de graders em execução de dois braços foram reconferidos na mesma página em 2026-10-10 pelo validador de qualidade (Verificado). Confira tudo com `claude plugin eval --help` na versão instalada.

## Sumário

- [Layout de pastas](#layout-de-pastas)
- [prompt.md](#promptmd)
- [Graders](#graders)
- [Flags e códigos de saída](#flags-e-códigos-de-saída)
- [Fluxo de iteração](#fluxo-de-iteração)
- [Receita de CI](#receita-de-ci)
- [README padrão dos evals](#readme-padrão-dos-evals)
- [Ler transcrições](#ler-transcrições)

## Layout de pastas

```text
<raiz-do-plugin>/
└── evals/
    ├── README.md                 ← como rodar, custo, status dos casos
    ├── .gitignore                ← results/
    └── <nome-do-caso>/
        ├── prompt.md             ← frontmatter + o pedido do usuário
        └── graders/
            ├── skill-fired.md    ← tool_used (indicador: fora do score)
            ├── resultado.md      ← regex / file_exists / llm
            └── passos.md         ← tool_used / tool_order
```

Alternativa ao par `prompt.md` + `graders/`: um `case.yaml` por caso (V-02). Não misture formatos num mesmo caso. O layout é diferente de `evals/evals.json` do skill-creator; um não lê o outro.

Execute `claude plugin eval` na raiz do plugin. Nomes de caso em kebab-case curto (caminhos longos dão aviso no verificador).

## prompt.md

Frontmatter aceito pelo verificador (chaves desconhecidas fazem o carregador rejeitar o caso): `schema_version`, `name`, `description`, `tags`, `plugins`, `runs`, `expected_outcome`, `model`, `max_turns`, `timeout_seconds`, `allowed_tools`, `append_system_prompt`, `env`. Use poucas: `description`, `tags`, `max_turns`, `allowed_tools` bastam para a maioria.

```markdown
---
description: Revisa Dockerfile e aponta tag latest e execução como root
tags: [dockerfile, dispara]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---
Esse Dockerfile vai para produção amanhã. Tem algum problema?

FROM node:latest
COPY . .
RUN npm install
USER root
CMD ["node", "server.js"]
```

Regras de redação do corpo:

1. Escreva como o usuário escreveria: sem nome da skill, sem "use o plugin".
2. Traga no texto o código, o log ou o contexto necessário: o workspace começa vazio.
3. Para comportamento sem arquivo de saída, o grader `llm` avalia a resposta final. Para provar que algo rodou, peça gravação do resultado em arquivo e cheque o arquivo e a ferramenta usada (V-02).
4. Conceda o mínimo em `allowed_tools`. Só as ferramentas somente leitura listadas ali são concedidas automaticamente (`Read`, `Glob`, `Grep`, `NotebookRead`, `Skill`, `AskUserQuestion`, `Agent`, `TodoWrite` e as de tarefa). `Write`, `Edit`, `Bash`, `WebFetch` e `WebSearch` são removidas da sessão até alguém rodar com `--allow-tools` (por exemplo `--allow-tools Write Edit`); a concessão vale para todos os casos da execução. Com `Bash` ou PowerShell concedidos, o run usa o sandbox do sistema: no Windows nativo não há backend e o caso falha, então use WSL2 (V-02).
5. Dados de exemplo sintéticos; nunca segredo real.

## Graders

Frontmatter de todo grader: `type` obrigatório; `weight` e `arm` opcionais (V-02). Tipos:

| type | Mede | Custo de juiz | Observação |
| --- | --- | --- | --- |
| `regex` | padrão no alvo | nenhum | `pattern` (regex JavaScript), `flags` (ex.: `i`; `(?i)` inline não é aceito), `match` (`not_contains` exige ausência; `"count:N"` exige N ocorrências), `target` (`last_message` padrão, `trace`, `files`, `{ source: file, path: <caminho> }`, `mock_calls`) |
| `tool_used` | uma ferramenta foi (ou não) usada; `input_match` filtra a entrada JSON | nenhum | `tool`, `input_match`, `min` (padrão 1), `max` (padrão ilimitado); `min: 0` + `max: 0` = não deve usar |
| `tool_order` | ordem entre ferramentas | nenhum | `before`, `after` (nome da ferramenta ou `{ tool, input_match }`); exige as duas chamadas |
| `file_exists` | arquivo criado durante o run | nenhum | `path` (glob), `exists: false` para exigir ausência; arquivo só modificado não conta |
| `llm` | juiz julga com o texto do grader | sim (o juiz vota PASS em 2 de 3) | `criteria` (no `.md` é o corpo), `focus` (mesmos valores de `target`); binário, um modo de falha |
| `baseline` | compara com transcrição de referência `.jsonl` | sim | `baseline_file` (`.jsonl` na pasta do caso), `criteria` |

Nota da execução = fração de graders aprovados (com pesos); nota do caso = média das execuções; o caso passa se atingir `--threshold` (padrão 1.0). **`tool_used: Skill` fica fora do score** nas duas arms numa execução de dois braços: é indicador de que o plugin disparou (V-02). Também ficam fora os graders com `arm: with-only`. Exceções: se todos os graders do caso estiverem nesse conjunto, eles voltam a contar; `arm: both` força a contagem nos dois braços; `--ablation none` não exclui nada.

Grader de disparo (substitua `<nome>`; o padrão aceita o prefixo `plugin:`):

```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?<nome>"'
---
```

Grader negativo (a skill **não** deve disparar). Use `arm: both`: sem ele, o grader de `Skill` fica fora do score na execução com baseline e o caso negativo deixa de medir sobredisparo (a doc recomenda exatamente este uso):

```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?<nome>"'
min: 0
max: 0
arm: both
---
```

Grader `llm` (um critério, PASS e FAIL concretos, corpo em texto simples):

```markdown
---
type: llm
---
PASS se a resposta aponta que a tag `latest` não fixa a versão da imagem base e que o contêiner roda como root, e propõe fixar a versão e usar usuário sem privilégios.
FAIL se declara o Dockerfile pronto para produção sem ressalva, ou inventa vulnerabilidades específicas sem base no texto.
```

Um juiz por modo de falha: dois critérios independentes (identifica o risco; não inventa vulnerabilidades) viram dois arquivos.

## Flags e códigos de saída

Flags confirmadas em V-02: `--case`, `--runs`, `--ablation none|with-without`, `--judge-model`, `--threshold`, `--max-cost-usd`, `--trust-plugin`, `--json [path]`, `--allow-tools`. Códigos de saída: 0 ok; 1 reprovação ou erro; 2 execução parcial (teto de custo ou credencial recusada). Três execuções por caso por padrão. Requisitos: Claude Code 2.1.269 ou superior e git 2.31 ou superior.

| Objetivo | Comando (forma; confira `--help`) |
| --- | --- |
| Desenvolver um caso, barato | `claude plugin eval . --case dispara-com-git-log --ablation none --runs 1` |
| Confirmar com as 3 execuções padrão | `claude plugin eval . --ablation none` |
| Medir o efeito do plugin | `claude plugin eval . --ablation with-without --max-cost-usd 5` |
| CI | ver receita abaixo |

O valor de `--max-cost-usd` é exemplo: calibre ao orçamento.

## Fluxo de iteração

1. Escreva o caso e o grader de disparo; rode com `--runs 1 --ablation none`.
2. Leia a transcrição; ajuste o prompt (se o caso for irreal) ou a `description` da skill (se o gatilho falhou).
3. Acrescente o grader de resultado e o de passos; rode de novo.
4. Quando o conjunto estabilizar, rode as 3 execuções padrão e depois `with-without`.
5. Registre data, versão do Claude Code, modelo, comando e resultado no README; mude o status do caso de `designed_not_executed` para `executado em <data>`.

Interpretação: se o caso passa nas duas arms, o plugin pode não estar contribuindo (o modelo base resolve). Se passa com plugin e falha sem, há efeito. Se passa mas o Δ é negativo, suspeite do juiz antes do plugin (V-02). Poucas execuções não provam nada: use mais de uma e mediana.

## Receita de CI

Forma da receita de V-02: `--trust-plugin`, `--json results.json`, modelos fixados, teto de custo. Exemplo (valores ilustrativos; `--trust-plugin` concede confiança ao plugin do repositório, use só em repositório próprio e revisado):

```bash
claude plugin eval . --trust-plugin --json results.json --max-cost-usd 5 --runs 3
echo "exit=$?"   # 0 ok, 1 reprovação/erro, 2 parcial
```

No Windows nativo, CI com suítes que concedem Bash precisa de runner Linux ou WSL2. Guarde `results.json` como artefato e **não** o versione (`results/` no `.gitignore`). Falha de custo (código 2) não é reprovação do plugin: reduza casos ou suba o teto conscientemente.

## README padrão dos evals

Conteúdo mínimo de `evals/README.md`:

1. Como rodar (`claude plugin eval .` na raiz do plugin; `--case`, `--runs`, `--ablation`), versão mínima do Claude Code e git, aviso de WSL2 no Windows com Bash.
2. Custo: cada execução e cada juiz consomem chamadas de modelo; use `--max-cost-usd`.
3. Regra de leitura de transcrições e de desconfiar de 100%.
4. Status dos casos: `designed_not_executed` até rodar; tabela caso -> o que mede -> graders -> status.
5. Aviso de que `tool_used: Skill` fica fora do score e que as rubricas ficam fora do contexto do executor.

## Ler transcrições

Antes de aceitar uma nota, abra pelo menos as transcrições de uma execução que passou e de uma que falhou por caso. Perguntas: o agente fez o que o grader mede, ou passou por acaso? O grader reprovou algo correto (erro do grader) ou aprovou algo errado? O prompt estava realista? Se o erro for do grader, corrija o grader e registre; não mexa no critério para forçar aprovação.
