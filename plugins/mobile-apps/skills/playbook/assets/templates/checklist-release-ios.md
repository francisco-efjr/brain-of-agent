# Checklist de release iOS

Composição do plugin sobre V-16, V-17, V-58 e V-73. Verificado em 2026-10-10: reabra as páginas oficiais antes de afirmar qualquer regra. Fim da seção 5 das App Review Guidelines (após 5.3.4) não foi lido. Relate falhas como "risco provável de rejeição". O agente nunca aciona "Submit for Review".

App: [nome] · Bundle ID: [id] · Versão e build: [x.y.z (n)] · Alvo mínimo: [iOS] · Lido em: [AAAA-MM-DD]

## A. Os 12 itens

| # | Item | Guideline ou fonte | Evidência (arquivo:linha ou "ausente em ...") | Status |
| --- | --- | --- | --- | --- |
| 1 | Exclusão de conta dentro do app | 5.1.1(v) | | |
| 2 | Login equivalente quando há login de terceiros (avaliar, não afirmar violação) | 4.8 | | |
| 3 | Compra in-app e restauração de compras | 3.1.1 | | |
| 4 | Conta de demonstração e backend ativo, ou modo demo previamente aprovado | 2.1 | | |
| 5 | O app é mais que um site empacotado | 4.2 | | |
| 6 | Conteúdo de usuário: filtro, denúncia, bloqueio, contato | 1.2 | | |
| 7 | ATT quando há rastreamento | 5.1.2 | | |
| 8 | Sem funções ocultas | 2.3.1 | | |
| 9 | `PrivacyInfo.xcprivacy` do app e dos SDKs; `NSPrivacyAccessedAPITypes` com motivo por API | V-17 | | |
| 10 | Purpose string específica, localizada (`InfoPlist.xcstrings`), menos de 4.000 bytes, por recurso protegido; sem string há ITMS-90683 | V-58 | | |
| 11 | Metadados que não podem ser alterados após o envio, revisados | V-73 | | |
| 12 | Build validado no Xcode e presente no TestFlight | V-73 | | |

Status: conforme, lacuna, não verificável (motivo), não aplicável (motivo).

## B. Sequência de 7 passos

| # | Passo | Requer macOS e Xcode | Ação do usuário |
| --- | --- | --- | --- |
| 1 | Apple Developer Program ativo | Não | Sim |
| 2 | Registro do app no App Store Connect (antes do primeiro envio) | Não | Sim |
| 3 | `Product > Archive` | Sim | — |
| 4 | "Validate App" | Sim | — |
| 5 | "Distribute App" e upload ao App Store Connect | Sim | Confirmar |
| 6 | TestFlight interno e externo; conferir falhas e feedback no Organizer | Parcial | Convidar testadores |
| 7 | Enviar a última build do TestFlight ao App Review | Não | **Sempre do usuário** |

Sem macOS: passos 3 a 5 ficam "Não verificável"; alternativas Xcode Cloud (V-74) ou EAS Build (V-75), com ficha de ação confirmada (`ficha-acao-release.md`).

## C. Extras por tipo de app

- Push: capability, `aps-environment`, App ID habilitado (ação do usuário) (V-52).
- Localização: `NSLocationWhenInUseUsageDescription`, e `NSLocationAlwaysAndWhenInUseUsageDescription` se houver segundo plano (V-58).
- SwiftData + CloudKit: esquema de produção promovido, só aditivo (V-61).
- Deep links: AASA hospedado e `applinks:` no entitlement (V-40).

## D. Resultado

Riscos prováveis de rejeição: [lista] · Altos: [lista] · Não verificáveis: [lista] · Ações do usuário: [lista]
