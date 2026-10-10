# Custo, escolha de modelo, cache, Batch e latência

Base: V-38 (preços, Batch, contagem de tokens, escolha de modelo), V-24 (prompt caching), V-25 (cache e latência), V-37 (cache e formato). **Dados voláteis, lidos em 2026-10-10.** A página de preços não traz data impressa: a data de leitura é a referência. Antes de orçar, reabra https://platform.claude.com/docs/en/about-claude/pricing e https://platform.claude.com/docs/en/build-with-claude/prompt-caching. A página de limites de taxa não foi lida.

## Tabela de preços (US$ por milhão de tokens, leitura de 2026-10-10)

| Modelo | Entrada base / saída | Leitura de cache | Batch (entrada / saída) |
| --- | --- | --- | --- |
| Fable 5.1 (Mythos 5.1: mesmo preço, disponibilidade limitada) | 10 / 50 | 0,25 | 5 / 25 |
| Opus 5.5 | 4 / 20 | 0,20 | 2 / 10 |
| Sonnet 5.5 | 2 / 10 | 0,10 | 1 / 5 |
| Haiku 5.5 (prompt até 100 mil tokens) | 0,10 / 0,50 | 0,01 | 0,05 / 0,25 |
| Haiku 5.5 (prompt acima de 100 mil) | 0,50 / 2,50 | 0,05 | 0,25 / 1,25 |

Regras (V-38, V-24): escrita de cache de 5 minutos a 1,25x e de 1 hora a 2x da entrada base (Fable 5.1: 12,50 e 20; Haiku 5.5: 0,125 e 0,20). Leitura de cache 0,1x como regra, 0,05x em Opus 5.5 e Sonnet 5.5, 0,025x em Fable 5.1 e Mythos 5.1. `inference_geo: "us"` soma 1,1x em tudo. Fast mode (pesquisa) tem preço premium (Opus 5.5: 8 / 40) e não combina com Batch. O novo tokenizador gera cerca de 30% mais tokens para o mesmo texto (Claude 4.7 em diante, inclusive Fable 5.1 e Mythos 5.1): recontar ao trocar de modelo.

## Mínimos de cache (V-24; releia a tabela na data de uso)

| Modelos | Mínimo cacheável |
| --- | --- |
| Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, Sonnet 5.5, Fable 5, Mythos 5, Haiku 5.5 | 512 tokens |
| Opus 4.8, Sonnet 5, Sonnet 4.6, Sonnet 4.5 | 1.024 |
| Opus 4.7, Mythos Preview, Haiku 3.5 | 2.048 |
| Opus 4.6, Opus 4.5, Haiku 4.5 | 4.096 |

Tabela reconferida na página de prompt caching em 2026-10-10 (Verificado). Atenção: Sonnet 5 fica em 1.024, não em 512.

Abaixo do mínimo não há erro nem cache. Prefixo na ordem tools, system, messages; até 4 pontos de corte explícitos (o quinto retorna erro 400); cache automático por campo de topo; TTL de 5 minutos (padrão) ou 1 hora; entradas de 1 hora antes das de 5 minutos. Medir `cache_creation_input_tokens` e `cache_read_input_tokens`: ambos zero = abaixo do mínimo ou prefixo mudou.

## Batch (V-38)

Até 100.000 requisições ou 256 MB (o que vier primeiro); a maioria termina em menos de 1 hora; expira se não concluir em 24 horas; resultados disponíveis por 29 dias; `stream: true` não se aplica; metade do preço. Procedimento para suíte de avaliação: enviar em lote, guardar o `custom_id`, baixar resultados em até 29 dias, tratar expiração como falha parcial e repetir o lote inteiro quando o prompt mudar.

Contagem de tokens: gratuita, é estimativa, tem limites por faixa (Start 5.000, Build 10.000, Scale 20.000 requisições por minuto), independente do limite de criação de mensagens, não usa cache de prompt e não aceita server tools (exceto advisor), conector MCP nem blocos de imagem/documento por URL ou arquivo.

## Contas de exemplo (Suposições do usuário; mostrar sempre a conta)

