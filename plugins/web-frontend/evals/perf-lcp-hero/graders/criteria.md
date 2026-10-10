---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta `loading="lazy"` no elemento LCP como erro (imagem acima da dobra não deve ter lazy-load) e que a imagem só existe no DOM depois da hidratação (o componente renderiza um esqueleto até o Effect rodar), portanto não é descobrível no HTML inicial.
2. Decompõe o LCP nas quatro subpartes e compara com o orçamento de referência (TTFB cerca de 40%, atraso de carregamento abaixo de 10%, duração cerca de 40%, atraso de renderização abaixo de 10%): reconhece que o atraso de carregamento (1,3 s, cerca de 27% de 4,8 s) e o atraso de renderização (1,9 s, cerca de 40%) são as subpartes que estouram, e que o TTFB de 0,9 s (cerca de 19%) não é a causa principal; os percentuais, se citados, são aproximadamente corretos.
3. Propõe correções ligadas ao código: renderizar a imagem no HTML inicial (Server Component ou remover o gate de estado), tirar o `loading="lazy"`, usar `fetchpriority="high"` com moderação (uma ou duas imagens) e `preload` só se o recurso não for descoberto no HTML; prioriza por efeito na subparte que doeu.
4. Diz que INP não foi medido e exige dado de campo ou uma interação real (TBT é indício de laboratório, não é INP), e que o resultado é de laboratório, não de campo (percentil 75 de usuários reais).
5. Manda remedir com a mesma ferramenta e as mesmas condições depois da mudança e dá ganho esperado apenas de forma qualitativa, sem números de segundos inventados.
6. Rotula o que é Verificado (lido nos dados e no código colados), Inferido (efeito esperado) e Não verificável; não propõe reescrita ampla nem dependência nova.
FAIL if qualquer um ocorrer: promete que o LCP cairá para um valor específico ou economiza N segundos; recomenda lazy-load ou mais lazy-load na imagem LCP; propõe reescrever a aplicação ou trocar de framework; trata o resultado de laboratório como dado de campo; afirma ter rodado Lighthouse ou aplicado a mudança; ignora a renderização no cliente do hero.
