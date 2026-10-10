# Oráculo antes/depois e ensaio para `gated-pipeline-migration`

Adaptado de `brains/qa/references/dados-ambientes-ci.md` (brain-of-agent, licença MIT, do autor deste plugin; seções "Equivalência de ambiente" e "Migração e liberação") e das fases de V-11 (`upgrading-dbt`, dbt Labs, Apache-2.0, reescrito). Trecho literal do brain, com atribuição:

> Migração requer oráculo antes/depois: contagens, chaves, totais, relações, casos especiais e capacidade de ler/escrever. Contagens iguais não impedem valores trocados entre clientes; amostras e invariantes por entidade ajudam a detectar essa classe de erro. Use volume realista para medir tempo e bloqueio.
> (brain-of-agent, `brains/qa/references/dados-ambientes-ci.md`, MIT)

As consultas são SQL quase padrão e exigem adaptação ao dialeto (Inferido). Executá-las é ação do usuário em ambiente de desenvolvimento ou ensaio, com custo estimado antes.

## Sumário

1. Desenhar o oráculo antes de mover dado
2. Consultas de comparação
3. Diferenças de plataforma que costumam mudar o resultado
4. Ensaiar falhas
5. Expandir, migrar, remover
6. Corte e rollback
7. Exemplo de T-07 preenchido (upgrade de versão)

## 1. Desenhar o oráculo antes de mover dado

Escreva o oráculo no plano, antes de qualquer migração, com dono e tolerância.

| Dimensão | O que medir | Tolerância | Quem confere |
| --- | --- | --- | --- |
| Volume | linhas por tabela e por partição/dia | zero, ou diferença explicada por filtro declarado | dono do dado |
| Chaves | unicidade e não nulo das PKs; órfãos de FK | zero | dono |
| Totais | soma de medidas (valor, quantidade) por dia e por categoria | zero para inteiros e decimais; tolerância definida para float | dono |
| Entidade | total e contagem por entidade para uma amostra (clientes de borda) | zero | dono |
| Faixa de chave | soma de controle por balde de hash de chave | zero | plataforma |
| Casos especiais | nulos históricos, duplicidades possíveis, campos legados, encoding, fuso, linhas com valor zero | caso a caso | dono |
| Capacidade | ler e escrever com o volume realista; tempo e bloqueios | meta de SLA | plataforma |

## 2. Consultas de comparação

```sql
-- (a) volume por partição, dos dois lados (rode em cada plataforma e compare as tabelas de resultado)
select cast(created_at as date) as d, count(*) as n, sum(amount) as soma
from <tabela> where created_at < :corte group by 1 order by 1;

-- (b) chaves únicas e não nulas
select count(*) as n, count(distinct order_id) as n_chaves,
       sum(case when order_id is null then 1 else 0 end) as chave_nula
from <tabela>;

-- (c) soma de controle por balde de chave: acha a faixa divergente sem varrer tudo
select mod(abs(<função_hash>(order_id)), 64) as balde, count(*) as n, sum(amount) as soma
from <tabela> group by 1 order by 1;

-- (d) invariantes por entidade para uma amostra de clientes (ids sintéticos ou mascarados)
select customer_id, count(*) as pedidos, sum(amount) as total, min(created_at) as primeiro, max(created_at) as ultimo
from <tabela> where customer_id in (<amostra>) group by 1 order by 1;
```
A função de hash difere por plataforma e precisa ser a mesma nos dois lados (ou use uma função determinística equivalente aplicada a um valor já normalizado em texto). Em (c), refine o balde divergente até chegar às linhas.

## 3. Diferenças de plataforma que costumam mudar o resultado

