# Planilha de custo por tarefa

Fontes: V-38 e V-24. Preços, mínimos de cache e nomes de modelo mudam por geração e a página de preços não traz data impressa: **releia https://platform.claude.com/docs/en/about-claude/pricing na data de uso e registre a data abaixo**. Números do usuário são Suposição até medidos.

- **Data de leitura dos preços:** [AAAA-MM-DD] · **Modelo:** [...] · **Tokenizador recontado nesta data:** [sim/não] (o tokenizador a partir da 4.7 gera cerca de 30% mais tokens que modelos anteriores)
- **Tarefa:** [descrição] · **Execuções por caso:** [N] · **Casos:** [N]

## Entradas

| Item | Valor | Rótulo (Verificado / Suposição) | Como medido |
| --- | --- | --- | --- |
| Tokens de entrada sem cache (por execução) | | | contagem de tokens no modelo-alvo |
| Tokens de entrada com leitura de cache | | | `cache_read_input_tokens` |
| Tokens de escrita de cache (5 min / 1 h) | | | `cache_creation_input_tokens` |
| Tokens de saída | | | `usage` da resposta |
| Preço entrada / saída (US$ por milhão) | | Verificado na data acima | página de preços |
| Multiplicador de cache (leitura / escrita 5 min / escrita 1 h) | | | página de caching |
| Fator de Batch (metade do preço quando aplicável) | | | página de Batch |

## Conta

```text
execuções = casos × execuções por caso
custo_entrada = execuções × tokens_entrada / 1.000.000 × preço_entrada   (separe parcela com cache)
custo_saída  = execuções × tokens_saída  / 1.000.000 × preço_saída
total        = custo_entrada + custo_saída  (× 0,5 se Batch)
```

Exemplo ilustrativo (Suposição): 30 casos × 3 execuções = 90; 8.000 tokens de entrada e 1.500 de saída; Sonnet 5.5 a US$ 2 / US$ 10 (leitura de 2026-10-10): entrada 0,72 M × 2 = US$ 1,44; saída 0,135 M × 10 = US$ 1,35; total US$ 2,79; em Batch, US$ 1,395. Recontar tokens e reconferir preços antes de orçar.

## Verificações

- [ ] Conteúdo estático antes do ponto de corte de cache; ambos os campos de uso medidos
- [ ] Batch considerado para suíte de avaliação (expira em 24 h; resultados por 29 dias)
- [ ] `effort` variado antes de trocar de modelo
- [ ] Custo inclui retries, chamadas de tool e juiz
- [ ] Preço sem data não entra no relatório
