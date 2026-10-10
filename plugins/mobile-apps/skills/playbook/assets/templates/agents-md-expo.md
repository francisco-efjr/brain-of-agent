# Modelo de AGENTS.md para projeto Expo

Redação própria a partir do guia da Expo para Claude Code e do template `create-expo` (V-36; o template é MIT, aqui destilado). O Claude Code lê `AGENTS.md` diretamente a partir da versão 2.1.277 (verificado em 2026-10-10; confira com `claude --version`). Em versões anteriores, referencie o arquivo a partir do `CLAUDE.md`. Copie o bloco abaixo para a raiz do projeto, preencha os valores entre colchetes e remova as linhas que não se aplicam (teste de remoção).

````markdown
# [NomeDoApp]

App Expo ([versão do SDK, lida de package.json]) com TypeScript e Expo Router.

## Antes de sugerir qualquer API
- Leia a versão major de `expo` no package.json e use a documentação dessa versão. APIs mudam por SDK.
- Instale dependências com `npx expo install`, que casa as versões com o SDK. Não use `npm install` direto para pacotes do ecossistema Expo.

## Verificação (rode antes de declarar pronto e cole a saída)
- `npx expo lint`
- `npx tsc --noEmit`
- `npx expo-doctor`
- Para alinhar versões após atualizar o SDK: `npx expo install --fix`
- Testes: [comando do projeto, ex.: `npx jest`]

## Estrutura
- Telas em `[src/app/ ou app/]` (Expo Router). Leia a estrutura atual antes de criar rotas; deve existir rota para `/`.
- Nomes de rota em kebab-case; modais com `presentation: "modal"`.
- No SDK 56 ou superior, importe de `expo-router/react-navigation`.

## Código nativo
- Não edite `ios/` nem `android/` à mão.
- Módulo nativo exige development build; o Expo Go não basta.
- Build, submissão e OTA usam EAS.

## Efeitos externos (só com confirmação que nomeie conta, app, build e canal)
- `eas update` em produção, `eas submit`, `--auto-submit`, atalho de TestFlight.
- OTA leva só JavaScript, estilo e assets. Mudança nativa exige nova build. `runtimeVersion` não muda por conveniência.
- Nunca infira produção pelo branch do git.

## Ambiente
- [Windows/macOS/Linux]. Xcode, simulador iOS e assinatura exigem macOS: sem macOS, marque como Não verificável. Build iOS na nuvem via EAS Build (ação do usuário).

## Segurança
- Nenhum segredo no cliente. Tokens em armazenamento seguro da plataforma (Keychain/Keystore), não em armazenamento simples.
````

Notas de uso:

- O plugin `expo@claude-plugins-official` (skills e MCP da Expo) é opcional e documentado em `references/ferramentas-e-mcp.md`; este plugin não o instala.
- "SecureStore" e outras bibliotecas específicas não aparecem no modelo porque a base não leu a documentação delas; acrescente o que o projeto usa.
- Estrutura `app/` ou `src/app/`: o template da Expo usa `src/app/`; ambas existem, siga o projeto.
