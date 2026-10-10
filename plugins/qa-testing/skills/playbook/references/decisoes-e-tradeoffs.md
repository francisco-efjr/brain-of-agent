# Decisões e tradeoffs em QA

Onde as fontes divergem, este arquivo registra a resolução adotada e o porquê, para que você aplique com consciência e saiba quando mudar. Rótulos: Verificado (lido na fonte, ver `fontes.md`), Inferido (síntese), Suposição. Validado em 2026-10-10.

## Sumário

- [Qual camada de teste usar](#qual-camada-de-teste-usar)
- [Comparativo das técnicas e camadas](#comparativo-das-técnicas-e-camadas)
- [Conflitos entre fontes e resolução (K1 a K15)](#conflitos-entre-fontes-e-resolução)
- [Decisões frequentes em uma linha](#decisões-frequentes-em-uma-linha)
- [Temas sem skill própria](#temas-sem-skill-própria)

## Qual camada de teste usar

Regra: **a menor camada que prova a regra**, ajustada por risco e custo. Pergunte em ordem; pare na primeira resposta "sim".

1. É lógica pura (cálculo, validação, regra, máquina de estados)? → **unitário**, com esperado calculado à mão.
2. O risco está em combinar módulos ou em persistência, serialização, transação, fila? → **integração** do serviço com banco real (motor e versão relevantes) e vizinhos simulados; declarar o que continua simulado.
3. O risco é o acordo entre consumidor e provedor (campo removido, tipo trocado, enum novo)? → **contrato** (Pact consumer-driven, ou verificação contra OpenAPI) mais pequena validação no sandbox do parceiro.
4. O domínio de entradas é amplo e a regra é uma propriedade (ordenar preserva elementos, serializar e ler preserva valor)? → **property-based** combinado com exemplos explícitos.
5. O risco só existe na jornada completa de valor (cliente compra e acompanha a entrega)? → **E2E curto**, poucos fluxos, ambiente de teste, terceiros com stub.
6. A dúvida é "a suíte pega defeito?" → **mutation check** manual ou ferramenta, só em módulo de risco alto.

Exemplo: regra "frete grátis a partir de R$ 199,00". O limite e o arredondamento são provados em unitário (R$ 198,99 / 199,00 / 199,01). A integração prova que a rota usa o subtotal **antes** do desconto lendo o valor persistido. Um único E2E prova que o cliente vê o frete zerado no checkout. Vinte variações pela interface seriam custo sem informação nova.

## Comparativo das técnicas e camadas

| Camada ou técnica | Pega tipicamente | Custo e velocidade | Armadilha principal | Fonte |
| --- | --- | --- | --- | --- |
| Unitário | Cálculo, validação, ramos, transições | Baratíssimo, milissegundos | Mockar tudo e não pegar defeito de integração | V-14, V-33 |
| Integração de serviço | Mapeamento, query, serialização, transação, idempotência | Barato a moderado | "Teste com container" descreve infraestrutura, não confiança; SQLite em memória não substitui PostgreSQL/MySQL | brain, V-36 |
| Contrato (Pact) | Quebra consumidor × provedor | Moderado, exige CI e broker | Não substitui E2E de jornada; `can-i-deploy` não foi confirmado na página lida | V-16 |
| E2E | Jornada entre camadas, integração real | Caro, lento, instável | Pipeline de horas e vermelho em que ninguém confia | V-14, V-19 |
| Property-based | Classes de entrada que ninguém listou | Moderado; exige propriedade bem definida | Propriedade vaga ("nunca lança erro") ou geração viesada | V-15 |
| Mutation | Força das asserções | Caro (executa a suíte por mutante) | Mutante equivalente conta como falha; score sem contexto | V-15, V-31 |
| Exploratório | O que ninguém imaginou | Humano, por sessão com tempo fixo | Charter largo demais ("explore o sistema") | brain, V-35 |

## Conflitos entre fontes e resolução

| ID | Conflito | Resolução adotada | Justificativa e rótulo |
| --- | --- | --- | --- |
| K1 | Pirâmide (base unitária) × troféu (ênfase em integração) × favo de mel (integração de serviço) | Escolha a menor camada que prova cada risco; o formato é consequência de onde nascem os defeitos; 60/25/10 é ponto de partida, nunca cota | Fowler/Vocke e Dodds divergem por contexto: backend com regra rica, SPA, microsserviços. Inferido (V-14 recomenda essa resolução) |
| K2 | Uma retentativa automática no CI × "retry detecta, não corrige" | No máximo uma retentativa, tratada como sinal: resultado "flaky" abre ticket com dono e prazo e não esconde a primeira falha | Playwright classifica flaky separado de passed (V-21, classe A); V-37 é classe C cruzada com A. Verificado + Inferido |
| K3 | TDD rígido (apagar código escrito antes do teste) × pragmático | Ciclo padrão com exceções declaradas (protótipo descartável, configuração, código gerado); código escrito antes do teste: perguntar antes de apagar | Apagar é ação destrutiva local; tom calmo. Verificado (V-31, V-33) |
| K4 | Healer automático que ajusta o teste × "editar teste é inaceitável" | Healer só corrige o teste quando a funcionalidade está correta; se parece quebrada, registra falha de produto e não toca a asserção; toda correção passa por revisão de diff | A doc do healer admite entregar "teste pulado" quando julga a funcionalidade quebrada, o que mascara regressão. Inferido (V-20, V-06) |
| K5 | Revisor que sempre acha algo × revisão completa | Revisor reporta só lacunas de correção e requisito, com confiança e "em dúvida, não reporte"; estilo fica de fora | Evita over-engineering. Verificado (V-01) |
| K6 | `data-cy` (Cypress) × role/label (Testing Library, Playwright) | Papel, rótulo e texto primeiro; atributo de teste como último recurso | A doc do Cypress já registra a decisão. Verificado (V-24, V-22, V-19) |
| K7 | Meta de cobertura (~70%) × 100% × score de mutação | Cobertura mede execução, não verificação: não usar como meta; mutação (ou mutation check manual) nos módulos de risco alto, com custo declarado | O defensor do ~70% admite que o número não vem de dados. Verificado (V-14) + brain |
| K8 | Execução autônoma longa (Ralph, harness) × segurança | Só em sandbox, com teto de iterações e revisão humana; o plugin não implementa loop autônomo, documenta o protocolo de feature list | A fonte do Ralph não traz aviso de sandbox; a recomendação vem de V-05 e V-06. Verificado |
| K9 | `/qa` do gstack conserta e comita sozinho × auditoria só relata | Dois modos: relatar (`qa-reporter`, sem Edit/Write) e corrigir (a pedido, escopo autorizado, sem commit/push automáticos, regressão que falha antes); parar e perguntar após 2 reversões | Plugin seguro por padrão. Verificado (V-35) + Inferido |
| K10 | Números de quarentena (14 dias, 5%, 50 execuções) | Publicar como "valores iniciais ajustáveis", nunca como padrão | V-37 é classe C e os números são convenção do autor. Verificado |
| K11 | "Avaliador cético separado" atribuído ao harness da Anthropic | Recomendar revisor separado com base em V-01 (Writer/Reviewer), sem atribuir ao harness | V-06 mostra um único agente verificando o próprio trabalho. Verificado |
| K12 | Testes gerados por LLM são fracos × usar IA para escrever testes | Permitir a geração, com `test-reviewer` em contexto limpo, mutation check e execução real | O relato de que 5 de 18 specs geradas falharam é sinal de classe C, não regra. Verificado (anedótico, V-29) |
| K13 | Colisão do nome `qa` com o namespace | A skill núcleo se chama `playbook`; invocação `/qa-testing:playbook` | Decisão de design. Suposição |
| K14 | `webapp-testing` manda tratar o helper como caixa-preta | O plugin documenta o comando, não embute o helper; ler o código antes de executar; screenshots no diretório de trabalho do projeto | `with_server.py` executa shell arbitrário (V-11). Verificado |
| K15 | "TDD sempre" × "não ampliar a suíte indefinidamente" | Teste novo só se responde às 4 perguntas do cartão de valor; correção localizada recebe um teste de regressão, não uma suíte nova | V-35 + brain. Inferido |

## Decisões frequentes em uma linha

- **Mock ou fake de banco?** Fake em memória serve à regra, mas não reproduz isolamento, collation, constraints nem concorrência: se o risco está na transação, use o banco real.
- **Quando verificar interação (spy/mock)?** Quando a interação é o efeito: notificação ao destinatário certo, nenhuma cobrança após recusa, mesma chave de idempotência em retry.
- **Um assert por teste?** Não é obrigação: retorno, estado e efeito podem exigir várias asserções no mesmo caso. Um comportamento por teste, sim.
- **Soft assertion?** Para vários campos independentes da mesma tela; nunca para pré-condição.
- **Page Object?** Útil no Playwright com métodos de intenção e sem `expect` escondido (Inferido); no Cypress a documentação os lista como antipadrão (Verificado, V-24).
- **Testar via UI ou via API?** Regras de validação e de estado: via API também, porque a tela esconde o botão e o back-end esquece a regra.
- **Snapshot?** Só com diff revisado; mascarar timestamp e ID, nunca preço, permissão ou status.
- **Quarentena ou apagar?** Quarentena fora do gate, com ticket, dono e prazo; passado o prazo, corrigir ou apagar. Não aposente teste só porque nunca falhou: confirme que ele **consegue** falhar.
- **Revisão de teste gerado por IA?** Sempre por revisor de contexto limpo, com checagem de mutação, e declarando que é o mesmo modelo.
- **Mais workers causam 5xx?** É capacidade do ambiente, não teste intermitente: reduza workers ou escale o ambiente.

## Temas sem skill própria

Lacunas registradas na síntese; o tratamento mínimo fica aqui.

**Regressão visual e snapshot.** Use para design system, checkout, páginas impressas e e-mails; não para tela que muda toda semana, onde o time aprende a aprovar diff sem olhar. Prefira captura de componente a página inteira, mascare conteúdo dinâmico, gere e compare no mesmo ambiente (mesmo container e versão do pacote) e revise o diff antes de atualizar a referência. Detalhes de API do Playwright em `automacao-web-e2e.md` (Inferido; confirme na versão instalada).

**Suíte lenta.** Em ordem: (1) medir p50/p90 do tempo até o feedback, não a média; (2) descer testes para a camada mais barata; (3) paralelizar só o que é independente (`fullyParallel` exige testes de fato independentes); (4) sharding entre máquinas; (5) seleção por mudança (`jest --findRelatedTests`, `nx affected`, `pytest-testmon`, Inferido do brain), sem esquecer dependências por dado, configuração e evento: o smoke dos fluxos críticos roda sempre; (6) `test-auditor` para aposentar o que custa mais do que protege. Orçamento de referência para regressão crítica por PR: até cerca de 15 min, senão o time para de esperar (valor do brain, ajustável).

**Cobertura como relatório.** Use cobertura de linhas e ramos como indício de lacuna em código alterado, não como nota. Em decisão regulada ou de segurança, MC/DC como técnica de desenho (ver `design-de-testes.md`), sem afirmar exigência normativa para o seu produto. Combine com mutação nos módulos de risco alto.
