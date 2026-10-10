---
name: fronteira-implementar-react
description: Caso de fronteira que mede se um pedido de implementar um componente de interface em React com TypeScript e Tailwind é atendido com código direto, sem acionar design-brief nem ui-audit e sem exigir plano de design ou aprovação, já que implementação em código é do plugin de frontend e não do plugin de UX.
tags: [ux-ui-design, negative, boundary, frontend]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 450
runs: 3
expected_outcome: "Entrega o componente ProductCard em TypeScript com Tailwind, props tipadas, preço em centavos formatado em reais, estados carregando e esgotado e exemplo de uso, de forma direta; não aciona design-brief nem ui-audit e não impõe plano de design nem gate de aprovação."
model: sonnet
---
Implementa em React 18 com TypeScript e Tailwind o componente `ProductCard` do nosso catálogo. Estou com Vite. Props: `name` (string), `priceCents` (number, em centavos), `imageUrl` (string), `soldOut` (boolean), `loading` (boolean) e `onAdd` (função chamada ao clicar). Mostra imagem, nome, preço formatado em reais e o botão "Adicionar ao carrinho". Quando `loading` é verdadeiro, mostra um esqueleto no lugar do conteúdo; quando `soldOut` é verdadeiro, o botão fica indisponível e diz "Esgotado". Quero só o código do componente e um exemplo de uso, nada de explicação longa.
