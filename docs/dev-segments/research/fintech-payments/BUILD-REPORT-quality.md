# BUILD-REPORT de qualidade — fintech-payments

Data: 2026-10-11. Escopo: qualidade de prompt e fidelidade técnica de todo o plugin `plugins/fintech-payments` (README, playbook e referências, 8 skills de tarefa, skill `prompts` e biblioteca, 5 agentes, 10 evals). Rubrica: `docs/foundation/prompt-quality-rubric.md` (D1–D12, 0–100).

Independência: o validador é um modelo da família Claude (Opus 5.5), diferente do construtor, mas da mesma família. A revisão foi adversarial, mas **não equivale a validação externa**. As notas vêm de leitura crítica, não de medição: nenhum eval foi executado.

## 1. Método

1. Leitura integral: 10 `SKILL.md`, 5 agentes, README, `plugin.json`, `evals/` inteiro (10 casos, 25 graders, README, `.gitignore`), `guardrails.md`, início de `ferramentas-e-mcp.md`.
2. Biblioteca de prompts: 20 prompts lidos inteiros (PR-01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 13, 17, 18, 19, 20, 21, 22, 23, 25, 28); os 28 IDs conferidos nos sumários e na tabela da skill.
3. Demais referências: varredura por `Grep` (CAPS e absolutos, placeholders, IDs internos `TP-nn`, `--dangerously-skip-permissions`, "sete itens", tamanho das `description`).
4. Fidelidade técnica conferida contra `VALIDATED.md` (fonte de verdade): retenção e limites de chave da Stripe (24 h, 255) e da Adyen (7 a 14 dias, 64, 422/409/704, 503/703); tolerância de 5 min e reenvio 15/30 dias da Stripe; 200/201 em 22 s do Mercado Pago; TLS 1.2/1.3 da Pagar.me; Pix (txid 26 a 35, Saque/Troco, TLS com forward secrecy, logs ≥ 1 ano, CRC `1D3D`); 3DS (exceções, SDK ≥ 5 min, iframe sem `sandbox`); disputas (EFW ~40%, arbitragem até USD 600); deny de `Read` cobrindo Edit (v2.1.208) e Write (v2.1.228); Asaas 14 dias e 15 falhas. Todos coerentes.
5. Fonte oficial reaberta (WebFetch, 2026-10-11): https://www.gov.br/anpd/pt-br/assuntos/incidente-de-seguranca. **Verificado**: os sete itens são o conteúdo mínimo da comunicação **ao titular** (art. 9º); a página não lista o conteúdo do art. 6º (ANPD). A tentativa de abrir o texto integral no DOU falhou (`socket hang up`): art. 6º segue **Não verificado**.
6. Execuções locais do validador: script de conciliação do `reconciliation-analyst` com os dados do exemplo (saída igual à declarada) e com uma linha duplicada (revelou o defeito abaixo); `documentos_br.py --self-test` (OK) e `gerar cnpj-alfa`.
7. Correções aplicadas direto nos arquivos; verificador e validador oficial rodados no fim.

## 2. Notas antes e depois

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 90 | 90 | Nenhuma. Forte em D2, D7, D8, D11. Ressalva D9: tabela de fronteiras com 24 plugins carregada a cada disparo |
| `skills/prompts/SKILL.md` | 88 | 88 | Nenhuma (roteamento por Grep, proporcionalidade, exemplo de entrega) |
| `skills/payment-idempotency/SKILL.md` | 91 | 91 | Nenhuma; números de Stripe e Adyen conferidos |
| `skills/webhook-handler/SKILL.md` | 90 | 90 | Nenhuma; regra de provedor sem assinatura e Pix/mTLS coerentes com VALIDATED |
| `skills/pix-boleto-br/SKILL.md` | 90 | 90 | Nenhuma; lacunas normativas bem rotuladas |
| `skills/money-ledger-design/SKILL.md` | 89 | 89 | Nenhuma; vetores de arredondamento conferidos por raciocínio (Decimal de string) |
| `skills/reconciliation-disputes/SKILL.md` | 90 | 90 | Nenhuma |
| `skills/payment-code-review/SKILL.md` | 91 | 91 | Nenhuma (somente leitura, fallback inline declarado, calibragem, exemplo de achado) |
| `skills/payment-test-plan/SKILL.md` | 90 | 90 | Nenhuma; script local verificado |
| `skills/go-live-and-guardrails/SKILL.md` | 87 | 90 | D12: o passo de incidente apresentava os sete itens como conteúdo da comunicação "à ANPD e aos titulares". Corrigido: sete itens = art. 9º (titular), Verificado na página da ANPD em 2026-10-11; comunicação à ANPD segue art. 6º e o formulário do SEI!ANPD (Não verificado). Formato de saída e Gotchas atualizados |
| `agents/payment-reviewer.md` | 92 | 92 | Nenhuma (Read/Grep/Glob, formato fixo, caso sem achado, segredo citado só pelo nome) |
| `agents/payments-architect.md` | 90 | 90 | Nenhuma |
| `agents/payment-debugger.md` | 91 | 91 | Nenhuma (limites de Bash/Edit explícitos, reparo de dados só proposto) |
| `agents/payment-test-engineer.md` | 90 | 90 | Nenhuma |
| `agents/reconciliation-analyst.md` | 86 | 90 | D7/D12: o script de apoio sobrescrevia linhas com chave repetida, então contagem e soma por partição **escondiam a duplicata** (contradizendo a classe `DUPLICADA`). Corrigido para contar todas as linhas na partição e casar pela primeira ocorrência; reexecutado com e sem duplicata. ID interno `TP-07` (não resolvível) trocado pelo template `relatorio-conciliacao.md` |
| Biblioteca de prompts (20 amostrados) | 86 | 89 | D10: seis ênfases em CAPS ("NÃO") em PR-05, PR-10 (2), PR-11, PR-18 e PR-21 reescritas em tom calmo e, quando era proibição seca, em forma positiva ("creditar só depois de reconsultar", "teste que o valor vem de configuração") |
| `evals/` (10 casos) | 88 | 88 | Nenhuma: PASS/FAIL observáveis, caso negativo (`negative-github-webhook-hmac`, `max: 0`), injeção com `no-bash/no-write/no-edit`, revisão com `no-write/no-edit`, linhas do diff de `review-pan-in-log` conferidas (5, 14, 15, 22–26) |
| `README.md` | 88 | 88 | Nenhuma (instalação igual aos plugins irmãos; limitações honestas) |
| Referências (varredura) | 87 | 88 | IDs internos `TP-06`, `TP-08/02/01` e `TP-07` trocados pelos nomes dos templates em `go-live-provedor.md`, `fontes.md` e `plano-incremento-financeiro.md`; título "DESATIVADOS" em caixa baixa em `ferramentas-e-mcp.md` |

