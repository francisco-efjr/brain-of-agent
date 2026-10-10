# ERC-4626: arredondamento, preview e ataque de inflação

Fontes: EIP-4626 (Final) e a doc ERC4626 do OpenZeppelin 5.x, lidas em V-10. A EIP não trata de inflação ou doação; a doc do OZ trata. Redação e conta próprias. Rótulos: **Verificado** = V-10; **Inferido** = matemática derivada aqui ou comportamento de implementação a confirmar na versão instalada.

IDs: `W3-VLT-01` funções e eventos corretos; `-02` arredondamento a favor do cofre; `-03` defesa contra inflação com teste; `-04` nenhum contrato usa `preview*` como preço; `-05` invariante de ativos totais contra shares.

## 1. Regras de arredondamento (W3-VLT-02, Verificado)

- `convertToShares` e `convertToAssets` arredondam para baixo.
- Princípio geral: a favor do cofre. Para baixo ao emitir shares ou ao enviar ativos; para cima quando o usuário deve fornecer mais (por exemplo, ativos necessários para um `mint` ou shares queimadas num `withdraw`).
- Teste de round-trip na mesma transação: depositar X e resgatar imediatamente nunca devolve mais que X.
- Shares são ERC-20; a implementação cumpre a especificação, não só a interface (`max*` e `preview*` coerentes com as operações reais).
- `preview*` é manipulável (depende do estado atual) e não é oráculo de preço. A EIP sugere `convert*` (com TWAP) para esse fim (W3-VLT-04).

## 2. Ataque de inflação passo a passo (Inferido: matemática; mecanismo Verificado em V-10)

Fórmula típica de emissão (sem offset): `shares = assets * totalSupply / totalAssets`, arredondada para baixo. A implementação do OZ adiciona termos virtuais (`totalSupply + 10**offset` e `totalAssets + 1`); confira na versão lida.

Cenário com cofre vazio e sem proteção, ativo com 18 decimais:

1. O atacante deposita 1 wei: recebe 1 share (`totalSupply = 1`, `totalAssets = 1`).
2. O atacante doa 10.000e18 ativos diretamente ao cofre por `transfer` (não passa por `deposit`): `totalAssets = 10.000e18 + 1`, `totalSupply = 1`.
3. A vítima deposita 10.000e18: `shares = 10.000e18 * 1 / (10.000e18 + 1) = 0` (arredondado para baixo). A vítima entrega os ativos e recebe zero shares.
4. O atacante resgata sua 1 share e leva todo o saldo (20.000e18 + 1). Lucro do atacante: os 10.000e18 da vítima; o custo da doação foi recuperado.

Variação: a vítima deposita 15.000e18 e recebe 1 share (`15.000e18 / (10.000e18 + 1) = 1`, arredondado para baixo). Com `totalSupply = 2` e `totalAssets = 25.000e18 + 1`, cada share vale cerca de 12.500e18: a vítima resgata ~12.500e18 e perde ~2.500e18 (um sexto do depósito), que o atacante embolsa depois de recuperar a doação.

## 3. Mitigações e como conferir (W3-VLT-03)

| Mitigação | Como funciona | Como conferir no código |
|---|---|---|
| Shares e ativos virtuais com offset de precisão | Soma `10**offset` às shares e `1` aos ativos nas fórmulas: o atacante precisaria doar proporcionalmente mais para arredondar a zero | Ler `_decimalsOffset()` e `_convertToShares` na versão instalada; offset 0 ainda tem o `+1` virtual, que reduz mas não elimina o ataque em todos os cenários (Inferido; a doc do OZ explica e não confirma o padrão da base) |
| Depósito inicial "morto" | O implantador deposita um valor relevante e queima as shares (para `address(0)` ou endereço sem chave) no deploy | Procurar o depósito inicial no script de deploy e no construtor |
| Verificação de mínimo de shares | `deposit` reverte se `shares == 0` ou se `shares < minShares` informado pelo usuário | `require`/erro na função; é defesa do usuário, não do cofre |
| Contabilidade interna de ativos | O cofre mantém `totalAssets` por contador próprio e ignora doações diretas | Procurar variável de contagem; cuidado com rebase e com ativos que mudam de saldo sozinhos |

Nota: o "depósito morto" e a contabilidade interna são práticas comuns do ecossistema, não verificadas nas fontes de V-10; rotule **Suposição** se citar em relatório sem ter lido a doc que as descreve.

## 4. Testes a propor (para `foundry-testing` executar)

Enunciados em linguagem natural (o usuário aprova antes de gerar código):

1. Round-trip: para qualquer `assets` no limite de `maxDeposit`, `redeem(deposit(assets))` devolve no máximo `assets`.
2. Inflação: um atacante deposita 1 wei, doa D ao cofre; uma vítima deposita V; a vítima, ao resgatar tudo, recebe pelo menos `V - perdaMaxima` (a perda máxima é definida pelo time: por exemplo, 1 wei por operação, ou 0,01 por cento do depósito).
3. Solvência: a soma de `convertToAssets(balanceOf(conta))` de todas as contas não excede `asset.balanceOf(cofre)` em nenhuma sequência de chamadas (invariante com handler).
4. `preview*` coerente: `previewDeposit(x)` não é maior que as shares que `deposit(x)` realmente emite.

Esqueleto do teste 2 (Foundry; ajuste nomes e decimals ao projeto):

```solidity
function test_inflation_victimKeepsValue() public {
    address attacker = makeAddr("attacker");
    address victim = makeAddr("victim");
    uint256 donation = 10_000e18;
    uint256 victimDeposit = 10_000e18;
    deal(address(asset), attacker, 1 + donation);
    deal(address(asset), victim, victimDeposit);

    vm.startPrank(attacker);
    asset.approve(address(vault), type(uint256).max);
    vault.deposit(1, attacker);                  // 1 wei de ativo
    asset.transfer(address(vault), donation);    // doação direta
    vm.stopPrank();

    vm.startPrank(victim);
    asset.approve(address(vault), type(uint256).max);
    vault.deposit(victimDeposit, victim);
    uint256 back = vault.redeem(vault.balanceOf(victim), victim, victim);
    vm.stopPrank();

    assertGe(back + MAX_LOSS, victimDeposit);    // MAX_LOSS definido pelo time
}
```

Resultado esperado: contra um cofre sem mitigação (offset 0 e sem depósito morto), o teste falha (a vítima recebe 0 ativos de volta); contra um cofre mitigado, passa. Registre a saída de `forge test` real; sem execução, escreva "teste proposto, não executado". Gotcha: `redeem` com zero shares pode reverter em algumas implementações (então o teste falha por revert, o que também indica o problema; registre qual).

## 5. O que registrar no relatório

- Versão do OZ lida e valor de `_decimalsOffset()` (ou a ausência dele).
- Se há depósito inicial no deploy (e quem o controla).
- Decimals do ativo: ativos com poucos decimals (6) tornam o arredondamento mais caro para a vítima em valores pequenos (Inferido).
- Quem usa o cofre como fonte de preço (outro protocolo): regra W3-VLT-04, aponte para `defi-oracle-l2-review`.
