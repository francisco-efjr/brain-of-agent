# Dados, push, permissões, deep links e segurança

Verificado em 2026-10-10. Fontes: V-25, V-40, V-45, V-52 a V-61, V-82, V-83 e o brain-of-agent (`qa/mobile.md`, MIT). Muitos passos dependem de contas Apple, Google e Firebase e de hospedagem de arquivos: o agente audita e prepara, o usuário executa (ação do usuário). Contratos de servidor (envio de push, API) pertencem a `/backend-api:playbook`.

## Sumário

- [Offline-first e sincronização](#offline-first-e-sincronização)
- [Push](#push)
- [Permissões](#permissões)
- [Deep links](#deep-links)
- [Armazenamento seguro e MASVS](#armazenamento-seguro-e-masvs)
- [Lacunas](#lacunas)

## Offline-first e sincronização

### Perguntas de projeto antes de codar

1. Quais dados ficam disponíveis offline e por quanto tempo?
2. Pode haver edição concorrente (celular e tablet, vários usuários)? Qual a política de conflito?
3. Qual a latência aceitável até o servidor refletir a mudança?
4. Alguma operação tem efeito financeiro ou irreversível que exija identidade de operação?

Sem respostas, assuma explicitamente e rotule Suposição (V-45 reescrito).

### Desenho (V-59, guia oficial Android, classe A)

- A **fonte local é a canônica** e a única que as camadas superiores leem; leituras expostas como tipos observáveis.
- Modelos separados de **rede, entidade e externo**, com mapeadores (a página usa `NetworkAuthor`, `AuthorEntity`, `Author`).
- Room para dados estruturados; DataStore para não estruturados.
- Escrita por tipo de dado: **online-only** (rede primeiro, depois local), **enfileirada** (fila drenada com backoff exponencial ao voltar a rede) ou **preguiçosa** (local primeiro, rede o quanto antes).
- Sincronização **pull**, **push** (réplica local) ou **híbrida**.
- Conflito: "há muitas estratégias"; "last write wins" é descrita como abordagem comum em mobile (timestamp no registro e a rede descarta dados mais antigos que o estado atual). É opção, não norma.
- O backoff exponencial está na página (leitura, fila de escrita e `Result.retry()` do WorkManager) sem valores numéricos nem limite de tentativas. A fila é só esboçada: ordem firme exige Room ou DataStore.

### Checklist de 7 itens

1. Fonte local única e leitura reativa.
2. Escrever local primeiro (quando o tipo de dado permite).
3. Estratégia de escrita escolhida por tipo de dado.
4. Timestamp ou versão no registro.
5. Fila persistente, recarregada na inicialização, ordenada, processada em série e idempotente.
6. Indicador de offline e nenhum sucesso fictício.
7. Teste de transição de rede (sem rede, volta da rede, interrupção no meio do envio).

Alertas do plugin (Inferido): hora local de dois aparelhos não dá uma ordem confiável; "última escrita vence" precisa dizer qual relógio ou versão manda, de preferência a do servidor; esperar sincronização indefinidamente é um defeito observável.

### Por que não copiar o checklist de terceiros (V-45)

O exemplo do skill da secondsky tem bugs confirmados: a fila não é recarregada do armazenamento na inicialização (e sobrescreve a fila salva); o listener de rede dispara processamento concorrente (reenvio duplicado e sobrescrita; o risco principal é duplicação, "perda" é parcial); descarta o item mais antigo acima de 1000. Use apenas a lista reescrita acima. Template: `assets/templates/plano-offline-sync.md`.

### WorkManager (V-60, classe B)

Para trabalho adiável que precisa sobreviver ao fechamento do app. Por worker: idempotente, nome único (evita duplicação), restrição de rede declarada, `retry` com política. Horário exato é outro mecanismo (conferir na documentação de alarmes; a página de introdução não os cita). Em Doze o WorkManager espera a janela de manutenção (V-63). Restrições e backoff não foram lidos (lacuna 8).

### SwiftData com CloudKit (V-61)

Duas capabilities: iCloud com CloudKit e contêiner; Background Modes com Remote notifications. Exige conta de desenvolvedor ativa com permissão de administrador. Limitações: sem `unique`, relacionamentos opcionais, regra `deny` não suportada, inverso explícito quando não inferível. O esquema de desenvolvimento é inicializado manualmente (build DEBUG) e promovido a produção antes do lançamento; o esquema de produção **só aceita adições** (sem apagar tipos nem alterar atributos). `ModelConfiguration(cloudKitDatabase: .private(...))` escolhe o contêiner; `.none` desliga a sincronização. **Conflito: a página não descreve resolução; "último gravador vence" é Suposição e não entra como fato.** Passos com Xcode e conta Apple são macOS e ação do usuário.

### Rede e operações ambíguas (brain `qa/mobile.md`)

Timeout no cliente não prova falha no servidor. Exemplo sintético: transferência de R$ 10,00 em sandbox, saldo inicial R$ 100,00, identificador `op-qa-001`; o servidor efetiva e a resposta não chega. Ao reconectar, a UI consulta e reconcilia pela identidade da operação. Oráculo: uma transferência, saldo R$ 90,00, comprovante da mesma operação, nenhuma segunda cobrança. "Apareceu uma mensagem de erro" não valida integridade financeira. Outros casos: token expira durante a sincronização (refresh coordenado, fila preservada); conflito com edição em outro aparelho (regra de versão, merge ou recusa, sem perda invisível); resposta antiga depois de consulta nova (a UI não retrocede); troca de Wi-Fi para dados móveis (estado consistente, sem laço de requisições); relógio local errado (fonte de tempo definida).

## Push

### iOS: APNs (V-52) e autorização (V-53)

Checklist de 6 itens:

1. Capability Push Notifications presente (adiciona o entitlement `aps-environment`).
2. Serviço de push habilitado no App ID da conta (**ação do usuário**: o agente não faz).
3. Registrar e receber o token **a cada launch**; o token é único por dispositivo e por app.
4. Tratar sucesso e falha (rede, APNs inalcançável, entitlement ausente) marcando e tentando de novo.
5. Enviar o token ao servidor por conexão cifrada, **sem cache local** (o token muda após restauração de backup, aparelho novo ou reinstalação) e sem log em texto.
6. Prever vários aparelhos por usuário.

Autorização (V-53): peça com as opções realmente usadas (`.alert`, `.sound`, `.badge`, opcional `.provisional`); o primeiro pedido exibe o diálogo e os seguintes não; pedir em contexto que explique o benefício (exemplo da página: depois do primeiro item criado) funciona melhor que no primeiro launch; `.provisional` entrega em silêncio, só na central de notificações, com botões Manter e Desativar, e permite pedir no primeiro launch porque não exibe diálogo; consulte `notificationSettings()` antes de agendar notificação local. **A página não trata de negação**: oferecer caminho alternativo ou atalho para Ajustes sem insistir é Inferido.

### Android: permissão (V-54) e FCM (V-55)

Checklist de 6 itens para FCM e permissão:

1. `POST_NOTIFICATIONS` declarada no manifesto e pedida em execução com `SDK_INT >= 33` e o contrato `RequestPermission`; em instalação nova no Android 13+ as notificações começam desligadas. O SDK do FCM 23.0.6+ declara a permissão, mas o pedido em execução continua com o app.
2. Tela de justificativa só quando `shouldShowRequestPermissionRationale()` for verdadeiro; `areNotificationsEnabled()` antes de enviar.
3. Serviço que estende `FirebaseMessagingService` com filtro `com.google.firebase.MESSAGING_EVENT` e `exported=false` (necessário para notificações em primeiro plano e payloads de dados).
4. Canal padrão via meta-data `default_notification_channel_id` (Android 8+); canais por tipo de aviso, **criados cedo** (para apps que targetam 12L ou inferior, um canal criado em segundo plano pode adiar o diálogo e notificações recebidas antes de aceitar "serão perdidas").
5. Token ou Firebase Installation ID: a seção do token de registro da página está marcada como depreciada e recomenda Installation IDs; reenvie ao servidor no callback sempre que o provedor atualizar.
6. Payload com dados suficientes; **nunca** remova a permissão com `tools:node="remove"` se o app usa notificações (bloqueia todas, não só as do FCM).

Isenções do Android 13 (V-54): sessões de mídia e `Notification.CallStyle` quando o app declara `MANAGE_OWN_CALLS`, implementa `ConnectionService` e chama `registerPhoneAccount()`. Notificações negadas de serviço em primeiro plano ainda aparecem no Gerenciador de Tarefas.

### Cross-platform

Permissão e token são coisas separadas. Conflito aparente entre APNs ("não guardar o token") e FCM (token ou FID salvo) é só de provedor: regra comum é reenviar ao servidor sempre que o provedor atualizar e não persistir o token APNs localmente (C4). Receber e tocar na notificação são eventos distintos: teste conteúdo na tela bloqueada, destino correto, ação duplicada, item removido e usuário que já saiu da conta; separe o teste do handler da entrega real (brain). Payload de envio, notificações silenciosas (`content-available`) e FCM no iOS não foram lidos (lacuna 5). Em RN e Flutter, push e permissões passam por módulos nativos (Inferido).

## Permissões

### iOS (V-58)

Inventarie as APIs protegidas no código e nos SDKs; uma chave `NS*UsageDescription` por recurso, com frase específica e localizada; verifique o status antes de cada uso (o usuário pode mudar nos Ajustes); trate falha de acesso quando não há API dedicada; peça no momento da necessidade e prepare fallback. "Reset Location & Privacy" reinicia permissões do aparelho de teste e afeta todos os serviços. Liga com 5.1.2 (V-16) e com o privacy manifest (V-17).

### Android (V-56)

Fluxo: `checkSelfPermission` a cada uso; `shouldShowRequestPermissionRationale()` para UI educativa; pedir pelo contrato `RequestPermission` (recomendado); tratar o resultado. O diálogo do sistema não é personalizável. Na negação: minimizar a perda de função, ser específico, não bloquear a UI e não pressionar (o exemplo da página comenta que não se deve apontar às configurações para convencer o usuário). Negar "mais de uma vez" encerra o diálogo no texto normativo; só a seção de depuração diz "duas vezes" (`USER_FIXED`). Comandos de depuração (`adb shell dumpsys package <pacote>`, `pm clear-permission-flags`) alteram flags do aparelho de teste: use em emulador.

### Localização em segundo plano (V-57)

Checklist de 6 itens (datar "verificado em 2026-10-10"): função central comprovada; tentar primeiro em primeiro plano; formulário de declaração; vídeo curto (recomendação de 30 s); divulgação in-app com o termo "location" e a lista de funcionalidades; nova declaração ao mudar a funcionalidade.

### Cenários de teste (brain)

Para cada permissão realmente usada: primeira solicitação, recusa, aceite, mudança nas configurações e retorno ao app; acrescente concessão temporária ou parcial se existir na combinação SO/API. O esperado distingue a função bloqueada das que continuam. Câmera e documentos: recusa não fecha o app; cancelamento volta ao fluxo; captura inválida não passa como anexo aceito. Biometria: sucesso, cancelamento, indisponibilidade e fallback; simular sucesso testa a reação do app, não a segurança do sensor. Sessão: expiração em segundo plano, logout, revogação, troca de conta, aparelho compartilhado; token nunca em log, vídeo ou relatório.

## Deep links

Checklist duplo (V-40, classe B); datar e conferir nas páginas oficiais.

| Plataforma | Checklist |
| --- | --- |
| Android (App Links) | `android:autoVerify="true"` em intent-filter com VIEW, BROWSABLE e DEFAULT e esquema http(s); `assetlinks.json` em `/.well-known/` para **cada host**; verificação assíncrona (esperar pelo menos 20 s); `adb shell pm get-app-links` e `pm verify-app-links --re-verify` (somente emulador, em referência); Android 15+ reverifica periodicamente (até sete dias) |
| iOS (Universal Links) | Arquivo `apple-app-site-association` em `/.well-known/`, sem extensão, HTTPS válido, **sem redirecionamento**; entrada `applinks:dominio` sem caminho nem barra final; cada subdomínio com entrada e arquivo próprios |

Regra de segurança: valide host, caminho e parâmetros de todo link recebido e peça confirmação antes de ação sensível; abrir uma rota não concede autorização sobre o objeto. Teste app fechado, em segundo plano e aberto; sessão ausente; parâmetro inválido; recurso inexistente; recurso de outra conta (brain). Não confirmados em página oficial: limite de 128 KB e regra "sem redirecionamento" no Android; a impressão digital da assinatura do Play App Signing é prática correta, mas Inferido aqui (conferir na doc do Play). Hospedagem de `assetlinks.json` e AASA é ação do usuário. Deep links no Expo Router e na camada Flutter não têm fonte.

## Armazenamento seguro e MASVS

### Android Keystore (V-82)

O material da chave nunca entra no processo do app e é não exportável; pode ficar em hardware seguro (TEE ou Secure Element) se o aparelho suportar o algoritmo; StrongBox no Android 9+ (API 28); nível de segurança por `KeyInfo.getSecurityLevel()` (API 29+) ou `isInsideSecurityHardware()` (API 28 e inferior); autenticação do usuário com `BiometricPrompt` e `setUserAuthenticationParameters()` (com `canAuthenticate()`); chave só biométrica é invalidada por padrão ao cadastrar nova biometria (`setInvalidatedByBiometricEnrollment(false)` muda); `KeyChain` para credenciais de sistema aprovadas pelo usuário. Com o SO comprometido o atacante pode usar as chaves, mas não extraí-las. "Evitar `SharedPreferences` para segredos" é Inferido.

### Keychain (V-83)

`kSecAttrAccessible` na criação define a acessibilidade; ordem de restrição decrescente: When Passcode Set (o item some se o código for removido), When Unlocked (padrão), After First Unlock (acesso em segundo plano), Always ("não recomendada", não "depreciada"). Use sempre a opção mais restritiva que faça sentido. O sufixo `ThisDeviceOnly` restaura no mesmo aparelho do backup e não migra; para dados muito sensíveis, `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly`; para exigir presença do usuário, `SecAccessControl` com `userPresence` (ou biometria específica); `applicationPassword` pede senha própria. Item sincronizável só aceitar variantes sem `ThisDeviceOnly` é Inferido. Metadados protegidos pelo Secure Enclave vêm de outra fonte não aberta.

### Regras

Segredo ou chave de serviço **nunca** no cliente: binários são inspecionáveis. Token em Keychain ou Keystore, não em `UserDefaults`, `SharedPreferences` ou arquivo (Inferido para o "evitar"; base em V-25, V-82, V-83). Logs, vídeos e traces sem token nem dados pessoais (S-18).

### MASVS por grupo (V-25)

Os oito grupos são os verificados; as linhas "o que verificar" são conhecimento estável do plugin (Inferido). Não cite níveis L1/L2/R nem IDs de controle: a base não os leu e o MASTG não foi aberto.

| Grupo | O que verificar no app |
| --- | --- |
| MASVS-STORAGE | Dados sensíveis em repouso: onde o token mora, o que vai para backup, logs, cache, capturas de tela |
| MASVS-CRYPTO | Chaves no Keystore/Keychain, sem chaves embutidas; algoritmos padrão em vez de cripto própria |
| MASVS-AUTH | Sessão, expiração, logout, revogação, autenticação local (biometria) para ações sensíveis |
| MASVS-NETWORK | TLS, exceções de ATS e da configuração de segurança de rede, validação de certificado |
| MASVS-PLATFORM | Deep links, intents, componentes exportados, WebViews, permissões |
| MASVS-CODE | Dependências atualizadas, entradas validadas, builds de release sem depuração |
| MASVS-RESILIENCE | Proteções contra adulteração, quando o modelo de ameaça as exige |
| MASVS-PRIVACY | Dados coletados, finalidade, consentimento, manifesto de privacidade, Data safety |

Threat modeling, pentest e supply chain ficam com `/security-appsec:playbook`.

## Lacunas

Payload e notificações silenciosas, FCM no iOS, chaves de privacidade além de câmera e localização, conflito do CloudKit, restrições e backoff do WorkManager, níveis e controles do MASVS e MASTG, push e permissões via módulos de RN/Flutter. Reabra a fonte antes de afirmar.
