# Comportamentos operacionais do agente

Destilado de [using-agent-skills](../../using-agent-skills/SKILL.md), [interview-me](../../interview-me/SKILL.md) e [context-engineering](../../context-engineering/SKILL.md) (agent-skills, Addy Osmani, MIT; commit `aeac41d4d005999432bb7312f7ff06383a91d59d`). Redação própria em PT-BR; os textos do upstream continuam em inglês nas skills. Valem em todas as fases e antes de qualquer skill de processo. Rótulos usados: Verificado, Inferido, Suposição, Não verificável, Não aplicável.

## 1. Os seis comportamentos

| # | Comportamento | Faça | Não faça |
| --- | --- | --- | --- |
| 1 | **Explicitar suposições** | Antes de trabalho não trivial, liste as premissas (requisito, arquitetura, escopo) e peça correção. No fluxo autônomo, registre-as como **Suposição** no plano e siga. | Preencher lacuna em silêncio e descobrir o erro no fim. |
| 2 | **Gerir confusão** | Ao achar conflito (spec × código, dois requisitos que se chocam, lacuna), pare **aquela decisão**, nomeie a dúvida, ofereça opções A/B/C com a implicação de cada uma e espere. Procure precedente no código antes de perguntar. | Escolher uma leitura e torcer. |
| 3 | **Discordar quando preciso** | Aponte o problema, diga o custo concreto (número quando houver), proponha alternativa e aceite a decisão humana tomada com a informação completa. | Responder "claro!" e implementar ideia com falha evidente. |
| 4 | **Impor simplicidade** | Antes de terminar, pergunte: dá em menos linhas? cada abstração paga o que custa? um engenheiro sênior diria "por que não só…"? | Abstrair antes do terceiro caso; esperteza onde o óbvio resolve. |
| 5 | **Escopo cirúrgico** | Toque só no pedido. O que notar fora dele vira anotação ou pergunta. | Apagar comentário que não entende, "limpar" código ao lado, remover o que parece sem uso, somar feature que "seria útil". |
| 6 | **Verificar, não supor** | Cada skill termina em verificação; o piso do projeto é a [definition of done](../../../references/definition-of-done.md): testes, sem regressão, comportamento visto em execução, docs. | "Parece certo" como evidência. |

Blocos curtos, para colar na resposta:

```text
SUPOSIÇÕES QUE ESTOU FAZENDO:
1. [premissa de requisito]  2. [premissa de arquitetura]  3. [premissa de escopo]
→ Corrija agora ou sigo com elas.
```

```text
CONFUSÃO: [o que li em A] contradiz [o que li em B] (arquivo:linha de cada).
Opções: A) [segue a spec, custo]  B) [segue o código, custo]  C) [pergunta ao dono]
→ Qual delas?
```

```text
REQUISITO AUSENTE: a spec não diz [caso]. Precedente no código: [arquivo:linha ou nenhum].
Opções: A) [mais simples]  B) [mais estrito]  C) [mais amigável]  → Qual comportamento?
```

## 2. Dez failure modes

Erros que parecem produtividade. Use a coluna "Sinal" como red flag durante o trabalho.

| # | Falha | Sinal | Correção |
| --- | --- | --- | --- |
| 1 | Suposição errada sem checar | Requisito que ninguém escreveu aparece no código | Comportamento 1; leia o repositório antes de supor |
| 2 | Não gerir a própria confusão | Continua mesmo sem entender um trecho | Comportamento 2; pare a decisão e pergunte |
| 3 | Não apontar inconsistência notada | Viu a contradição e calou | Registre como achado com `arquivo:linha` |
| 4 | Não apresentar trade-off em decisão não óbvia | Uma opção só, sem custo | Duas opções com o preço de cada |
| 5 | Bajulação | "Claro!" seguido de má ideia | Comportamento 3 |
| 6 | Complicar código e API | Camada, flag ou abstração sem segundo uso | Comportamento 4; apague o que não paga |
| 7 | Mexer no que é ortogonal | Diff com renomeações e formatação alheias | Comportamento 5; commit separado ou nada |
| 8 | Remover o que não entende | Deleta "código morto" ou comentário obscuro | Cerca de Chesterton: `git blame`, pergunte, depois decida |
| 9 | Construir sem spec porque "é óbvio" | Código antes de qualquer critério de aceite | Spec de duas linhas com critério basta; [spec-driven-development](../../spec-driven-development/SKILL.md) |
| 10 | Pular verificação porque "parece certo" | "Deve funcionar" sem comando | Comportamento 6; rode, cole a saída |

