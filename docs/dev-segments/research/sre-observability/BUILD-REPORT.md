# BUILD-REPORT consolidado: plugin `sre-observability`

Data: 2026-10-10 · Papel: gate final (verificador determinístico + validador oficial + contagem de componentes) · Escopo: `plugins/sre-observability`

Fontes consolidadas: `BUILD-REPORT-structural.md` (validador estrutural) e `BUILD-REPORT-quality.md` (validador de qualidade de prompt e conteúdo técnico).

## 1. Resumo

- Resultado do gate: **PASS**. O verificador determinístico terminou com `RESULT: PASS` e sem erros; o validador oficial `claude plugin validate` terminou com `Validation passed`.
- Nenhuma correção nova foi necessária nesta etapa do gate. As correções de conteúdo já foram aplicadas pelo validador de qualidade (ver seção 4).
- Pendências que dependem de ação do usuário ou de ambiente (execução de evals, marketplace, fonte do Lighthouse timespan) estão na seção 6. Nenhuma delas bloqueia o gate estrutural.

## 2. Contagem de componentes

Contagens feitas nesta etapa com `find` e pelo próprio verificador. Verificado.

| Componente | Quantidade | Observação |
| --- | --- | --- |
| Skills (`skills/*/SKILL.md`) | 11 | 9 de tarefa + `playbook` + `prompts` |
| Agentes (`agents/*.md`) | 4 | `incident-support`, `reliability-reviewer`, `postmortem-scribe`, `perf-analyst`; somente `Read, Grep, Glob` |
| Commands | 0 | pasta `commands/` ausente, previsto |
| Casos de eval (`evals/<caso>/`) | 14 | 12 originais + 2 novos (`pergunta-pontual-burn-rate`, `negativo-refatorar-funcao-python`); todos `designed_not_executed` |
| Prompts na biblioteca (blocos de prompt) | 36 | PR-01 a PR-24 em `prompt-library.md` (24) e PR-25 a PR-36 em `prompts-resiliencia-e-operacao.md` (12) |
| Arquivos de referência (`skills/*/references/`) | 27 | incluindo `prompt-library.md` e `prompts-resiliencia-e-operacao.md` |
| Templates (`skills/playbook/assets/templates/`) | 15 | |
| Arquivos totais no plugin | 103 (verificador) | `find` contou 105 incluindo `README.md` e o manifesto; a diferença é de critério de contagem do verificador, não de conteúdo |

Divergência de contagem: o relatório estrutural registrou 12 casos de eval e 98 arquivos. Ambos os números são anteriores à etapa de qualidade, que acrescentou 2 casos. Os valores atuais são 14 casos e 103 arquivos (verificador).

## 3. Saídas resumidas das validações

Verificado nesta etapa:

- `python tools/verify_plugin.py plugins/sre-observability`: `Plugin: sre-observability {'skills': 11, 'agents': 4, 'commands': 0, 'evals': 14, 'files': 103}` · `RESULT: PASS` · exit 0.
- `claude.exe plugin validate plugins/sre-observability`: `Validating plugin manifest: ...\.claude-plugin\plugin.json` · `✔ Validation passed` · exit 0.

Checagens do relatório estrutural (repetidas aqui como registro, não reexecutadas nesta etapa): frontmatter de 11 skills e 4 agentes conforme; nenhum link relativo quebrado; nenhum arquivo vazio; `plugin.json` sem campos desconhecidos; sem hooks, `.mcp.json`, `.lsp.json` ou `bin/`; `release-health` com `disable-model-invocation: true`.

Checagens do relatório de qualidade (Verificado na época, com 67 URLs consultadas): todas responderam 200, exceto placeholders de exemplo e o repositório `brain-of-agent`, que respondeu 404 sem autenticação.

## 4. Notas (o que mudou na etapa de qualidade)

- Nota média dos 30 itens avaliados individualmente subiu de 89,2 para 91,6; mínimo 88; nenhum item abaixo de 80. Notas são julgamento de leitura, não medição.
- Correções factuais aplicadas: limiares "ruim" de Core Web Vitals (4 s, 500 ms, 0,25) agora Verificados nas páginas individuais do web.dev; Lighthouse e INP qualificados por modo de medição; código de saída 99 do k6 Verificado com ressalva; exemplo do limiar de 35× do Workbook reescrito.
- Permissões: `Write` removido de `allowed-tools` em várias skills; nenhuma skill pré-aprova `Bash` sem padrão. `root-cause-investigation` pré-aprova apenas `git log`, `git diff` e `git show`.
- Inconsistência corrigida: README dizia 8 passos em `slo-design`; a skill tem 9.
- Segurança: todas as skills de tarefa e os agentes declaram conteúdo lido como dado; três evals testam injeção com texto hostil.
- Direitos autorais: fontes de terceiros (MIT/Apache-2.0) creditadas e sem trecho literal.
- Desvio aceito do plano (SYNTHESIS 4.6): as cinco referências temáticas previstas para `prompts` não foram criadas. Os 36 prompts estão em dois arquivos com sumário e índice no `SKILL.md`. Registrado como decisão.

## 5. Notas de rótulo

Verificado: resultados do verificador e do validador oficial, contagens, existência de arquivos. Inferido: modo timespan do Lighthouse (fonte de blog, não página oficial estável). Não verificável: execução dos evals (CLI local anterior a 2.1.269), visibilidade do repositório `brain-of-agent`, marketplace da raiz de `dev-segments`.

## 6. Pendências

1. Executar `claude plugin eval` com Claude Code 2.1.269 ou superior (3 execuções por caso) e ler os transcripts antes de citar taxa de acerto. Ação do usuário.
2. Publicar o marketplace: `.claude-plugin/marketplace.json` não existe na raiz de `dev-segments`, embora o `plugin-format-spec.md` o descreva. Confirmar também a visibilidade do repositório `francisco-efjr/brain-of-agent`, que respondeu 404 sem autenticação. Ação do usuário.
3. Confirmar o modo timespan do Lighthouse em documentação oficial atual (a página de user flows retornou 404 na consulta).
4. Itens sem fonte classe A (já rotulados Não verificável no plugin): profilers por linguagem, consulta lenta de banco, head versus tail sampling, estrutura oficial de runbook, template de postmortem do PagerDuty, crash reporting e RUM de mobile.
5. Opcional: reduzir a repetição do bloco "Plataformas" nos quatro agentes; criar eval isolado por agente e um eval do modo `SRE-COMPLETO` legítimo.
6. Os códigos P-nn, C-nn e PAD-nn na biblioteca remetem a `docs/foundation/prompt-principles.md`, que não viaja com o plugin. Há uma nota no arquivo; o ideal é manter só o motivo escrito.

## 7. Resultado do gate

- `verify_plugin.py`: PASS, sem erros.
- `claude plugin validate`: passou.
- Correções nesta etapa: nenhuma.
