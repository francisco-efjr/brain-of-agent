# Notas (eval-13, com skill)

## Arquivos da skill lidos
- skills/qa/SKILL.md (inteiro)
- skills/qa/references/unitarios-e-integracao.md (inteiro; guiou: oráculo independente, não chamar a função para montar o esperado, asserção que distingue implementação errada plausível, mutação como verificação, "não diga que passou sem executar")
- skills/qa/references/design-de-testes.md (inteiro; guiou: valor-limite em dinheiro com passo de R$ 0,01, 3 valores nos limites, partição incluindo faixa sem desconto, pergunta ao PO quando arredondamento/regra não está escrita)

Não abri: scripts/valores_limite.py (gerei os limites à mão, a faixa é simples), templates, demais referências.

## Arquivos produzidos (em outputs/)
- resposta.md: texto final ao usuário (inclui o código completo)
- test_desconto.py: testes pytest
- desconto.py: cópia fiel do original (para rodar os testes aqui)
- desconto_corrigido.py + correcao.diff: correção mínima de 2 linhas, usada só para provar que os testes ficam verdes
- notas.md

## Execução
- pytest NÃO está instalado (Python 3.14, nenhum interpretador com pytest). Não instalei nada.
- Executei com um shim mínimo de pytest + runner que escrevi em scratchpad (fora da pasta de saída): suporta parametrize empilhado, ids, pytest.param e raises. Não é o pytest real.
- Original: 48 passam, 5 falham (500,00 não VIP; 500,00 VIP; VIP 50,00; VIP 99,99; varredura). Corrigido: 53/53.
- Mutação manual (13 mutantes sobre a versão corrigida): 13 mortos.

## Defeitos achados na função
1. `subtotal > 500` deveria ser `>= 500` (docstring: "a partir de R$ 500,00").
2. VIP recebe +2 pontos mesmo abaixo de R$ 100 (percentual 0 + 0,02); docstring diz "em qualquer faixa com desconto".

## Incertezas
- Defeito 2 depende da leitura de "faixa com desconto". Li como "faixa < R$ 100 não conta". Sinalizei ao usuário como pergunta ao Produto; os testes afetados estão isolados (test_vip_abaixo_de_100_continua_sem_desconto e a varredura).
- Contagem de 53 casos é a do meu shim; o pytest real deve coletar o mesmo número, mas não verifiquei. Os ids dos params são ASCII de propósito (pytest escapa não-ASCII nos ids).
- Fora do escopo/sem teste: entrada float (TypeError), subtotal com mais de 2 casas (ex.: 499,995 cai em 5% hoje; regra não diz), `cliente_vip` não-bool, mensagem da exceção (a regra só pede ValueError).
- Não testei desempenho da varredura no pytest real (4 mil iterações x 2 chamadas, rodou em fração de segundo no shim).
- Optei por deixar os testes vermelhos contra a função atual (sem xfail), porque a regra escrita é o oráculo e o relato dos defeitos é o resultado útil; se o time preferir mergear antes de corrigir, dá para marcar os 5 casos com xfail(strict=True).
