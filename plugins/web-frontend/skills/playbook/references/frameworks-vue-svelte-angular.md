# Vue e Nuxt, Svelte e SvelteKit, Angular

Regras de revisão por framework, com a versão lida e o que ficou como lacuna. Leia quando o projeto não for React/Next ou quando a tarefa pedir comparação de abordagem. Conferido em 2026-10-10 (V-25, V-26, V-27, V-47, V-49, V-50, V-52). **Antes de aplicar qualquer regra, confirme a versão no `package.json`**: Nuxt 3 e 4 diferem, SvelteKit anterior à 2.16 usa tipos individuais, Angular v22 trouxe Signal Forms.

## Sumário

- [Matriz de decisão por framework](#matriz-de-decisão-por-framework)
- [Vue](#vue)
- [Nuxt 4](#nuxt-4)
- [Svelte 5](#svelte-5)
- [SvelteKit](#sveltekit)
- [Angular v22](#angular-v22)
- [Lacunas](#lacunas)

## Matriz de decisão por framework

| Pergunta | Vue / Nuxt | Svelte / SvelteKit | Angular |
| --- | --- | --- | --- |
| Valor derivado | `computed` | `$derived` | `computed` / `linkedSignal` / `resource` |
| Efeito colateral | `watch`/`watchEffect` com parcimônia (Inferido) | `$effect` como último recurso, sem atualizar estado | `effect` só para API não reativa |
| Dado de página | `useFetch` / `useAsyncData` | `load` em `+page.server.js` ou `+page.js` | Não verificado (SSR e `@defer` não lidos) |
| Formulário | Não verificado | Form actions não lidas | reactive forms (central, grande), template-driven (curto); Signal Forms: avaliar após ler o guia |
| SSR | cuidado com estado singleton entre requisições | `load` de servidor separa o que é segredo | Não verificado |

## Vue

Fontes: Vue, production deployment (V-25) e SSR (V-52), Verificado.

Build de produção (setup customizado, sem Vite padrão):

1. `vue` resolve para `vue.runtime.esm-bundler.js`.
2. Flags de compilação definidas e `process.env.NODE_ENV` substituído por `"production"` (builds de desenvolvimento têm avisos e validações que custam desempenho).
3. `app.config.errorHandler` registrado para reportar erros.

SSR (Vue):

- **Poluição de estado entre requisições:** módulos de servidor são inicializados uma vez e reaproveitados; um singleton (app, router, store) vaza dado de um usuário para outro. Crie app, router e store por requisição.
- Código de navegador (`window`, `document`) só em hooks de ciclo de vida (`onMounted`).
- Fontes de mismatch na hidratação: valores aleatórios e fusos horários diferentes; use `v-if` com `onMounted` ou uma semente. `data-allow-mismatch` existe a partir do Vue 3.5, como exceção documentada, não como correção.
- Teleport precisa de contêiner dedicado em SSR.
- Estado serializado em `<script>` exige escape adequado (Inferido, regra de V-22; a página do Vue não trata disso). Nunca `v-html` com dado externo.

## Nuxt 4

Fontes: Nuxt 4.6.0, data fetching e rendering (V-49, V-52), Verificado. A URL sem `/4.x/` retornou 404 na pesquisa: use `https://nuxt.com/docs/4.x/getting-started/data-fetching`.

Escolha de API de dados:

| Caso | Use |
| --- | --- |
| Carga de página com uma chamada | `useFetch` |
| Lógica própria (CMS, SDK, várias chamadas com `Promise.all`) | `useAsyncData` com `key` explícita |
| Ação do usuário (submit, clique) | `$fetch` |
| Não bloquear a navegação | `lazy: true` ou `useLazyFetch`, em vez de "não dar await" |

Regras: `useFetch` e `useAsyncData` repassam os dados do servidor ao cliente no payload, evitando buscar duas vezes na hidratação; `$fetch` solto no `setup` pode buscar duas vezes. Para `useAsyncData`, crie sempre a sua chave, sobretudo em composables. Chaves iguais compartilham `data`, `error` e `status`; nesse caso as opções `handler`, `deep`, `transform`, `pick`, `getCachedData` e `default` precisam coincidir (aviso em dev), enquanto `server`, `lazy`, `immediate`, `dedupe` e `watch` podem diferir. Com `server: false` ou `lazy`, trate `status` e `data` indefinido no `setup`. Efeitos como uma ação de store Pinia dentro de `useAsyncData` devem usar `callOnce`. Use `pick` para reduzir payload.

Modos de renderização (`routeRules`: `redirect`, `ssr`, `cors`, `headers`, `swr`, `isr`, `prerender`, `noScripts`, `appMiddleware`):

| Necessidade | Escolha |
| --- | --- |
| Conteúdo e SEO | SSR universal |
| App interno sem SEO | SPA (`ssr: false`) |
| Conteúdo fixo | prerender |
| Mistura por rota | `routeRules` (renderização híbrida não funciona com `nuxt generate`) |
| Cache em borda | `swr` (`true` ou segundos) ou `isr`; `isr` só adiciona cache em CDN em plataformas que suportam (Netlify e Vercel, segundo a página); `swr` com cache completo depende do preset do Nitro |

Não existe opção `cache` em `routeRules`; o cache é `swr` ou `isr`. `ssr: false` exclui o componente do bundle de servidor. Dependência de plataforma de CDN vira pedido de integração para `/devops-cloud-infra:playbook`.

## Svelte 5

Fonte: Svelte best practices (V-27, Verificado; a página não cobre `{@html}` nem SvelteKit).

- `$state` só para o que deve ser reativo; `$state.raw` para objetos grandes que são reatribuídos, não mutados.
- `$derived` em vez de `$effect` para valores calculáveis.
- `$effect` é último recurso e não deve atualizar estado.
- `{@attach}` para integrar bibliotecas externas; `createSubscriber` para fontes externas reativas.
- `<svelte:window>` e `<svelte:document>` para listeners globais.
- Segurança: `{@html}` com dado externo é um sink de XSS (regra de V-22, Inferida para Svelte); sanitize antes.

## SvelteKit

Fonte: `https://svelte.dev/docs/kit/load` (V-50, lida inteira, Verificado).

- `+page.server.js` roda só no servidor e devolve dado serializável com devalue (aceita `Date`, `Map`, `Set`, `BigInt`, `RegExp`, promises para streaming). `+page.js` roda nos dois lados e pode devolver classes e construtores. **Segredo e banco só em `+page.server.js`.**
- O `fetch` do `load` herda `cookie` e `authorization` no servidor.
- Evite waterfalls: busque independentes em paralelo (`Promise.all`) e chame `await parent()` só depois de buscar o resto.
- **Não use `redirect()` nem `error()` dentro de `try/catch`.**
- `setHeaders` não aceita o mesmo cabeçalho duas vezes nem `set-cookie`.
- Em streaming, promise que rejeita antes de a renderização começar, sem tratamento, pode derrubar o servidor (o `fetch` do SvelteKit já trata).
- Recarregar dado: `depends('app:chave')` no load e `invalidate('app:chave')` no cliente; `refreshAll()` substitui `invalidateAll` (descontinuado). O load de servidor não depende automaticamente das URLs buscadas, para não vazar segredo.
- Tipos: `PageProps`/`LayoutProps` a partir da 2.16.0.

## Angular v22

Fontes: angular.dev, signals e forms (V-26, V-47, Verificado; a seção Signal Forms não carregou em texto).

Signals:

- `computed` é somente leitura, lazy e memoizado: derivação vai nele (ou em `linkedSignal` ou `resource`), não em `effect`.
- `effect` só para efeitos em APIs não reativas.
- Contexto reativo vale só em código síncrono: leia os sinais antes de qualquer `await`; `untracked` para ler sem dependência.
- Em componentes OnPush, sinal lido no template marca o componente.
- A página não decide signals contra observables: não afirme preferência oficial (Não verificado).

Formulários:

- Reactive forms: mais escaláveis, reutilizáveis e testáveis, com acesso direto ao modelo e teste sem renderizar a UI. Template-driven: casos simples.
- `setValue()` exige a estrutura completa e acusa erro de aninhamento; `patchValue()` falha silenciosamente nesses erros. Prefira `setValue` quando quiser que o erro de estrutura apareça.
- Mostre erro após `markAsTouched`; estado por `markAsTouched` e `markAsDirty`.
- Acessibilidade de erro não é tratada no guia: use `acessibilidade-wcag22.md`.
- Projeto novo na v22: avalie Signal Forms depois de ler o guia (existem e há página "Migrating from Reactive Forms"; não lidas).

## Lacunas

Signal Forms, Angular SSR e `@defer`; Composition API do Vue em profundidade; form actions e SSR do SvelteKit; TypeScript em Vue e Svelte; bibliotecas de estado de cliente (Pinia, Zustand, Redux, SWR) foram excluídas da pesquisa: siga a que o projeto já usa. Frameworks fora deste eixo (Solid, Qwik, Astro, HTMX) não têm fonte validada. Trate tudo isso como Não verificado e peça a documentação ao usuário.
