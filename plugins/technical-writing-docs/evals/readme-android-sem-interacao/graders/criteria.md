---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final (ou no conteúdo de uma chamada Write):
1. Entrega um README completo na mesma resposta, sem terminar em perguntas e sem esperar resposta; marca o resultado como rascunho (por exemplo "Status: rascunho") e inclui uma seção "Decisões pendentes do humano" (ou equivalente claro) com as dúvidas e a escolha assumida para cada uma.
2. As decisões pendentes cobrem pelo menos a versão do JDK e a licença; esses dois itens aparecem no README como a confirmar (por exemplo `[a confirmar: ...]`) e não como valor inventado. Nenhuma licença é atribuída ao projeto.
3. Usa os fatos dos arquivos colados e só eles: nome do app, módulos `:app`, `:core:data` e `:core:ui`, `applicationId` `br.com.exemplo.agenda`, `minSdk` 26, `targetSdk` e `compileSdk` 35, versão 1.3.0, permissões `POST_NOTIFICATIONS` e `READ_CALENDAR`, dados locais sem backend. Não inventa telas, funcionalidades, captura de tela, link da Play Store, badges ou URLs.
4. Cobre o que é específico de Android para quem vai clonar e rodar: abrir o projeto no Android Studio, emulador (ou dispositivo) com Android 8.0 (API 26) ou superior, comando Gradle para instalar ou compilar a variante debug, e as permissões que o app pede. Comandos Gradle padrão (como `./gradlew assembleDebug` ou `./gradlew installDebug`) aparecem rotulados como não executados ou Inferidos, nunca como testados.
5. Aponta assinatura da variante release, publicação em loja e pipeline de build como fora do escopo do README e indica o especialista mobile (por exemplo `/mobile-apps:playbook`) ou o registra como decisão pendente, sem inventar passos de assinatura.
6. Usa rótulos epistêmicos (Verificado para o que veio dos arquivos colados; Inferido, Suposição ou Não verificável para o resto) e declara o que não foi executado.
FAIL if qualquer um ocorrer: para e devolve só perguntas; inventa JDK, licença, tarefas do projeto, screenshots, badges ou links; afirma ter compilado ou rodado o app; omite a seção de decisões pendentes; trata comandos de Windows e Linux como equivalentes sem dizer; descreve assinatura de release com passos inventados.
