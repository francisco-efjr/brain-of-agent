# Relatório de auditoria de performance — [sistema ou 'full']

Modo: somente leitura (sem edição de código). Gravar este arquivo exige confirmação do usuário. Engine e versão: [..] · Hardware-alvo: [..] · Data: [AAAA-MM-DD]

## Insumos

| Insumo | FOUND ou ABSENT | Onde |
| --- | --- | --- |
| Orçamento de frame (ms) | | |
| Orçamento de memória | | |
| Draw calls, carga, tamanho de build | | |
| Dados de profiler (CPU e GPU) no hardware-alvo | | |
| Build de teste | | |

## Orçamentos do projeto

| Métrica | Orçamento | Medido | Resultado |
| --- | --- | --- | --- |
| Tempo de quadro | [ms ou AUSENTE] | [ms ou nada] | OK / FALHOU / NÃO AVALIADO |

Métrica sem orçamento ou sem medição é NÃO AVALIADO, nunca "passa". 16,67 ms genérico não é orçamento do projeto.

## Classificação

[CPU-bound | GPU-bound | indeterminado] — evidência: [..]

## Hotspots

| # | Candidato ou confirmado | Local (`arquivo:linha`) | Impacto | Esforço (S/M/L) | Ganho esperado (Inferido) | Risco |
| --- | --- | --- | --- | --- | --- | --- |

Análise estática gera **candidato**; o profiler confirma. Itens M e L: decisão do usuário (implementar, reduzir escopo, adiar).

## Veredito

[COMPLETO | NÃO AVALIADO] — faltou: [lista de insumos]

## Próximos passos

Medir em ms em build no hardware-alvo, V-Sync desligado; bisseção; uma mudança por medição; remedir o mesmo cenário.
