# Design de CLI para humanos e para agentes

Sumário: 1. Contrato em uma tabela · 2. Streams e exit codes · 3. Ajuda e descoberta · 4. Entrada: flags, argumentos, TTY · 5. Saída: humano, `--json`, `--plain`, cor · 6. Configuração e segredos · 7. Destrutivo, idempotência e operações longas · 8. Nomes e verbos · 9. Erros acionáveis · 10. CLI pronta para agente · 11. Distribuição e teste de contrato (Inferido) · 12. Exemplos · 13. O que a fábrica acrescentou

Fontes: V-13 (clig.dev), V-64 (Azure CLI; Heroku e Atlassian são sinal C), V-11 (ferramentas para agentes), V-12 (Ronacher). A extensão do guia de ferramentas MCP (V-11) para CLI é Inferido. Rótulos: Verificado = está na fonte; Inferido = dedução da fábrica; Suposição = a confirmar com o usuário.

## 1. Contrato em uma tabela

| Tema | Regra | Por que | Fonte |
| --- | --- | --- | --- |
| Streams | Resultado em `stdout`; log, progresso, aviso e erro em `stderr` | Quem faz pipe só quer o resultado | V-13, V-64 |
| Exit code | 0 em sucesso, não zero em falha, códigos distintos e documentados | Scripts e CI decidem pelo código | V-13 |
| Não encontrado | Código próprio para "recurso não existe" (o `show` do Azure CLI usa 3) | Automação distingue erro de ausência | V-64 |
| `--json` | Objeto estável (nunca string ou booleano solto); `--plain` para texto simples | Compatibilidade de quem automatiza | V-13, V-64 |
| Cor | Desligada sem TTY e com `NO_COLOR` definido; flag `--no-color` | Logs e pipes ficam legíveis | V-13, V-64 |
| Prompt | Nunca perguntar sem TTY; `--no-input` falha listando as flags que faltaram | Agente e CI ficam pendurados | V-13, V-12 |
| Confirmação | Proporcional ao risco; todo prompt contornável por `--yes` ou `--force` | Humano seguro, script possível | V-13, V-64 |
| Segredo | Nunca por flag; nas CLIs que escrevemos, também não por variável de ambiente: arquivo com permissão restrita, stdin ou store do sistema | Argumentos vão para listas de processo e logs | V-13 |
| Ajuda | `--help` com exemplos primeiro; toda flag com descrição | Descoberta sem sair do terminal | V-13, V-64 |
| Velocidade | Primeira resposta rápida (clig.dev cita 100 ms como meta) | Travar é pior que quebrar | V-13, V-12 |
| Estabilidade | Nome de flag, exit code e formato de saída só mudam com versão e nota de migração; depois de GA, não quebrar entradas e saídas | Quem automatiza quebra em silêncio | V-64 (Heroku, sinal) |

## 2. Streams e exit codes

Proposta de tabela (a fábrica propõe; só o código 3 vem de fonte, V-64; o 2 para uso inválido é convenção estável de muitos parsers, como `argparse`, Inferido):

| Código | Significado | Quando |
| --- | --- | --- |
| 0 | Sucesso | Operação concluída, inclusive "nada a fazer" quando documentado |
| 1 | Falha geral | Erro de execução sem categoria própria |
| 2 | Uso inválido | Flag desconhecida, argumento faltando, combinação proibida |
| 3 | Não encontrado | `show` ou `get` de recurso inexistente |
| 4 a 9 | Reservados | Categorias do projeto (rede, permissão, conflito) documentadas no `--help` |

Regras: erro nunca sai com 0; aviso que não impede o resultado sai com 0 e vai para `stderr`; código documentado no `--help` ou na página de manual; testes fixam o código de cada caminho (seção 11). Defina também o que `Ctrl+C` faz (código e limpeza); SIGTERM sem tratamento sai com 143 em muitos runtimes, Inferido (V-09 cita 143 para o `claude -p`).

## 3. Ajuda e descoberta

