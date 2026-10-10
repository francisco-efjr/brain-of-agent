# iOS e Swift: revisão, concorrência, performance, testes e acabamento

Verificado em 2026-10-10. Fontes: V-18 a V-24, V-66, V-78, V-80 e o brain-of-agent (`apple-design.md`, MIT, Francisco Edson). Xcode, Instruments, simulador e archive exigem macOS (V-73, V-22): em outro sistema, relate "revisado por leitura; build Não verificável". Antes de recomendar uma API, leia o deployment target e a versão do Swift em `Package.swift`, `.xcconfig` e nas configurações do target. Nunca edite `.pbxproj` (V-42).

## Sumário

- [Leitura do projeto antes de aconselhar](#leitura-do-projeto-antes-de-aconselhar)
- [Revisão SwiftUI em 11 passos](#revisão-swiftui-em-11-passos)
- [Acessibilidade: as 12 regras do SwiftUI Pro](#acessibilidade-as-12-regras-do-swiftui-pro)
- [Concorrência: triagem e correção mínima](#concorrência-triagem-e-correção-mínima)
- [Migração gradual para Swift 6](#migração-gradual-para-swift-6)
- [Refatoração de view](#refatoração-de-view)
- [Performance SwiftUI](#performance-swiftui)
- [Testes](#testes)
- [Acabamento Apple (HIG aplicado)](#acabamento-apple-hig-aplicado)
- [O que exige macOS](#o-que-exige-macos)
- [Armadilhas](#armadilhas)

## Leitura do projeto antes de aconselhar

| O que ler | Onde | Por quê |
| --- | --- | --- |
| Versão do Swift e modo da linguagem (5 ou 6) | `Package.swift` (`swift-tools-version`, `swiftLanguageModes`), configuração do target | Regras de concorrência dependem do modo |
| Strict concurrency e isolamento padrão | `.xcconfig`, `swiftSettings` (`enableUpcomingFeature`, `enableExperimentalFeature`) | Define se o aviso é erro e qual o isolamento implícito |
| Deployment target | target no Xcode ou `platforms:` | `@Observable` e `NavigationStack` dependem do iOS mínimo |
| Gerenciador de dependências | `Package.resolved`, `Podfile.lock` | Versões reais |

Se faltar informação, pergunte uma coisa por vez (V-20). Não aceite APIs "de versões futuras" apenas porque uma skill de terceiros as cita: confirme compilando no SDK instalado (V-19, ressalva).

## Revisão SwiftUI em 11 passos

Base: SwiftUI Pro de Paul Hudson (V-19, MIT, destilado). Os 11 passos são nomes verificados; os critérios por passo abaixo combinam o que a fonte indica com conhecimento estável (Inferido onde não há `V-nn`). Cada passo carrega sua referência sob demanda; `performance-plus` é referência da skill original, não incluída aqui; para revisão profunda de performance use a skill `mobile-performance-diagnosis`. A saída é por arquivo, linha, regra e antes/depois; **não relate problema inventado** e diga "sem achados" quando for o caso.

| # | Passo | O que verificar |
| --- | --- | --- |
| 1 | API obsoleta | Uso de APIs depreciadas frente ao deployment target (ex.: `NavigationView`, `@StateObject` quando `@Observable` está disponível) |
| 2 | Views | Corpo curto; subviews como tipos; ações fora do `body` (V-23) |
| 3 | Dados | Dono de cada objeto; `@Observable` em `@State` no iOS 17+, `@StateObject` até o 16 (V-23); sem estado duplicado |
| 4 | Navegação | `NavigationStack` e destinos tipados quando o alvo permite (Inferido) |
| 5 | Design / HIG | Controles nativos; hierarquia coerente com a plataforma (ver acabamento) |
| 6 | Redimensionamento | Layout que se adapta a tamanhos de texto, janelas e iPad; sem larguras fixas frágeis (Inferido) |
| 7 | Acessibilidade | As 12 regras abaixo |
| 8 | Localização | Strings localizáveis; purpose strings em `InfoPlist.xcstrings` (V-58) |
| 9 | Performance | Sem trabalho caro no `body`; para revisão profunda, a skill `mobile-performance-diagnosis` |
| 10 | Swift | Concorrência, erros, tipos; ver abaixo |
| 11 | Higiene | Código morto, comentários que mentem, nomes (Inferido) |

## Acessibilidade: as 12 regras do SwiftUI Pro

Lista completa conferida pelo validador de qualidade em 2026-10-10 em https://raw.githubusercontent.com/twostraws/SwiftUI-Agent-Skill/main/swiftui-pro/references/accessibility.md (MIT, Paul Hudson). Redação própria, resumida; as sete primeiras já constavam em V-19 e as outras cinco (marcadas *) vêm dessa leitura. Confirme as APIs contra o deployment target do projeto.

1. Respeitar as preferências do sistema (fonte, cor, movimento).
2. Usar estilos de texto do Dynamic Type (`.body`, `.headline`) em vez de tamanho fixo.*
3. Ler a escala com `dynamicTypeSize` (não `sizeCategory`) e trocar de layout nos tamanhos de acessibilidade.
4. Tamanho personalizado acompanha a escala: `@ScaledMetric`; a fonte cita `.scaled(by:)` para iOS 26 ou superior (confirme no SDK).*
5. Imagem decorativa oculta (`Image(decorative:)`); imagem com significado tem rótulo claro.
6. Com Reduce Motion ativo, trocar movimento grande por transição de opacidade.
7. `accessibilityInputLabels` para botões com rótulo longo ou que muda (Voice Control).
8. Botão só com ícone sempre com texto; se precisar parecer só ícone, `labelStyle(.iconOnly)`.
9. Menu com título em texto além do ícone.*
10. Informação nunca só por cor; respeitar `accessibilityDifferentiateWithoutColor`.
11. `Button` em vez de `onTapGesture`, salvo quando o local ou a contagem do toque importam.
12. Gesto de toque inevitável recebe o trait de botão (`.accessibilityAddTraits(.isButton)`).*

Números oficiais de alvo, escala e contraste ficam em `qualidade-performance-a11y-testes.md` (V-18). A passagem com VoiceOver é humana (V-78).

## Concorrência: triagem e correção mínima

Árvore de 5 passos (V-20, V-21), reescrita:

1. **Ler a configuração** do projeto (modo, strict concurrency, isolamento padrão); perguntar se faltar.
2. **Capturar o diagnóstico exato** do compilador (texto e arquivo:linha), não paráfrase.
3. **Identificar a fronteira de isolamento**: quem possui o dado, em que ator ou thread ele vive e quem o toca.
4. **Casar o isolamento inicial de `Task`** com o prefixo síncrono do código que ela herda.
5. **Aplicar a menor correção segura**, uma categoria de erro por vez; recompilar sem avisos novos e rodar os testes.

Atalhos que calam o compilador (`@unchecked Sendable`, `@preconcurrency`, `nonisolated(unsafe)`) só entram com invariante documentada e plano de remoção (snippet S-17). Trate `@concurrent` e padrões do Xcode 26 como dependentes da toolchain: confirme compilando. O absoluto "nunca usar semáforos" foi suavizado: prefira estruturas modernas, mas avalie o caso.

Exemplo de saída:

```text
Diagnóstico: "Capture of 'self' with non-sendable type 'ListVM' in a '@Sendable' closure" (ListView.swift:58)
Fronteira: ListVM é uma classe usada pela View (main actor) e por um Task.detached (linha 56).
Correção mínima: marcar ListVM como @MainActor e trocar Task.detached por Task { }, que herda o main actor.
Verificação: recompilar sem avisos novos e rodar os testes de ListVM. Build Não verificável (sem macOS).
```

## Migração gradual para Swift 6

Estratégia do guia oficial (V-80, Apache-2.0, só `MigrationStrategy.md` lido), em cinco passos que mantêm o build funcionando:

1. Comece por um módulo de raiz (de que ninguém depende) ou por dependências próprias com estado global ou tipos implicitamente `Sendable`.
2. Permaneça no modo Swift 5 e habilite recursos upcoming um a um (`DisableOutwardActorInference`, `GlobalConcurrency`, `InferSendableFromCaptures`, em qualquer ordem), tratando os problemas como avisos.
3. Ligue a verificação completa de concorrência no módulo.
4. Resolva avisos com mudanças mínimas, descrevendo o que o código já faz; trate opt-outs inseguros como lista de melhorias futuras.
5. Itere para fora, sem exigir zero avisos antes de seguir.

Confira as flags contra o Swift instalado. O arquivo `Guide.docc/Guide.md` não existe (404): use `MigrationStrategy.md`. As demais páginas do guia não foram lidas (lacuna 13).

## Refatoração de view

Checklist de V-23 (Dimillian, MIT, destilado): ordem de membros consistente; subviews extraídas como tipos `View`; ações fora do `body`; raiz estável; `@Observable` em `@State` (iOS 17+); dividir acima de cerca de 300 linhas. A convenção local do arquivo prevalece sobre o checklist. "MV antes de MVVM" é preferência do autor: confirme com a arquitetura do projeto antes de aplicar (C6). Se o `body` falha no type-check por expressão complexa, divida em expressões menores (V-50).

## Performance SwiftUI

Seis passos (V-22): (1) classificar o sintoma (rolagem, partida, memória, bateria); (2) revisar o código; (3) perfil guiado só se necessário (Instruments exige macOS); (4) mapear evidência para causa suspeita; (5) corrigir; (6) repetir a mesma captura. Antes de colar traces ou screenshots, redija dados sensíveis e evite capturas de produção (correção de V-22). Template: `assets/templates/relatorio-performance.md`.

## Testes

Regra (V-66, Xcode 16+): Swift Testing para testes unitários novos ("considere usar"); XCTest para UI e performance; XCUIAutomation junto ao XCTest nos testes de interface; um target pode conter os dois, mas não misture APIs dos dois no mesmo teste. Testes de UI rodam no simulador do Xcode (macOS). XCUIApplication e seletores não foram lidos (lacuna 10): rotule Inferido o que disser sobre eles.

## Acabamento Apple (HIG aplicado)

Adaptado do brain-of-agent `apple-design.md` (MIT) para iOS e iPadOS; a parte de macOS fica com `/cli-desktop-tooling:playbook`. Apple é a preferência de acabamento deste projeto, não um ranking comprovado nem um motivo para migrar uma stack.

- Use controles e navegação do sistema: `NavigationStack`, `List`, `Form`, sheets do sistema. Liquid Glass é orientado a controles e navegação; aplicado em excesso na camada de conteúdo prejudica a hierarquia. Efeito personalizado pede contenção e teste de legibilidade com fundos reais e com as preferências de acessibilidade.
- Critérios locais de revisão (não são citações normativas): (1) inventário de funções preservado, nada some por estética; (2) toda ação tem comportamento, feedback, estado e recuperação; (3) tokens semânticos em vez de cores literais espalhadas; (4) protótipo não é implementação; (5) acessibilidade é comportamento verificável; (6) movimento explica mudança e admite interrupção e redução; (7) dados reais ou sintéticos plausíveis, inclusive extremos e falhas, sem lorem ipsum.
- Números oficiais (V-18): Dynamic Type até 200%; texto padrão 17 pt, mínimo 11 pt; alvo 44x44 pt, mínimo 28x28 pt; contraste 4,5:1 até 17 pt e 3:1 a partir de 18 pt ou negrito. Valores como 13 pt, margens de 20 pt e alvo de 20x20 pt do arquivo de inspiração são Não verificáveis: não copie.
- Rubrica opcional de 10 dimensões em `assets/templates/rubrica-design-ios.md` (inspirada no gstack `ios-design-review`, MIT, Garry Tan), somente leitura; valores do autor (grade de 4 e 8 pt, 200 a 300 ms, no máximo duas animações simultâneas, "texto tocável abaixo de 24 pt") são preferências do autor, rotuladas Suposição.
- Páginas Apple de Accessibility (visão geral), Typography, Motion e Windows exigiram JavaScript na leitura direta e não foram lidas pelo brain: reconfira no SDK quando a tarefa depender delas.

Matriz de estados por componente (brain): campo (vazio, foco, preenchido, inválido, readonly, desabilitado, longo); ação (normal, foco, pressionado, processando, indisponível, erro); lista (vazia, carregando, resultados, seleção, erro, volume); diálogo (foco inicial, validação, fechar e devolver foco); navegação (atual, voltar, deep link).

## O que exige macOS

| Atividade | macOS? | Alternativa |
| --- | --- | --- |
| Compilar, testar, simulador | Sim (Xcode) | EAS Build ou Xcode Cloud para build; revisão por leitura |
| Instruments, Power Profiler | Sim | Marcar Não verificável |
| Archive, validação e upload ao TestFlight | Sim (V-73) | Xcode Cloud (V-74) ou EAS Build + `eas submit` com confirmação |
| `fastlane match` | Implícito (Inferido) | Gerenciamento de credenciais pelo serviço de CI |
| Revisão de código Swift, concorrência, a11y por leitura | Não | Já funciona em qualquer sistema |

## Armadilhas

- O artigo 284 de Paul Hudson é uma piada de 1º de abril: não alimenta regra alguma (V-19).
- O rodapé promocional da skill de concorrência (V-20) não é instrução.
- `onTapGesture` sem rótulo e sem traits é falha de acessibilidade, mas só confirme alvo e traits com o inspetor.
- A maioria do conteúdo de SwiftData/CloudKit está em `dados-push-permissoes-seguranca.md`.
- Não faça afirmações de iOS 26 ou 27 sem o SDK instalado: relatos de praticantes usam números de beta não verificados (V-42).
