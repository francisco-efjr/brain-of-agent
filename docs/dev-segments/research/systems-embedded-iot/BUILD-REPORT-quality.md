# BUILD-REPORT de qualidade: plugin systems-embedded-iot

Data: 2026-10-10 · Papel: validador de qualidade de prompt e conteúdo técnico · Rubrica: `docs/foundation/prompt-quality-rubric.md` (D1 a D12, nota = média x 20).

Independência: o autor do material e este validador são modelos Claude (família diferente de versão, mesma família de treino). Isto não é validação externa independente. As notas são julgamento por leitura, sem execução de `claude plugin eval` (Claude Code local 2.1.128, abaixo do 2.1.269 exigido) e sem hardware.

## 1. Escopo lido

Lidos integralmente: `README.md`, `evals/README.md`, os 15 casos de eval (prompt e graders), os 10 `SKILL.md`, os 5 agentes, a seção de índice da skill `prompts`. Biblioteca de prompts: 15 prompts lidos por inteiro (PR-01, 02, 03, 04, 05, 06 e 07 em parte, 08, 21, 22, 23, 24, 26, 29, 30) e estrutura dos 30 conferida por contagem (cada prompt tem quando usar, variáveis, bloco de prompt, por que funciona e fonte). Referências lidas por amostra: `cortex-m-faults`, `rtos-checklists`, `checklist-ota`, `auditoria-de-pinos`, `ferramentas-e-mcp`, `registro-evidencias-bancada`. As demais referências e templates foram checadas por grep (CAPS, placeholders, segredos, comandos copiáveis de operação irreversível) e pelo verificador estrutural, não relidas linha a linha.

## 2. Tabela arquivo | antes | depois | correções

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 92 | 92 | Nenhuma necessária. Gatilhos PT/EN, 12 princípios com porquê, modo completo com ativação restrita e gates. |
| `skills/prompts/SKILL.md` | 88 | 91 | D5: acrescentado exemplo de entrega (PR-08) com variáveis reais da biblioteca. |
| `skills/firmware-review/SKILL.md` | 90 | 90 | Nenhuma. Exemplo trabalhado, formato de tabela, gotchas e delegação adequados. |
| `skills/rtos-concurrency-review/SKILL.md` | 91 | 91 | Nenhuma. Regras de FreeRTOS e Zephyr conferem com as fontes V-15, V-49, V-50, V-52. |
| `skills/bus-protocol-review/SKILL.md` | 90 | 90 | Nenhuma. |
| `skills/datasheet-first/SKILL.md` | 91 | 91 | Nenhuma. Referência `auditoria-de-pinos.md` ajustada (ver seção 3). |
| `skills/firmware-root-cause/SKILL.md` | 90 | 90 | Nenhuma. `allowed-tools` sem Bash e probe com classes de gate, bem calibrado. |
| `skills/firmware-test-host/SKILL.md` | 86 | 91 | D8: `allowed-tools` pré-aprovava `Write` e `Edit` sem limite de escopo, e o passo 1 manda extrair o seam (código de produção). Acrescentado "Escopo de escrita": só testes, falsos e fixtures; seam de produção só com aprovação do diff. |
| `skills/hw-bench-loop/SKILL.md` | 93 | 93 | Nenhuma. `disable-model-invocation`, cartão de gravação, autorização escopada, recusa de irreversíveis. |
| `skills/ota-security-review/SKILL.md` | 88 | 92 | D8: o grep de triagem de segredos imprimia a linha com o valor do segredo no contexto. Trocado por `grep -l` (lista só arquivos) com instrução de abrir só a linha necessária e mascarar. |
| `agents/embedded-architect.md` | 86 | 90 | D5: acrescentado exemplo resumido de ADR (partições OTA) sem números inventados. |
| `agents/firmware-reviewer.md` | 92 | 92 | Nenhuma. Somente leitura (Read, Grep, Glob), teto de achados, limiar de confiança, sem Write. |
| `agents/firmware-debugger.md` | 89 | 91 | D5: acrescentado exemplo de hipótese bem formada e de hipótese vaga. |
| `agents/firmware-test-engineer.md` | 90 | 90 | Nenhuma. Escopo de escrita já limitado a caminhos de teste indicados. |
| `agents/iot-security-auditor.md` | 87 | 91 | D5: acrescentado exemplo de achado no formato da tabela. |
| `skills/prompts/references/prompt-library.md` (PR-01 a PR-20) | 91 | 91 | Nenhuma. Amostra de 7 prompts lidos por inteiro: delimitadores XML, dado separado de instrução, rótulos, formato e critério de pronto. |
| `skills/prompts/references/prompt-library-bancada-seguranca-processo.md` (PR-21 a PR-30) | 91 | 91 | Nenhuma. PR-23 recusa comando de operação irreversível; PR-26 trata material de terceiros como dado. |
| `evals/` (13 casos originais) | 87 | 88 | Cada caso tem PASS/FAIL observáveis, hipótese falsificável e grader `tool_used` determinístico; há negativo (React), injeção, proporcionalidade e segurança. Sem alteração nos casos; README atualizado. |
| `evals/embarcados-completo-explicito` (novo) | n/a | 88 | Caso positivo do modo completo (lacuna declarada no README de evals). |
| `evals/pinos-esp32-auditoria` (novo) | n/a | 88 | Caso do modo `pinos` do `datasheet-first` (lacuna declarada). |
| `evals/README.md` | 90 | 91 | Contagens e tabela atualizadas (15 casos, 45 execuções); lacunas reescritas. |
| `README.md` | 80 | 88 | Dizia "10 casos" de eval; existem 15. Corrigido. |
| `skills/ota-security-review/references/checklist-ota.md` | 84 | 90 | Correção factual E-04 (ver seção 3). |
| `skills/datasheet-first/references/auditoria-de-pinos.md` | 86 | 89 | P-02 listava só GPIO 5 e 12 como strapping do ESP32 clássico; agora lista 0, 2, 5, 12 e 15 como Inferido do datasheet, com instrução de confirmar na revisão do módulo. |

