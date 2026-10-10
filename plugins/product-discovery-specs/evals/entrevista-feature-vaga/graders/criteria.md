---
type: llm
---
PASS if todos os itens abaixo são observáveis no transcript e na resposta final:
1. Não escreve nem propõe código de produto (sem arquivos, sem trechos de implementação, sem comandos de instalação) e não trata "Já pode começar?" como aprovação: explica que primeiro vem a entrevista e a spec.
2. Faz no máximo 3 perguntas na rodada (ou um play back curto seguido de até 3 perguntas), com as abertas primeiro, e não repergunta o que já foi dito (Next.js, Postgres, e-mail e senha, pacientes que se cadastram sozinhos).
3. Levanta ao menos uma regra implícita relevante, como conta existente com o mesmo e-mail (vincular ou duplicar), paciente que perde acesso ao Google, ou verificação de e-mail, e pergunta ou propõe o que fica fora de escopo (outros provedores, remover a senha, migração de contas).
4. Diz que não vê o repositório e rotula o que presume como Suposição, ou propõe ler o código; não afirma fatos sobre ele.
5. Descreve ou oferece um SPEC.md com critérios que têm um check cada e marcadores [NEEDS CLARIFICATION], e pede aprovação do texto completo antes de qualquer implementação.
FAIL if qualquer um ocorrer: cria arquivos de código ou comandos de instalação; faz 6 ou mais perguntas de uma vez; assume respostas do usuário como fato; aceita "já pode começar" como aprovação; escolhe a biblioteca de autenticação como requisito da spec.
