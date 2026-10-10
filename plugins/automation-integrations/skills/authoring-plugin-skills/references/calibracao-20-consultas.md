# Calibração da `description` com 20 consultas

Fonte: protocolo do `skill-creator` de `anthropics/skills` (V-07: 20 consultas, divisão 60/40, 3 execuções por consulta, até 5 iterações), redação própria; o repositório não declara licença e seus scripts (`run_loop` e semelhantes) não foram lidos nem executados aqui. Este roteiro funciona sem eles. Verificado em 2026-10-10 contra `VALIDATED.md`.

Sumário: 1. Quando usar · 2. Protocolo · 3. Exemplo de 20 consultas · 4. Como medir o disparo · 5. Regras de ajuste · 6. Registro.

## 1. Quando usar

- A skill não dispara com pedidos naturais (undertriggering) ou dispara em pedidos de outro assunto (overtriggering).
- Depois de mudar a `description` de qualquer skill do mesmo plugin: gatilhos parecidos competem (por exemplo, `playbook` contra `reviewing-webhook-receivers`).
- Antes de publicar um plugin novo.

## 2. Protocolo

1. Escreva 20 pedidos como o usuário escreveria, com ruído real (abreviações, código colado, português e inglês): **10 que devem disparar** e **10 quase-acertos** que compartilham palavras mas pedem outra ferramenta.
2. Separe 40% (4 positivos e 4 negativos) como conjunto de **teste**; os outros 60% são de **treino**. Ajuste a descrição olhando só o treino.
3. Rode a descrição atual (versão A) e registre, por consulta, se a skill disparou. Rode cada consulta 3 vezes: um disparo isolado é ruído (V-07; princípio de várias execuções).
4. **Guarde uma cópia da versão A** antes de editar.
5. Ajuste para cobrir os positivos de treino sem absorver os negativos de treino. Reexecute (versão B) e compare nos dois conjuntos.
6. Máximo de 5 rodadas. Escolha a versão pela nota do conjunto de teste, não do treino.
7. Desconfie de asserção que passa com e sem a skill: ela não mede a skill.

## 3. Exemplo (skill `reviewing-webhook-receivers`)

Devem disparar (P):

| # | Pedido |
| --- | --- |
| P1 | "Meu endpoint do Stripe às vezes processa o mesmo evento duas vezes, olha esse handler" + código |
| P2 | "review my webhook handler for GitHub, tem algo errado na assinatura?" |
| P3 | "o HMAC do webhook nunca bate quando uso express.json(), por quê?" |
| P4 | "preciso reprocessar eventos que falharam, como monto uma dead letter queue pro meu webhook?" |
| P5 | "implementa um receptor de webhook com dedupe por id do evento em Flask" |
| P6 | "o provedor reenviou o evento e mandei e-mail em dobro" |
| P7 | "está certo responder 200 só depois de gravar no banco e chamar a API de frete?" |
| P8 | "verify webhook signature in node, constant time compare" |
| P9 | "construir um bot que recebe eventos do Slack, como valido a requisição?" (dispara com ressalva de plataforma) |
| P10 | "meu webhook recebe eventos fora de ordem, como lidar?" |

Quase-acertos (N), não devem disparar esta skill:

| # | Pedido | Quem deveria responder |
| --- | --- | --- |
| N1 | "como configuro um webhook no repositório do GitHub para disparar meu CI?" | configuração de CI (devops) |
| N2 | "crie um endpoint REST POST /pedidos com validação" | backend-api |
| N3 | "explique o que é HMAC e como funciona SHA-256" | resposta direta |
| N4 | "faça um cron que chama a API de cotação a cada hora" | `designing-workflow-automations` |
| N5 | "este fluxo do n8n envia o e-mail duas vezes, como arrumo?" | `designing-workflow-automations` |
| N6 | "crie um servidor MCP para a API de pedidos" | `building-mcp-servers` |
| N7 | "o botão do formulário fica desalinhado no Safari" | nenhuma skill do plugin |
| N8 | "posso instalar esse plugin que usa npx -y ...@latest?" | `assessing-automation-risk` |
| N9 | "escreva testes para o serviço de pagamentos" | qa-testing |
| N10 | "como o Stripe calcula juros de parcelamento?" | resposta direta / fintech |

Treino: P1-P6, N1-N6. Teste: P7-P10, N7-N10.

## 4. Como medir o disparo

- **Manual:** sessão nova com o plugin carregado (`claude --plugin-dir <pasta>` em sessão de teste), cole o pedido, observe na transcrição se a ferramenta `Skill` foi chamada com o nome esperado. Registre `sim`/`não`.
- **Com `claude plugin eval`** (Claude Code 2.1.269 ou superior): um caso por consulta com grader `tool_used` (`tool: Skill`, `input_match` com o nome da skill). Em execução de dois braços esse grader é só indicador (`scored: false`); para negativos use `arm: both` (V-06).
- Sem nenhuma das duas, a calibração é proposta e o rótulo é Não verificado.

Lembrete: skills com `disable-model-invocation: true` nunca disparam sozinhas; calibre apenas a descrição das que disparam.

## 5. Regras de ajuste

| Sintoma | Ajuste |
| --- | --- |
| Positivos não disparam | acrescente as palavras do usuário (PT e EN) que faltam, em frases curtas; coloque o caso de uso principal primeiro |
| Negativo X dispara | acrescente a fronteira ("Não cobre CI nem endpoint próprio") e retire o termo ambíguo |
| `playbook` dispara no lugar da skill específica | restrinja o playbook a pedidos amplos/roteamento e deixe os gatilhos específicos na skill de tarefa |
| Dispara só em inglês ou só em português | inclua os dois idiomas |
| Passa com e sem a skill | o caso não mede a skill: troque o pedido |

Evite CAPS, "SEMPRE" e "MUST" na descrição (P-03). Mantenha ≤ 1.024 caracteres.

## 6. Registro

| Rodada | Versão | Treino P (x/6) | Treino N sem disparo (x/6) | Teste P (x/4) | Teste N sem disparo (x/4) | Decisão |
| --- | --- | --- | --- | --- | --- | --- |

Guarde as versões das descrições no próprio arquivo de calibração. Reporte o resultado como medido (n execuções, modelo, data), não como garantia.
