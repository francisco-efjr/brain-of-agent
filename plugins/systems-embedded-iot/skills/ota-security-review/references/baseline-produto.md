# Baseline de segurança de produto IoT: perguntas, não texto de norma

Uso: passo 5 da skill `ota-security-review`. As 13 perguntas derivam dos **títulos** das provisões da ETSI EN 303 645 V2.1.1 (junho de 2020) e os temas de capacidade derivam da NIST IR 8259A; o texto das normas não é reproduzido. A ETSI reserva todos os direitos: só títulos e paráfrase (V-43). O NISTIR 8259 de 2020 foi retirado em 20/04/2026; a referência atual é a IR 8259 Rev. 1, "Foundational Cybersecurity Activities for IoT Product Manufacturers", publicada em abril de 2026 (V-42). Lidas em 2026-10-10.

Escopo: a EN 303 645 trata de IoT de **consumo**. A skill não afirma conformidade legal nem certificação (V-43). Para produto industrial ou outro mercado, use as perguntas como ponto de partida e declare o que falta.

Sumário: [Como aplicar](#como-aplicar) · [13 perguntas derivadas da ETSI](#13-perguntas-derivadas-da-etsi) · [Temas de capacidade NIST 8259A](#temas-de-capacidade-nist-8259a) · [ISVS como índice](#isvs-como-índice) · [Pergunta por evidência](#pergunta-por-evidência)

## Como aplicar

1. Para cada pergunta, procure evidência no repositório e na documentação do produto (configuração, código, processo). Registre Verificado (visto), Inferido ou Não verificável.
2. Quando a resposta depende de processo da empresa (relato de vulnerabilidades, política de suporte), peça o documento: o repositório de firmware não prova política.
3. Cite o número da provisão; distinga "shall" de "should" **apenas** nos itens abaixo, que foram lidos como tal (V-43). Nos demais, não atribua força normativa sem abrir o PDF.
4. Achado de produto sem arquivo:linha tem "Local: processo/documento"; peça o artefato.

## 13 perguntas derivadas da ETSI

| Provisão (título) | Pergunta de produto | O que procurar | Força lida |
| --- | --- | --- | --- |
| 5.1 Sem senhas padrão universais | Cada dispositivo tem credencial única ou definida pelo usuário? Existe senha de fábrica igual em toda a frota? | provisionamento, arquivos de configuração, strings no binário | 5.1-1 "shall" (V-43) |
| 5.2 Gestão de relatos de vulnerabilidade | Existe canal público para relatar vulnerabilidade e processo de tratamento? | política de divulgação, contato de segurança | não lida |
| 5.3 Manter o software atualizado | Os componentes são atualizáveis com segurança? O dispositivo verifica atualizações após inicializar e periodicamente? Há período de suporte declarado? | mecanismo OTA, assinatura, agenda de verificação | 5.3-1 "should"; 5.3-5 "should" (V-43) |
| 5.4 Armazenar parâmetros sensíveis com segurança | Chaves, tokens e dados pessoais ficam em armazenamento protegido (não em texto simples na flash)? | NVS cifrada, elemento seguro, criptografia de flash | não lida |
| 5.5 Comunicar com segurança | Toda comunicação sensível usa canal autenticado e cifrado; parâmetros críticos de segurança são gerenciados com segurança? | TLS e validação de certificado, MQTT na porta 8883 (V-33) | 5.5-8 gestão segura de parâmetros críticos (V-43) |
| 5.6 Minimizar superfícies de ataque expostas | Portas, serviços e interfaces de depuração desnecessários estão desligados (UART de download, JTAG, servidor web, mDNS)? | configuração de rede, `sdkconfig`, estado de JTAG (V-45) | não lida |
| 5.7 Garantir a integridade do software | O software é verificado por assinatura no boot e na atualização? Adulteração é detectada? | secure boot, assinatura de imagem (V-44, V-45) | não lida |
| 5.8 Proteger dados pessoais | Que dados pessoais o dispositivo coleta, onde ficam, como saem? | telemetria, logs, campos de payload | não lida |
| 5.9 Resiliência a quedas | O dispositivo continua funcionando de forma segura e se recupera após queda de rede ou de energia? | reconexão, watchdog, testes de queda (ver `checklist-ota.md`) | não lida |
| 5.10 Examinar dados de telemetria | A telemetria é examinada quanto a anomalias de segurança? Há registro de eventos relevantes? | log de eventos, métricas, motivo de reset | não lida |
| 5.11 Facilitar a exclusão de dados do usuário | O usuário consegue apagar seus dados e restaurar o dispositivo? | função de reset de fábrica, apagamento seguro | não lida |
| 5.12 Facilitar instalação e manutenção | Instalar, configurar e manter é simples e seguro? Há feedback físico simples (LED, botão) para estados críticos? | fluxo de provisionamento, indicadores | não lida |
| 5.13 Validar dados de entrada | Toda entrada (rede, usuário, interfaces) é validada quanto a tamanho, tipo e conteúdo? | parsers, limites de buffer, rejeição de campos inválidos | não lida |

Mapeamento para outras skills: 5.5 e 5.13 cruzam com `bus-protocol-review` (TLS, validação de payload); 5.3 e 5.7 com o checklist de OTA; 5.6 com a revisão de interfaces de depuração; 5.4 e 5.1 com a custódia de chaves e o provisionamento.

## Temas de capacidade NIST 8259A

A NIST IR 8259A (final, 29/05/2020) define o *Core Baseline* de capacidades de dispositivo e se usa com a série 8259 (hoje Rev. 1) (V-42). Os rótulos de capacidade abaixo são os temas tradicionais da série e **devem ser conferidos no PDF da 8259A antes de publicar o texto** (Inferido, V-42):

| Tema | Pergunta |
| --- | --- |
| Identificação do dispositivo | O dispositivo tem identificador único e verificável, e a frota é inventariável? |
| Configuração do dispositivo | A configuração de segurança pode ser alterada apenas por entidades autorizadas? |
| Proteção de dados | Dados armazenados e em trânsito estão protegidos? |
| Acesso lógico às interfaces | O acesso às interfaces locais e de rede é controlado? |
| Atualização de software | O software pode ser atualizado com segurança? |
| Consciência do estado de segurança | O dispositivo registra e expõe eventos e estado de segurança? |

Não atribua "seis atividades" à Rev. 1: a página lida não as enumera (V-42). As atividades da Rev. 1 são do fabricante antes da venda; abra o PDF para qualquer afirmação sobre elas.

## ISVS como índice

O ISVS (OWASP IoT Security Verification Standard) está em release candidate 1.0.0-RC2, "not yet a finalized standard", CC BY-SA 4.0 (V-41). Use só os cinco capítulos como roteiro de perguntas de projeto, sem copiar texto: ecossistema (V1), aplicação de espaço de usuário (V2), plataforma de software (V3), comunicação (V4) e plataforma de hardware (V5). O OWASP IoT Top 10 de 2018 não foi lido (PDF 404): não cite categorias. O FSTM (metodologia de ataque a firmware em nove estágios) só se aplica com autorização escrita do dono do dispositivo; não é parte deste fluxo.

## Pergunta por evidência

Exemplo de linha do checklist preenchido:

| Pergunta | Evidência | Local | Rótulo | Ação |
| --- | --- | --- | --- | --- |
| 5.1: credencial única por dispositivo? | `prov.c` lê a senha de um segredo gravado na fábrica; mas `config.h` define `DEFAULT_ADMIN_PASS` | `config.h:17` | Verificado | remover a senha padrão e exigir provisionamento por dispositivo |
| 5.2: canal de relato de vulnerabilidade? | não há `SECURITY.md` nem contato no repositório | processo/documento | Não verificável | pedir o documento de política ao responsável |
