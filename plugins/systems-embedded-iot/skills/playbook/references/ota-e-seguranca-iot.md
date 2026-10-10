# OTA, bootloader e segurança de dispositivo IoT

Fontes lidas em 2026-10-10: V-24, V-41, V-42, V-43, V-44, V-45, V-46, V-60, V-27 (ver `fontes.md`). Este arquivo **não contém comando de queima de eFuse, geração de chave de produção ou ativação de proteção permanente**, de propósito (P-12, V-27). Textos de ETSI, NIST, ISVS e MISRA não são reproduzidos; as perguntas são redação própria. O plugin não afirma conformidade legal nem com IEC 61508, ISO 26262 ou DO-178C.

Sumário: 1. Portão de irreversíveis · 2. MCUboot · 3. OTA do ESP-IDF · 4. Secure Boot v2 do ESP-IDF · 5. Decisão MCUboot x ESP-IDF · 6. Checklist de OTA · 7. Baseline de produto (ETSI e NIST como perguntas) · 8. ISVS e FSTM · 9. Segurança funcional · 10. Gotchas.

## 1. Portão de irreversíveis (V-27, V-62)

São irreversíveis ou "permanentes na prática" (Inferido; a página do ESP-IDF não usa a palavra "irreversível"): queima de eFuse/OTP, chaves de secure boot, criptografia de flash, proteção de leitura permanente, anti-rollback por contador em eFuse. Regras:

1. O agente **não** emite nem executa comando para essas operações. Descreve pré-requisitos, riscos e caminho de recuperação, e produz a lista "Ações humanas necessárias".
2. Sem caminho de recuperação confirmado, não há procedimento de escrita.
3. Ensaie primeiro em unidades de desenvolvimento, nunca na linha de produção.
4. Escrita em dispositivo (gravar, apagar, resetar, escrever memória) usa dry-run quando houver e leitura de verificação depois.
5. Enviar código, pesos ou especificações privados a sites externos exige consentimento do usuário e registro.
6. Se o usuário insistir em "comandos prontos para colar", ofereça: revisão da configuração, checklist (`assets/templates/checklist-ota-seguranca.md`) e apontamento à documentação oficial do fabricante.

Lista de pré-requisitos a levantar antes de qualquer decisão humana: caminho de recuperação; chave privada fora do repositório e em HSM/servidor de assinatura; estado de proteção de leitura/escrita; JTAG e modo de download pela UART; política de downgrade; quantidade de unidades de desenvolvimento ensaiadas; quem aprova.

## 2. MCUboot (V-24 design; V-44 integração Zephyr)

- Slots primário e secundário; modos swap, overwrite-only, direct-XIP e RAM-load. Swap-using-scratch **não é recomendado**; a página sugere swap-using-offset ou swap-using-move. `scratch_partition` só existe no swap com scratch.
- Verificação de hash e assinatura, com chave pública casada por hash. Swap de teste que reverte no reset se a imagem não se confirmar. Resultados FAIL e PANIC interrompem o boot.
- Downgrade: por versão (só overwrite-only) ou por contador de segurança em armazenamento confiável.
- No Zephyr: `CONFIG_BOOTLOADER_MCUBOOT` no `prj.conf` ou `SB_CONFIG_BOOTLOADER_MCUBOOT` no sysbuild; partições `boot_partition`, `slot0_partition`, `slot1_partition` (e `scratch_partition`) no devicetree; assinatura automática com a chave configurada ou `scripts/imgtool.py`; integração de gerenciamento via mcumgr (hoje só MCUboot é suportado para upgrade de imagem). Os dois nomes de Kconfig para a chave seguem sem esclarecimento na página: conferir na árvore do Zephyr.
- Chaves: as de exemplo do repositório "should never be used for production"; a tabela de custódia põe a chave privada de produção em "HSM, signing ceremony, release team only".
- Regra de revisão: o **build de produção falha** se a chave de desenvolvimento estiver configurada; a chave privada nunca entra no repositório nem no `prj.conf`; partições e modo de swap estão no devicetree e casam com o plano de recuperação. Gerar chave de produção, assinar imagem de produção e gravar são ações humanas.
- Versões lidas: README do repositório cita 2.5.0-rc1 (Apache-2.0, 2,2 mil estrelas na página). Guias por plataforma (nRF, STM32) não foram lidos.

## 3. OTA do ESP-IDF (V-46)