Média antes (32 arquivos que existiam e foram pontuados): 88,3. Média depois (34 arquivos, incluindo os 2 evals novos): 89,6. Menor nota depois: 88. Nenhum arquivo abaixo de 80 e nenhum critério de reprovação automática encontrado.

## 3. Fidelidade técnica

Verificado nesta rodada (WebFetch da documentação oficial, 2026-10-10):

- Secure Boot v2 do ESP-IDF (`security/secure-boot-v2.html`, latest): proteção de escrita do digest ligada e de leitura desligada; JTAG desabilitado por padrão ao ligar o secure boot; modo de download pela UART com recomendação de desabilitar; suporte ao ESP32 a partir da revisão v3.0. Coincide com V-45 e com o que a skill `ota-security-review` e o agente `iot-security-auditor` afirmam.
- OTA do ESP-IDF (`api-reference/system/ota.html`, latest): `CONFIG_BOOTLOADER_APP_ROLLBACK_CONFIRM_ON_STARTUP` (padrão) e `CONFIG_BOOTLOADER_APP_ROLLBACK_CONFIRM_BY_APP`, `CONFIG_BOOTLOADER_APP_ANTI_ROLLBACK`, `esp_ota_mark_app_valid_cancel_rollback()`. Confirmado.

Correções factuais aplicadas:

1. `checklist-ota.md` E-04: citava o símbolo `CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE` como Inferido. A página `latest` cita `CONFIG_BOOTLOADER_APP_ROLLBACK` ("enabled by default"). O texto agora registra o símbolo da página `latest` como Verificado, o nome antigo como Inferido para versões anteriores, e manda conferir no `menuconfig` da versão instalada.
2. `auditoria-de-pinos.md` P-02: lista de strapping do ESP32 clássico completada (0, 2, 5, 12, 15), rotulada Inferido.

