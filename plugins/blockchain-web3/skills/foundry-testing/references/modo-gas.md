# Modo gas: otimização com evidência

Fontes: Foundry (gas-tracking), documentação do otimizador do Solidity, regra de evidência do repositório decipher-gas-optimizoor (7 estrelas, sem licença encontrada: só a regra foi aproveitada, sem texto nem hook) — tudo em V-23. Rótulos: **Verificado** = V-23; **Inferido** = detalhe de uso fora das páginas lidas.

IDs: `W3-GAS-01` antes e depois do mesmo teste; `-02` ganho mínimo acordado; `-03` sem trocar segurança por gás sem registro; `-04` `optimizer_runs` registrado.

## 1. Fluxo

1. Estabeleça a linha de base antes de mudar qualquer coisa:
   - `forge test --gas-report` (gás por função e por contrato);
   - `forge snapshot` (gera `.gas-snapshot` com o gás por teste).
2. Aplique uma mudança por vez.
3. Meça de novo com o **mesmo teste**: `forge snapshot --diff` mostra a diferença contra o `.gas-snapshot` anterior.
4. Em CI: `forge snapshot --check` falha se um teste passar a gastar mais (bom guarda-corpo contra regressão).
5. Cheatcodes para medir trechos: `vm.startSnapshotGas`/`vm.stopSnapshotGas` e `pauseGasMetering` (Verificado como existentes em V-23; confira a assinatura na versão instalada).
6. Registre: versão do Foundry, `optimizer`, `optimizer_runs`, `via_ir`, teste usado, gás antes e depois.

## 2. Regras de evidência

- Toda alegação de economia traz antes e depois do mesmo teste (`W3-GAS-01`). Sem medição, escreva "não medido".
- Ganho abaixo do limite acordado não entra (`W3-GAS-02`). O limite é decisão do time; o decipher usa 500 gás por salvamento e 100 gás no relatório como valores do projeto dele (V-23), não como regra universal.
- Otimização nunca troca segurança por gás sem registro (`W3-GAS-03`): `unchecked` só com prova do limite, remoção de verificação só com argumento escrito.
- `optimizer_runs` é uma estimativa de execuções do opcode ao longo da vida do contrato, não número de passes: valores altos favorecem custo de execução à custa de custo de deploy; escolha pelo perfil de uso e registre (`W3-GAS-04`).
- Medições de teste unitário não representam custo real em produção quando há cold/warm storage, calldata ou rede diferentes; diga isso quando a decisão for sensível.

## 3. Domínios de otimização (lista de trabalho, V-23)

Layout de storage (empacotar variáveis), laços (cache de `length`, saída antecipada), `calldata` em vez de `memory` em parâmetros externos de leitura, custo de deploy, tipos, erros customizados em vez de strings, `immutable`/`constant`, `unchecked` com prova de limite, visibilidade e eventos. Cada ideia vira uma mudança medida, não um pacote.

## 4. Exemplo de registro

```markdown
| Mudança | Teste | Antes (gás) | Depois (gás) | Delta | Segurança afetada? |
| calldata em batchTransfer(address[]) | test_batchTransfer | 184.220 | 181.905 | -2.315 | não (parâmetro somente leitura) |
| unchecked no incremento do laço | test_batchTransfer | 181.905 | 180.100 | -1.805 | não: i < len, len limitado por MAX_BATCH (prova) |
```

(Números ilustrativos do formato; os reais vêm de `forge snapshot --diff`.) Se o ganho ficar abaixo do limite acordado, a linha vai para "descartado por ganho insuficiente".

## 5. Limites

- Esta skill não otimiza sem teste que exercite a função.
- Não otimiza contrato com achado de segurança aberto no mesmo trecho antes de o achado ser tratado.
- Hooks que rodam `forge snapshot --diff` a cada salvamento (decipher) executam shell: estão documentados em `ferramentas-e-mcp.md` do playbook, desativados, e não fazem parte deste plugin.
