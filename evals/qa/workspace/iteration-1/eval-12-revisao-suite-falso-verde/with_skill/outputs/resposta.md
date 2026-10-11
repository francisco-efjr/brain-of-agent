Revisei o `test_pedidos.py`. O "tudo verde" tem explicação: dos 6 testes, só 1 consegue falhar por erro de regra de negócio, e ele cobre um único exemplo (R$ 100,00 com cupom DEZ). Os outros ou não conseguem falhar, ou só detectam "a API caiu".

**Premissas:** pytest, `loja.pedidos` é código Python da própria loja, a API é REST em homologação e os preços são `float` (o arquivo usa `100.0`, `10.1`). Se algo disso estiver errado, me avise, porque muda parte dos achados.

**O que verifiquei e o que não verifiquei:** não consegui rodar a suíte contra o sistema (não existe o pacote `loja` aqui, e não há rede). O que fiz foi carregar as funções de teste reais do seu arquivo, sem alterá-lo, contra implementações substitutas minhas de `calcular_total` e `criar_pedido`, uma correta e várias com um defeito plantado. Isso prova o que os testes detectam, não que a loja tem esses defeitos. Os achados marcados "(verificado)" saíram dessa execução. Os "(inferido)" vêm da leitura do código.

## Achados, do mais grave ao menos grave

### 1. Falsos verdes: testes que passam com o código quebrado

**1.1 `test_pedido_sem_estoque` (linhas 32-37) nunca falha.** O `assert False` está dentro do `try`, e `AssertionError` é um `Exception`, então o `except Exception: pass` engole a própria falha do teste. (verificado) Passou com `criar_pedido` vendendo SKU sem estoque, e passou com `criar_pedido` quebrado por um `TypeError`. Estoque é dinheiro e cliente furioso: esta é a regra que mais deveria estar protegida.

```python
with pytest.raises(EstoqueInsuficiente):   # a exceção real do domínio
    criar_pedido([{"sku": "SEM-ESTOQUE", "qtd": 1}])
# e depois: nenhum pedido criado, estoque inalterado
```

**1.2 `test_cancelar_pedido` (40-43) não tem asserção, só `print`.** (verificado) Passou com a API devolvendo 500 e com `pedido_id` igual a `None` (a chamada foi para `/pedidos/None/cancelar`). Só falharia se a resposta não fosse JSON ou a conexão caísse. Correção: afirmar o 200, depois consultar o pedido e conferir o estado `CANCELADO`, e provar que um segundo cancelamento é recusado.

**1.3 `test_total_varios_itens` (46-48) compara a função com ela mesma.** O esperado é o próprio `calcular_total(...)`, então passa com qualquer implementação determinística. (verificado) Passou com soma que perde o último item e com total sem arredondar. Além disso, há um risco real escondido: `10.1*3 + 0.2` em float dá `30.499999999999996`, não `30.50`. Se esse valor chega ao pagamento, é centavo perdido ou cobrança estranha. Correção: o esperado vem de uma conta feita à mão, fora do código.

```python
# 10,10 x 3 = 30,30; + 0,20 = 30,50
assert total == pytest.approx(30.50, abs=0.005)
assert round(total, 2) == total   # no máximo 2 casas (premissa a confirmar)
```

Em médio prazo, dinheiro em `Decimal` ou centavos inteiros resolve a causa e não só o sintoma.

**1.4 `test_criar_pedido` e `test_consultar_pedido` só olham o status.** O de criação confere 200 e que existe um `id`. O de consulta confere só 200. Nenhum verifica itens, quantidade, total ou estado, e nada garante que a consulta devolve o pedido que foi criado. Um 200 com itens errados passa. Correção: ler de volta e comparar itens e quantidade enviados; se o preço de "ABC" for conhecido, conferir também o total.

**1.5 `test_total_com_desconto` (27-29) faz patch na própria função testada.** É um anti-padrão, mas aqui o efeito é curioso: o `patch` altera `loja.pedidos.calcular_total`, e o teste chama o nome já importado na linha 6, então o patch não tem efeito e o teste acaba rodando a função real. (verificado) Ele de fato falha com cupom ignorado e com desconto de 20%. Mesmo assim: o patch é código morto que dá falsa sensação de isolamento, e se alguém refatorar para chamar `loja.pedidos.calcular_total(...)` o teste vira tautologia (verificado na variante). Remova o patch. E um único exemplo com um item não pega soma errada com vários itens nem arredondamento.

### 2. Intermitência e dependência de ordem

- **`pedido_id` é global** (linha 10): `consultar` e `cancelar` só funcionam se `criar` rodou antes e passou. Com `pytest -k`, `--lf` (rerodar só os que falharam), `-n` (paralelo) ou ordem aleatória, o ID vira `None`. (inferido pelo código; a URL com `None` foi verificada no item 1.2.) Correção: cada teste cria o seu pedido por uma fixture.
- **`time.sleep(5)` (linha 22):** espera fixa. Se a propagação demora 6 s, falha às vezes; se demora 0,3 s, desperdiça 4,7 s por execução. O sleep sugere consistência eventual, então a espera deve ser por condição, com prazo e mensagem de diagnóstico (a função `esperar_ate` está no `test_pedidos_api.py`).
- **`requests` sem `timeout`:** uma API travada trava a suíte e o CI inteiro.
- **Homologação compartilhada, sem limpeza:** cada rodada cria pedidos reais e a única "limpeza" é o cancelamento que nem é verificado. A fixture nova cancela só o que o próprio teste criou.
- `BASE` fixa no código: URL e credenciais devem vir do ambiente.

