# Checklist Google Play de pré-submissão

Verificado em 2026-10-10. Fontes oficiais: target API (V-14, https://developer.android.com/google/play/requirements/target-sdk, página marcada "Last updated 2026-10-01"), exclusão de conta (V-15, https://support.google.com/googleplay/android-developer/answer/13327111), localização em segundo plano (V-57, https://support.google.com/googleplay/android-developer/answer/9799150), auditoria `play-policy-insights` (V-13, Apache-2.0, usada só como modelo de checklist; seus scripts Python não são executados). Redação própria. Padrões de Grep e itens marcados **Inferido** são conhecimento estável do domínio.

| # | Item | Fonte | Como detectar | Correção mínima |
| --- | --- | --- | --- | --- |
| A1 | `targetSdk` atende ao prazo | V-14 | Nativo: Grep `targetSdk` em `app/build.gradle(.kts)`. Expo: `android.targetSdkVersion` do `expo-build-properties` em `app.json`/`app.config.*`. Flutter: `android/app/build.gradle(.kts)` (muitas vezes `flutter.targetSdkVersion`, resolvido pela versão do Flutter: **Inferido**) | Elevar para a API exigida ou registrar a extensão aprovada no Play Console |
| A2 | Exclusão de conta dentro do app e link web | V-15 | Mesmos Grep do item 1 de iOS; procure a URL de exclusão na política/ficha | Caminho no app + link web funcional + perguntas de exclusão respondidas no Data safety |
| A3 | Data safety coerente com o código e a política de privacidade | V-13 | Inventário do passo 2 (SDKs, permissões, endpoints) comparado com a declaração e `PRIVACY.md`/URL | Corrigir a declaração ou o código; o preenchimento no console é ação do usuário |
| A4 | Localização em segundo plano | V-57 | Grep `ACCESS_BACKGROUND_LOCATION` em manifestos (inclusive de dependências, via manifest merge) | Ver subitens abaixo |
| A5 | Permissões de alto risco | V-13 (nível geral); lista **Inferido** | Grep `READ_SMS\|RECEIVE_SMS\|READ_CALL_LOG\|QUERY_ALL_PACKAGES\|MANAGE_EXTERNAL_STORAGE\|ACCESS_BACKGROUND_LOCATION\|SYSTEM_ALERT_WINDOW\|REQUEST_INSTALL_PACKAGES` | Remover o que não é central ou preencher a declaração/justificativa exigida pelo Play |
| A6 | Conta de demonstração | V-13 | Notas de acesso do app no console (sem evidência no código) | Credenciais de teste válidas e backend ativo. Ação do usuário |
| A7 | Trilha de teste antes de produção | V-35, V-76 | `eas.json` (submit), `fastlane/Fastfile`, `play { track ... }` no Gradle | Interna ou fechada primeiro; promoção de trilha só com confirmação (ver `mobile-release-pipeline`) |
| A8 | Pacote em formato AAB | conhecimento estável (**Inferido**) | `bundleRelease` vs `assembleRelease` em scripts de CI; `eas.json` com `buildType: "app-bundle"` | Publicar `.aab` para a loja |

## A1: valores de target API (V-14)

Verificado na página de 2026-10-01; reconferir antes de afirmar.

- A partir de 2026-08-31: novos apps e atualizações de **celular e tablet** devem targetar **API 36**. **Wear OS e Automotive**: API 35. **TV e XR**: API 34.
- Apps existentes devem targetar pelo menos **API 35** para continuar visíveis a novos usuários em aparelhos com versão mais nova.
- **Extensão até 2026-11-01** (os formulários do Play Console aparecem "mais tarde no ano").
- Isenção para apps privados de organização.
- O prazo principal já passou em 2026-10-10: diga isso ao usuário, com a data da página.

## A2: exclusão de conta, 6 itens (V-15)

1. Caminho de exclusão dentro do app.
2. Link web funcional para pedir a exclusão.
3. Perguntas de exclusão respondidas no Data safety.
4. A exclusão cobre os dados declarados no Data safety e os dos provedores de serviço.
5. Passos extras (por exemplo, cancelar assinatura) explicados ao usuário.
6. Retenção de dados divulgada.

Apps não móveis (TV, Wear) estão dispensados do caminho no app. **Não** inclua "desativar conta não conta como exclusão" como regra oficial: a página não diz isso (V-15).

## A4: localização em segundo plano, 6 itens (V-57)

1. Só se for necessária à funcionalidade central; nunca só para anúncio ou analytics.
2. Tentar antes entregar a função com localização em primeiro plano.
3. Formulário de declaração no Play Console (apps que targetam Android 10+ com `ACCESS_BACKGROUND_LOCATION`). Ação do usuário.
4. Vídeo curto: a página recomenda 30 s ou menos; é recomendação, não limite rígido.
5. Divulgação em destaque **dentro do app**, com o termo "location", indicando o uso em segundo plano (frases como "quando o app está fechado" ou "quando não está em uso") e listando as funcionalidades; não basta a política de privacidade.
6. Nova declaração ao mudar a funcionalidade que usa a permissão.

A página não pede botão de aceitar obrigatório: o prompt do sistema serve de consentimento. Sem data de atualização na página (só ©2026): reconferir.

## Notas por stack

- Expo: manifestos Android podem não estar no repositório (prebuild gerenciado). Procure `android.permissions`, `android.blockedPermissions` e plugins em `app.json`. Ausência em `android/` não prova ausência da permissão no build.
- Flutter: plugins adicionam permissões por manifest merge; revise o manifesto mesclado do build (`build/app/intermediates/merged_manifests/`, caminho **Inferido**) quando existir, e diga se não existir.
- SDKs de terceiros respondem pelo Data safety do app. Liste os SDKs detectados e peça ao usuário a declaração de cada um.

## Antes de dizer "conforme"

Reconfira as páginas oficiais citadas e escreva a data. Se não puder abrir a página nesta sessão, rotule o fato como "do VALIDATED em 2026-10-10, não reconferido".
