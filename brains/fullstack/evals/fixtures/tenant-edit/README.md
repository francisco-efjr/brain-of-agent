# Fixture sintética: edição de cliente por tenant

`customer_baseline.py` é **deliberadamente incorreto** e existe somente para
reproduzir o defeito de autorização. Não reutilizar em produto. `customer.py`
é a candidata corrigida, sob o contrato e limites descritos em `handoff.md`.
A função assume titularidade da transação; não é implementação universal.

Execução da candidata a partir da raiz:

```bash
python3 -m unittest discover -s brains/fullstack/evals/fixtures/tenant-edit -v
```

Para reproduzir a falha anterior, copie esta pasta para diretório temporário,
substitua `customer.py` pela cópia de `customer_baseline.py` e rode somente
`test_customer.CustomerTests.test_cross_tenant_no_mutation`. Resultado esperado
é falha; nunca sobrescreva a candidata no repositório para essa demonstração.

Logs antes/depois e hashes preservam o forward-test original por IA.
Reexecuções determinísticas dos testes não são novas tentativas de modelo.
O dataset público tem casos projetados; esta fixture teve código executado,
sem comparação causal baseline-sem-skill versus skill ou validação humana.
