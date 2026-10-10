# Testes unitários e de integração, TDD e dados de teste

Use para escolher fronteiras, revisar asserções, substituir dependências, decidir o próximo teste ou montar massa de dados. A unidade é um **comportamento observável**, não necessariamente uma classe: um teste pode atravessar vários objetos e continuar barato, determinístico e útil. Base: `unitarios-e-integracao.md`, `dados-ambientes-ci.md` e `testes-e-debugging.md` do brain-of-agent (MIT, conteúdo próprio, condensado e adaptado) com V-25, V-28, V-31, V-33, V-15, V-36 (ver `fontes.md`). Validado em 2026-10-10.

## Sumário

- [Nível e oráculo](#nível-e-oráculo)
- [Dublês sem falsa confiança](#dublês-sem-falsa-confiança)
- [Mocks e timers no Vitest](#mocks-e-timers-no-vitest)
- [Exemplo executável: limite de reserva](#exemplo-executável-limite-de-reserva)
- [Integração que demonstra a fronteira real](#integração-que-demonstra-a-fronteira-real)
- [Tempo, concorrência e assincronismo](#tempo-concorrência-e-assincronismo)
- [Propriedades, modelos e mutação](#propriedades-modelos-e-mutação)
- [TDD, legado e manutenção](#tdd-legado-e-manutenção)
- [Dados de teste](#dados-de-teste)

## Nível e oráculo

| Pergunta | Menor nível convincente | O que verificar |
| --- | --- | --- |
| O desconto arredonda conforme a regra? | unitário, dinheiro em representação definida pelo domínio (centavos inteiros) | exemplos calculados independentemente; ordem e modo de arredondamento |
| O acesso depende do dono e do perfil? | unitário da política + integração da rota | matriz de permissões e ausência de leitura/mutação indevida |
| A transação desfaz alterações parciais? | integração com o banco e o mecanismo de transação reais | dados persistidos após falha injetada, lidos por nova conexão |
| O serializer mantém casas decimais e fuso? | integração do adapter | campos produzidos e lidos, incluindo nulos e fronteiras |
| Consumidor e provedor continuam compatíveis? | contrato verificado dos dois lados | cenários de uso reais; contrato sozinho não prova efeito de negócio |
| O usuário conclui a operação no app? | poucos E2E | resultado visível e efeito persistido por ID de correlação |

**Derive o esperado de uma regra independente.** Para 10% sobre R$ 100,00, escreva R$ 90,00 no teste; chamar a mesma função de desconto para montar o esperado repete o defeito. Para algoritmos complexos, um modelo simples, uma tabela aprovada ou uma propriedade delimitada pode ser o oráculo. Snapshot é fotografia revisável, não especificação. Uma asserção deve distinguir implementação correta de errada plausível: `resultado != null` não distingue preço correto de preço dez vezes maior. Verificar retorno, estado e efeitos pode exigir várias asserções no mesmo caso.

## Dublês sem falsa confiança

| Dublê | Finalidade | Risco |
| --- | --- | --- |
| Stub | resposta controlada ("recusado") | divergir do contrato real |
| Fake | implementação simplificada (repositório em memória) | não reproduz isolamento, collation, constraints nem concorrência do banco |
| Spy | observar interação preservando comportamento | verificar detalhe interno sem valor para o usuário |
| Mock | configurar e verificar interações (uma cobrança com chave e valor definidos) | testar o roteiro de chamadas, não a regra |
| Dummy | preencher parâmetro não usado | ocultar que o parâmetro passou a ser relevante |

Use objetos reais simples por padrão. Substitua relógio, aleatoriedade, rede, sistema de arquivos e efeitos caros quando atrapalham o teste da regra. Quando o risco está na fronteira, teste também a fronteira real: um fake de banco não prova que a transação funciona no banco real. Verificação de interação faz sentido quando **a interação é o efeito** (notificação ao destinatário certo, nenhuma cobrança após recusa, mesma chave de idempotência no retry); evite verificar ordem de métodos privados.

Python: substitua o nome no módulo em que ele é consultado (se `pedidos.py` faz `from gateway import cobrar`, o alvo usual é `pedidos.cobrar`); `autospec` detecta assinatura errada, não semântica nem compatibilidade de rede; configure os retornos para não tratar um `Mock` como resultado válido. No pytest, o teardown após `yield` não roda se a fixture falhar antes do `yield`: registre a limpeza conforme adquire recursos. Fixtures devem deixar visível o dado que explica a regra: `pedido(total_centavos=10000, status="pendente")` em vez de um objeto padrão enorme.

## Mocks e timers no Vitest

Fonte: documentação do Vitest (V-25, Verificado na versão da página lida). `vi.fn`, `vi.spyOn` e `vi.mock` (com hoisting); `importOriginal` para mock parcial; o mock só afeta acesso externo ao módulo; limpe e restaure mocks entre testes; `vi.setSystemTime` não reseta sozinho (use `vi.useRealTimers()`); `vi.stubGlobal` e `import.meta.env` persistem entre testes, a menos que use `unstubGlobals`/`unstubEnvs` ou `vi.unstubAll*`. Jest não tem fonte oficial lida: confirme na documentação. Regra: resetar mocks, relógio e globals entre testes (S-07).

## Exemplo executável: limite de reserva

Regra **didática**, não universal: aceitar quantidade inteira de 1 até o saldo disponível, inclusive; entrada inválida não altera estoque; booleanos não contam como inteiros. A função está no arquivo para ser executável isoladamente; em um projeto, importe a implementação real. Salve como `test_reserva.py` e rode `python3 -m unittest -v test_reserva` (só biblioteca padrão; `subTest` identifica cada partição que falhar).

```python
import unittest


class Estoque:
    def __init__(self, disponivel):
        self.disponivel = disponivel

    def reservar(self, quantidade):
        if type(quantidade) is not int or quantidade <= 0:
            raise ValueError("quantidade deve ser inteiro positivo")
        if quantidade > self.disponivel:
            raise ValueError("estoque insuficiente")
        self.disponivel -= quantidade
        return self.disponivel


class TestReserva(unittest.TestCase):
    def test_aceita_limites_inclusivos_e_decrementa_exatamente(self):
        for quantidade, esperado in [(1, 4), (4, 1), (5, 0)]:
            with self.subTest(quantidade=quantidade):
                estoque = Estoque(5)
                self.assertEqual(estoque.reservar(quantidade), esperado)
                self.assertEqual(estoque.disponivel, esperado)

    def test_recusa_quantidade_invalida_sem_mutacao(self):
        for quantidade in [0, -1, 6, 1.5, "1", None, True]:
            with self.subTest(quantidade=quantidade):
                estoque = Estoque(5)
                with self.assertRaises(ValueError):
                    estoque.reservar(quantidade)
                self.assertEqual(estoque.disponivel, 5)

    def test_segunda_reserva_considera_o_saldo_atual(self):
        estoque = Estoque(5)
        estoque.reservar(4)
        with self.assertRaisesRegex(ValueError, "estoque insuficiente"):
            estoque.reservar(2)
        self.assertEqual(estoque.disponivel, 1)

    def test_estoque_esgotado_recusa_reserva(self):
        estoque = Estoque(0)
        with self.assertRaises(ValueError):
            estoque.reservar(1)
        self.assertEqual(estoque.disponivel, 0)


if __name__ == "__main__":
    unittest.main()
```

(Exemplo de brain-of-agent, MIT, atribuição mantida.)

**Verificado em 2026-10-10** (execução local com Python 3.14.4): os 4 testes acima passaram ("Ran 4 tests ... OK"), e a mutação `quantidade > self.disponivel` → `>=` fez o teste de limites inclusivos falhar com `ValueError: estoque insuficiente`. O teste detecta `>` trocado por `>=`, decremento ausente, decremento errado e uso do saldo inicial na segunda reserva. **Não** prova concorrência, persistência nem autorização, e o número de testes não é cobertura do produto. Se a implementação passar a lançar `TypeError` por contrato, atualize a expectativa após confirmar a mudança da regra, não só para obter verde.

## Integração que demonstra a fronteira real

Escolha uma fronteira por objetivo e declare o que continua simulado. "Teste com container" descreve infraestrutura, não a confiança obtida. Para banco, use o motor, a versão relevante, o schema e as migrações, extensões e opções de produção quando essas diferenças podem mudar o resultado.

| Risco | Arranjo | Estímulo | Oráculo independente |
| --- | --- | --- | --- |
| Perda de atomicidade | pedido e estoque gravados; falha entre débito e conclusão | executar a confirmação | em nova transação: estoque e pedido no estado anterior; nenhum evento definitivo publicado |
| Duplicação por retry | mesma chave e mesmo payload em duas requisições | repetir após resposta perdida | um lançamento; mesma identidade; saldo alterado uma vez |
| Reuso indevido da chave | chave conhecida com payload diferente | mudar o valor e reenviar | conflito previsto no contrato; operação original e saldo preservados |
| Corrida no último item | estoque 1; duas conexões independentes | liberar os dois workers por uma barreira | um pedido confirmado; estoque 0; o outro recebe conflito definido |
| Evento fora de ordem | pedido já cancelado | entregar evento de estado anterior | estado final respeita a regra; o pedido não ressuscita |
| Migração incompatível | snapshot sintético com dados antigos e raros | migrar e ler/escrever nas versões suportadas | registros reconciliados; constraints válidas; recuperação executável |

Uma única conexão de teste com rollback externo pode mascarar commit, visibilidade e efeitos em outras conexões; para provar commit e concorrência, observe por conexões independentes. SQLite em memória não substitui PostgreSQL ou MySQL. Se a operação grava no banco e publica em broker, falhe entre as duas ações e verifique o mecanismo real de recuperação (outbox, por exemplo), duplicatas, reentrega e consistência eventual; status HTTP de sucesso não prova que o consumidor aplicou o evento. API, contrato e mensageria: `nao-funcional-e-contrato.md` (skill `test-strategy`).

## Tempo, concorrência e assincronismo

- **Tempo de negócio:** injete um relógio; teste imediatamente antes, no instante exato e depois da expiração; declare precisão, fuso e se a fronteira é inclusiva. Relógio falso local não avança o do banco nem o de outro processo.
- **Duração e timeout:** use tempo monotônico; aguarde a condição com prazo e diagnóstico; ao expirar, falhe mostrando o último estado observado. Nunca retorne sucesso só porque o prazo terminou.
- **Concorrência:** duas chamadas sequenciais não testam corrida. Use barreiras ou ganchos para sobrepor o trecho crítico, capture a conclusão de todos os workers e falhe se uma exceção ficar sem observação.
- **Eventos:** correlacione pelo ID exclusivo do teste (evento de execução anterior no tópico gera falso verde); separe mensagem recebida, processada e efeito confirmado.
- **Aleatoriedade:** registre seed, menor caso que falhou e versão do gerador; a seed sozinha pode não reproduzir após atualizar a biblioteca ou mudar a ordem dos testes.

## Propriedades, modelos e mutação

Property-based pede um domínio de entrada e uma propriedade que vale para ele (fast-check gera centenas de casos e faz *shrinking* até a menor entrada que falha; V-15). "Nunca lança erro" é inadequado se entradas inválidas devem falhar.

| Propriedade candidata | Pré-condição | Armadilha |
| --- | --- | --- |
| reservar `n` reduz o saldo exatamente em `n` | `n` inteiro positivo ≤ saldo | gerar só zero ou rejeitar quase todos os exemplos |
| ordenar preserva elementos e multiplicidades | identidade e ordenação definidas | verificar só a ordem e aceitar perda de elementos |
| serializar e desserializar preserva o valor | tipos representáveis, normalização acordada | duas funções com o mesmo erro dão round-trip verde |
| mesmo evento repetido não repete o efeito | mesmo ID, mesmo escopo, dentro da retenção da deduplicação | supor idempotência eterna ou para payload diferente |
| total não diminui ao acrescentar item | sem descontos progressivos, tetos ou frete variável | declarar monotonicidade onde a regra não permite |

Combine exemplos explícitos com propriedades. Para fluxos, mantenha um modelo simples de estados, gere sequências de ações, compare o sistema ao modelo após cada transição e preserve a menor sequência que falhou (stateful testing, por exemplo no Hypothesis); não replique o algoritmo de produção dentro do modelo.

**Mutação** avalia a capacidade de detectar alterações plausíveis (trocar comparadores, remover efeito, inverter condição). Comece pela regra de maior risco e veja **qual comportamento deixou de ser verificado**. Mutante sobrevivente pode ser teste fraco, código não exercitado ou mudança equivalente; não adicione asserção artificial só para elevar o indicador. Na documentação lida, o Stryker distingue mutante morto de sobrevivente e existe para JS/TS, .NET e Scala (V-15); a fórmula do score e o tratamento de equivalentes não constam na página, então registre a fórmula da ferramenta que usar. Cobertura de linha e ramos e score de mutação são pistas complementares, não notas universais. O mutation check manual de 5 passos está em `padroes-e-antipadroes.md`.

## TDD, legado e manutenção

**Ciclo (V-28, V-31, V-33):** observe o teste falhar pelo motivo correto (comportamento ausente; erro de import não demonstra nada), implemente o mínimo, rode o teste e depois a suíte do escopo, refatore com tudo verde. "Use red/green TDD" no pedido ativa o fluxo; sem o vermelho confirmado, o teste pode passar sem exercitar o código novo. Em **correção de bug**: reproduza o comportamento errado, escreva o teste do exemplo do incidente (falhando), corrija, e generalize só as fronteiras plausíveis. Skill: `tdd-guard`. Exceções declaradas ao ciclo: protótipo descartável, configuração, código gerado; ao pular, diga ao usuário e registre o que não foi coberto.

**Legado sem especificação:** teste de caracterização registra o comportamento atual para proteger a alteração; marque comportamentos suspeitos (o registro não os transforma em regra aprovada) e declare que o teste já passa. Snapshot: revise o diff semântico antes de atualizar; mascarar timestamp e ID ajuda, mascarar preço, permissão ou status remove o oráculo.

**Revisando uma suíte:** procure primeiro testes que passam com implementação errada, depois vazamentos de estado, esperas e dependências frágeis. Remova duplicação sem esconder dados e asserções em helpers genéricos. Refatoração interna que preserva o contrato não deveria exigir regravar um roteiro de mocks. Investigação reproduzível: esperado/observado, build, ambiente, dados redigidos, passos mínimos, hipóteses refutáveis, uma causa por vez. Ex.: pedido duplicado pode nascer de duplo clique, retry de gateway, reprocessamento de fila ou falta de constraint; corrigir só o debounce deixa os outros caminhos vulneráveis; siga o identificador da operação entre camadas.

## Dados de teste

Objetivo: reproduzir uma condição importante e interpretar o resultado, não igualar todos os ambientes a qualquer custo (base: `dados-ambientes-ci.md` do brain, Inferido: sem fonte externa lida, lacuna registrada em `fontes.md`).

**Dados que demonstram a regra.** Comece pela condição que diferencia o resultado: para limite diário de R$ 1.000,00, "cliente válido" é insuficiente; informe limite, total já usado, valor da nova operação, data/fuso e estado das operações que contam para o acumulado. Factory ou builder deixa visível só o que importa.

| Objetivo | Massa mínima útil | Controle adicional |
| --- | --- | --- |
| valor-limite | fronteira e vizinhos com precisão definida | resto válido para isolar a causa da recusa |
| autorização | duas identidades, dois donos/tenants, perfis explícitos | provar que o objeto inacessível existe sem usar dados reais |
| transição de estado | registro em cada origem relevante | criar o estado por caminho coerente ou declarar setup direto |
| paginação | quantidade na fronteira; empates na ordenação | ID para desempate; criação/remoção concorrente |
| desempenho | cardinalidade e distribuição relevantes | hot keys, índices, skew; volume sozinho não representa a carga |
| migração | registros de versões antigas e exceções válidas | nulos históricos, duplicidades, campos legados, encoding |

**Sintético e seguro.** Prefira dados sintéticos e contas de teste. Use domínios reservados (`example.com`, `example.test`) e nunca endereços aleatórios que possam pertencer a alguém; não envie SMS, e-mail, pagamento ou notificação a destinos gerados ao acaso. CPF/CNPJ com dígitos válidos só atendem à estrutura. Dado derivado de produção só com autorização e transformação **antes** de chegar ao ambiente de teste; mascarar o nome e manter documento, geolocalização ou combinação rara pode continuar identificando alguém; pseudonimização não é garantia de anonimização (verifique finalidade, acesso, retenção e risco com os responsáveis). Evidência também contém dados: traces, screenshots, dumps e requisições carregam token ou documento (S-21). Não copie segredos para fixture, snapshot ou commit.

**Isolamento e limpeza.** O teste é dono dos recursos que cria. Identidade exclusiva por execução e por teste (execução + worker + caso + sufixo): a seed reproduz valores, o namespace evita colisão. Estratégias: schema/banco descartável por execução (descarte mesmo após falha); transação por teste com rollback (pode mascarar commit e efeitos externos); tenant/namespace exclusivo (caches, filas e usuários globais podem continuar compartilhados); fixture restaurada para leitura; dados criados por API (a API de setup não deve ignorar invariantes relevantes à prova). Limpe por IDs registrados ou namespace validado, **nunca** por critério amplo ("apagar todos os pedidos de hoje"); confira o destino antes da mutação (URL com `test` não prova que o banco é descartável); limpeza que falhou aparece no relatório sem apagar o erro original. Testes que precisam preservar estado (atualização de app, migração) são um único cenário com preparação própria; o teste B não pode depender implicitamente do A.

**Equivalência de ambiente.** Registre um manifesto curto da execução: artefato/commit, configuração (revisão + flags, sem segredos), dados/schema (migrações + seed/namespace), dependências (reais, sandbox, simuladas, com versões), comando e fuso, plataforma, limites conhecidos. Escolha a fidelidade por risco (cálculo puro não precisa de cluster). Faça um preflight pequeno (identidade do ambiente, versão implantada, dependências, relógio, permissões): falha de setup é **bloqueio**, não aprovação nem automaticamente defeito do produto. Virtualizador de serviço deve ser estrito (requisição inesperada falha com diagnóstico, não recebe 200 genérico) e declarar o que não prova (um PSP virtual verifica retry e UI, não certificados nem o PSP real).
