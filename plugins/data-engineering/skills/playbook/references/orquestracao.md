# Orquestração: Airflow, Dagster e Prefect

Quando abrir: revisar, criar, testar ou depurar DAG; planejar backfill; pedir "asset do Dagster"; escolher regras agnósticas de orquestrador.
Rótulos: Verificado = V-13/V-14/V-15 (Airflow doc stable = 3.3.2, conferida em 2026-10-10); Inferido = dedução; Lacuna = sem fonte. Confira a versão instalada (`airflow version`), porque importações e defaults mudam entre Airflow 2 e 3.

## Sumário
1. Revisão de DAG: 12 perguntas com exemplos
2. DAG de referência
3. Autoria, teste e depuração com gates
4. Backfill
5. Dagster
6. Prefect e outros (lacuna L-14)

## 1. Revisão de DAG: 12 perguntas com exemplos
Fonte: V-13 (doc oficial do Airflow, Classe A; reforço da Astronomer, Classe B). A lista de 15 regras que circulava em resumos estava errada (X-11); esta segue a doc.

| # | Pergunta | Ruim | Melhor |
| --- | --- | --- | --- |
| 1 | A tarefa é idempotente? Trate a tarefa como transação | `insert into mart.orders select ...` | Apagar o intervalo e inserir, ou `MERGE` por chave |
| 2 | Lê o intervalo da execução? | `where d = (select max(d) from raw.orders)` | `where d >= '{{ data_interval_start }}' and d < '{{ data_interval_end }}'` |
| 3 | Há `now()`/`datetime.now()` em lógica crítica? | `datetime.now().date()` no filtro | Datas do intervalo da execução |
| 4 | Há código pesado, banco, rede ou `Variable.get()` no topo? | `BUCKET = Variable.get('bucket')` no módulo | Dentro da tarefa ou por Jinja `{{ var.value.bucket }}` |
| 5 | Há segredo no código? | URL de conexão com senha em string | Connection ou secrets backend |
| 6 | XCom carrega dado grande? | `xcom_push(value=df.to_dict('records'))` | Gravar em armazenamento remoto e passar o caminho (claim-check) ou XCom backend de objetos |
| 7 | Retry com backoff e limites? | Sem retries nem limites | `retries`, backoff exponencial, `max_active_runs`, `max_active_tasks`, pools |
| 8 | Sensor longo é deferrable ou `reschedule`? | Sensor em `poke` por horas | Operador deferrable ou `mode="reschedule"` |
| 9 | Há SubDAG? | `SubDagOperator` | TaskGroup |
| 10 | O DAG importa sem erro? | Descoberto no scheduler | Teste de import (carregar o arquivo/`DagBag` e checar erros) |
| 11 | Há check de qualidade? | Carga sem validação | Operadores de check (contagem, nulos, chave) |
| 12 | `catchup` foi decidido de propósito? | Padrão implícito | Valor explícito com comentário do motivo |
Extras da doc: setup e teardown; Dynamic Task Mapping em vez de loops; operadores de provider antes de código genérico; Assets (Airflow 3) para agendamento orientado a dados; TaskFlow API. Segredo no `Variable` também é desencorajado em texto claro (Inferido).
Observação de versão: a afirmação do material da Astronomer sobre DataFrames no Task SDK não tem suporte na página oficial; ignore.

## 2. DAG de referência
Esqueleto ilustrativo. Confirme importações e parâmetros na versão instalada; em Airflow 2.x use `from airflow.decorators import dag, task`; em projetos novos de Airflow 3 a doc recomenda `airflow.sdk` (V-13). `[...]` marca o que depende do projeto.
```python
from datetime import timedelta
import pendulum
from airflow.sdk import dag, task   # Airflow 3; em 2.x: airflow.decorators

@dag(
    schedule="@daily",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,                       # decisão explícita; documente o motivo
    max_active_runs=1,
    default_args={"retries": 3, "retry_delay": timedelta(minutes=5)},   # backoff: conferir parâmetro na versão
    tags=["orders", "daily"],
)
def orders_daily():
    @task
    def extract(data_interval_start=None, data_interval_end=None) -> str:
        # lê [data_interval_start, data_interval_end), grava em armazenamento remoto e devolve só o caminho
        ...
        return "s3://[BUCKET]/orders/2026-01-01/"      # exemplo de caminho; claim-check

    @task
    def load(path: str, data_interval_start=None, data_interval_end=None) -> None:
        # MERGE por chave, ou DELETE do intervalo + INSERT em uma transação
        ...

    @task
    def check(data_interval_start=None, data_interval_end=None) -> None:
        # contagem origem vs destino do intervalo; falha a tarefa se diferir sem explicação
        ...

    load(extract()) >> check()

orders_daily()
```
Idempotência em SQL (um dialeto genérico; adapte ao seu warehouse):
```sql
begin;
delete from mart.orders where order_date >= '{{ data_interval_start }}' and order_date < '{{ data_interval_end }}';
insert into mart.orders select ... from staging.orders where order_date >= '{{ data_interval_start }}' and order_date < '{{ data_interval_end }}';
commit;
```
Sem transação, a janela fica vazia entre as duas instruções: prefira `MERGE` quando o warehouse suporta e a chave existe.

