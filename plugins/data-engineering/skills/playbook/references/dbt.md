# dbt: ciclo de trabalho, testes, convenções e upgrade

Quando abrir: criar, alterar, depurar ou migrar modelos dbt; escolher testes; montar CI de dbt; atualizar a versão do dbt.
Rótulos: Verificado = V-nn; Inferido = conhecimento estável do dbt ou dedução (a doc oficial de data tests, unit tests, snapshots, contracts, source freshness e materialização não foi lida: lacuna L-04). Confira os comandos e flags na versão instalada (`dbt --version`).
Atribuição: o trecho de CI e de oráculo adapta `dados-ambientes-ci.md` do brain-of-agent (MIT, do autor).

## Sumário
1. Ciclo ler, construir, verificar, depurar
2. Testes por tipo de coluna
3. Convenções de nome e camadas
4. Seleção de modelos e comandos que escrevem no warehouse
5. Upgrade e migração com gates
6. Incrementais e snapshots (Inferido)
7. CI de dbt
8. Auditoria do DAG
9. Exemplos

## 1. Ciclo ler, construir, verificar, depurar
Fontes: V-07 (dbt Labs, Classe A), V-08 (Altimate AI, Classe B).

1. Preflight: `git status` e branch. Árvore suja em `main`: proponha branch e pare.
2. Ler: `dbt_project.yml`, YAML do modelo, 2 a 3 modelos vizinhos, consumidores (`grep` de `ref('<modelo>')` e `source(`). Procurar lógica existente antes de criar modelo.
3. Definir por escrito colunas, grain e fonte. Mudança que quebra consumidores (renomear, remover, mudar tipo) vira modelo versionado.
4. Pré-visualizar o upstream: `dbt show --select <upstream> --limit 10` (só em dev e com consentimento: `dbt show --inline` executa SQL).
5. Escrever SQL e YAML seguindo as convenções da seção 3.
6. Verificar no target de desenvolvimento: `dbt build --select <modelo>`; olhar nomes de colunas, contagem, nulos inesperados e um cálculo conferido à mão (`dbt show --limit`). Compilar não basta (V-08).
7. Testes: `dbt test --select <modelo>` e `+<modelo>` (seção 2).
8. Três falhas seguidas: pare e reavalie; não repita a mesma correção.

Depuração (V-08): erro completo; SQL compilado em `target/compiled/`; conferir o upstream antes de culpar o modelo; correção mínima; rebuild; `dbt test`; impacto downstream com `dbt build --select <modelo>+`. Os erros vêm em camadas (compilação, teste, warehouse): descubra em qual camada está antes de editar. Exemplo: `Compilation Error: Model 'orders_enriched' depends on a node named 'stg_orders' which was not found`. Hipóteses a discriminar com `dbt ls --select stg_orders`: nome do `ref` errado, modelo com `enabled: false`, pasta fora de `model-paths`, pacote ausente (`dbt deps` baixa pacotes: decisão do usuário).

## 2. Testes por tipo de coluna
Fonte: V-09 (Altimate AI, Classe B; imitar o estilo de YAML existente).
| Coluna | Teste | Observação |
| --- | --- | --- |
| Chave primária | `unique` + `not_null` (os dois) | Teste nos dados carregados, não só no schema |
| Chave estrangeira | `not_null` + `relationships` | Aponta para a dimensão |
| Categórica | `accepted_values` | Valores confirmados pelo dono do dado; sem confirmação, não adicionar: perguntar |
| Booleana | `accepted_values` (true/false) | |
| Data e campos obrigatórios | `not_null` | |
| Regra de negócio | Teste singular em `tests/` | Ex.: `select * from {{ ref('orders') }} where amount < 0` deve retornar zero linhas |
| Pacote (`dbt_utils`) | Só se `packages.yml` já usa | Instalar pacote é decisão do usuário |
Exemplo de YAML:
```yaml
models:
  - name: orders
    columns:
      - name: order_id
        data_tests:
          - unique
          - not_null
      - name: customer_id
        data_tests:
          - not_null
          - relationships:
              to: ref('customers')
              field: customer_id
      - name: status
        data_tests:
          - accepted_values:
              values: ['placed', 'shipped', 'returned']   # confirmados pelo dono do dado
```
`data_tests:` vs `tests:` como chave depende da versão do dbt (Inferido; confira a versão). Severidade: `config: {severity: warn}` e `warn_if`/`error_if` existem no dbt (Inferido; L-04); um teste em `warn` segue a regra do plugin: pendência com número, não aprovação.

