# documentos_br.py: massa sintética de CPF e CNPJ

Origem e licença: `documentos_br.py` é cópia sem alterações de `brains/qa/scripts/documentos_br.py` do repositório `francisco-efjr/brain-of-agent` (conteúdo próprio do usuário), licença MIT, Copyright (c) 2026 Brain of Agent contributors. Python 3, somente biblioteca padrão. Este plugin não o executa automaticamente: o usuário ou o agente `payment-test-engineer` o roda em ambiente de teste.

Uso (da raiz desta skill):

```text
python scripts/documentos_br.py gerar cpf -n 5 --mascara
python scripts/documentos_br.py gerar cnpj -n 5
python scripts/documentos_br.py gerar cnpj-alfa -n 5 --mascara
python scripts/documentos_br.py validar 529.982.247-25 11222333000181 12.ABC.345/01DE-35
python scripts/documentos_br.py --self-test
```

Autoteste executado em 2026-10-10 (Python 3.14, Windows): `self-test: OK`. `validar` aceitou `529.982.247-25` (CPF), `11222333000181` (CNPJ) e `12ABC34501DE35` (CNPJ alfanumérico).

Avisos:

- Um CPF ou CNPJ gerado com dígito verificador correto pode pertencer a uma pessoa ou empresa real. Use só em ambiente de teste e nunca para consultar bases externas (Receita, bureaus de crédito) nem para cadastrar em sistemas de terceiros.
- A docstring do script cita regras do CNPJ alfanumérico (inscrições novas a partir de julho de 2026, cálculo do DV com valor ASCII menos 48) e uma nota técnica: são informações herdadas do brain, **Não verificadas** contra a fonte primária. A especificação do Pix do BCB (2.9.0 ou posterior) confirma apenas que os schemas de CNPJ aceitam caracteres alfanuméricos.
- Os DVs do CPF e do CNPJ são cálculo determinístico; validar um documento não prova que ele existe.
