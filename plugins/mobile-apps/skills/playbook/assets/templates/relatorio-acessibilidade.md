# Relatório de acessibilidade mobile

Base: checklist de 9 itens (V-48), números oficiais (V-18, V-09, V-79), VoiceOver (V-78) e regras do SwiftUI Pro (V-19). O agente confere código; a **passagem manual com VoiceOver ou TalkBack é verificação humana** e fica como pendência explícita. Para RN e Flutter não há fonte validada de APIs de semântica: rotule Inferido.

Plataforma e versões lidas: [iOS / Android / RN / Flutter; versões] · Telas: [lista] · Data: [AAAA-MM-DD]
Referência numérica: iOS alvo 44x44 pt (mínimo 28 pt), Dynamic Type até 200%, contraste 4,5:1 até 17 pt e 3:1 a partir de 18 pt ou negrito; Android alvo 48x48 dp, contraste 4,5:1 abaixo de 18 sp (ou negrito abaixo de 14 sp) e 3:1 no restante.

## Achados por tela

| Tela | Item (1 a 9) | Plataforma | Achado | Evidência (arquivo:linha) | Correção | Status (conforme / lacuna / não verificável) |
| --- | --- | --- | --- | --- | --- | --- |
| [Login] | 3 (alvos) | Android | [IconButton de 32.dp] | [LoginScreen.kt:57] | [remover o `size(32.dp)`; o `IconButton` aplica 48 dp] | Lacuna |

Itens: (1) rótulos e decorativos; (2) controles nativos em vez de gestos; (3) alvos; (4) texto escalável; (5) agrupamento e títulos; (6) ordem de foco; (7) contraste e cor; (8) Reduce Motion e alternativa a gestos; (9) estado dinâmico anunciado e hints.

## Pendências humanas

| Teste | Quem | Gestos ou ferramenta | Telas | Estado |
| --- | --- | --- | --- | --- |
| Passagem com VoiceOver (deslizar, toque duplo, Screen Curtain, ordem de leitura) | [pessoa] | iOS | [telas] | Pendente |
| Passagem com TalkBack | [pessoa] | Android | [telas] | Pendente |
| Maior tamanho de texto | [pessoa] | ambos | [telas] | Pendente |

## Não verificável e lacunas

- [ex.: contraste de componentes não textuais, fora de V-79]
- [ex.: traits e regra do tipo no rótulo no iOS: Inferido]
- [ex.: build iOS sem macOS]

## Resumo

Conformes: [n] · Lacunas: [n] · Pendências humanas: [n] · Próximo passo: [ação]
