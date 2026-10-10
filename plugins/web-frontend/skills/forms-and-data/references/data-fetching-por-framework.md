# Data fetching, cache e renderização por framework

Base: V-47 (Angular v22), V-48 (TanStack Query), V-49 (Nuxt 4.6.0), V-50 (SvelteKit), V-51 (Next.js 16.4.0), V-52 (Vue SSR e Nuxt 4). Lido em 2026-10-10; o modelo de cache do Next muda rápido, então registre a versão que você leu e confirme a do projeto. Exemplos são redação própria. Lacunas: Signal Forms do Angular, Angular SSR e `@defer`, form actions do SvelteKit, guia de client-side data fetching do Next, mutations e invalidação do TanStack Query: Não verificado; consulte a documentação antes de afirmar.

## Sumário

1. Tabela de decisão
2. Next.js 16.4: dois modelos de cache
3. TanStack Query
4. Nuxt 4
5. SvelteKit
6. Angular v22: reactive forms
7. Matriz de renderização

## 1. Tabela de decisão

| Situação | Escolha |
| --- | --- |
| Next, carga de página, dado do servidor | Server Component com `fetch` ou acesso a dados no servidor; cache conforme o modelo do projeto |
| React puro ou Next com dado interativo do cliente | TanStack Query (ou a biblioteca já usada) em vez de `fetch` dentro de Effect |
| Nuxt, carga de página | `useFetch` |
| Nuxt, lógica própria (CMS, SDK, `Promise.all`) | `useAsyncData` com `key` explícita |
| Nuxt, ação do usuário (submit) | `$fetch` |
| SvelteKit, carga de rota | `load` (`+page.server.js` para segredo e banco) |
| Angular, formulário central | reactive forms |

## 2. Next.js 16.4: dois modelos de cache

Comece sempre lendo `next.config.*`.

```ts
// next.config.ts: com Cache Components
import type { NextConfig } from 'next';
const nextConfig: NextConfig = { cacheComponents: true };
export default nextConfig;
```

Com `cacheComponents: true` (V-51; a documentação 16.4 também trata de `partialPrefetching`, e deixá-lo sem definir gera aviso; confira a página para o local da opção):

```tsx
import { Suspense } from 'react';
import { cacheLife, cacheTag } from 'next/cache';       // confirme os nomes de import na versão instalada

async function listarProdutos() {
  'use cache';                                         // cache no nível de dados
  cacheLife('hours');                                  // sempre par com cacheLife
  cacheTag('produtos');                                // invalidação pontual
  return buscarProdutos();                             // acesso a dados do projeto
}

async function PrecoAtual({ id }: { id: string }) {    // dado por requisição
  const preco = await buscarPrecoAoVivo(id);
  return <span>{preco}</span>;
}

export default async function Page() {
  const produtos = await listarProdutos();
  return (
    <>
      <ProdutoLista itens={produtos} />
      <Suspense fallback={<span>Carregando preço...</span>}>  {/* o fallback entra no shell estático */}
        <PrecoAtual id={produtos[0].id} />
      </Suspense>
    </>
  );
}
```

Regras do modelo: dado por requisição e APIs de runtime vão em `<Suspense>`; `Math.random()`, `Date.now()` e `crypto.randomUUID()` pedem `connection()` (de `next/server`; confirme) dentro de `<Suspense>` ou `'use cache'`; `performance.now()` é exceção (telemetria). Apps novos de `create-next-app` já vêm com Cache Components; os dois serão padrão no próximo major (V-51). Com Cache Components, o ISR segue outro guia: `generateStaticParams` define o que entra no build, URLs fora da lista recebem o App Shell na hora e o resultado completo é guardado.

Sem `cacheComponents` (modelo anterior, "Caching (Previous Model)"):

```tsx
export const revalidate = 3600;               // segundos; prefira intervalo alto (1 hora em vez de 1 segundo)
export async function generateStaticParams() { /* caminhos do build */ }
// após uma escrita, em Server Action ou Route Handler:
//   revalidateTag('produtos')  ou  revalidatePath('/produtos')   (confira a assinatura na versão instalada)
```

Comportamento do modelo anterior: stale-while-revalidate; a regeneração acontece na próxima requisição; falha na revalidação mantém o último dado bom; o cabeçalho `x-nextjs-cache` mostra `HIT`, `STALE`, `MISS` ou `REVALIDATED`. Limites do ISR: só Node.js (não funciona com static export); `revalidate = 0` ou `no-store` tornam a rota dinâmica; com várias instâncias, o cache em arquivo é por instância e a revalidação sob demanda só atinge a instância chamada, então use cache handler compartilhado (pedido de integração para `devops-cloud-infra`); o Proxy não roda em revalidação sob demanda.

Decisão (Inferida das recomendações): conteúdo que muda pouco, tempo de revalidação alto; evento de escrita, `revalidateTag` ou `revalidatePath`; tempo real, renderização dinâmica. Nunca misture regras dos dois modelos no mesmo projeto.

## 3. TanStack Query

```tsx
const { data, error, isPending } = useQuery({
  queryKey: ['pedidos', { status, pagina }],                      // todos os parâmetros que mudam o resultado
  queryFn: ({ signal }) => buscarPedidos({ status, pagina, signal }), // signal permite cancelar a requisição
  staleTime: 60_000,                                              // escolhido de propósito
});

if (isPending) return <Carregando />;
if (error) return <ErroComTentarNovamente erro={error} />;
return <Lista itens={data} />;
```

