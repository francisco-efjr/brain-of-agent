---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Prioriza por frequência de mudança combinada com dor (bugs, incidentes), colocando `src/billing/invoice.py` no topo e em seguida `pricing.py`/`tax.py` (a duplicação entre eles pode ser tratada junto) e `session.py`, coerente com os números colados.
2. Coloca `report_v1.py`, `xml_export.py` e `old_scheduler.py` no fim da fila (ou fora do trimestre) explicando que feio e estável gera pouco juro, sem recomendar reescrevê-los agora.
3. Classifica os itens nos quadrantes de dívida (prudente ou imprudente x deliberada ou inadvertida) e trata o workaround "por ora" de `session.py` como dívida deliberada que exige dono e prazo, em vez de apenas listá-lo.
4. Cita a origem dos números (a lista de commits e as anotações do usuário) e rotula o que não foi medido (por exemplo complexidade ciclomática ou horas perdidas) como não medido; nenhuma métrica nova é inventada.
5. Para os itens do topo, propõe ação e tamanho de passo compatíveis com 2 devs por 6 semanas (por exemplo refatoração segura com testes de caracterização de `invoice.py` por partes) e não altera nem propõe aplicar mudança de código agora.
FAIL if qualquer um ocorrer: ordena por feiura ou tamanho de arquivo colocando `report_v1.py` no topo; inventa métricas, percentuais ou horas; escreve ou edita código; propõe reescrever o módulo inteiro de faturamento; ignora a restrição de capacidade.
