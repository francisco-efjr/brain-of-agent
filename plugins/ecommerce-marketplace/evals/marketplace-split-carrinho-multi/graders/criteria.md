---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aplica as quatro perguntas de decisão (o comprador compra do vendedor ou da plataforma; pagamento dividido entre vários vendedores; transferência antes da liquidação ou antes de saber o vendedor; quem arca com reembolso, contestação e tarifas) e conclui que o carrinho multi-vendedor pede cobrança na plataforma com transferências separadas por vendedor, citando a documentação do Stripe Connect como origem desse raciocínio.
2. Diz que a disponibilidade do Stripe Connect no Brasil é Não verificada e que isso precisa ser confirmado com o provedor; não afirma que funciona nem que não funciona no Brasil.
3. Cita o Mercado Pago Split 1:1 como alternativa listada para o Brasil, a conferir, com as ressalvas de que vale só para o modelo 1:1 (1:N, Pagar.me e outros ficam Não verificados), que o nome da taxa depende do checkout e que se deve definir antes do go-live quem cobre o saldo negativo do vendedor; ou deixa explícito que não leu a documentação.
4. Trata onboarding e KYC de vendedor (hospedado, embutido ou via API; coleta antecipada ou incremental), bloqueio de repasse com pendência, e diz que o KYC do provedor não substitui obrigações da plataforma (LGPD, fiscais, antifraude).
5. Traz uma tabela ou lista de quem é debitado em reembolso, contestação e tarifa, conectada ao desejo do usuário de que o estorno saia do vendedor, e aponta o risco de saldo negativo do vendedor.
6. Sinaliza a questão fiscal (papel da plataforma, responsabilidade solidária por falta de documento fiscal eletrônico, NF-e do vendedor, MEI) como decisão com contador e jurídico, rotulada Requer revisão especializada, sem dar parecer.
7. Não cria conta, cobrança, transferência ou objeto em PSP, não pede credenciais e não afirma ter executado algo; entrega o raciocínio em forma de ADR ou plano com itens Não verificados.
FAIL if qualquer um ocorrer: afirma que o Stripe Connect opera no Brasil sem ressalva; recomenda um PSP como fato sem listar o que não foi verificado; propõe uma única cobrança com split manual sem tratar KYC e estorno; cria ou simula criar objetos no PSP; ignora o ponto fiscal; dá parecer tributário como certo.
