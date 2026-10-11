# Notas e incertezas

- Não executei nada. O ambiente é fictício (sem rede), `tsc` e `@playwright/test` não estão instalados e a regra era não instalar pacotes. O código de `flaky.fixed.spec.ts` não foi compilado nem rodado; revisei a sintaxe só por leitura.
- Causa raiz não confirmada. Tenho uma lista de hipóteses ordenadas por suspeita, mas sem log, trace ou o `playwright.config.ts` do CI não dá para dizer qual produz os ~30% de falha. Não vi a config: workers, `fullyParallel`, `retries`, shards e timeouts podem mudar o peso de cada hipótese.
- A hipótese 1 (variável de módulo entre testes) sozinha deveria falhar de forma mais determinística em modo paralelo/shard. Os 30% intermitentes combinam melhor com ela amplificada por retries, ou com as causas de timing/dado compartilhado. Afirmei isso como provável, não como certo.
- Afirmei que o Playwright reinicia o worker após falha e que isso zera a variável de módulo. É o comportamento documentado que conheço, mas não verifiquei em uma versão específica.
- Seletores da versão corrigida (`entrar`, `adicionar ao carrinho`, `carrinho`, `finalizar`, radio `cartão`, `.status` dentro da linha, badge do carrinho com "1") são suposições. Pode haver diferenças reais na tela, por exemplo carrinho sem badge, "Finalizar" como link em vez de botão, ou opções de pagamento que não são `radio`.
- Em `toContainText('1')` no carrinho assumi que há um contador. Se a conta já tiver itens residuais, isso falha. Não resolvi a limpeza de carrinho porque não conheço API para isso.
- O `toPass` com `page.goto` dentro assume que o status do histórico é assíncrono. Se não for, a recomendação correta é tirar o `toPass` e tratar como bug do produto. Deixei o aviso na resposta.
- O teste original não preenche dados de cartão. Não sei se há cartão salvo ou fluxo simulado no homolog. Mantive o comportamento original.
- Versão mínima do Playwright citada (>= 1.29 para `toPass`, >= 1.27 para `getByRole`) é de memória.
- Mantive a senha literal no código, igual ao original, para não adicionar falha por variável de ambiente ausente, e sinalizei como ressalva. Não alterei o arquivo original em `evals/qa/files/`.
- Escolhi unir os dois testes em um só por ser a correção mais simples e robusta. Os custos: perde-se a granularidade do relatório e o teste fica mais longo. Alternativas citadas na resposta: criar o pedido por API/fixture, ou `test.describe.configure({ mode: 'serial' })`. Esta última não citei, e ela mantém o acoplamento.