- `--help` e `-h` em todo nível; `--version` com a versão publicada.
- Estrutura: uso em uma linha, descrição curta, exemplos reais (dois ou três, copiáveis), depois lista de comandos e flags. Heroku (sinal) pede descrição em minúscula, até 80 colunas, sem ponto final (V-64).
- Erro de uso mostra a linha de uso e um exemplo, não o manual inteiro.
- Sugira o próximo passo ao fim de uma operação (Atlassian, sinal C, V-64).

## 4. Entrada: flags, argumentos, TTY

- Prefira flags a argumentos posicionais quando houver mais de um valor (Heroku, Atlassian: sinal C). Unidades fora do nome do argumento (`--timeout 30s`, aceitar sufixos como `1h`) (V-64).
- Proibido JSON bruto como parâmetro: exponha as propriedades como flags (V-64).
- Detecte TTY: sem TTY, não pergunte. Em Python: `sys.stdin.isatty()` e `sys.stdout.isatty()`; em Go, `term.IsTerminal`; em Rust, `std::io::IsTerminal` (conhecimento estável, Inferido; confira na versão da linguagem).
- Aceite `-` como "ler de stdin" para arquivos (convenção estável, Inferido).

## 5. Saída: humano, `--json`, `--plain`, cor

- Padrão humano: curto, legível, tabela só se couber em 80 colunas; amigável a `grep` (Heroku, sinal).
- `--json`: sempre objeto no topo, campos estáveis, listas dentro de um campo (`{"items": [...], "next": null}`), sem texto misturado no `stdout`. Operações que devolvem o recurso (`create`, `update`) o imprimem.
- `--plain`: uma linha por registro, campos separados por tab, sem cor.
- Progresso e spinner só em TTY e em `stderr`.
- Verbosidade: `--quiet`, `--verbose`; para agentes, modo `concise` e `detailed` (V-11): o padrão curto poupa tokens, o detalhado traz identificadores e metadados.
- Listas: limite padrão, paginação e dica de filtro quando truncar (V-11). O limite de 25.000 tokens citado em V-11 é do Claude Code, não de CLIs: use como ordem de grandeza do que cabe numa resposta de ferramenta, nunca como regra de CLI.

## 6. Configuração e segredos

- Precedência (maior para menor): flags, variáveis de ambiente, configuração do projeto, do usuário, do sistema (V-13). Siga XDG no Linux (V-13); no Windows use `%APPDATA%` ou `%LOCALAPPDATA%` (Inferido).
- Segredo: não ler de variável de ambiente nas CLIs que escrevemos (V-13) nem de flag; use arquivo com permissão restrita, stdin ou store do sistema. Exceção declarada: segredos de assinatura injetados pelo cofre do CI (por exemplo `TAURI_SIGNING_PRIVATE_KEY`, V-20) são o padrão documentado daquela ferramenta; não os trate como violação em revisão.
- Nunca imprima segredo em log, `--verbose` ou mensagem de erro; mascare.

## 7. Destrutivo, idempotência e operações longas

- Apagar, mover, publicar e sobrescrever exigem flag explícita e, em TTY, confirmação proporcional (digitar o nome do recurso para ações graves) (V-13).
- `--dry-run` mostra o que mudaria sem mudar (V-25, V-28 usam o padrão; em PowerShell é `-WhatIf`, ver `scripts-powershell-e-shell.md`).
- `create` é idempotente e devolve o recurso; `update` age como PATCH; `set` substitui tudo; `delete` não devolve nada (V-64).
- Operação longa: `--no-wait` devolve na hora e existe o comando `wait` (V-64).
- Execução duplicada: pidfile ou lock responde "já rodando" em vez de abrir um segundo processo (V-12).

## 8. Nomes e verbos

