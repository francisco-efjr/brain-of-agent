# Registro de evidências mobile

Adaptado do template `registro-evidencias-qa` do brain-of-agent (MIT, Francisco Edson). Uma linha por ação verificável. Leitura de código não é teste executado; captura de tela não prova persistência; CI verde não prova o fluxo se as asserções forem fracas; "só emulador Android" não se estende a iOS, aparelho físico ou loja.

Projeto e revisão (commit): [ ] · Ambiente (SO, macOS?, emulador ou aparelho, versões de SDK): [ ] · Data: [AAAA-MM-DD]

| Evidência | Item ou caso (ID do checklist) | Método (execução / análise estática / leitura / revisão por IA / revisão humana) | Ambiente e revisão | Dados sanitizados? | Resultado (passou / falhou / não executado / não verificável) | Artefato (caminho ou ID) | Limitação |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E-01 | [ex.: TST-10] | [execução] | [Android emulador API 34] | Sim | [passou] | [log do Gradle] | [não cobre iOS] |

## Execução (detalhe)

ID: [id] · Caso: [id] · Tentativa: [n]
Comando literal: `[comando]`
Estado inicial: [conta sintética, build instalada, permissões]
Esperado e fonte do oráculo: [resultado observável]
Obtido (saída relevante, redigida): [texto]
Estado: [passou / falhou / não executado / não verificável]
Alcance da conclusão: [o que a evidência prova e o que não prova]

Na falha, preserve o primeiro erro antes de repetir; registre build ou commit, dispositivo e SO, estado inicial, etapas, timestamp com fuso, screenshot ou hierarquia de UI, logs redigidos e ID da operação.

## Mudança e revalidação

Achado original: [id]
Correção e revisão: [arquivos e commit]
Revalidação: [casos, evidências, resultados]
Regressões por impacto: [escopo e resultados]
Pendências: [o que falta, incluindo passagens humanas e passos que exigem macOS]

## Redação

Antes de anexar: tokens, dados pessoais e dados de produção removidos de logs, traces e capturas (snippet S-18).
