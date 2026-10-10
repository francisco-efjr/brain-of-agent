# Checklist de release Android

Composição do plugin sobre V-13, V-14, V-15, V-57 e V-76. Verificado em 2026-10-10: regras e prazos do Google Play mudam, reabra as páginas oficiais antes de afirmar. O agente não promove trilhas nem envia nada ao Play Console.

App: [nome] · applicationId: [id] · versionName e versionCode: [x.y.z (n)] · minSdk e targetSdk lidos: [valores] · Lido em: [AAAA-MM-DD]

## A. Itens

| # | Item | Regra | Evidência (arquivo:linha ou "ausente em ...") | Status |
| --- | --- | --- | --- | --- |
| 1 | `targetSdk`: API 36 para celular e tablet (novos apps e atualizações a partir de 2026-08-31, com extensão até 2026-11-01); Wear OS e Automotive 35; TV e XR 34; reconferir a página | V-14 | | |
| 2 | Exclusão de conta dentro do app e link web funcional | V-15 | | |
| 3 | Perguntas de exclusão no Data safety; cobre os dados declarados e os provedores; retenção divulgada | V-15 | | |
| 4 | Data safety coerente com o código e com a política de privacidade | V-13 | | |
| 5 | Permissões de alto risco justificadas | V-13 | | |
| 6 | Conta de demonstração disponível | V-13 | | |
| 7 | Localização em segundo plano apenas se central: formulário, vídeo curto (recomendação de 30 s), divulgação in-app com o termo "location" e a lista de funcionalidades | V-57 | | |
| 8 | `POST_NOTIFICATIONS` declarada e pedida em execução (API 33+); canal criado cedo | V-54, V-55 | | |
| 9 | Assinatura do app e Play App Signing: ação do usuário; impressão digital correta em `assetlinks.json` (Inferido) | V-40 | | |
| 10 | Trilha interna antes de produção; promoção só com confirmação nomeada | V-35, V-76 | | |

## B. Publicação por Gradle (opcional)

Gradle Play Publisher (V-76) está em modo de manutenção e não é oficial do Google. Se o projeto o usa: conta de serviço no Google Cloud com a API do Android Publisher e papel mínimo; chave fora do repositório (cofre do CI); primeiro upload manual no Play Console; trilha interna antes de produção. Versões mínimas de Gradle e AGP não constam na base: leia o README atual.

## C. Observações

- Notas de versão: rascunho em `notas-de-versao.md`, sem detalhes internos.
- Android vitals: conferir wake locks e demais métricas antes de ampliar o lançamento (V-62, verificado em 2026-10-10).
- Dispositivos: declarar quais foram testados (emulador, aparelho físico); não estender o resultado a iOS.

## D. Resultado

Riscos prováveis de rejeição: [lista] · Altos: [lista] · Não verificáveis: [lista] · Ações do usuário (Play Console, Data safety, formulários): [lista]
