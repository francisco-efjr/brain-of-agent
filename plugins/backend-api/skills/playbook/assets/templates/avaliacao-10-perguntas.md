# Avaliação de dez perguntas para tools de agente

> Destilado de V-06 (anthropics/skills, mcp-builder, Apache-2.0 na skill) e V-01 (Anthropic Engineering). Mede se um agente cumpre tarefas reais com as tools expostas. Estado inicial: **desenhada, não executada** — troque quando rodar, com a saída anexada.

## Critérios de cada par pergunta-resposta

1. **Independente:** não depende da resposta de outra pergunta.
2. **Somente leitura:** não altera dados nem dispara efeito externo.
3. **Complexa:** exige várias chamadas de tool (busca, filtro, composição).
4. **Realista:** é algo que um usuário pediria.
5. **Verificável por string:** a resposta correta é comparável por igualdade (número, ID, nome), sem julgamento subjetivo.
6. **Estável:** a resposta não muda com o tempo nem com o uso do sistema (use dados semeados).

## Molde

```xml
<evaluation>
  <qa_pair>
    <question>[Qual foi o total, em reais, do pedido mais caro feito por [cliente semeado] em [mês]?]</question>
    <answer>[149.90]</answer>
  </qa_pair>
  <!-- ... mais 9 pares ... -->
</evaluation>
```

## Execução e leitura dos resultados

| # | Pergunta (resumo) | Acertou | Nº de chamadas | Tokens | Erros de tool | Observação da transcrição |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [..] | [sim|não] | [n] | [n] | [n] | [tool confusa? parâmetro ambíguo? resposta gigante?] |

- Meça acerto, número de chamadas, tokens e erros; **leia as transcrições**: o problema costuma estar na descrição da tool, não no modelo.
- Mantenha um conjunto separado de teste para não ajustar descrições ao conjunto de avaliação.
- Repita as execuções (uma só não prova nada) e registre o modelo e a data.
- Fronteira: avaliação de modelo, RAG e agentes complexos pertence a `/llm-ai-agents:playbook`.
- Não afirme resultado de avaliação que não foi executada.
