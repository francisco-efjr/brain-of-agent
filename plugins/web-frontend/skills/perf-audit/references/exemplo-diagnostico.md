# Exemplo de diagnóstico: LCP de 4,8 s com imagem em lazy-load

Cenário nosso, usado para calibrar a skill. Base: V-15 (limiares e subpartes), V-18 (checklist), V-57 (medição), V-61 (agente de performance). Números abaixo são do cenário, não de projeto real. Os ganhos esperados são qualitativos de propósito.

## Entrada

Trecho de um relatório do Lighthouse (mobile, 3 execuções, mediana):

```text
LCP 4,8 s · elemento: <img src="/hero.jpg" loading="lazy">
TTFB 0,9 s · atraso de renderização 1,9 s · CLS 0,03 · INP não medido
```

Queixa: "a página de produto demora a mostrar a foto principal".

## Raciocínio

1. Limiar (p75): LCP acima de 4 s é "ruim" (V-15). O valor de laboratório 4,8 s está na faixa ruim; o p75 de campo não foi fornecido (Não verificado).
2. Subpartes: 4,8 s - 0,9 s (TTFB) - 1,9 s (atraso de renderização) = 2,0 s para atraso de carregamento mais duração do carregamento. A divisão entre os dois não consta do trecho.
3. Contra o orçamento de referência (atraso de renderização abaixo de cerca de 10%): 1,9 s é cerca de 40% de 4,8 s. É a subparte que mais destoa. Causa a investigar: renderização do elemento depende de JavaScript (hidratação), CSS ou fonte bloqueantes, ou a imagem só é pintada depois de um passo do cliente.
4. `loading="lazy"` no elemento LCP: o navegador adia a requisição até saber que a imagem está perto da viewport, o que aumenta o atraso de carregamento. A regra é não aplicar lazy-load à imagem do LCP (V-15). Isso explica parte dos 2,0 s, não os 1,9 s de renderização.
5. TTFB de 0,9 s representa cerca de 19% do LCP, abaixo da referência de cerca de 40% para essa subparte: não é o gargalo principal, mas 0,9 s merece atenção em separado (servidor, cache, redirecionamentos).
6. CLS 0,03 está bom (abaixo de 0,1). INP não medido: exige dado de campo ou interação real.

## Correções por prioridade

| # | Problema | Onde olhar | Por que ajuda | Como validar |
| --- | --- | --- | --- | --- |
| 1 | `loading="lazy"` no elemento LCP | `Grep "hero"`, `components/Hero.tsx` (atributo da `<img>`) | Remove o adiamento da requisição da imagem principal | Remedir; subparte "atraso de carregamento" deve cair |
| 2 | Imagem possivelmente não descobrível cedo | Ver se `src` está no HTML do servidor ou só aparece após JS | Descoberta precoce permite iniciar o download mais cedo | Ver o HTML inicial (`view-source`) e o trace |
| 3 | `fetchpriority="high"` ausente na imagem LCP | Atributo da `<img>` (apenas nesta imagem) | Aumenta a prioridade de rede da imagem principal; usar em no máximo uma ou duas | Remedir; checar que outras imagens não receberam o atributo |
| 4 | Atraso de renderização de 1,9 s | Pedir trace de desempenho; investigar CSS e fontes bloqueantes e hidratação | É a subparte mais acima do orçamento | Trace antes e depois; ver o que acontece entre o fim do download e a pintura |
| 5 | TTFB de 0,9 s | Cabeçalhos de cache, tempo do servidor, redirecionamentos (no máximo um) | Reduz a primeira parcela do LCP | Medir TTFB antes e depois |

Itens 1 a 3 são verificáveis por leitura de código; 4 e 5 precisam de trace e de medição de servidor (Inferido até lá). Se o projeto usa `next/image`: no Next 16 ou superior, `priority` está descontinuada em favor de `preload`, e a documentação da versão 16.4.0 recomenda, na maioria dos casos, `loading="eager"` ou `fetchPriority="high"` no elemento LCP; em Next 15 ou anterior, a prop é `priority` (Verificado em https://nextjs.org/docs/app/api-reference/components/image, 2026-10-10). Confira a versão no `package.json` antes de recomendar.

## O que não fazer

- Prometer "ganho de 1,5 s": sem remedição o número é invenção.
- Reescrever o componente de página ou trocar de framework por causa de uma imagem.
- Aplicar `fetchpriority="high"` a todas as imagens do carrossel.
- Concluir que o problema é só a imagem: sobram 1,9 s de atraso de renderização sem explicação.

## Registro antes e depois (T-11)

| Métrica | Bom | Ruim | Antes | Depois | Condições | Origem |
| --- | --- | --- | --- | --- | --- | --- |
| LCP | 2,5 s | 4 s | 4,8 s | a medir | Lighthouse mobile padrão, 3 execuções, mediana, build de produção local | Laboratório |
| TTFB (subparte) | cerca de 40% do LCP | n/a | 0,9 s | a medir | idem | Laboratório |
| Atraso de renderização | abaixo de 10% | n/a | 1,9 s | a medir | idem | Laboratório |
| CLS | 0,1 | 0,25 | 0,03 | n/a | idem | Laboratório |

Depois da correção, repita o mesmo comando, na mesma máquina e rede, e preencha a coluna "Depois" com a mediana. Se o dado de campo (p75) existir, registre-o em linha separada com a data da coleta.
