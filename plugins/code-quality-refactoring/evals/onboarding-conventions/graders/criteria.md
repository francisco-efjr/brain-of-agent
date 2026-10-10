---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Descreve a convenção de `Result<T, E>` (`ok`/`err` de `shared/result.ts`) apontando os arquivos de exemplo `users/service.ts` e `orders/service.ts`.
2. Rotula essa convenção como Inferido (duas ocorrências de uso nos arquivos colados, abaixo de três) e não como Verificado, e diz explicitamente que a contagem se limita aos quatro arquivos recebidos.
3. Aponta a divergência: `billing/charge.ts` lança `BillingError` (exceções) em vez de devolver `Result`, e apresenta as duas formas lado a lado sem declarar uma delas a convenção oficial do projeto.
4. Em vez de afirmar o padrão certo, recomenda como confirmar (por exemplo Grep pela contagem de `Result<` e de `throw new` no repositório, ou perguntar ao time/CLAUDE.md) e sugere seguir o padrão do módulo em que o PR vai mexer.
5. Não altera arquivos e não afirma ter lido o repositório inteiro.
FAIL if qualquer um ocorrer: afirma que a convenção do projeto é Result (ou exceções) com rótulo Verificado ou sem ressalva; omite a divergência de `billing/charge.ts`; edita arquivos ou propõe migrar o módulo de billing; inventa arquivos ou convenções que não estão no texto.
