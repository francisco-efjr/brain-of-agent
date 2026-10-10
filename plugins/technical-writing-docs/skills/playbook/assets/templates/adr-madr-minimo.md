# Template: ADR (MADR mínimo) e variante com validação

Fontes: MADR 4.0.0 (licença MIT OR CC0-1.0; https://adr.github.io/madr/), "Documenting Architecture Decisions" de Michael Nygard (dedicação CC0 1.0 na página; https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) e a variante "com validação" do brain-of-agent (MIT). Estrutura adaptada com redação própria (V-30). Registra decisão **já tomada**; decidir é do plugin `architecture-design`.

Regras: número novo (próximo livre da pasta, nunca reaproveitado); ADR aceita não é reescrita; mudança vira nova ADR que cita a anterior e a antiga só recebe a linha de status. O contexto descreve **forças**, não a solução. Registre ao menos duas alternativas reais e uma consequência negativa. Sem segredos nem hostnames internos.

## Versão mínima

````markdown
# [NNNN]. [TÍTULO: frase curta]

- Status: [proposta | aceita | rejeitada | deprecated | substituída por ADR-NNNN]
- Data: [AAAA-MM-DD]
- Decisores: [NOMES OU PAPÉIS]

## Contexto e enunciado do problema

[Forças em jogo: requisitos, restrições, prazos, riscos. Neutro, sem anunciar a solução.]

## Opções consideradas

- [OPÇÃO A]
- [OPÇÃO B]
- [Não mudar nada, quando for plausível]

## Decisão

Escolhemos [OPÇÃO], porque [MOTIVO EM UMA FRASE].

### Consequências

- Positivas: [...]
- Negativas: [...]
- Neutras: [...]

### Confirmação (opcional)

[Como saberemos que foi implementada: teste, revisão de código, métrica.]
````

## Variante com validação (decisões de maior custo)

Acrescente ao mínimo:

````markdown
## Opções (comparação)

| Opção | Benefício | Custo ou risco | Compatibilidade | Evidência |
| --- | --- | --- | --- | --- |
| [A] | [...] | [...] | [...] | [arquivo:linha, benchmark, link] |

## Validação e revisão

Critério observável ou experimento que sustenta a escolha: [...]. Condição que exige reconsiderar a decisão: [...]. Links para requisito e artefatos: [...].
Limites de reversibilidade: não prometa rollback de dados só porque existe migração down.
````

## Revisão em cinco perguntas (Nygard)

1. O contexto descreve forças e não a solução?
2. A decisão está em voz ativa?
3. O status diz se substitui algo?
4. Há consequência negativa registrada?
5. O número é novo?

Depois, teste de leitor limpo: "o que foi decidido, por quê, o que perdemos".
