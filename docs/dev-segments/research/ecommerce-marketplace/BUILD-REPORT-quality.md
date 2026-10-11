# BUILD-REPORT de qualidade: ecommerce-marketplace

Data: 2026-10-11. Escopo: qualidade de prompt e fidelidade técnica de todo o plugin `C:\Users\Francisco Edson\dev-segments\plugins\ecommerce-marketplace` (README, playbook e referências, 8 skills de tarefa, skill `prompts` e biblioteca, 5 agentes, evals).
Rubrica: `docs/foundation/prompt-quality-rubric.md` (D1–D12, 0–100). Fonte de verdade técnica: `VALIDATED.md` (V-01 a V-59).

**Declaração de independência:** este validador é um modelo Claude, da mesma família dos construtores. A revisão foi adversarial e conferiu fatos contra o `VALIDATED.md` e duas páginas oficiais, mas não equivale a validação externa. As notas abaixo são autoatribuídas por esse revisor (AP-16 de `prompt-principles.md`).

## 1. Método

1. Leitura integral de `playbook/SKILL.md`, das 8 skills de tarefa, de `prompts/SKILL.md`, dos agentes `revisor-checkout`, `arquiteto-loja` e `auditor-pagamentos-integracoes` (os outros dois por seções e tabelas de critérios), do README e de todos os `prompt.md` e graders dos evals.
2. Biblioteca de prompts: amostra de 15 prompts (P-01, P-02, P-03, P-04, P-06, P-11, P-13, P-25, P-27, P-28, P-29, P-30, P-31, P-32, P-33) mais o índice das duas partes.
3. Conferência de afirmações técnicas contra `VALIDATED.md`: V-03, V-07, V-09, V-10, V-14, V-15, V-17, V-29 a V-39, V-42, V-45 a V-51, V-54 a V-59. Varredura por CAPS/ameaças, placeholders e menções a `--dangerously-skip-permissions`.
4. Conferência de direitos autorais: P-27 (trecho literal de cerca de 15 linhas) e P-30 (adaptação) vêm do `brain-of-agent` (MIT, `Copyright (c) 2026 Brain of Agent contributors`, conferido em `docs/foundation/brain-of-agent-snapshot/LICENSE`), com atribuição. O script `documentos_br.py` é cópia integral do repositório do próprio autor (MIT), com cabeçalho de origem. Nenhum literal de terceiros sem licença foi encontrado.
5. WebFetch em https://web.dev/articles/inp e https://web.dev/articles/lighthouse-user-flows para a afirmação "Lighthouse não mede INP".

## 2. Notas antes e depois

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 88 | 88 | Nenhuma necessária. Router, processo com critérios de saída, modo ECOMMERCE-COMPLETO, fronteiras e rótulos completos; fatos (Stripe fora de 2xx, Asaas por token, NTs adiadas para 26/10 e 16/11/2026, Pix 2.10.0) conferem com V-09, V-30, V-31, V-34. |
| `skills/checkout-seguro/SKILL.md` | 86 | 87 | "Lighthouse não mede INP" vira "o relatório padrão (carregamento, sem interação) não mede INP; TBT é proxy (V-15)", com aviso de conferir a versão instalada. |
| `skills/webhook-pagamento/SKILL.md` | 85 | 87 | A delegação dizia que `auditor-pagamentos-integracoes` faz "testes locais e leitura", mas o agente não tem Bash. Agora diz "somente leitura; devolve os comandos de teste para a sessão principal rodar com permissão". |
| `skills/estoque-reserva-pedido/SKILL.md` | 87 | 87 | Nenhuma. Medusa (reserva, locks, cancelamento), Shopify (`committed`, `names`) e Nuvemshop conferem com V-39, V-48, V-49, V-50, V-52. |
| `skills/precos-promocoes/SKILL.md` | 87 | 87 | Nenhuma. As contas 160/162 estão certas; o limite de 25 funções e `productDiscountsAdd` conferem com V-38; o arredondamento está rotulado Inferido. |
| `skills/catalogo-busca-seo/SKILL.md` | 86 | 87 | Gotcha de INP corrigido como no checkout. `theme dev` (7 dias), `sort_by` com até 3 campos, merchant listing e facetas conferem com V-14, V-17, V-37, V-45, V-46. |
| `skills/marketplace-split/SKILL.md` | 87 | 87 | Nenhuma. As 4 perguntas, KYC (revisão a cada 6 meses), MP 1:1 (`marketplace_fee`/`application_fee`) e a rejeição de "B2C nada a fazer" conferem com V-11, V-29, V-47, V-57. |
| `skills/fiscal-frete-br/SKILL.md` | 88 | 88 | Nenhuma. As alíquotas de 2026 (arts. 343/346/348), DIFAL (LC 190/2022, EC 87/2015 com 100% desde 2019), contingência sem números e CFOP/NCM como regra de projeto conferem com V-33, V-56, V-58, V-59. |
| `skills/loja-operacao-segura/SKILL.md` | 85 | 88 | Ficou explícito quem executa a escrita no passo 5: o usuário, ou o agente comando a comando depois do "sim" e da permissão de cada escrita. Em live, o padrão é o usuário executar. O exemplo agora é coerente com isso. Antes, o corpo e o exemplo se contradiziam. |
| `skills/prompts/SKILL.md` | 80 | 86 | Acrescentados: a fronteira negativa na `description` ("não use quando a pessoa quer a tarefa feita agora"); o passo 6, para quando nenhum prompt atende (esqueleto comum, declarado como redação nova); e um `<example>` de entrega. A primeira versão da edição quebrou o YAML (dois-pontos sem aspas) e foi corrigida. |
| Biblioteca de prompts (amostra de 15) | 86 | 87 | P-29: a nota sobre AGENTS.md atribuía a versão 2.1.277 ao `@AGENTS.md`. Corrigido conforme V-07: com o import, os dois arquivos são lidos; sem ele, o CLAUDE.md suprime o AGENTS.md; a leitura direta exige v2.1.277 ou posterior. Os demais prompts têm papel, tags XML, formato de saída, rótulos, fonte com classe e "por que funciona". |
| `agents/revisor-checkout.md` | 90 | 90 | Nenhuma. Somente leitura (sem Bash, com motivo), checklist C1–C14 com detecção, corte de confiança e "Ignorado por ser dado". |
| `agents/arquiteto-loja.md` | 89 | 89 | Nenhuma. |
| `agents/auditor-pagamentos-integracoes.md` | 89 | 89 | Nenhuma. A tabela por provedor confere com V-09, V-30, V-31, V-35, V-41, V-42, V-51. |
| `agents/revisor-a11y-checkout.md` | 88 | 88 | Nenhuma. Os níveis WCAG (3.3.7 A, 3.3.8/2.5.8/1.3.5/1.4.3 AA, 2.3.3 AAA) estão corretos. |
| `agents/auditor-catalogo-seo.md` | 87 | 87 | Nenhuma. |
| Evals (12 → 13 casos + README) | 84 | 87 | Novo caso `prompts-pedido-prompt-webhook-br`, porque a skill `prompts` não tinha disparo medido. Ele tem um `criteria` com PASS/FAIL observáveis e um `skill-fired`. O README dos evals foi atualizado (13 casos, custo de 39 execuções, cobertura, V-30). Os graders já existentes estão bons: há caso negativo com `min: 0, max: 0`, casos de segurança com `no-exec`/`no-write`/`no-store-call` e as contas do caso de cupom estão certas (164/166). |
| `README.md` | 83 | 87 | O agente `auditor-pagamentos-integracoes` aparecia como "Leitura e testes locais"; agora está "Somente leitura". A linha dos evals dizia "10 casos"; agora diz 13. |

