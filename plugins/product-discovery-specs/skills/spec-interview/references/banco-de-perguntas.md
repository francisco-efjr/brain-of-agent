# Banco de perguntas da entrevista de spec

Use como repertório, não como roteiro: escolha até 3 por rodada, só as que o repositório e a conversa ainda não responderam. Cada pergunta traz o que a resposta destrava; se nada se destrava, não pergunte.

Base: V-01 (entrevista guiada), V-15 (uma pergunta por vez e play back), V-35 (só o que apenas o usuário sabe), V-42 (palavras vagas, regras implícitas, NFR, base própria MIT). A estrutura em fases (problema, limites, ler o código antes de perguntar, rascunho e "o que errei?") é inspirada no processo do gstack `spec` (MIT, Copyright (c) 2026 Garry Tan), com redação própria.

## Sumário

- [Bloco 1: problema, usuário e resultado](#bloco-1-problema-usuário-e-resultado)
- [Bloco 2: comportamento](#bloco-2-comportamento)
- [Bloco 3: limites, risco e não funcionais](#bloco-3-limites-risco-e-não-funcionais)
- [Perguntas de fechamento](#perguntas-de-fechamento)
- [Como reagir a respostas fracas](#como-reagir-a-respostas-fracas)

## Bloco 1: problema, usuário e resultado

| Pergunta | O que destrava |
| --- | --- |
| Quem é a pessoa que vai usar isto e em que situação ela está? | persona e contexto; evita feature "para todo mundo" |
| O que ela faz hoje para resolver (mesmo que mal)? O que dói nisso? | status quo; separa problema real de ideia de solução |
| Por que agora? O que mudou ou o que custa esperar? | prioridade e prazo real |
| Qual resultado, em número ou fato observável, mostra que deu certo? | critério de sucesso (`SC-`) e métrica; se o usuário não souber, registre lacuna |
| Quem decide se está bom? | dono da aprovação |

Verifique "o que existe hoje" no código antes de perguntar (Read/Grep). Se a resposta do usuário contradiz o código, cite o arquivo e peça para decidir qual vale.

## Bloco 2: comportamento

| Pergunta | O que destrava |
| --- | --- |
| Descreva o caminho feliz do começo ao fim, na ordem em que a pessoa vê. | fluxo principal |
| Em que pontos o fluxo pode falhar ou a pessoa pode desistir? O que ela deve ver então? | caminhos negativos e mensagens |
| O que acontece com dados que já existem? | migração, registros antigos, conta duplicada |
| E se a pessoa fizer duas vezes, ou parar no meio e voltar? | idempotência, retomada |
| O que deve acontecer se uma dependência (serviço externo, e-mail, pagamento) estiver fora do ar? | falhas e fallback |
| Isto vale igual na web, no app e na API? | canais |
| O que a pessoa pode desfazer, editar ou cancelar? | reversibilidade |

Exemplo de aprofundamento útil (o usuário provavelmente não considerou): "Se alguém perder o acesso à conta Google, como volta a entrar?".

## Bloco 3: limites, risco e não funcionais

| Pergunta | O que destrava |
| --- | --- |
| O que está explicitamente fora desta entrega? | `Fora de escopo`; evita "já que estamos aí" |
| Quem pode e quem não pode fazer isto? Existe outro cliente, plano ou tenant? | permissão |
| Quais são os limites (tamanho, quantidade, tempo, quantas vezes)? | números a registrar; sem resposta, `[NEEDS CLARIFICATION]` |
| Há dado pessoal envolvido? Por quanto tempo é guardado e quem vê? | LGPD (conferir com jurídico; a skill não dá parecer legal) |
| Como saberemos em produção que funciona ou quebrou? | observabilidade como requisito |
| Qual o pior resultado se isto quebrar? | define o rigor da revisão |
| Que restrições técnicas já estão decididas? (stack, serviço, prazo) | entram em "Restrições", não nos critérios |

A tabela completa de palavras vagas, regras implícitas e NFR está em `../../acceptance-criteria/references/palavras-vagas-e-regras-implicitas.md`.

## Perguntas de fechamento

1. "O que eu entendi errado?" depois do rascunho (a pergunta direta acha mais erro que "está bom?").
2. "Falta alguma regra que só você conhece?"
3. "Quem precisa aprovar isto além de você?"

## Como reagir a respostas fracas

| Resposta | Reação |
| --- | --- |
| "Não sei" | registre `[NEEDS CLARIFICATION: <pergunta> \| dono: <quem responde>]` e siga; não proponha um valor como se fosse fato |
| "O que você achar melhor" | dê uma recomendação com o motivo, marque como palpite e peça confirmação (V-29) |
| "Rápido", "fácil", "seguro" | troque por pergunta mensurável ("em quanto tempo, medido onde?") |
| Respostas que mudam o escopo no meio | volte ao play back e atualize "fora de escopo" |
| Cansaço visível | ofereça parar e gravar o que há, com as lacunas listadas |
