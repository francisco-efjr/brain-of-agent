# language: pt
# Exemplo didático adaptado de brains/qa/references/requisitos-e-bdd.md do brain-of-agent (MIT, Francisco Edson).
# Os horários pressupõem relógio controlado pelo teste (relógio falso injetado), nunca espera real.
# Pergunta ainda aberta com o dono (PO): "na última hora" é janela deslizante ou hora cheia?
# Ficam fora do Gherkin, como testes técnicos ou checklist: token fora de logs, acessibilidade do fluxo
# e regras da nova senha (já cobertas no cadastro).
Funcionalidade: Recuperação de senha
  Para voltar a acessar a conta quando esquece a senha,
  o titular redefine a senha por um link enviado ao e-mail cadastrado.

  Regra: A resposta não revela se o e-mail tem conta

    Cenário: Pedido para e-mail com conta envia o link
      Dado que existe uma conta com o e-mail "ana@exemplo.com"
      Quando a recuperação de senha é pedida para "ana@exemplo.com"
      Então a resposta é "Se houver uma conta com esse e-mail, enviaremos um link."
      E um link de redefinição é enviado para "ana@exemplo.com"

    Cenário: Pedido para e-mail sem conta não envia nada
      Dado que não existe conta com o e-mail "bia@exemplo.com"
      Quando a recuperação de senha é pedida para "bia@exemplo.com"
      Então a resposta é "Se houver uma conta com esse e-mail, enviaremos um link."
      Mas nenhum e-mail é enviado

  Regra: O link vale por até 30 minutos e uma única vez

    Contexto:
      Dado que Ana recebeu um link de redefinição às 10:00:00

    Esquema do Cenário: Link dentro do prazo troca a senha
      Quando Ana usa o link às <horário> para definir a senha "NovaSenha2026"
      Então Ana consegue entrar com a senha "NovaSenha2026"

      Exemplos: até o limite
        | horário  |
        | 10:29:59 |
        | 10:30:00 |

    Cenário: Link vencido não troca a senha
      Quando Ana usa o link às 10:30:01 para definir a senha "NovaSenha2026"
      Então a troca é recusada com "Este link expirou. Peça um novo."
      E a senha de Ana continua a mesma

    Cenário: Link já usado não troca a senha de novo
      Dado que Ana usou o link às 10:05:00 para definir a senha "NovaSenha2026"
      Quando Ana usa o mesmo link às 10:06:00 para definir a senha "OutraSenha2026"
      Então a troca é recusada com "Este link já foi usado."
      E Ana consegue entrar com a senha "NovaSenha2026"

  Regra: Só o link mais recente vale

    Cenário: Novo pedido invalida o link anterior
      Dado que Ana recebeu links de redefinição às 10:00:00 e às 10:05:00
      Quando Ana usa o link das 10:00:00 às 10:06:00
      Então a troca é recusada com "Este link expirou. Peça um novo."

  Regra: Trocar a senha encerra as sessões e avisa o titular

    Cenário: Sessões abertas são encerradas após a troca
      Dado que Ana está conectada no celular e no notebook
      Quando Ana redefine a senha pelo link
      Então as duas sessões são encerradas
      E Ana recebe um e-mail avisando que a senha foi trocada

  Regra: No máximo 5 pedidos por e-mail por hora

    Cenário: Quinto pedido na mesma hora ainda envia o link
      Dado que já foram feitos 4 pedidos para "ana@exemplo.com" na última hora
      Quando a recuperação de senha é pedida para "ana@exemplo.com"
      Então um link de redefinição é enviado para "ana@exemplo.com"

    Cenário: Sexto pedido na mesma hora não envia e-mail
      Dado que já foram feitos 5 pedidos para "ana@exemplo.com" na última hora
      Quando a recuperação de senha é pedida para "ana@exemplo.com"
      Então a resposta é "Muitas solicitações. Tente de novo mais tarde."
      E nenhum e-mail é enviado
