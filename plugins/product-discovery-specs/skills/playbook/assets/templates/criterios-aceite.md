# Critérios de aceite: [história ou requisito]

Ordem de escrita: **caminho feliz**, depois **falhas e bordas**, depois **não funcionais**. Um padrão principal por spec. Cada critério: um comportamento, dado concreto, resultado observável, sem verbo de interface nem tecnologia.

## Escolha do formato

| Formato | Use quando |
| --- | --- |
| Regra + exemplo | padrão; cálculo e limite |
| Given/When/Then | o negócio lê os cenários; há contexto |
| EARS | sistema, regulado, embarcado |
| Checklist | itens simples e independentes |

Formato escolhido para esta spec: [um deles] · motivo: [uma linha].

## Regra + exemplo

1. **Regra:** [enunciado]. **Exemplo:** [entrada concreta, resultado]. **Oráculo:** [o que faria o teste falhar].

## Given/When/Then

```gherkin
Regra: [enunciado da regra]

  Cenário: [título que diz a regra]
    Dado [estado]
    Quando [um único evento]
    Então [resultado observável]
```

## EARS

- Ubíquo: O [sistema] deve [resposta].
- QUANDO [gatilho], o [sistema] deve [resposta].
- ENQUANTO [estado], o [sistema] deve [resposta].
- ONDE [opção presente], o [sistema] deve [resposta].
- SE [condição indesejada], ENTÃO o [sistema] deve [resposta].

## Checklist

- [ ] [item verificável sozinho, com valor esperado]

## Cobertura por camada

| Camada | Critérios |
| --- | --- |
| Caminho feliz | |
| Falhas e bordas (vazio, limite, repetição, concorrência, dependência fora do ar) | |
| Não funcionais (desempenho, segurança, acessibilidade, logs, i18n, LGPD, compatibilidade, recuperação) | |

## Revisão final (5 perguntas + 6 itens)

- [ ] Descreve o quê, não o como? Sobrevive a uma mudança de implementação?
- [ ] Sem verbos de interação ("clicar", "digitar")? Um comportamento por cenário? `Then` observável?
- [ ] Escopo específico; caminho feliz primeiro; bordas explícitas; erros com recuperação visível; testável; sem detalhe de implementação.

**Limites declarados como Suposição:** [valor, dono para confirmar]. **Perguntas abertas:** [pergunta, dono].
