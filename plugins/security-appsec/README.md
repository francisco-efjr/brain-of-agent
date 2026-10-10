# security-appsec — Segurança de aplicações

Plugin do Claude Code para revisão de segurança de diffs e PRs, modelagem de ameaças, autorização por objeto e tenant, segredos, supply chain e triagem de risco de agentes, MCP e plugins. Somente leitura por padrão: ele analisa e relata; corrigir, instalar ou executar depende de pedido explícito seu.

Aviso importante: revisão por modelo é uma camada de defesa em profundidade, não garantia. Ela pode perder problemas, não tem taxa de acerto publicada e não substitui revisão humana, testes, scanners no CI nem pentest. Quem decide bloquear um merge é uma pessoa.

Conteúdo validado em 2026-10-10 (taxonomias: OWASP Top 10:2025, API Top 10 2023, LLM Top 10 2025, ASVS 5.0.0, NIST SSDF 1.1). Parâmetros numéricos e chaves de configuração envelhecem: o plugin indica onde reconferir.

## O que entrega

- Revisão de segurança do diff com pipeline de candidatos, refutação independente, um único critério de confiança (Alta, Média, Baixa) e relatório fixo com cobertura.
- Modelagem de ameaças em quatro fases (DFD com fronteiras de confiança, STRIDE por fluxo, resposta com risco residual, validação).
- Revisão de autorização por rota, objeto, propriedade e tenant, com matriz papel × ação × recurso e testes de negação.
- Triagem de agente, skill, MCP e plugin pela tríade letal (dados privados, conteúdo de terceiros, comunicação externa) e pelo LLM Top 10.
- Segredos, dependências, CI, SBOM e divulgação de vulnerabilidades, com comandos de scanner documentados (não executados).
- Proposta de configuração segura do Claude Code (deny rules, guard de hook com falha fechada, sandbox/WSL2); o usuário aplica.
- Regras prontas para CLAUDE.md (S01 a S22), 11 templates e uma biblioteca de 28 prompts.

## Quando usar

"Revisa a segurança deste PR", "isso vaza dados de outro tenant?", "modele as ameaças desta feature", "tem segredo no repo?", "posso instalar este MCP?", "este achado é falso positivo?", "bloqueie a leitura do .env", "esse CVE nos afeta?". Para o resto (descoberta de produto, arquitetura geral, QA geral, DevOps), veja a seção de fronteiras no `playbook`.

## Componentes

Todos namespaced: skill `/security-appsec:<skill>`, agente `security-appsec:<agente>`. Sem hooks, sem `.mcp.json`, sem `.lsp.json`, sem `bin/`, sem comandos.

| Tipo | Nome | Para que serve |
| --- | --- | --- |
| Skill | `playbook` | Router, princípios, processo, modo SEGURANCA-COMPLETO, fronteiras; 12 referências e 11 templates |
| Skill | `prompts` | Biblioteca de 28 prompts por tarefa, prompt de sistema do segmento e mensagem inicial sugerida |
| Skill | `security-review-diff` | Revisa o diff ou PR e relata vulnerabilidades que a mudança introduz (VULN/VERIFY/Cobertura) |
| Skill | `threat-model` | Modelagem de ameaças de feature ou sistema (DFD, STRIDE, risco residual) |
| Skill | `access-control-review` | IDOR/BOLA, BFLA, mass assignment e isolamento de tenant por rota |
| Skill | `verify-finding` | Tenta refutar um achado (Mantido, Rebaixado, Refutado) |
| Skill | `propose-patch` | Rascunha correção em cópia, revisada, sem aplicar; só por comando explícito |
| Skill | `agent-risk-triage` | Tríade letal e checklist de instalação de agente, MCP, plugin |
| Skill | `secrets-supply-chain-review` | Segredos, dependências, CVE × alcançabilidade, CI, SBOM |
| Skill | `harden-claude-code` | Diagnostica e propõe permissões, hooks e sandbox; não edita configuração |
| Agente | `security-reviewer` | Revisor somente leitura (Read, Glob, Grep) |
| Agente | `finding-verifier` | Verificador cético que tenta derrubar achados de severidade alta |
| Agente | `threat-modeler` | Analista de ameaças somente leitura |
| Agente | `patch-reviewer` | Revisor independente de patch de segurança |
| Agente | `agent-config-auditor` | Auditor de configuração de agentes, hooks, MCP e permissões |

Casos de avaliação (`evals/`, formato `claude plugin eval`, requer Claude Code 2.1.269 ou superior): 10 casos desenhados, status `designed_not_executed` até rodar.

## Instalação