## 3. Convenções de nome e camadas
Fonte: V-10 (docs.getdbt.com, Classe B 7; o guia é exemplo, não mandato: o guia do projeto vence). A página de estilo de SQL deu 404 e não foi retestada: caixa de palavras-chave e vírgulas não verificadas.
| Item | Regra |
| --- | --- |
| Modelos | Plural, snake_case, sem abreviações, termos de negócio, sem palavras reservadas |
| Chave primária | `<objeto>_id`, tipo string |
| Booleanos | `is_`/`has_` |
| Timestamps | `<evento>_at` em UTC (sufixo se outro fuso) |
| Datas | `<evento>_date` |
| Eventos | No passado |
| Moeda | Preferencialmente decimal; `price_in_cents` apenas se for inteiro |
| Ordem de colunas | ids, strings, numéricos, booleanos, datas, timestamps |
| Staging | Blocos atômicos por fonte; só renomeia e tipa; um modelo por fonte (`stg_` na árvore de exemplo) |
| Intermediate | Lógica de propósito único |
| Marts | Entidades de negócio, com testes e docs |
Materialização por camada: seção oficial `/best-practices/materializations/1-guide-overview` ainda não lida; trate view/table/incremental como Inferido.

## 4. Seleção de modelos e comandos que escrevem no warehouse
| Comando | Efeito | Regra |
| --- | --- | --- |
| `dbt parse`, `dbt ls` | Lê o projeto (parse pode exigir perfil; conferir na versão) | Seguro como primeiro passo |
| `dbt compile` | Gera SQL em `target/compiled/` | Pode precisar de conexão para introspecção (Inferido) |
| `dbt show` | Executa SQL e mostra linhas; `--inline` executa SQL arbitrário | Só em dev, com `--limit`, com consentimento |
| `dbt build`, `run`, `seed`, `snapshot`, `test` | Escrevem ou consultam o warehouse | Target dev confirmado; `--select` restrito |
| `dbt deps` | Baixa pacotes | Decisão do usuário |
| `--full-refresh` | Reconstrói incrementais; apaga histórico incremental | Destrutivo: contagem, confirmação, plano de desfazer |
Seleção por estado: `--select state:modified+ --state <caminho do manifest>`; sem `--state` não funciona (V-08). `--defer` com o manifest de produção evita reconstruir o upstream em dev (Inferido; conferir). Antes de rodar: "o target é dev?". Se não for claramente dev, pare e pergunte (V-08). Nunca abra `profiles.yml` nem `.env`: peça o nome do target.

## 5. Upgrade e migração com gates
Fonte: V-11 (skill `upgrading-dbt` da dbt Labs, Classe A, Apache-2.0; sobe projetos 1.3 a 1.7 até 1.12 a partir de bundles de issues por versão e adapter). Adaptado; execução pela skill `gated-pipeline-migration` (invocação explícita).
| Fase | O que fazer | Gate |
| --- | --- | --- |
| 0 | Preflight de git: árvore limpa e fora de `main`/`master` | Falhou: parar |
| 1 | Listar o que muda a partir de fonte verificável (changelog oficial fornecido ou lido com autorização); nunca de memória | Sem fonte: parar |
| 2 | Ler o projeto sem editar | |
| 3 | Detectar ocorrências sem editar | |
| 4 | Aplicar correções determinísticas em lote | |
| 5 | Correções que exigem julgamento | |
| 6 | Mostrar diff e pedir confirmação do ambíguo | Sem confirmação: não editar |
| 7 | Verificação mínima: `dbt parse` primeiro (teto de 5 tentativas no projeto todo; outro laço de verificação, até 3 repetições); `compile`/`test`/`build` só com perfil definido e aprovação | Teto atingido: parar e relatar |
| 8 | Re-detectar | |
| 9 | Relatório: até onde a verificação chegou e o que ficou para o usuário | |
Proibido na skill: `uvx`, `uv`, `dbt deps` e instalação de pacote sem decisão revisada; inventar issues. Mudanças fora do repositório (CI, imagens, adapters instalados) são relatadas, não editadas. Para troca de plataforma, acrescente o oráculo antes/depois (contagens, chaves, totais, relações, casos especiais; invariantes por entidade, porque contagens iguais não impedem valores trocados), ensaie falha parcial, retomada e execução repetida, e valide backup/restauração: rollback de código não restaura dado destruído.