Média: 86,4 antes e 87,6 depois (18 artefatos). Mínimo depois: 86 (`prompts/SKILL.md`). Nenhum artefato fica abaixo de 80 e nenhum critério de reprovação automática foi encontrado.

## 3. Verificações de segurança

- Segredos: nenhum valor real. As credenciais aparecem só como nome de variável de ambiente. Verificado por leitura e grep.
- Ações externas e destrutivas: escrita em loja, cobrança, reembolso, emissão fiscal e publicação exigem confirmação humana. A skill `loja-operacao-segura` tem `disable-model-invocation: true`. Verificado.
- Revisores: os 5 agentes têm `tools: Read, Grep, Glob`, sem Write, Edit ou Bash. Verificado.
- `--dangerously-skip-permissions`: 13 menções, todas como risco restrito a sandbox e repositório confiável, nunca como padrão. Verificado.
- Ativos proibidos: não há `hooks/`, `.mcp.json`, `.lsp.json` nem `bin/`. Os hooks aparecem só documentados em `ferramentas-e-mcp.md`. Verificado.
- Conteúdo externo como dado: o tema é tratado em todas as skills e agentes e é testado no eval `injecao-em-pr-e-keyword`. Verificado por leitura.

## 4. Execução dos verificadores (após as edições)

| Comando | Resultado | Rótulo |
| --- | --- | --- |
| `python tools/verify_plugin.py plugins/ecommerce-marketplace` | PASS (10 skills, 5 agentes, 13 evals, 103 arquivos) | Verificado |
| `claude plugin validate plugins/ecommerce-marketplace` | Validation passed (a 1ª rodada falhou no YAML de `prompts/SKILL.md` por edição minha; corrigido e reexecutado) | Verificado |

## 5. Pendências

1. **Lacuna do verificador da fábrica:** `verify_plugin.py` deu PASS com o frontmatter YAML de `prompts/SKILL.md` quebrado (dois-pontos sem aspas na `description`), e só o `claude plugin validate` apontou o erro. Sugestão: o verificador passar a usar um parser YAML estrito. (Verificado neste ciclo.)
2. **INP no Lighthouse:** a afirmação foi atenuada para o relatório padrão. Não verifiquei se a versão atual do Lighthouse mede INP em modo timespan: a página web.dev que li (2021) cita só TBT e CLS em timespans. Rótulo: Não verificável até ler a documentação vigente do Lighthouse.
3. **Evals sem execução:** os 13 casos seguem `designed_not_executed`. O caso novo também precisa de uma rodada com `claude plugin eval .` (Claude Code 2.1.269 ou superior) para calibrar o juiz.
4. **Agentes sem caso de eval próprio** (registrado no README dos evals): faltam casos de delegação ao `revisor-checkout` e de `revisor-a11y-checkout` sem renderização.
5. **SYNTHESIS §4.8:** o template `matriz-ecommerce-completo.md` não está listado (pendência do validador estrutural). O plugin está correto; quem precisa ser atualizado é o SYNTHESIS.
6. **Repetição do gotcha `--dangerously-skip-permissions`:** aparece em cada skill. Mantive porque é regra da fábrica, ao custo de algumas linhas por skill (D9). Decisão do usuário: centralizar no playbook ou manter.
