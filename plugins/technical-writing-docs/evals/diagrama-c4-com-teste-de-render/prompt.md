---
name: diagrama-c4-com-teste-de-render
description: Mede se o diagrama C4 de contêineres é entregue em Mermaid com um nível só e menos de 15 nós, com aviso de que C4 é experimental, pedido de teste de preview no GitHub, fallback em flowchart e texto explicativo, sem afirmar que renderiza.
tags: [technical-writing-docs, diagramas, diagramar-arquitetura]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega diagrama Mermaid de contêineres com menos de 15 nós, avisa que o C4 do Mermaid é experimental, pede para conferir o preview no GitHub e oferece flowchart equivalente, acompanha texto explicativo e não afirma que renderiza."
model: sonnet
---
Faz o diagrama C4 de contêineres do meu sistema para colocar no README do GitHub. É um sistema de agendamento:

- Web app em React (SPA), usada por clientes no navegador.
- API em Node (Express), que o web app chama por HTTPS e JSON.
- PostgreSQL, onde a API lê e grava os agendamentos.
- Fila Redis: a API publica jobs de lembrete; um worker em Node consome os jobs.
- O worker envia e-mails de lembrete por um provedor de e-mail externo (SMTP).

Não tenho o repositório aqui, é só essa descrição.
