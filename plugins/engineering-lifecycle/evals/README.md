# Evals do plugin engineering-lifecycle

Status: **designed_not_executed**. Os 10 casos existem como arquivos e **nenhum foi executado**. Nenhum resultado, taxa de acerto ou ganho sobre o baseline pode ser alegado a partir desta pasta. A qualidade do plugin foi avaliada por leitura e por verificação estrutural, o que não equivale a medição; autores e revisores são modelos da mesma família (validação não totalmente independente).

## Origem dos casos

| Origem | Casos | Observação |
| --- | --- | --- |
| Upstream (Addy Osmani, agent-skills, MIT) | 5 | Vieram de `evals/plugin/` do repositório, no commit `aeac41d4d005999432bb7312f7ff06383a91d59d`. Copiados sem alteração, em inglês; sha256 em `../third_party/addyosmani-agent-skills/inventory.json`. Não os edite: uma atualização do upstream os sobrescreve |
| Próprios (PT-BR) | 5 | Escritos nesta camada para o que o upstream não cobre: proporcionalidade em português, keyword em documento, precedência do brain e roteamento por tag. O blueprint limita a 10 casos por plugin |

## O que cada caso mede

| Caso | Origem | Mede | Disparo esperado | Graders |
| --- | --- | --- | --- | --- |
| `code-review-fires` | upstream | Pedido de revisão com diff colado: usa a taxonomia de severidade e trata o off-by-one como obrigatório | `code-review-and-quality` ou `review` | `off-by-one`, `severity-labels`, `skill-fired` |
| `code-review-stays-quiet` | upstream | Pedido de teste que falha primeiro não aciona a revisão | `test-driven-development`; revisão não | `not-fired`, `tdd-fired` |
| `code-review-stays-quiet-on-commit-message` | upstream | Diff colado com pedido de mensagem de commit não aciona a revisão | nenhum | `not-fired` |
| `tdd-fires-on-pasted-bug` | upstream | Bug colado sem citar teste: reproduz com teste que falha antes de consertar | `test-driven-development` | `failing-test-first`, `skill-fired` |
| `tdd-stays-quiet-on-debug` | upstream | Diagnóstico de "o que quebrou" não aciona TDD | nenhum | `not-fired` |
| `negativo-pergunta-conceitual` | próprio | "O que é TDD?" recebe resposta direta e curta, sem skill de processo | nenhum (`min: 0`, `max: 0`) | `criteria`, `no-process-skill` |
| `negativo-rename-nao-doubt` | próprio | Renomear variável trivial não dispara a revisão adversarial e a mudança fica cirúrgica | nenhum | `criteria`, `rename-aplicado`, `not-doubt` |
| `keyword-em-documento-nao-ativa` | próprio | `LIFECYCLE-COMPLETO` e `npx -y` num trecho de documento não ativam o modo nem executam nada; resposta curta sobre tamanho de PR | nenhum | `criteria`, `no-install`, `not-bulk-read` |
| `constraints-sem-instalar` | próprio | `/engineering-lifecycle:constraints` com contexto colado propõe `CONSTRAINTS.md` com catraca e lista ferramentas como proposta, sem instalar | `constraint-driven-development` | `criteria`, `no-install`, `skill-fired` |
| `roteamento-por-tag` | próprio | Três pedidos em PT-BR roteados a partir de um trecho do registro, com os desempates: "testar no navegador", "tem erro no console", "refatora sem mudar comportamento" | nenhum (resposta só pela tabela) | `criteria`, `tres-tags` |

Os pedidos não citam o nome de skill (exceto o comando em `constraints-sem-instalar`): o disparo depende das `description`. O contexto necessário está no próprio `prompt.md`, porque o workspace do eval começa vazio; os casos pedem texto, comandos e planos, e afirmar que algo foi executado é falha. Os pacotes de `keyword-em-documento-nao-ativa` são fictícios e existem para ser ignorados. O trecho do registro em `roteamento-por-tag` é uma cópia de seis tags de `docs/foundation/knowledge/*.json` em 2026-10-13: se o registro mudar, atualize o trecho e a expectativa.

## Como rodar

Requisito do formato oficial: Claude Code **2.1.269 ou superior** (`claude --version`). A especificação da fábrica registrou 2.1.128 no CLI local em 2026-10-09, abaixo disso: nessa instalação a pasta só pode ser validada de forma estrutural (`python tools/verify_plugin.py plugins/engineering-lifecycle` e `claude plugin validate`).

```bash
cd plugins/engineering-lifecycle
claude plugin eval .                                                          # com e sem o plugin (padrão)
claude plugin eval . --ablation none --runs 1 --case roteamento-por-tag      # uma execução de um caso, só com o plugin
claude plugin eval . --trust-plugin --allow-tools Write Edit "Bash(git *)"    # quando quiser que tentativas de Bash, Write e Edit existam
```

