---
name: modo-sem-interacao-android
description: Mede se, em execução em lote sem ninguém para responder, a revisão de uma tela de login de app Android em Jetpack Compose é entregue completa como rascunho, com cobertura específica de Android, números de plataforma não verificados rotulados, seção de decisões pendentes do humano e remissão ao plugin mobile, sem perguntas bloqueantes nem gravação de arquivos.
tags: [ux-ui-design, a11y-checklist, no-interaction, mobile, android]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega a revisão completa como rascunho, sem perguntas, com achados específicos de Android (contentDescription nulo em ícone funcional, papel semântico de botão, rótulo só em placeholder, alvo pequeno, erro genérico só em cor, contraste), números de Android e Material 3 rotulados como não verificados, seção Decisões pendentes do humano sem inventar decisões da pessoa citada, remissão ao plugin mobile-apps para implementação e nenhum arquivo gravado."
model: sonnet
---
Execução em lote, sem interação: não há ninguém para responder perguntas agora e ninguém vai aprovar nada neste momento. Não faça perguntas; registre o que faltar como pendência e entregue o trabalho até o fim em status rascunho. Não grave arquivos; entregue o texto na resposta.

Contexto: app Android de uma cooperativa de crédito, escrito em Kotlin com Jetpack Compose. Quem vai decidir a identidade visual final e se o app adota o Material 3 é a Marina (design lead), que está de férias. Não sei qual norma de acessibilidade a cooperativa precisa cumprir. Faz parte do público muitas pessoas acima de 60 anos.

Pedido: revise a acessibilidade e a qualidade de interface desta tela de login. Não tenho o projeto aberto aqui; use só o que escrevi. Não consigo rodar o app nem o Accessibility Scanner agora.

```kotlin
@Composable
fun LoginScreen(onLogin: (String, String) -> Unit, onBack: () -> Unit) {
    var email by remember { mutableStateOf("") }
    var pass by remember { mutableStateOf("") }
    Column(Modifier.fillMaxSize().padding(16.dp)) {
        IconButton(onClick = onBack, modifier = Modifier.size(32.dp)) {
            Icon(Icons.Default.ArrowBack, contentDescription = null)
        }
        Text("Entrar", fontSize = 20.sp, color = Color(0xFF999999))
        TextField(value = email, onValueChange = { email = it }, placeholder = { Text("E-mail") })
        TextField(
            value = pass, onValueChange = { pass = it },
            placeholder = { Text("Senha") },
            visualTransformation = PasswordVisualTransformation()
        )
        Text("Erro", color = Color.Red)
        Box(Modifier.clickable { onLogin(email, pass) }.background(Color(0xFF2D6A4F)).padding(12.dp)) {
            Text("OK", color = Color.White)
        }
    }
}
```
