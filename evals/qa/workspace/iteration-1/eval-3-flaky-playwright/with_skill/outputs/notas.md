# Notas (eval-3-flaky-playwright, with_skill)

## Arquivos da skill lidos
- skills/qa/SKILL.md (inteiro)
- skills/qa/references/automacao-web.md (inteiro; seção "Teste intermitente" e "Revisão de PR de testes E2E" foram a base)
- skills/qa/references/dados-ambientes-ci.md (inteiro; diagnóstico/quarentena, isolamento, manifesto de ambiente)
- skills/qa/scripts/repetir_teste.py (lido; rodei só `--self-test`, que passou, fora do projeto)
- Consulta pontual por grep em skills/qa/references/dominios.md (e-commerce/pagamentos: aprovação assíncrona, estados do pedido) e listagem de assets/templates (não usei nenhum template; o pedido não pedia documento).

Não li evals/ além de flaky.spec.ts.

## Arquivos gerados
- resposta.md (resposta final ao usuário)
- flaky.spec.corrigido.ts (jornada fundida, esperas por condição; só checagem de sintaxe com `node --check`)
- playwright.config.trecho.ts (trecho de config; só checagem de sintaxe)

## Incertezas
- Nada foi executado contra a loja: URL fictícia, sem rede, Playwright e tsc não instalados. O diagnóstico é inferido do código; deixei isso explícito na resposta e dei o comando para confirmar.
- Não conheço o DOM nem a API: nomes de botão/link, `data-testid="item-carrinho"`, rota do carrinho (`/api/carrinho`), formato do número do pedido, elemento de "logado" estão marcados como AJUSTE no código.
- A ordem de probabilidade dos suspeitos é julgamento meu (conta compartilhada e espera fixa como mais compatíveis com "3 em 10 só no CI"); sem a mensagem do primeiro erro no CI e sem o playwright.config.ts não dá para cravar.
- Fundir os dois testes em um é uma decisão de design (jornada sequencial, conforme dados-ambientes-ci.md); a alternativa (pedido criado por API em fixture) depende de endpoint que não conheço.
- A frase "30 verdes ainda compatíveis com taxa de até uns 10%" vem da referência automacao-web.md (aproximação pela regra do três: 3/30); citei como aproximação.
- Comportamento de `toPass` com `expect` aninhado (timeout do expect interno) e `test.slow()` baseado no que conheço do Playwright, sem checar a versão do usuário; a referência da skill cita Playwright 1.63.
- Não incluí asserção de total do pedido por não conhecer o preço do produto 123; apontei como lacuna.
