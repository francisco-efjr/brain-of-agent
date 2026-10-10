# Desafio de premissas, alternativas e desenho de experimento

Duas partes: (1) processo de desafio de premissas e alternativas, inspirado nos workflows `office-hours` e `plan-ceo-review` do gstack (MIT, Copyright (c) 2026 Garry Tan; https://github.com/garrytan/gstack), reescrito sem preâmbulo de binários, telemetria nem formatos próprios; (2) checklist de experimento A/B de V-27 (Evan Miller, "How Not To Run An A/B Test", 2010-04-18). O texto detalhado das perguntas diagnósticas do modo "startup" do gstack (seção `phase-2a`) não estava no snapshot e não é reproduzido (Não verificável).

## Sumário

- [Desafio de premissas](#desafio-de-premissas)
- [Alternativas](#alternativas)
- [Ledger de decisões](#ledger-de-decisões)
- [Desenho de experimento A/B](#desenho-de-experimento-ab)
- [Exemplo A/B resolvido](#exemplo-ab-resolvido)
- [Alternativas à espera fixa](#alternativas-à-espera-fixa)

## Desafio de premissas

Antes de propor solução, desafie, em ordem:

1. **É o problema certo?** Um enquadramento diferente tornaria a solução muito mais simples ou mais impactante?
2. **O que acontece se não fizermos nada?** A dor é real e recorrente ou hipotética? Qual a evidência (nota, dado) e qual o custo de esperar?
3. **O que já existe e resolve parte?** Produtos concorrentes, processos manuais, código reaproveitável. Pergunte antes de reinventar.
4. **Como o usuário recebe a entrega?** Código sem canal de distribuição ou adoção ninguém usa; descreva como chega ao usuário (ou declare que está fora de escopo).

Apresente as premissas como afirmações para o usuário concordar ou discordar:

```text
PREMISSAS (confirme ou corrija):
1. O problema principal é <X> para <usuário>.            concorda / discorda?
2. Hoje resolvem com <Y>, ao custo de <Z>.               concorda / discorda?   [origem: relato do usuário]
3. A menor entrega que prova valor é <W>.                concorda / discorda?
```

Se o usuário discordar de uma premissa, revise o entendimento e volte. Nenhuma implementação começa antes deste passo (gate).

Se a busca de panorama na web for autorizada: use termos genéricos da categoria, nunca o nome ou o conceito proprietário do produto, para não vazar ideia ainda não pública.

## Alternativas

Gere 2 ou 3 caminhos distintos. Um deles é o mínimo viável (menor diff, entrega mais rápida).

```text
ALTERNATIVA A: <nome>  (atual / mínima)
  Resumo: <1 a 2 frases>
  Esforço: P | M | G      Risco: baixo | médio | alto
  Prós: <2 a 3>   Contras: <2 a 3>   Reaproveita: <o que já existe>
ALTERNATIVA B: <nome>  (intermediária)
ALTERNATIVA C: <nome>  (maior / ideal, opcional)
Recomendação: <qual e por quê>  [é recomendação, não decisão]
```

Esforço P/M/G é estimativa relativa, Suposição; quem confirma é o time.

## Ledger de decisões

Opcional, útil quando há muitas escolhas ao longo de uma conversa longa.

| ID | Decisão | Evidência | Status | Aprovado por e escopo |
| --- | --- | --- | --- | --- |
| DEC-01 | <ex.: manter escopo, sem integração com X> | <nota, dado, relato> | proposta / aceita / recusada | <nome>, <até quando> |

Regra herdada da inspiração: observação não aprova mudança; só o humano aprova. Decisão material vira registro durável com `decision-recorder`.

## Desenho de experimento A/B

Checklist (V-27; a estatística é atemporal, mas a cobertura de experimentação do atlas é parcial: sem OEC, métricas de guarda, SRM):

1. **Hipótese**: "Mudar X aumenta a métrica Y para o público Z."
2. **Métrica primária** única e definição operacional (fórmula, janela, fonte). Métricas secundárias são exploratórias.
3. **Efeito mínimo de interesse δ**: o menor efeito que justificaria a mudança, em unidades da métrica (para conversão, pontos percentuais em forma decimal: 0,5 p.p. = 0,005). Decisão de negócio, anterior ao teste.
4. **σ²**: para conversão, p(1 - p) com p a taxa base.
5. **Tamanho de amostra fixo antes de começar**: n ≈ 16 x σ² / δ² por braço (regra de bolso do autor). Inferido: o fator 16 corresponde a cerca de 80% de poder e 5% de significância; confira no artigo.
6. **Critério de parada fixado**: n atingido ou data final, nunca "quando o p-valor passar de significante".
7. **Sem espiar para decidir.** Olhar o painel é aceitável; decidir parar por causa dele não. Dez espiadas com nível nominal de 1% resultam em cerca de 5% de falso positivo real (tabela do artigo).
8. **Plano de decisão**: o que fazer se melhora, se fica igual, se piora, definido antes.
9. **Randomização e unidade** (usuário, sessão): defina antes e verifique que os braços têm tamanhos coerentes (SRM não está no atlas validado; faça uma checagem simples de proporção e leve ao especialista).
10. **Dono da análise** e onde o resultado será registrado.

Para análise avançada (CUPED, SRM formal, OEC), aponte `data-science-ml`.

## Exemplo A/B resolvido

Pedido: "Vou rodar um A/B de checkout com 10 mil visitantes por braço. Vou olhar toda manhã e encerro quando o p-valor cair abaixo de 0,05. Taxa base 4% e quero detectar +0,5 ponto percentual. Está bom?"

| Passo | Cálculo |
| --- | --- |
| p (taxa base) | 0,04 |
| σ² = p(1 - p) | 0,04 x 0,96 = 0,0384 |
| δ | 0,5 ponto percentual = 0,005 |
| n ≈ 16 x σ² / δ² | 16 x 0,0384 / 0,000025 = 24.576 por braço |

Conferência:

```bash
python -c "p=0.04; d=0.005; print(16*p*(1-p)/d**2, (16*p*(1-p)/10000)**0.5)"   # ~24576 e ~0.00784 (arredondamento de ponto flutuante)
```

Leitura:

- 10 mil por braço é cerca de 41% do necessário pela regra de bolso. Invertendo a regra, δ ≈ raiz(16 x σ² / n) = raiz(16 x 0,0384 / 10.000) ≈ 0,0078, ou seja, só efeitos a partir de cerca de 0,78 ponto percentual seriam detectáveis de forma confiável; o efeito de interesse (0,5 p.p.) ficaria fora do alcance (Inferido: depende do poder assumido).
- Olhar toda manhã e parar ao ver p < 0,05 é o padrão que infla o falso positivo (V-27). A ressalva: o artigo quantifica o caso de 10 espiadas com 1% nominal; para 5% nominal o efeito qualitativo é o mesmo (Inferido, não li a tabela completa).
- Recomendação: fixar n (cerca de 24,6 mil por braço, rótulo "regra de bolso do autor") e a data final antes de começar; decidir só ao fim; ou, se o time precisa decidir antes, desenhar um teste sequencial com checkpoints definidos ou uma abordagem bayesiana, com análise acompanhada por quem conhece estatística. Decisão final: do time.
- Não afirmo "está bom" nem "está ruim" sem a premissa de poder e significância confirmada.

## Alternativas à espera fixa

- **Sequencial com checkpoints definidos antes**: o plano lista quando se olha e qual limiar se usa em cada olhada (ajustado para as múltiplas olhadas). A sintaxe e os limiares exatos pedem estatístico: indique, não improvise.
- **Bayesiano**: decisão por probabilidade posterior e regra de parada declarada; exige priors e critério de decisão escritos antes.
- Em ambos: a regra de decisão é parte do desenho, não do pós-teste.
