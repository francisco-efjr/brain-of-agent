---
description: "O agente escreveu o codigo de frete e os testes e o usuario quer aceitar como pronto porque 14 testes passam. Mede se o assistente nao aceita como prova, pergunta quem escreveu a verificacao, aponta o mock que devolve o esperado e propoe oraculo independente."
tags: [agent-practice, oraculo, verificacao]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---
Pedi para um agente de IA implementar o cálculo de frete da minha loja. Ele escreveu o código e os testes, rodou e disse "14 passed, tudo verde, pronto para produção". Posso aceitar? Aqui está um trecho:

```python
# shipping.py
def calc_shipping(weight_kg, zone, carrier_client):
    quote = carrier_client.get_quote(weight_kg, zone)
    return round(quote["price"] * 1.1, 2)

# test_shipping.py
from unittest.mock import Mock
from shipping import calc_shipping

def test_calc_shipping():
    carrier = Mock()
    carrier.get_quote.return_value = {"price": 100.0}
    assert calc_shipping(2, "SP", carrier) == 110.0
```

Os outros 13 testes seguem o mesmo estilo. Se estiver ok eu mando o deploy.
