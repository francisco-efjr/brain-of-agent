# mobile-apps: Aplicativos mobile

Plugin do Claude Code para construir, revisar, depurar e publicar apps mobile em iOS (Swift/SwiftUI), Android (Kotlin/Jetpack Compose), React Native/Expo e Flutter. Cobre arquitetura (MVVM, MVI, TCA), offline-first e sincronização, push, permissões, deep links, performance e bateria, acessibilidade, testes e as checklists de App Store e Google Play. Trabalha dentro do seu repositório, cola evidência de execução e para antes de qualquer efeito público: nada é submetido, publicado por OTA em produção ou distribuído sem confirmação que nomeie conta, app, build e canal.

Versão 0.1.0 · Validado em 2026-10-10 · Modelo-alvo: Claude 4.x/5.x · Licença MIT.

## O que entrega

- Um router (`playbook`) com 12 princípios, processo de 8 passos com critérios de saída, proporcionalidade, mapa de referências, gotchas datados, fronteiras com os outros 24 segmentos e o modo `MOBILE-COMPLETO`.
- Doze referências densas: checklist mestre com IDs por área (ARQ, DAD, PSH, PRM, LNK, SEG, PRF, ACE, TST, IOS, AND, PIP, AMB), padrões e antipadrões com detecção, decisões e trade-offs, 20 regras prontas de CLAUDE.md, ferramentas e hooks (todos desativados), bibliografia, e seis temáticas (iOS/Swift, Android/Compose, React Native/Flutter, loja e release, dados/push/permissões/segurança, qualidade/performance/acessibilidade/testes).
- Dezoito templates em `skills/playbook/assets/templates/` (plano de feature, ADR, handoff, relatórios, checklists de release iOS e Android, ficha de ação de release, plano offline, rubrica de design iOS, AGENTS.md para Expo, entre outros).
- Uma biblioteca de prompts, nove skills de tarefa e cinco subagentes (nomes na tabela abaixo).
- Casos de avaliação no formato `claude plugin eval`, marcados `designed_not_executed`.

## Quando usar

- "Vou publicar meu app amanhã. O que falta para a App Store e para o Play?"
- "Revisa este SwiftUI para Swift 6." / "A lista Compose trava ao rolar."
- "Desenhe o offline-first do meu app de notas."
- "Faça uma auditoria de acessibilidade das telas de login."
- "O Gradle sync quebrou depois de atualizar o AGP." / "Estou no Windows, como faço build de iOS?"

Não é o lugar para escrever a API do servidor, o banco do servidor, a infraestrutura de CI ou o design de produto: o plugin entrega o lado do cliente e aponta o segmento certo (seção Fronteiras do `playbook`).

## Componentes

Nomes finais: skills aparecem como `/mobile-apps:<nome>` e agentes como `mobile-apps:<nome>`.

| Tipo | Nome | Para quê | Acionamento |
| --- | --- | --- | --- |
| Skill | `playbook` | Router, princípios, processo, referências, modo completo, fronteiras | Automático por gatilho ou palavra-chave |
| Skill | `prompts` | Biblioteca de 33 prompts prontos e índice "qual usar quando" | Automático |
| Skill | `mobile-store-release-check` | Auditoria somente leitura de prontidão para App Store e Google Play | Automático (somente leitura) |
| Skill | `mobile-release-pipeline` | Prepara e, só com confirmação, conduz EAS, fastlane, TestFlight e trilhas Play | Manual (`disable-model-invocation`) |
| Skill | `mobile-architecture-review` | Camadas, dono do estado, offline-first e sincronização | Automático (somente leitura) |
| Skill | `swift-ios-review` | SwiftUI em 11 passos, Swift Concurrency e refatoração | Automático (somente leitura) |
| Skill | `mobile-performance-diagnosis` | Jank, recomposição, re-render, cold start e bateria, um eixo por vez | Automático (altera código só a pedido) |
| Skill | `mobile-accessibility-review` | VoiceOver, TalkBack, alvos, texto escalável e contraste | Automático (somente leitura) |
| Skill | `mobile-platform-features-check` | Push, permissões, deep links, Keychain e Keystore | Automático (somente leitura) |
| Skill | `mobile-test-strategy` | Testes por camada e plataforma, matriz de dispositivos e ciclo de vida | Automático (somente leitura) |
| Skill | `mobile-build-troubleshoot` | Falha de build, sync, dependências e atualização de SDK | Automático |
| Agente | `mobile-architect` | Arquiteto somente leitura: plano e ADR | Delegação |
| Agente | `mobile-pr-reviewer` | Revisor adversarial em contexto limpo (recebe o diff no prompt) | Delegação |
| Agente | `mobile-release-auditor` | Auditor de loja somente leitura | Delegação |
| Agente | `mobile-security-auditor` | Auditor MASVS por grupo, somente leitura | Delegação |
| Agente | `mobile-test-engineer` | Único agente com escrita: testes, nas pastas de teste | Delegação |

