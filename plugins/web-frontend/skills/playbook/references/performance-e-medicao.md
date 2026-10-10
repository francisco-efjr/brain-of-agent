# Performance web e medição

Orçamentos de Core Web Vitals, diagnóstico por subparte do LCP, checklist de PR, ordem de revisão de React por impacto e o passo de medição que as fontes de regras não trazem. Leia em `perf-audit`, em revisão de PR com risco de desempenho ou em pedido "página lenta". Conferido em 2026-10-10 (V-15, V-18, V-57, V-10, V-61).

## Sumário

- [Regra de ouro: medir antes e depois](#regra-de-ouro-medir-antes-e-depois)
- [Limiares de Core Web Vitals](#limiares-de-core-web-vitals)
- [Orçamento e diagnóstico do LCP](#orçamento-e-diagnóstico-do-lcp)
- [Interação (INP) e estabilidade (CLS)](#interação-inp-e-estabilidade-cls)
- [Checklist de PR em 10 itens](#checklist-de-pr-em-10-itens)
- [Ordem de revisão de React por impacto](#ordem-de-revisão-de-react-por-impacto)
- [Medição: Lighthouse, DevTools e CI](#medição-lighthouse-devtools-e-ci)
- [Campo contra laboratório](#campo-contra-laboratório)
- [Formato do relatório](#formato-do-relatório)
- [Lacunas](#lacunas)

## Regra de ouro: medir antes e depois

Sem número, a recomendação vira palpite. Toda mudança de performance traz medição antes e depois nas mesmas condições (build, dispositivo ou emulação, rede, cache, viewport, usuário logado ou não), registradas em `../assets/templates/orcamento-performance.md`. Prefira dado de campo no percentil 75 quando existir; Lighthouse de laboratório é diagnóstico, não veredito (V-15, V-57). Não otimize métrica sintética se o fluxo real está bom (V-61).

## Limiares de Core Web Vitals

Verificado em web.dev (V-15): avaliados no percentil 75 dos acessos.

| Métrica | Bom | Ruim (acima de) |
| --- | --- | --- |
| LCP (Largest Contentful Paint) | até 2,5 s | 4 s |
| INP (Interaction to Next Paint) | até 200 ms | 500 ms |
| CLS (Cumulative Layout Shift) | até 0,1 | 0,25 |

Entre "bom" e "ruim" a faixa é "precisa melhorar". A página de INP lida não traz técnicas de otimização; as técnicas abaixo vêm de V-18 e prática comum.

## Orçamento e diagnóstico do LCP

Subpartes do LCP e diretrizes de orçamento (web.dev optimize-lcp, atualizada em 31 mar 2025; são diretrizes, não regras; V-15):

| Subparte | Orçamento aproximado |
| --- | --- |
| Time to First Byte (TTFB) | cerca de 40% |
| Atraso de carregamento do recurso | abaixo de 10% |
| Duração do download do recurso | cerca de 40% |
| Atraso de renderização do elemento | abaixo de 10% |

Atenção à ordem: 40/10/40/10 (um relatório anterior trocou para 40/10/10/40). Decomponha o LCP medido nessas quatro partes e ataque a que passa do orçamento.

Checklist LCP em 5 itens (V-15):

1. O elemento LCP é descobrível no HTML inicial (não só após JS ou CSS).
2. Recurso descoberto só por CSS ou JS recebe `preload`.
3. `fetchpriority="high"` com moderação: em no máximo uma ou duas imagens.
4. Nenhum `loading="lazy"` na imagem do LCP nem em imagens acima da dobra.
5. Evite renderizar no cliente o elemento do LCP.

## Interação (INP) e estabilidade (CLS)

Práticas de V-18 (classe B, awesome-copilot, MIT; destilação):

- Handlers de evento abaixo de 50 ms; quebre tarefas longas. A Long Animation Frames API (Chrome 123 ou superior) ajuda a localizar quadros longos.
- Em React, `useTransition` e `useDeferredValue` adiam trabalho não urgente.
- Virtualize listas acima de cerca de 100 itens, preservando navegação assistiva e busca quando elas fazem parte do uso (brain).
- Anime só `transform` e `opacity`.
- No máximo um redirect no carregamento (cada um custa de 200 a 300 ms, segundo V-18).
- CLS: dimensões de imagem e de embed declaradas, banners injetados com espaço reservado, `font-display` adequado (Inferido por prática comum, confirme no DevTools).

## Checklist de PR em 10 itens

Por fase, para revisar um PR de frontend (V-18, destilado):

| Fase | Item |
| --- | --- |
| Carregamento | 1. Scripts com `defer` ou `async`; sem bloqueio no `<head>` sem motivo. |
| Carregamento | 2. Imagens com dimensões e formato adequado; sem lazy-load acima da dobra. |
| Carregamento | 3. Fontes em WOFF2 com `font-display` definido. |
| Render | 4. Animações só em `transform` e `opacity`. |
| Render | 5. Listas longas virtualizadas. |
| Interação | 6. Handlers curtos; trabalho pesado fora do caminho do evento. |
| Interação | 7. `useTransition` ou `useDeferredValue` para atualizações não urgentes (React). |
| Bundle | 8. Sem barrel files que puxam módulos inteiros. |
| Bundle | 9. Import dinâmico por rota ou por componente pesado. |
| Bundle | 10. Nada de dependência nova para problema pequeno; medir tamanho antes de adicionar. |

## Ordem de revisão de React por impacto

Base: `vercel-labs/agent-skills` `react-best-practices` (V-10; classe B; MIT declarado e não confirmado, por isso só destilação). A fonte tem 70 regras em 8 categorias em ordem de impacto; parte das regras é específica do Next.js. Revise nesta ordem e pare ao achar o gargalo medido:

| Prioridade | Categoria | Pergunta curta |
| --- | --- | --- |
| 1 (crítico) | Waterfalls | Há `await` independentes em série? Dá para buscar em paralelo (`Promise.all`)? |
| 2 (crítico) | Bundle | Há barrel imports, biblioteca inteira importada, componente pesado sem import dinâmico? |
| 3 (alto) | Servidor | Há dados serializados demais indo ao cliente? Há busca duplicada entre componentes? |
| 4 | Data fetching no cliente | A mesma consulta é feita em vários lugares sem biblioteca de cache? |
| 5 | Re-render | Há estado derivado guardado em effect? Objetos ou funções novos a cada render quebrando memoização que de fato importa? |
| 6 | Renderização | Há trabalho caro no render? Listas sem chave estável? |
| 7 | JavaScript | Laços e cópias desnecessárias em caminhos quentes? |
| 8 | Padrões avançados | Só depois de medir. |

O que a fonte não traz e este plugin acrescenta (Inferido, prática comum): passo de medição antes de mexer (React Profiler para re-render, bundle analyzer para bundle, Lighthouse e aba Performance do DevTools para o resto). Memoização (`useMemo`, `useCallback`) só com medição, e pergunte se o projeto usa React Compiler antes (V-13, V-44). A alegação "2 a 10 vezes" de ganho em waterfalls feita pelo material não foi verificada.

## Medição: Lighthouse, DevTools e CI

(V-57; Lighthouse overview atualizada em 2025-06-02, página de 16 meses: confira a documentação atual.)

- DevTools (Lighthouse e aba Performance) é o caminho recomendado para páginas locais e autenticadas. A extensão do Chrome não testa páginas locais nem autenticadas.
- CLI, em build de produção local, anexando o JSON ao relatório (precisa de Chrome):

```bash
lighthouse <url> --output json --output-path <arquivo>
```

  Instalar o CLI (`npm install -g lighthouse`) é código de terceiros: faça só com autorização do usuário.
- CI: Lighthouse CI com `lighthouserc.js` na raiz e `lhci autorun` com asserções de orçamento (limiares acima) para falhar o build. Fixe a versão (`@lhci/cli@0.15.x` no guia lido). **Omita o upload para "temporary public storage"**: ele gera URL pública do relatório (aviso do próprio guia). Detalhes de risco em `ferramentas-e-mcp.md`.
- A nota de acessibilidade do Lighthouse é parcial e não substitui axe nem teste manual.
- Registre: viewport, throttling de CPU e rede, cache limpo ou não, versão do Lighthouse e do Chrome, número de execuções (mediana de várias; uma execução não prova nada).

## Campo contra laboratório

Laboratório (Lighthouse, DevTools) é reprodutível e bom para diagnosticar; campo (usuários reais, percentil 75) é o que a avaliação de Core Web Vitals usa. Quando houver RUM ou dados de campo, prefira-os e peça-os ao usuário (a coleta pertence a `/sre-observability:playbook`). Fonte para dados de campo (CrUX) não foi lida neste plugin: Não verificado.

## Formato do relatório

`../assets/templates/orcamento-performance.md`: métrica, limiar bom e ruim, antes, depois, condições, origem (campo ou laboratório). Achados no formato do relatório de revisão: problema, evidência (número), onde olhar (`arquivo:linha`), por que ajuda, como validar depois. Não proponha reescrita ampla nem dependência nova para problema pequeno.

## Lacunas

DevTools Performance em profundidade e CrUX não foram lidos; compatibilidade por navegador de recursos novos (container queries, Trusted Types) deve ser conferida na tabela do MDN no momento do uso; Angular SSR e `@defer` sem fonte lida. Trate como Não verificado.
