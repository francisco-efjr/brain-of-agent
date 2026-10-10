# BUILD-REPORT-quality: mobile-apps

Data: 2026-10-10 · Validador: Claude Opus 5.5, em contexto de validação de prompt, com a rubrica `docs/foundation/prompt-quality-rubric.md` (D1–D12, 0–100).
Independência: os construtores eram outro modelo, mas da mesma família (Anthropic). A revisão é só parcialmente independente, e as notas são julgamento por leitura, não medição (AP-16). Nenhum eval foi executado.

## Escopo lido

- 11 `SKILL.md`, 5 agentes, `README.md`, `plugin.json`, `evals/README.md` e os 10 casos de eval (prompt e graders).
- Biblioteca `prompt-library.md`: a ficha, as convenções, o índice de fontes e 22 dos 33 prompts lidos por inteiro: P-01 a P-05, P-08, P-13 a P-18, P-22 a P-24 e P-27 a P-33.
- Referências lidas em parte ou conferidas por Grep: `ios-swift.md`, `checklist-completo.md`, `fontes.md`, `ferramentas-e-mcp.md`, `review-11-passos.md`, além de buscas por placeholders, CAPS, `--dangerously-skip-permissions` e referências externas.
- Fontes de apoio: `BUILD-REPORT-structural.md` (pendências), `SYNTHESIS.md` e `VALIDATED.md` (consultados por Grep: V-04, V-11, V-18, V-20, V-29, V-33 a V-36, V-40, V-49, V-58, V-62, V-63, V-65, V-79 e V-80).

## Fidelidade técnica conferida em fonte (2026-10-10)

| Afirmação | Fonte aberta | Resultado |
| --- | --- | --- |
| `allowed-tools: Read, Grep, Glob` em 8 skills descritas como "somente leitura" | https://code.claude.com/docs/en/skills | **Impreciso.** O campo só pré-aprova as ferramentas no turno da invocação e não restringe nada. Quem retira ferramentas é `disallowed-tools`, que também vale só até a próxima mensagem. Adicionado `disallowed-tools: Write, Edit, NotebookEdit` às 7 skills de auditoria e planejamento. A semântica foi documentada no playbook, no README e em `mobile-release-pipeline`. |
| Regra de permissão para bloquear `.pbxproj` (alternativa ao hook) | https://code.claude.com/docs/en/permissions | Confirmado: regras `Edit(...)` valem para todas as ferramentas nativas de edição, usam padrão gitignore e normalizam caminhos do Windows para POSIX. O exemplo `deny` foi acrescentado a `ferramentas-e-mcp.md`. |
| As 12 regras de acessibilidade do SwiftUI Pro (só 7 constavam; pendência 4 do estrutural) | https://raw.githubusercontent.com/twostraws/SwiftUI-Agent-Skill/main/swiftui-pro/references/accessibility.md (MIT, Paul Hudson) | Lista completa lida e resumida com redação própria em `ios-swift.md`. Faltavam: estilos do Dynamic Type no lugar de tamanho fixo, `@ScaledMetric` e `.scaled(by:)` (iOS 26, a conferir no SDK), título em menus e o trait de botão em gesto inevitável. Também atualizados ACE-10 e `review-11-passos.md`, e a leitura foi registrada em `fontes.md`. |
| Strong skipping padrão no Kotlin 2.0.20+ (P-08, skill de performance, eval Compose) | VALIDATED V-11 (`stability.md`) | Consistente. |
| Contraste e alvo: iOS 4,5:1 até 17 pt e 3:1 a partir de 18 pt ou negrito, 44/28 pt; Android 4,5:1 abaixo de 18 sp (negrito abaixo de 14 sp), 48 dp | V-18, V-79 | Consistente. |
| Orçamento Flutter de 16 ms (8 ms de build e 8 ms de render) | V-29 | Consistente. |
| Purpose string com menos de 4.000 bytes e ITMS-90683, inclusive por SDK | V-58 | Consistente. |
| Doze: no máximo um alarme `AllowWhileIdle` a cada 9 min; vitals com 2 h em 24 h, 5% e P90/P99 acima de 60 min | V-62, V-63 | Consistente; as consequências de loja continuam como possibilidade. |
| Expo SDK 56: `expo-router/react-navigation`, `headerLargeTitleEnabled`; Claude Code 2.1.277 para `AGENTS.md` | V-33, V-36 | Consistente. |
| Passos e flags da migração para Swift 6 | V-80 | Consistente. |
| AGP 8.x exige JDK 17 (eval `modo-completo-em-log`) | Conhecimento estável do domínio | Consistente com a mensagem de log do próprio caso. |

