---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Identifica que o layout raiz inteiro está marcado como client sem motivo (a interatividade é só a saudação ou nenhuma) e que isso leva o layout e seus imports ao bundle do cliente; propõe manter o layout como Server Component e, se houver interatividade, mover só uma folha para Client Component.
2. Identifica a busca de `/api/me` em `useEffect` no cliente como problema (requisição só depois da hidratação, "Entrar" piscando para quem está logado) e propõe buscar no servidor (Server Component ou leitura de sessão), sem inventar uma API específica de autenticação.
3. No `Cart`, identifica `visiveis` e `total` como estado derivado de `items` e `busca`, sincronizado por Effects que só chamam `setState`, e propõe calcular durante o render; cita ao menos duas das três perguntas ("existe sistema externo?", "é consequência de uma ação do usuário?", "pode ser calculado no render?") ou o equivalente.
4. Não adiciona `useMemo`, `useCallback` ou `memo` por reflexo: se mencionar memoização, condiciona à medição ou ao projeto não usar React Compiler.
5. Trata versão e configuração como premissa: pergunta ou rotula como Suposição a versão do Next, do React e se existe `cacheComponents`, e não mistura regras dos dois modelos de cache.
6. Entrega achados com localização (arquivo e linha ou trecho), correção mínima por achado e uma nota do que está bom ou fora do escopo; não reescreve o projeto e não afirma ter rodado build, testes ou o app.
FAIL if qualquer um ocorrer: mantém os dois Effects do carrinho; adiciona `useMemo`/`useCallback` sem condição; recomenda `'use client'` em mais arquivos; mistura `revalidate` clássico com `use cache` na mesma recomendação; afirma ter executado `next build`, `tsc` ou os testes; reescreve a aplicação toda.
