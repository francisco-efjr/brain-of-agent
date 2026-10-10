# Ferramentas, hooks e MCP recomendados (todos desativados)

Nada aqui vem ativo no plugin: não há `hooks/hooks.json`, `.mcp.json`, `.lsp.json` nem `bin/`, e o plugin nunca escreve `settings.json`. Este arquivo documenta o que vale habilitar **conscientemente** no seu projeto, com JSON pronto, riscos e o que foi ou não verificado. Instalar ou executar qualquer item é decisão sua. O plugin não traz comandos de instalação: instaladores de terceiros usam `curl … | bash` e scripts que editam configuração; abra a página oficial de cada projeto, leia o instalador antes de rodar e fixe a versão. Conferido em 2026-10-10 (itens V em [fontes.md](fontes.md)).

## Sumário

- [Regras de adoção](#regras-de-adoção)
- [T-01 Foundry](#t-01-foundry)
- [T-02 Slither](#t-02-slither)
- [T-03 Echidna e Medusa](#t-03-echidna-e-medusa)
- [T-04 Verificação formal](#t-04-verificação-formal)
- [T-05 Plugin de upgrades do OpenZeppelin](#t-05-plugin-de-upgrades-do-openzeppelin)
- [T-06 Permissões do projeto (JSON)](#t-06-permissões-do-projeto-json)
- [T-07 Hook PreToolUse de guarda](#t-07-hook-pretooluse-de-guarda)
- [T-08 Hook de gás](#t-08-hook-de-gás)
- [T-09 MCP e indexação: o que não recomendar](#t-09-mcp-e-indexação-o-que-não-recomendar)
- [Windows](#windows)

## Regras de adoção

1. Leia o código e a licença antes de executar qualquer pacote de terceiros; fixe a versão (nunca `latest`/`master`).
2. Hook roda shell com as suas permissões: revise como revisaria um PR. Hook é guardrail, não fronteira de segurança.
3. Teste de exploração só em fork local; credenciais fora do agente; RPC por variável de ambiente.
4. Confirme sintaxe na versão instalada (`/permissions`, `/hooks`, `forge --help`): nomes mudam.
5. Ferramenta AGPL (Slither, Echidna): usar como ferramenta é permitido; **copiar código ou texto para o plugin, não**.

## T-01 Foundry

| Item | Detalhe |
| --- | --- |
| Uso | `forge` (build, test, fuzz, invariantes, fork, snapshot de gás), `cast`, `anvil` |
| Quem instala/roda | Usuário; instalação pela página oficial https://getfoundry.sh |
| Licença | Apache-2.0 (repositório, consultado em 2026-10-10) |
| Risco | Instaladores de terceiros usam `curl … \| bash`. `cast send`, `forge create` e `forge script --broadcast` movem fundos: negados por deny/hook ([T-06](#t-06-permissões-do-projeto-json)). `ffi = true` faz testes executar programas do repositório. Versão afeta recursos (`check_interval`, modo de otimização) |
| Comandos que o plugin usa | `forge build`, `forge test`, `forge snapshot` (e `--diff`/`--check`), `forge test --gas-report` |
| Fonte | V-02, V-23, V-04 |

`forge script`, keystore (`--account`), `anvil --fork-url` e `forge verify` não foram validados (lacuna L10): o plugin não detalha fluxos de deploy; só a política de recusa.

## T-02 Slither

Análise estática da Trail of Bits (AGPL-3.0). README: 100 detectores; `slither .` na raiz de projetos Hardhat/Foundry/Dapp/Brownie; `--checklist` gera relatório em Markdown; `--print` com printers (`human-summary`, `inheritance-graph`, `contract-summary`, `loc`, `entry-points`, `call-graph`, `cfg`, `function-summary`, `vars-and-auth`, `not-pausable`); API Python para detectores; integra com CI; Solidity ≥ 0.4 e Vyper.

Fluxo (desenho próprio): compilar → `slither .` filtrando `lib`, `test` e `mock` e guardando a saída na pasta de auditoria → ler o código de cada achado de alto impacto → classificar (real: precisa de PoC; falso positivo: motivo; risco aceito: motivo e dono) → comparar com a rodada anterior. **Relatório vazio não é "sem bugs"**: registre limites de cobertura. Quem instala e executa é o usuário; o plugin não pré-aprova `Bash(slither *)`. Fonte: V-12.

## T-03 Echidna e Medusa

Echidna (AGPL-3.0): propriedades `echidna_` com retorno booleano, modos de asserção, integração com Foundry e otimização (README). Medusa: **não lido** (lacuna L7); mencionar como "a avaliar". Complementam o `foundry-testing`; não são necessários para o fluxo do plugin. Fonte: V-26.

## T-04 Verificação formal

Halmos, Certora e similares: **Não verificável** (não lidos). Mencione apenas como "a avaliar" quando o usuário pedir provas formais; nenhuma recomendação do plugin depende deles.

## T-05 Plugin de upgrades do OpenZeppelin

Validação de layout de storage entre versões (UPG-03). A página não informa a versão do plugin: confirme a compatibilidade com o OpenZeppelin instalado. O usuário executa; o resultado entra no relatório com o comando e a saída. Fonte: V-09.

## T-06 Permissões do projeto (JSON)

Aplicado **pelo usuário** em `.claude/settings.json`. Sintaxe dos padrões de Bash e a chave `disableBypassPermissionsMode` dentro de `permissions` são **Inferidas** a partir da documentação (Verificado: regras `Read(...)` de deny, `permissions.disableBypassPermissionsMode` com `"disable"`, hook `PreToolUse` não sobrepõe deny). Valide com `/permissions` na versão instalada.

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)", "Read(./.env.*)", "Read(./secrets/**)", "Read(./keys/**)",
      "Bash(cast send *)", "Bash(forge create *)", "Bash(*--broadcast*)"
    ],
    "allow": [
      "Bash(forge build *)", "Bash(forge test *)",
      "Bash(git diff *)", "Bash(git status *)", "Bash(git log *)"
    ],
    "disableBypassPermissionsMode": "disable"
  }
}
```

Notas:

1. O deny de Bash **não** casa caminho absoluto nem `sh -c '…'`: mantenha sandbox de rede limitado ao RPC usado em fork e a chave fora do alcance do agente.
2. `.claudeignore` não tem efeito para bloquear leitura.
3. `disableBypassPermissionsMode` vale em qualquer escopo; é mais útil em managed settings.
4. Hook `PreToolUse` não sobrepõe regras de deny/ask.
5. `Bash(slither *)` fica fora da allowlist de propósito: o Slither compila o projeto e pode acionar o build do framework (por exemplo Hardhat, que executa a configuração JavaScript do repositório; Inferido). Se você usa Slither em repositório confiável, adicione a regra por sua conta e risco ou aprove cada execução.
6. `forge snapshot` não está nessa allowlist (Inferido): adicione `Bash(forge snapshot *)` se usar o modo `gas`.
7. Skills e agentes do plugin declaram `allowed-tools` como pré-aprovação; se a versão instalada também os restringe é **Não verificável aqui**: não dependa disso.

## T-07 Hook PreToolUse de guarda

Desenho (V-05): hooks são comandos de shell; `PreToolUse` com `exit 2` bloqueia a chamada e a mensagem de stderr volta ao Claude; com vários hooks vale a decisão mais restritiva. O exemplo oficial do guia usa matcher `Edit|Write` para `.env`; o caso `Bash` e os nomes dos campos de stdin abaixo são desenho próprio (**Inferido**). Python stdlib; o usuário copia para `.claude/hooks/web3_guard.py` depois de revisar.

```python
#!/usr/bin/env python3
"""web3_guard: bloqueia leitura/edição de segredos e comandos que movem fundos."""
import json, re, sys

data = json.load(sys.stdin)
tool = data.get("tool_name", "")
args = data.get("tool_input", {}) or {}
alvo = args.get("file_path", "") if tool in ("Edit", "Write", "Read") else args.get("command", "")

padroes = [
    r"(^|[\\/])\.env(\.|$)", r"\.key$", r"keystore",
    r"--broadcast", r"\bcast\s+send\b", r"\bforge\s+create\b", r"--private-key",
]
# scripts de deploy: leitura é livre (a auditoria precisa lê-los); edição fica com o usuário
if tool in ("Edit", "Write"):
    padroes.append(r"script[\\/]Deploy.*\.s\.sol$")
for p in padroes:
    if re.search(p, alvo or "", re.IGNORECASE):
        print("Bloqueado pela regra web3_guard: ação reservada ao usuário (segredo ou transação).", file=sys.stderr)
        sys.exit(2)
sys.exit(0)
```

Configuração (o usuário insere em `.claude/settings.json`; **Inferido**, valide com `/hooks`):

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Edit|Write|Read|Bash",
        "hooks": [ { "type": "command", "command": "python3 .claude/hooks/web3_guard.py" } ] }
    ]
  }
}
```

Riscos: executa shell com as suas permissões; regex não é scanner (comando ofuscado passa); hooks assíncronos em modo bypass podem rodar antes do bloqueio (relato, sinal C). Em Windows o comando pode ser `python` em vez de `python3` (Suposição). Defesa principal: deny + sandbox + assinatura fora do agente.

## T-08 Hook de gás

Ideia (V-23): rodar `forge snapshot --diff` a cada salvamento de `.sol` e alertar regressão acima de um limite. Origem sem licença (repositório `decipher-gas-optimizoor`): **só o conceito**, nenhum código copiado. Risco: roda shell a cada salvamento. Alternativa mais segura: `forge snapshot --check` no CI.

## T-09 MCP e indexação: o que não recomendar

| Item | Decisão |
| --- | --- |
| MCPs de análise de contratos (weasel, solidity-audit-mcp) | **Não recomendar**: 30★ e 3★, instalação por `curl`/dependências, não reverificados |
| plamen, proofhound, Demeter e similares | **Não instalar nem referenciar a instalação** (editam `settings.json`, registro, `~/.claude`; `--break-system-packages`) |
| The Graph, Ponder, Envio (indexação) | Lacuna L2: sem política de reorg/finalidade validada |
| Hardhat | Lacuna L3: sem fonte validada |
| `trailofbits/skills` | CC-BY-SA-4.0: o usuário pode instalar por conta própria pelas instruções do repositório; este plugin não copia texto |

## Windows

O dono do repositório usa Windows 11. Instalação e comportamento de Foundry e Slither em Windows são **Não verificáveis aqui** (lacuna L15). Consulte a página oficial do projeto para o seu sistema (WSL pode ser necessário: **Suposição**). O avaliador de plugins (`claude plugin eval`) pode ter requisito próprio em Windows (WSL2, segundo o plugin irmão `qa-testing`): confira na documentação da versão instalada.
