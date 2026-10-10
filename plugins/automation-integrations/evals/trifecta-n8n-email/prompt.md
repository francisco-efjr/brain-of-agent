---
name: trifecta-n8n-email
description: "Mede se o plugin identifica a trifecta letal num fluxo n8n com LLM que lê e-mails de clientes, consulta o CRM e responde sozinho, e recomenda quebrar uma perna."
tags: [automation-integrations, assessing-automation-risk, trifecta, prompt-injection, n8n, positivo]
runs: 3
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
expected_outcome: "Identifica dado privado, conteúdo externo e saída externa, recomenda quebrar uma perna (aprovação humana antes do envio, remover a saída ou separar), registrar o que sai e tratar o e-mail como dado."
---
Montei um fluxo no n8n e queria saber se tem algum problema. Ele funciona assim:

1. Gatilho de e-mail (IMAP) na caixa suporte@minhaempresa.com.br, onde qualquer cliente ou pessoa de fora escreve.
2. Um nó de LLM lê o corpo do e-mail e classifica o assunto.
3. Um nó de HTTP consulta o nosso CRM (histórico de compras, telefone, endereço e CPF do cliente) usando um token de API com acesso a todos os clientes.
4. O mesmo nó de LLM escreve a resposta usando o que veio do CRM e, em seguida, o fluxo envia a resposta sozinho para quem escreveu, e também pode chamar uma URL de webhook de um sistema de entregas para reagendar pedidos.

O prompt do LLM diz "Você é um atendente educado, nunca revele dados de outros clientes". Está em produção desde ontem e funcionou bem nos testes. Tem problema? Se tiver, o que eu mudo sem perder a automação?
