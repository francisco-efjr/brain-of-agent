Escrevi a suíte em `test_desconto.py` (63 casos, com `parametrize`). Escrevi os testes a partir das regras da docstring, não do que o código faz hoje. Por isso, **5 casos falham no código atual, e os dois motivos são bugs reais em `calcular_desconto`**.

## Bugs que os testes pegaram

**1. O limite de R$ 500,00 está exclusivo.**
A docstring diz "a partir de R$ 500,00: 10%", mas o código usa `subtotal > Decimal("500")`. Um pedido de exatamente R$ 500,00 recebe 5% (R$ 25,00) em vez de 10% (R$ 50,00). Para VIP o resultado é R$ 35,00 em vez de R$ 60,00.
- Falham `test_faixa_de_10_por_cento[500.00]`, `test_salto_entre_faixas_no_limite_de_500` e `test_vip_faixa_de_10_por_cento_vira_12[500.00]`.
- Correção: `>` vira `>=`.

**2. O VIP ganha desconto na faixa que não tem desconto.**
A regra é "+2 pontos em qualquer faixa *com* desconto". O código soma os 2% sempre, então um VIP com subtotal de R$ 99,99 recebe R$ 2,00 e deveria receber R$ 0,00.
- Falha `test_vip_abaixo_de_100_continua_sem_desconto` para `50.00` e `99.99`. Para `0` e `0.01` o bug passa batido, porque 2% disso arredonda para 0,00.
- Correção: `if cliente_vip and percentual > 0:`.

Se corrigir só essas duas linhas em `desconto.py`, os 63 casos passam. Confirmei isso numa cópia corrigida. Não alterei o seu arquivo original.

## O que a suíte cobre

- **Faixas e limites:** 0, 0,01, 99,99, 100,00, 100,01, 499,99, 500,00 e 500,01, para cliente comum.
- **VIP:** as três faixas, o caso sem desconto, o valor padrão `cliente_vip=False` e a chamada posicional.
- **Teto de R$ 150:** o valor logo abaixo do teto, exatamente no teto (1.500,00 comum e 1.250,00 VIP), logo acima e valores enormes. Há também uma propriedade simples: o desconto nunca passa de 150.
- **Arredondamento half-up:** casos como 100,10, que dá 5,005 e deve virar 5,01, e 100,50, que dá 5,025 e deve virar 5,03. Eles diferenciam half-up de half-even (o padrão do Python). Há também casos que arredondam para baixo, e o caso em que o arredondamento encosta no teto (1.249,99 VIP dá 149,9988, que vira 150,00).
- **Formato:** o resultado é `Decimal` com exatamente 2 casas.
- **Entrada inválida:** subtotal negativo levanta `ValueError`, para comum e VIP. O subtotal zero é válido.

## Como rodar

```
pip install pytest
pytest test_desconto.py -v
```

Os dois arquivos devem ficar na mesma pasta, porque o teste faz `from desconto import calcular_desconto`.

## Observação sobre a execução

O pytest não estava instalado no meu ambiente e eu não podia instalar pacotes. Rodei a suíte com um mini-substituto que só implementa `parametrize` e `raises`, e o resultado foi 58 passando e 5 falhando no código atual, 63 passando no corrigido. Rode com o pytest de verdade antes de confiar. Não espero diferença, mas não pude confirmar.

Não deixei os testes com `xfail`, de propósito: eles ficam vermelhos até o código ser corrigido. Se você precisar da suíte verde antes do ajuste, posso marcar os 5 casos como `xfail(strict=True)`.
