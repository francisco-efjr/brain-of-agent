Com 10 dias úteis, 1 QA e zero automação, você não consegue testar tudo. A estratégia é decidir o que NÃO vai ficar sem teste (dinheiro e dados do cartão), automatizar só o que se repete a cada deploy, e transformar os 4 devs em parte da estratégia de qualidade. Segue um plano que dá para começar amanhã.

## 1. Princípio: priorize por risco, não por tela

Em cartão de crédito, o que mais machuca (financeira e reputacionalmente) é, nesta ordem:

1. **Dinheiro errado**: limite concedido/consumido errado, cobrança duplicada, fatura com valor ou vencimento errado.
2. **Dados do cartão expostos**: número, CVV e validade vazando em log, resposta de API, URL, e-mail ou ferramenta de monitoramento.
3. **Acesso indevido**: um cliente vendo cartão ou fatura de outro (IDOR), ou gerando cartão sem passar pela aprovação.
4. **Fluxo travado**: cliente aprovado que não consegue gerar o cartão, ou compra recusada sem motivo.
5. **Cosmético / UX**: fica por último e só entra se sobrar tempo.

## 2. Divisão do trabalho (a parte mais importante)

| Camada | Quem | O quê |
|---|---|---|
| Testes unitários das regras de cálculo | **Devs** | Limite, juros/encargos, fechamento e vencimento da fatura, arredondamento, estorno. Peça isso formalmente: "nenhuma regra de cálculo entra sem teste unitário com valores de borda". É o que mais reduz o seu risco. |
| API automatizada do fluxo crítico | **Você** (com 1 dev ajudando no dia 1-2) | Smoke do fluxo ponta a ponta + regras de negócio de maior risco |
| Exploratório manual | **Você** | Tudo o que é novo, visual, ambíguo ou de difícil automação |
| Bug bash | **Time todo** | 1 hora no dia 8, cada um tentando quebrar o fluxo que NÃO escreveu |

Sobre automação: em 10 dias, **automatize em nível de API, não de UI**. É mais rápido, mais estável e pega o que importa (cálculo e regra). Use a ferramenta que os devs já dominam (Postman/Newman, pytest, Playwright em modo API, REST-assured etc.) para que eles consigam manter depois. No máximo 1 ou 2 testes E2E de UI cobrindo o caminho feliz. Rode a suíte a cada deploy em staging; mesmo uma suíte pequena que roda sempre vale mais que uma grande que ninguém roda.

## 3. Calendário sugerido

| Dia | Foco |
|---|---|
| **1** | Reunião de 2-3h com PO e devs: escopo exato, critérios de aceite, integrações (processadora/emissor, bureau/score, bandeira, antifraude, meio de pagamento da fatura), regras de negócio por escrito, ambientes e massa de dados. Montar a matriz de risco (seção 1) e definir os critérios de go/no-go (seção 6). |
| **2-3** | Setup de ambiente e massa de dados. Esqueleto da automação de API: criar solicitação, aprovar limite, gerar cartão, fazer compra, consultar fatura. Em paralelo, testar manualmente o que já estiver em staging. Peça aos devs para entregar **na ordem do fluxo** (solicitação primeiro, fatura por último) e testar cada pedaço quando ficar pronto, em vez de esperar tudo no dia 7. |
| **4-6** | Testes profundos por módulo (seção 4), começando por aprovação de limite, compra e fatura. Cada bug automatizável vira teste de regressão. |
| **7** | Segurança e dados sensíveis (seção 5), concorrência, falhas de integração (timeout, indisponibilidade). |
| **8** | Fluxo completo ponta a ponta, **bug bash** de 1h, triagem de bugs. |
| **9** | **Congelamento de código** (só correção de bug bloqueante). Regressão automatizada + smoke manual em ambiente igual ao de produção. |
| **10** | Go/no-go de manhã. Se for go: deploy, smoke em produção com contas internas, monitoramento ativo. |

Reserve **30-40% do tempo para reteste de correções**. Quem planeja só "testar" e esquece o ciclo bug-corrige-reteste estoura o prazo. Se algum dia as features ainda não estiverem prontas, não espere parado: escreva casos e automação contra o contrato da API/mocks.

## 4. O que testar em cada etapa (os casos de maior valor)

**Solicitação**
- Validação de CPF, idade mínima, dados obrigatórios, campos com tamanho/caracteres extremos.
- Solicitação duplicada (duplo clique, reenvio, dois dispositivos), cliente que já tem cartão ou já tem solicitação em análise.
- Falha de KYC/antifraude, abandono e retomada do fluxo, consentimento (LGPD) registrado.
- Mensagens de erro que não revelam informação demais.

**Aprovação de limite**
- Valores de borda de cada faixa da política de crédito (exatamente no corte, 1 centavo acima e abaixo).
- Negado, aprovado parcial, aprovado total; limite mínimo e máximo; arredondamento.
- Bureau/score indisponível ou lento (timeout): o que acontece? Cliente fica preso, é aprovado por engano ou é negado com mensagem correta?
- Reanálise, e trilha de auditoria: quem/qual regra decidiu e quando.
- Não dá para gerar cartão sem limite aprovado (tente pular a etapa chamando a API direto).

**Geração do cartão**
- Número válido (Luhn), BIN correto, validade e CVV gerados; unicidade.
- **Idempotência**: um retry ou timeout não pode gerar dois cartões nem duas cobranças de emissão.
- Exibição de dados completos só após autenticação; mascaramento nas demais telas.
- Bloqueio, cancelamento, segunda via/reemissão e o que acontece com compras em andamento.

