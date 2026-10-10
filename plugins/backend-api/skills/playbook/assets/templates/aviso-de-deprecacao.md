# Aviso de deprecação — [endpoint, campo ou versão]

> Base: V-35 (Azure REST API Guidelines, CC BY 4.0, destilado), V-30 (depreciar antes de remover) e brain-of-agent (MIT). Cabeçalhos `Deprecation` (RFC 9745, Standards Track, 2025) e `Sunset` (RFC 8594, Informational, 2019) **Verificados** em 2026-10-10 em rfc-editor.org.

| Item | Conteúdo |
| --- | --- |
| O que muda | [campo `x` removido | versão `v1` descontinuada | enum `status` ganha valores] |
| Quem é afetado | [consumidores conhecidos; uso medido por versão nos últimos 30 dias] |
| Versão e datas | Anúncio: [data] · Início da sinalização: [data] · Remoção (sunset): [data] |
| Substituto | [endpoint/campo novo; guia de migração: link] |
| Compatibilidade enquanto isso | A versão antiga continua funcionando até a data; nenhuma quebra dentro de uma versão |
| Sinalização na resposta | `Deprecation: @[segundos desde a época Unix]` (data estruturada, RFC 9745) · `Sunset: [HTTP-date, ex.: Thu, 31 Dec 2026 23:59:59 GMT]` (RFC 8594; não pode ser anterior ao `Deprecation`) · `Link: <[url do guia]>; rel="deprecation"; type="text/html"` (RFC 9745) |
| Spec | Operação marcada `deprecated: true` no OpenAPI; GraphQL `@deprecated(reason: "...")` |
| Comunicação | [e-mail/changelog/portal]; responsável: [..]; lembretes em [T-60, T-30, T-7 dias] |
| Critério para remover | Uso da versão antiga abaixo de [limite combinado] ou data atingida com consumidores avisados |
| Plano de reversão | [reativar rota por feature flag até X; dado não é recriado por rollback] |
| Teste | Resposta da versão antiga contém os cabeçalhos; a nova funciona; remoção testada em ambiente de teste |
| `.proto` | Número de campo nunca reutilizado; campo removido marcado `reserved`; `buf breaking` no CI |

Rótulos: [Verificado | Inferido | Suposição]. Publicar o aviso é ação externa: só com autorização concreta do responsável.
