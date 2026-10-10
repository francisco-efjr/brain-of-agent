# Checklist de OTA, chaves e segurança de dispositivo - <produto / versão>

Fontes: V-24, V-27, V-42 a V-46 (ver `references/ota-e-seguranca-iot.md`). Este checklist **não contém comando de queima de eFuse, geração de chave de produção ou ativação de proteção permanente**: esses itens viram "Ação humana necessária". Textos de ETSI e NIST não são reproduzidos; as perguntas são redação própria. Status por item: OK (evidência), FALHA, PENDENTE, N/A (motivo) ou NV (não verificável). Rótulo: Verificado, Inferido, Suposição.

Plataforma: [MCUboot (Zephyr) / ESP-IDF OTA] · Modo: [swap offset / move / overwrite / XIP; ou otadata + ota_0/ota_1] · Mercado: [consumo -> ETSI aplica / outro]

## 1. OTA

| # | Item | Status | Evidência | Rótulo |
| --- | --- | --- | --- | --- |
| O1 (*) | Imagem assinada e verificada antes do boot | | | |
| O2 (*) | Confirmação só após autoteste (rede, sensores, barramentos principais), controlada pela aplicação | | | |
| O3 (*) | Reversão automática se não confirmar, testada em bancada (imagem que trava; imagem que não confirma) | | | |
| O4 | Partição de fábrica mantida como recuperação | | | |
| O5 | Modo de upgrade casa com o caminho de recuperação | | | |
| O6 | Política de downgrade decidida (versão / contador de segurança / anti-rollback em eFuse) | | | |
| O7 | Download com TLS e validação de certificado | | | |
| O8 | Queda de energia no meio do OTA deixa estado recuperável (testado cortando energia) | | | |
| O9 | Versão reportada ao backend após o boot | | | |

## 2. Chaves e segredos

| # | Item | Status | Evidência | Rótulo |
| --- | --- | --- | --- | --- |
| C1 (*) | Chave de exemplo/desenvolvimento ausente do build de produção (build falha se configurada) | | | |
| C2 (*) | Chave privada de produção fora do repositório, `prj.conf`, `sdkconfig` e logs; em HSM ou cerimônia de assinatura | | | |
| C3 | Credenciais (Wi-Fi, broker, tokens) não versionadas; provisionamento fora do código | | | |
| C4 | Segredos por dispositivo (não universais) | | | |

## 3. Portão de irreversíveis (listar, não executar)

| Operação | Necessária? | Pré-requisitos levantados | Caminho de recuperação | Aprovador humano |
| --- | --- | --- | --- | --- |
| eFuse / OTP (digest de chave, bits de proteção) | | | | |
| Secure boot | | | | |
| Criptografia de flash | | | | |
| Proteção de leitura permanente / RDP | | | | |
| Anti-rollback por contador em eFuse | | | | |
| Desabilitar JTAG / modo de download pela UART | | | | |

Estado declarado de JTAG e download pela UART: <...>. Ensaio em unidades de desenvolvimento: <quantas, resultado>.

## 4. Baseline de produto (13 perguntas, paráfrase de títulos do ETSI EN 303 645 V2.1.1)

| Provisão | Pergunta | Resposta e evidência | Status |
| --- | --- | --- | --- |
| 5.1 | Senha única por dispositivo ou definida pelo usuário (sem padrão universal)? | | |
| 5.2 | Canal e processo para relato de vulnerabilidades? | | |
| 5.3 | Software atualizável com segurança; verifica atualizações após iniciar e periodicamente? | | |
| 5.4 | Parâmetros sensíveis armazenados com segurança? | | |
| 5.5 | Comunicação segura e gestão segura de parâmetros críticos? | | |
| 5.6 | Superfície de ataque mínima (portas, serviços, depuração)? | | |
| 5.7 | Integridade do software verificada? | | |
| 5.8 | Dados pessoais protegidos e minimizados? | | |
| 5.9 | Resiliência a quedas de rede/energia? | | |
| 5.10 | Telemetria examinada quanto a dados sensíveis? | | |
| 5.11 | Usuário apaga seus dados com facilidade? | | |
| 5.12 | Instalação e manutenção simples? | | |
| 5.13 | Entradas validadas? | | |

Capacidades do NIST IR 8259A (temas tradicionais da série; **conferir no PDF antes de publicar**: Inferido): identificação, configuração, proteção de dados, controle de acesso lógico, atualização de software, consciência de estado. NISTIR 8259 (2020) foi retirado em 20/04/2026: use a Rev. 1.

## 5. Ações humanas necessárias

- <lista priorizada: quem, o quê, quando>

## 6. Fora de escopo / Não verificável

- Conformidade legal não é afirmada. Segurança funcional (IEC 61508, ISO 26262, DO-178C) não é afirmada. Testes ativos contra dispositivos de terceiros só com autorização escrita do usuário (FSTM).
