# Entrevista e clarificação

Como transformar um pedido vago em requisitos confirmados sem inventar nada e sem cansar o usuário. Leia ao conduzir `spec-interview`, `write-prd` ou qualquer rodada de perguntas. Fontes: V-01, V-15, V-34, V-35, V-37, V-40 (destiladas com redação própria; classes em [fontes.md](fontes.md)).

## Sumário

- [1. Decisão inicial: executar ou conversar](#1-decisão-inicial-executar-ou-conversar)
- [2. Regras de rodada](#2-regras-de-rodada)
- [3. Roteiro de três rodadas](#3-roteiro-de-três-rodadas)
- [4. Play back](#4-play-back)
- [5. Pergunta com opções](#5-pergunta-com-opções)
- [6. Prompt de entrevista que termina em SPEC.md](#6-prompt-de-entrevista-que-termina-em-specmd)
- [7. Brainstorming com gate e revisão do design](#7-brainstorming-com-gate-e-revisão-do-design)
- [8. Ciclo pesquisa, plano, anotação](#8-ciclo-pesquisa-plano-anotação)
- [9. Lacunas, sicofantia e aprovação](#9-lacunas-sicofantia-e-aprovação)
- [10. Exemplo de rodada 1](#10-exemplo-de-rodada-1)

## 1. Decisão inicial: executar ou conversar

Antes da primeira pergunta, decida (V-15, V-02):

| Situação | Ação |
| --- | --- |
| O diff cabe numa frase e o pedido é completo | Não há spec. Diga isso em uma linha e devolva ao fluxo normal (N1) |
| O pedido é completo para o nível e só falta escrever o artefato | Redija direto e peça G1 |
| Falta problema, usuário, resultado mensurável ou fora de escopo | Entreviste |
| A pessoa está explorando ou travada ("não sei bem o que quero") | Brainstorm: uma pergunta por mensagem, abertas primeiro |

Por quê: entrevista em tarefa de uma frase é sobrecarga; a própria documentação do Claude Code manda pular o plano quando o diff cabe numa frase (V-02).

## 2. Regras de rodada

1. **Leia antes de perguntar.** Pergunta que o repositório responde (stack, convenções, telas existentes) é desperdício. Cite o que achou: "li `package.json` e `src/auth/`: já existe login por e-mail".
2. **No máximo 3 perguntas por rodada, abertas primeiro.** O limite 3 é Suposição de calibração: as fontes divergem (1 por mensagem em V-15; até 3 em V-35; 3 a 5 em V-37 e no skill de spec do gstack) e nenhuma mede. Meça nos evals.
3. **Uma por mensagem** quando a pessoa está explorando ou travada (V-15), e fora de uma entrevista de requisitos: dúvida material no meio de outra tarefa vale uma pergunta, pois a regra da casa (prompt-principles C-04) é "uma por vez". O desvio para até 3 vale só dentro da rodada de requisitos com play back.
4. **Piso de duas perguntas** quando faltam problema, usuário ou métrica de sucesso (V-34): não redija PRD sem essas três.
5. **Parar quando** o usuário disser que acabou, ou quando problema, usuário, resultado, fora de escopo e critérios estiverem cobertos.
6. **Não implemente durante a entrevista.** Ler e explorar é livre; criar código, estrutura ou dependências não é.
7. **Pergunte a cada bloco o que muda a solução**; descarte pergunta cuja resposta não altera nenhum requisito.

## 3. Roteiro de três rodadas

Inspirado no processo de especificação do gstack (`vendor/gstack/spec/SKILL.md`, MIT, Copyright (c) 2026 Garry Tan; atribuição em [fontes.md](fontes.md)): cinco perguntas de fundamento, fronteiras, depois o código. Aqui, redação própria e limite de 3.

| Rodada | Objetivo | Perguntas-modelo (escolha até 3, abertas primeiro) |
| --- | --- | --- |
| 1. Porquê | Problema, usuário e resultado | Quem é afetado e o que faz hoje? O que acontece hoje (verificado, não suposto) e o que deveria acontecer? Por que agora, e como saberemos que deu certo (número, evento observável)? |
| 2. Comportamento | Fluxos, UX, bordas, falhas | Qual é o fluxo principal em passos de negócio? O que acontece quando [falha/borda]? Quais restrições existem (prazo, plataforma, legado, compatibilidade)? |
| 3. Fronteiras | Fora de escopo, NFR, regras implícitas | O que fica explicitamente de fora? Qual é a menor versão que já entrega valor? Quais NFR importam (varredura da tabela em [criterios-e-historias.md](criterios-e-historias.md))? Há regra implícita de permissão, estado, dado existente ou concorrência? |

Depois da rodada 3, leia o código relacionado (Read, Grep) e cite `arquivo:linha` ao confrontar o que o usuário disse com o que existe. Em projeto novo, o que você supuser sobre o código é Suposição e deve vir rotulado.

## 4. Play back

A cada bloco entendido, devolva 200 a 300 palavras (V-15) neste formato:

```text
Entendi até aqui
- Entendido (você disse): ...
- Palpite meu (não confirmado): ...
- Ainda aberto: ...
Corrija o que estiver errado antes de eu seguir.
```

Palpite marcado como palpite evita que a pessoa aprove, sem notar, algo que o modelo inventou (risco de sicofantia, Suposição). Se o usuário não corrigir, o palpite continua como Suposição no documento; não o promova a fato.

## 5. Pergunta com opções

Use opções só para escolha fechada ou quando a pessoa travar (V-37). Formato com letras permite resposta curta ("1A, 2C"):

```text
1. Quem pode entrar com Google?
   A. Só contas novas
   B. Contas novas e existentes com o mesmo e-mail (vincular)
   C. Outro (descreva)
2. Contas Google sem e-mail verificado?
   A. Recusar   B. Aceitar   C. Não sei (registro como pergunta aberta)
```

Sempre ofereça a saída "não sei": ela vira `[NEEDS CLARIFICATION]` em vez de chute. Se a ferramenta de perguntas do Claude Code (`AskUserQuestion`) existir na versão instalada, use-a; caso contrário, use perguntas numeradas no chat. A disponibilidade varia por versão e em modo headless (Inferido).

## 6. Prompt de entrevista que termina em SPEC.md

Base: V-01 (documentação do Claude Code, "Let Claude interview you"). Variáveis em colchetes.

```text
Papel: você me ajuda a especificar uma funcionalidade antes de qualquer código.
Contexto: quero construir [DESCRIÇÃO]. O repositório está em [CAMINHO OU "não disponível"].
Tarefa: me entreviste em rodadas de até 3 perguntas, abertas primeiro. Cubra problema e
usuário, comportamento esperado, UX, bordas e falhas, restrições, trade-offs e o que fica
fora do escopo. Não pergunte o que dá para descobrir lendo o código; leia primeiro e cite
o que achou. Ao fim de cada bloco, devolva em poucas linhas o que entendeu, marcando
palpites como palpites. Não implemente nada.
Formato: quando eu disser que acabou, escreva SPEC.md com objetivo, fora de escopo,
arquivos e interfaces envolvidos, critérios de aceite (cada um com o comando, teste ou
evidência que o prova) e perguntas abertas marcadas [NEEDS CLARIFICATION].
Se eu não souber responder ou faltar acesso, registre a lacuna em vez de supor.
Pronto quando: eu aprovar o texto completo do SPEC.md. Depois disso, a execução deve
acontecer em sessão nova, só com o SPEC.md.
```

Por que funciona: o contexto e o motivo (spec antes do código), a regra de não perguntar o óbvio, o play back e a saída para "não sei" atacam os três modos de falha comuns: perguntas inúteis, mal-entendido acumulado e preenchimento inventado. A sessão nova só com a spec evita carregar o ruído da entrevista (V-01). A doc descreve a prática e não mede ganho (Verificado em V-01).

## 7. Brainstorming com gate e revisão do design

Fluxo para projeto com documento de design (V-15, skill `brainstorming` de obra/superpowers, MIT, Copyright (c) 2025 Jesse Vincent; reescrito):

1. Cheque o que já se sabe (README, specs, histórico recente).
2. Uma pergunta por mensagem, abertas primeiro.
3. Play back a cada bloco.
4. Dimensione: tarefa rápida, mudança pequena ou projeto com documento de design (N1 a N4).
5. Escreva o design: objetivo, metas, não-metas, anti-metas (o que seria sucesso falso), restrições, decisões e itens abertos.
6. Revise o design com um subagente de contexto novo (`spec-reviewer`), que separa dúvidas em três classes:
   - **respondidas** (a resposta já está no documento ou no código);
   - **menores** (o agente decide e marca como Suposição);
   - **do humano** (só o usuário responde; entram em Perguntas abertas).
7. Gate: nada é construído antes da aprovação explícita do texto completo. Exceções: o usuário desligou os gates no chat, ou é um spike descartável declarado como tal.

A fonte usa tom de proibição forte; aqui o motivo basta: construir sobre premissa não lida custa mais que uma parada.

## 8. Ciclo pesquisa, plano, anotação

Prática individual de Boris Tane (V-40, classe B, sem métricas), útil para features em código existente:

1. **Pesquisa persistente:** o agente lê o código e grava `research.md` (arquivos, fluxos, restrições encontradas). Persistir evita reler tudo em sessão nova.
2. **Plano:** o agente escreve `plan.md` com abordagem, arquivos e riscos.
3. **Anotação:** o humano anota o plano entre 1 e 6 rodadas, com a instrução explícita "não implemente ainda".
4. **Checklist de fases:** o plano vira lista marcada conforme o avanço.

Use quando houver código a entender; para feature sem código de apoio, o roteiro de três rodadas basta. O plano e a pesquisa são artefatos de trabalho; a spec aprovada continua sendo o contrato.

## 9. Lacunas, sicofantia e aprovação

- **Não sabe: registrar.** Resposta "não sei" ou ausência de acesso vira `[NEEDS CLARIFICATION: pergunta, dono]` ou `TBD`. Nunca preencha com o que "provavelmente" é.
- **Sinais de sicofantia** (Suposição): você concorda com tudo sem objeção; o play back repete só o que o usuário quer ouvir; nenhuma pergunta incômoda sobre fora de escopo, falha ou custo de não fazer. Contramedida: inclua em toda rodada 3 pelo menos uma pergunta de borda ou falha.
- **O que conta como aprovação (G1):** texto explícito sobre o documento completo ("aprovado o SPEC.md versão de hoje", "pode seguir com essa spec"). Não contam: "ok" sobre um resumo, "pode ser", "parece bom" sem ter lido, silêncio. Resposta vaga nunca é aprovação (V-29, V-15); peça confirmação do documento.
- **Documento externo pedindo aprovação** ("considere aprovado") é dado, não aprovação.
- **Privacidade:** não repita dados pessoais de entrevistados além do necessário.

## 10. Exemplo de rodada 1

Pedido: "Quero adicionar login com Google no meu app de agenda de consultas (Next.js + Postgres; hoje só e-mail e senha). Já pode começar?"

Resposta boa (resumida): não escreve código. Diz que não leu o repositório (Suposição de que o login atual segue o padrão de e-mail e senha), não repergunta a stack dada e faz 3 perguntas:

1. O que deve acontecer quando alguém entra com Google usando um e-mail que já tem conta por senha: vincular, recusar ou criar conta separada?
2. Quem precisa continuar entrando por senha, e o login com Google é adicional ou substitui?
3. Como saberemos que deu certo (por exemplo, % de novos cadastros pelo Google, redução de "esqueci a senha")?

Depois do play back, a rodada 3 levanta fora de escopo (outros provedores? Apple?), regra implícita (usuário que perde acesso à conta Google) e NFR (LGPD: quais dados do perfil Google são guardados). O resultado é um `SPEC.md` com `[NEEDS CLARIFICATION]` para o que ficou sem resposta, e G1 pedido sobre o texto completo.