Defaults (V-48, página "important defaults"): queries nascem stale (`staleTime` 0); `gcTime` de 5 minutos para queries inativas; falhas são repetidas 3 vezes com espera exponencial antes de exibir erro; refetch em foco da janela, reconexão e montagem. `staleTime`: 2 minutos para dado vivo moderado, `Infinity` para invalidar só manualmente, `'static'` para valor que nunca refaz (flag lida no boot). Sem comparação com Zustand, Redux ou SWR: a pesquisa os excluiu por pedido; siga a biblioteca que o projeto já usa.

## 4. Nuxt 4

```vue
<script setup lang="ts">
const route = useRoute();
// carga de página: useFetch repassa o dado do servidor ao cliente no payload (sem buscar duas vezes)
const { data: pedido, status, error } = await useFetch(`/api/pedidos/${route.params.id}`, {
  pick: ['id', 'status', 'total'],   // reduz o payload serializado
});
</script>
```

```ts
// lógica própria: key explícita; Promise.all para independentes
const { data } = await useAsyncData('painel', () =>
  Promise.all([$fetch('/api/resumo'), $fetch('/api/alertas')]),
);

// ação do usuário (submit): $fetch, não useFetch
async function salvar() {
  await $fetch('/api/pedidos', { method: 'POST', body: form });
}
```

Regras (V-49): `$fetch` solto no `setup` pode buscar duas vezes; chaves iguais de `useAsyncData` compartilham `data`, `error` e `status`, e opções como `handler`, `deep`, `transform`, `pick`, `getCachedData` e `default` precisam coincidir (aviso em desenvolvimento); `server: false` deixa `data` indefinido no `setup`: trate `status`; efeito de store (Pinia) dentro de `useAsyncData` usa `callOnce`; `lazy` não bloqueia a navegação. Nuxt 3 tem diferenças: use a documentação da versão do projeto (a lida foi a da série 4.x).

## 5. SvelteKit

```ts
// src/routes/pedidos/+page.server.ts: segredo e banco só no servidor
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, depends }) => {
  depends('app:pedidos');                       // permite invalidate('app:pedidos')
  const [pedidos, resumo] = await Promise.all([ // independentes em paralelo
    fetch('/api/pedidos').then((r) => r.json()),
    fetch('/api/resumo').then((r) => r.json()),
  ]);
  return { pedidos, resumo };
};
```

Regras (V-50): `+page.server.js` roda só no servidor e devolve dado serializável (devalue aceita `Date`, `Map`, `Set`, `BigInt`, `RegExp` e promises para streaming); `+page.js` roda nos dois lados; o `fetch` do `load` herda `cookie` e `authorization` no servidor; evite waterfalls com `await parent()` cedo; nunca `redirect()` ou `error()` dentro de `try`/`catch` (seriam capturados); `setHeaders` não aceita o mesmo cabeçalho duas vezes nem `set-cookie`; em streaming, promise que rejeita antes da renderização e sem tratamento pode derrubar o servidor; `invalidate(url)`, `refreshAll()` e `depends(url)` recarregam; load de servidor não depende automaticamente de URLs buscadas (para não vazar segredo); `PageProps` e `LayoutProps` a partir da 2.16.0 (antes, tipos individuais).

## 6. Angular v22: reactive forms

```ts
import { FormBuilder, Validators } from '@angular/forms';

form = this.fb.nonNullable.group({
  nome: ['', [Validators.required, Validators.minLength(2)]],
  email: ['', [Validators.required, Validators.email]],
});

// setValue exige a estrutura completa e acusa erro de aninhamento; patchValue falha em silêncio nesses erros
this.form.setValue({ nome: 'Ana', email: 'ana@exemplo.com' });
```

Regra de escolha (V-47): formulário central, grande, com reuso de modelo e teste sem DOM, reactive forms; formulário curto e isolado, template-driven; projeto novo na v22, avalie Signal Forms depois de ler o guia (conteúdo não lido: lacuna). Mostre o erro depois de `markAsTouched`. O guia não trata de acessibilidade de erro: use o checklist de formulário da skill. Derivação com `computed` e `effect` só para efeitos externos (V-26).

## 7. Matriz de renderização (V-52)

| Necessidade | Modo |
| --- | --- |
| Conteúdo público com SEO | SSR universal |
| App interno sem SEO | SPA (`ssr: false`) |
| Conteúdo fixo | prerender |
| Mistura por rota | `routeRules` do Nuxt (não funciona com `nuxt generate`) |
| Cache em borda | `swr` ou `isr` conforme a plataforma (Netlify e Vercel, segundo a página); não existe opção `cache` em `routeRules` |

Checklist Vue (V-52): sem `window` fora de `onMounted`; app, router e store por requisição, porque módulos de servidor são inicializados uma vez e estado singleton vaza entre usuários; valor aleatório ou data só no cliente (`v-if` + `onMounted` ou semente); `data-allow-mismatch` a partir do Vue 3.5; Teleport precisa de contêiner dedicado; nunca `v-html` com dado externo. Estado serializado em `<script>` com escape adequado é Inferido (regra de V-22), não está na página.