**Compra online**
- Aprovada, recusada por limite (limite exato, 1 centavo a mais), valor mínimo, centavos.
- Cartão bloqueado, cancelado, vencido, CVV/validade errados, autenticação adicional (3DS ou equivalente, se houver).
- **Concorrência**: duas compras simultâneas que juntas estouram o limite. Este é o clássico bug de fintech.
- Timeout do autorizador: o limite fica retido? Há desfazimento da autorização?
- Reenvio da mesma transação (idempotência), estorno total e parcial, cancelamento, compra pendente versus lançada.
- Parcelamento (se existir) e moeda estrangeira (se existir).

**Fatura**
- Fechamento e vencimento: virada de mês, dias 29/30/31, fevereiro, fuso horário, vencimento em fim de semana/feriado.
- Compra feita antes e depois do fechamento cai na fatura certa.
- Soma bate com os lançamentos; estornos e créditos aplicados corretamente.
- Pagamento total, parcial, mínimo, atrasado, pagamento a maior; liberação do limite após pagar.
- Juros, multa, IOF e encargos: **peça as fórmulas e exemplos numéricos ao negócio** e transforme em casos. Dinheiro deve ser tratado como decimal, nunca float; procure erro de arredondamento de centavos.
- Consistência entre fatura em tela, PDF, boleto/PIX e o que o back-end considera devido.

## 5. Transversais que não podem ficar de fora

- **Dados sensíveis**: confira logs, respostas de API, URLs, e-mails, ferramentas de monitoramento e analytics. Número completo e CVV não podem aparecer em lugar nenhum fora da exibição autenticada. Não use dados reais de clientes em staging.
- **Autorização**: troque o ID na requisição e tente acessar cartão/fatura de outro usuário; acessar endpoints sem token ou com token expirado; tentar alterar limite pelo cliente.
- **Abuso**: rate limit em solicitação e em exibição de dados do cartão; tentativas repetidas.
- **Resiliência**: o que acontece se uma integração cair no meio do fluxo? O cliente fica com dinheiro/limite/estado inconsistente?
- **Reconciliação**: o saldo/limite que o sistema mostra bate com o que a processadora registra?
- **Mobile e acessibilidade básica**: o fluxo funciona no celular (provavelmente seu principal canal) e é navegável por leitor de tela nas telas principais.
- **Performance mínima**: um teste simples de carga na compra e na consulta de fatura, só para saber que não cai com o primeiro pico.

## 6. Critérios de go/no-go (defina no dia 1, não no dia 10)

Sugestão de base, ajuste com o PO:

- Zero bugs abertos de severidade crítica (dinheiro errado, dado do cartão exposto, acesso a dados de outro cliente, fluxo principal quebrado).
- Fluxo completo (solicitação até fatura) passando no ambiente de pré-produção, e a suíte automatizada verde.
- Cálculos de limite e fatura validados contra exemplos numéricos fornecidos pelo negócio.
- Plano de rollback e monitoramento definidos.
- Bugs menores abertos estão listados, com dono e prazo.

## 7. Reduza o risco do lançamento em si

Mesmo com bom teste, 10 dias para um produto financeiro é apertado. Proponha ao PO um lançamento **gradual**:

- **Feature flag / kill switch** para desligar a emissão ou a compra rapidamente.
- Primeiro, **funcionários e um grupo pequeno de clientes** (lista restrita), com limites baixos.
- Dashboard e alertas desde o dia 1: taxa de erro por etapa, compras recusadas, divergência de conciliação, tempo de resposta.
- Conciliação diária manual nas primeiras semanas.
- Um canal de plantão com dev de prontidão nos primeiros dias.

Isso transforma "todos os bugs que não achei" em "bugs que afetam poucas pessoas e que dá para corrigir".

## 8. Comunique o que NÃO será coberto

Dia 1 ou 2, envie ao PO e à liderança um resumo curto: o que será testado a fundo, o que só superficialmente e o que não será testado. Isso protege você e o produto, e permite que alguém decida conscientemente aceitar o risco, em vez de descobrir no dia 11.

## 9. Perguntas que mudam o plano (faça no dia 1)

1. O cartão é emitido de verdade (via processadora/BIN patrocinador) ou simulado nesta primeira versão? Existe sandbox da processadora e da bandeira?
2. Há alguma certificação ou homologação externa (bandeira, processadora, regulador, compliance/PCI) com prazo próprio? Elas costumam levar mais tempo que os testes e podem ser o verdadeiro caminho crítico.
3. Quem define e valida as regras de crédito, juros e encargos? Elas estão por escrito?
4. Quais ambientes existem hoje (dev, staging, pré-prod) e qual é parecido com produção?
5. Qual é a stack dos devs, para escolher a ferramenta de automação que eles consigam manter?
6. O prazo de 10 dias é inegociável? Se for, o que pode sair do escopo (por exemplo, parcelamento ou moeda estrangeira) para proteger o essencial?

---

**Resumo para os primeiros 2 dias:** (1) reunião de alinhamento e matriz de risco; (2) pedir testes unitários dos cálculos aos devs; (3) ambiente + massa de dados; (4) automação de API do caminho feliz, rodando a cada deploy; (5) começar o exploratório por aprovação de limite, compra e fatura; (6) mandar o resumo de cobertura ao PO.

Se quiser, posso montar a matriz de risco em planilha, uma lista de casos de teste para um dos módulos (por exemplo, fatura) ou o esqueleto da automação de API na ferramenta que você escolher.
