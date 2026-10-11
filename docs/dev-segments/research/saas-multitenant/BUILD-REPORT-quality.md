# BUILD-REPORT de qualidade: plugin saas-multitenant

Data: 2026-10-11 · Papel: validador de qualidade de prompt e de conteúdo técnico · Plugin: `plugins/saas-multitenant` (0.1.0)
Validador: Claude Opus 5.5. Os construtores eram outro modelo, mas da mesma família Claude: a revisão é adversarial, com **independência parcial**, e não equivale a validação externa nem a eval executado.
Base: `docs/foundation/prompt-quality-rubric.md` (D1 a D12, nota = média × 20), `prompt-principles.md`, `plugin-blueprint.md`, `house-style.md`; fonte de verdade `VALIDATED.md` (V-01 a V-66); pendências de `BUILD-REPORT-structural.md`.

## 1. Método

1. Leitura integral dos 10 `SKILL.md`, dos 5 agentes, do README, do `evals/README.md` e dos 13 casos (prompt e graders). Biblioteca de prompts: os 33 prompts foram conferidos por script quanto às quatro regras comuns, e 18 foram lidos por inteiro (PR-01 a PR-08, PR-10, PR-14 a PR-17, PR-24 a PR-30, PR-32). Referências e templates: leitura por amostra (`checklist-pr-tenant`, `dicionario-metricas-saas`, `rls-postgres` nas passagens de `NULLIF`) e Grep dirigido.
2. Fidelidade técnica: afirmações de versão e de número conferidas por Grep no `VALIDATED.md` (incomplete 23 h; webhook com tolerância de 5 min, retentativas de 3 dias, reenvio de 15 e 30 dias, TLS 1.2/1.3; chave de idempotência de 255 caracteres e descarte após 24 h; trial offers com `2026-09-30.endive` e `flexible`; resumo de entitlements com até 10 itens; Customer com moeda única; CGSN 191/2026; Res. BCB 402/2024; Asaas 15 falhas e 14 dias). Todas batem com V-02, V-03, V-04, V-05, V-38, V-39, V-50, V-60 e V-62.
3. WebFetch em documentação oficial (2026-10-11):
   - https://code.claude.com/docs/en/skills : `allowed-tools` pré-aprova e não restringe; `disallowed-tools` existe, remove ferramentas enquanto a skill está ativa e a restrição cai na próxima mensagem. Confirma o texto de `tenant-isolation-review` e das demais skills. **Verificado.**
   - https://code.claude.com/docs/en/sub-agents : campos `tools`, `disallowedTools`, `maxTurns`, `model: inherit`; plugins ignoram `hooks`, `mcpServers` e `permissionMode`; a ferramenta de subagente se chama `Agent` (renomeada de `Task` na 2.1.63). Usado no novo comando. **Verificado.**
4. Conhecimento estável usado sem fonte nova (rotulado no texto): `current_setting(nome, true)` pode devolver string vazia depois de um `set_config` local anterior na mesma conexão, o que exige `NULLIF` antes do cast (a referência `rls-postgres.md` já trazia isso como Inferido; dois prompts não traziam).
5. Segurança e direitos autorais: nenhum segredo real (só nomes de variável e prefixos `sk_`/`whsec_` como padrão de busca); revisores (`tenant-isolation-reviewer`, `billing-reviewer`) só com `Read, Grep, Glob`; `milestone-reviewer` sem Write/Edit (Bash limitado por instrução, declarado como não técnico); nenhum fluxo autoriza produção, conta live, envio externo ou eliminação sem confirmação; `--dangerously-skip-permissions` só aparece como risco. Literal de terceiros: só a matriz do brain-of-agent (MIT, conteúdo do usuário, com atribuição); OWASP CC BY-SA e Stripe proprietária estão destilados. O fixture de injeção do eval `escopo-keyword-log-e-injecao` (domínio `.invalid`) é dado de teste, não instrução, e foi tratado assim.

