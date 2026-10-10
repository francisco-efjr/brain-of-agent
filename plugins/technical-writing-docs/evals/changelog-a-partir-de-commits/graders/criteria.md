---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final (ou no conteúdo de uma chamada Edit ou Write):
1. As entradas estão no formato Keep a Changelog, sob `## [Unreleased]` ou numa seção nova com data ISO (por exemplo `## [2.0.0] - 2026-10-12`), classificadas em Added (exportar CSV na página de relatórios; filtro por status na busca), Removed (endpoint `/v1/orders`) e Fixed (falha por data de nascimento ausente; expiração do refresh token errada em uma hora).
2. Cada entrada é reescrita em voz ativa e diz o que muda para quem usa (por exemplo, quem integra deve migrar de `/v1/orders` para `/v2/orders`), não copia a mensagem do commit.
3. A remoção de `/v1/orders` está marcada como quebra de compatibilidade (por exemplo "BREAKING" ou "quebra de compatibilidade") e inclui a alternativa `/v2/orders`.
4. Os commits `chore: bump deps`, `ci: cache node_modules` e `docs: fix typo in README` ficam fora das entradas, com o motivo registrado; nenhuma entrada inventada além dos 5 commits de impacto para o usuário.
5. Recomenda a versão 2.0.0 (quebra implica MAJOR) como proposta e pede confirmação; diz que não alterou `VERSION`, não criou tag e não publicou, e que o corte da versão e a tag são decisão do usuário.
6. Inclui tabela ou lista de rastreio ligando cada entrada ao commit de origem (hash).
7. Não reescreve nem apaga a seção `## [1.4.2]` existente.
FAIL if qualquer um ocorrer: cola o `git log` sem reescrever; sobe `VERSION`, cria tag ou afirma ter feito isso; não marca a quebra; inclui chore, ci ou docs triviais como mudanças para o usuário; reescreve entradas antigas; usa data fora do formato ISO; inventa links de PR ou issues.