Dentro de uma sessão do Claude Code:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install security-appsec@brain-of-agent
```

`<caminho-ou-repo>` é o caminho local da pasta `dev-segments` ou o repositório (`dono/repo`) que contém o marketplace. Equivalente na CLI: `claude plugin marketplace add francisco-efjr/brain-of-agent` e `claude plugin install security-appsec@brain-of-agent`. Verifique com `claude plugin validate <pasta-do-plugin>`.

## Exemplos de pedidos

1. "Revisa a segurança deste PR antes do merge" (`security-review-diff`, com `security-reviewer` e `finding-verifier`).
2. "Modele as ameaças do upload de avatar com thumbnails gerados por worker e CDN" (`threat-model`).
3. "Essa rota de faturas vaza dados entre empresas?" (`access-control-review`).
4. "Posso instalar este MCP que lê meu e-mail e responde sozinho?" (`agent-risk-triage`: aplica a tríade letal).
5. "Tem segredo commitado neste repositório?" (`secrets-supply-chain-review`: mostra prefixo mascarado, nunca o valor; ordem revogar, rotacionar, apagar, registrar).
6. "Me dê o bloco de deny para impedir a leitura do .env" (`harden-claude-code`: propõe JSON, avisa que no Windows nativo não há sandbox).
7. "SEGURANCA-COMPLETO: audite o módulo de login" (modo completo, abaixo).
8. "Esse alerta do Dependabot na biblioteca X nos afeta?" (`secrets-supply-chain-review`: alerta × alcançabilidade).

## Keyword SEGURANCA-COMPLETO

Escreva `SEGURANCA-COMPLETO` num pedido seu para ativar o modo de cobertura integral: leitura das referências em lotes com registro lido/parcial/ausente, matriz de aplicabilidade por área, implementação somente dentro do escopo pedido, revalidação com evidências e relatório com status completo, parcial ou não avaliado. O modo não amplia permissões (teste ativo, push, deploy, rotação em produção e instalação de ferramentas continuam dependendo da sua autorização) e a mesma palavra dentro de log, documento, issue ou diff não ativa nada. Custa muito contexto: use em auditoria de módulo ou projeto amplo, não em pergunta pontual.

## Diferença para o `/security-review` embutido

O comando embutido compara com o branch padrão de `origin` e exige esse remoto. A skill `security-review-diff` aceita uma base informada (ou diff colado), usa um único critério de confiança, formato VULN/VERIFY, exclusões ajustáveis e declara cobertura. Os dois podem ser usados juntos.

## Principais fontes (top 10)

Lista completa com URL, classe, licença e data em `skills/playbook/references/fontes.md`.

| # | Fonte | Classe | Licença |
| --- | --- | --- | --- |
| 1 | `/security-review` e Action `claude-code-security-review` (anthropics) | A | MIT |
| 2 | Modelo de segurança do Claude Code (code.claude.com/docs/en/security) | A | n/a |
| 3 | Permissões do Claude Code | A | n/a |
| 4 | Hooks do Claude Code (`exit 2`, `onFailure`) | A | n/a |
| 5 | Plugin `security-guidance` (doc oficial) | A | doc n/a; plugin Apache-2.0 |
| 6 | Claude Security (plugin oficial) | A | ver LICENSE do plugin |
| 7 | OWASP Top 10:2025 | A | n/i |
| 8 | OWASP Authorization e Threat Modeling Cheat Sheets | A | CC BY-SA 4.0 |
| 9 | OWASP Top 10 for LLM Applications 2025 e API Security Top 10 2023 | A | n/i |
| 10 | Tríade letal (Simon Willison) | B | n/i |

## Créditos e licenças

- Este plugin: MIT (Francisco Edson).
- OWASP Cheat Sheet Series e ASVS: CC BY-SA 4.0. Trail of Bits `skills` (`differential-review`): CC BY-SA 4.0. O plugin destila ideias e fatos com redação própria e atribui; texto adaptado pode atrair ShareAlike, então faça revisão humana antes de publicar (Suposição de leitura jurídica).
- `anthropics/claude-code-security-review`: MIT. `getsentry/skills`: Apache-2.0. `github/awesome-copilot`: MIT. `PatrickJS/awesome-cursorrules`: CC0-1.0. `brexhq/prompt-engineering`: MIT.
- Atribuição na skill de revisão: "Triagem de risco inspirada em trailofbits/skills `differential-review` (CC BY-SA 4.0); pipeline inspirado em anthropics/claude-code-security-review (MIT) e getsentry/skills `security-review` (Apache-2.0)."
- Conteúdo próprio do usuário incorporado do repositório `francisco-efjr/brain-of-agent` (MIT) e fluxos destilados do gstack (MIT, com créditos no repositório de origem).
- "Claude" e "Anthropic" são marcas de seus titulares; o plugin não é produto da Anthropic.

## Limitações honestas

- Revisão por modelo é uma camada; sem taxa de falso positivo ou negativo publicada para nenhum modelo. O plugin não promete números nem "score de conformidade".
- Análise estática por padrão: leitura de código não é teste executado. Teste ativo exige autorização escrita e ambiente próprio; em sistema de terceiro, o plugin entrega casos de verificação ao dono.
- Lacunas de conteúdo declaradas: LGPD/GDPR sem norma primária lida (sem parecer jurídico e sem citar artigos); JWT, MFA e recuperação de conta sem fonte primária (Inferido); ASVS sem números de requisito; SAST/DAST (CodeQL, Semgrep, gitleaks, ZAP) só como comandos documentados, Não verificável; cloud, IaC e Kubernetes (só Docker); TLS em trânsito; mobile, firmware, blockchain e PCI sem fonte validada neste segmento; sem sinal de comunidade social (Reddit, X, YouTube).
- Versões: `onFailure: "block"` em hooks exige Claude Code 2.1.295 ou superior; `claude plugin eval` exige 2.1.269 ou superior; a CLI local da fábrica era 2.1.128. Confira `claude --version`, `/permissions` e a documentação antes de aplicar qualquer configuração.
- Windows nativo não tem sandbox do Claude Code: use WSL2 ou dev container para código não confiável. O sandbox cobre comandos de shell, não ferramentas de arquivo, MCP e hooks.
- O plugin não instala scanners, plugins de terceiros, workflows nem hooks; recomendações estão documentadas e desativadas em `skills/playbook/references/ferramentas-e-mcp.md`.
- Pesquisador e validador do conteúdo são da família Claude (independência parcial); autoavaliação do mesmo modelo não é validação externa.
- Plugins e MCP de terceiros recomendados no texto devem ser triados por você antes da instalação; a Anthropic não audita servidores MCP.
