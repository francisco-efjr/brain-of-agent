# Notas e incertezas

- Resposta escrita só com conhecimento próprio, sem Skill e sem ler skills/ ou evals/, conforme pedido. Nenhuma requisição de rede.
- Contas verificadas com script local (Python, busca gulosa com restrições): 432 brutas, 336 só com a regra SSO=>Enterprise, 294 com Safari restrito a macOS/iOS. 111 pares válidos; 16 linhas cobrem os 111 (verificado no script).
- O 16 não é provadamente o mínimo. O limite inferior é 14 (pares válidos navegador x SO). O PICT real pode devolver 16 a 18; não instalei nem rodei o PICT, então a sintaxe do modelo (IF/THEN, IN {...}) está escrita de memória e não foi testada.
- Premissa assumida: Safari só em macOS/iOS (Safari para Windows foi descontinuado em 2012; não existe no Android). Edge, Chrome e Firefox existem nos 4 SOs. Se o app for distribuído de forma incomum, isso muda.
- Afirmação de que "a maioria das falhas é disparada por 1 ou 2 fatores" (estudos do NIST/Kuhn) vem de memória, sem fonte checada agora. Escrevi de forma qualitativa, sem percentuais.
- Afirmação de que Chrome e Firefox no iOS usam WebKit é a regra geral da Apple; há exceções regionais (UE) que não detalhei.
- As "triplas de risco" (Edge+Windows+SSO, Safari+macOS+SSO, Chrome+iOS+Google) são heurística minha sobre onde login quebra entre navegadores (redirects, pop-ups, cookies de terceiros, ITP do Safari). Dependem de como o login do app é implementado; o usuário pode ter outros pontos de maior risco.
- Não sei o tráfego real, as funcionalidades nem a arquitetura do app; por isso a recomendação de usar o analytics para fixar combinações e a oferta de refinar a lista depois.
- Não considerei versões de navegador, tablets, modo escuro, acessibilidade, rede lenta; mencionei só de passagem no item de limites.
- Escolhi tom de conversa e uma tabela de 16 linhas no corpo da resposta, o que a deixa longa; pode ser enxugada se o ambiente de chat preferir respostas curtas.
