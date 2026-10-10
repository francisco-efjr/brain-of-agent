# Decisões e trade-offs de frontend

Matrizes para as escolhas que mais se repetem. Cada decisão traz critério, a condição que a inverte e a fonte. O humano decide escolhas de arquitetura (renderização, cache, biblioteca de estado); o agente apresenta a matriz, recomenda com nível de confiança e espera a confirmação. Registro de decisão material: `../assets/templates/adr-frontend.md`. Conferido em 2026-10-10.

## Sumário

- [Renderização: SSR, SSG, ISR, SPA, prerender](#renderização-ssr-ssg-isr-spa-prerender)
- [Cache no Next.js 16.4](#cache-no-nextjs-164)
- [Formulários](#formulários)
- [Onde mora cada estado](#onde-mora-cada-estado)
- [Data fetching por framework](#data-fetching-por-framework)
- [Qual tipo de teste](#qual-tipo-de-teste)
- [Tailwind v3 ou v4 e tokens](#tailwind-v3-ou-v4-e-tokens)
- [Memoização e React Compiler](#memoização-e-react-compiler)
- [Plano obrigatório ou opcional](#plano-obrigatório-ou-opcional)
- [Avaliador de UI e custo](#avaliador-de-ui-e-custo)
- [Contexto do agente: CLAUDE.md, AGENTS.md, rules, skills](#contexto-do-agente-claudemd-agentsmd-rules-skills)
- [Migrações frequentes](#migrações-frequentes)

## Renderização: SSR, SSG, ISR, SPA, prerender

Fontes: Nuxt 4 rendering e Vue SSR (V-52), Next.js ISR e caching (V-51), brain (frontend-e-estado). Termos variam por framework: confirme na documentação da versão instalada.

| Necessidade | Escolha | Custo e condição que inverte |
| --- | --- | --- |
| Conteúdo público com SEO e dado por requisição | SSR | servidor sempre no caminho; cuide de poluição de estado entre requisições (Vue) e hidratação consistente |
| Conteúdo fixo ou raramente alterado | SSG / prerender | build refaz; conteúdo novo exige novo build ou ISR |
| Conteúdo que muda de vez em quando e precisa de cache | ISR / `swr` | só em runtime com suporte (Next: Node.js, não static export; Nuxt: `isr` depende de plataforma, `swr` do preset do Nitro); cache por instância sem handler compartilhado |
| App interno sem SEO | SPA (`ssr: false` no Nuxt) | primeira renderização no cliente; LCP pior; sem custo de servidor de render |
| Mistura por rota | híbrido: `routeRules` (Nuxt; não funciona com `nuxt generate`), segmentos do App Router (Next) | mais regras para manter; documente a decisão por rota |
| Tempo real | renderização dinâmica / cliente | sem cache de página; dado por requisição em `<Suspense>` (Next com Cache Components) |

Hidratação exige valores iniciais iguais no servidor e no cliente (hora, locale, armazenamento local, aleatoriedade) (brain). Dependência de CDN e plataforma vira pedido de integração para `/devops-cloud-infra:playbook`. Angular SSR e `@defer` não foram lidos: Não verificado.

## Cache no Next.js 16.4

(V-51.) Pergunta única: **`cacheComponents` está ligado em `next.config.*`?** Não misture os modelos.

| Estado | Modelo | Como decidir o conteúdo |
| --- | --- | --- |
| `cacheComponents: true` | Cache Components: `'use cache'` + `cacheLife`, `cacheTag`, `<Suspense>` para dado por requisição | dado de banco em função com `'use cache'` e `cacheLife`; runtime API (cookies, headers) e dado por requisição em `<Suspense>`; nada de `Date.now()` solto |
| ausente ou `false` | modelo anterior: `revalidate`, `revalidatePath`, `revalidateTag`, `generateStaticParams`, `dynamicParams` | muda pouco: revalidate alto (1 hora em vez de 1 segundo); escrita: `revalidateTag` ou `revalidatePath`; tempo real: dinâmico |

Apps novos do `create-next-app` já vêm com Cache Components e Partial Prefetching ligados; os dois serão padrão no próximo major (a doc lida em 2026-10-06). Ao migrar do modelo anterior para o novo, trate como projeto de migração com ADR e testes, não como ajuste de passagem. Confirmar na página atual antes de afirmar.

## Formulários

Fontes: Next.js forms e `useActionState` (V-46), Angular forms (V-47), web.dev/WCAG (V-45).

| Situação | Escolha | Observação |
| --- | --- | --- |
| Formulário simples, funciona sem JS | HTML nativo + validação nativa + envio ao servidor | `required`, `type`, `pattern`; servidor valida sempre |
| React/Next com App Router | Server Action + `useActionState` + schema (`safeParse`) | autenticar/autorizar em cada action; erros devolvidos como estado |
| React sem Server Actions | biblioteca de formulário que o projeto já usa (por exemplo React Hook Form com Zod, V-43) | não introduza outra |
| Angular, formulário central ou grande, reuso de modelo, teste sem DOM | reactive forms | `setValue` expõe erro de estrutura; `patchValue` falha silenciosamente |
| Angular, formulário curto e isolado | template-driven | |
| Angular v22 novo | avaliar Signal Forms depois de ler o guia | existem na v22; conteúdo não lido: Não verificado |
| Vue / Svelte | Não verificado (form actions do SvelteKit e formulários de Vue não lidos) | siga o padrão do projeto |

Em qualquer escolha: rótulo visível, erro ligado ao campo, resumo único para vários erros, 3.3.4 em envio sensível (`acessibilidade-wcag22.md`).

## Onde mora cada estado

Fonte: brain `frontend-e-estado.md`, V-13, V-48, V-26, V-27.

| Tipo de estado | Fonte de verdade | Exemplos |
| --- | --- | --- |
| Domínio do servidor | servidor, via query/loader com cache | lista de pedidos, perfil |
| Navegação | URL | filtros, ordenação, aba, paginação (compartilháveis) |
| Rascunho | estado local do formulário (com opção de persistir) | texto digitado antes de enviar |
| Efêmero de interação | estado local do componente | menu aberto, hover, foco |
| Derivado | calculado no render (`computed`, `$derived`) | total, lista filtrada |

Biblioteca de estado de cliente (Zustand, Redux, Pinia, SWR) **não foi pesquisada**: siga a que o projeto já usa e não recomende outra. Se o projeto não tem, comece pelo estado do próprio framework e da URL.

## Data fetching por framework

(V-13, V-48, V-49, V-50.)

| Framework | Padrão | Cuidado |
| --- | --- | --- |
| React puro | biblioteca (TanStack Query) ou, manual, Effect com flag `ignore` | `queryKey` com todos os parâmetros; `staleTime` de propósito; 3 retries já embutidos |
| Next (App Router) | Server Component com `await`; busca em paralelo (`Promise.all`) | waterfalls; guia de client-side data fetching do Next não lido |
| Nuxt 4 | `useFetch` (página), `useAsyncData` com `key` (lógica própria), `$fetch` (ação) | chave explícita; opções coincidentes para a mesma chave |
| SvelteKit | `load` em `+page.server.js` (segredo) ou `+page.js` | `redirect()` fora de `try`; `depends`/`invalidate` |
| Angular | `resource`/signals; HTTP via serviços | SSR e `@defer` não lidos |

## Qual tipo de teste

(V-55, V-20, V-56, V-41, brain.) Regra de escolha: o nível mais barato que pega o defeito.

| Quero pegar | Nível |
| --- | --- |
| Regra de negócio, formatação | unitário |
| Estado difícil de alcançar (erro, vazio, 1.000 itens) | componente |
| Interação interna e a11y de um widget | componente em navegador real (Storybook `play`, Vitest Browser Mode) |
| Aparência de componente estável | visual com baseline controlada |
| Jornada crítica com backend real | E2E (poucos) |
| Compatibilidade de motor | matriz Chromium, WebKit, Firefox no noturno; Safari real antes do release |

Playwright é a escolha padrão para projeto novo sem restrição forte (brain); time Java ou C# com Grid, ou Safari real obrigatório, aponta Selenium; time JS que valoriza time-travel e teste de componente maduro aponta Cypress. Não migre suíte estável por moda.

## Tailwind v3 ou v4 e tokens

(V-43, V-53.) Leia o `package.json`. v3: `tailwind.config.*` com tema em JS. v4: CSS com `@import "tailwindcss"` e `@theme`. Um modelo por projeto. Se houver mistura, proponha plano de migração antes de editar. Sem Tailwind, tokens como variáveis CSS em `:root` com nomes semânticos funcionam igual; o DTCG é só vocabulário (V-54).

## Memoização e React Compiler

(V-13, V-44.) Projeto com React Compiler: não adicione `useMemo`/`useCallback` por hábito; remova só com teste e medição. Projeto sem Compiler: memoize com medição (Profiler). Se não souber, pergunte (é dúvida material).

## Plano obrigatório ou opcional

(V-01 contra V-04.) UI nova ou redesenho: plano obrigatório (`plano-ui.md`). Correção localizada em que o diff cabe numa frase: pule o plano. Escolha de arquitetura (cache, renderização, biblioteca): gate humano antes de construir. Proporcionalidade é a regra de desempate.

## Avaliador de UI e custo

(V-09.) O avaliador cético com quatro critérios (design, originalidade, craft, funcionalidade), capturas e nota 0 a 10 foi caro no harness da Anthropic: no exemplo documentado, uma execução solo custou US$ 9 em 20 minutos contra US$ 200 em 6 horas no harness completo (modelos 4.5 e 4.6; valores de 2026, podem ter mudado). Use o `ui-evaluator` só em tela de produto, não em componente isolado. O limiar "reprovar abaixo de 6" é decisão de design deste plugin (Suposição). A nota é insumo; estética e UX são decisão humana; o avaliador é da mesma família do autor (independência parcial).

## Contexto do agente: CLAUDE.md, AGENTS.md, rules, skills

(V-30, V-32, V-33.) Ordem de colocação: hook ou permissão (garantia) > CLAUDE.md (fato universal curto, abaixo de 200 linhas; raiz de frontend abaixo de 60) > `.claude/rules/*.md` com `paths` > skill (procedimento) > subagente > MCP. O número de linhas de outros produtos (300, 500, 35 KB) não vale aqui: vale a documentação do produto-alvo. Se o projeto serve vários agentes com `AGENTS.md`, o `CLAUDE.md` importa `@AGENTS.md`.

## Migrações frequentes

Cobertura parcial; trate o resto como Não verificado e consulte o guia oficial da versão: React 18 para 19, Pages Router para App Router, Tailwind v3 para v4 (V-43, V-53: usar `@theme`; passo a passo não lido), Nuxt 3 para 4, Cypress para Playwright (V-40, `regras-migracao-testes.md`). Qualquer migração: plano em fatias, branch próprio, testes verdes antes e depois, ADR da decisão e nenhuma mistura de convenções de duas versões no mesmo arquivo.