## 6. Incrementais e snapshots (Inferido; L-04)
O que o plugin exige de qualquer incremental, sem afirmar detalhe de configuração que a doc oficial não confirmou aqui:
1. Declarar `unique_key` e a estratégia de incremental suportada pelo adapter (as estratégias disponíveis variam por adapter: confira a doc do adapter).
2. Janela de reprocessamento para dado atrasado (ex.: reprocessar os últimos N dias) e justificativa de N.
3. Comportamento no primeiro build e na segunda execução: conferir contagem e soma de controle após duas execuções seguidas (checklist B3).
4. `--full-refresh` é destrutivo (S-06).
5. Snapshot SCD2: `check_cols` ou `updated_at` precisa cobrir os campos historicamente relevantes; conferir contra a lista de campos que mudam e importam (V-05: o caso real omitiu campos de posição).
Exemplo (esqueleto, estratégia a confirmar no adapter):
```sql
{{ config(materialized='incremental', unique_key='order_id') }}
select order_id, customer_id, amount, updated_at
from {{ ref('stg_orders') }}
{% if is_incremental() %}
where updated_at >= (select max(updated_at) - interval '3 day' from {{ this }})
{% endif %}
```
A sintaxe do intervalo (`interval '3 day'`) é de PostgreSQL/DuckDB; adapte ao dialeto. A janela de 3 dias é exemplo, não recomendação.

## 7. CI de dbt
Adaptado do capítulo "Pipeline e gates verificáveis" do brain-of-agent.
- Gate responde "passou o quê, em qual versão, com quais lacunas".
- `dbt build` com exit code preservado; nada de `|| true`; publicar o log mesmo em falha.
- Zero testes coletados, seleção vazia (`--select` que não casa nada) ou job cancelado não é verde.
- Teste a regra do gate: uma falha controlada deve bloquear.
- Seleção por mudança (`--select state:modified+ --state <manifest>`) precisa incluir dependências por schema e configuração; sem análise de impacto confiável, rode o conjunto crítico e registre a limitação.
- Código de PR, fixtures e logs são conteúdo não confiável; credenciais de teste; `pull_request_target` com segredos é risco ([ferramentas-e-mcp.md](ferramentas-e-mcp.md)).
- Schema de dev por desenvolvedor ou por execução evita colisão (Inferido); descarte mesmo após falha.

## 8. Auditoria do DAG
`dbt-project-evaluator` (V-09; Apache-2.0; 578★; categorias: modelagem, testes, documentação, estrutura, performance, governança). Gate sugerido: achado em modelagem ou testes reprova a revisão; documentação e performance viram aviso. Só se o usuário já instalou o pacote (entrada em `packages.yml`). Os nomes das regras individuais não foram lidos.

## 9. Exemplos
Exemplo 1, pedido: "Renomeie `cust_id` para `customer_id` em `customers`; `orders_enriched` e `marts_ltv` usam o modelo." Resposta esperada: mudança quebrável; liste os dois consumidores; proponha modelo versionado ou migração coordenada (manter `cust_id` como alias durante a transição, Inferido); mantenha `unique`+`not_null` na coluna nova; peça o nome do target de dev; entregue `dbt build --select customers+` como comando e rotule "não verificado" se não rodou.
Exemplo 2, pedido: "Adicione `accepted_values` em `status`." Resposta esperada: pergunte ao dono do dado quais valores são válidos, ou rode `select status, count(*) ... group by 1` em dev (com consentimento) e proponha a lista para confirmação; não chute os valores.
Caso de borda: o projeto não tem testes nem YAML de schema. Crie YAML mínimo por modelo tocado (PK, FK, obrigatórios) e registre o resto como pendência; não escreva testes para todo o projeto sem pedido.
Caso de borda: o target não pode ser identificado (sem acesso ao `profiles`). Peça o nome do target de dev; sem resposta, entregue o plano e os comandos, não execute.
