# Notas (eval-12, revisão de suíte com falso verde)

## Arquivos da skill lidos (em /Users/francisco.junior/novo projeto/brain-of-agent/skills/qa)

- `SKILL.md` (inteiro; seções "Revisão de suíte", "Anti-padrões", "Honestidade e limites" e checklist guiaram a ordem dos achados e a separação verificado/inferido/suposição)
- `references/unitarios-e-integracao.md` (inteiro: dublês, oráculo, "where to patch", revisão de suíte)
- `references/automacao-api.md` (inteiro: status, anti-padrões "dependência de ordem", "token fixo", "oráculo circular", `esperar_ate`, autorização/IDOR)
- `references/dados-ambientes-ci.md` (inteiro: isolamento, limpeza, quarentena, gate)
- `references/dominios.md` e `references/seguranca.md`, `references/design-de-testes.md`: lidos só por trechos via grep/sed (e-commerce, ponto flutuante/arredondamento; tokens/JWT/segredos; partição e valor-limite)
- `scripts/repetir_teste.py`: só o cabeçalho (não usei: não há como repetir a suíte aqui)
- Não abri: templates, `estrategia.md`, `bugs-e-relatorios.md`, `automacao-web.md`, demais scripts.

Não li nada em `evals/` além de `evals/qa/files/test_pedidos.py` (não abri `desconto.py` nem os outros arquivos da pasta `files`).

## O que foi executado

- `demonstracao_falso_verde.py` (stdlib; saída em `saida_demonstracao.txt`): carrega o `test_pedidos.py` original sem alterá-lo (`sys.dont_write_bytecode`, `exec` do código-fonte), injeta stubs de `loja.pedidos`, `requests` e um shim mínimo de `pytest`, e roda as funções de teste reais contra 1 implementação correta + 7 mutantes inventados por mim.
- `py_compile` em `test_pedidos_api.py` e `test_pedidos_regras.py`.
- `test_pedidos_regras.py` rodou contra os mesmos mutantes via shim de pytest (não é o pytest real).
- `test_pedidos_api.py` NÃO foi executado (sem rede, sem API, sem pytest/requests instalados; não instalei pacotes).

## Incertezas

- `loja.pedidos` não existe neste ambiente; assinatura de `calcular_total(itens, cupom=None)` e comportamento de `criar_pedido` são deduzidos do uso no arquivo. As implementações "corretas" e os mutantes são ficção minha.
- Contrato da API desconhecido: usei 200 na criação (como no original), 404 para pedido alheio, 409 para segundo cancelamento, `CANCELADO` como estado, campos `id`, `itens[].sku/qtd`, `status`. Todos marcados `AJUSTE` no código.
- Premissa de que o total sai arredondado em 2 casas (`round(total, 2) == total`) e de que quantidade <= 0 deve ser recusada: não está no arquivo; se o projeto usa Decimal/centavos ou aceita outra regra, esses testes devem ser adaptados. Pode haver falso vermelho se a premissa estiver errada.
- Achado do patch em `test_total_com_desconto`: concluí e verifiquei que o patch não tem efeito porque o teste usa o nome importado na linha 6 (`from loja.pedidos import calcular_total`). Isso vale enquanto `calcular_total` não se chamar recursivamente pelo módulo; não dá para saber pelo arquivo.
- "Só 1 dos 6 testes detecta erro de regra de negócio" é a minha leitura; `test_criar_pedido`/`test_consultar_pedido` ainda detectam API fora do ar ou erro de autenticação.
- Os códigos de regra do ruff (PT015, S110) citados na resposta são de memória; ruff não está instalado aqui e eu disse isso ao usuário ("confirme na versão que vocês usam"). `mutmut` também não está instalado e não foi rodado.
- O token do arquivo decodifica (Base64) para `sub: qa-admin`; não sei se é válido. Não reproduzi o valor na resposta.
- Não sei quais bugs escaparam para produção; a lista de lacunas é por risco típico do domínio de pedidos, não por evidência dos incidentes (por isso a pergunta 1).