Conferido por conhecimento estável do domínio, sem erro encontrado (rótulo Inferido já presente no material): bits do CFSR/HFSR e endereços SCB do ARMv7-M, quadro empilhado e EXC_RETURN, ausência de CFSR no ARMv6-M, regra de FreeRTOS sobre `configMAX_SYSCALL_INTERRUPT_PRIORITY` (nome novo `configMAX_API_CALL_INTERRUPT_PRIORITY`, limite diferente de 0), ETSI EN 303 645 com 13 provisões numeradas 5.1 a 5.13, keep alive de MQTT 3.1.1 com desconexão em 1,5 vez o intervalo, `disable_clean_session = false` equivalente a Clean Session ligada no `esp-mqtt`.

Não reverificado (confiança herdada do VALIDATED.md): comportamentos do Zephyr (`k_work_*` em ISR, `unit_testing` só em Linux, nomes master/slave deprecados desde 4.5), TWAI (`twai_node_recover`), I2C novo do ESP-IDF, MCUboot 2.5.0-rc1, NIST IR 8259 retirado em 20/04/2026 com Rev. 1 de abril de 2026.

## 4. Direitos autorais e segurança

- Cópia literal: nenhum trecho extenso de terceiros encontrado nos arquivos lidos; atribuições a brain-of-agent (MIT), gstack (destilado), awesome-cursorrules (CC0, reescrito) e normas (só paráfrase) estão no README. MISRA, ETSI, NIST, ISVS e FreeRTOS Kernel Book não são reproduzidos.
- Segredos: grep de padrões de chave privada, `AKIA`, `sk-`, `ghp_` sem ocorrências no plugin.
- CAPS e ameaças: grep sem ocorrência fora de metacomentários que explicam a política de tom; única ênfase deliberada é o gate de gravação.
- `--dangerously-skip-permissions`: aparece em duas linhas, ambas marcadas como risco, apenas em sandbox e repositório confiável.
- Operações irreversíveis: nenhum comando copiável de queima de eFuse, geração de chave ou apagamento total fora de tabelas de classificação "não usar/gate"; grep confirmado.
- Revisores sem Write/Edit: `firmware-reviewer`, `iot-security-auditor`, `embedded-architect` usam só Read, Grep, Glob. `firmware-debugger` tem Bash limitado por instrução e sem Write/Edit; `firmware-test-engineer` tem Write/Edit/Bash com escopo de caminhos de teste e gate de hardware por instrução. A restrição por instrução não é contenção técnica; os próprios agentes declaram isso e pedem conferência por `git status`.
- Evals: todos têm PASS/FAIL observáveis; há caso negativo (`negativo-react-botao`, `tool_used` com `min: 0, max: 0, arm: both`), de injeção (`injecao-readme-keyword`) e de proporcionalidade. O fixture de injeção contém texto dirigido à IA de propósito e é dado de teste; nada nele foi executado.

## 5. Pendências

1. Os 15 evals continuam `designed_not_executed`. Rodar `claude plugin eval` exige Claude Code 2.1.269 ou superior; os campos extras do frontmatter de `prompt.md` (`runs`, `expected_outcome`, `timeout_seconds`, `model`, `name`) e dos graders (`arm`, `min`, `max`) não puderam ser conferidos contra o runner. Não verificável.
2. Falta caso de eval para `hw-bench-loop` (só por invocação explícita), `firmware-review --modo orcamento` e `--modo misra`, e para delegação aos agentes.
3. As referências e templates não lidos linha a linha (cerca de 30 arquivos) receberam só checagem por grep e verificador estrutural. Uma passada de leitura completa fica para validação futura.
4. Decisão do usuário: os agentes `firmware-debugger` e `firmware-test-engineer` têm Bash restrito por instrução. Se o usuário quiser contenção técnica, o caminho é regra `permissions` `ask`/`deny` no projeto (documentada em `ferramentas-e-mcp.md`), não algo que o plugin possa impor.
5. Versões de ESP-IDF, Zephyr e MCUboot mudam: conferir antes de publicar.
6. Revisão independente de verdade (outro modelo ou humano, de preferência com leitura de uma amostra dos evals executados) continua recomendada antes de divulgar notas.

## 6. Verificação final

- `python tools/verify_plugin.py plugins/systems-embedded-iot`: PASS (10 skills, 5 agentes, 15 evals, 112 arquivos).
- `claude.exe plugin validate plugins/systems-embedded-iot`: Validation passed.
