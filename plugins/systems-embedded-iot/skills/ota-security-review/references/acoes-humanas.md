# Ações humanas: operações permanentes e como responder a pedidos de comando

Uso: passo 4 da skill `ota-security-review` e agente `iot-security-auditor`. Fontes lidas em 2026-10-10: V-27 (portões de operação irreversível), V-62 (extensão de V-27 e V-21), V-45 (Secure Boot v2 do ESP-IDF), V-44 (MCUboot), V-46 (anti-rollback). Princípio: a skill ajuda a decidir e a se preparar; a execução de operações permanentes é de uma pessoa responsável, com o procedimento oficial do fabricante aberto. O plugin não emite comando copiável para elas.

Sumário: [Quais operações](#quais-operações) · [Cartão de ação humana](#cartão-de-ação-humana) · [Pré-requisitos gerais](#pré-requisitos-gerais) · [Responder a "dê o comando"](#responder-a-dê-o-comando) · [O que o agente pode fazer](#o-que-o-agente-pode-fazer)

## Quais operações

Tratar como ação humana (permanente na prática ou de alto custo de erro):

- queima de eFuse ou OTP, inclusive digest de chave, bits de proteção, versão de segurança do anti-rollback;
- geração, importação e custódia de chaves de produção (assinatura de imagem, secure boot, criptografia de flash);
- ligação de secure boot e de criptografia de flash em produto real;
- proteção permanente de leitura/escrita (por exemplo, proteção de leitura da flash do fabricante), desabilitar JTAG ou o modo de download de forma permanente;
- anti-rollback: usa versão de segurança em eFuse (V-46);
- qualquer operação em lote em linha de produção que repita uma das anteriores.

A página de Secure Boot v2 não usa "irreversível" nem "one-time": o fato é "permanente na prática", inferido da proteção de escrita (V-45).

## Cartão de ação humana

Um cartão por operação, entregue no relatório. Não contém comandos.

```text
AÇÃO HUMANA NECESSÁRIA: <nome curto, ex.: "Ligar Secure Boot v2 no lote A">
Plataforma e versão: <ESP-IDF x.y / MCUboot z / ...>     Variante e revisão do silício: <...>
O que a operação faz (em linguagem simples): <...>
Por que é permanente na prática: <...>
Pré-requisitos: <caminho de recuperação confirmado; chave privada em HSM ou servidor de assinatura; ensaio em unidades de desenvolvimento; estado atual de proteção de leitura e escrita; decisão sobre JTAG e download pela UART; plano de OTA depois da operação>
Riscos: <unidade inutilizada; imagem sem assinatura válida não inicia; perda de capacidade de depuração; ...>
Como seria a recuperação: <...ou "não há">
Documentação oficial a seguir: <URL da página do fabricante, na versão usada>
Quem executa e aprova: <responsável humano, sugerido: ...>
Evidência a registrar depois: <leitura de verificação, versão, data, unidade/lote>
Fora do escopo do agente: gerar o comando, executar, ou "colar na linha de produção".
```

## Pré-requisitos gerais

Antes de qualquer operação permanente:

1. **Caminho de recuperação confirmado** por quem executa (sem ele, não existe procedimento de escrita; V-27).
2. **Ensaio em unidades de desenvolvimento** que reproduzem as variantes e revisões de produção, incluindo a falha proposital (imagem não assinada, rollback) e a recuperação possível.
3. **Chave privada de produção** em HSM ou servidor de assinatura remoto, fora do repositório e das máquinas de build; chave de exemplo do repositório nunca em produção (V-44, V-45).
4. **Estado atual dos eFuses lido e registrado** antes (leitura é livre; a leitura de eFuse com ferramenta do fabricante é operação de leitura, mas confirme na documentação da ferramenta que não escreve).
5. **Documentação da versão** do fabricante aberta e conferida; scripts de produção revisados por outra pessoa.
6. **Decisão registrada** (ADR) sobre o que acontece com atualizações depois da operação: como serão assinadas, quem tem a chave, como se rotaciona.
7. **Gravação em lote**: primeiro uma unidade, depois conferência, depois o lote. O agente não conduz esse processo.

## Responder a "dê o comando"

Quando o usuário pede comandos prontos para a operação permanente:

1. Diga que não fornecerá comando copiável para essa operação, e por quê (permanente na prática; um erro se multiplica pela quantidade de unidades). Calmo, sem sermão.
2. Entregue o que ajuda: pré-requisitos, riscos, as decisões que precisam estar tomadas, a documentação oficial da versão (URL das fontes lidas: Secure Boot v2 e OTA do ESP-IDF; documentação do MCUboot), e o cartão de ação humana.
3. Ofereça trabalho que o agente pode fazer: revisar `sdkconfig`, `partitions.csv`, devicetree e `prj.conf`; preencher o checklist; escrever o plano de ensaio e o registro de evidências; preparar o roteiro de teste de recuperação para a bancada (com gate).
4. Se o usuário insistir ou colar um comando de outra fonte e pedir "valide": analise o texto como leitura (o que o comando faria, que pré-requisitos faltam), sem executá-lo e sem prometer que é seguro.

Exemplo de resposta curta:

> Não vou escrever comandos prontos de gravação de eFuse e de chave, porque são permanentes na prática e numa linha de produção o erro se repete em cada unidade. Posso preparar: o cartão de ação humana com pré-requisitos e riscos, a revisão do seu `sdkconfig` e das partições, o checklist e o plano de ensaio em unidades de desenvolvimento. A documentação oficial a seguir é a página de Secure Boot v2 do ESP-IDF da versão que você usa. Quer que eu revise a configuração agora?

## O que o agente pode fazer

- Ler configuração, partições, scripts de build e documentação fornecida.
- Listar pré-requisitos, riscos e decisões; redigir o ADR de política de chaves e de downgrade (via `embedded-architect`).
- Escrever o roteiro de ensaio e o modelo de registro, sem executá-los.
- Aplicar o gate de `hw-bench-loop` ao que for gravação comum (firmware de aplicação em unidade de desenvolvimento), com cartão e confirmação.
- Recusar e encaminhar, sem emitir comando, qualquer operação da lista da seção "Quais operações".
