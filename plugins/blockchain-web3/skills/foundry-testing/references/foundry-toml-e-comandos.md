# foundry.toml e comandos de teste

Fontes: Foundry (invariant-testing, fuzz-testing, gas-tracking; V-02, V-23). Rótulos: **Verificado** = V-02/V-23 (chaves e comportamentos listados); **Inferido** = conhecimento estável do Foundry fora de VALIDATED; os valores numéricos dos blocos abaixo são **ilustrações, não recomendações**: a doc não indica valores ideais de `runs` e `depth` (V-02). Registre os que usar e por quê. Confira `forge --version` do projeto: recursos recentes variam por versão.

## 1. Bloco `[invariant]`

```toml
[invariant]
runs = 256              # ilustração: nº de sequências por invariante
depth = 128             # ilustração: chamadas por sequência
fail_on_revert = false  # decisão consciente: ver abaixo
shrink_run_limit = 5000 # Verificado como chave (V-02); valor ilustrativo
# check_interval, max_time_delay, max_block_delay: existem em versões recentes (V-02); confira a versão
```

Chaves registradas em V-02: `runs`, `depth`, `fail_on_revert`, `shrink_run_limit`, `check_interval`, `max_time_delay`, `max_block_delay`, além do modo de otimização (função que devolve `int256` a maximizar).

`fail_on_revert` (W3-TST-04): decida e documente quais reverts são esperados.
- `true`: qualquer revert do handler derruba o teste. Exige um handler que só produza entradas válidas (`bound`), mas mostra no mesmo instante que o handler está mal escrito.
- `false`: chamadas que revertem são descartadas. É o valor do exemplo da doc, que não o recomenda. O risco (Inferido) é a propriedade parecer coberta enquanto a maioria das chamadas falha; mitigue com contadores de chamadas bem-sucedidas.
Registre a decisão e o motivo no relatório e no template `especificacao-de-invariantes.md`.

## 2. Bloco `[fuzz]`

```toml
[fuzz]
runs = 256              # padrão de 256 execuções (Verificado em V-02)
max_test_rejects = 65536 # limite de entradas rejeitadas por vm.assume (nome da chave: Verificado; valor ilustrativo)
seed = "0x1"            # fixe a seed para reproduzir; varie em outras execuções
```

## 3. Otimizador e gás (referência para o modo gas)

```toml
[profile.default]
optimizer = true
optimizer_runs = 200    # ilustração; é uma estimativa de execuções ao longo da vida do contrato (V-23)
via_ir = false          # via-IR é um pipeline alternativo; teste os dois e meça
```

## 4. Segurança do `foundry.toml` ao ler repositório alheio

Procure e relate antes de rodar `forge test`:

```text
ffi = true                          # testes podem executar comandos de shell via vm.ffi
fs_permissions = [...]              # leitura/escrita de arquivos por cheatcodes
[rpc_endpoints] com URLs literais   # podem conter chave de provedor: não imprima, não copie
```

`ffi` pode também vir de flag (`--ffi`) ou variável de ambiente; na dúvida, pergunte. `forge build` não executa `vm.ffi`, mas `forge test` e scripts podem. Em repositório de terceiros ou não revisado, peça confirmação do usuário antes de rodar testes (Inferido).

## 5. Comandos de uso diário

| Objetivo | Comando |
|---|---|
| Versão | `forge --version` |
| Compilar | `forge build` |
| Todos os testes | `forge test` |
| Só invariantes | `forge test --match-test invariant_ -vvv` |
| Reproduzir sequência de falha | `forge test --match-test invariant_<nome> -vvvv` |
| Só um contrato | `forge test --match-contract VaultInvariants` |
| Relatório de gás | `forge test --gas-report` |
| Linha de base de gás | `forge snapshot` (gera `.gas-snapshot`) |
| Comparar gás | `forge snapshot --diff` |
| Falhar se piorar (CI) | `forge snapshot --check` |

Nunca no repertório desta skill: `cast send`, `forge create`, `forge script ... --broadcast`, e qualquer comando com chave privada em linha de comando. Se o usuário pedir, recuse a execução, prepare o comando sem chave e pare (ele roda no terminal dele).

## 6. O que registrar em cada execução

```text
Foundry: <saída de forge --version>
Comando: forge test --match-test invariant_ -vvv
Config:  runs=<..> depth=<..> fail_on_revert=<..> seed=<..>
Resultado: <passou/falhou por invariante> ; testes executados: <N>
Contadores do handler: <função: chamadas>
```
