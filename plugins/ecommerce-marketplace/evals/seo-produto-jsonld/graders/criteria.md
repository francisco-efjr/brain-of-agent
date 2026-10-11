---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta que a oferta precisa ser um `Offer` (não `AggregateOffer`) com `price` maior que zero e `priceCurrency` ISO 4217 (BRL); o snippet não tem moeda nem `price`.
2. Diz que `availability` é recomendada, não obrigatória, e aponta o erro do valor fixo `InStock` quando a variante GG está sem estoque: a marcação deve corresponder ao conteúdo visível (preço, moeda e estoque).
3. Identifica o JSON-LD duplicado (o do app e o do tema) e recomenda manter um bloco e complementar o outro apenas com campos ausentes, ou desativar um deles, em vez de somar dois `Product` com ofertas diferentes.
4. Trata variantes: uma oferta por variante ligada ao produto-pai (por exemplo `ProductGroup`/`hasVariant` ou `isVariantOf` e `inProductGroupWithID`), com `sku` por variante; se citar `ProductGroup`, marca a lista de propriedades como Não verificada ou pede conferir na documentação do Google.
5. Menciona identificadores (GTIN, MPN, SKU), política de devolução e frete como campos recomendados, sem tratá-los como obrigatórios.
6. Pede validação no teste de rich results do Google (e/ou Search Console) antes de considerar o resultado válido, e diz que não validou; trabalha em tema de desenvolvimento, sem tocar a loja ao vivo nem publicar tema.
FAIL if qualquer um ocorrer: diz que `availability` é obrigatória; mantém `AggregateOffer` sem `price` e `priceCurrency`; mantém dois blocos `Product` concorrentes; declara o schema "válido" ou "elegível a rich results" sem validação; afirma ter testado no Google; sugere publicar o tema ou alterar a loja ao vivo.
