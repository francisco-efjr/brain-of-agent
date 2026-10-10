# Plano de migração: [título da mudança]

Estado: [rascunho | revisado | aprovado pelo responsável] · Data: [AAAA-MM-DD] · Autor/Revisor: [nomes]
Regra: este plano não aplica nada. Quem executa é o responsável pelo ambiente, em janela combinada.

## 1. Mudança

[O que muda e por quê, em 2 a 4 frases. Requisito ou incidente que originou.]

## 2. Ambiente (rótulo: Verificado | Inferido | Suposição)

| Item | Valor | Rótulo |
| --- | --- | --- |
| SGBD e versão | [ex.: PostgreSQL 15.x] | |
| ORM e ferramenta de migração | [ex.: Django 5.x / Alembic] | |
| Tabela(s) afetada(s) e tamanho | [linhas, GB] | |
| Réplicas, pooler | [ex.: 2 réplicas, PgBouncer modo transaction] | |
| Versões da aplicação que coexistem | [ex.: v41 e v42 durante o deploy] | |
| Consumidores (jobs, BI, serviços) | [lista] | |

## 3. DDL com lock declarado

| # | Comando | Lock/efeito esperado | Bloqueia leitura? Escrita? | Alternativa em etapas | Rótulo |
| --- | --- | --- | --- | --- | --- |
| 1 | [SQL] | [ex.: ACCESS EXCLUSIVE, metadado] | [sim/não] | [NOT VALID, CONCURRENTLY…] | |

## 4. Fases

| Fase | Ação (SQL ou procedimento) | Saída verificável | Rollback da fase |
| --- | --- | --- | --- |
| 1 Expand | | | |
| 2 Backfill | [lotes de N, idempotente, checkpoint em [local]] | [contagem origem = destino] | |
| 3 Verify | | [divergência abaixo de [limite]] | |
| 4 Migrate | [flag, frações] | [métricas estáveis por faixa] | |
| 5 Contract (escrita) | | [nenhum acesso ao caminho antigo nos logs por [N] dias] | |
| 6 Limpeza | [migração separada] | [registro do que foi removido] | [restauração de backup] |

## 5. Orçamentos e critério de interrupção

- `lock_timeout`: [valor de partida] · `statement_timeout`: [valor] · retry: [n tentativas, intervalo]
- Duração máxima por lote: [s] · espaço extra: [GB] · lag de réplica máximo: [s]
- Interromper se: duração ou lock acima do orçamento; erro crescente; divergência de contagem; capacidade esgotada.

## 6. Rollback × restauração

- Reverter código: [como]. Compatibilidade entre versões: [como].
- Exige restauração de dados: [quais fases/operações]. Perda potencial: [descrever].
- Backup verificado em [data], restauração testada em [data/ambiente].

## 7. Verificação

- Contagens antes/depois: [consulta]. Invariantes: [consultas]. Amostra: [critério].
- Ensaio em cópia com volume e distribuição reais: [feito | pendente]. Resultado: [duração, picos de lock].
- Comandos que o usuário executa: [lista com a saída esperada].

## 8. Responsável, janela e comunicação

[Quem executa · janela · quem acompanha · canal de incidente]

## 9. O que falta para concluir

[Dados ou acessos que o agente não teve: versão, volume, plano, permissões.]
