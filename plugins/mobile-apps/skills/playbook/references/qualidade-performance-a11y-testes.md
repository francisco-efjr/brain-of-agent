# Qualidade: performance, bateria, acessibilidade, testes e QA mobile

Verificado em 2026-10-10. Fontes: V-08, V-11, V-18, V-22, V-29, V-30, V-32, V-48, V-62 a V-70, V-78, V-79 e o brain-of-agent (`qa/mobile.md`, MIT, Francisco Edson; ideias de processo do gstack `ios-qa`, MIT, Garry Tan, destiladas). Estratégia geral de QA (automação web e API, carga) pertence a `/qa-testing:playbook`; aqui fica o específico de plataforma mobile.

## Sumário

- [Performance: ciclo de medição](#performance-ciclo-de-medição)
- [Bateria](#bateria)
- [Acessibilidade](#acessibilidade)
- [Estratégia de testes](#estratégia-de-testes)
- [QA mobile: matriz de risco](#qa-mobile-matriz-de-risco)
- [Ciclo de vida e persistência](#ciclo-de-vida-e-persistência)
- [Atualização e compatibilidade](#atualização-e-compatibilidade)
- [Automação confiável e diagnóstico](#automação-confiável-e-diagnóstico)
- [Tiers de evidência](#tiers-de-evidência)
- [Roteiro mínimo de release](#roteiro-mínimo-de-release)

## Performance: ciclo de medição

Princípio comum a todas as plataformas (V-11, V-22, V-32, V-30, V-29): **reproduzir uma transição, classificar o eixo, mudar uma coisa, remedir a mesma captura**; reverter se não houver ganho. Debug e simulador não representam: use build release ou profile no aparelho de menor capacidade. Memoização, `@Immutable` e `useMemo` sem problema medido são antipadrão. Prometer ganho numérico sem medição é falha: escreva "Não verificável (sem medição)".

| Plataforma | Eixos e ferramentas | Fonte |
| --- | --- | --- |
| Compose | Estabilidade, fase de leitura de State, escrita de snapshot; relatório do compilador; strong skipping padrão no Kotlin 2.0.20+; `@Immutable`/`@Stable` são promessas | V-11 |
| SwiftUI | Classificar sintoma, revisar código, perfil guiado só se necessário (Instruments, macOS), mapear evidência, corrigir, repetir a mesma captura | V-22 |
| Flutter | Orçamento de 16 ms (8 de build, 8 de render); profile mode com DevTools; trabalho fora de `build()`; `setState` mínimo; `const`; listas lazy | V-29 |
| React Native | Release; remover `console.*`; `getItemLayout`; FlashList ou Legend List; `useNativeDriver`; Perf Monitor; medir só cold start para TTI | V-30, V-32 |

Não há benchmark nem baseline profile exigidos por V-11 (lacuna). Para o relatório, use `assets/templates/relatorio-performance.md` e **redija dados sensíveis** de traces e screenshots (correção de V-22: o original não orienta isso nem limita dispositivos de produção).

Exemplo de relatório (uma linha):

```text
Sintoma: rolagem da lista de pedidos cai de quadros em aparelho de entrada (release).
Causa suspeita: leitura de scroll em composição recompõe todos os itens (fase de leitura de State).
Evidência: relatório do compilador + captura "antes" anexada (dados sensíveis redigidos).
Correção: mover a leitura para o modificador de layout; uma mudança.
Validação: mesma captura depois; números na tabela; revertido se sem ganho.
```

## Bateria

- **Android** (V-62, V-63): wake locks parciais excessivos no Android vitals (mais de 2 h acumuladas de wake locks não isentos em 24 h é sessão excessiva; limiar com 5% das sessões em 28 dias; investigar tags com P90 ou P99 acima de 60 min); Doze e App Standby (trabalho adiável via WorkManager, mensagem crítica via FCM de alta prioridade só se gerar notificação, alarmes com `setAndAllowWhileIdle`/`setExactAndAllowWhileIdle`, no máximo um a cada nove minutos por app; exclusão de otimização só com justificativa). Verificado em 2026-10-10; reconfira. Teste em emulador com `adb shell dumpsys deviceidle force-idle` e `unforce`.
- **iOS** (V-64, classe B): processo "fazer menos trabalho, trabalhar com mais eficiência, não abusar das APIs"; reaja ao Low Power Mode (`ProcessInfo.processInfo.isLowPowerModeEnabled`, observando a notificação de estado de energia): reduza animações, taxa de quadros, localização, sincronizações; retome ao sair. Medir com as ferramentas da Apple (macOS). A página arquivada de Low Power Mode é de 2016 e a sintaxe Swift dela é obsoleta. Artigos de detalhe e Power Profiler não foram lidos (lacuna 9).

## Acessibilidade

### Checklist de 9 itens (V-48 estendido por V-78 e V-79)

Números vêm de fontes A (V-18, V-09, V-79): não use "20x20 pt", "13 pt" nem "24 pt" de fontes de inspiração (C15).

1. Todo controle interativo tem rótulo; decorativos ocultos. Rótulo curto e sem repetir o tipo ("Enviar", não "Botão enviar") no Android (V-79); no iOS a regra do tipo é Inferido até ler traits (V-78).
2. Controles nativos em vez de gestos: `Button`, não `onTapGesture` (V-19).
3. **Alvos:** 44x44 pt no iOS (mínimo absoluto 28x28 pt, V-18); 48x48 dp no Android (V-79: `Button` e `IconButton` já aplicam; elementos personalizados precisam de `sizeIn`).
4. **Texto escalável:** Dynamic Type até 200% (140% no watchOS); texto padrão 17 pt e mínimo 11 pt no iOS; `sp` no Android; teste no maior tamanho.
5. Agrupar elementos relacionados e marcar títulos (`mergeDescendants`, `heading()` no Android; agrupamento no iOS para a ordem certa).
6. Ordem de foco igual à visual.
7. **Contraste:** iOS 4,5:1 até 17 pt e 3:1 a partir de 18 pt ou negrito; Android 4,5:1 abaixo de 18 sp (ou negrito abaixo de 14 sp) e 3:1 no restante; informação nunca só por cor. Contraste de componentes não textuais não consta em V-79.
8. Respeitar Reduce Motion e dar alternativa visível a gestos (`customActions` no Android).
9. Estado dinâmico anunciado (botão selecionado, por exemplo, pois a mudança de cor não é percebida); hint só quando necessária, e conteúdo longo demais no rótulo pode ir para a dica (V-78).

### VoiceOver (V-78) e TalkBack

Auditoria com VoiceOver ligado (Ajustes > Acessibilidade > VoiceOver). Gestos-chave: deslizar para navegar, toque duplo para ativar, toque com dois dedos para parar ou retomar a fala, deslizar com dois dedos para cima para ler tudo, toque triplo com três dedos para ligar e desligar o Screen Curtain. Verifique acesso a todo elemento e a ordem de leitura. Elementos personalizados não são reconhecidos por padrão: precisam de `isAccessibilityElement` e rótulo. `UILabel` e `accessibilityLabel` são coisas diferentes.

A passagem manual com VoiceOver ou TalkBack é **verificação humana**: o agente confere código e registra a pendência. Traits e a regra do tipo no rótulo do iOS: Inferido até a página de traits ser lida. RN e Flutter: sem fonte de APIs de semântica, rotule Inferido. Material 3 oficial não foi lido.

### Responsabilidades

O agente revisa rótulos, alvos, escala, contraste, ordem e movimento por leitura de código e, quando o ambiente permite, por inspetor. O humano executa a passagem com leitor de tela. Seletores de teste não substituem nomes acessíveis úteis a pessoas.

## Tokens do design system em Compose/SwiftUI

Quando o app adota o design system da casa (`design-systems/mo-baile/`, criado pelo usuário), mapeie os tokens semânticos para o tema nativo; não crie um tema paralelo. Os valores vêm do código de origem, não desta referência. O Mo baile nasceu de `Theme/DesignTokens.swift`, `Theme/PraiaLightTheme.swift` e `Theme/PraiaDarkTheme.swift`, conforme `design-systems/mo-baile/github.md` (Screen map). Mantenha no repositório do app uma tabela token→arquivo nativo, para rastrear código→token.

- **Compose:** papéis de cor no `MaterialTheme` (`ColorScheme`); métricas, raios e movimento que o Material não cobre num objeto próprio via `CompositionLocal`. Claro, escuro e alto contraste são variantes do tema, escolhidas pela configuração do sistema.
- **SwiftUI:** Asset Catalog com Appearances (Any, Dark, High Contrast) e cores nomeadas, por exemplo `Color("label.primary")`, lidas por um `Theme` injetado em `Environment`.
- **Reduzir movimento e transparência:** no Compose, ler a escala de animação do sistema (`Settings.Global.ANIMATOR_DURATION_SCALE`) e injetar no tema; no SwiftUI, `@Environment(\.accessibilityReduceMotion)` e `accessibilityReduceTransparency`. O efeito é o mesmo do fallback de token da web: troca de movimento e de material, sem `if` nas telas.
- **Molas:** `spring(dampingRatio, stiffness)` no Compose e `.smooth`, `.snappy`, `.bouncy` no SwiftUI, com constantes nomeadas que espelham `tokens/motion.css` do DS.
- **Tipografia:** `sp` no Compose e `Font.TextStyle` (Dynamic Type) no SwiftUI, nunca tamanhos fixos vindos do protótipo macOS.
- **Lint de aderência:** detekt ou Android Lint com regra própria contra `Color(0x…)` e `.dp` literal fora do tema; SwiftLint `custom_rules` contra `Color(red:` e `.font(.system(size:`.
- **Estado:** ícone, texto e cor juntos (`Icon` ou `Label` com `contentDescription` ou `accessibilityLabel`).
- Visão completa e precedência do DS: `/ux-ui-design:playbook`.

## Estratégia de testes

| Camada | Android | iOS | Flutter | React Native |
| --- | --- | --- | --- | --- |
| Unitário | Local (JVM); ViewModel com fake (V-08) | Swift Testing para novos (V-66) | Unitário (V-67) | Jest (V-69) |
| Componente / UI | `createComposeRule` (V-65); Espresso para Views (V-68) | XCTest + XCUIAutomation (V-66; simulador, macOS) | Widget test (V-67) | RNTL por texto/papel (V-69) |
| Integração | Instrumentado (V-08) | XCTest | `integration_test`; `patrol` para UI nativa (V-67) | Integração com Jest (V-69) |
| E2E | Só o vital | Só o vital | Poucos | Detox, Appium ou Maestro só para o vital (V-69, V-70, V-37) |

Regras: muitos testes baratos, poucos caros, sem pirâmide numérica oficial; não use `sleep` (espere condição); `testID` só em E2E de app multilíngue (C2); nenhum teste enfraquecido para passar; vermelho antes do verde em bug novo; Detox exige conferir a faixa de RN (V-70). Instalação de ferramentas de teste é decisão do usuário (V-44). Plano: `assets/templates/plano-testes-mobile.md`.

## QA mobile: matriz de risco

Comece pelo risco do app e pela base real de dispositivos; uma lista genérica de aparelhos não é estratégia. Emulação de viewport no navegador não executa o binário mobile nem prova permissões, ciclo de vida, armazenamento ou integrações nativas. Registre app/build, SO e versão, modelo, resolução, idioma, escala de fonte, tipo de instalação, estado das permissões, flags e backend. Não deduza a versão mínima suportada pela versão instalada no aparelho disponível.

| Dimensão | Escolha inicial | Quando ampliar |
| --- | --- | --- |
| SO | Mínima suportada e versão representativa atual da base | Mudança de SDK, APIs nativas, permissões ou incidente em uma versão |
| Hardware | Aparelho representativo e um com recursos limitados | Câmera, NFC, biometria, memória, fabricante ou problema térmico |
| Tela e entrada | Tela pequena e fonte ampliada | Tablet, dobrável, orientação ou teclado especial no escopo |
| Distribuição | Instalação limpa e atualização desde versão em uso | Migração de banco local, assinatura, login ou esquema de armazenamento |
| Rede | Estável e interrupção no fluxo crítico | App offline, upload, streaming, rede corporativa ou reconexão frequente |
| Acessibilidade | TalkBack/VoiceOver e fonte ampliada no fluxo crítico | Componentes novos, gestos próprios, gráficos ou controles sem rótulo |

Emulador e simulador dão retorno rápido e estados reproduzíveis; valide em aparelho físico os riscos que dependem de hardware, consumo, rede real ou comportamento de fabricante. O Android distingue testes locais e instrumentados e admite emulador ou aparelho nos instrumentados (V-08); isso não torna os ambientes equivalentes.

| Abordagem | Boa adequação | Limite explícito |
| --- | --- | --- |
| Testes de regra / view-model | Estados, cálculo, validação, sincronização controlada | Não provam renderização nem integração com o SO |
| Espresso / Compose test | Time próximo ao código Android, componentes e UI | Abordagem compatível com a tecnologia de UI do projeto |
| XCTest + XCUIAutomation | Fluxos e estado da UI Apple | Exige infraestrutura do projeto Apple |
| Appium | Automação externa por drivers, mais de uma plataforma | Servidor, driver e cliente têm compatibilidades próprias |
| Maestro | Jornadas declarativas com seletores visíveis ou IDs | Validar suporte às interações nativas antes de migrar a suíte |
| Exploração em aparelho | Interrupções, ergonomia, acessibilidade, falhas difíceis de modelar | Registrar estado e evidência para reproduzir |

Preserve o stack do projeto se ele atende ao risco. Não gere capabilities, gestos ou comandos de sessão de memória quando a versão da ferramenta é desconhecida. Template: `assets/templates/matriz-dispositivos-risco.md`.

## Ciclo de vida e persistência

"Fechei e abri" é ambíguo. Identifique a transição: ir para Home, recriar uma tela, remover da lista de recentes, forçar parada, encerrar o processo e reinstalar têm efeitos diferentes. No Android, a opção "Don't keep activities" destrói activities ao sair delas e não prova todos os cenários de morte do processo (URL da opção de desenvolvedor não reaberta: ver `fontes.md`).

| Momento de interrupção | Ação controlada | Resultado a definir e testar |
| --- | --- | --- |
| Formulário parcialmente preenchido | Alternar de app e retornar | Campos preservados conforme regra; dado sensível tratado conforme política |
| Resposta crítica pendente | Enviar a segundo plano e encerrar o processo de teste | Ao reabrir, consultar a operação existente; não criar nova cobrança automaticamente |
| Conteúdo autenticado | Bloquear aparelho; expirar sessão; retomar | Exigir autenticação quando previsto; não exibir dado de outra sessão |
| Upload parcial | Interromper o processo e reabrir | Retomar ou reiniciar conforme contrato, sem arquivo corrompido nem duplicado |
| Mudança de configuração | Girar a tela ou mudar de tamanho | Estado coerente, sem submissão duplicada |
| Fila offline persistida | Reiniciar o app e o aparelho | Fila preserva identidade, ordem necessária e estado de confirmação |

Preservar todo dado sempre pode ser tão errado quanto perder tudo: defina o esperado com produto e segurança. Teste também sair da conta A e entrar na B no mesmo aparelho: cache, notificações, busca recente, anexos e fila não vazam entre contas.

## Atualização e compatibilidade

Não limpe dados antes do teste que pretende provar atualização. (1) Registre o build anterior, a identidade sintética e o estado persistido. (2) Atualize para o artefato candidato e registre sua identidade exata. (3) Confira abertura, migração, autenticação, itens e totais reconciliados. (4) Execute uma leitura e uma escrita importantes; abrir a home é pouco. (5) Teste falha ou interrupção de migração em ambiente controlado quando esse é o risco; confirme recuperação e ausência de alteração parcial. Instalação limpa, atualização e reinstalação são cenários diferentes; desinstalar não apaga necessariamente todo o estado (backup, credenciais, restauração).

Backends convivem com apps antigos: cubra o cliente anterior ainda suportado contra o backend novo e a política de atualização obrigatória. Rollback de backend não remove binários distribuídos; rollback de app nem sempre é instantâneo. Planeje compatibilidade, flags remotas e recuperação de dados antes de liberar.

## Automação confiável e diagnóstico

- Prepare contas e registros sintéticos por API ou fixture quando criar pela UI não é o comportamento em teste; redefina permissões, sessão e dados sem apagar o estado que o cenário de atualização exige.
- Localize por semântica e identificador estável exposto pelo app; texto serve quando faz parte do comportamento e o idioma está controlado. Coordenadas, índices e XPath longo quebram com teclado, tela e conteúdo.
- Aguarde condição com limite e evidência do estado final. No Maestro, `assertVisible` já aguarda o elemento até o timeout, o que não equivale a repetir uma ação de negócio: repetir "Confirmar pagamento" para contornar lentidão pode duplicar a operação.
- Na falha, capture build ou commit, dispositivo e SO, estado inicial, etapas, timestamp com fuso, screenshot ou hierarquia de UI, logs redigidos e ID da operação. Preserve o primeiro erro antes de repetir. Se a UI mostra sucesso e a API não, registre os dois.
- Lentidão: separe partida fria e quente, bloqueio de UI, tempo do servidor, renderização e consumo prolongado; defina metas e compare com baseline no mesmo perfil. ANR, crash, memória e bateria pedem observação específica, não só cronômetro de E2E.
- Registro: `assets/templates/registro-evidencias.md`.

## Tiers de evidência

Ideia destilada do gstack `ios-qa` (MIT, Garry Tan; só o conceito, nenhum comando): distinga **(1) estado preparado por fixture**, **(2) UI do provedor externo** e **(3) sucesso real no provedor externo**. Um tier não prova o seguinte. Captura de tela não prova persistência; CI verde não prova o fluxo se as asserções forem fracas; revisão por leitura não é teste executado.

## Roteiro mínimo de release

Adapte à mudança; não é certificação universal:

- Uma jornada crítica com resultado persistido na matriz escolhida.
- Interrupção e retomada no ponto de maior risco da jornada.
- Operação com resposta perdida, quando há efeito remoto relevante.
- Atualização preservando dados, se a release toca armazenamento, sessão ou SDK.
- Negativo de permissão ou autorização relevante e troca de conta.
- Uso do fluxo com leitor de tela e fonte ampliada nas partes alteradas.
- Evidências da versão candidata, lacunas e risco residual por plataforma.

Se só houve emulador Android, escreva exatamente isso. Não estenda o resultado a iOS, a aparelho físico nem à distribuição de loja sem execução correspondente.