## Notas por artefato

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 87 | 89 | Gotcha sobre `allowed-tools` (pré-aprovação) e `disallowed-tools` (vale até a próxima mensagem), com URL e data. |
| `skills/mobile-store-release-check/SKILL.md` | 85 | 89 | `disallowed-tools` adicionado. O passo 5 mandava "gerar rascunho em arquivo", o que contradizia "não altera o projeto": agora o rascunho vai na resposta. |
| `skills/mobile-release-pipeline/SKILL.md` | 88 | 89 | Limite reescrito: `allowed-tools` não restringe nada, e a ausência de `Bash` nele faz cada comando passar pelo prompt de permissão. |
| `skills/mobile-architecture-review/SKILL.md` | 85 | 88 | `disallowed-tools` adicionado. Plano, desenho e ADR vão inteiros na resposta, com o caminho sugerido. Os códigos `Cn` e `lacuna n` ganharam legenda em `fontes.md`. |
| `skills/swift-ios-review/SKILL.md` | 85 | 88 | `disallowed-tools` adicionado. A referência pendente `performance-plus` (que não existe no plugin) passou a apontar para `mobile-performance-diagnosis`. A lista completa das 12 regras de acessibilidade está nas referências. |
| `skills/mobile-performance-diagnosis/SKILL.md` | 83 | 87 | D8: o passo 4 ("mudar um eixo") não dizia quem autoriza. Agora aplica só se o usuário pediu a correção; senão entrega o diff e o roteiro de medição. README ajustado de "somente leitura" para "altera código só a pedido". |
| `skills/mobile-accessibility-review/SKILL.md` | 87 | 89 | `disallowed-tools` adicionado. |
| `skills/mobile-platform-features-check/SKILL.md` | 87 | 89 | `disallowed-tools` adicionado. |
| `skills/mobile-test-strategy/SKILL.md` | 86 | 88 | `disallowed-tools` adicionado (a skill planeja; quem escreve testes é o agente). |
| `skills/mobile-build-troubleshoot/SKILL.md` | 86 | 86 | Sem mudança: log tratado como dado, mesmo comando reexecutado, escalada após 3 tentativas, limpeza só com confirmação. |
| `skills/prompts/SKILL.md` | 87 | 88 | `disallowed-tools` adicionado. |
| `skills/prompts/references/prompt-library.md` (22 prompts lidos) | 87 | 88 | Nenhum prompt reescrito: todos têm papel, dados em tags, formato de saída, rótulos e gate. P-04 aponta para as 12 regras, agora completas em `ios-swift.md`. P-03 usa o bloco literal de V-49, que é texto original do validador; não há problema de licença. |
| `agents/mobile-architect.md` | 89 | 89 | Sem mudança: somente leitura com `tools: Read, Grep, Glob`, modo sem interação, fatias verticais e formato fixo. |
| `agents/mobile-pr-reviewer.md` | 90 | 90 | Sem mudança: sem Bash por motivo explícito, limiar de confiança e checklist por plataforma. |
| `agents/mobile-release-auditor.md` | 88 | 88 | Sem mudança. |
| `agents/mobile-security-auditor.md` | 89 | 89 | Sem mudança: segredo mascarado, sem IDs MASVS não lidos. |
| `agents/mobile-test-engineer.md` | 88 | 88 | Sem mudança: escrita só em pastas de teste, Bash só com comando autorizado, sem deploy, para após 3 falhas. |
| `evals/` (10 casos + README) | 84 | 88 | `no-exec` e `no-publish` casavam a entrada inteira do Bash: `eas` casava "release" na descrição (falso FAIL). Agora casam só o campo `command`, com `\b`. `no-full-reading` não casava caminho do Windows serializado em JSON (`references\\fontes.md`), o que daria falso PASS; corrigido com `[\\/]+`. Regex testado com entradas sintéticas. Novo caso 11 `ios-sem-mac-windows` (reserva do SYNTHESIS; pendência 2), com `criteria`, `skill-fired` e `no-exec`. README atualizado: 11 casos e 33 execuções, a ressalva de que os graders supõem entrada serializada em JSON e os próximos candidatos. |
| `README.md` | 86 | 87 | Semântica de `allowed-tools`/`disallowed-tools` explicada. A linha de `mobile-performance-diagnosis` foi corrigida. |
| Referências tocadas (`ios-swift.md`, `checklist-completo.md`, `review-11-passos.md`, `fontes.md`, `ferramentas-e-mcp.md`) | — | — | Lista das 12 regras completa, alternativa `permissions.deny` para `.pbxproj`, legenda dos códigos `Cn` e `lacuna n`, e registro da fonte aberta. |

