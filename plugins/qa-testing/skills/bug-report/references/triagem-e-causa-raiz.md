# Triagem, severidade, causa raiz e escape analysis

Apoio da skill `bug-report`. Leia ao classificar severidade e prioridade, conduzir uma triagem, verificar uma correção, fazer 5 porquês ou escape analysis, ou escrever um relatório de teste.

Base: conteúdo próprio do brain-of-agent (MIT), reescrito e com exemplo novo; RIMGEA é da disciplina Bug Advocacy do BBST (Cem Kaner) e a ODC é da IBM, citadas como no brain (Inferido, não reverificado em fonte externa); regras de redação do título e de um bug por relatório vêm de V-27 (Verificado). Referências a leis (CDC, LGPD) são pontos de partida: confirme com o jurídico.

## Sumário

- [Severidade e prioridade](#severidade-e-prioridade)
- [Triagem](#triagem)
- [Ciclo de vida e verificação da correção](#ciclo-de-vida-e-verificação-da-correção)
- [5 porquês](#5-porquês)
- [Ishikawa](#ishikawa)
- [Classificação da origem](#classificação-da-origem)
- [Escape analysis](#escape-analysis)
- [Comunicação e bug advocacy](#comunicação-e-bug-advocacy)
- [Defeito em produção](#defeito-em-produção)
- [Relatório de teste curto](#relatório-de-teste-curto)

## Severidade e prioridade

Severidade mede o **estrago**; prioridade mede a **urgência** de corrigir em relação ao resto do trabalho. QA propõe a severidade (técnica, relativamente objetiva); o PO decide a prioridade (negócio), com o desenvolvedor informando custo e risco.

| Severidade | Critério objetivo (basta um) | Exemplos |
| --- | --- | --- |
| Bloqueador | impede usar ou testar um fluxo principal inteiro, sem contorno; ou impede a release de subir | login falha para todos; checkout retorna 500 em qualquer pedido; build não sobe em homologação |
| Crítica | dinheiro errado; perda ou corrupção de dados; falha de segurança explorável; violação legal ou regulatória; função principal quebrada para um grupo de usuários sem contorno | cobrança em duplicidade; usuário vê pedido de outro (IDOR); botão "Pagar" inacessível por teclado e leitor de tela |
| Alta | função importante errada com contorno difícil ou caro; regra de negócio violada sem perda direta | upload de comprovante falha acima de 2 MB (contorno: comprimir o PDF); filtro ignora a categoria |
| Média | função secundária errada, ou principal com contorno simples; mensagem que confunde | ordenação por preço errada a partir da 2ª página; erro de validação que não diz qual campo |
| Baixa | cosmético ou de texto, sem efeito na decisão nem no resultado do usuário | ícone desalinhado; vírgula faltando no texto de ajuda |

| Prioridade | Significa | Gatilhos típicos |
| --- | --- | --- |
| P1 | corrigir agora; interrompe o trabalho ou vira hotfix | muitos usuários, dinheiro ou dados em jogo, prazo legal, evento iminente |
| P2 | corrigir antes da release ou nesta sprint | fluxo frequente, contorno existe mas é ruim |
| P3 | planejar no backlog | impacto limitado, contorno razoável |
| P4 | se sobrar tempo; candidato a "não corrigir" com risco aceito | raro e de baixo impacto |

As dimensões divergem, por isso há dois campos. Alta severidade e baixa prioridade: o fechamento anual trava acima de 50 mil linhas, mas o próximo uso é em março e há contorno por CSV. Baixa severidade e alta prioridade: nome do parceiro errado no banner no dia do lançamento da parceria.

Corrija quando vir: tudo crítico (a classificação para de informar; peça o critério da tabela); severidade pelo cargo de quem reportou ("o diretor viu" muda a prioridade, não a severidade); severidade rebaixada porque a correção é difícil (custo influencia prioridade, nunca severidade); campo único "criticidade: alta", que esconde se o estrago é grande mas pode esperar.

## Triagem

O objetivo é sair de cada defeito novo com **decisão, dono e prazo**. Quem: QA (fato e impacto), dev da área (custo, risco, causa provável) e PO (prioridade); em produção, também suporte ou SRE. Cadência: diária de 15 minutos na reta final da release; no resto, assíncrona com prazo combinado (por exemplo, bug novo triado em 1 dia útil).

Perguntas, nesta ordem: é defeito (diverge de requisito, regra, lei ou expectativa razoável)? Reproduz, com que frequência? Já existe? Qual o impacto real (usuários, dinheiro, risco legal ou de segurança, contorno)? Severidade e prioridade? Quem corrige, até quando, entra nesta release? Que teste de regressão nasce daqui?

| Resolução | Legítima quando | Resposta que evita atrito | Depois |
| --- | --- | --- | --- |
| Não é bug | ambiente fora do ar, massa errada, engano de quem testou, falha de terceiro fora do produto | "Era a massa do ambiente; corrigi e anotei no guia para não repetir." | se confundiu quem testa, pode confundir o usuário: olhe a usabilidade |
| Funciona como projetado | o comportamento segue regra explícita e aceita | "Confere com a RN-12. Se o efeito para o cliente não for o desejado, abro como melhoria para o PO." | regra que produz resultado ruim é defeito de requisito |
| Duplicado | mesma causa e mesmo sintoma de um bug aberto | "Duplicado do CHK-512; levei para lá o vídeo e o request id novos." | sintoma igual não prova causa igual: se as condições diferem, mantenha separado e vincule |
| Não reproduz | após tentativa honesta com os mesmos dados, versão e ambiente | "Consegue 15 minutos para reproduzirmos juntos? Mando o HAR e o horário exato." | nunca feche se há ocorrências no log de produção |
| Adiado / não corrigir | impacto baixo ou custo desproporcional, decidido por quem é dono do risco | "Registro como risco aceito por [nome], com revisão em [data]." | o bug continua visível como risco conhecido |

QA não "ganha" a triagem: se o defeito foi adiado e o risco ficou registrado com dono e data, o trabalho foi bem feito.

## Ciclo de vida e verificação da correção

```text
Novo -> Triado -> Em correção -> Corrigido -> Em verificação -> Fechado
          |            ^                            |
          |            +-------- Reaberto <---------+  (verificação falhou)
          +-> Adiado (risco aceito, com data de revisão)
          +-> Rejeitado (não é bug | duplicado | não reproduz | como projetado)
```

Os nomes variam entre ferramentas; o essencial é existir um estado entre "corrigido" e "fechado". O dev marca como corrigido; **quem verifica fecha**.

1. **Confirme o build:** o ambiente roda a versão com o commit da correção? Confira o hash exposto (endpoint, rodapé, tela "sobre"). Muitas reaberturas falsas nascem aqui.
2. **Teste de confirmação:** os passos originais com os mesmos dados, depois as variações da tabela de isolamento, inclusive as que não reproduziam.
3. **Regressão ao redor:** o que mais usa o código alterado? Para uma regra de desconto: percentual e fixo, com e sem frete grátis, limites do frete, cupom expirado, dois cupons, pedido sem cupom.
4. **Automatize** no nível mais barato que prova a regra um teste que falharia sem a correção, e rode-o contra o código antigo para confirmar (receita no `verification-gate`).

Reabra quando o mesmo sintoma persiste nas mesmas condições (informe a versão testada e a evidência nova). Abra bug novo, vinculado, quando a correção resolveu o original mas causou outro efeito, ou o sintoma aparece em outra condição. Taxa de reabertura alta é sinal de processo (correção sem teste, definição de pronto fraca), não de pessoa.

## 5 porquês

Use para defeito crítico, escape para produção ou padrão repetido; o produto é **uma ação concreta, com dono e prazo, que impede a classe de defeito**. Exemplo novo (notificação de pagamento processada duas vezes):

1. Por que o cliente recebeu dois créditos? O handler de webhook processou o mesmo evento duas vezes.
2. Por que processou duas vezes? O provedor reenviou o evento após timeout e o handler não deduplica.
3. Por que não deduplica? A chave de idempotência (ID do evento) nunca foi gravada; a tabela de eventos só tem o ID do pedido.
4. Por que nenhum teste pegou? Os testes enviam cada webhook uma vez; reentrega não estava na lista de riscos.
5. Por que não estava? A análise de risco da integração não incluiu o comportamento de retry do provedor.

Ações: caso "mesmo evento 2x" e "eventos fora de ordem" no teste de integração do handler (QA e dev, esta sprint); coluna de ID de evento com restrição de unicidade (dev, próxima sprint); item "retry do parceiro" no checklist de análise de risco de integrações (QA, a partir de agora).

Armadilhas: parar em "o dev errou"; seguir uma só cadeia quando há várias causas contribuintes; preencher um porquê com palpite em vez de evidência.

## Ishikawa

Use quando houver muitas causas candidatas: o defeito é a "cabeça" e cada espinha é uma categoria. Pessoas (conhecimento, sobrecarga), processo (refinamento, revisão, definição de pronto), ferramentas (CI, análise estática), requisitos (ambíguo, incompleto), ambiente (configuração, versão, infraestrutura), dados (massa, migração, legado). O valor está em forçar o time a olhar além do código antes de eleger uma causa.

## Classificação da origem

Registrar a origem transforma bugs avulsos em dados de processo (a ODC, da IBM, formaliza a ideia).

| Origem | Sinal típico | Prevenção que funciona |
| --- | --- | --- |
| Requisito | regra ambígua, ausente ou contraditória | exemplos concretos no refinamento, critérios de aceite com dados |
| Design | a solução não comporta o caso | revisão de design com casos de borda, protótipo testado |
| Código | lógica, limite, nulo, tipo, concorrência | teste unitário, revisão de código, análise estática |
| Ambiente | só acontece em um ambiente; versão, recurso, rede | paridade entre ambientes, infraestrutura como código |
| Dados | registro legado, migração, massa inexistente em teste | teste de migração, dados realistas anonimizados |
| Configuração | flag, variável, parâmetro ou permissão errada | configuração versionada e validada na subida |
| Integração | contrato divergente com outro serviço | teste de contrato, virtualização fiel, monitoramento |

Registre também em que fase o defeito entrou e em que fase foi achado: a distância é o custo.

## Escape analysis

Para cada defeito que escapou para produção ou fase tardia, responda "por que nenhum teste pegou?":

| Por que escapou | Ação concreta |
| --- | --- |
| Não havia teste para esse risco | adicionar o caso e revisar a análise de risco da área para achar os vizinhos |
| Havia teste, com dado ou ambiente diferente | incluir o dado que dispara o defeito; reduzir a diferença de ambiente |
| Havia teste, mas a asserção não verificava o efeito | fortalecer a asserção (valor, não só status 200) e procurar o mesmo padrão em outros testes |
| O teste falhou e foi ignorado (flaky, quarentena, "sempre falha") | corrigir o teste; rever a política de quarentena |
| Só aparece com volume, concorrência ou tempo de produção | teste de carga ou de concorrência direcionado; alerta no monitoramento |
| O cliente detectou, não o monitoramento | monitoramento sintético ou alerta de métrica de negócio para o fluxo |
| Risco conhecido e aceito | nenhuma ação de teste; confirmar que a aceitação foi consciente e por quem |

"Testar mais" e "ter mais atenção" não são ações. Ação tem verbo, artefato, dono e prazo: "Adicionar à suíte de integração o caso evento duplicado (Ana, até 17/10)". Para acompanhar eficácia ao longo do tempo, o DDP (achados pelos testes / (achados pelos testes + achados em produção), por área e período) serve para decidir onde investir, nunca para comparar pessoas.

## Comunicação e bug advocacy

O objetivo é levar à decisão certa, não vencer discussão. RIMGEA resume a investigação: **R**eplicate (reproduza antes de relatar), **I**solate (reduza ao mínimo), **M**aximize (busque a pior consequência: o centavo de arredondamento aparece no fechamento do mês?), **G**eneralize (onde mais aparece), **E**xternalize (impacto no mundo real: cliente, dinheiro, suporte, lei) e **A**nd say it clearly and dispassionately.

| Evite | Prefira |
| --- | --- |
| "Você esqueceu de aplicar o desconto" | "O total não aplica o desconto quando o frete é grátis" |
| "Como isso passou?" | "Esse caso não estava nos critérios; sugiro incluí-lo" |
| "URGENTE!!! Tudo quebrado" | "Checkout cobra R$ 25,00 a mais em pedidos com cupom e frete grátis" |
| "Não fecho enquanto não corrigir" | "Se for adiado, registro como risco aceito por quem decidir" |

Com dev: chegue com reprodução mínima e request id; ofereça 15 minutos de pareamento em vez de dez comentários; discuta o comportamento esperado, não a implementação. Com PO: fale em impacto de negócio (clientes, R$, risco legal, chamados) e apresente opções com custo: corrigir agora, desligar por feature flag, contornar com comunicação, adiar com risco registrado.

## Defeito em produção

Sequência: **mitigar antes de corrigir.** (1) classificar pelo impacto (usuários, dinheiro, dados, segurança); (2) mitigar: rollback, desligar a flag, contorno operacional; (3) comunicar o status com a próxima atualização em horário marcado; (4) corrigir com escopo mínimo, teste de confirmação, regressão focada e smoke pós-deploy (hotfix que pula todos os testes é a origem clássica do segundo incidente); (5) postmortem sem culpados em poucos dias.

Papel do QA: reproduzir fora de produção com dados no formato dos reais, anonimizados; medir a extensão (onde mais acontece, desde quando, quantos registros); definir os testes do hotfix; levar a escape analysis ao postmortem. Pergunte "como o sistema permitiu", nunca "quem errou".

**Teste de regressão obrigatório.** Todo defeito de produção vira ao menos um teste automatizado que falha sem a correção, no nível mais barato que prova a regra, com o ID do incidente no nome (ex.: `test('INC-2026-031: evento de webhook duplicado credita uma vez', ...)`), para que quem pense em apagá-lo saiba por que existe. Some os casos achados ao generalizar.

## Relatório de teste curto

Estrutura na ordem em que o gestor lê: recomendação em uma linha; riscos abertos (3 a 5) em linguagem de negócio; escopo testado e **não** testado; números (planejados, executados, aprovados, falhos, não executados; defeitos por severidade); tendência; condições do teste; decisões pedidas com dono e data. Versão que cabe numa mensagem (dados fictícios):

```text
Release 3.8.0: recomendação LIBERAR COM RESSALVA.
Ressalva: a correção do CHK-512 (cupom + frete grátis cobra a mais) precisa estar no build final.
Testado: compra, pagamento (cartão, PIX, boleto), cadastro e busca: 212 de 220 casos executados, 205 aprovados, 7 com falha.
Não testado: regressão do app iOS (8 casos; dispositivo indisponível).
Risco: falha no checkout iOS. Mitigação: smoke no iOS após a publicação + alerta de erro no checkout.
Defeitos abertos: 0 bloqueadores, 1 crítico, 3 médios, 5 baixos.
Decisão pedida (PO, até 08/10): aceitar o iOS sem a regressão completa?
```

Armadilhas: relatório melancia (100% de aprovação com 40% dos casos não executados); contar casos em vez de pesar riscos; misturar verificado com inferido; esconder bloqueios de ambiente, que também são risco.
