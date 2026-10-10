# Solidity: pitfalls, controle de acesso, upgradeability e mapa OWASP

Itens V-01, V-08, V-09 e V-13 de [fontes.md](fontes.md). Conferido em 2026-10-10; a documentação do Solidity não traz data e alguns exemplos históricos usam pragmas antigos. Confirme `pragma`, versão do compilador e do OpenZeppelin instalados antes de citar API. Os exemplos de código abaixo são redação própria deste plugin.

## Sumário

- [Pitfalls do Solidity (SOL)](#pitfalls-do-solidity-sol)
- [Controle de acesso com OpenZeppelin (ACC)](#controle-de-acesso-com-openzeppelin-acc)
- [Upgradeability (UPG)](#upgradeability-upg)
- [Mapa OWASP SC Top 10 (2025)](#mapa-owasp-sc-top-10-2025)
- [SWC como identificador opcional](#swc-como-identificador-opcional)
- [EthTrust v3 quando o usuário pedir conformidade](#ethtrust-v3-quando-o-usuário-pedir-conformidade)
- [Limites desta página](#limites-desta-página)

## Pitfalls do Solidity (SOL)

### SOL-01 Reentrância e Checks-Effects-Interactions

Toda chamada externa transfere o controle ao destino, que pode chamar de volta antes de a função terminar. A defesa é de ordem: validar, atualizar estado, só então chamar fora. Pagamentos por saque (pull) deixam o destinatário iniciar a retirada em vez de o contrato empurrar fundos.

```solidity
// Vulnerável: o saldo só cai depois da chamada externa.
function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount, "insufficient");
    (bool ok, ) = msg.sender.call{value: amount}("");
    require(ok, "send failed");
    balances[msg.sender] -= amount;
}

// Corrigido: efeitos antes da interação (e, opcionalmente, nonReentrant).
function withdraw(uint256 amount) external nonReentrant {
    if (balances[msg.sender] < amount) revert Insufficient();
    balances[msg.sender] -= amount;
    (bool ok, ) = msg.sender.call{value: amount}("");
    if (!ok) revert SendFailed();
}
```

Cenário do primeiro: contrato atacante com `receive()` que chama `withdraw` de novo; cada reentrada passa no `require` porque o saldo ainda não caiu. Confira onde `ReentrancyGuard` está na versão do OpenZeppelin instalada (o caminho mudou entre 4.x e 5.x: **Inferido**, estável, confirme em `lib/`). Reentrância também ocorre sem `call` de ether: hooks de ERC-721/1155/777, `safeTransfer*` e callbacks de pool (veja ERC-03 e HOOK-10) e **entre funções** que compartilham estado (reentrância cruzada).

### SOL-02 Retorno de chamada de baixo nível

`call`, `send` e `delegatecall` devolvem `false` em falha em vez de reverter. Ignorar o booleano deixa o estado seguir como se o envio tivesse ocorrido. Verificação: toda ocorrência de `.call(`/`.send(` tem o retorno testado e erro customizado.

### SOL-03 `tx.origin`

`tx.origin` é o endereço que iniciou a transação, não o chamador direto. Um contrato malicioso chamado pelo dono herda o `tx.origin` do dono e passa uma checagem `require(tx.origin == owner)`. Use `msg.sender`.

### SOL-04 Laços e limite de gás

Laço sobre estrutura que cresce por ação de usuário (lista de apostadores, de beneficiários) pode passar do limite de gás do bloco e travar a função, inclusive travar fundos. Isso é **achado válido** em contrato (SC10), mesmo que o prompt de revisão web exclua DoS. Correção: paginação, saque individual (pull), limite de tamanho.

### SOL-05 Dados `private` e aleatoriedade

`private` impede acesso por outros contratos, não a leitura do storage por qualquer nó. Não guarde segredo ali. Aleatoriedade derivada de variáveis de bloco pode ser influenciada por quem produz o bloco; use fonte de aleatoriedade verificável. A página do Solidity fala disso em termos gerais; não atribua a ela afirmações específicas sobre `block.timestamp` ou `blockhash`.

### SOL-06 `unchecked`, conversões e divisão

Desde 0.8 a aritmética reverte por padrão, exceto dentro de `unchecked`. Cada bloco `unchecked` precisa de prova de limite escrita (por exemplo, "i < length, length ≤ 2^64"). Conversões para tipo menor truncam sem erro em casts explícitos; divisão inteira arredonda para baixo: multiplique antes de dividir e decida a direção do arredondamento em cada fórmula de preço/share.

### SOL-07 `delete` e mappings

`delete` em struct ou array não limpa as chaves de um `mapping` interno. Estado "apagado" que ainda guarda valores permite reuso indevido. Limpe chave por chave ou desenhe sem depender de `delete`.

### SOL-08 Proxy sem permissões

Um proxy que repassa chamadas arbitrárias não deve ser dono, admin ou detentor de papel em outro contrato: qualquer um poderia induzi-lo a chamar a função protegida.

### SOL-09 Valor retido, fail-safe e warnings

Limite o valor que o contrato retém (tetos de depósito, saques por período). Prever modo fail-safe (pausa, limites de emergência) com quem pode acionar e desativar. Compile com versão atual e leve warnings a sério: zere-os ou justifique cada um.

Outras armadilhas listadas pela página oficial (consulte-a para detalhes): profundidade da pilha, ponteiros de função interna em contratos upgradeable, envio e recebimento de Ether, complemento de dois. A página não cobre oráculos, MEV nem assinaturas: use [oraculos-l2-defi.md](oraculos-l2-defi.md) e [padroes-erc-e-assinaturas.md](padroes-erc-e-assinaturas.md).

## Controle de acesso com OpenZeppelin (ACC)

Base: documentação de Access Control da série 5.x. Nomes variam em outras versões.

| Conceito | O que significa na revisão |
| --- | --- |
| Papéis `bytes32`, `hasRole`/`onlyRole` | Cada função de estado mapeia para um papel; função sem papel precisa de justificativa |
| Admin por papel | Cada papel tem papel administrador definido; um ciclo ou admin errado concede poder demais |
| `DEFAULT_ADMIN_ROLE` | Risco alto; o admin de todos os papéis por padrão. Um só titular, em produção multisig |
| `AccessControlDefaultAdminRules` | Um admin, transferência em duas etapas com atraso: reduz perda por erro de endereço |
| `AccessControlEnumerable` | Permite enumerar membros (útil em auditoria e monitoramento) |
| `TimelockController` | Proposer/executor com atraso mínimo; dá janela de reação a usuários |

Pontos de revisão que a doc sustenta:

1. **ACC-01** Tabela entry point × papel; para cada função que muda estado, um teste com ator sem papel que deve reverter.
2. **ACC-02** Quem recebe o `DEFAULT_ADMIN_ROLE` no construtor/initializer? Se for o deployer EOA, há plano para transferir a multisig?
3. **ACC-03** Renunciar ao admin pode travar o sistema se proposer/executor do timelock ficarem indisponíveis. Exija plano de recuperação **antes** de qualquer renúncia.
4. **ACC-04** Monitorar `RoleGranted`/`RoleRevoked`. É controle operacional: peça ao dono; se não houver evidência, rotule **Suposição**.
5. **ACC-05** Funções irmãs: compare cada par (`deposit`/`depositFor`, `pause`/`unpause`, `setFee`/`setFees`). Uma com modificador e a vizinha sem é suspeita até haver justificativa escrita.

```solidity
// Suspeito: a versão em lote esqueceu o papel.
function setFee(uint256 f) external onlyRole(FEE_MANAGER) { fee = f; }
function setFees(uint256[] calldata fs) external { for (uint i; i < fs.length; ++i) fees[i] = fs[i]; }
```

Preferir bibliotecas auditadas a papéis ou criptografia próprios reduz superfície; ainda assim, confirme que o papel certo foi aplicado.

## Upgradeability (UPG)

Base: documentação dos plugins de upgrades e do Writing Upgradeable, mais o README do repositório do OpenZeppelin. A página do plugin não cobre `immutable`.

### Escolha do padrão (UPG-01)

| Padrão | Quem atualiza | Atenção |
| --- | --- | --- |
| Transparent | `ProxyAdmin` (no 5.x o parâmetro é `initialOwner`) | O admin não chama a implementação; não reutilize um `ProxyAdmin` já implantado (desabilita a upgradeability) |
| UUPS | A própria implementação | Exige sobrescrever `_authorizeUpgrade`; sem restrição de acesso qualquer um troca a implementação |
| Beacon | Dono do beacon | Todos os proxies mudam atomicamente: bom para frotas, risco concentrado |

```solidity
// Falha crítica em UUPS: upgrade sem restrição.
function _authorizeUpgrade(address) internal override {}
// Correto: restringir (papel ou owner).
function _authorizeUpgrade(address) internal override onlyOwner {}
```

### Initializers (UPG-02)

- Contratos upgradeable não usam construtor para estado: usam `initializer`/`onlyInitializing`.
- A implementação chama `_disableInitializers()` no construtor, para que ninguém a inicialize diretamente.
- Initializers chamam os initializers dos pais.
- Sem valores iniciais em declarações de campo (`uint256 fee = 10;` não vai para o storage do proxy).
- Um `initialize` de V2 não roda num proxy já inicializado: use `reinitializer(n)` (**Inferido**, conhecimento estável do OZ).

### Layout de storage (UPG-03)

Não mude tipo ou ordem de variável existente, não insira antes, não remova; novas variáveis vão no fim. Alternativas: `__gap` ou storage com namespace (ERC-7201, Solidity ≥ 0.8.20, usado pelo OZ upgradeable desde o 5.0). Contratos criados com `new` dentro de um upgradeable não são upgradeable. `delegatecall` e `selfdestruct` são proibidos na implementação.

```solidity
// V1: totalDeposits ocupa o slot 0 (depois dos slots de bases).
// V2 ERRADO: feeBps inserida antes desloca totalDeposits e balances.
uint256 public feeBps;        // novo, no lugar errado
uint256 public totalDeposits;
// V2 CERTO: variável nova no fim (ou em namespace ERC-7201).
uint256 public totalDeposits;
mapping(address => uint256) public balances;
uint256 public feeBps;        // novo, no fim
```

Compare o layout entre versões com a ferramenta de validação do plugin de upgrades (o usuário executa; a versão do plugin não aparece na página, confirme a compatibilidade com o OpenZeppelin instalado).

### Versões e cadeia de suprimento (UPG-04, UPG-05)

Layouts de storage de contratos upgradeable são incompatíveis entre versões maiores (4.9.3 para 5.0.0 é dado como inseguro no README): troca de versão maior exige plano de migração. O repositório usa tags: `latest` (auditada), `dev` (final, não auditada), `next` (candidata). Pine a tag auditada e leia `audits/` antes de adotar versão. EIPs 1967, 1822 e 7201 não foram lidas diretamente nesta pesquisa (lacuna L11).

## Mapa OWASP SC Top 10 (2025)

Rótulo principal dos achados. A lista é de alto nível e a licença exibida pelo OWASP é ambígua: este mapa é destilação própria, sem texto copiado. Confirme numeração e nomes na [página do projeto](https://owasp.org/www-project-smart-contract-top-10/).

| Rótulo | Tema | Verificação concreta |
| --- | --- | --- |
| SC01 | Controle de acesso | Para cada função de estado, qual papel? Existe ator sem papel que consiga chamá-la (teste `vm.prank`)? Funções irmãs comparadas? |
| SC02 | Manipulação de oráculo | Fonte do preço, idade (`updatedAt` × heartbeat), possibilidade de manipular por pool raso |
| SC03 | Erros de lógica | Invariante de negócio (conservação, solvência) escrita e testada por fuzz/invariante |
| SC04 | Validação de entrada | Cada parâmetro externo tem limite/forma verificados; endereço zero; arrays de tamanhos diferentes |
| SC05 | Reentrância | Chamada externa antes de atualizar estado; hooks de token; reentrância cruzada |
| SC06 | Chamadas externas sem checagem | Retorno de `call`/`transfer` de token tratado; `SafeERC20` |
| SC07 | Flash loan | O que depende de saldo/preço instantâneo na mesma transação? (MEV e flash loan: lacuna L12) |
| SC08 | Overflow/underflow | Blocos `unchecked` com prova de limite; casts de tipo |
| SC09 | Aleatoriedade insegura | Fonte de aleatoriedade influenciável por produtor de bloco |
| SC10 | Negação de serviço | Laços ilimitados, gás de pior caso, dependência de chamada externa que pode reverter |

## SWC como identificador opcional

O SWC Registry (37 entradas, SWC-100 a SWC-136) declara-se não atualizado a fundo desde 2020, incompleto e possivelmente com erros. Use só como identificador estável no campo opcional `swc_id`, nunca como lista de verificação: SWC-107 reentrância, SWC-115 `tx.origin`, SWC-101 overflow, SWC-114 ordem de transação, SWC-136 dado privado on-chain.

## EthTrust v3 quando o usuário pedir conformidade

Especificação da Enterprise Ethereum Alliance (março de 2025, Apache-2.0) com três níveis: [S] verificável por ferramenta automática, [M] análise estática rigorosa com julgamento humano, [Q] correção da lógica de negócio. A página afirma esperar um sucessor no segundo semestre de 2026: confira a edição vigente. O texto completo (cerca de 270 mil caracteres) não foi lido nesta pesquisa, só o cabeçalho e os níveis; não declare conformidade EthTrust com base neste plugin.

## Limites desta página

- Não cobre MEV, flash loans em profundidade, pontes e mensageria cross-chain (lacunas L12 e L13).
- Vyper: nenhum item das fontes cobre; revisão genérica de Vyper é **Suposição**.
- Hardhat e indexação: sem fonte validada (lacunas L3 e L2).
