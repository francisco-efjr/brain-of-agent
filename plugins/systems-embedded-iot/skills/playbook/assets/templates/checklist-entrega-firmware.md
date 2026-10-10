# Checklist de go/no-go de firmware - <versão / release>

Adaptado de `checklist-release.md` do brain-of-agent (MIT, Francisco Edson). Preencha antes da decisão. Status: OK, PENDENTE, FALHOU ou N/A (N/A exige motivo na coluna Evidência). Evidência: comando e saída, log de bancada, link de CI ou ID de ticket; "testado" sem evidência conta como PENDENTE. Itens com (*) são bloqueantes: PENDENTE ou FALHOU = NO-GO, salvo aceite formal de quem decide, registrado no parecer. Risco residual: o que acontece em campo se o item não estiver OK, em linguagem de decisão ("unidades não recuperam após queda de energia durante OTA"), não em jargão.

| Campo | Valor |
| --- | --- |
| Versão de firmware / hash | |
| Hardware alvo e revisões cobertas | |
| Data e janela | |
| Tipo de liberação | completa / gradual por lote / atrás de flag |
| Responsável pelo checklist | |
| Decisores | |

## 1. Funcional

| # | Item | Status | Evidência | Risco residual |
| --- | --- | --- | --- | --- |
| F1 (*) | Critérios de aceite das funcionalidades da versão verificados (`features.json` com `passes` e evidência) | | | |
| F2 (*) | Nenhum defeito crítico aberto no escopo | | | |
| F3 | Defeitos altos abertos têm contorno e aceite registrado | | | |

## 2. Temporização, memória e energia

| # | Item | Status | Evidência | Risco residual |
| --- | --- | --- | --- | --- |
| T1 (*) | Pilha por tarefa medida (high-water) com margem declarada | | | |
| T2 | Flash/RAM do `.map` dentro do orçamento com margem | | | |
| T3 | Corrente por estado medida na placa com o firmware desta versão | | | |
| T4 | Latência de ISR / deadline crítico medido (analisador lógico ou equivalente) | | | |

## 3. Robustez

| # | Item | Status | Evidência | Risco residual |
| --- | --- | --- | --- | --- |
| R1 (*) | Todo erro de barramento/rede tem caminho testado (host ou bancada) | | | |
| R2 | Watchdog ativo e motivo de reset registrado | | | |
| R3 | Reconexão com backoff e jitter testada | | | |
| R4 | Soak test: uptime de <N> horas sem reset inesperado | | | |

## 4. Segurança e OTA

| # | Item | Status | Evidência | Risco residual |
| --- | --- | --- | --- | --- |
| S1 (*) | Imagem assinada com chave de produção (custódia humana); chave de exemplo ausente do build | | | |
| S2 (*) | OTA: confirmação após autoteste e rollback testados em bancada; partição de fábrica mantida | | | |
| S3 | Segredos ausentes do repositório, `sdkconfig`, `prj.conf` e logs | | | |
| S4 | JTAG/UART de download: estado declarado; irreversíveis tratados por humano | | | |
| S5 | Baseline de produto (ETSI/NIST) respondido em `checklist-ota-seguranca.md` | | | |

## 5. Build, CI e rastreabilidade

| # | Item | Status | Evidência | Risco residual |
| --- | --- | --- | --- | --- |
| B1 (*) | Build reprodutível: toolchain e versões fixadas; hash do artefato de CI igual ao gravado | | | |
| B2 | Testes de host, análise estática e sanitizers verdes no CI | | | |
| B3 | Versão embutida no firmware e reportada ao backend | | | |
| B4 | Matriz de hardware testada (revisões de placa) | | | |
| B5 | Plano de rollback e quem executa; publicar tag é ato humano | | | |

## Parecer

GO / NO-GO / GO com condições: <...>. Itens bloqueantes abertos: <...>. Aceites formais de risco: <quem, quando>. Lacunas conhecidas: <...>.