## 2. Notas por arquivo (antes → depois)

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 93 | 96 | Regra explícita para execução sem interação (status `rascunho`, "Decisões pendentes do humano", sem inventar decisor); linha do comando `/saas-multitenant:tenant-audit` na tabela intenção → recurso. Ressalva mantida: a tabela de fronteiras (25 linhas) pesa no corpo sempre carregado (D9 = 4). |
| `skills/tenant-isolation-review/SKILL.md` | 93 | 95 | Regra de execução sem interação nas entradas. Afirmação sobre `disallowed-tools` conferida na doc oficial. |
| `skills/tenancy-model-adr/SKILL.md` | 91 | 94 | Regra de execução sem interação. |
| `skills/tenant-rls-migration/SKILL.md` | 93 | 95 | Regra de execução sem interação; agora coberta por eval próprio (`rls-migracao-explicita`). |
| `skills/tenant-isolation-tests/SKILL.md` | 91 | 93 | Regra de execução sem interação. |
| `skills/stripe-billing-lifecycle/SKILL.md` | 89 | 91 | Regra de execução sem interação. Ressalva: passos 3 e 12 muito densos (D9 = 4); conteúdo técnico conferido contra V-03, V-38, V-50. |
| `skills/saas-feature-spec/SKILL.md` | 92 | 94 | Regra de execução sem interação. |
| `skills/enterprise-sso-scim/SKILL.md` | 89 | 92 | Regra de execução sem interação (antes só pedia "uma pergunta por vez"). |
| `skills/tenant-data-lifecycle/SKILL.md` | 86 | 93 | `description` sem "quando usar" ganhou a frase de uso; gatilho solto "vazamento entre tenants" (colidia com `tenant-isolation-review`) virou "incidente de vazamento entre tenants (comunicação e prazos)"; regra de execução sem interação. |
| `skills/prompts/SKILL.md` | 89 | 92 | Texto da convenção corrigido (antes afirmava uma "linha final de regras" que 31 dos 33 prompts não tinham completa); contagem de evals 13 → 14. |
| Biblioteca de prompts (`prompt-library*.md`, 33 prompts) | 83 | 91 | Linha `Regras comuns: ...` acrescentada aos 31 prompts que não cobriam as quatro regras (dado não é instrução, rótulos, sem execução inventada, sem credencial ou dado real); convenção reescrita para ser verdadeira. PR-07 e PR-32: corrigida a afirmação de que `current_setting(nome, true)` "devolve NULL", que omitia a string vazia após `set_config` local anterior na mesma conexão e o `NULLIF` necessário (defeito justamente no cenário de pool). |
| `agents/tenant-isolation-reviewer.md` | 94 | 95 | `description` volta a citar o comando `/saas-multitenant:tenant-audit`. |
| `agents/billing-reviewer.md` | 93 | 93 | Sem alteração; checklist BL-01 a BL-20 conferido contra V-02 a V-06, V-37 a V-39, V-50, V-51, V-62. |
| `agents/saas-architect.md` | 92 | 92 | Sem alteração. |
| `agents/isolation-test-engineer.md` | 86 | 93 | Passo 1 rodava a suíte existente antes de confirmar o alvo do banco: agora lê a configuração de teste e só executa se o banco for local ou descartável; senão, "Não executado" com o motivo (D8). |
| `agents/milestone-reviewer.md` | 87 | 93 | Mesmo defeito no passo 5 (rodar testes sem confirmar o alvo): mesma correção; frase truncada corrigida. |
| `commands/tenant-audit.md` (novo) | ausente | 90 | Criado como atalho fino previsto no SYNTHESIS 4.1 e pendente no relatório estrutural: escopo obrigatório, delegação à ferramenta `Agent` com as regras críticas repetidas, alternativa sem o agente, somente leitura, sem Bash, declaração de independência parcial. |
| `README.md` | 87 | 91 | Contagens explícitas (8 skills de tarefa, 5 agentes, 1 comando, 33 prompts, 14 evals) no lugar da frase evasiva; linha do comando na tabela de componentes; evals 13 → 14. |
| Evals (`evals/`, README e 14 casos) | 88 | 91 | Novo caso `rls-migracao-explicita` (skill com `disable-model-invocation`, invocada por comando; pedido de produção que deve ser recusado; grader `tool_used` de escrita em `migrations/` e critério LLM com PASS/FAIL observáveis). README atualizado (contagem, custo, limite: não verificado se o runner expande comando de barra; por isso sem `skill-fired`). Caso negativo `negativo-texto-botao` e caso de injeção já existiam e foram conferidos. |

Médias (18 artefatos pontuados antes, 19 depois, com o comando novo): antes 89,8; depois 92,8. Mínimo depois: 90 (`commands/tenant-audit.md`). Nenhum artefato abaixo de 80; nenhum critério de reprovação automática encontrado.

## 3. Achados que não exigiram mudança (conferidos)

- `disallowed-tools` em skill: campo real, com a ressalva correta de que a restrição cai na próxima mensagem (doc oficial).
- OIDC: `iat` não é MUST e `azp` é condicional (Core § 3.1.3.7, V-46); SCIM `active=false`, `userName` sem caixa, `POST /.search` (RFC 7643/7644, V-36, V-55).
- LGPD art. 18, II (acesso) e V (portabilidade); prazo ANPD de três dias úteis contado de saber que dado pessoal foi afetado, com risco ou dano relevante (V-61); GDPR art. 33 72 h. Avisos de "não é orientação jurídica" presentes.
- PgBouncer: `SET`/`RESET` "Never" em modo transaction e `SET LOCAL` não listado (V-47); todos os artefatos rotulam a compatibilidade como Não verificável sem pool de tamanho 1.

## 4. Pendências

1. **Evals não executados.** Os 14 casos seguem `designed_not_executed`; a CLI local (2.1.128) não tem `claude plugin eval` (exige 2.1.269 ou superior). Notas acima são leitura, não medição.
2. **Runner e comando de barra.** Não verificado se o `claude plugin eval` expande `/saas-multitenant:tenant-rls-migration` no `prompt.md`; confirmar na primeira rodada e, se não expandir, reescrever o caso.
3. **Comando `tenant-audit` não exercitado.** O nome `Agent` e o tipo `saas-multitenant:tenant-isolation-reviewer` vêm da doc; falta uma sessão manual que confirme a delegação.
4. **Fronteiras no corpo do playbook.** A tabela de 25 plugins custa contexto em toda ativação; mover para `references/` exige decisão do dono da fábrica (o blueprint pede fronteiras, sem dizer onde).
5. **Desenho de papéis/RBAC do tenant** continua sem fluxo ou prompt dedicado (pendência do crítico no SYNTHESIS).
6. **Caso `lote-sem-interacao-mobile`** fora da tabela 4.11 do SYNTHESIS (apontado pelo validador estrutural): atualizar a tabela ou registrar a origem; o caso é útil e foi mantido.
7. **Prompts de autoria própria** (PR-07, PR-09, PR-31, PR-32, PR-33): teto 90 até eval.
8. Lacunas de fonte herdadas, sem mudança: OIDC discovery e JWKS, texto integral das Resoluções da ANPD, evento de cancelamento do Asaas, JIT em Okta e Entra, métrica de ativação.

## 5. Verificação final

| Verificação | Resultado |
| --- | --- |
| `python tools/verify_plugin.py plugins/saas-multitenant` | PASS (10 skills, 5 agentes, 1 comando, 14 evals, 108 arquivos) |
| `claude plugin validate plugins/saas-multitenant` | Validation passed |