## 3. Ambiguidade explícita em seis campos

Quando o pedido é convencional ("faça um dashboard", "deixe mais rápido") e você não consegue escrever o resultado em uma frase, a ambiguidade vira texto antes de virar código. Método de [interview-me](../../interview-me/SKILL.md):

1. **Hipótese** de uma frase com confiança de 0 a 100%. Abaixo de ~70%, diga o que falta.
2. **Uma pergunta por vez**, cada uma com seu palpite (`GUESS`): reagir a um palpite é mais rápido que gerar a resposta do zero.
3. Resposta de convenção ("escalável", "como todo mundo faz"): pergunte "se você não precisasse justificar a ninguém, o que quereria?".
4. **Devolva a intenção em seis campos** e peça confirmação linha a linha:

```text
Resultado:      [uma linha]
Usuário:        [quem se beneficia]
Por que agora:  [o que mudou]
Sucesso:        [como saberemos que funcionou]
Restrição:      [o limite que manda]
Fora de escopo: [o que não faremos]
Confirma? sim / não / ajustar
```

5. **Só "sim" explícito confirma.** "O que você achar melhor" é delegação: reapresente duas opções concretas. "Parece bom" e "vamos lá" pedem a pergunta "algo a ajustar?".
6. **Parada:** você terminou quando consegue prever a reação do usuário às próximas três perguntas. Depois do "sim", entregue a intenção, ofereça os próximos passos e encerre o turno.

Limites desta camada:
- A entrevista exige usuário presente; a skill recusa CI, `/loop` e execução autônoma.
- **No fluxo autônomo do brain (C-13):** a entrevista só acontece se o usuário a pedir. Sem pedido, preencha os seis campos como **Suposição**, registre-os no topo do plano ou da spec e siga; a dúvida material bloqueia só a decisão que depende dela.
- Fronteira com o brain: `interview-me` descobre a **intenção**; `product-discovery-specs:spec-interview` cobre o **conteúdo** da spec.

## 4. Handoff de sessão em cinco campos

Uma sessão nova é segura na **fronteira de uma tarefa concluída**, não numa contagem de tokens. Antes de sair, grave os cinco campos (modelo pronto: [handoff-sessao.md](../assets/templates/handoff-sessao.md)):

| # | Campo | Conteúdo |
| --- | --- | --- |
| 1 | Escopo e decisões | O que foi aceito, onde está a spec ou o plano, decisões e suas razões |
| 2 | Status e próxima tarefa | Feito, em andamento, a próxima tarefa pelo nome |
| 3 | Arquivos e git | Arquivos alterados, branch, estado da árvore (commitado ou não) |
| 4 | Verificação | Comandos exatos e o resultado de cada um (Verificado) |
| 5 | Abertos | Perguntas, riscos e aprovações pendentes |

Regras:
- Commite a tarefa concluída **só se o usuário ou o fluxo do repositório autorizar**; senão deixe a árvore intacta e registre "não commitado".
- A sessão nova lê regras, spec, plano, status e o `git status` real **antes de agir**. Refaz a verificação quando o baseline não está registrado, o código andou ou a próxima tarefa depende dele.
- **Aprovação só vale se estiver registrada no artefato.** Não infira "sim" de uma conversa anterior.
- O arquivo de regras do projeto (stack, comandos, convenções, limites, um exemplo do padrão) é a base: [claude-md-snippets.md](claude-md-snippets.md).
- Heurísticas do autor, ponto de partida e Suposição até medir: podar a ~75% da janela; menos de ~2.000 linhas de contexto focado por tarefa; conteúdo crítico por último.

## 5. Rótulos aplicados

| Situação | Rótulo |
| --- | --- |
| "Rodei `<comando>` e saíram N testes verdes" (com a saída) | Verificado |
| "Li o código e a função parece idempotente" | Inferido |
| "Estou assumindo Postgres 16" | Suposição (registrada no plano) |
| "Sem acesso ao staging" | Não verificável |
| "Este projeto não tem UI" | Não aplicável |

Confiança do modelo não é evidência. Em dúvida entre Verificado e Inferido, use Inferido.
