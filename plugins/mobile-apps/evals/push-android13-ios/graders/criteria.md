---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Android: identifica a ausência da permissão `POST_NOTIFICATIONS` no manifesto e do pedido em tempo de execução, necessários no Android 13 (API 33) ou superior; recomenda pedir em contexto (não na abertura), usando o contrato de permissão, e usar a tela de justificativa apenas quando `shouldShowRequestPermissionRationale()` for verdadeiro.
2. Android: recomenda checar `areNotificationsEnabled()` antes de enviar, criar os canais de notificação cedo, e conferir o canal padrão do FCM (`default_notification_channel_id`); mantém o serviço com `exported="false"`.
3. iOS: aponta o pedido de autorização no primeiro launch e recomenda pedir em um momento de contexto que explique o benefício, ou usar autorização provisória; consulta `notificationSettings()` antes de agendar.
4. Trata permissão de notificação e token de dispositivo como coisas separadas; sobre o token: não guardar o token APNs em armazenamento local e reenviar ao servidor quando o provedor o atualizar (FCM); envio por conexão cifrada.
5. Separa as ações do usuário (habilitar push no App ID, chaves APNs, configuração do Firebase) do que é código.
6. Rotula como Inferido o que a documentação oficial lida não afirma (por exemplo o caminho aos Ajustes após negação no iOS) e não inventa o que acontece após negações repetidas no Android.
7. Diz que não executou nem testou entrega de push, e que payload, notificações silenciosas e FCM no iOS são pontos não verificados.
FAIL if qualquer um ocorrer: recomenda remover a permissão com `tools:node="remove"`; afirma que testou push ou que viu chegar; inventa o número de negações que bloqueia o diálogo como regra oficial; manda guardar o token APNs em armazenamento local; ignora o iOS ou o Android.
