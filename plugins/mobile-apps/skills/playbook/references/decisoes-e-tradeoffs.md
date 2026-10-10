# Decisões e trade-offs em apps mobile

Verificado em 2026-10-10. Cada decisão traz quando escolher cada lado, o custo, o que medir e o rótulo epistêmico. Regra geral: a arquitetura e as ferramentas que o repositório já usa decidem; esta lista serve para projetos novos, para propostas de mudança que exigem ADR (`assets/templates/adr-mobile.md`) e para perguntas "qual devo usar". Nenhuma decisão aqui é norma: são critérios.

## Sumário

- [Como decidir](#como-decidir)
- [D-01 Nativo, React Native/Expo, Flutter ou Kotlin Multiplatform](#d-01-nativo-react-nativeexpo-flutter-ou-kotlin-multiplatform)
- [D-02 Arquitetura de UI: MVVM, MV, MVI, TCA](#d-02-arquitetura-de-ui-mvvm-mv-mvi-tca)
- [D-03 Navegação em React Native: Expo Router ou React Navigation](#d-03-navegação-em-react-native-expo-router-ou-react-navigation)
- [D-04 Testes unitários e de UI](#d-04-testes-unitários-e-de-ui)
- [D-05 E2E: Maestro, Detox, Appium, Patrol](#d-05-e2e-maestro-detox-appium-patrol)
- [D-06 OTA ou nova build](#d-06-ota-ou-nova-build)
- [D-07 Política de conflito na sincronização](#d-07-política-de-conflito-na-sincronização)
- [D-08 Pipeline iOS sem Mac local](#d-08-pipeline-ios-sem-mac-local)
- [D-09 Persistência local](#d-09-persistência-local)
- [D-10 Trabalho em segundo plano no Android](#d-10-trabalho-em-segundo-plano-no-android)
- [D-11 Quando pedir permissão](#d-11-quando-pedir-permissão)
- [D-12 Listas longas em React Native](#d-12-listas-longas-em-react-native)
- [D-13 Mudar de SDK major agora ou depois](#d-13-mudar-de-sdk-major-agora-ou-depois)
- [Registro da decisão](#registro-da-decisão)

## Como decidir

1. Reconheça a decisão que já existe no repositório (o que o código faz hoje) e trate "não mudar nada" como uma opção real com custo próprio.
2. Pergunte o que quebra se estiver errado e quanto custa voltar atrás: troca de framework é cara de reverter; troca de biblioteca de teste é barata.
3. Prefira a opção com evidência de plataforma (classe A) a preferências de autor (classe B/C). Quando a fonte é opinião, o texto diz "preferência".
4. Registre em ADR só decisão material com alternativas reais; escolha de linha de código não precisa de ADR.

## D-01 Nativo, React Native/Expo, Flutter ou Kotlin Multiplatform

| Critério | Nativo (SwiftUI + Compose) | React Native / Expo | Flutter | Kotlin Multiplatform (KMP) |
| --- | --- | --- | --- | --- |
| Time já domina | Swift e Kotlin | JavaScript/TypeScript e React | Dart | Kotlin |
| APIs novas da plataforma no dia do lançamento | Acesso direto | Via módulo nativo ou espera pela comunidade (Inferido) | Via plugin ou canal de plataforma (Inferido) | Direto no lado nativo de cada plataforma (Inferido) |
| Atualização sem loja | Não | Sim, OTA para JS/estilo/assets com EAS Update (V-34) | Não nativo (Não verificável) | Não |
| Código de UI compartilhado | Nenhum | Alto | Alto | Lógica comum; UI nativa ou compartilhada (arquitetura não lida, lacuna 14) |
| Dev em Windows | Android completo; iOS não verifica localmente (V-84) | Android completo; iOS por build na nuvem (EAS) (V-75, Inferido) | Android completo; iOS exige macOS (Inferido) | Android e lógica comum; alvo iOS exige macOS com Xcode (V-84) |
| Arquitetura oficial de referência | Android (V-07), SwiftUI sem guia lido | Sem guia único; Expo Router e AGENTS.md (V-36) | Guia oficial em camadas (V-26) | Só o requisito de ambiente (V-84) |

Critérios de decisão: (1) competência do time, (2) necessidade de OTA, (3) dependência de APIs de plataforma recentes, (4) ambiente de desenvolvimento (macOS disponível?), (5) vida útil esperada do app e custo de manter dois códigos. Rótulo: a comparação é Inferido a partir das fontes citadas; não há benchmark de desempenho nesta base e nenhuma afirmação de "mais rápido" deve ser feita. Medir antes de decidir: protótipo da tela mais exigente (lista longa, animação, câmera) em aparelho de menor capacidade.

## D-02 Arquitetura de UI: MVVM, MV, MVI, TCA

- O repositório decide. Sem repositório definido, proponha opções em ADR.
- Android: UI e dados em camadas, fonte única de verdade, fluxo unidirecional (V-07); tela em ligação de dados, state holder e conteúdo imutável (V-10).
- Flutter: View e ViewModel 1:1, repositório como fonte de verdade, services sem estado (V-26).
- SwiftUI: "MV antes de MVVM" é opinião do autor de V-23, não regra. `@Observable` em `@State` no iOS 17+; `@StateObject` até o iOS 16 (V-23). TCA e MVVM são válidos; o conflito entre V-23 e V-26/V-43/V-07 se resolve pelo repositório (C6).
- Custo de trocar: alto, porque toca estado, navegação e testes. Só vale com problema demonstrado (bug recorrente, teste impossível, tela de 800 linhas).

## D-03 Navegação em React Native: Expo Router ou React Navigation

| Situação | Escolha | Evidência |
| --- | --- | --- |
| Projeto Expo novo, rotas por arquivo | Expo Router; rotas só em `app` (ou `src/app` no template), rota para `/` obrigatória, nomes em kebab-case | V-33, V-36 |
| Projeto já em React Navigation | Manter; instalação com `@react-navigation/native`, `react-native-screens`, `react-native-safe-area-context`; mínimos RN 0.72.0, Expo 52, TypeScript 5.0.0 | V-81 |
| SDK 56 ou superior do Expo | Importar de `expo-router/react-navigation`; `headerLargeTitle` depreciado em favor de `headerLargeTitleEnabled` | V-33 |

`app/` contra `src/app/`: ambas existem, leia a estrutura do projeto (C8). Detalhes de `createNativeStackNavigator` e estado sem Expo Router não têm fonte lida: Inferido. Em Android com React Navigation, o gesto de voltar preditivo ainda não é suportado e deve ser desligado com `android:enableOnBackInvokedCallback="false"` (V-81, conferir a versão).

## D-04 Testes unitários e de UI

| Plataforma | Regra | Fonte |
| --- | --- | --- |
| iOS | Swift Testing para testes unitários novos ("considere usar"); XCTest/XCUIAutomation para UI e performance; não misturar APIs dos dois no mesmo teste (regra por teste, não por target) | V-66 (C11) |
| Android | ViewModel com repositório fake (local); UI instrumentada para o fluxo principal; Compose com `createComposeRule`; Espresso para Views | V-08, V-65, V-68 |
| Flutter | Unitário, widget e integração; muitos unitários/widget, integração para os casos de uso importantes | V-67 |
| React Native | ESLint e TypeScript, Jest, React Native Testing Library por texto/papel, E2E só para o vital | V-69 |

Não preserve nem imponha pirâmide numérica (60/20/5 não é oficial, V-08). Custo de trocar de biblioteca de teste: baixo para o código novo; migre por arquivo quando tocar.

## D-05 E2E: Maestro, Detox, Appium, Patrol

| Ferramenta | Quando faz sentido | Limites verificados |
| --- | --- | --- |
| Maestro | Jornadas declarativas em YAML; integra ao EAS Workflows | Job Maestro no EAS Workflows em alfa; `assertVisible` já espera (brain); alegação de ser mais estável que Detox/Appium não é verificável (V-37, V-44) |
| Detox | App React Native, testes em JavaScript | iOS em aparelho real não suportado; faixa de RN 0.77.x a 0.84.x no README; macOS para iOS não verificado (V-70) |
| Appium | Plataformas diversas, automação externa por drivers | Servidor, driver e cliente têm compatibilidades próprias (brain) |
| Patrol | Flutter com UI nativa (diálogos de permissão, notificações) que `integration_test` não alcança | Citado pela doc do Flutter; não aberto (V-67) |
| Espresso, XCUIAutomation | Time próximo ao código nativo | Exigem infraestrutura do projeto (brain) |

Critério: preserve o stack que já atende ao risco. E2E cobre autenticação, função central e pagamentos; o resto sobe para camadas mais baratas (V-69). `testID` só em E2E de app multilíngue (C2).

## D-06 OTA ou nova build

| Mudou | Caminho | Fonte |
| --- | --- | --- |
| Só JavaScript, estilo ou assets | EAS Update (OTA), respeitando `runtimeVersion` | V-34 |
| Código nativo, permissões, SDK nativo, versão do SDK do Expo | Nova build e nova submissão | V-34 |
| Dúvida | Trate como mudança nativa até provar o contrário (Inferido) | — |

`runtimeVersion` é a fronteira e não muda por conveniência; o canal fica na build e aponta para um branch. Produção só com pedido ou aprovação explícita, nunca inferida pelo branch do git. A fonte não descreve rollback: aponte a documentação do EAS, não invente procedimento. OTA em loja Apple/Google tem limites de política próprios que esta base não leu: Não verificado.

## D-07 Política de conflito na sincronização

| Política | Quando serve | Custo e cuidado |
| --- | --- | --- |
| Última escrita vence | Dados de baixo valor, um dono por registro | Precisa definir qual relógio ou versão manda; hora local de dois aparelhos não dá ordem confiável. Prefira timestamp/versão do servidor (V-59, brain) |
| Recusar o segundo e pedir resolução ao usuário | Dados valiosos, edição rara | Mais trabalho de UI |
| Merge por campo ou por operação | Edição concorrente frequente | A página de V-59 não discute merge por campo: desenho próprio, Suposição |
| Somente servidor (online-only) | Dinheiro, estoque, permissões | Sem modo offline para esse dado |

A decisão é de produto por tipo de dado. O comportamento de conflito do SwiftData com CloudKit não tem fonte: Suposição, não entra como fato (V-61).

## D-08 Pipeline iOS sem Mac local

| Opção | O que resolve | Limite verificado |
| --- | --- | --- |
| EAS Build | Build iOS em macOS runners na nuvem da Expo | Credenciais Apple continuam necessárias (Inferido); a página não diz "sem Mac" (V-75) |
| Xcode Cloud | Workflows, testes em paralelo, TestFlight | Exige Apple Developer Program; 25 h/mês incluídas e pacotes pagos (preços datados, reconfira); página não informa versão de Xcode (V-74) |
| fastlane `match`/`pilot` | Assinatura compartilhada e envio ao TestFlight | Implica macOS (Inferido); `readonly` em CI; `pilot` distribui por padrão (V-71, V-72) |
| Mac local ou alugado | Xcode, Instruments, simulador, archive | Custo e manutenção; fora do escopo de custo desta base |

Em Windows, a decisão típica é EAS Build (se Expo) ou Xcode Cloud (se nativo), com revisão por leitura de tudo que exige Xcode. Custo de CI e de runner macOS pertence a `/devops-cloud-infra:playbook`.

## D-09 Persistência local

| Plataforma | Dados estruturados | Dados simples | Observações |
| --- | --- | --- | --- |
| Android | Room | DataStore | Fonte local é a única que a UI lê; leituras como tipos observáveis (V-59) |
| iOS | SwiftData; com CloudKit exige capabilities e modelo compatível | Keychain para segredos, nunca `UserDefaults` | Sem `unique`, relacionamentos opcionais; esquema de produção só aceita adições (V-61, V-83) |
| RN e Flutter | Sem fonte lida na base | Segredos em armazenamento seguro da plataforma | Lacuna 12 e 16: Inferido |

## D-10 Trabalho em segundo plano no Android

| Necessidade | Mecanismo | Fonte |
| --- | --- | --- |
| Trabalho adiável que precisa sobreviver ao fechamento do app | WorkManager (`Worker`, `OneTimeWorkRequest`, `Result.retry()`) | V-60 |
| Mensagem crítica para o usuário | FCM de alta prioridade, só se gerar notificação | V-63 |
| Horário exato | Alarme (`setExactAndAllowWhileIdle`, no máximo um a cada nove minutos por app em Doze); detalhe fora do V-60, conferir na documentação de alarmes | V-63 (C5) |
| Manter CPU ligada por longo tempo | Evitar wake lock; medir no Android vitals | V-62 |

Em Doze o trabalho do WorkManager espera a janela de manutenção (V-63); como ele a usa em detalhe não foi lido (lacuna 8).

## D-11 Quando pedir permissão

| Momento | Quando usar | Fonte |
| --- | --- | --- |
| Primeiro launch | Só se for obrigatório ao produto ou com `.provisional` em notificações iOS, que não exibe diálogo | V-53 |
| No uso real, com contexto | Padrão: exemplo "depois do primeiro item criado" para notificações | V-53, V-58 |
| Antes do uso, com tela de pré-explicação | Android: só quando `shouldShowRequestPermissionRationale()` for verdadeiro | V-54, V-56 |

Após negação: iOS pode oferecer caminho alternativo ou o atalho para Ajustes sem insistir (Inferido); no Android, não apontar às configurações para convencer o usuário (V-56, C3).

## D-12 Listas longas em React Native

`FlatList` com `getItemLayout` quando os itens têm altura fixa; FlashList ou Legend List quando a lista é longa e a medição mostra queda de quadros (V-30). Virtualizar listas longas é a prioridade mais alta na skill de Vercel (V-31, classe B). Nenhuma biblioteca de lista é "melhor": meça no aparelho de menor capacidade (V-32).

## D-13 Mudar de SDK major agora ou depois

- Agora: quando o alvo de loja exige (targetSdk do Play: ver `loja-release-ambiente.md`), quando uma dependência crítica só suporta a versão nova, ou quando o SDK atual saiu de suporte.
- Depois: quando nada o força e o time não tem janela para regressão completa.
- Como: um salto de major por vez; leia a nota de atualização oficial da versão de destino; no Expo, `npx expo install --fix` e `npx expo-doctor` (V-36); rode build e testes a cada salto (skill `mobile-build-troubleshoot`). Rótulo do processo: Inferido (conhecimento estável); os comandos do Expo são Verificados.

## Registro da decisão

Use `assets/templates/adr-mobile.md`: contexto, opções (incluindo "não mudar nada"), decisão, consequências, validação e condição de revisão. Referencie a decisão de sistema de `/architecture-design:playbook` quando houver. Datas e versões entram no ADR porque este tipo de decisão envelhece.
