# Ficha de padrões de acesso: [produto ou módulo]

Preencha antes de modelar. Sem esta ficha, o modelo NoSQL é palpite e o relacional perde os índices certos.

## Entidades

| Entidade | Descrição | Volume atual | Crescimento (por mês) | Retenção |
| --- | --- | --- | --- | --- |

## Invariantes (o que nunca pode ser falso)

[Ex.: estoque nunca negativo; e-mail único por tenant; pedido pertence a um cliente.]

## Consultas

| # | Pergunta que o sistema responde | Frequência | Latência-alvo | Cardinalidade do resultado | Consistência exigida | Leitura/escrita |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [ex.: pedidos de um cliente por data] | [req/s] | [ms] | [ex.: 20] | [forte / eventual] | |

## Tenancy e dados sensíveis

[Modelo de tenancy; colunas com dado pessoal; requisitos de região, chave, backup por tenant.]

## Restrições do ambiente

[SGBD e versão, hospedagem, equipe que opera, janela de manutenção, RPO/RTO.]

## Perguntas em aberto (uma por vez)

[Lista; cada item marca qual decisão depende dele.]
