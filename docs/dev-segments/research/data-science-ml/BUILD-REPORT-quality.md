# BUILD-REPORT qualidade de prompt: data-science-ml

Data: 2026-10-10. Papel: validador independente de qualidade de prompt e conteúdo técnico (rubrica D1 a D12, 0 a 100). Declaração de independência: o validador é do mesmo fornecedor de modelo dos construtores (mesma família); a independência é de contexto, não de fornecedor. As notas são estimativas por leitura (Suposição), não medição; nenhum eval foi executado.

## 1. Método

Leitura integral de README, `playbook`, 8 skills de tarefa, `prompts` (SKILL e 12 prompts amostrados: PR-01, 05, 08, 11, 14, 16, 19, 20, 23, 27, 32, 33), 5 agentes e os 10 casos de eval com todos os graders. Referências lidas por amostragem: `ferramentas-e-mcp`, `padroes-e-antipadroes` (seção 4), `fontes`, snippets de avaliação, backtest, inferência, eval de LLM e tuning, e 3 templates. Contas conferidas à mão: SRM 25,6 (p ≈ 4,2e-7), 1 − 0,95^20 = 0,6415, n ≈ 15,7·σ²/δ², Wilson 27/30 = 0,744 a 0,965, Wilson 0/30 = 0 a 0,114, pass^3 = 0,422, pass@3 e pass^3 do exemplo (0,708 e 0,0083), Rogan-Gladen do exemplo (0,87). Todas corretas.

## 2. Fidelidade técnica (fontes oficiais consultadas em 2026-10-10)

| Afirmação do plugin | Fonte consultada | Resultado |
| --- | --- | --- |
| `Read` deny bloqueia Edit e Write no mesmo caminho; `Edit` deny cobre ferramentas de edição; `/path` ancorado na raiz do projeto, `//path` absoluto | https://code.claude.com/docs/en/permissions | Verificado |
| `Stop` não aceita matcher; exit 2 em `Stop` impede parar e em `PreToolUse` bloqueia; `onFailure` exige v2.1.295 | https://code.claude.com/docs/en/hooks | Verificado |
| `disallowed-tools` é campo válido de skill | https://code.claude.com/docs/en/skills | Verificado |
| `allowed-tools` apenas pré-aprova, não restringe | https://code.claude.com/docs/en/skills | Verificado; gerou a correção 2 abaixo |
| scikit-learn 1.9.1, PyTorch 2.14 | `VALIDATED.md` linhas 209 e 285 (registradas pela pesquisa) | Verificado no registro; não reaberto nas páginas |
| `TargetEncoder` (sklearn 1.3+), `CalibratedClassifierCV(estimator=)` (1.2+), `early_stopping` do LightGBM por callback, `early_stopping_rounds` no construtor do XGBoost 2.x, `scale_pos_weight` e `max_delta_step` | conhecimento estável; o plugin já rotula "confira a versão" | Inferido, coerente |

Nenhuma afirmação técnica incorreta foi encontrada. Nenhum trecho literal acima de 40 linhas; as atribuições (MIT de pitcany, param087, ECC, claude-cookbooks, brain-of-agent) estão em `fontes.md` e nos blocos "Fonte" de cada prompt. Sem segredos. Todos os cinco agentes têm `tools: Read, Grep, Glob`. Nenhum hook, `.mcp.json`, `.lsp.json` ou `bin/`. `--dangerously-skip-permissions` aparece apenas como risco (sandbox, repositório confiável).

