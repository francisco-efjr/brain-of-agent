# Bugs e relatórios

Como registrar, classificar, triar, verificar e analisar defeitos, e como
relatar o resultado de um ciclo de testes para quem decide. Leia ao escrever
ou revisar um bug report, ao discutir severidade e prioridade, ao conduzir uma
triagem ou um postmortem e ao montar um relatório de teste.

## Sumário

- [Anatomia de um bug report excelente](#anatomia-de-um-bug-report-excelente)
- [Título e reprodução mínima](#título-e-reprodução-mínima)
- [Evidências e dados pessoais](#evidências-e-dados-pessoais)
- [Severidade e prioridade](#severidade-e-prioridade)
- [Triagem](#triagem)
- [Ciclo de vida e verificação da correção](#ciclo-de-vida-e-verificação-da-correção)
- [Análise de causa raiz e escape analysis](#análise-de-causa-raiz-e-escape-analysis)
- [Comunicação e bug advocacy](#comunicação-e-bug-advocacy)
- [Relatório de teste](#relatório-de-teste)
- [Defeito em produção](#defeito-em-produção)

## Anatomia de um bug report excelente

Um bug report é bom quando quem não estava presente consegue reproduzir,
entender o impacto e decidir **sem perguntar nada**. Cada pergunta de volta
custa horas ou dias, e bug que gera muitas perguntas tende a ser adiado.

| Campo | Por que existe | Armadilha |
| --- | --- | --- |
| Título | é o que aparece na lista, na triagem e na busca por duplicados | descrever a causa suposta ("NullPointer no CupomService") em vez do sintoma |
| Ambiente e versão | o defeito pode existir só em um build, navegador, dispositivo ou ambiente | "última versão"; informe build, commit ou release |
| Pré-condições | estado necessário antes do passo 1: perfil, dados, flag ligada | omitir o que você já tinha configurado e esqueceu |
| Passos | caminho mínimo e numerado até o defeito | 15 passos, dos quais 10 são irrelevantes |
| Resultado esperado | define o oráculo — por que isso é defeito | "deveria funcionar", ou o valor copiado da tela (oráculo circular); cite a regra, o cálculo ou a fonte |
| Resultado obtido | o que de fato aconteceu, com valores | "deu erro" sem mensagem, código ou valor |
| Frequência | separa defeito determinístico de intermitente | "às vezes" sem número |
| Evidência | prova e atalho para o diagnóstico | vídeo de 5 minutos; print sem destaque; dado pessoal exposto |
| Impacto | traduz o defeito para quem prioriza | deixar o PO deduzir |
| Severidade e prioridade sugeridas | ponto de partida para a triagem | inflar para chamar atenção |
| Informações adicionais | contorno, primeira versão afetada, bugs relacionados, hipótese de causa | misturar hipótese com fato; rotule a hipótese |

O mesmo defeito, relatado mal e bem:

| Campo | Ruim | Bom |
| --- | --- | --- |
| Título | Erro no cupom | Checkout: total ignora cupom quando o frete é grátis |
| Ambiente | homolog | Homologação, build 3.8.0-rc2 (commit `3f9c1a2`), Chrome 141, Windows 11 |
| Pré-condições | — | Usuário `cliente.qa01@exemplo.test`; cupom `PRIMEIRA10` (10%, válido até 31/12/2026); frete grátis a partir de R$ 199,00 |
| Passos | Coloquei uns produtos, apliquei o cupom e o valor ficou errado | 1. Adicionar "Fone XZ" (R$ 250,00) ao carrinho. 2. Ir ao checkout com CEP 01310-100. 3. Aplicar `PRIMEIRA10`. |
| Esperado | O valor certo | Total R$ 225,00 = R$ 250,00 − 10% (R$ 25,00) + frete R$ 0,00 (regra RN-12 da história CHK-431) |
| Obtido | Valor errado | Total R$ 250,00. O resumo lista "Cupom −R$ 25,00", mas o valor não é subtraído |
| Frequência | — | 5 de 5 com subtotal ≥ R$ 199,00; 0 de 5 com subtotal de R$ 150,00 (frete pago) |
| Evidência | print da tela inteira | Print com o total destacado; resposta de `POST /api/checkout/totais` (request id `req-7f3a91`) com `desconto: 25.00` e `total: 250.00` |
| Impacto | — | Cliente paga R$ 25,00 a mais em todo pedido com cupom e frete grátis; cobrança indevida pode gerar devolução em dobro (CDC, art. 42, parágrafo único) |
| Sev./Prior. | URGENTE!!! | Severidade Crítica (valor cobrado errado, sem contorno para o cliente); prioridade sugerida P1 — campanha de cupons começa em 10/10 |

O bom é **reproduzível** (dados concretos), **verificável** (o esperado vem de
uma regra) e **decidível** (impacto em reais e clientes). Template em
`assets/templates/bug-report.md`.

## Título e reprodução mínima

### Fórmula do título

**Onde + o que acontece + em que condição**, com os termos do domínio que
alguém usaria para buscar duplicados.

| Evite | Prefira |
| --- | --- |
| Bug no login | Login: conta bloqueada após 3 tentativas mesmo com a senha correta na 3ª |
| Tela quebrada | Extrato: tabela sobrepõe o rodapé em telas de 360 px de largura |
| Erro 500 | API de pedidos: `POST /pedidos` retorna 500 quando o CEP vem com hífen |
| Não funciona no iPhone | Cadastro (iOS 18, Safari): botão "Continuar" não responde com o teclado aberto |

Verbo observável ("ignora", "duplica", "retorna 500", "exibe"); nada de "não
funciona", "problema" ou "erro" sozinhos; sintoma no título e hipótese de
causa no corpo; até uns 100 caracteres.

### Reduzir até o mínimo

1. **Corte passos.** Tire um passo por vez e veja se o defeito continua. O que
   sobra é o necessário.
2. **Isole a variável.** Mude uma condição por vez e registre em tabela. A
   coluna "reproduz?" é o dado mais útil que você pode entregar ao dev:

   | Variação | Reproduz? |
   | --- | --- |
   | Subtotal R$ 250,00, frete grátis | sim (5/5) |
   | Subtotal R$ 150,00, frete pago | não (0/5) |
   | Subtotal de exatos R$ 199,00 (limite do frete grátis) | sim (3/3) |
   | Outro cupom percentual (`VOLTA15`) | sim |
   | Cupom de valor fixo (`MENOS20`) | não |
   | Firefox e app Android | sim — não depende do cliente |

   A tabela já aponta onde olhar: desconto percentual combinado com frete
   grátis, no servidor.
3. **Desça de camada.** Se o defeito passa pela API, reproduza com `curl` e
   tire a interface da equação:

   ```bash
   curl -s -X POST "$BASE_URL/api/checkout/totais" \
     -H "Authorization: Bearer $TOKEN_QA" -H "Content-Type: application/json" \
     -d '{"itens":[{"sku":"FONE-XZ","qtd":1}],"cep":"01310-100","cupom":"PRIMEIRA10"}' \
     | jq '{subtotal, desconto, frete, total}'
   ```

4. **Ache o commit com `git bisect`** quando houver uma versão boa e uma ruim.
   Com um teste que reproduz o defeito, o Git faz a busca binária sozinho —
   cerca de 10 passos para 1.000 commits.

   ```bash
   git bisect start
   git bisect bad                    # o commit atual tem o defeito
   git bisect good v3.7.0            # última release em que funcionava
   git bisect run sh -c 'npm ci --silent || exit 125; npx vitest run cupom-frete'
   git bisect reset                  # volta para onde você estava
   ```

   O comando do `run` sai com 0 se o commit está bom, 125 se não dá para
   testar (o Git pula o commit) e outro código entre 1 e 127 se está ruim.
   Deixe o teste reprodutor **sem commit**: arquivos não rastreados
   sobrevivem aos checkouts do bisect.

### Defeito intermitente

Intermitente não é "não reproduz": é um defeito com frequência menor que
100%, e frequência é dado. Registre:

- **Frequência medida** ("falhou 3 de 20 tentativas"); para repetir de forma
  controlada, use `scripts/repetir_teste.py`.
- **Condições de cada ocorrência:** horário com fuso (prefira UTC, como os
  logs), usuário, dados, instância ou pod, carga, rede, outra aba aberta.
- **Timestamp e correlation id (ou request id) de cada falha** — é o que acha
  a linha certa entre milhões de linhas de log.
- **O que as falhas têm em comum e as passagens não têm.** Se todas ocorreram
  com duas abas abertas, o próximo passo é testar isso de propósito.
- **Hipóteses por categoria** — tempo, concorrência, dados, ambiente, ordem;
  taxonomia completa em `references/dados-ambientes-ci.md`.

## Evidências e dados pessoais

| Evidência | Use quando | Como fazer bem |
| --- | --- | --- |
| Print anotado | defeito visual ou valor errado na tela | destaque a área (retângulo ou seta), mostre URL e horário, corte o resto |
| Vídeo curto | sequência, animação, timing ("o botão pisca e some") | até cerca de 1 minuto, começando perto do defeito; diga em que segundo ele ocorre |
| Console do navegador | tela quebra ou não reage | copie o erro com o stack trace como texto, não um print borrado |
| HAR | requisição errada, resposta inesperada, lentidão | grave só a sessão do defeito e revise antes de anexar (ver abaixo) |
| Logs do servidor | erro 5xx, processamento assíncrono | trecho com timestamp e correlation id, não o arquivo inteiro |
| Request id / trace id | todo defeito que passa pelo servidor | o elo mais barato entre o relato e o log; copie do cabeçalho da resposta ou da tela de erro |
| Trace do Playwright | falha de teste automatizado | anexe o `trace.zip`: traz ações, DOM, rede e console |
| Registro afetado | dado gravado errado | ID do pedido ou registro e a consulta usada para conferir |

**Dado pessoal em evidência é tratamento de dado pessoal** sob a LGPD. O
ticket é lido por muita gente, às vezes por fornecedores, e anexos ficam para
sempre. Pelo princípio da necessidade (art. 6º, III), anexe só o necessário:

- Use usuários e dados de teste sempre que puder — isso resolve quase tudo.
- Mascare CPF (`***.456.789-**`), e-mail, telefone, endereço e nome. Nunca
  exponha número completo de cartão, senha, token ou cookie de sessão.
- HAR e trace contêm cabeçalhos, cookies e corpos de requisição. Versões
  recentes do Chrome exportam o HAR "sanitized" por padrão (sem `Cookie`,
  `Set-Cookie` e `Authorization`), mas corpos e URLs continuam lá.
- Em automação, mascare na origem:
  `await page.screenshot({ path: 'checkout.png', mask: [page.getByTestId('cpf')] })`.
- Defeito vindo de produção com dado de cliente real: referencie o ID do
  registro, não copie o dado. Se o anexo for indispensável, use área de acesso
  restrito e apague após a correção.

## Severidade e prioridade

Severidade mede o **estrago** do defeito; prioridade mede a **urgência** de
corrigir em relação ao resto do trabalho. QA propõe a severidade (técnica,
relativamente objetiva); o PO decide a prioridade (negócio), com o dev
informando custo e risco da correção.

| Severidade | Critério objetivo (basta um) | Exemplos |
| --- | --- | --- |
| Bloqueador | impede usar ou testar um fluxo principal inteiro, sem contorno; ou impede a release de subir | login falha para todos; checkout retorna 500 em qualquer pedido; build não sobe em homologação |
| Crítica | dinheiro errado; perda ou corrupção de dados; falha de segurança explorável; violação legal ou regulatória; função principal quebrada para um grupo de usuários sem contorno | cobrança em duplicidade; usuário vê pedido de outro (IDOR); botão "Pagar" inacessível por teclado e leitor de tela |
| Alta | função importante errada com contorno difícil ou caro; regra de negócio violada sem perda direta | upload de comprovante falha acima de 2 MB (contorno: comprimir o PDF); filtro de busca ignora a categoria |
| Média | função secundária errada, ou principal com contorno simples; mensagem que confunde | ordenação por preço errada a partir da 2ª página; erro de validação que não diz qual campo |
| Baixa | cosmético ou de texto, sem efeito na decisão nem no resultado do usuário | ícone desalinhado; vírgula faltando no texto de ajuda |

| Prioridade | Significa | Gatilhos típicos |
| --- | --- | --- |
| P1 | corrigir agora; interrompe o trabalho em andamento ou vira hotfix | muitos usuários, dinheiro ou dados em jogo, prazo legal, evento iminente |
| P2 | corrigir antes da release ou nesta sprint | fluxo frequente, contorno existe mas é ruim |
| P3 | planejar no backlog | impacto limitado, contorno razoável |
| P4 | se sobrar tempo; candidato a "não corrigir" com risco aceito | raro e de baixo impacto |

As duas dimensões divergem, e é por isso que existem dois campos:

- **Alta severidade, baixa prioridade.** O fechamento anual de auditoria trava
  acima de 50 mil linhas, mas o próximo uso é em março e a exportação em CSV
  serve de contorno; ou um travamento em versão de sistema operacional que
  deixa de ser suportada no mês que vem, com poucos usuários nela.
- **Baixa severidade, alta prioridade.** Nome do parceiro errado no banner da
  home no dia do lançamento da parceria; logotipo antigo no login na véspera
  da demo para o maior cliente.

Corrija quando vir: **tudo crítico** (a classificação para de informar; peça o
critério da tabela); **severidade pelo cargo** de quem reportou ("o diretor
viu" muda a prioridade, não a severidade); **severidade rebaixada porque a
correção é difícil** (custo influencia prioridade, nunca severidade); **um
campo só** ("criticidade: alta"), que esconde se o estrago é grande mas pode
esperar, ou o contrário.

## Triagem

O objetivo é sair de cada defeito novo com **decisão, dono e prazo**.

- **Quem:** QA (fato e impacto), dev da área (custo, risco, causa provável) e
  PO (prioridade); em produção, também suporte ou SRE.
- **Cadência:** diária de 15 minutos na reta final da release; no resto do
  tempo, assíncrona com prazo combinado (ex.: bug novo triado em 1 dia útil).
- **Perguntas, nesta ordem:** é defeito (diverge de requisito, regra, lei ou
  expectativa razoável)? Reproduz, com que frequência? Já existe? Qual o
  impacto real — usuários, dinheiro, risco legal ou de segurança, contorno?
  Severidade e prioridade? Quem corrige, até quando, entra nesta release? Que
  teste de regressão nasce daqui?

Resoluções que não são "corrigir", e como responder sem criar atrito:

| Resolução | Legítima quando | Resposta que evita atrito | Depois |
| --- | --- | --- | --- |
| Não é bug | ambiente fora do ar, massa errada, engano de quem testou, falha de terceiro fora do produto | "Era a massa do ambiente; corrigi e anotei no guia de ambiente para não repetir." | se confundiu quem testa, pode confundir o usuário: vale olhar a usabilidade |
| Funciona como projetado | o comportamento segue uma regra explícita e aceita | "Confere com a RN-12. Se o efeito para o cliente não for o desejado, abro como melhoria para o PO avaliar." | regra que produz resultado ruim é defeito de requisito: registre como tal |
| Duplicado | mesma causa e mesmo sintoma de um bug aberto | "Duplicado do CHK-512; levei para lá o vídeo e o request id, que são novos." | sintoma igual não prova causa igual: se as condições diferem, mantenha separado e vincule |
| Não reproduz | após tentativa honesta com os mesmos dados, versão e ambiente | "Consegue 15 minutos para reproduzirmos juntos? Mando o HAR e o horário exato das falhas." | descubra o que difere; nunca feche se há ocorrências no log de produção |
| Adiado / não corrigir | impacto baixo ou custo desproporcional, decidido por quem é dono do risco | "Registro como risco aceito por [nome], com revisão em [data]." | o bug continua visível como risco conhecido |

QA não "ganha" a triagem. Se o defeito foi adiado, mas o risco ficou
registrado com dono e data, o trabalho foi bem feito.

## Ciclo de vida e verificação da correção

```text
Novo → Triado → Em correção → Corrigido → Em verificação → Fechado
         │           ▲                          │
         │           └──────── Reaberto ◄───────┘  (verificação falhou)
         ├→ Adiado (risco aceito, com data de revisão)
         └→ Rejeitado (não é bug | duplicado | não reproduz | como projetado)
```

Os nomes variam entre ferramentas; o essencial é existir um estado entre
"corrigido" e "fechado". O dev marca como corrigido; **quem verifica fecha**.

Verificação da correção:

1. **Confirme o build:** o ambiente roda a versão com o commit da correção?
   Confira o hash ou a versão exposta (endpoint, rodapé, tela "sobre") —
   muitas reaberturas falsas nascem aqui.
2. **Teste de confirmação:** os passos originais com os mesmos dados, depois
   as variações da tabela de isolamento, inclusive as que não reproduziam.
3. **Regressão ao redor:** o que mais usa o código alterado? Para o cupom:
   percentual e fixo, com e sem frete grátis, subtotal de R$ 198,99, R$ 199,00
   e R$ 199,01, cupom expirado, dois cupons, pedido sem cupom.
4. **Automatize**, no nível mais barato que prova a regra, um teste que
   falharia sem a correção; rode-o contra o código antigo para confirmar.

**Reabrir ou abrir novo?** Reabra quando o mesmo sintoma persiste nas mesmas
condições, informando a versão testada e a evidência nova. Abra um bug novo,
vinculado, quando a correção resolveu o original mas causou outro efeito, ou
quando o sintoma aparece em outra condição — dois defeitos no mesmo ticket
fazem um deles sumir. Taxa de reabertura alta indica correção sem teste do
lado do dev ou definição de pronto fraca: é sinal de processo, não de pessoa.

## Análise de causa raiz e escape analysis

Faça análise de causa para defeitos críticos, escapes para produção e
padrões repetidos — não para todo bug. O produto é **uma ação concreta, com
dono e prazo, que impede a classe de defeito**, não só a instância.

### 5 porquês

Pergunte "por quê?" a partir do sintoma até chegar a uma causa sobre a qual o
time pode agir. No caso do cupom:

1. Por que o total ignorou o cupom? Com frete grátis, o serviço de frete
   recalcula o total a partir do subtotal bruto.
2. Por que do bruto? A regra de frete grátis fica no serviço de frete, que não
   recebe os descontos.
3. Por que não recebe? O contrato carrinho→frete não tem campo de desconto, e
   ninguém o revisou quando a regra mudou.
4. Por que nenhum teste pegou? Testes de cupom usam frete pago; os de frete
   grátis, nenhum cupom. A combinação não estava na tabela de decisão.
5. Por que não estava? O refinamento não incluiu o time de frete nem QA.

Ações: tabela de decisão cupom × frete na história e nos testes unitários (QA
e dev, nesta sprint); teste de contrato carrinho→frete com desconto (dev do
frete, próxima sprint); dono de cada serviço tocado presente no refinamento
(PO, a partir de agora).

Armadilhas: parar em "o dev errou" — pessoas erram, o sistema é que deve
pegar; seguir uma só cadeia quando há várias causas contribuintes; preencher
um porquê com palpite em vez de evidência.

### Ishikawa (espinha de peixe)

Use quando houver muitas causas candidatas: o defeito é a "cabeça" e cada
espinha é uma categoria — **pessoas** (conhecimento, sobrecarga), **processo**
(refinamento, revisão, definição de pronto), **ferramentas** (CI, análise
estática), **requisitos** (ambíguo, incompleto), **ambiente** (config, versão,
infraestrutura) e **dados** (massa, migração, legado). O valor está em forçar
o time a olhar além do código antes de eleger uma causa.

### Classificação da origem

Registrar a origem transforma bugs avulsos em dados para melhorar o processo
(a ODC — Orthogonal Defect Classification, da IBM — formaliza essa ideia).

| Origem | Sinal típico | Prevenção que funciona |
| --- | --- | --- |
| Requisito | regra ambígua, ausente ou contraditória; "não sabíamos que tinha que fazer isso" | exemplos concretos no refinamento, three amigos, critérios de aceite com dados |
| Design | a solução não comporta o caso (arquitetura, modelo de dados, fluxo de UX) | revisão de design com casos de borda, protótipo testado |
| Código | lógica, limite, nulo, tipo, concorrência | teste unitário, revisão de código, análise estática |
| Ambiente | só acontece em um ambiente; versão de runtime, recurso, rede | paridade entre ambientes, infraestrutura como código |
| Dados | registro legado, migração, massa que não existe em teste | teste de migração, dados realistas anonimizados |
| Configuração | flag, variável, parâmetro ou permissão errada | config versionada e validada na subida; teste com a config de produção |
| Integração | contrato divergente com outro serviço ou terceiro | teste de contrato, virtualização fiel, monitoramento da integração |

Registre também **em que fase o defeito entrou** e **em que fase foi achado**:
a distância entre as duas é o custo dele.

### Escape analysis: por que nenhum teste pegou?

Para cada defeito que escapou para produção (ou para uma fase tardia):

| Por que escapou | Ação concreta |
| --- | --- |
| Não havia teste para esse risco | adicionar o caso e revisar a análise de risco da área para achar os vizinhos |
| Havia teste, com dado ou ambiente diferente | incluir o dado que dispara o defeito; reduzir a diferença de ambiente |
| Havia teste, mas a asserção não verificava o efeito | fortalecer a asserção (valor, não só status 200) e procurar o mesmo padrão em outros testes |
| O teste falhou e foi ignorado (flaky, quarentena, "sempre falha") | corrigir o teste; rever a política de quarentena |
| Só aparece com volume, concorrência ou tempo de produção | teste de carga ou de concorrência direcionado; alerta no monitoramento |
| Foi o cliente quem detectou, não o monitoramento | monitoramento sintético ou alerta de métrica de negócio para esse fluxo |
| Risco conhecido e aceito | nenhuma ação de teste; confirmar que a aceitação foi consciente e por quem |

"Testar mais" e "ter mais atenção" não são ações. Ação tem verbo, artefato,
dono e prazo: "Adicionar à suíte de contrato o caso desconto + frete grátis
(Ana, até 17/10)".

Ao longo do tempo, acompanhe o DDP (defect detection percentage): achados
pelos testes ÷ (achados pelos testes + achados em produção), por área e
período. Serve para decidir onde investir, nunca para comparar pessoas.

## Comunicação e bug advocacy

O objetivo de um bug report é **levar à decisão certa** sobre o defeito. Bug
advocacy é dar a quem decide os fatos para decidir bem — não é vencer
discussão. O curso BBST Bug Advocacy (Cem Kaner) resume a investigação em
RIMGEA: **Replicate** (reproduza antes de relatar), **Isolate** (reduza ao
mínimo), **Maximize** (busque a pior consequência — o centavo de
arredondamento no pedido aparece no fechamento do mês?), **Generalize** (onde
mais aparece: outros cupons, outras telas com o mesmo cálculo),
**Externalize** (impacto no mundo real: cliente, dinheiro, suporte, lei) e
**And say it clearly and dispassionately** (com clareza e sem emoção).

| Evite | Prefira | Por quê |
| --- | --- | --- |
| "Você esqueceu de aplicar o desconto" | "O total não aplica o desconto quando o frete é grátis" | descreve o sistema, não a pessoa |
| "Como isso passou?" | "Esse caso não estava nos critérios; sugiro incluí-lo" | aponta a lacuna do processo |
| "URGENTE!!! Tudo quebrado" | "Checkout cobra R$ 25,00 a mais em pedidos com cupom e frete grátis" | dado convence mais que ênfase |
| "Não fecho enquanto não corrigir" | "Se for adiado, registro como risco aceito por quem decidir" | QA torna o risco visível; quem decide é o dono do produto |

- **Com dev:** chegue com a reprodução mínima e o request id; ofereça 15
  minutos de pareamento em vez de dez comentários; discuta o comportamento
  esperado, não a implementação; aceite "funciona como projetado" quando há
  regra — e leve a regra ao PO se ela prejudica o usuário.
- **Com PO:** fale em impacto de negócio (clientes afetados, R$, risco legal,
  chamados no suporte) e apresente opções com custo: corrigir agora, desligar
  a funcionalidade por feature flag, contornar com comunicação, adiar com risco
  registrado. Decidir não corrigir é legítimo; decidir sem informação, não.

## Relatório de teste

O relatório de execução (ou de ciclo) existe para apoiar uma decisão — quase
sempre "liberar ou não". O gestor precisa ver a decisão recomendada, o risco
que sobra e o que se pede dele; não precisa de lista de 400 casos, jargão ou
percentual de aprovação sem contexto. Template completo, com exemplo, em
`assets/templates/relatorio-de-teste.md`.

Estrutura, na ordem em que o gestor lê:

1. **Recomendação em uma linha:** liberar, liberar com ressalvas ou não, e por quê.
2. **Riscos abertos** (3 a 5), em linguagem de negócio, com a decisão que cada um pede.
3. **Escopo:** o que foi testado, o que **não** foi e o risco que isso deixa.
4. **Números:** casos planejados, executados, aprovados, com falha, não
   executados; defeitos abertos por severidade.
5. **Tendência:** defeitos abertos e fechados ao longo do ciclo — está estabilizando?
6. **Condições do teste:** ambiente fora do ar, dados faltando, intermitência.
7. **Decisões pedidas e próximos passos**, com dono e data.

| Em vez de | Escreva |
| --- | --- |
| "92% dos casos passaram" | "Compra, pagamento e cadastro passaram; as falhas restantes são de relatórios administrativos, com 2 defeitos de severidade média" |
| "Bug CHK-512 aberto" | "Clientes com cupom e frete grátis pagam até 10% a mais; a campanha de 10/10 depende dessa combinação" |
| "Não deu tempo de testar o app iOS" | "O app iOS não foi testado nesta versão; uma falha no checkout atingiria os clientes iOS. Opções: adiar o iOS 2 dias ou liberar com smoke e monitoramento reforçado" |

Armadilhas: relatório melancia (verde por fora, vermelho por dentro: "100% de
aprovação" com 40% dos casos não executados); contar casos em vez de pesar
riscos (500 casos de baixo risco não compensam 1 de pagamento não testado);
misturar verificado com inferido; esconder bloqueios de ambiente, que também
são risco.

Versão curta, que cabe em uma mensagem:

```text
Release 3.8.0 — recomendação: LIBERAR COM RESSALVA.
Ressalva: a correção do CHK-512 (cupom + frete grátis cobra a mais) precisa
estar no build final; sem ela, não liberar antes da campanha de 10/10.
Testado: compra, pagamento (cartão, PIX, boleto), cadastro e busca —
212 de 220 casos executados, 205 aprovados, 7 com falha.
Não testado: regressão do app iOS (8 casos; dispositivo indisponível).
Risco: falha no checkout iOS. Mitigação proposta: smoke no iOS logo após a
publicação + alerta de erro no checkout.
Defeitos abertos: 0 bloqueadores, 1 crítico, 3 médios, 5 baixos.
Decisão pedida (PO, até 08/10): aceitar o iOS sem a regressão completa?
```

## Defeito em produção

Sequência: **mitigar antes de corrigir.**

1. **Classificar** o incidente pelo impacto: usuários, dinheiro, dados, segurança.
2. **Mitigar:** rollback, desligar a feature flag, contorno operacional.
   Corrigir com calma depois de estancar é mais seguro que hotfix às pressas.
3. **Comunicar** o status, com a próxima atualização em horário marcado.
4. **Corrigir e verificar:** hotfix com escopo mínimo, teste de confirmação,
   regressão focada no que o diff toca e smoke pós-deploy. Hotfix que pula
   todos os testes é a origem clássica do segundo incidente.
5. **Postmortem sem culpados** em poucos dias, com a memória fresca.

Papel do QA: reproduzir fora de produção (com dados no formato dos reais,
anonimizados); medir a extensão (onde mais acontece, desde quando, quantos
registros); definir os testes do hotfix; levar a escape analysis ao postmortem.

O postmortem traz resumo e impacto (usuários, duração, valor, dados); linha do
tempo com horários (entrada do defeito, deploy, detecção, mitigação,
correção); causas contribuintes, quase sempre várias; a escape analysis; o
que funcionou, para manter; e ações com dono e prazo, acompanhadas até o fim.
Pergunte "como o sistema permitiu", nunca "quem errou": quem teme punição
esconde informação, e a próxima falha fica mais provável.

**Teste de regressão obrigatório.** Todo defeito de produção vira pelo menos
um teste automatizado que falha sem a correção, no nível mais barato que
prova a regra, com o identificador do incidente no nome ou em anotação — ex.:
`test('INC-2026-031: desconto percentual com frete grátis', ...)` — para que
quem pense em apagá-lo saiba por que existe. Some os casos achados ao
generalizar.