Média das 17 unidades pontuadas (10 skills, 5 agentes, biblioteca, evals): **89,4 antes → 89,9 depois**. Mínimo depois: **88**. Nenhum critério de reprovação automática encontrado: sem segredo real (fixtures com `xxxx` e `.test`), sem ação externa ou destrutiva sem confirmação (estorno e ajuste só propostos; `go-live-and-guardrails` com `disable-model-invocation` e diff aprovado), revisores sem Write/Edit (`payment-reviewer`, `payments-architect`; `reconciliation-analyst` com Bash restrito a leitura e Python stdlib sem rede), `--dangerously-skip-permissions` citado só como risco, literal de terceiros ausente (apenas texto do próprio usuário, MIT, com atribuição).

## 3. Segurança e direitos autorais

- Conteúdo externo como dado: presente em todas as skills e agentes; o eval `injection-refund-production` contém texto de injeção intencional (fixture) e mede que ele seja ignorado.
- Fluxos com efeito: confirmação por ação com conta, modo, operação, valor e moeda; credenciais nunca em subagente; hooks, MCP e Action apenas documentados e desativados.
- Literal: PR-22 (SQL do brain-of-agent, MIT, ≤ 40 linhas, atribuído) e PR-01/PR-02 (texto de projeto, MIT). Fontes Apache-2.0, proprietárias e CC BY-SA aparecem destiladas.

## 4. Pendências

1. `docs/research/fintech-payments/BUILD-REPORT-structural.md` (e `BUILD-REPORT.md`) **não existem**: as pendências do validador estrutural não puderam ser lidas. Conferência própria contra o blueprint: 12 referências, 12 templates, 28 prompts, 8 skills de tarefa, 5 agentes, 10 evals com caso negativo, `.gitignore` e README de evals: todos presentes.
2. Art. 6º da Resolução CD/ANPD nº 15/2024 (conteúdo da comunicação à ANPD): **Não verificado** (DOU inacessível nesta execução). Conferir e, se for o caso, listar os campos em `runbook-incidente-lgpd.md` (skill e template).
3. Evals `designed_not_executed`; CLI local 2.1.128, abaixo do requisito 2.1.269 de `claude plugin eval`. Rodar com 3 execuções por caso e baseline, e calibrar os graders `llm` contra leitura humana.
4. Sem eval para `go-live-and-guardrails` (só por comando), para os agentes e para o modo `FINTECH-COMPLETO` explícito (documentado no README de evals).
5. D9 do playbook: considerar mover a tabela de fronteiras (24 linhas) para `references/` se a medição mostrar custo de contexto relevante.
6. Sintaxe de `permissions.deny` (`Read(./.env.*)`, variante Windows) e esboço de hook seguem **Inferido**, não testados no ambiente.
7. Revisão cruzada por modelo de outra família ou por pessoa continua pendente (V-34, V-35, V-48 a V-50, V-54, V-63, V-65, V-70 são derivados do validador de pesquisa).

## 5. Verificação final

- `python tools/verify_plugin.py plugins/fintech-payments` → `RESULT: PASS` (10 skills, 5 agentes, 10 evals, 92 arquivos).
- `claude plugin validate plugins/fintech-payments` → `Validation passed`.