Lista de verificação (Inferido, conhecimento estável de SQL; confirme na documentação de cada engine):
- Divisão inteira: alguns engines devolvem inteiro, outros decimal.
- Ordenação de NULL (primeiro ou último) e ordenação de texto (collation, maiúsculas e minúsculas, acentos).
- Precisão e arredondamento de decimal e de float; tipo numérico padrão.
- Precisão de timestamp (micro, nano) e fuso padrão da sessão; `DATE(ts)` e `CURRENT_DATE` dependem do fuso.
- Semântica de `NOT IN` com NULL, `UNION` vs `UNION ALL` e de `GROUP BY` com NULL.
- Funções de data e texto com nomes iguais e comportamento diferente.
- Palavras reservadas e identificadores com caixa (entre aspas).
- Tipos semiestruturados (JSON/VARIANT/STRUCT): nulo SQL vs nulo JSON.
- Transações, isolamento e atomicidade de DDL.
- Limites (tamanho de linha, de consulta, de partições).
Cada diferença encontrada no código vira um caso de teste do oráculo.

## 4. Ensaiar falhas

Em ambiente de ensaio, e só com autorização do dono do ambiente:
- Falha parcial no meio da carga e retomada: o resultado final é igual ao de uma execução sem falha.
- Execução repetida (idempotência): a segunda execução não muda contagens nem somas.
- Dado atrasado, duplicado ou fora de ordem na entrada.
- Indisponibilidade da origem ou do destino por alguns minutos: backlog, recuperação e alertas observáveis.
- Falha de setup (credencial, permissão, versão errada) é bloqueio, não aprovação: registre e pare.

## 5. Expandir, migrar, remover

1. **Expandir:** crie a coluna/tabela/modelo novo ao lado do antigo; ambos funcionam.
2. **Migrar:** consumidores passam ao novo, um a um, com lista e data; período de convivência definido; teste de convivência das versões suportadas.
3. **Remover:** só quando nenhum consumidor usa o antigo (confirmado por quem conhece os consumidores externos ao repositório; Suposição enquanto não houver confirmação).
Um upgrade de versão que exige mudança de modelo segue o mesmo trilho (ver `dbt-model-workflow`, modelo versionado).

## 6. Corte e rollback

- Corte é decisão humana nomeada, com a hora, os critérios de saída e os de rollback escritos antes.
- Rollback de código não restaura dado destruído. Valide backup e restauração, ou um caminho de correção, antes de qualquer etapa destrutiva; a skill não executa restauração.
- Execução paralela (antigo e novo) por uma janela, com reconciliação diária pelo oráculo, reduz o risco; custo e confusão de duas fontes precisam ser aceitos pelo dono.
- Finalize com o risco residual e a ação que ele exige, por exemplo "integração X não executada; liberação depende de verificar Y no candidato Z". "Nada encontrado" sem cobertura declarada não é aprovação.

## 7. Exemplo de T-07 preenchido (upgrade de versão, ilustrativo)

```text
Migração: dbt <origem> -> <destino>; adapter <x>
Fase 0 Preflight: branch migracao/dbt-novo, árvore limpa, commit de partida abc1234 (Verificado)
Fase 1 Fonte: guia oficial de upgrade <URL> lido em 2026-10-10; 7 mudanças (4 determinísticas, 2 julgamento, 1 fora do repo)
Fase 2 Leitura: dbt_project.yml, packages.yml, 143 modelos, 12 macros
Fase 3 Detecção: 23 ocorrências determinísticas; 5 de julgamento (arquivo:linha na tabela anexa)
   Portão: usuário aprovou plano em <data/hora>
Fase 4 Determinísticas: aplicadas (23)
Fase 5 Julgamento: 3 aplicadas após confirmação; 2 pendentes (decisão do usuário)
Fase 6 Diff: mostrado e confirmado
Fase 7 Verificação: parse OK (tentativa 2/5); build não executado (sem target dev confirmado)
Fase 8 Re-detecção: 0 residuais determinísticas; 2 de julgamento listadas
Fase 9 Relatório: fora do repositório (imagem base do CI; configuração do scheduler) para o usuário
Oráculo (se houver dados): n/a para upgrade só de código; obrigatório em troca de plataforma
Não verificado: execução em dev, comportamento em runtime de macros customizadas
```