- Duas partições OTA (`ota_0`, `ota_1`) mais `otadata` de dois setores (0x2000 bytes); estados NEW, PENDING_VERIFY, VALID, INVALID, ABORTED (e UNDEFINED).
- `esp_ota_mark_app_valid_cancel_rollback()` confirma. A partição de fábrica não sofre rollback.
- Confirmação automática é o padrão (`CONFIG_BOOTLOADER_APP_ROLLBACK_CONFIRM_ON_STARTUP`) e acontece após a inicialização dos componentes, pouco antes de `app_main`. Para confirmar só após autoteste (rede, sensores, barramentos principais), desligue o padrão e confirme pela aplicação.
- `ESP_ERR_OTA_ROLLBACK_FAILED` quando não há app válida na outra partição.
- **Anti-rollback** por versão de segurança em eFuse (`CONFIG_BOOTLOADER_APP_ANTI_ROLLBACK`) exige confirmação controlada pela aplicação e **usa eFuse: decisão e execução humanas**.
- A página não trata de assinatura da imagem OTA (isso está em Secure Boot v2).

## 4. Secure Boot v2 do ESP-IDF (V-45)

- RSA-PSS; a ROM verifica o bootloader de segundo estágio, que verifica cada app; digest da chave pública RSA-3072 em eFuse; bit de proteção de escrita ligado e **proteção de leitura desligada**; `CONFIG_SECURE_BOOT_V2_ALLOW_EFUSE_RD_DIS` mantém a possibilidade de proteger leitura de eFuse depois.
- A página diz que "can be good practice" usar servidor de assinatura remoto (não é "recomenda"); desabilitar o modo de download pela UART é "recommended"; JTAG já é desabilitado por padrão via eFuse quando o secure boot liga.
- A página cobre o ESP32 v3.0 em diante; outras variantes têm página própria: conferir.
- Portão: habilitar secure boot só com plano de recuperação, chave fora do repositório, assinatura remota ou HSM e checklist de eFuse aprovado por humano.

## 5. Decisão MCUboot x OTA nativo do ESP-IDF (comparação Inferida)

| Critério | MCUboot (Zephyr) | ESP-IDF (`otadata`) |
| --- | --- | --- |
| Slots | `slot0`/`slot1` no devicetree | `ota_0`/`ota_1` + `otadata` na tabela de partições |
| Reversão | swap de teste que reverte no reset | estados PENDING_VERIFY e rollback |
| Confirmação | imagem confirmada pela aplicação | `esp_ota_mark_app_valid_cancel_rollback()` |
| Downgrade | versão (overwrite-only) ou contador de segurança | anti-rollback por eFuse |
| Assinatura | `imgtool.py`, chave configurada, HSM em produção | Secure Boot v2, digest em eFuse |
| Chave de exemplo | do repositório, nunca em produção | idem (chave de desenvolvimento) |

As semelhanças são Inferidas; as diferenças acima foram lidas. Escolher entre os dois só faz sentido quando o RTOS não está decidido: veja `decisoes-e-tradeoffs.md`.

## 6. Checklist de OTA (V-24, V-44, V-46)

1. Imagem assinada e verificada **antes** do boot?
2. Confirmação após autoteste (rede, sensores, barramentos principais) controlada pela aplicação, com reversão automática?
3. Rollback testado em bancada (imagem que trava no boot; imagem que não confirma)?
4. Partição de fábrica mantida como recuperação?
5. Política de downgrade decidida de propósito (contador de segurança/anti-rollback usa eFuse: ação humana)?
6. O modo de upgrade (swap, overwrite, XIP) casa com o caminho de recuperação?
7. Chave de assinatura fora do repositório, `prj.conf`, `sdkconfig` e logs; build de produção rejeita chave de exemplo?
8. Transporte do download com TLS e validação de certificado (ver `barramentos-e-protocolos.md`, MQTT/HTTP)?
9. Queda de energia no meio do OTA deixa o dispositivo em estado recuperável (Inferido; testar cortando energia)?
10. Versão do firmware reportada ao backend após o boot e usada para decidir confirmação (Inferido).

Template: `assets/templates/checklist-ota-seguranca.md`.

## 7. Baseline de produto: perguntas, não texto de norma

**ETSI EN 303 645 V2.1.1** (IoT de consumo; todos os direitos reservados: só títulos e paráfrase própria). As 13 provisões viram 13 perguntas de produto (V-43):

