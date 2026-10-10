# Hooks do Uniswap v4 e cenários de incidente como perguntas de revisão

Fontes: Trail of Bits, "Building secure Uniswap v4 hooks" (2026-07-30, Nicolas Donboly; V-17) e listagem de rekt.news (V-18). Destilação própria, sem texto das fontes. Rótulos: **Verificado** = V-17/V-18 (7 padrões do blog; 8 a 10 acrescentados pelo validador); **Inferido** = detalhe de API do Uniswap v4 não lido por mim nesta etapa (confira a versão de `v4-core`/`v4-periphery` do projeto).

## 1. Hooks (W3-HOOK-01..10)

Para cada hook, liste as permissões que ele declara (bits do endereço) e os callbacks que implementa; depois responda:

| ID | Padrão de falha | Pergunta de revisão | Teste a propor |
|---|---|---|---|
| HOOK-01 | Callback sem verificar o chamador | Todo callback restringe `msg.sender` ao PoolManager (BaseHook/SafeCallback ou checagem própria)? | Chamar o callback direto de uma conta qualquer: deve reverter |
| HOOK-02 | Confiar em qualquer pool | O hook deriva o `PoolId` da `PoolKey` e só atende pools permitidos (allowlist)? Um pool malicioso com o mesmo hook consegue mudar o estado? | Registrar um pool não permitido e chamar swap/liquidez |
| HOOK-03 | Contabilidade com sinal, arredondamento e baldes misturados | Valores positivos/negativos (delta) têm o sinal certo? Arredondamento favorece o protocolo? Os baldes (token0/token1, taxa/principal) não se misturam? | Invariante de conservação e round-trips (adicionar e remover liquidez, swap ida e volta) |
| HOOK-04 | Lógica no hook errado | O que depende do estado antes do swap está em `beforeSwap`, e o que depende do estado depois está em `afterSwap`? | Teste que lê o estado nos dois pontos |
| HOOK-05 | Bits do endereço como API | As permissões do endereço batem com os callbacks implementados? Um callback implementado e não habilitado nunca roda; o inverso reverte | Testar o endereço minerado contra `getHookPermissions` |
| HOOK-06 | Falhas bloqueando saída | Código opcional (estatística, recompensa) está isolado com `try`/`catch`, para que falha dele não impeça swap, remoção de liquidez ou saque? | Fazer o código opcional reverter e conferir que o fluxo principal continua |
| HOOK-07 | Estado temporário alterado em chamadas aninhadas | Estado transitório é chaveado por `PoolId` e por chamador? Operações sobrepostas são rejeitadas? O estado é limpo ao final? | Chamada aninhada/reentrante com dois pools |
| HOOK-08 | Token com taxa de transferência | O hook assume que o valor recebido é o valor pedido? | Fork/mocks com token de taxa |
| HOOK-09 | Rebase | Saldos guardados pelo hook mudam sem evento? | Mock de rebase |
| HOOK-10 | Hooks de callback em tokens | Tokens com hooks de transferência chamam código externo no meio do fluxo (reentrância)? | Token com callback reentrante |

Observações:

- O blog recomenda fuzzing com Echidna e Medusa. O plugin trata Foundry como padrão (V-02); Echidna/Medusa ficam como ferramentas do usuário (Medusa não foi lido, lacuna L7).
- Os padrões são específicos do Uniswap v4; para outros AMMs, use só as perguntas gerais (contabilidade, isolamento de falhas, validação do chamador).
- Rótulo do que estiver fora do blog: **Inferido** (por exemplo, nomes exatos de callbacks e deltas).

## 2. Cenários como perguntas (W3-SCN-01..06)

Origem: oito incidentes listados em rekt.news entre 2026-09-14 e 2026-10-08 (V-18, Verificado na listagem). Causas podem mudar com post-mortems: use como cenário de teste, não como fato técnico, e não cite valores.

| ID | Cenário | Pergunta de revisão | Onde olhar |
|---|---|---|---|
| SCN-01 | Oráculo raso: preço de token inflado como colateral; oráculo adulterado por pool manipulada | Algum preço vem de pool com pouca liquidez ou de um único ponto? Colateral novo passa por um limite de preço/liquidez? | `defi-oracle-l2-review` passo 2 e 3; W3-ORA-04 |
| SCN-02 | Lastro de mint/bridge: mint sem lastro por falha de encaminhamento | O mint só ocorre contra evidência de lastro no mesmo passo? O encaminhamento pode ser forjado? | Funções de mint, handlers de mensagens (pontes: fora da cobertura, lacuna L13) |
| SCN-03 | Colisão de chave de cache ou de hash | Chaves compostas usam `abi.encode` (não `encodePacked` com tipos dinâmicos)? | `keccak256(abi.encodePacked(...))` |
| SCN-04 | Assinaturas válidas abusadas | Cada assinatura está presa a cadeia, contrato, nonce e validade? | `wallet-signing-review`; W3-SIG-02 |
| SCN-05 | Custódia e rotação de chaves | Quem controla chaves de admin/operador/relayer? Há multisig, timelock, plano de rotação e monitoramento de `RoleGranted`/`RoleRevoked`? | W3-ACC-02..04; fora do código: pergunta ao time |
| SCN-06 | Serviços de terceiros que mudam configuração | O protocolo depende de serviço externo (feed, relayer, API de segurança) que pode alterar parâmetros sem aviso? | Dependências fora da cadeia: pergunta ao time |

Como usar: no relatório, uma seção "Perguntas ao time" com a resposta que o código dá ou "não determinável pelo código". Perguntas sem resposta viram pendência (Apêndice B), não achado.
