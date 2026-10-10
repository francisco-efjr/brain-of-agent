# Spec, PRD e spec-driven development

Estrutura, regras de qualidade e ciclo de vida de spec e PRD. Leia ao usar `write-spec`, `write-prd`, `spec-interview` ou `spec-to-tasks`. Fontes: V-09, V-11, V-28, V-34, V-35, V-38, V-39, V-41 (destiladas).

## Sumário

- [1. Spec ou PRD: qual escrever](#1-spec-ou-prd-qual-escrever)
- [2. Esqueleto de spec](#2-esqueleto-de-spec)
- [3. Regras de qualidade](#3-regras-de-qualidade)
- [4. PRD enxuto](#4-prd-enxuto)
- [5. Spec de bugfix](#5-spec-de-bugfix)
- [6. Gates por fase](#6-gates-por-fase)
- [7. Quanto de spec manter](#7-quanto-de-spec-manter)
- [8. Spec viva](#8-spec-viva)
- [9. Fluxo de comandos spec-driven e precedência](#9-fluxo-de-comandos-spec-driven-e-precedência)
- [10. Exemplo: requisito antes e depois](#10-exemplo-requisito-antes-e-depois)

## 1. Spec ou PRD: qual escrever

| Artefato | Responde | Escala | Template |
| --- | --- | --- | --- |
| PRD enxuto | Por que o produto ou iniciativa existe, para quem, como medir, o que fica fora | Iniciativa ou produto (N3 a N4) | `prd-enxuto.md` |
| Spec de feature | Que comportamento a feature entrega, com critérios verificáveis | Feature (N3) | `spec.md` |
| Spec curta | Um comportamento pequeno, com check | Uma tela, endpoint ou regra (N2) | `spec-curta.md` |
| Spec de bugfix | Comportamento atual, esperado e o que não pode mudar | Correção com risco de regressão | `spec-bugfix.md` |

O PRD aponta para as specs; as specs herdam do PRD o problema e as métricas. Não duplique texto entre os dois: referencie por ID.

## 2. Esqueleto de spec

Esqueleto próprio, inspirado no template de especificação do spec-kit (github/spec-kit, MIT, Copyright GitHub, Inc.; V-09). Os comentários HTML do template original são orientação ao redator, não comandos.

1. **Cabeçalho:** título, status (`Draft`), data, entrada (pedido original, link ou arquivo).
2. **Histórias de usuário priorizadas (P1, P2, P3):** cada uma com "por que esta prioridade", "teste independente" (como provar que esta história sozinha entrega valor) e critérios de aceite. Cada história é um MVP útil sozinha: implementar só a P1 já entrega algo demonstrável.
3. **Casos de borda,** escritos como perguntas ("o que acontece se o arquivo tem 0 linhas?").
4. **Requisitos funcionais `FR-001...`** no tom "o sistema deve...". Toda lacuna: `[NEEDS CLARIFICATION: pergunta, dono]`.
5. **Entidades-chave** no nível de domínio (nome, o que representa, relações); sem tabelas nem tipos.
6. **Critérios de sucesso `SC-001...`**: mensuráveis, sem tecnologia, que alguém consiga medir sem ler o código.
7. **Premissas** (decisões reversíveis tomadas por falta de resposta) e **Fora de escopo**.
8. **Perguntas abertas** listadas ao fim, cada uma com dono.

Versões do spec-kit variam; só o template de placeholders foi lido (V-09). O fluxo completo do spec-kit é pesado para mudança pequena (V-39).

## 3. Regras de qualidade

1. **Sem tecnologia em `FR` e `SC`.** "Resposta em até 2 s para 95% das buscas" (SC) em vez de "índice no PostgreSQL" (decisão do plano).
2. **Cada história entrega valor sozinha** e tem teste independente.
3. **Limites mensuráveis no lugar de adjetivos** (V-34): "p95 < 800 ms medido na página de listagem com 200 usuários simultâneos".
4. **Lacuna vira marcador,** nunca texto inventado: `[NEEDS CLARIFICATION: ...]` na spec, `TBD` no PRD, e entra em Perguntas abertas com dono.
5. **Fora de escopo obrigatório** (V-34, V-37): o que parece incluído e não está.
6. **Todo `FR` mapeia a pelo menos um `SC` ou critério** (rastreabilidade); todo critério tem oráculo (ver [criterios-e-historias.md](criterios-e-historias.md)).
7. **Escolha um padrão principal de critério por spec** (regra + exemplo, Given/When/Then, EARS ou checklist): misturar quatro dificulta a leitura (V-20).
8. **Histórias que cabem numa sessão focada** quando a execução será por agente (V-37).
9. **Tom neutro:** só a decisão e o motivo, sem jargão de marca.

## 4. PRD enxuto

Alvo de 600 a 1.000 palavras (V-35). Se faltar problema, usuário ou métrica, **faça até 3 perguntas e pare**, sem PRD naquela resposta (V-35, V-34). Seções:

| # | Seção | Conteúdo mínimo |
| --- | --- | --- |
| 1 | Resumo | Duas a quatro frases: quem, que problema, que resultado |
| 2 | Problema e contexto | Evidência observada (rotulada: dado, relato, Suposição) |
| 3 | Objetivos e métricas | 3 a 5, cada uma com definição operacional: nome, fórmula, fonte do dado, janela, baseline (ou `TBD`), meta |
| 4 | Usuários e segmentos | Quem usa e quem decide; tarefas principais |
| 5 | Não-objetivos | Obrigatório; o que não será feito agora e por quê |
| 6 | Solução | Comportamento e UX em nível de produto, `FR-` de alto nível |
| 7 | Riscos | Matriz dos quatro riscos ([descoberta-e-experimentos.md](descoberta-e-experimentos.md)) |
| 8 | Premissas e Perguntas abertas | Tudo que for desconhecido; "nada inventado no corpo" |
| 9 | Faseamento | MVP, v1.1, v2.0, cada fase com resultado esperado |
| 10 | Requisitos de IA | Só se o produto usa IA (modelo, avaliação, falha aceitável); do contrário, omita |

Regras: nenhum número sem origem rotulada (dado, estimativa, Suposição); sem tamanho de mercado nem concorrente inventado; adjetivo vira limite ou `TBD`. O caminho de salvamento é confirmado com o usuário (as fontes têm caminhos fixos do autor; não copiar, V-35).

## 5. Spec de bugfix

Estrutura de três blocos (V-41, docs do Kiro, vendor; destilado):

- **Comportamento atual:** o que acontece hoje, com passos de reprodução e evidência.
- **Comportamento esperado:** o que deveria acontecer, com exemplo concreto.
- **Comportamento inalterado:** o que não pode mudar com a correção (guarda de regressão).

Antes de projetar a correção, faça a checagem de inconsistências, ambiguidades e lacunas da spec (V-41). Um bug pequeno não precisa de fluxo completo: se o diff cabe numa frase e os três blocos cabem em cinco linhas, use `spec-bugfix.md` enxuto ou o nível N1.

## 6. Gates por fase

Em fluxos de quatro fases (Specify, Plan, Tasks, Implement; post do GitHub, V-11), faça três perguntas antes de avançar:

1. Há lacunas (requisito sem check, `[NEEDS CLARIFICATION]` aberto)?
2. Faltam bordas ou caminho negativo?
3. Algo desalinha da spec anterior?

Em caso de dúvida, volte uma fase; não avance carregando marcador aberto. O gate é configurável; o padrão é ativo (G1 sobre a spec, G2 sobre o plano).

## 7. Quanto de spec manter

Níveis de rigor (Böckeler, V-39): **spec-first** (escreve a spec, depois a descarta), **spec-anchored** (a spec é mantida e evolui com o código), **spec-as-source** (a spec gera o código; não há evidência de que funcione, V-39). Este plugin adota **spec-anchored**; spec-as-source está fora de escopo.

| Situação | Quanto de spec |
| --- | --- |
| Diff de uma frase | Nenhuma |
| Mudança de uma tela | Spec curta |
| Regras de negócio, vários fluxos | Spec com critérios testáveis e **dono da manutenção** |
| Iniciativa nova | PRD + spec por feature |

Spec de intenção guarda o porquê, o fora de escopo, as decisões já tomadas e as lacunas a perguntar. Revisar muito markdown cansa; se a pessoa começa a dizer "ok" sem ler, reduza o artefato (sinal de over-spec, V-39).

## 8. Spec viva

Specs atualizadas junto com código e testes preservam o aprendizado; spec congelada antes do trabalho o perde (V-28, ensaio de opinião, sem dados). Três artefatos vivos: a spec de intenção, os testes de comportamento e as notas de decisão (`decisao-produto.md`).

Procedimento de atualização pós-implementação (`write-spec`, modo atualização):

1. Compare a spec com o que foi construído (diff, descrição, testes).
2. Liste divergências em três grupos: adicionado, modificado, removido.
3. Para cada divergência, peça a decisão ao humano: **a spec muda** (o construído está certo) ou **o código muda** (a spec está certa).
4. Atualize a spec, registre a data e a decisão. Sem decisão, mantenha como pergunta aberta; nunca escolha em silêncio quem está certo.

O ensaio de V-28 não descreve o diff entre spec e construído; este procedimento é construção nossa (Inferido).

## 9. Fluxo de comandos spec-driven e precedência

Um projeto pequeno e de autor único (ai-prd-workflow, V-38, MIT, 298 estrelas na consulta) usa a sequência PRD, features, regras, RFCs e testes, com **precedência PRD, depois features, depois regras, depois RFCs** quando houver conflito, e a regra de que a revisão de um RFC recusa código escrito na mesma conversa. Aproveite as duas ideias (precedência e revisão em contexto novo). O README dele oferece `curl ... | bash`: **não recomendado**; se for estudar, clone, leia e fixe uma tag.

## 10. Exemplo: requisito antes e depois

Antes (reprovado): `FR-003: o sistema deve exportar relatórios de forma rápida e segura para vários formatos etc.`

Problemas: "rápida", "segura", "vários", "etc." sem limite; nenhuma entidade; nenhum check.

Depois:

```text
FR-003: o sistema deve exportar as vendas do período filtrado em CSV (UTF-8, separador ";")
        para até 100.000 linhas; acima disso, deve enviar o arquivo por e-mail ao solicitante.
FR-004: o sistema deve permitir a exportação apenas a usuários com o perfil "gerente".
SC-002: 95% das exportações de até 10.000 linhas concluem em até 10 s (medido no ambiente de
        homologação com 20 exportações simultâneas). [Suposição de limite: confirmar com o dono]
[NEEDS CLARIFICATION: o formato XLSX entra nesta entrega? dono: PO]
```

Observe: cada requisito tem dado concreto e oráculo; o limite proposto por nós está rotulado como Suposição; a dúvida real virou marcador com dono.
