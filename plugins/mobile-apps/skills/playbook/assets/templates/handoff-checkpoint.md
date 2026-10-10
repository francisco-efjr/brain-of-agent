# Handoff e checkpoint mobile

Adaptado do template `handoff-checkpoint` do brain-of-agent (MIT, Francisco Edson). Gere ao fim da sessão ou antes de a janela de contexto encher. Não inclua segredos nem dados pessoais.

- Objetivo e escopo autorizado:
- Revisão (commit/branch) e ambiente (SO, macOS disponível?, emulador ou aparelho, versões de SDK):
- Estado do workspace e mudanças do usuário preservadas:
- Leituras completas, parciais e ausentes (referências do plugin, arquivos do projeto) e ponto de retomada:
- Fontes de verdade e decisões (ADR, spec):

| Item | Estado (verificado / inferido / suposição / não verificável) | Alteração (arquivos) | Evidência (comando e saída) | Limitação ou próxima ação |
| --- | --- | --- | --- | --- |
| [ex.: fila offline persistente] | Verificado | [OfflineQueue.kt] | [`./gradlew testDebugUnitTest`: 42 passed] | [teste em aparelho físico pendente] |

- Comandos executados, resultados e primeira falha:
- Dados e integrações usados e limpeza necessária (contas sintéticas, builds de teste):
- Checks invalidados por mudanças posteriores:
- Ações externas pendentes que são do usuário (App Store Connect, Play Console, chaves, DNS de `assetlinks.json`/AASA):
- Passagem humana pendente (VoiceOver/TalkBack, aparelho físico):
- Pendências, riscos e impedimentos:
- Próxima ação concreta:

Ao retomar, confirme o commit e o workspace antes de assumir que este estado continua válido. Reexecute os checks afetados.
