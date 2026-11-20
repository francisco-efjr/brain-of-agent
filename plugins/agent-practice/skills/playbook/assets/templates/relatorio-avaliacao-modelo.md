# Relatório de avaliação de modelo ou ferramenta: <título>

Data de consulta: <AAAA-MM-DD> (todo número abaixo vale para esta data) · Responsável pela decisão: <nome> · Avaliador: <agente> · Auditor cego: <quem>

## 1. Decisão a tomar e tarefa real

- Decisão: <escolher X para Y> · Orçamento: <...> · Restrições de dados: <...>
- Tarefa parecida com a real (que o responsável sabe resolver): <...>
- Rubrica (quesitos ponderados) e faixas congeladas antes de rodar: A <menos de 30 min de conserto> · B <1 a 2 h> · C/D <mais>

## 2. Candidatos (combinação modelo + ferramenta + prompt + contexto)

| # | Modelo (versão confirmada) | Ferramenta/harness | Esforço de raciocínio | Prompt/contexto | Como confirmei o modelo contratado |
| --- | --- | --- | --- | --- | --- |
| 1 | <...> | <...> | <...> | <...> | <...> |

## 3. Método e isolamento

- Rodadas por candidato: <k> · Ambiente isolado (sem plugins pessoais, sem gabarito ao alcance): <sim> · Logs varridos: <resultado> · Rodadas anuladas: <...>
- Avaliação cega por avaliador independente, conferida à mão: <sim/não>

## 4. Resultados

| Candidato | Notas por rodada | Média | Ruído (amplitude) | Trabalho humano que sobra | Faixa | Custo medido |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | <...> | <...> | <...> | <...> | <A-D> | <US$ ou R$ · como contei> |

Diferença acima do ruído? <sim/não>. Se não, leia o topo como grupo e decida por preço, tempo e ferramenta (AVA-03, AVA-08).

## 5. Custo real

- Soma de todas as voltas e releituras de cache: <...> · Código das métricas auditado: <sim/não> · Prompt caching usado: <sim/não>
- Assinatura × token, esforço por tarefa, modelo menor para leitura em massa: <análise>

## 6. Benchmarks de terceiros citados (AVA-B01 a B11)

| Fonte (URL, data) | Tarefa/critério | Rodadas | Acima do ruído? | Quem corrigiu e o que foi publicado | Custo contado como | Saturada? | Vazamento? | Quem escreveu a verificação | Gabarito ao alcance? | Rodei o meu? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <...> | <...> | <...> | <...> | <...> | <...> | <...> | <...> | <...> | <...> | <...> |

## 7. Anúncios e promessas citados (AVA-C01 a C14)

| Afirmação | Coluna (medido por terceiro / palavra de quem vende / ninguém sabe) | Quem lucra | Testável por independente? | Comparado com quem e régua | Aconteceu ou poderia? | O que mudaria minha conclusão |
| --- | --- | --- | --- | --- | --- | --- |
| <...> | <...> | <...> | <...> | <...> | <...> | <...> |

## 8. Afirmações verificadas na fonte primária

| Afirmação | Fonte primária | Data | Rótulo (Verificado / Inferido / Suposição / Não verificável) |
| --- | --- | --- | --- |
| <...> | <URL> | <...> | <...> |

## 9. Recomendação (decisão é humana)

- Opções e trade-offs: <...>
- Recomendação do agente: <...> · Decisão do responsável: <pendente | texto do chat>
- Validade: reavaliar em <prazo> ou quando <gatilho>; memória e processo ficam em formato aberto para trocar de modelo (CUS-05).

## 10. Limites do método

<Amostra pequena compara versões e não se generaliza; caixa-preta por API não certifica origem; escopo da tarefa testada (AVA-12).> Pedido, registros e critérios guardados em: <caminho>.
