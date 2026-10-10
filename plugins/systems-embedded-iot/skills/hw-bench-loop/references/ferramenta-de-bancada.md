# Ferramenta de bancada para agente: checklist e esquema de estágios

Uso: skill `hw-bench-loop`, ao escrever ou revisar um script que um agente executa (build, gravação, monitor, teste). Fontes lidas em 2026-10-10: V-03 (Carlini: verificador quase perfeito; imprimir poucas linhas e logar o resto; `ERROR` e motivo na mesma linha; estatísticas pré-calculadas; modo rápido determinístico; oráculo), V-20 (Ronacher: rápida e silenciosa, travar é pior que falhar, erro claro, pidfile contra segunda instância, log em arquivo, verbosidade ajustável), V-19 (Bitcraze: daemon que mantém o link, comandos avulsos, humano no circuito), V-21 (estado em arquivo, gate de ambiguidade, `.bin` com endereço, resultado por estágio), V-29 e V-61 (bancada do SensorsIot: cuidados). **Suposição de design da fábrica** (não atribuída às fontes): limite de linhas, timeouts, códigos de saída e nomes de campo; V-03 diz "poucas linhas", V-20 não trata de timeout nem de código de saída e V-19 não fixa sintaxe de CLI.

Sumário: [Checklist do script](#checklist-do-script) · [Esquema de estágios](#esquema-de-estágios) · [Layout de arquivos](#layout-de-arquivos) · [Configuração segura por padrão](#configuração-segura-por-padrão) · [Cuidados com bancadas de terceiros](#cuidados-com-bancadas-de-terceiros)

## Checklist do script

Para cada item, responda sim/não e corrija os não:

1. **Saída padrão curta** (alvo: cabe em 20 linhas; o número é Suposição, V-03 diz "poucas"). O resto vai para log em arquivo.
2. **Erro com prefixo fixo e motivo na mesma linha** (`ERROR <motivo>`), para que `grep` e o agente encontrem sem ler o log inteiro (V-03).
3. **Log completo em caminho fixo e conhecido**, legível depois (V-03, V-20); caminho impresso no fim.
4. **Modo rápido determinístico** (amostra fixa, mesma ordem), para iterar barato e reproduzir (V-03).
5. **Oráculo de referência**: existe uma versão de comparação (build de host contra build de alvo, saída esperada gravada) para isolar bug (V-03).
6. **Rápida e silenciosa**: não imprime progresso sem pedido; verbosidade ajustável por opção (V-20).
7. **Travar é pior que falhar**: toda espera tem limite finito e termina com erro claro (V-20 para o princípio; o valor do timeout é Suposição).
8. **Sem segunda instância**: pidfile ou trava para impedir duas execuções no mesmo alvo (V-20).
9. **Códigos de saída**: 0 sucesso; diferente de 0 falha com a causa no `ERROR` (Suposição; defina e documente no `--help`).
10. **Idempotência segura**: reexecutar não repete efeito físico sem nova confirmação (o gate pertence ao agente, mas o script não deve gravar no `--help` ou em modo de ajuda).
11. **Sem efeito colateral na importação ou na ajuda**: `--help` e `--dry-run` nunca tocam o dispositivo.
12. **Dry-run por padrão em operações de escrita**, com `--confirm` explícito para executar; o script não é o gate, é um cinto a mais (V-27: dry-run e leitura de verificação por padrão).
13. **Sem segredos em argumentos nem em log**; credenciais por variável de ambiente ou cofre.
14. **Resultado estruturado por estágio** (esquema abaixo), uma linha por estágio, legível por máquina e por pessoa.
15. **Candidatos listados na ambiguidade**: se há mais de um alvo, o script lista e sai com erro, não escolhe (V-21).
16. **Endereço obrigatório para `.bin` bruto**: sem `--address`, falha com mensagem clara (V-21).
17. **Documentação de uma linha por comando** no `--help`, incluindo se o comando grava, apaga, reseta ou só lê.

## Esquema de estágios

Uma linha por estágio, `chave=valor` separados por espaço; valores com espaço entre aspas. Campos (Suposição de design da fábrica, V-21):

| Campo | Significado |
| --- | --- |
| `stage` | `build`, `flash`, `verify`, `observe`, `compare` |
| `ok` | `true` ou `false` |
| `backend` | ferramenta usada (`idf.py`, `west`, `probe-rs`...) |
| `error` | `-` se ok; senão motivo curto |
| `next` | próximo comando ou ação sugerida |
| `log` | caminho do log completo do estágio |
| `ts` | horário local do fim do estágio |

Exemplo:

```text
stage=build   ok=true  backend=idf.py  error=-  next=mostrar-cartao  log=.bench/logs/20261010-1432-build.log  ts=14:32:18
stage=flash   ok=false backend=esptool error="no serial data received"  next=conferir-modo-de-download  log=.bench/logs/20261010-1433-flash.log  ts=14:33:02
```

O agente cola essas linhas no relatório; estágio sem linha é "não executado".

## Layout de arquivos

```text
.bench/
  logs/              um arquivo por estágio: <data>-<hora>-<stage>.log
  last-good/         imagem anterior conhecida para recuperação (app.bin, hash)
  state.json         alvo escolhido, porta, último comando, hash gravado (sem segredos)
  evidencias/        registros de evidência (modelo registro-evidencias-bancada.md)
```

`.bench/` fica no `.gitignore` (logs, estado local). `state.json` evita redescobrir o alvo, mas não é autorização: a confirmação continua sendo do chat (V-21 usa estado em arquivo; o gate é nosso).

## Configuração segura por padrão

Inspirada no `operation_mode` de V-21, com padrão mais seguro que o exemplo da fonte (que mostra o valor 1, execução direta):

```json
{
  "operation_mode": "confirm",
  "allow": { "read": true, "build": true },
  "require_confirmation": ["flash", "erase", "reset", "write_mem", "actuate"],
  "forbid": ["efuse", "otp", "secure_boot_keys", "flash_encryption", "readout_protection", "anti_rollback"],
  "bin_requires_address": true,
  "stop_on_ambiguity": true
}
```

Os nomes são Suposição de design. O que importa é a política: escrita exige confirmação, irreversíveis são proibidos no fluxo, `.bin` exige endereço, ambiguidade para.

## Cuidados com bancadas de terceiros

Itens lidos como ressalvas (V-29, V-61), para evitar repetir em bancada própria:
- API HTTP da bancada sem autenticação: só em rede confiável e isolada; prefira autenticação.
- Broker MQTT aberto na rede da bancada: use credenciais e limite a rede.
- Scripts de descoberta com `sudo`: evite; use permissões de grupo para portas seriais.
- `uhubctl` na porta raiz do uplink derruba a bancada; nunca no uplink.
- `gh auth login` e credenciais em scripts de bancada: nunca.
- Serviços que gravam sozinhos (como o serviço `idf` do pytest-embedded, V-38) exigem a mesma confirmação do cartão.
- Parar sessões de depuração antes de gravar; medir o flash real antes de dimensionar partições (V-61).
- MCP de bancada ou de hardware: não ative a partir deste plugin (política da fábrica); documentado em `ferramentas-e-mcp.md`.