Média antes: 86,7 · média depois: 88,3 · mínimo depois: 86 (`mobile-build-troubleshoot`). Nenhum artefato abaixo de 80 e nenhum critério de reprovação automática encontrado.

## Segurança e direitos autorais

- Nenhum segredo no plugin. Os exemplos mascaram valores e mandam rotacionar.
- Ações externas (`eas update` em produção, `eas submit`, `--auto-submit`, `fastlane pilot`, `match nuke`, promoção de trilha, "Submit for Review") exigem ficha confirmada no chat. `mobile-release-pipeline` tem `disable-model-invocation: true`.
- Revisores e auditores (4 agentes) não têm Write, Edit nem Bash. O único agente com escrita é `mobile-test-engineer`, restrito a pastas de teste.
- `--dangerously-skip-permissions` aparece só como risco, com allowlist como alternativa e sandbox descartável como única exceção.
- Nenhum hook, `.mcp.json`, `.lsp.json` ou `bin/` ativo. O hook e a regra `deny` estão só documentados.
- Literal de terceiros: o único bloco literal (P-03) é texto próprio do validador (V-49). As 12 regras do SwiftUI Pro foram resumidas com redação própria e atribuição (MIT). O resto é destilado com fonte.
- Os 11 evals têm PASS/FAIL observáveis. Os casos negativos são `negativo-sql-ranking` (distante) e `flutter-camadas-negativo-proximo` (próximo, com `max: 0` para a skill de Swift). Três casos têm graders de não execução.

## Pendências do validador estrutural: decisões

1. **Seis arquivos `prompts-*.md` previstos na seção 4.2.** Decisão: **não criar**. `prompt-library.md` tem sumário e IDs `P-nn` estáveis citados por outras skills. A skill `prompts` manda ler por `Grep ^## P-NN`, o que já dá carga sob demanda. Dividir o arquivo duplicaria conteúdo ou quebraria referências. O blueprint permite arquivo único ("+ arquivos por subtema se grande"). Fica a recomendação de atualizar a seção 4.2 do `SYNTHESIS.md` (não editado aqui, por ser documento de pesquisa).
2. **Eval reserva `ios-sem-mac-windows`.** Criado.
3. **Graders curtos.** Revisados: os `tool_used` são determinísticos e úteis, e três tinham regex com falso positivo ou falso negativo, já corrigidos.
4. **`accessibility.md` e `stability.md` externos.** `accessibility.md` foi aberto e incorporado como resumo com atribuição. `stability.md` já estava resumido via V-11 e é citado só como origem, sem precisar ser aberto.

## Pendências abertas

- Executar `claude plugin eval .` (Claude Code 2.1.269 ou superior; a instalação local registrada é 2.1.128) com 3 execuções por caso. Na primeira rodada, confirmar que os graders `tool_used` comparam o regex com a entrada serializada em JSON, porque, se não for assim, os graders de não execução passam sem medir.
- `disallowed-tools` vale só até a próxima mensagem do usuário. Em auditorias de várias mensagens, "somente leitura" volta a ser regra de conduta. Para garantia, use regras `deny` no projeto (decisão do usuário).
- Atualizar a seção 4.2 do `SYNTHESIS.md` para refletir o arquivo único de prompts.
- Casos de eval para `mobile-test-strategy` e `mobile-pr-reviewer`, e para `MOBILE-COMPLETO` pedido pelo próprio usuário, seguem ausentes.
- Lacunas de fonte herdadas, sem mudança: acessibilidade em RN e Flutter, payload de push, MASVS (níveis e IDs), navegação, conflito no CloudKit e energia no iOS.

## Verificação final

| Verificação | Resultado |
| --- | --- |
| `python tools/verify_plugin.py plugins/mobile-apps` | PASS (11 skills, 5 agentes, 11 evals, 107 arquivos) (Verificado) |
| `claude.exe plugin validate plugins/mobile-apps` | Validation passed (Verificado) |
| Tamanho do `playbook/SKILL.md` | 208 linhas (abaixo de 300) (Verificado) |
| Execução dos evals | Não executado (`designed_not_executed`) |