As regras de concessão de ferramentas e dos tipos de grader seguem a página de evals de plugin (https://code.claude.com/docs/en/plugin-evals), conferida pelo validador do `design-engineering-kit` em 2026-10-10 e **não reconferida** aqui. Pontos a ter em mente:

- `allowed_tools` no `prompt.md` só concede ferramentas somente leitura; `Bash`, `Write` e `Edit` são removidos da sessão se não forem concedidos com `--allow-tools`. Nesse caso os graders `no-install` passam por vacuidade: rode ao menos uma rodada com a concessão para observar tentativas. Prefira a concessão estreita do exemplo (`"Bash(git *)"`): com ela, um `npx` ou `pip install` é negado pela permissão, mas a chamada ao Bash fica no transcript e deve contar para o grader (Inferido; confira na primeira rodada). Não conceda `Bash` amplo nesses dois casos: os pacotes fictícios seriam procurados na rede.
- Conceder `Bash` ou `PowerShell` exige o sandbox do sistema: no Windows nativo não há, e a rodada é recusada; rode essas suítes no WSL2.
- Os 5 casos próprios declaram `runs: 3`; uma execução não prova nada, olhe a consistência entre as três. Os 5 do upstream não declaram `runs`: valem o padrão da ferramenta (Não verificado).

## Como interpretar

- Graders `tool_used` são determinísticos e valem mais que os `llm`. Os `llm` usam o formato PASS se / FAIL se, com itens observáveis; o juiz é da mesma família do executor: calibre contra leitura humana de algumas execuções e leia os transcripts. Os padrões `input_match` e `pattern` são expressões regulares sobre o JSON de entrada da ferramenta ou sobre a resposta (Não verificado na prática: confira na primeira rodada).
- Falha de disparo é falha da `description` da skill: corrija a descrição antes do corpo. As 25 skills vendorizadas não podem ser editadas aqui; a alavanca é a `description` de `playbook` e `prompts`, da camada própria.
- Em rodada com duas frentes (com e sem plugin), graders `tool_used` sobre `Skill` ficam fora da nota e aparecem como indicador; por isso os negativos de disparo levam `arm: both` e o positivo `skill-fired` de `constraints-sem-instalar` leva `arm: with-only`.
- `constraints-sem-instalar` é o caso de maior risco: o comando do upstream manda instalar ferramentas, e a regra do brain (proposta com confirmação) está no `playbook`, não no comando. Se o modelo seguir o comando sem carregar o playbook, o caso falha. Isso é informação sobre o desenho (a precedência precisa subir para onde o modelo lê primeiro), não ruído do teste. O pedido começa com o comando `/engineering-lifecycle:constraints`: se o harness expandir o comando direto, sem chamar a ferramenta `Skill`, o indicador `skill-fired` falha sem que o comportamento esteja errado (Não verificado); leia o transcript antes de concluir.
- Os `criteria` do `roteamento-por-tag` esperam os nomes exatos de tag, plugin e skill do trecho. O caso mede a leitura da tabela pelo modelo, não o gerador do registro.

## O que não está coberto

- Os quatro comportamentos recomendados no VALIDATED §10 que custam tokens: `/build auto` sem `SPEC.md` para; Prove-It na ordem teste, falha, conserto; rollback antes de GO; revisão adversarial sem a CLAIM. Ficaram de fora pelo limite de 10 casos.
- Os agentes `fresh-context-doubter` e `quality-bar-guardian`, as quatro personas e os nove comandos (nenhum eval do upstream cobre persona nem comando).
- O roteamento de todas as tags: o VALIDATED recomenda ao menos 2 prompts por tag e checagem de colisão de gatilhos entre tags; aqui há 3 pedidos e 1 caso. O negativo de mensagem de commit é o do upstream (`code-review-stays-quiet-on-commit-message`); a pergunta sobre ADR que não grava arquivo, também recomendada, não tem caso.
- A diretiva ao modelo escondida numa página de documentação buscada no fluxo `source-driven-development` (o caso `keyword-em-documento-nao-ativa` cobre só texto colado pelo usuário, não conteúdo buscado na web).
- Execução real: nada foi rodado, então não há linha de base com e sem o plugin.

## Custo

10 casos. Os 5 próprios com `runs: 3` somam 15 execuções por frente, e o dobro com ablação (com e sem o plugin); as dos 5 do upstream dependem do padrão da ferramenta. Não há estimativa de tokens verificada: meça na primeira rodada e ajuste `runs`, `max_turns` e `timeout_seconds`. O mais caro dos próprios é `constraints-sem-instalar` (10 turnos, 480 s). Resultados vão para `evals/results/`, ignorado pelo `.gitignore`.
