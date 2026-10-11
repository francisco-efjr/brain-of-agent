# BUILD-REPORT consolidado: ecommerce-marketplace

Data: 2026-10-11. Plugin: `C:\Users\Francisco Edson\dev-segments\plugins\ecommerce-marketplace`.
Fontes consolidadas: `BUILD-REPORT-structural.md` (validação estrutural) e `BUILD-REPORT-quality.md` (qualidade de prompt e fidelidade técnica). Esta consolidação refaz as validações no estado atual do plugin.

## 1. Resultado final (gate)

| Verificação | Comando | Resultado | Rótulo |
|---|---|---|---|
| Verificador da fábrica | `python tools\verify_plugin.py <pasta>` | PASS, 0 erros, 0 avisos (10 skills, 5 agentes, 0 commands, 13 evals, 103 arquivos) | Verificado |
| Validador oficial | `claude plugin validate <pasta>` | "Validation passed" | Verificado |

Correções necessárias nesta rodada: nenhuma. Ambas as validações passaram sem alteração no plugin.

Observação sobre o relatório estrutural: ele registra 12 evals e 100 arquivos. Esses números estão defasados. O estado atual é 13 evals e 103 arquivos, pois o caso `prompts-pedido-prompt-webhook-br` foi acrescentado depois (ver relatório de qualidade, seção 2).

## 2. Contagem de componentes

| Componente | Quantidade | Detalhe | Rótulo |
|---|---|---|---|
| Skills | 10 | 8 de tarefa (`checkout-seguro`, `webhook-pagamento`, `estoque-reserva-pedido`, `precos-promocoes`, `catalogo-busca-seo`, `marketplace-split`, `fiscal-frete-br`, `loja-operacao-segura`), mais `playbook` e `prompts` | Verificado |
| Agentes (subagentes) | 5 | `revisor-checkout`, `arquiteto-loja`, `auditor-pagamentos-integracoes`, `revisor-a11y-checkout`, `auditor-catalogo-seo` | Verificado |
| Blocos de prompt na biblioteca | 35 | 22 em `prompt-library.md` (P-01 a P-22) e 13 em `prompt-library-catalogo-fiscal-ops.md` | Verificado |
| Casos de eval | 13 | Cada um com `prompt.md` e graders; todos `designed_not_executed` | Verificado |
| Arquivos de referência | 28 | Dentro de `references/` das skills (12 no `playbook`, 16 nas demais) | Verificado |
| Templates (assets) | 14 | Em `skills/playbook/assets/templates/` | Verificado |
| Scripts (assets) | 1 | `skills/playbook/assets/scripts/documentos_br.py` (MIT, com cabeçalho de origem) | Verificado |
| Arquivos totais | 103 | Verificador da fábrica | Verificado |

Ativos desativados (conforme a política): nenhum `hooks/`, `.mcp.json`, `.lsp.json` ou `bin/`.

## 3. Qualidade de prompt e fidelidade técnica

- Média de qualidade: 86,4 antes e 87,6 depois das correções, em 18 artefatos. Mínimo depois: 86 (`skills/prompts/SKILL.md`). Nenhum artefato abaixo de 80. Autoavaliação do revisor (mesma família de modelo); não equivale a validação externa. Rótulo: Inferido.
- Correções aplicadas na rodada de qualidade (todas já no plugin):
  - `checkout-seguro` e `catalogo-busca-seo`: a afirmação "Lighthouse não mede INP" foi atenuada para o relatório padrão, com TBT como proxy.
  - `webhook-pagamento`: a delegação ao `auditor-pagamentos-integracoes` foi corrigida, pois o agente é somente leitura e não tem Bash.
  - `loja-operacao-segura`: ficou explícito quem executa a escrita no passo 5.
  - `prompts/SKILL.md`: acrescentadas fronteira negativa, passo para quando nenhum prompt atende e um `<example>`. Uma edição intermediária quebrou o YAML e foi corrigida.
  - Biblioteca, P-29: a versão do `@AGENTS.md` foi corrigida conforme V-07.
  - `README.md` e evals: agente marcado como "Somente leitura"; evals atualizados para 13 casos.