Pedido (caso de reserva `custo-30-casos`): 30 casos × 3 execuções no Sonnet 5.5, ~8 mil tokens de entrada e ~1,5 mil de saída por execução. Os números de tokens são **Suposição** do usuário.

1. Execuções: 30 × 3 = 90.
2. Entrada: 90 × 8.000 = 720.000 tokens = 0,72 M × US$ 2 = **US$ 1,44**.
3. Saída: 90 × 1.500 = 135.000 tokens = 0,135 M × US$ 10 = **US$ 1,35**.
4. Total sem cache nem Batch: **US$ 2,79**.
5. Com Batch (metade do preço, entrada 1 / saída 5): 0,72 × 1 + 0,135 × 5 = US$ 0,72 + US$ 0,675 = **US$ 1,395**. Ressalva: resultados só em até 24 h; aplica-se se a suíte não é interativa.
6. Efeito do tokenizador (+30% se os 8 mil/1,5 mil foram medidos num modelo anterior ao 4.7): 2,79 × 1,3 ≈ US$ 3,63. Recontar com o modelo-alvo.
7. Com cache de prefixo (sem Batch), supondo que 6.000 dos 8.000 tokens de entrada são um prefixo estático idêntico e que as 90 execuções caem dentro da janela de 5 minutos: escrita 6.000 × 1,25 × US$ 2/M = US$ 0,015; leituras 89 × 6.000 = 534.000 tokens × US$ 0,10/M = US$ 0,0534; entrada variável 90 × 2.000 = 180.000 × US$ 2/M = US$ 0,36; saída US$ 1,35; total ≈ **US$ 1,78**. Se as execuções espaçarem mais de 5 minutos, o cache expira e o ganho some (use TTL de 1 hora a 2x na escrita). Combinar cache com Batch: **Não verificado**.

Planilha (template `planilha-de-custo.md`): colunas: tarefa, modelo, tokens de entrada (sem cache), tokens de entrada em cache (escrita), tokens de entrada em cache (leitura), tokens de saída, execuções, fator Batch, custo, data dos preços, data da contagem de tokens.

## Escolha de modelo e `effort` (V-38)

1. Monte a suíte própria (20 a 50 tarefas, ver `eval-design`).
2. Comece pelo modelo mais barato que a suíte aceitar (estratégia efficiency-first começa no Haiku 5.5; capability-first começa no Opus 5.5; a página de escolha de modelo lista as duas).
3. Antes de trocar de modelo, varie o `effort`: ajustar o esforço costuma ser melhor do que trocar de modelo. Padrões: `high` em Fable 5.1, Opus 5 e Sonnet 5.5; `medium` em Opus 5.5 e Haiku 5.5.
4. Suba de modelo só para os casos que falham na suíte. Combine modelos quando fizer sentido (executor com advisor, ou orquestrador com trabalhadores baratos).
5. Registre modelo, `effort`, data e contagem de tokens junto de cada rodada.

Ao trocar para Opus 5.5, Sonnet 5.5, Fable 5.1 ou Mythos 5.1: `tool_choice` `any`/`tool` retorna 400 (Verificado na página "Define tools" em 2026-10-10); desligar o raciocínio ou usar `computer_20251124` no Opus 5.5 exige ler a página de migração antes (Não verificado).

## Latência (Inferido a partir de V-24, V-25, V-38; sem página de latência lida)

| Alavanca | Efeito esperado | Cuidado |
| --- | --- | --- |
| `effort` menor | Menos raciocínio, resposta mais rápida | Medir qualidade na suíte |
| Modelo menor | Menor latência e custo | Medir qualidade; subir só nos casos que falham |
| Streaming | Latência percebida menor (primeiro token) | Não reduz o tempo total; o cliente precisa montar JSON de tool só ao fim do bloco |
| Cache de prefixo | A fonte de RAG relata menos da metade da latência em medição do fabricante | Prefixo estável; ambos os campos de uso zerados indicam falha |
| Fast mode | Mais rápido a preço premium (pesquisa) | Não combina com Batch; opção paga |
| Menos tokens de saída | Menos tempo | Saída estruturada concisa; `response_format` concise em tools |

Meça p50 e p95 na suíte própria, incluindo retries e chamadas de tool. Não prometa latência.
