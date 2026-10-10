# Árvore de oportunidades e matriz dos quatro riscos

Fontes: V-32 (Teresa Torres, Product Talk; implementação MIT do phuryn/pm-skills `opportunity-solution-tree`) e V-25 (Marty Cagan, SVPG, 2017-12-04). Destilado com redação própria; o texto do Product Talk não tem licença de reuso e não foi reproduzido. O "snapshot" de entrevista é Inferido (fontes secundárias).

## Sumário

- [Árvore de oportunidades](#árvore-de-oportunidades)
- [Regras de construção](#regras-de-construção)
- [Exemplo de ramo](#exemplo-de-ramo)
- [Matriz dos quatro riscos](#matriz-dos-quatro-riscos)
- [Como escolher o próximo teste](#como-escolher-o-próximo-teste)

## Árvore de oportunidades

```markdown
# Árvore: <resultado>

Resultado: <um resultado de negócio/produto, mensurável; ex.: "aumentar a retenção da semana 4">
Evidência de partida: <entrevistas N01..N12 | dados | nenhuma (Suposição)>

## Oportunidade O1: <necessidade, dor ou desejo do usuário> (notas: N03, N07)
Score (se houver dado): importância <0-1> x (1 - satisfação <0-1>) = <valor>   [origem: pesquisa X]
### Soluções
- S1: <ideia>
- S2: <ideia>
- S3: <ideia>
### Testes de premissa (para a solução escolhida)
| Premissa | Hipótese | Método | Métrica | Limiar |
| --- | --- | --- | --- | --- |
| <o que precisa ser verdade> | <afirmação> | <como testar barato> | <o que medir> | <valor que muda a decisão> |

## Oportunidade O2: ...
```

## Regras de construção

Pré-requisitos (V-32): uma teoria do cliente-alvo, um resultado claro e pelo menos 3 a 4 entrevistas com histórias. Sem isso, a árvore é palpite: marque Suposição.

- **Uma árvore por resultado.** Vários resultados, várias árvores.
- **Oportunidades são necessidades, dores ou desejos do usuário**, não funcionalidades. "Precisa lembrar de repetir o pedido semanal" é oportunidade; "notificação push" é solução.
- **3 a 7 oportunidades**, com foco nas 2 ou 3 melhores (phuryn, V-32).
- **Uma oportunidade-alvo por vez** (Torres, V-32). Escolha com critérios explícitos (impacto no resultado, evidência, tamanho), não por simpatia.
- **Pelo menos 3 soluções** para a oportunidade-alvo (phuryn; Torres fala em cerca de 3): evita o primeiro palpite.
- **1 a 2 testes de premissa por solução**, cada um com hipótese, método, métrica e limiar (V-32).
- **Revisão a cada 3 a 4 entrevistas** (V-32): a árvore muda com a evidência; registre o que mudou.
- Cada oportunidade cita as notas de origem. Oportunidade sem nota é Suposição e deve dizer isso.

Opportunity Score: Importância x (1 - Satisfação), com ambas normalizadas de 0 a 1 (V-32). Exige importância e satisfação coletadas; não estime por conta própria.

## Exemplo de ramo

Fictício, apenas para o formato; nenhum número é dado real.

```markdown
Resultado: aumentar a retomada de pedido na semana seguinte (métrica: pedidos recorrentes / clientes ativos)
Evidência de partida: nenhuma ainda (Suposição); entrevistas planejadas.

## O1: "Esqueço de repetir o pedido da semana" (notas: nenhuma; hipótese a validar)
### Soluções
- S1: lembrete automático no dia habitual do cliente
- S2: botão "repetir último pedido" na tela inicial
- S3: pedido recorrente com cobrança automática
### Testes de premissa para S2
| Premissa | Hipótese | Método | Métrica | Limiar |
| --- | --- | --- | --- | --- |
| Clientes costumam pedir quase o mesmo | Pelo menos X% dos pedidos repetem 80% dos itens do anterior | análise do histórico de pedidos | % de pedidos com itens repetidos | X definido com o produto antes de olhar os dados |
```

O limiar X fica em aberto de propósito: só o humano define o que muda a decisão.

## Matriz dos quatro riscos

Dono sugerido pela fonte: produto para valor e negócio, design para usabilidade, engenharia para viabilidade (V-25). Preencha uma matriz por ideia ou feature.

| Risco | Pergunta de teste | Dono | Evidência que resolve | Status |
| --- | --- | --- | --- | --- |
| Valor | As pessoas vão querer isto, a ponto de mudar o que fazem hoje? | produto | entrevistas sobre comportamento passado; teste de fumaça; dados de uso | aberto |
| Usabilidade | Conseguirão usar sem ajuda? | design | teste de usabilidade (vá a `ux-ui-design`) | aberto |
| Viabilidade | Conseguimos construir com tempo, tecnologia e equipe atuais? | engenharia | mapa do código (`feasibility-scout`); protótipo descartável | aberto |
| Negócio | Funciona para o negócio (custo, jurídico, canais, marca)? | produto/negócio | análise de custo; parecer jurídico; piloto | aberto |

Nesta matriz, "Status" é um de: aberto, em teste, resolvido (cite a evidência), aceito (risco aceito por quem, com data).

## Como escolher o próximo teste

1. Liste riscos abertos.
2. Para cada um, estime (julgamento, Suposição) dano se for falso e custo de testar.
3. Teste primeiro o de maior dano e menor custo. Deixe claro que a estimativa é julgamento humano, e peça a confirmação.
4. Defina de antemão o resultado que muda a decisão. Teste sem limiar não decide nada.