| Provisão (título) | Pergunta de produto |
| --- | --- |
| 5.1 Sem senhas padrão universais | Cada unidade tem senha única ou definida pelo usuário? |
| 5.2 Gestão de relatos de vulnerabilidade | Existe canal público para relatar falhas e processo de resposta? |
| 5.3 Manter o software atualizado | Os componentes são atualizáveis com segurança? O dispositivo checa atualizações após iniciar e periodicamente? |
| 5.4 Armazenar parâmetros sensíveis com segurança | Chaves e credenciais ficam protegidas em repouso? |
| 5.5 Comunicar com segurança | Há criptografia adequada e gestão segura de parâmetros críticos? |
| 5.6 Minimizar superfície de ataque | Portas, serviços e interfaces de depuração desnecessários estão desligados? |
| 5.7 Garantir integridade do software | O boot e as atualizações verificam integridade/assinatura? |
| 5.8 Proteger dados pessoais | Quais dados pessoais são coletados e como são protegidos? |
| 5.9 Resiliência a quedas | Falha de rede ou energia deixa o dispositivo funcional ou recuperável? |
| 5.10 Examinar telemetria | A telemetria é revisada quanto a dados sensíveis? |
| 5.11 Facilitar apagar dados do usuário | O usuário apaga seus dados com facilidade? |
| 5.12 Facilitar instalação e manutenção | Instalação e manutenção são simples (inclui feedback físico simples, como LED)? |
| 5.13 Validar dados de entrada | Toda entrada (rede, UI, API) é validada? |

Exemplos de força (V-43): 5.1-1 usa "shall"; 5.3-1 usa "should"; 5.3-5 diz que o dispositivo "should" verificar atualizações após a inicialização e periodicamente; 5.5-8 exige gestão segura de parâmetros críticos. Distinga "shall" de "should" só citando o número da provisão. A norma vale para IoT de **consumo**; conformidade legal não é afirmada.

**NIST IR 8259A** ("IoT Device Cybersecurity Capability Core Baseline", final, 29/05/2020) define capacidades de dispositivo; a **Rev. 1 da IR 8259** ("Foundational Cybersecurity Activities for IoT Product Manufacturers", abril de 2026) descreve atividades do fabricante antes da venda. **NISTIR 8259 (2020) foi retirado em 20/04/2026: use a Rev. 1.** A página da Rev. 1 não enumera as atividades e a 8259A não contém as seis atividades: não atribua "seis atividades" a elas sem abrir o PDF. Perguntas por tema tradicional da série (rótulos Inferidos; **conferir no PDF da 8259A antes de publicar**): o dispositivo tem identificação, configuração, proteção de dados, controle de acesso lógico, atualização de software e consciência de estado (cybersecurity state awareness)?

## 8. OWASP ISVS e FSTM (V-41)

- ISVS v1.0 RC2 (CC BY-SA 4.0, "not yet a finalized standard"): use os cinco capítulos como **índice de perguntas** de projeto, sem copiar texto: V1 ecossistema, V2 aplicação de espaço de usuário, V3 plataforma de software, V4 comunicação, V5 plataforma de hardware.
- FSTM (CC BY-SA 4.0): metodologia de nove estágios para análise de firmware de **terceiros** (reconhecimento até exploração de binários). Só com autorização escrita do usuário; fora do escopo padrão do plugin e do `iot-security-auditor`.
- OWASP IoT Top 10 (2018): o PDF listado dá 404 e as dez categorias não foram lidas: **não cite categorias**.

## 9. Segurança funcional (V-60)

Zephyr declara como **objetivo** obter IEC 61508 (SIL 3 / SC 3) para um escopo limitado de código, ainda a definir; é meta de processo, não certificação obtida. ISO 26262 e DO-178C não foram cobertos. Em pedido de segurança funcional, entregue o que o projeto pode fazer (rastreabilidade, cobertura medida, análise estática, revisão independente) e diga que a conformidade exige normas pagas e processo fora do escopo do plugin.

## 10. Gotchas

- Mantenha segredos fora do repositório: `sdkconfig`, `prj.conf`, logs e `.env` entram em varredura de revisão (grep por padrões de chave, PEM, senhas literais).
- Telemetria e logs podem vazar dado pessoal (ETSI 5.8, 5.10).
- `west flash`, `idf.py flash`, `imgtool sign` com chave de produção e o upload de imagem por `mcumgr` são ações humanas ou de gravação; o hook de exemplo (`ferramentas-e-mcp.md`) já pede confirmação para eles.
- Chave de exemplo no build de produção é achado crítico.
