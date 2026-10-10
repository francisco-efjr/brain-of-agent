# Relatório de debug

Data: [AAAA-MM-DD]  ·  Ambiente/build: [versão, SO, branch/commit]  ·  Frequência: [constante | intermitente, N de M execuções]

| Campo | Conteúdo |
| --- | --- |
| Sintoma | [esperado x observado, com dados redigidos] |
| Reprodução | [comando exato] -> [saída resumida]; se não reproduziu, por quê |
| Causa raiz | [o que estava errado, em uma ou duas frases] |
| Hipóteses testadas | [H1: comando e resultado (confirmada/refutada)]; [H2: ...] |
| Correção | [o que mudou, com `arquivo:linha`] |
| Evidência | [comando e saída antes e depois] |
| Teste de regressão | [`arquivo:linha`; comando que o roda; visto falhando sem a correção: sim/não] |
| Prevenção | [o que impede a volta: validação, constraint, teste, alerta] |
| Relacionado | [bugs anteriores na mesma área, dívida, notas arquiteturais] |
| Revalidação (5 passos) | 1 reprodução original: [ ]  2 casos adjacentes: [ ]  3 tipos/lint/build/testes: [ ]  4 jornada real: [ ]  5 diff final e artefato testado: [ ] |
| Rótulos | [Verificado / Inferido / Suposição / Não verificável, por afirmação] |
| Status | DONE (causa achada, correção, teste de regressão, suíte verde) · DONE_WITH_CONCERNS (corrigido, mas não totalmente verificável, ex.: intermitente) · BLOCKED (causa não identificada) · NEEDS_CONTEXT |

Causa não identificada: escreva "causa não identificada", liste as evidências coletadas e o que falta medir (ex.: instrumentar [PONTO], esperar a próxima ocorrência).
Escalada registrada: correções falhas na sessão [N/2]; hipóteses refutadas [N/3].