### 3. Token de admin no código (linha 9)

Não repito o valor aqui. Ele decodifica para `sub: qa-admin`.
- **Credencial no repositório:** se for válida, trate como vazada e rotacione; apagar o commit não revoga nada.
- **Expira:** um dia a suíte inteira vira 401 sem ninguém ter mexido no produto.
- **Cega o teste mais importante:** todos os testes rodam como admin, então a suíte nunca prova que o cliente A não enxerga nem cancela o pedido do cliente B. Falha de autorização é bug típico de produção e esta suíte não tem como pegá-la.

### 4. Lacunas: o que a suíte não cobre (e provavelmente é por onde o bug escapa)

| Risco | O que falta | Prioridade |
| --- | --- | --- |
| Autorização | cliente comum (não admin), pedido de outro cliente (esperado 404 ou 403, igual ao de pedido inexistente), sem token, token expirado | Alta |
| Dinheiro | cupom inválido/expirado, desconto maior que o total, arredondamento em centavos, quantidade 0 ou negativa, carrinho vazio | Alta |
| Estoque | sem estoque sem efeito colateral, último item com dois compradores ao mesmo tempo, estoque devolvido após cancelamento | Alta |
| Ciclo de vida | cancelar duas vezes, cancelar pedido já enviado ou entregue | Média |
| Duplicidade | duplo clique ou retry criando dois pedidos (idempotência) | Média |
| Erros | SKU inexistente, JSON malformado, falha de dependência (5xx) | Média |

Incluí no código novo: autorização entre dois clientes, sem token, quantidade inválida, cancelamento com transição de estado, cupom com vários itens e arredondamento. **Não incluí:** concorrência no último item, idempotência, estoque após cancelamento e falha de dependência. Esses riscos continuam sem proteção até alguém definir o contrato (veja as perguntas abaixo).

## O que entreguei

Pasta: `/Users/francisco.junior/novo projeto/brain-of-agent/evals/qa/workspace/iteration-1/eval-12-revisao-suite-falso-verde/with_skill/outputs/`

- `test_pedidos_regras.py`: regras de total, cupom, quantidade e estoque. Sem rede, sem ordem, esperado calculado à mão.
- `test_pedidos_api.py`: API com fixture que cria e limpa o pedido, espera por condição, `timeout`, e dois clientes comuns (A e B), tokens vindos de `API_TOKEN_A` e `API_TOKEN_B`.
- `demonstracao_falso_verde.py` e `saida_demonstracao.txt`: a execução descrita acima (só biblioteca padrão; roda com `python3 demonstracao_falso_verde.py`).

**Nível de verificação do código novo:** compila (`py_compile`), e a parte de regras foi executada contra os mesmos defeitos plantados usando um substituto mínimo do pytest, porque o pytest não está instalado aqui. Resultado, com 7 defeitos plantados: os 3 testes de lógica do arquivo original detectam só 2 (cupom ignorado e desconto de 20%) e deixam passar os outros 5 (soma que perde um item, total sem arredondar, quantidade negativa aceita, venda sem estoque, `criar_pedido` quebrado por `TypeError`). O arquivo novo detecta 6 dos 7 como entregue e os 7 depois do ajuste da exceção (ver abaixo). **O `test_pedidos_api.py` não foi executado**: depende do seu ambiente.

**Ajustes obrigatórios (marcados com `AJUSTE` no código):** a exceção real de "sem estoque" e de quantidade inválida (com `Exception` genérica o teste ainda falha se nada for lançado, mas aceita qualquer erro, como o `TypeError`); nomes de campo e de estado; 200 ou 201 na criação; 404 ou 403 para pedido alheio; 409 no segundo cancelamento. São palpites meus; confirme no contrato antes de confiar no verde.

## Como evitar que isso volte

1. Antes de merge, faça o "teste do teste": introduza de propósito um defeito por regra (cupom ignorado, `>` trocado por `>=`, estoque não decrementado) e confirme que algum teste fica vermelho. É o que o script de demonstração faz; com o `mutmut` isso fica automático. Eu não rodei o `mutmut` aqui.
2. Um linter pega parte disso: as regras `PT015` (assert False) e `S110` (try/except/pass) do ruff cobrem os casos do item 1.1, mas confirme os códigos na versão que vocês usam.
3. Cobertura de linha não ajuda aqui: o `test_pedido_sem_estoque` executa as linhas de `criar_pedido` e conta como cobertura sem verificar nada.

## Perguntas que mudariam a resposta

1. Quais 3 a 5 bugs escaparam recentemente para produção? Com eles eu mapeio, um a um, "qual teste deveria ter pego", e priorizo o que falta com dado em vez de suposição. É a melhor entrada que vocês podem me dar.
2. O token `qa-admin` é válido e está em outros repositórios ou no CI? Se sim, rotacione hoje.
3. Valores monetários: `float` mesmo, ou `Decimal`/centavos em algum ponto? Qual a regra de arredondamento?
4. Qual o contrato de criação (200 ou 201) e de erros (qual status para sem estoque, quantidade inválida, pedido alheio, cancelamento repetido)?
5. Existe ambiente de homologação descartável, ou os pedidos criados ficam acumulando?