Estrutura `[substantivo] [verbo]` com verbo em todo comando; subgrupos com hífen; evite subgrupo que só contém subgrupos (V-64). Verbos com semântica fixa: `create`, `update`, `set`, `show`, `list` (um comando só), `delete`, `wait`. O mesmo conceito tem o mesmo nome em toda a CLI. Para agentes, nome inequívoco com prefixo do recurso e parâmetros sem ambiguidade (`--user-id`, não `--user`); prefixo contra sufixo muda por modelo e deve ser medido com o modelo-alvo (V-11).

## 9. Erros acionáveis

Formato: problema, causa provável, correção, exemplo de uso correto (V-11, V-13, V-64). Vai para `stderr`, com exit code não zero, sem stack trace por padrão (use `--verbose` ou `--debug`).

Antes:

```text
Erro: invalid value
```

Depois:

```text
erro: --format 'yaml' não é suportado (valores aceitos: json, plain, table).
uso:  mytool export --format json --output relatorio.json
dica: mytool export --help
```

Quando faltar dado sem TTY: `erro: faltam --dest e --yes para rodar sem terminal interativo.` com o comando completo sugerido.

## 10. CLI pronta para agente (V-11, V-12, extensão Inferido)

Checklist (cada item é verificável por leitura de código ou por `--help` colado):

- [ ] cada subcomando faz uma coisa, com nome inequívoco
- [ ] saída padrão curta; `--json` estável; modo `concise` e `detailed`
- [ ] listas limitadas ou paginadas, com dica de filtro
- [ ] erro diz o que faltou e mostra o uso correto
- [ ] nenhum prompt sem TTY; toda confirmação tem `--yes`
- [ ] ação destrutiva exige flag explícita
- [ ] execução duplicada bloqueada (pidfile ou lock)
- [ ] serviços escrevem log em arquivo que o agente lê; o caminho é fixo e documentado no `CLAUDE.md` (sugestão da fábrica, Inferido: Ronacher não trata de timeouts nem fixa o caminho do log, V-12)
- [ ] operações idempotentes ou com `--dry-run`
- [ ] testada com uma tarefa real de vários passos, lendo a transcrição (V-11)

Heurística, não norma: CLI simples e log em arquivo antes de MCP no ciclo local (V-12, B); MCP onde a alternativa é pouco confiável (C-6 em `fontes.md`).

## 11. Distribuição e teste de contrato (Inferido; sem item V, lacuna 14)

- `--version` igual à versão publicada.
- Teste de contrato que fixa `stdout`, `stderr` e exit code de cada caminho (snapshot da ajuda e dos erros).
- Completions de shell e canal de instalação (winget, gerenciador da linguagem, binário único) declarados no README. Não recomende ferramenta específica sem fonte; para winget veja V-43 em `distribuicao-assinatura-update.md`.
- Desinstalação documentada ao fim das instruções de instalação (V-13).
- Telemetria só com opt-in e documentada (conhecimento estável, Inferido).

## 12. Exemplos

Revisão de trecho (Python), achado por achado:

```python
dest = input("Destino do backup: ")
if input("Apagar backups antigos? (s/n) ") == "s":
    delete_old(dest)
print("Backup ok!!!")
sys.exit(0)  # sempre
```

| ID | Severidade (Inferido) | Evidência | Correção |
| --- | --- | --- | --- |
| CLI-04 | Alta | `input()` sem checar TTY trava em agente e CI | `--dest` e `--no-input`; sem TTY e sem flag, erro listando as flags |
| CLI-17 | Alta | Apagar sem `--yes` | `--delete-old` explícito mais `--yes`; `--dry-run` |
| CLI-02 | Alta | `sys.exit(0)` sempre | Código por caminho, documentado |
| CLI-03 | Alta | Erro e status em `stdout` | Erros em `stderr` |

## 13. O que a fábrica acrescentou (não é das fontes)

Timeout padrão, caminho de log fixo, tabela de exit codes além do código 3, bloco F e a regra de segredo "nem por variável de ambiente" (a regra é do clig.dev, V-13; a exceção do cofre de CI é da fábrica). Se o usuário discordar, siga a convenção do repositório.