## 3. Autoria, teste e depuração com gates
Fonte: V-14 (Astronomer `authoring-dags`, `testing-dags`, `debugging-dags`; Apache-2.0; Classe B). Correção importante: o `testing-dags` original dispara a DAG sem pedir consentimento e sem limite de iterações; o consentimento está só na skill de autoria. As salvaguardas abaixo são do plugin e estão rotuladas como tais.

Fases (seis, na fonte): descobrir, planejar, implementar, validar, testar, iterar.
| Fase | Ação | Gate (plugin) |
| --- | --- | --- |
| Descobrir | Convenções, conexões, variáveis, providers, versão do Airflow | |
| Planejar | Plano curto (template `plano-de-pipeline.md`) | Esperar aprovação do usuário antes de implementar |
| Implementar | Provider operators, TaskGroups, Dynamic Task Mapping, setup/teardown, Assets no Airflow 3 | |
| Validar | Teste de import; avisos de depreciação | |
| Testar | Disparar execução | Pedir consentimento antes de disparar e avisar que pode gravar dados; máximo de 3 ciclos disparo-correção, depois reavaliar com o usuário |
| Iterar / depurar | Log da exceção final; `upstream_failed` → investigar a tarefa que realmente falhou; timeout → consultar estado e perguntar antes de esperar mais | |
Depuração (V-14): classificar a falha (dados, código, infraestrutura, dependência); comparar com uma execução verde; verificar drift (imagem `latest`, versão de Python e de pacotes, upgrade recente); relatório com causa raiz, impacto (tabelas, downstream, dashboards), correção e prevenção (checks, alertas, pins). Template `relatorio-de-causa-raiz.md`. Hipóteses ordenadas por evidência a favor e contra, com o experimento mais barato que discrimina cada uma. Três hipóteses refutadas: parar e reportar.
A CLI `af`/Astro e o `astro-airflow-mcp` são ação do usuário ([ferramentas-e-mcp.md](ferramentas-e-mcp.md)). O hook `Stop` das skills originais não vem neste plugin.

## 4. Backfill
O plugin produz o plano; nunca executa (template `plano-de-backfill.md`). Itens (Inferido, ancorado em V-13, V-18, V-25):
1. Intervalo explícito (início e fim) e granularidade da partição.
2. Idempotência provada em dev: duas execuções, mesma contagem e soma de controle.
3. Estimativa de custo/bytes (`dry_run`/`EXPLAIN`) e limites de concorrência (`max_active_runs`, pools) para não saturar origem e warehouse.
4. Ensaio em dev com um intervalo pequeno.
5. Checagem pós-carga: contagem origem vs destino por partição.
6. Rollback: como restaurar o intervalo anterior (backup, time travel do warehouse, ou recarga), com a limitação de que rollback de código não restaura dado.
7. Aprovação humana nomeada para o alvo e o intervalo.
Exemplo de pedido e resposta: "Reprocesse janeiro de 2025 de `orders`." → plano com intervalo `[2025-01-01, 2025-02-01)`, 31 partições diárias, `MERGE` por `order_id`, ensaio em 2 dias, estimativa de bytes por partição pedida ao usuário (`dry_run`), `max_active_runs` baixo, checagem de contagem por dia e pergunta de quem aprova a execução em produção.

## 5. Dagster
Fonte: V-15 (`dagster-io/skills`, Apache-2.0, 211★; Classe B; docs mostram versão 1.13.26; o plugin antigo `dagster-expert` é stub deprecado). Cobertura parcial.
- Sequência de verificação: `dg check` → `dg list defs` → `dg launch` local no asset alterado → só então ambiente publicado.
- Todo asset idempotente, com `code_version`; asset check de frescor e de contagem; partição explícita para backfill (estes três últimos são Inferido: páginas de asset checks e partições não lidas).
- Construtos citados na fonte: `@dg.asset`, `deps`, `@multi_asset`, `@graph_asset`, `key_prefix`, `dg scaffold defs`.
- `dg launch`, `dg api` e `dg plus` alteram estado (materializar, encerrar runs, deploy): ação com autorização explícita do usuário na sessão.
- Ler a referência do tópico na doc da versão instalada em vez de responder de memória; a API muda entre versões.

## 6. Prefect e outros (lacuna L-14)
Prefect está no escopo do segmento e não tem item validado. Aplique só princípios agnósticos, rotulados Inferido, e mande conferir a doc oficial da versão instalada; não cite API do Prefect:
1. Idempotência por chave ou intervalo.
2. Intervalo de dados explícito na execução, sem "agora".
3. Sem trabalho pesado ou acesso a rede na importação do módulo do fluxo.
4. Segredos em armazenamento de segredos, nunca no código.
5. Consentimento antes de executar com efeito; teto de 3 ciclos.
6. Teste de carga do módulo (importa sem erro).