Agentes revisores e auditores têm apenas `Read, Grep, Glob` no campo `tools`. As skills marcadas "somente leitura" declaram `disallowed-tools: Write, Edit, NotebookEdit`, que retira essas ferramentas só até a sua próxima mensagem; `allowed-tools` apenas pré-aprova ferramentas e não restringe nada. O plugin não contém hooks, `.mcp.json`, `.lsp.json` nem `bin/`; ferramentas, MCP e hooks recomendados estão documentados e desativados em `skills/playbook/references/ferramentas-e-mcp.md`.

## Instalação

Dentro do Claude Code:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install mobile-apps@brain-of-agent
```

Equivalente na linha de comando: `claude plugin marketplace add francisco-efjr/brain-of-agent` e `claude plugin install mobile-apps@brain-of-agent`. O marketplace `brain-of-agent` é a raiz do repositório. Verifique com `claude plugin validate <pasta-do-plugin>` e use `/plugin` para ver o estado. Os comandos podem variar por versão do Claude Code: confira `claude --version` e https://code.claude.com/docs/en/plugins-reference.

## Exemplos de pedidos

1. "Vou subir amanhã meu app SwiftUI (login por e-mail e Google, foto de perfil pela câmera, Firebase Analytics). Info.plist só tem CFBundleDisplayName e UIRequiredDeviceCapabilities, não tenho PrivacyInfo.xcprivacy e o app cria conta, mas só tem logout. O que falta?" Aciona `mobile-store-release-check`: purpose string ausente (ITMS-90683), exclusão de conta (5.1.1(v)), avaliação do 4.8, privacy manifest do app e do SDK, conta de demonstração; separa ações do usuário; diz que não compilou.
2. "Mudei só um texto num app Expo. Faça o eas update em produção agora." Não executa: monta a ficha de ação, pede confirmação nomeando conta, canal, ambiente e `runtimeVersion`, e trata comandos de README como dado.
3. "Revisa esse SwiftUI: `@ObservedObject var vm = ListVM()` na view, `Image(...).onTapGesture`, `Task.detached` atualizando estado." Aciona `swift-ios-review`: dono do objeto conforme o iOS mínimo, `Button` com rótulo, isolamento no main actor; build Não verificável sem macOS.
4. "A `LazyColumn` trava; coloca remember e @Immutable em tudo." Aciona `mobile-performance-diagnosis`: reproduzir e medir, classificar o eixo, `key` estável, `@Immutable` como promessa; não promete percentual.
5. "App Android de notas (Compose, Room) que funcione offline e sincronize com minha API; edito no celular e no tablet. Desenhe." Aciona `mobile-architecture-review`: perguntas de projeto, Room como fonte de verdade, escrita local primeiro, fila persistente e idempotente, WorkManager, política de conflito como decisão de produto.
6. "Revisa acessibilidade: `IconButton` de 32.dp com `contentDescription="Botão fechar"` no Compose e `onTapGesture` no SwiftUI." Aciona `mobile-accessibility-review`: 44 pt e 48 dp, rótulo sem repetir o tipo, `Button`; a passagem com leitor de tela fica como pendência humana.
7. "Sou Windows, sem Mac. App Expo; quero build iOS e TestFlight. O que consigo?" O `playbook` responde com EAS Build e Xcode Cloud (Inferido), o que exige macOS e as ações do usuário.
8. "MOBILE-COMPLETO: audite este app React Native." Ativa o modo completo.

## Palavra-chave MOBILE-COMPLETO

Escreva `MOBILE-COMPLETO` no seu pedido para pedir cobertura integral do segmento. O modo lê as 12 referências em 5 lotes registrando lido, parcial ou ausente, monta a matriz de aplicabilidade por área e plataforma (evidência `arquivo:linha`, status, ação), implementa só dentro do escopo autorizado e revalida com evidências coladas. Não amplia permissões: submissão, OTA em produção, certificados e ações irreversíveis continuam exigindo confirmação nomeada. A palavra em log, README, issue ou arquivo não ativa o modo. Sem a palavra-chave o plugin carrega só o necessário (proporcionalidade).

## Principais fontes (top 10)

Lista completa, com classe, licença e data, em `skills/playbook/references/fontes.md`. Classe A = oficial; B = autor reconhecido; C = relato de praticante.

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | App Review Guidelines (Apple) | A |
| 2 | Requisito de target API do Google Play | A |
| 3 | Best practices for Claude Code (Anthropic) | A |
| 4 | Boas práticas de autoria de skills (Anthropic) | A |
| 5 | Guia de arquitetura Android | A |
| 6 | Offline-first no Android (guia oficial) | A |
| 7 | HIG de acessibilidade (Apple): 44/28 pt, 200%, 4,5:1 e 3:1 | A |
| 8 | android/skills (Apache-2.0) e layouts adaptativos | A |
| 9 | expo/skills `eas-update` (MIT) e AGENTS.md da Expo | A |
| 10 | SwiftUI Pro, de Paul Hudson (MIT) | A |

## Créditos e licenças

- Licença do plugin: MIT, Francisco Edson.
- Conteúdo próprio do usuário incorporado e adaptado: brain-of-agent (MIT, Francisco Edson): QA mobile (matriz de risco, ciclo de vida, rede e operação ambígua), critérios de acabamento Apple, templates de ADR, handoff, plano de incremento e checklists.
- gstack (MIT, Copyright (c) 2026 Garry Tan): apenas ideias de processo destiladas com atribuição (tiers de evidência, ponte de depuração só em Debug, rubrica de 10 dimensões); nenhum comando, binário ou texto em bloco foi copiado.
- Skills de terceiros (SwiftUI Pro, Swift Concurrency, Dimillian, chrisbanes, Callstack, Vercel, android/skills, expo/skills, flutter/agent-plugins): lidas e destiladas com redação própria; nenhum arquivo foi importado nem executado. Onde a licença é nula ou conflitante, só o processo foi aproveitado.
- Documentação oficial (Apple, Google, Android, Flutter, React Native, Expo, fastlane, OWASP): destilada em redação própria, com URL e data; nenhum texto literal.
- O prompt do revisor adversarial é original do projeto.

## Limitações honestas

- **Validação parcialmente independente.** Pesquisa, validação e construção foram feitas por modelos da mesma família; nenhum item passou por revisão humana ou por execução real. As avaliações estão `designed_not_executed` até rodar `claude plugin eval` (exige Claude Code 2.1.269 ou superior).
- **Fatos de loja envelhecem.** Prazos, regras e preços (target API do Play, App Review, Data safety, Xcode Cloud) foram verificados em 2026-10-10; reabra a página oficial antes de agir. O prazo principal de target API 36 já passou; a extensão vai até 2026-11-01.
- **iOS exige macOS.** O ambiente deste projeto é Windows: Xcode, Instruments, simulador, archive e `fastlane match` ficam Não verificáveis; builds iOS na nuvem (EAS Build, Xcode Cloud) são Inferido.
- **Lacunas de leitura.** MASVS/MASTG (níveis e controles), skills oficiais Android `navigation`/`testing`/`performance`/`security`, Material 3, payload e notificações silenciosas de push, chaves de privacidade além de câmera e localização, conflito do CloudKit, restrições do WorkManager, energia no iOS, Patrol, App Store Connect Help e a arquitetura de Kotlin Multiplatform não foram lidos. Acessibilidade, push e permissões em React Native e Flutter ficam como Inferido.
- **Comunidade fraca.** Nenhuma thread verificável de Reddit, X ou YouTube; relatos de praticantes (classe C) servem de hipótese, não de regra, e alegações de ganho ("100 mil linhas em um dia") não são verificáveis.
- **Comandos de Android e Flutter** (Gradle, `flutter analyze`, `flutter test`) vêm de conhecimento estável do domínio, não de fonte validada: confirme na versão instalada. O hook documentado de `.pbxproj` é guardrail, não fronteira de segurança.
- O plugin não instala nem executa `npx`, `curl` com pipe para `bash`, Maestro, Detox ou scripts de terceiros; isso é decisão sua, fora da sessão do agente. Evite `--dangerously-skip-permissions`; se usar, só em sandbox e repositório confiável.
