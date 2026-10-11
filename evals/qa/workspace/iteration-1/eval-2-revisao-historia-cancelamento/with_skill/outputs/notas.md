# Notas

## Arquivos da skill lidos

- skills/qa/SKILL.md (inteiro)
- skills/qa/references/requisitos-e-bdd.md (inteiro: tabela de palavras vagas, INVEST, regras implícitas, Example Mapping, three amigos, exemplo de recuperação de senha)
- skills/qa/assets/templates/revisao-de-historia.md (usado como esqueleto da resposta)
- skills/qa/references/dominios.md (inteiro; usei as seções de pagamentos/estorno/idempotência e e-commerce: estados do pedido, arrependimento CDC art. 49)

Não abri: estrategia.md, design-de-testes.md, bugs-e-relatorios.md e demais referências; nenhum script da skill foi executado (não se aplicavam a uma revisão de texto).

## Incertezas

- O domínio não foi dito. Assumi e-commerce com pedido, pagamento (cartão, Pix, boleto) e envio, e pedido possivelmente com vários itens. Declarei isso na resposta como suposição.
- Os estados do pedido (criado, aguardando pagamento, pago, em separação, enviado, entregue) vêm do modelo genérico de dominios.md, não do sistema real.
- A referência ao CDC art. 49 (7 dias a partir do recebimento) vem do dominios.md; não confirmei em fonte primária. Na resposta pedi confirmação com o jurídico e não declarei conformidade.
- Os valores dos critérios propostos (R$ 300,00 = R$ 280,00 + R$ 20,00 de frete, 5 minutos, 10 s) são exemplos para o time reagir; marquei os que dependem de decisão entre colchetes. Pode haver quem ache que propor critérios reescritos passa do papel do QA (a referência diz que a revisão sai "com perguntas, não com a história reescrita sozinho"); por isso rotulei como hipóteses, mas o template tem a seção.
- Donos das perguntas são papéis sugeridos (PO, financeiro, logística, jurídico, mobile), já que as pessoas não foram informadas.
- Não sei se "cancelar item" ou pedidos de marketplace existem; ficou como pergunta, não como requisito.
- A resposta ficou longa para um pedido curto; pesei entre o tamanho e a necessidade de cobrir dinheiro, estados e canais. Se for demais para o chat, o bloco "Riscos e onde testar" é o primeiro candidato a cortar.
