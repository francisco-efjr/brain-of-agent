---
name: lote-sem-interacao-mobile
description: Mede se, em execução em lote sem ninguém para responder e com apps Android e iOS em campo, o plugin entrega o desenho completo em status rascunho, com Suposições rotuladas e uma seção de decisões pendentes do humano com decisores indicados no pedido, trata a organização ativa e o acesso por plano como contrato aditivo do servidor, aponta o plugin de mobile para o lado do aplicativo e não grava arquivos.
tags: [saas-multitenant, playbook, no-interaction, mobile, entitlements]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega o desenho como rascunho completo (organização ativa resolvida pelo servidor por requisição, token por tenant, acesso derivado de entitlements locais e webhook, contrato aditivo com versão mínima do app), rotula Suposições, inclui Decisões pendentes do humano com opções e impacto atribuídas a Marta e Paulo, aponta mobile-apps para o lado do aplicativo, diz que a compra pela loja do aparelho não foi coberta, e não grava arquivos nem espera resposta."
model: sonnet
---
Execução em lote, sem interação: não há ninguém para responder perguntas agora e ninguém vai aprovar nada neste momento. Não faça perguntas; registre o que faltar como pendência e entregue o trabalho até o fim em status rascunho. Não grave arquivos; entregue o texto na resposta.

Contexto: SaaS B2B de gestão de equipes de campo (cada empresa cliente é um tenant, PostgreSQL, API em Node). Há app Android e app iOS usados por técnicos, que ficam meses sem atualizar, e um painel web. Um técnico pode trabalhar para duas empresas clientes (consultor). A cobrança é por assento, pela Stripe, com planos Free, Pro e Business. Hoje o app manda o `tenantId` no corpo das requisições e guarda um único token. A política do que acontece quando a assinatura de uma empresa fica `past_due` quem decide é a Marta (CPO), que está de licença; a versão mínima suportada do app quem decide é o Paulo (CTO), que está em viagem. Não sei se algum cliente compra a assinatura pela loja de aplicativos.

Pedido: desenhe como o app troca de organização e como o servidor decide o acesso do tenant quando a assinatura muda (inclusive `past_due`), sem quebrar os apps antigos. Não tenho o repositório aberto aqui; use só o que escrevi.