- Fatos conferidos contra `VALIDATED.md`: Stripe, Asaas, NTs 26/10 e 16/11/2026, Pix 2.10.0, Medusa, Shopify, Nuvemshop, Mercado Pago, alíquotas 2026, DIFAL, WCAG e o limite de 25 funções. Conferência por leitura, não por execução.

## 4. Segurança e direitos autorais

- Segredos: nenhum valor real. Credenciais aparecem só como nome de variável de ambiente. Verificado.
- Escrita externa, cobrança, reembolso, emissão fiscal e publicação exigem confirmação humana. `loja-operacao-segura` tem `disable-model-invocation: true`. Verificado.
- Agentes: 5 com `tools: Read, Grep, Glob`, sem Write, Edit ou Bash (o `revisor-checkout`, o `arquiteto-loja` e os demais declaram o motivo quando necessário). Verificado.
- `--dangerously-skip-permissions`: 13 menções, todas como risco restrito a sandbox e repositório confiável, nunca como padrão. Verificado.
- Literais de terceiros: P-27 (trecho de cerca de 15 linhas) e P-30 (adaptação) vêm de `brain-of-agent` (MIT), com atribuição. `documentos_br.py` é cópia integral de repositório MIT, com cabeçalho. Nenhum literal sem licença encontrado. Verificado por leitura.
- Conteúdo externo tratado como dado em todas as skills e agentes, com caso de teste `injecao-em-pr-e-keyword`. Verificado por leitura.

## 5. Consistência estrutural

- README: 10 skills e 5 agentes, todos existentes. Verificado.
- Caminhos `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/` resolvem. Verificado.
- Referências cruzadas entre skills e agentes resolvem. Verificado.
- Plugins irmãos citados no `playbook/SKILL.md` existem como pasta e têm `skills/playbook/SKILL.md`. Conteúdo deles não verificado. Não verificado.
- Falso positivo descartado: `localhost:3000` em `e2e-playwright-checkout.md` é URL de desenvolvimento.

## 6. Pendências

1. Template `matriz-ecommerce-completo.md` não aparece no SYNTHESIS §4.8 (que prevê 12). Sugestão: atualizar o SYNTHESIS, não o plugin. Rótulo: Inferido.
2. Evals não executados: os 13 casos seguem `designed_not_executed`. Falta rodar `claude plugin eval .` (Claude Code 2.1.269 ou superior) para calibrar o juiz, em especial o caso novo. Rótulo: Não verificado.
3. Agentes sem caso de eval próprio: delegação ao `revisor-checkout` e `revisor-a11y-checkout` sem renderização. Rótulo: Verificado (lacuna real).
4. Lacuna do verificador da fábrica: `verify_plugin.py` deu PASS com YAML quebrado em `prompts/SKILL.md`; só o `claude plugin validate` acusou. Sugestão: parser YAML estrito no verificador. Rótulo: Verificado na rodada de qualidade.
5. INP no Lighthouse: a documentação vigente não foi lida. A afirmação foi atenuada por precaução. Rótulo: Não verificável até ler a documentação atual do Lighthouse.
6. Gotcha de `--dangerously-skip-permissions` repetido em cada skill (custo de algumas linhas por skill, D9). Decisão do usuário: centralizar no playbook ou manter.

## 7. Saídas resumidas das validações

```
verify_plugin.py: Plugin: ecommerce-marketplace {'skills': 10, 'agents': 5, 'commands': 0, 'evals': 13, 'files': 103}
verify_plugin.py: RESULT: PASS
claude plugin validate: Validating plugin manifest: .claude-plugin\plugin.json
claude plugin validate: Validation passed
```

## 8. Conclusão

O plugin passa no verificador da fábrica (0 erros, 0 avisos) e no validador oficial. Os componentes previstos estão presentes. As pendências são de execução de evals, documentação do SYNTHESIS e uma lacuna do verificador, não bloqueiam o gate.
