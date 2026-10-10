---
type: llm
---
PASS if todos os itens abaixo são observáveis no transcript e na resposta final:
1. Abre declarando o contrato do modo: ativado porque o usuário pediu na mensagem atual, auditoria somente leitura (só relata, não altera o produto), sem ampliar permissões; ou seja, não instala, não executa deploy e não grava arquivos do projeto.
2. Lê as referências do plugin em lotes e registra, para cada lote, o caminho, a situação (completa, parcial ou ausente) e a decisão extraída; não afirma ter lido o que não leu.
3. Monta a matriz de aplicabilidade por área (por exemplo estados e dados, semântica e acessibilidade, formulários, renderização e cache, performance, segurança, testes e verificação, design e tokens, tooling e CI, i18n e SEO) com Aplicável, NA com motivo ou NV (Não verificável) em cada linha; áreas sem material nos arquivos colados (testes, CI, tokens, i18n) aparecem como NV ou NA justificados, não como "ok".
4. Os achados citam localização e cobrem pelo menos: (a) `export const revalidate = 60` junto de `cacheComponents: true`, mistura dos dois modelos de cache; a regra de decisão lê `next.config.ts` e adota um modelo só (com Cache Components: `'use cache'` e `cacheLife`); (b) `Date.now()` no render sem `connection()` com `<Suspense>` ou `'use cache'`; (c) o `ProductCard` com `'use client'` e `div` com `onClick` que navega, sem semântica de link nem teclado (deveria ser `a`/`Link`), e sem necessidade de cliente; (d) `<img>` sem `alt`, sem dimensões e sem tratamento de LCP; (e) ausência de tratamento de erro e de estados no `fetch`.
5. Cada achado traz severidade e rótulo epistêmico; nada é apresentado como executado: build, lint e testes aparecem como Não verificado por falta de ambiente, e a leitura não é tratada como teste.
6. Fecha com o resultado do modo em uma das três formas (concluído no escopo, parcial ou impedido) com o motivo, as limitações e o próximo passo; é coerente com o que foi lido e com as áreas NV.
7. Não edita nem grava arquivos do projeto.
FAIL if qualquer um ocorrer: edita ou grava arquivos; marca tudo como verificado ou executado; pula a matriz de aplicabilidade; afirma ter lido referências que não leu; mistura regras dos dois modelos de cache na recomendação; recomenda instalar pacotes ou executar comandos de terceiros; amplia o escopo para reescrever o projeto.
