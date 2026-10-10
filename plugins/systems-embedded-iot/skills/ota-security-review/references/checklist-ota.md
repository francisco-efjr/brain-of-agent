# Checklist de OTA e bootloader: MCUboot e ESP-IDF

Uso: consulta da skill `ota-security-review`. Fontes lidas em 2026-10-10: V-24 (documento de design do MCUboot), V-44 (MCUboot no Zephyr: habilitar, assinar, custodiar chaves), V-45 (Secure Boot v2 do ESP-IDF), V-46 (OTA do ESP-IDF). A comparação entre as duas plataformas é Inferida (V-46). Rótulos: Verificado (lido na fonte), Inferido (conhecimento estável ou comparação), Não verificável (guias de plataforma não lidos). Símbolos Kconfig variam por versão: confirme na versão instalada.

Sumário: [MCUboot](#mcuboot) · [ESP-IDF OTA](#esp-idf-ota) · [Secure Boot v2 do ESP-IDF](#secure-boot-v2-do-esp-idf) · [Comparação e decisão](#comparação-e-decisão) · [Testes de bancada do caminho de atualização](#testes-de-bancada-do-caminho-de-atualização) · [Canal de download](#canal-de-download)

## MCUboot

| # | Verificação | Motivo | Rótulo |
| --- | --- | --- | --- |
| M-01 | Slots primário e secundário definidos no devicetree (`slot0_partition`, `slot1_partition`) mais `boot_partition`; `scratch_partition` só no modo swap com rascunho, que a documentação marca como "not recommended" em favor de swap-using-offset ou swap-using-move. | Partições erradas ou modo inadequado impedem a reversão. V-44. | Verificado |
| M-02 | Modo escolhido de propósito: swap, overwrite-only, direct-XIP ou RAM-load, casando com o caminho de recuperação. | Cada modo tem comportamento diferente de reversão e de downgrade. V-24. | Verificado |
| M-03 | Imagem verificada por hash e assinatura antes do boot, com a chave pública casada por hash. | Imagem não autorizada não pode iniciar. V-24. | Verificado |
| M-04 | Swap de teste: a imagem nova roda uma vez e reverte no reset se não for confirmada; o aplicativo confirma só **depois do autoteste**. No Zephyr, a confirmação é feita pela aplicação por API do pacote DFU do MCUboot ou por gerenciador remoto (`mcumgr`); nome exato da função e do comando: confira na versão (Inferido). | Evita ficar com firmware que não conecta. V-24. | Verificado (mecanismo); API Inferido |
| M-05 | Downgrade: por versão apenas no overwrite-only, ou por contador de segurança em armazenamento confiável nos demais modos; decisão registrada. | Impede que uma imagem antiga vulnerável volte. V-24. | Verificado |
| M-06 | Resultados FAIL e PANIC interrompem o boot: o produto tem comportamento definido (modo de recuperação, LED, reinício controlado), não laço de reinício. | Evita tijolo silencioso. V-24. | Verificado (interrupção); comportamento do produto é decisão |
| M-07 | `CONFIG_BOOTLOADER_MCUBOOT` no `prj.conf` (ou `SB_CONFIG_BOOTLOADER_MCUBOOT` no sysbuild) habilitado; assinatura automática com a chave configurada ou com `scripts/imgtool.py`. | Imagem sem assinatura correta é rejeitada. V-44. | Verificado |
| M-08 | Chave de exemplo do repositório não configurada em produção; build de produção falha se a chave de desenvolvimento estiver ativa. | A documentação diz que a chave de exemplo "should never be used for production". V-44. | Verificado (frase); a falha de build é regra de revisão da fábrica |
| M-09 | Chave privada de produção em HSM ou cerimônia de assinatura; nunca em repositório, `prj.conf`, CI sem cofre ou log. | A tabela de custódia da documentação coloca a chave privada de produção em "HSM, signing ceremony, release team only". V-44. | Verificado |
| M-10 | Nomes de Kconfig da chave de assinatura (há dois na documentação) conferidos na árvore do Zephyr da versão em uso. | A página não esclarece os dois nomes. V-44. | Não verificável sem a árvore |
| M-11 | Gerenciamento remoto de imagem (`mcumgr`): é o único mecanismo de upgrade de imagem suportado hoje no Zephyr segundo a página; transporte autenticado e canal protegido. | Superfície de ataque do dispositivo. V-24. | Verificado (suporte); proteção do transporte Inferido |
| M-12 | Guias por plataforma (nRF, STM32) não foram lidos; a revisão desses alvos exige o guia do fabricante. | Lacuna declarada. V-44. | Não verificável |

## ESP-IDF OTA

| # | Verificação | Motivo | Rótulo |
| --- | --- | --- | --- |
| E-01 | Partições `ota_0` e `ota_1` mais `otadata` de dois setores (0x2000 bytes); partição de fábrica mantida. | A de fábrica não sofre rollback e serve de recuperação. V-46. | Verificado |
| E-02 | Estados da imagem entendidos: NEW, PENDING_VERIFY, VALID, INVALID, ABORTED (e UNDEFINED). | O bootloader decide pelo estado. V-46. | Verificado |
| E-03 | Confirmação controlada pela aplicação: `esp_ota_mark_app_valid_cancel_rollback()` chamado **depois do autoteste** (rede, sensores, barramentos principais). A confirmação automática é o padrão (símbolo citado na página: `CONFIG_BOOTLOADER_APP_ROLLBACK_CONFIRM_ON_STARTUP`) e acontece após a inicialização dos componentes, pouco antes de `app_main`; para exigir autoteste, desligue-a e confirme manualmente. | Confirmação precoce impede o rollback de uma imagem sem conectividade. V-46. | Verificado |
| E-04 | Rollback habilitado no bootloader (opção de rollback do ESP-IDF; a página `latest` lida em 2026-10-10 cita `CONFIG_BOOTLOADER_APP_ROLLBACK`, "enabled by default"; em versões anteriores o símbolo era `CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE`, Inferido; confira no `menuconfig` e no `sdkconfig` da versão instalada) e **testado em bancada** com imagem de teste que falha o autoteste. | Teste prova a reversão; leitura de configuração não. V-46. | Verificado (símbolo da página `latest`); nome em versões anteriores Inferido; requisito Verificado |
| E-05 | `ESP_ERR_OTA_ROLLBACK_FAILED` tratado: não há app válida na outra partição. | Caminho de erro explícito. V-46. | Verificado |
| E-06 | Anti-rollback decidido de propósito: usa versão de segurança em eFuse (`CONFIG_BOOTLOADER_APP_ANTI_ROLLBACK`) e exige confirmação controlada pela aplicação; é **ação humana** permanente na prática. | Impede downgrade, mas um erro de versão no eFuse não se desfaz. V-46, V-45. | Verificado (mecanismo); "permanente na prática" Inferido |
| E-07 | Tamanho das partições dimensionado após medir a flash real e o tamanho da imagem; deixar margem de crescimento. | Partição pequena para a próxima versão quebra o OTA. V-61 (prática destilada) | Inferido |
| E-08 | Assinatura da imagem OTA tratada na seção Secure Boot v2 abaixo (a página de OTA não cobre assinatura). | V-46, V-45. | Verificado (ausência na página) |

## Secure Boot v2 do ESP-IDF

Cobertura da página lida: ESP32 a partir da revisão v3.0. Para outras variantes use a página da variante (Não verificável aqui).

| # | Verificação | Motivo | Rótulo |
| --- | --- | --- | --- |
| B-01 | Esquema RSA-PSS; a ROM verifica o bootloader de segundo estágio, que verifica cada app. | Cadeia de confiança. V-45. | Verificado |
| B-02 | Digest da chave pública RSA-3072 no eFuse; bit de proteção de escrita ligado e proteção de leitura desligada; `CONFIG_SECURE_BOOT_V2_ALLOW_EFUSE_RD_DIS` mantém a possibilidade de proteger leitura de eFuse depois. | Chave pública não é segredo, mas deve ser imutável. V-45. | Verificado |
| B-03 | Servidor de assinatura remoto: a página diz "can be good practice". | Chave privada fora das máquinas de build. V-45. | Verificado (frase) |
| B-04 | Modo de download pela UART: a página recomenda desabilitar; estado declarado no checklist. JTAG: desabilitado por padrão quando o secure boot liga; estado declarado. | Superfícies de depuração e de recuperação. V-45. | Verificado |
| B-05 | Queima de eFuse, geração da chave de produção e ligação de secure boot são ações humanas; o agente não emite comando. | V-27, V-45. | Verificado (política) |
| B-06 | A página não usa "irreversível" nem "one-time"; use "permanente na prática". | Precisão. V-45. | Verificado |

## Comparação e decisão

Inferida a partir de V-44 e V-46 (as semelhanças são Inferido):

| Aspecto | MCUboot (Zephyr) | ESP-IDF |
| --- | --- | --- |
| Onde mora o estado | trailer do slot / dados do MCUboot | `otadata` (dois setores) |
| Reversão | swap de teste e reset sem confirmação | estados PENDING_VERIFY e rollback |
| Recuperação | outro slot, modo de recuperação do produto | partição de fábrica |
| Assinatura | imagem assinada, chave pública casada por hash | Secure Boot v2 (RSA-PSS) com digest em eFuse |
| Downgrade | versão (overwrite-only) ou contador de segurança | anti-rollback por eFuse |
| Ação humana permanente | chave de produção em HSM; proteção de leitura | eFuse de chave, anti-rollback, criptografia de flash |

Decisão para o relatório: escreva qual modo e qual política de downgrade o produto adota e **por quê** (custo de reversão, recuperação em campo, risco de ataque de downgrade); registre alternativas descartadas (modelo ADR no agente `embedded-architect`).

## Testes de bancada do caminho de atualização

Todos exigem placa, passam pelo gate de `hw-bench-loop` (cartão de gravação, confirmação) e geram registro de evidência nível "em hardware".

1. **Atualização feliz**: imagem N para N+1 com autoteste ok; confirmar que a imagem fica válida e o estado reflete isso.
2. **Imagem que falha o autoteste**: deve reverter automaticamente à imagem anterior (E-04, M-04).
3. **Queda de energia no meio da transferência e no meio do swap**: o dispositivo deve voltar com uma imagem válida (anterior ou nova), nunca sem imagem. Execução exige ferramenta de corte de energia controlada (Suposição de bancada).
4. **Imagem com assinatura inválida ou truncada**: deve ser rejeitada sem substituir a atual.
5. **Downgrade**: conforme a política decidida (rejeitar, permitir só em fábrica).
6. **Sem rede após atualização**: o autoteste deve falhar e reverter, em vez de confirmar.

## Canal de download

Inferido (conhecimento estável; as fontes lidas não tratam do transporte da imagem):
- Transporte autenticado e cifrado (TLS) com validação de certificado do servidor; decisão explícita sobre o bundle de autoridades ou fixação de certificado.
- A imagem é verificada pela assinatura de qualquer forma; o transporte não substitui a assinatura.
- O dispositivo não aceita URL de atualização de fonte não autenticada; credenciais de acesso ao servidor de atualização não ficam no firmware versionado.
- Limite de tamanho e de tentativas, e backoff, para o cliente de download (ver `bus-protocol-review` para rede).
