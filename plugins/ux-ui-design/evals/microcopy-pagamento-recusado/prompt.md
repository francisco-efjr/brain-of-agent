---
name: microcopy-pagamento-recusado
description: Mede se a reescrita de textos de uma tela de pagamento recusado segue erro em três partes, botão verbo mais objeto, alternativas por tom, nota de localização e tom de marca marcado como Suposição, sem culpar o usuário nem inventar prazos, valores ou políticas.
tags: [ux-ui-design, ux-writing, microcopy]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 450
runs: 3
expected_outcome: "Tabela por elemento com texto recomendado, duas alternativas com tom, justificativa e nota de localização; erro em três partes sem culpar o usuário e sem código técnico; botões específicos; tom de marca marcado como Suposição; fatos ausentes marcados para confirmar, sem inventar prazos, estorno ou valores."
model: sonnet
---
Reescreve os textos dessa tela, estão secos e o suporte recebe muita reclamação. O app é o Pagaí, uma carteira digital para autônomos no Brasil. Quero um tom caloroso mas direto. Não temos guia de voz escrito.

Tela de pagamento recusado (hoje):
- Título: "Erro"
- Mensagem: "Erro 500: falha na transação (cód. 0x3F)"
- Botão principal: "OK"
- Link abaixo: "Tente novamente mais tarde"

Contexto: a recusa acontece quando o banco do cartão nega a compra ou quando a conexão cai no meio. O app não sabe dizer qual dos dois foi. O cartão não é cobrado quando a transação é recusada, mas eu não sei dizer em quanto tempo algum valor reservado volta, então não prometa prazo. Limites: título até 30 caracteres, mensagem até 90, botões até 20. Também sai um e-mail com o mesmo aviso; me dá o assunto e a primeira linha dele.
