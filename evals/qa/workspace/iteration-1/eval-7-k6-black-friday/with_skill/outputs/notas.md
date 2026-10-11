# Notas — eval-7 k6 Black Friday (with_skill)

## Arquivos da skill lidos
- skills/qa/SKILL.md (inteiro)
- skills/qa/references/performance.md (inteiro; base do desenho: modelo aberto, Lei de Little, SLO/SLI, k6 completo, thresholds, abortOnFail/delayAbortEval, dropped_iterations, tipos de teste, template de relatório)
- skills/qa/references/dominios.md (inteiro; seção E-commerce: estoque do último item, cupom, "Pico" -> performance.md)
- skills/qa/references/dados-ambientes-ci.md (inteiro; manifesto do ambiente, massa sintética, virtualização, limpeza por namespace, preflight)
- skills/qa/references/estrategia.md (parcial: linhas 20-80 e 270-300; perguntas de contexto, "testar em produção com segurança", carga em produção só com autorização)
- Não abri: scripts/*.py, assets/templates/* (não necessários; não usei o template de relatório porque ainda não há resultado). Não li a pasta evals/ do repositório fora da pasta de saída.

## Verificação executada (local, sem rede, sem k6)
- k6 não está instalado; `node --check` na sintaxe (cópia .mjs).
- Harness em Node (no scratchpad) com stubs de k6/http, k6, k6/execution, k6/metrics e k6/data: rodei setup() e as quatro jornadas, caminhos de erro (502 HTML, produto errado, carrinho sem o item, busca sem resultado) e imprimi taxas/VUs/estágios/thresholds dos 5 perfis. Achou um bug (duração composta "2m30s"), corrigido.
- Não executei nada contra rede ou sistema real.

## Incertezas
- Rotas, nomes de campos e formato das respostas (busca, produto, login, carrinho, frete, pedido) são inventados; marcados como [PREMISSA] no script e na resposta.
- Taxas do funil (60%/20%/25%) e SLOs (p95/p99 por endpoint) são suposições sem dado do usuário; o script os trata como parâmetro/constante.
- Interpretei "3x" como 3x pedidos/hora (3.600/h = 1/s) e o pico de 1.200/h como média de hora cheia; pico por minuto desconhecido.
- Compatibilidade com o runtime do k6 (Goja): evitei matchAll/flatMap, mas usei object spread, template literals e `exec.scenario.iterationInTest` / `exec.vu.iterationInInstance`; não validei em k6 real. `rate` inteiro com `timeUnit: '1m'` é o que a skill/documentação do k6 permite, mas conferir ao rodar o smoke.
- Threshold `pedidos_criados: count>=90% do esperado` calculado pela área da rampa; no k6 real o número exato de iterações em taxas muito baixas (smoke) pode variar de 1; se o smoke falhar só por isso, reduzir o percentual.
- Sub-métricas por tag `name` com abortOnFail só no perfil carga; no estresse thresholds vermelhos são esperados.
- Tamanho do gerador (VUs ~555 na carga, ~1.100 no estresse) estimado por Lei de Little com durações de jornada supostas; sem medir memória/CPU reais do k6.
- Removi dados/usuarios.json (gerado, 400 KB); precisa rodar gerar_massa.py. As contas precisam ser semeadas no staging pela equipe (não coberto).