## 3. Notas D1 a D12 (antes e depois) e correções

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `README.md` | 84 | 90 | Removida linguagem de fábrica ("33 planejados", "componentes escritos em paralelo"); acrescentado o contrato de entrega dos agentes (somente leitura, relatório na resposta) |
| `skills/playbook/SKILL.md` | 90 | 93 | Exemplo concreto de fechamento de incremento (D5), com placeholders em vez de números |
| `skills/prompts/SKILL.md` + biblioteca (12 prompts amostrados) | 90 | 90 | Sem alteração: estrutura, variáveis visíveis, avisos de dado/instrução, limites de escrita e fontes presentes |
| `skills/ds-leakage-audit/SKILL.md` | 91 | 94 | `disallowed-tools: Write, Edit, NotebookEdit, Bash` (a doc oficial diz que `allowed-tools` só pré-aprova); texto passa a descrever a garantia real |
| `skills/ds-eda/SKILL.md` | 90 | 90 | Sem alteração |
| `skills/ds-model-evaluation/SKILL.md` | 91 | 91 | Sem alteração |
| `skills/ds-train-debug/SKILL.md` | 89 | 89 | Sem alteração |
| `skills/ds-time-series-backtest/SKILL.md` | 90 | 90 | Sem alteração |
| `skills/ds-inference-review/SKILL.md` | 86 | 91 | Taxonomia do veredito inconsistente (formato listava 3 valores, exemplo dizia "nenhuma conclusão"): acrescentado `inconclusiva` com regra de uso e exemplo alinhado |
| `skills/ds-llm-eval/SKILL.md` | 91 | 91 | Sem alteração |
| `skills/ds-mlops-promotion/SKILL.md` | 90 | 90 | Sem alteração |
| `agents/ds-leakage-auditor.md` | 92 | 92 | Sem alteração |
| `agents/ds-experiment-reviewer.md` | 91 | 91 | Sem alteração |
| `agents/ds-model-promotion-reviewer.md` | 91 | 91 | Sem alteração |
| `agents/ds-inference-reviewer.md` | 87 | 91 | Mesmo veredito `inconclusiva` no processo e no formato de saída |
| `agents/ds-eval-auditor.md` | 90 | 90 | Sem alteração |
| `evals/` (10 casos, 12 depois) | 83 | 89 | Dois casos novos: `keyword-completo-em-readme` (keyword em conteúdo lido não ativa o modo; nota injetada citada; nenhum comando) e `pergunta-pontual-sem-referencias` (proporcionalidade, sem ler referências). README dos evals atualizado (12 casos, 36 execuções, cobertura) |

Média antes: 89,3 (17 itens agrupados). Média depois: 91,0. Mínimo antes: 83 (evals). Mínimo depois: 89. Nenhum componente abaixo de 80 antes ou depois.

## 4. Observações adversariais sem correção (baixo risco)

- Os blocos "Fonte" citam "corrigido pelo validador" e "reescrito pelo validador": rastreio de proveniência, útil, mas é histórico de fábrica dentro de um produto. Mantido por rastreabilidade (D9 levemente penalizado).
- Skills de tarefa herdam `allowed-tools: Read, Grep, Glob` por convenção; como isso só pré-aprova, o limite real depende das permissões do usuário. Apenas `ds-leakage-audit` e `prompts` impõem restrição com `disallowed-tools`. `ds-mlops-promotion` e as demais podem precisar gravar relatórios em `reports/` a pedido, por isso não foram restringidas.
- Os dois casos novos excedem a faixa 6 a 10 do blueprint (agora 12); a lacuna que fecham (ativação indevida do modo completo e proporcionalidade) justifica, e o verificador não impõe teto.
- Graders `tool_used` com `max: 3` (referências do playbook) e os regex de `no-exec` dependem de o runner comparar com o JSON serializado da chamada: Não verificado (CLI local 2.1.128 < 2.1.269).

## 5. Pendências

1. Executar `claude plugin eval .` (Claude Code 2.1.269 ou superior), 3 execuções por caso, com e sem plugin; calibrar os graders `llm` contra leitura humana.
2. Comando opcional `commands/ds-validate.md` continua ausente (decisão do dono do plugin); README, playbook e prompts já tratam como "não incluído".
3. Casos de eval para cada agente (contrato de entrega, modo sem interação), notebooks reprodutíveis, visualização e tuning de GBM.
4. Lacunas de conteúdo já declaradas: interpretabilidade e justiça, ranking, CatBoost, deep learning além do loop, ML embarcado, fontes primárias de A/B (Kohavi/ExP) e de causal (Hernán e Robins) não lidas.
5. Revisão humana ou de outro fornecedor de modelo para independência real.
