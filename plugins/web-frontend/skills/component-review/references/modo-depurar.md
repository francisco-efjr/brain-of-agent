# Modo depurar: bugs de renderização, hidratação e estado

Procedimento de reproduzir, isolar, testar uma hipótese por vez, corrigir o mínimo e travar com teste. Base: V-13 (Effects), V-49 e V-52 (SSR, payload, poluição entre requisições), V-51 (valores não determinísticos em Cache Components), V-26 e V-27 (derivação em Angular e Svelte); padrão de depuração PAD-06 do projeto. A lista de causas de hidratação é Inferida: não há página primária de hidratação lida (lacuna aberta da síntese); confirme na documentação do framework e da versão instalada.

## Protocolo

1. **Reproduzir.** Passos exatos, URL, dados, navegador. Sem reprodução, peça logs e passos; não "conserte" por palpite.
2. **Ler a mensagem inteira.** Em React, o erro de hidratação costuma trazer o trecho que divergiu entre servidor e cliente; copie-o no relatório.
3. **Hipóteses ordenadas** pela tabela abaixo. Uma por vez, cada uma com um experimento barato e um resultado esperado antes de rodar.
4. **Correção mínima** que ataca a causa, mais **teste de regressão que falhava antes** da correção (vermelho-verde). Aplique só se o usuário pediu para corrigir; senão entregue o diff proposto.
5. **Parar** após duas correções que falham ou três hipóteses descartadas: reporte o que foi testado, o que foi descartado e proponha novo plano (reproduzir em componente isolado, bisect do commit, instrumentar com logs).

## Tabela de hipóteses

| Sintoma | Hipóteses (mais provável primeiro) | Experimento de um passo | Correção típica |
| --- | --- | --- | --- |
| "Hydration failed" ou "text content does not match" | 1) valor que muda entre servidor e cliente no render: `Date.now()`, `new Date()`, `Math.random()`, `toLocaleString()` com locale ou fuso diferentes; 2) leitura de `window`, `localStorage`, `navigator` no render inicial; 3) HTML aninhado inválido (`<div>` dentro de `<p>`, `<a>` dentro de `<a>`); 4) extensão do navegador alterando o DOM | Janela anônima sem extensões; registrar o valor suspeito no servidor e no cliente; inspecionar o HTML do servidor com `view-source` | 1) valor vindo do servidor e passado por props; 2) ler dado de navegador depois da montagem ou com `useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot)`; 3) corrigir o aninhamento; 4) nenhuma (não é bug do app) |
| Erro com `Date.now()` ou `Math.random()` em Next com `cacheComponents` | Valor não determinístico fora de `'use cache'` ou de `connection()` (V-51) | Ler a mensagem do build e o `next.config.*` | Mover para `'use cache'` ou chamar `connection()` dentro de `<Suspense>` |
| O estado não atualiza após `setState` | 1) mutação direta de array ou objeto; 2) closure obsoleta em handler, timer ou Effect; 3) `key` instável que remonta o componente e zera o estado; 4) componente definido dentro de outro componente (remonta a cada render) | `console.log` do valor e da identidade do objeto antes e depois; React DevTools: o componente remontou? | 1) criar novo objeto; 2) atualização funcional `setX((prev) => ...)` ou dependências corretas; 3) `key` estável (id, não índice de lista mutável); 4) mover a definição para fora |
| Loop infinito de render | 1) `setState` no corpo do render; 2) Effect que atualiza uma dependência dele mesmo; 3) objeto ou função recriada a cada render usada como dependência | Remover o Effect e ver se para; `console.count` no corpo | Derivar no render, mover para handler, estabilizar a dependência |
| Dado antigo aparece depois de trocar filtro ou busca | Respostas fora de ordem: a consulta A chega depois da B | Limitar a rede nas DevTools e logar a ordem de chegada | Associar resultado à identidade da consulta, `ignore` no cleanup, cancelamento com `AbortController` (o servidor ainda pode ter executado) ou biblioteca com `queryKey` completa |
| Render em excesso | Estado alto demais; contexto largo; props novas a cada render | React DevTools Profiler, opção de registrar por que cada componente renderizou | Descer o estado, dividir o contexto; memoização só com medição |
| Vue/Nuxt SSR: dado de um usuário aparece para outro | Estado singleton de módulo reaproveitado entre requisições (V-52) | Duas requisições seguidas com usuários diferentes | App, router e store criados por requisição |
| Vue/Nuxt: dado buscado duas vezes | `$fetch` solto no `setup` (V-49) | Aba de rede: duas requisições iguais na carga | `useFetch` ou `useAsyncData` com `key` explícita |
| Angular: valor "atrasado" | `effect` propagando estado entre sinais (V-26) | Ler o `effect` | `computed` ou `linkedSignal`; ler sinais antes de `await` |
| Svelte 5: valor desatualizado | `$effect` atualizando estado (V-27) | Ler o `$effect` | `$derived` |

## Exemplo: hidratação por data local

Sintoma: aviso de hidratação em `/pedidos`, o texto "10/10/2026, 21:30" no servidor e "10/10/2026, 18:30" no cliente.

1. Hipótese 1 (valor dependente de fuso): o servidor roda em UTC e o navegador em UTC-3. Experimento: registrar `new Date(pedido.criadoEm).toLocaleString()` nos dois lados. Resultado esperado se a hipótese for verdadeira: horas diferentes. Confirmado.
2. Correção mínima: formatar com fuso explícito e igual nos dois lados.

```tsx
// Ruim: depende do fuso e do locale do ambiente de execução.
<time>{new Date(pedido.criadoEm).toLocaleString()}</time>

// Bom: mesmo resultado em servidor e cliente.
<time dateTime={pedido.criadoEm}>
  {new Intl.DateTimeFormat('pt-BR', { dateStyle: 'short', timeStyle: 'short', timeZone: 'America/Sao_Paulo' })
    .format(new Date(pedido.criadoEm))}
</time>
```

3. Teste de regressão: teste de unidade do formatador com `criadoEm` fixo e fuso explícito; e, no e2e, falhar o teste se o console tiver erro de hidratação (`page.on('console', ...)` e `expect(erros).toEqual([])`).

Se o produto precisa do fuso do usuário, formate depois da montagem (o Effect aqui sincroniza com um sistema externo, o relógio e o fuso do navegador) e aceite o salto de conteúdo, ou envie o fuso em cookie para o servidor.

## Quando o bug não é do componente

- Cache do framework servindo dado velho: leia `next.config.*` e siga um só modelo (V-51); detalhe em `forms-and-data`.
- Resposta da API errada: reproduza com a chamada direta e entregue um pedido de integração ao backend.
- Estilo "quebrado" só em produção: confira ordem de CSS e purga do Tailwind (classes montadas dinamicamente por concatenação não são detectadas; use nomes completos).
