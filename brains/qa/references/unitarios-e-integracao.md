# Testes unitários e de integração

Use para escolher fronteiras, revisar asserções, substituir dependências ou
decidir o próximo teste. A unidade é um comportamento observável; não precisa
ser exatamente uma classe. Um teste pode atravessar vários objetos e ainda
ser barato, determinístico e útil.

## Sumário

- [Escolha do nível e do oráculo](#escolha-do-nível-e-do-oráculo)
- [Dublês sem falsa confiança](#dublês-sem-falsa-confiança)
- [Exemplo executável: limite de reserva](#exemplo-executável-limite-de-reserva)
- [Integração que demonstra a fronteira real](#integração-que-demonstra-a-fronteira-real)
- [Tempo, concorrência e assincronismo](#tempo-concorrência-e-assincronismo)
- [Propriedades, modelos e mutação](#propriedades-modelos-e-mutação)
- [TDD, legado e manutenção](#tdd-legado-e-manutenção)

## Escolha do nível e do oráculo

| Pergunta | Menor nível convincente | O que verificar |
| --- | --- | --- |
| O desconto arredonda conforme a regra? | unitário, dinheiro em representação definida pelo domínio | exemplos calculados independentemente; ordem e modo de arredondamento |
| O acesso depende do dono e do perfil? | unitário da política + integração da rota | matriz de permissões e ausência de leitura/mutação indevida |
| A transação desfaz alterações parciais? | integração com o banco e o mecanismo de transação utilizados | dados persistidos após falha injetada e nova conexão |
| O serializer mantém casas decimais e fuso? | integração do adapter/serializer | bytes ou campos produzidos e lidos, incluindo nulos e fronteiras |
| Consumidor e provedor continuam compatíveis? | contrato verificado dos dois lados | cenários de uso reais; contrato sozinho não prova efeito de negócio |
| O usuário conclui a operação no app? | poucos fluxos E2E | resultado visível e efeito persistido por ID de correlação |

Derive o esperado de uma regra independente. Para um desconto de 10% sobre
R$ 100,00, escreva R$ 90,00 no teste; chamar a mesma função de desconto para
montar o esperado só repete o defeito. Para algoritmos complexos, um modelo
simples, uma tabela aprovada ou uma propriedade bem delimitada pode ser o
oráculo. Snapshot é uma fotografia revisável, não uma especificação automática.

Uma asserção deve distinguir uma implementação correta de uma errada
plausível. `resultado != null` não distingue preço correto de preço dez vezes
maior. Verificar retorno, estado e efeitos pode exigir várias asserções no
mesmo caso: “uma asserção por teste” não é uma obrigação.

## Dublês sem falsa confiança

| Dublê | Finalidade | Exemplo | Risco |
| --- | --- | --- | --- |
| Stub | fornecer resposta controlada | provedor retorna “recusado” | resposta divergir do contrato real |
| Fake | implementação simplificada funcional | repositório em memória | não reproduzir isolamento, collation, constraints ou concorrência do banco |
| Spy | observar interação preservando ou delegando comportamento | registrar notificações enviadas ao adapter | verificar detalhe interno sem valor para o usuário |
| Mock | configurar e verificar interações | enviar exatamente uma cobrança com chave e valor definidos | testar o roteiro de chamadas, não a regra |
| Dummy | preencher parâmetro não usado neste cenário | objeto sem comportamento necessário | ocultar que o parâmetro passou a ser relevante |

Use objetos reais simples por padrão. Substitua relógio, aleatoriedade,
rede, sistema de arquivos e efeitos caros quando essas fronteiras atrapalham
o teste da regra. Quando o risco está na fronteira, teste também a fronteira
real. Um fake de banco não prova que uma transação funciona no banco real.

Verificações de interação fazem sentido quando **a interação é o efeito**:
uma notificação enviada ao destinatário certo, nenhuma cobrança após recusa,
mesma chave de idempotência em um retry. Evite verificar ordem de métodos
privados que pode mudar sem alterar esse contrato.

Em Python, substitua o nome no módulo em que ele é consultado. Se
`pedidos.py` faz `from gateway import cobrar`, o alvo usual é
`pedidos.cobrar`. `autospec`/`create_autospec` ajudam a detectar chamadas com
assinatura errada; não provam semântica nem compatibilidade de rede. Configure
os retornos explicitamente para não tratar um objeto Mock como resultado
válido. Consulte [unittest.mock](https://docs.python.org/3/library/unittest.mock.html#where-to-patch).

Fixtures devem deixar visível o dado que explica a regra. Prefira
`pedido(total_centavos=10000, status="pendente")` a um enorme objeto padrão
cuja combinação crítica está escondida. Estado mutável compartilhado entre
testes exige isolamento deliberado. No pytest, teardown após `yield` não
executa se a fixture falhar antes de chegar ao `yield`; registre limpeza
conforme recursos são adquiridos, ou separe aquisições em fixtures menores.
Veja [fixtures e teardown](https://docs.pytest.org/en/stable/how-to/fixtures.html).

## Exemplo executável: limite de reserva

Regra **didática**, não universal: aceitar quantidade inteira de 1 até o saldo
disponível, inclusive; entrada inválida não altera estoque. A especificação
define que booleanos não contam como inteiros. O exemplo inclui a função
para ser executável isoladamente; em um projeto, importe a implementação real
em vez de manter uma cópia no arquivo de teste.

Salve o bloco como `test_reserva.py` e rode `python3 -m unittest -v test_reserva`.
Usa apenas a biblioteca padrão. `subTest` identifica cada partição que falhar;
a API está em [unittest](https://docs.python.org/3/library/unittest.html).

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

Esse teste detecta `>` trocado por `>=`, decremento ausente, decremento errado
e uso do saldo inicial na segunda reserva. Não prova concorrência, persistência
ou autorização. As quatro funções contêm várias entradas; não reporte seu
número como cobertura de todo o produto. Se a implementação passa a lançar
`TypeError` por contrato, atualize a expectativa após confirmar a mudança da
regra, não apenas para obter verde.

## Integração que demonstra a fronteira real

Escolha uma fronteira por objetivo e declare o que continua simulado. “Teste
com container” descreve infraestrutura, não a confiança obtida. Para banco,
use o motor, versão relevante, schema/migrações, extensões e opções de
produção quando essas diferenças podem mudar o resultado.

| Risco | Arranjo | Estímulo | Oráculo independente |
| --- | --- | --- | --- |
| perda de atomicidade | pedido e estoque gravados; provocar falha entre débito e conclusão | executar confirmação | em nova transação: estoque e pedido permanecem no estado anterior; nenhum evento definitivo publicado |
| duplicação por retry | mesma chave e mesmo payload em duas requisições | repetir a confirmação após resposta perdida | um lançamento financeiro; mesma identidade da operação; saldo alterado uma vez |
| reutilização indevida da chave | chave conhecida com payload diferente | mudar valor e reenviar | conflito previsto no contrato; operação original e saldo preservados |
| corrida no último item | estoque 1; duas conexões independentes, dois pedidos | liberar os dois workers por uma barreira | só um pedido confirmado; estoque 0; outro recebe conflito/recusa definida |
| evento fora de ordem | pedido já cancelado | entregar evento de estado anterior | estado final respeita regra aprovada; evento registrado/tratado sem ressuscitar o pedido |
| migração incompatível | snapshot sintético com dados antigos e casos raros | migrar e ler/escrever com versões suportadas | registros reconciliados; constraints válidas; plano de recuperação executável |

Em transações, uma única conexão de teste com rollback externo pode mascarar
commit, visibilidade e efeitos em outras conexões. Para provar commit e
concorrência, observe por conexões independentes e pelo limite transacional
real. SQLite em memória não substitui automaticamente PostgreSQL/MySQL.

Se uma operação grava no banco e publica em broker, falhe entre essas ações.
Verifique o mecanismo real de recuperação (por exemplo, outbox), duplicatas,
reentrega e consistência eventual. Status HTTP de sucesso sozinho não prova
que o consumidor aplicou o evento. Para contratos e mensageria, complemente
com [automação de API](automacao-api.md).

## Tempo, concorrência e assincronismo

- **Tempo de negócio:** injete um relógio; teste imediatamente antes, no
  instante exato e depois da expiração. Declare precisão, fuso e se a
  fronteira é inclusiva. Avançar um relógio falso local não avança o relógio
  do banco ou de outro processo.
- **Duração e timeout:** use tempo monotônico quando disponível. Aguarde a
  condição com prazo e diagnóstico; ao expirar, falhe mostrando último estado
  observado. Nunca retorne sucesso apenas porque o prazo terminou.
- **Concorrência:** duas chamadas sequenciais não testam corrida. Use barreiras
  ou ganchos controlados para sobrepor o trecho crítico, capture a conclusão
  de todos os workers e falhe se qualquer exceção ficar sem observação.
- **Eventos:** correlacione pelo ID exclusivo do teste. Um evento de execução
  anterior no tópico pode gerar falso verde. Separe mensagem recebida,
  processada e efeito confirmado.
- **Aleatoriedade:** registre seed e menor caso que falhou, além da versão
  do gerador. Uma seed sozinha pode não reproduzir uma falha após atualização
  de biblioteca ou mudança na ordem dos testes.

## Propriedades, modelos e mutação

Property-based testing pede um domínio de entrada e uma propriedade que vale
para ele. “Nunca lança erro” é inadequado se entradas inválidas devem falhar.

| Propriedade candidata | Pré-condição necessária | Armadilha |
| --- | --- | --- |
| reservar `n` reduz saldo exatamente em `n` | `n` inteiro positivo e menor ou igual ao saldo | gerar só zero ou rejeitar quase todos os exemplos |
| ordenar preserva elementos e multiplicidades | mesma noção de identidade e ordenação definida | verificar só ordem e aceitar perda de elementos |
| serializar e desserializar preserva valor | tipos representáveis e normalização acordada | duas funções com o mesmo erro produzirem round-trip verde |
| mesmo evento repetido não repete efeito | mesmo ID, mesmo escopo e dentro da retenção da deduplicação | supor idempotência eterna ou para payload diferente |
| total não diminui ao acrescentar item | sem descontos progressivos, tetos ou frete variável | declarar monotonicidade onde a regra não permite |

Combine exemplos explícitos e propriedades; um complementa o outro. Para
fluxos, mantenha um modelo simples de estados e gere sequências de ações.
Compare o sistema ao modelo após cada transição e preserve a menor sequência
que falhou. Essa é uma aplicação de [stateful testing do Hypothesis](https://hypothesis.readthedocs.io/en/latest/stateful.html).
Não replique o algoritmo de produção inteiro dentro do modelo.

Mutação avalia a capacidade de detectar alterações plausíveis: trocar
comparadores, remover efeito ou inverter condição. Comece pela regra de
maior risco e veja **qual comportamento deixou de ser verificado**. Mutante
sobrevivente pode significar teste fraco, código não exercitado ou mudança
equivalente; não adicione uma asserção artificial só para elevar o indicador.
Registre a fórmula da ferramenta: tratamento de equivalentes, ignorados,
timeouts e erros de compilação varia. Cobertura de linha/ramos e score de
mutação são pistas complementares, não notas universais de qualidade.

## TDD, legado e manutenção

No ciclo TDD, observe o teste falhar pelo motivo correto antes da correção,
faça a menor alteração que satisfaz a regra e refatore com a suíte verde.
Erro de importação não demonstra que o teste detecta o defeito. Em correção,
reproduza o comportamento errado, teste o exemplo do incidente e generalize
apenas as fronteiras plausíveis relacionadas.

Em legado sem especificação, teste de caracterização registra o comportamento
atual para proteger a alteração. Marque comportamentos suspeitos: o registro
não os transforma em regra aprovada. Para snapshots, revise o diff semântico
antes de atualizar; mascarar timestamps e IDs pode ajudar, mas mascarar preço,
permissão ou status remove justamente o oráculo.

Ao revisar uma suíte, procure primeiro os testes que passam com implementação
errada, depois vazamentos de estado, esperas e dependências frágeis. Remova
duplicação sem esconder dados e asserções importantes em helpers genéricos.
Uma refatoração interna que preserva o contrato não deveria exigir regravar
um roteiro inteiro de mocks.
