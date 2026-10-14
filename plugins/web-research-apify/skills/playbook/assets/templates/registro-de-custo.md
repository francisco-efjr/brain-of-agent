# Registro de custo Apify — <pesquisa> — <AAAA-MM-DD>

Como usar: uma linha por run, **incluindo falhas, timeouts e runs abortadas**. Preencha a linha "planejada" **antes** de chamar `call-actor` e complete depois. O MCP não mostra o custo real: peça ao usuário o valor do Console (Billing/Usage ou lista de Runs) e escreva quem informou; sem o valor, escreva "não verificável". Nunca registre token ou segredo, nem credencial no resumo do input.

```markdown
# Registro de custo Apify — <pesquisa> — <AAAA-MM-DD>
Orçamento aprovado: US$ <total> (por <quem>, em <mensagem/data>) · por run: US$ <x> · Actors permitidos: <lista>
Perfil de tools: <P0–P3> · Prefixo: <mcp__…> · Versão do servidor: <vX | não verificável>

| # | Data/hora | Plano | Actor · build | runId | datasetId | Input (resumo, sem segredos) | memory/timeout | Teto US$ | Estimativa US$ | Status | Itens lidos | Custo real US$ (Console) | Informado por | Obs. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Resumo: teto comprometido (soma) US$ … ≤ orçamento? · custo real conhecido US$ … de … runs (resto: não verificável) ·
saldo pelo teto US$ … · runs repetidas 0 · Actors fora da lista 0 · textos dirigidos à IA n ·
datasets a apagar (PII): … · pendências do humano: ler custo no Console / apagar / revogar token
```

## Campos

| Campo | O que escrever |
| --- | --- |
| Plano | ID do plano aprovado (`PL-...`); run sem plano é achado de severidade alta na auditoria |
| Actor · build | `owner/name` e build, ou "não informado" |
| Input (resumo) | Campos relevantes e limites de volume; sem URLs privadas nem credenciais |
| memory/timeout | `callOptions.memory` (ou "padrão") e `callOptions.timeout` em segundos |
| Teto US$ | `callOptions.maxTotalChargeUsd`, ou "sem teto" em Actor usage-based |
| Estimativa US$ | A conta do plano (rótulo Inferido) |
| Status | `SUCCEEDED`, `FAILED`, `TIMED-OUT`, `ABORTED`, `RUNNING` ou "erro sem runId" |
| Custo real | Valor lido no Console pelo usuário; "não verificável" até lá |
| Informado por | "usuário (Console)", "apify-api-read (H-05b, não testado)" ou "—" |

## Exemplo de linha (valores fictícios)

| # | Data/hora | Plano | Actor · build | runId | datasetId | Input (resumo) | memory/timeout | Teto US$ | Estimativa US$ | Status | Itens lidos | Custo real US$ | Informado por | Obs. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-13 14:02 | PL-2026-10-13-01 | trudax/reddit-scraper-lite · não informado | RUN_EXEMPLO | DS_EXEMPLO | searches 1, maxItems 20, comentários 0 | padrão / 300 s | 0,15 | 0,12 | SUCCEEDED | 20 | não verificável | — | pedir o valor ao usuário |

## Regras de fechamento

- **Teto comprometido** = soma dos tetos de todas as runs (inclusive as que falharam). Deve ser ≤ orçamento aprovado.
- **Saldo pelo teto** = orçamento − teto comprometido. **Saldo real** = orçamento − custo real informado, apenas com custo conhecido.
- Run repetida (mesmo Actor e mesmo input) sem novo plano: registre como achado, não apague a linha.
- Datasets com dado pessoal: liste em "datasets a apagar" e planeje a exclusão (dataset sem nome expira em 7 dias; nomeado fica retido).
