# Roadmap Now-Next-Later, OKR e pitch: modelos e regras

Fontes: V-45 (ProdPad, Now-Next-Later; autoatribuída, classe B 5), V-43 (Google re:Work, OKR), V-26 (Shape Up, 37signals, © todos os direitos reservados: apenas destilado, sem trecho), V-25 (quatro riscos), V-44. Posturas de escopo: inspiração do gstack `plan-ceo-review` (MIT, Copyright (c) 2026 Garry Tan), redação própria, Suposição de calibração. Modelos editáveis em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/` (`roadmap-nnl.md`, `okr.md`, `pitch.md`).

## Sumário

- [Roadmap Now-Next-Later](#roadmap-now-next-later)
- [OKR com definição operacional](#okr-com-definição-operacional)
- [Pitch com apetite](#pitch-com-apetite)
- [Posturas de escopo](#posturas-de-escopo)
- [Lacunas](#lacunas)

## Roadmap Now-Next-Later

Modelo:

```markdown
# Roadmap <produto> (revisado em AAAA-MM-DD)

## Now (em andamento, bem definido)
| Iniciativa | Problema | Resultado esperado | Grau de certeza | Objetivo/OKR |
| --- | --- | --- | --- | --- |
| <nome> | <problema do usuário> | <métrica ou fato observável> | alto: <evidência> | O1 |

## Next (fila depois do Now, menos detalhe)
| Iniciativa | Problema | Resultado esperado | Grau de certeza | Objetivo/OKR |

## Later (problemas maiores e vagos, ainda não decompostos)
| Tema | Problema | O que precisamos aprender antes | Grau de certeza |
```

Regras:

- Now é definido e cabe na capacidade; Next tem menos detalhe; Later é vago de propósito (V-45).
- Datas não são obrigatórias; datas fixas forçam prazo e reduzem flexibilidade (V-45). Se o usuário pedir datas, registre como "alvo" e quem se compromete.
- Grau de certeza carrega evidência: "alto: 6 entrevistas com o mesmo problema" é diferente de "alto: o diretor pediu".
- Item sem ligação com objetivo vira candidato a corte, com o `decision-recorder` registrando.
- Roadmap voltado a clientes é publicação externa: só depois de confirmação.

## OKR com definição operacional

Regras do guia (V-43): um objetivo qualitativo; cerca de 3 key results mensuráveis por objetivo; 3 a 5 objetivos por equipe; nota de 0,0 a 1,0; sucesso por volta de 0,7, com "ponto ideal" de 0,6 a 0,7; nota baixa é dado de calibração; não é avaliação de desempenho; notas não são ciência.

Modelo:

```markdown
# OKR <equipe> <ciclo>

Objetivo O1: <qualitativo, inspirador, sem número>
- KR1: <resultado mensurável>
  - Nome: <nome da métrica>
  - Fórmula: <numerador / denominador>
  - Fonte do dado: <evento, tabela, sistema; ou TBD>
  - Janela: <período e corte, ex.: semanal por coorte>
  - Baseline: <valor atual ou TBD>
  - Meta: <valor ou TBD> (origem: dado | estimativa | Suposição)
  - Nota ao fim do ciclo: <0,0 a 1,0>
- KR2: ...
- KR3: ...
```

Por que definição operacional (Inferido, conhecimento estável do domínio): sem fórmula, fonte e janela, duas pessoas medem a mesma métrica de jeitos diferentes e a nota perde sentido. Meta sem baseline é Suposição: escreva isso.

Exemplo ilustrativo (números fictícios, só para mostrar o formato):

```markdown
Objetivo O1: Fazer a primeira experiência no app ser tranquila.
- KR1: Aumentar a taxa de cadastro concluído
  - Nome: Taxa de cadastro concluído
  - Fórmula: cadastros concluídos / cadastros iniciados
  - Fonte do dado: TBD (qual evento marca início e conclusão?)
  - Janela: semanal, por coorte da semana de início
  - Baseline: TBD (medir 4 semanas antes de fixar meta)
  - Meta: TBD (Suposição até haver baseline)
```

Usos incorretos que você deve recusar: usar nota de OKR em avaliação de desempenho individual; KR que é tarefa ("lançar a tela X") em vez de resultado; objetivo com número embutido.

## Pitch com apetite

Estrutura destilada de Shape Up (V-26). O ciclo de seis semanas é contexto do autor; adapte à sua cadência.

```markdown
# Pitch: <nome>

## Problema
<situação concreta que dói; um caso real, não abstrato>

## Apetite
<quanto tempo/esforço vale gastar; definido ANTES da solução; "se não cabe, a solução encolhe", não o prazo estica>

## Solução (baixa fidelidade)
<esboço de fluxo/conceito, sem tela final nem especificação técnica>

## Limites (dentro do escopo)
- <o que entra>

## Rabbit holes
- <onde a equipe pode ficar presa; como evitar>

## No-gos
- <o que não será feito nesta aposta>

## Riscos de premissa
- <o que precisa ser verdade; liga à matriz dos quatro riscos (valor, usabilidade, viabilidade, negócio)>
```

Verificação do pitch: o apetite está explícito? Há rabbit hole nomeado? Os no-gos impedem a expansão natural do escopo? A solução cabe no apetite sem "se der tempo"?

## Posturas de escopo

Opcional, para decidir o quanto mudar o escopo de um plano (Suposição de calibração, não validada por fonte do atlas):

| Postura | Quando tende a servir | Cuidado |
| --- | --- | --- |
| Expandir | produto ou iniciativa nova, risco baixo de errar o essencial | cada expansão exige aprovação |
| Expandir seletivamente | capacidade nova sobre produto existente | oferecer cada expansão com oportunidade, esforço e risco; o que for recusado vai para "fora de escopo" |
| Manter | correção, refatoração, prazo fixo | aprofundar bordas, falhas e observabilidade sem aumentar escopo |
| Reduzir | muitos arquivos ou frentes, capacidade curta | propor o núcleo mínimo e cortar só com aprovação |

Regra herdada da fonte de inspiração: observação não aprova mudança; só o humano aprova. Depois de escolhida a postura, não alterne no meio da conversa sem avisar.

## Lacunas

- Roadmap por resultado (Pichler, Perri, SVPG) não está no atlas; Now-Next-Later tem uma única fonte, autoatribuída.
- North Star, HEART e AARRR não têm fonte aprovada; não são citados como práticas validadas.
- OKR: o guia do Google é curto e não traz evidência de eficácia.
