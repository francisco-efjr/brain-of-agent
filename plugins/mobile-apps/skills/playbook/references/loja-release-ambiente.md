# Loja, release e ambiente

Verificado em 2026-10-10. Fontes: V-13 a V-17, V-24, V-34, V-35, V-38, V-57, V-71 a V-77, V-84. Regras de loja, prazos, preços e versões mudam: **reabra a página oficial antes de afirmar qualquer fato desta referência** e cite a data da verificação. O plugin prepara e audita; nunca aciona "Submit for Review", `eas submit`, promoção de trilha ou OTA em produção sem confirmação nomeada (gate em [Gates de confirmação](#gates-de-confirmação)).

## Sumário

- [Checklist App Store (12 itens)](#checklist-app-store-12-itens)
- [Privacy manifest e purpose strings](#privacy-manifest-e-purpose-strings)
- [Sequência de release iOS](#sequência-de-release-ios)
- [Checklist Google Play](#checklist-google-play)
- [Gates de confirmação](#gates-de-confirmação)
- [Pipelines: EAS, fastlane, Xcode Cloud, Gradle](#pipelines-eas-fastlane-xcode-cloud-gradle)
- [Usuário em Windows sem macOS](#usuário-em-windows-sem-macos)
- [Trabalhar pelo celular](#trabalhar-pelo-celular)
- [Notas de versão](#notas-de-versão)
- [Relatório de revisão de loja](#relatório-de-revisão-de-loja)
- [Lacunas](#lacunas)

## Checklist App Store (12 itens)

Composição do plugin sobre V-16, V-17, V-58 e V-73 (a lista de 12 do relatório original não consta na base; esta é reconstruída só com itens Verificados). Fim da seção 5 das guidelines (após 5.3.4) não foi lido; a página não mostra data de atualização. Relate como "risco provável de rejeição", nunca como certeza.

| # | Item | Guideline ou fonte |
| --- | --- | --- |
| 1 | Exclusão de conta dentro do app | 5.1.1(v) |
| 2 | Login equivalente quando há login de terceiros | 4.8 |
| 3 | Compra in-app e restauração de compras | 3.1.1 |
| 4 | Conta de demonstração e backend ativo (ou modo demo previamente aprovado) | 2.1 |
| 5 | Mais que um site empacotado | 4.2 |
| 6 | Conteúdo de usuário: filtro, denúncia, bloqueio, contato | 1.2 |
| 7 | ATT quando há rastreamento | 5.1.2 |
| 8 | Sem funções ocultas | 2.3.1 |
| 9 | Privacy manifest do app e dos SDKs | V-17 |
| 10 | Purpose string específica e localizada por recurso protegido | V-58 |
| 11 | Metadados que não podem ser alterados após o envio, revisados | V-73 |
| 12 | Build validado no Xcode e presente no TestFlight (requer macOS) | V-73 |

Exemplo de aplicação a um app novo (SwiftUI, login por e-mail e Google, foto de perfil pela câmera, Firebase Analytics): faltam `NSCameraUsageDescription` (risco de ITMS-90683), exclusão de conta no app (5.1.1(v)); avaliar 4.8 por causa do login Google (o login próprio por e-mail pode atender; não afirme violação); conferir `PrivacyInfo.xcprivacy` do app e do SDK do Firebase e os motivos de required reason APIs; fornecer conta de demonstração (2.1).

## Privacy manifest e purpose strings

- **Privacy manifest** (V-17): `PrivacyInfo.xcprivacy` descreve dados coletados (todas as plataformas) e uso de "required reason APIs" (iOS, iPadOS, tvOS, visionOS, watchOS). Não é "obrigatório para todo app": depende de coleta de dados e de uso dessas APIs, e vale para SDKs de terceiros que estejam na lista da Apple ou que usem required reason API, coletem dados, permitam coleta pelo app ou contatem domínios de rastreamento. Para cada API, `NSPrivacyAccessedAPITypes` com o motivo.
- **Purpose strings** (V-58): o sistema pede permissão na primeira tentativa de acesso e lembra a escolha; a string não pode ser vazia, deve ter menos de 4.000 bytes, descrever com exatidão e especificidade o motivo, em geral uma frase completa. Sem string, o acesso falha e o app pode cair; a App Review rejeita código que referencia APIs protegidas sem a string (ITMS-90683), inclusive por SDKs de terceiros, e o desenvolvedor responde por eles. Localize com `InfoPlist.xcstrings`. `NSLocationWhenInUseUsageDescription` é obrigatória para localização em uso e `NSLocationAlwaysAndWhenInUseUsageDescription` para segundo plano. Chaves além de câmera e localização (fotos, microfone, Bluetooth, ATT) não foram conferidas uma a uma (lacuna 6).

## Sequência de release iOS

Fonte: V-73 (documentação do Xcode). Sete passos, com a marcação de onde o macOS e o usuário entram.

| # | Passo | macOS | Ação do usuário |
| --- | --- | --- | --- |
| 1 | Apple Developer Program ativo (a Apple cria a conta do App Store Connect) | Não | Sim |
| 2 | Criar o registro do app no App Store Connect antes do primeiro envio | Não | Sim |
| 3 | `Product > Archive` | Sim (Xcode) | — |
| 4 | "Validate App" | Sim | — |
| 5 | "Distribute App" (TestFlight & App Store, TestFlight Internal Only, Release Testing...) e upload | Sim | Confirmar |
| 6 | TestFlight: beta interno e externo; relatórios de falha e feedback no Organizer | Parcial | Convidar testadores |
| 7 | Enviar a última build do TestFlight para o App Review e conferir metadados imutáveis | Não | **Sempre do usuário** |

O Xcode gerencia certificados de assinatura na nuvem. TestFlight Beta App Review em detalhe, provisionamento e App Store Connect API não foram cobertos (lacuna 11).

## Checklist Google Play

| Item | Regra | Fonte |
| --- | --- | --- |
| Target API | A partir de 2026-08-31, novos apps e atualizações de celular e tablet devem targetar API 36; Wear OS e Automotive API 35; TV e XR API 34; apps existentes API 35 para continuar visíveis a novos usuários em aparelhos mais novos; extensão até 2026-11-01 (formulário no Play Console); isenção para apps privados de organização. **O prazo principal já passou em 2026-10-10**; página marcada "Last updated 2026-10-01"; reconfira antes de afirmar | V-14 |
| Exclusão de conta | Caminho dentro do app, link web funcional, perguntas de exclusão no Data safety, cobertura dos dados do Data safety e dos provedores, passos extras (cancelar assinatura) explicados, retenção divulgada. Apps não móveis (TV, Wear) estão dispensados do caminho no app. A página **não** diz que "desativar conta não conta como exclusão" | V-15 |
| Data safety e política de privacidade | Coerentes com o código | V-13 |
| Permissões de alto risco e conta de demonstração | Justificadas e disponíveis | V-13 |
| Localização em segundo plano | Só se for necessária à funcionalidade central, nunca só para anúncio ou analytics; formulário (apps com `ACCESS_BACKGROUND_LOCATION` que targetam Android 10+); vídeo de 30 s ou menos é recomendação; divulgação em destaque dentro do app com o termo "location", indicação de uso em segundo plano (frases como "quando o app está fechado") e lista de funcionalidades; sem botão de aceitar obrigatório. Nova declaração ao mudar a funcionalidade. Sem data na página: reconfira | V-57 |
| Trilhas | Interna, fechada, aberta, produção; trilha interna antes de produção | V-35 |

`play-policy-insights` (V-13) audita em permissões/APIs, conta e identidade, Data safety e privacidade, mas executa scripts Python do repositório: o plugin não os executa e destila só o checklist.

## Gates de confirmação

Modelo de V-34, estendido por V-35, V-71, V-72 e V-73. Efeitos externos exigem uma **ficha de ação** (`assets/templates/ficha-acao-release.md`) confirmada por texto do usuário no chat:

- Conta, plataforma(s), app, build ID, canal e branch, ambiente, `runtimeVersion`, perfil de build, mensagem.
- Comandos exatos com versões fixas (nenhum `@latest`, nenhum instalador).
- Efeitos esperados, rollback conhecido (ou "a fonte não descreve rollback") e o que é ação do usuário.

Exigem confirmação nomeada: `eas update` em produção, `eas submit`, `--auto-submit`, atalho de TestFlight, `fastlane pilot` com distribuição, promoção de trilha e qualquer criação, revogação ou `match nuke` de certificados. "Submit for Review" no App Store Connect é sempre do usuário. Segredos (`MATCH_PASSWORD`, chaves de API, contas de serviço) nunca em chat, repositório nem log. Produção nunca é inferida pelo branch do git.

## Pipelines: EAS, fastlane, Xcode Cloud, Gradle

| Ferramenta | Fatos verificados | Cuidados |
| --- | --- | --- |
| EAS Update (V-34) | OTA para JS, estilo e assets; `runtimeVersion` como fronteira; canal na build aponta para branch | Fonte não descreve rollback; `allowed-tools` original amplo |
| EAS Build / Submit (V-35, V-75) | Build iOS em macOS runners da Expo; EAS gerencia keystores Android e credenciais iOS ou usa as suas; `eas build --local` roda na sua máquina; monitorar com `eas build:list` e `eas submit:list` | A página não diz "sem Mac" nem exige conta Apple (implícito); sem preço nem fila; submissão sem gate no original |
| fastlane `match` (V-71) | Armazenamento em Git privado, GCS ou S3; "recomenda-se sempre usar `readonly` em CI"; senha por `MATCH_PASSWORD`; `nuke` revoga certificados e perfis e desativa builds Ad Hoc e Enterprise (exige confirmação); o caminho dos perfis mudou no Xcode 16 | A página não diz "requer macOS" literalmente; cita Keychain e caminhos de `~/Library`, o que implica macOS (Inferido) |
| fastlane `pilot` (V-72) | `upload` acha o `.ipa`; `skip_submission` envia sem distribuir (padrão `false`, ou seja, **distribui por padrão**); chave da API do App Store Connect é a autenticação preferida; papel "App Manager" ou "Admin" atualiza build e testadores, "Developer" só envia; há seção "Upload from Linux" que exige Transporter | Produzir o `.ipa` exige Xcode em macOS (V-73) |
| Xcode Cloud (V-74) | Workflows a cada commit, testes em paralelo, TestFlight; 25 h de computação por mês incluídas no Developer Program; pacotes pagos listados na página (preços datados: reconfira) | Página não informa versão de macOS ou Xcode; configuração normalmente pelo Xcode ou App Store Connect (Inferido) |
| Gradle Play Publisher (V-76) | Conta de serviço no Google Cloud com a API do Android Publisher; primeiro upload manual no Play Console; plugin por módulo `com.android.application` | Modo de manutenção, projeto independente, versões mínimas de Gradle/AGP não informadas |
| E2E no EAS (V-37) | Job Maestro em alfa; perfil `e2e-test` sem credenciais | Alfa pode mudar |

Custo e infra de runners macOS pertencem a `/devops-cloud-infra:playbook`; versionamento e branches a `/git-workflow-release:playbook`.

## Usuário em Windows sem macOS

Nota para o ambiente deste projeto (V-74, V-75, V-77, V-84):

| Dá para fazer em Windows | Exige macOS | Alternativa |
| --- | --- | --- |
| Alvo Android completo (Gradle, emulador); lógica comum de KMP e de RN/Flutter | Xcode, Instruments, simulador iOS | Revisão por leitura; marcar Não verificável |
| Revisar código Swift e SwiftUI, concorrência, acessibilidade por leitura | Archive, validação e upload local, `fastlane match` | EAS Build (Expo) ou Xcode Cloud (nativo); distribuição exige credenciais Apple (Inferido) |
| Orquestrar EAS Build/Submit e Xcode Cloud com ficha confirmada | Alvo iOS de KMP (V-84) | Mac alugado ou próprio, ação do usuário |

Regra: nunca diga que o app iOS compilou, passou nos testes ou foi enviado sem a saída correspondente na sessão (snippet S-02). A divisão exata do que compila em Windows em KMP e o fluxo "EAS Build sem Mac" são Inferido.

## Trabalhar pelo celular

V-77 (reconfira, o produto muda): o app Claude (iOS e Android) é cliente de sessões; o código não roda no celular. Caminhos: sessões na nuvem (repositório no GitHub), Remote Control (sessão na sua máquina, que precisa ficar ligada), projetos e Dispatch (Pro ou Max). Exige conta claude.ai; `/plugin` e `/resume` não funcionam no app; Bypass permissions não é selecionável por ele. A combinação com EAS Build ou Xcode Cloud para ter iOS "do celular" é raciocínio do plugin (Inferido).

## Notas de versão

Rascunho em arquivo, nunca enviado à loja (V-24, reescrito): triagem em Novo, Melhorado e Corrigido; cinco a dez bullets; validar cada bullet contra o diff; remover detalhes internos antes de colar em nota pública; ler qualquer script de coleta antes de usá-lo e nunca executar o de terceiros sem autorização. Template: `assets/templates/notas-de-versao.md`.

## Relatório de revisão de loja

Formato de V-38 (rshankras/claude-code-apple-skills, MIT): somente leitura (`Read, Glob, Grep`); fases descoberta, segurança, privacidade, UX, distribuição, API; tabela por prioridade com arquivo:linha, impacto, código atual, correção, pontos fortes e plano de ação. Suavize "Must Fix": use "risco provável de rejeição". Contagem "25 itens em 5 áreas" não é sustentada. Template: `assets/templates/relatorio-revisao-mobile.md`.

## Lacunas

App Store Connect Help (TestFlight Beta App Review, provisionamento), `fastlane deliver`, versão de Xcode do Xcode Cloud, versões mínimas do Gradle Play Publisher, alternativas oficiais de publicação Android, IAP e StoreKit/Play Billing além da guideline 3.1.1 e crash reporting não têm fonte lida. Pagamentos pertencem a `/fintech-payments:playbook`; crash reporting a `/sre-observability:playbook`.
