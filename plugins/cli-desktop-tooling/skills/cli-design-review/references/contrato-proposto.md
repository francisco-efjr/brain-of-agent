# Contrato proposto de CLI (modelos para colar no relatório)

Verificado em 2026-10-10 contra V-13 e V-64. Tudo aqui é modelo ilustrativo: nenhum trecho foi executado. O código `3` para "não encontrado" segue o `show` do Azure CLI (V-64); os demais códigos são proposta da fábrica (Inferido) e devem seguir o que o projeto já publica.

## Tabela de exit codes (modelo)

| Código | Significado | Quando usar |
| --- | --- | --- |
| 0 | Sucesso | Operação concluída; também "nada a fazer" quando for idempotente |
| 1 | Falha genérica | Erro inesperado de execução |
| 2 | Uso incorreto | Flag inválida, argumento faltando, `--no-input` sem as flags necessárias |
| 3 | Não encontrado | `show` ou `delete` de recurso inexistente |
| 4 | Conflito ou pré-condição | Recurso já existe quando `create` não é idempotente; versão divergente |
| 130 | Interrompido | Ctrl+C (convenção de shells POSIX; conferir no Windows) |

Regra: documente a tabela em `--help` e no README, e mude só com versão maior e nota de migração (V-64).

## Esquema JSON estável (modelo)

`show --json` devolve um objeto na raiz; `list --json` devolve um objeto com a lista dentro de uma chave, para poder acrescentar campos (paginação) sem quebrar quem consome:

```json
{
  "schema_version": 1,
  "items": [{ "id": "abc123", "name": "build-linux", "state": "ready" }],
  "next_page": null
}
```

Erros com `--json` vão para stderr, também como objeto, mantendo stdout vazio:

```json
{ "error": { "code": "not_found", "message": "pacote 'abc' não encontrado", "hint": "pkgctl list --filter name=abc" } }
```

Evite devolver string ou booleano solto na raiz (V-64) e evite campos cujo tipo muda entre versões.

## Mensagem de erro acionável (modelo)

Estrutura: problema, causa, correção, exemplo de uso (V-11, V-13, V-64).

```text
erro: falta confirmação para remover 'build-linux' (stdin não é um terminal)
dica: repita com --yes para confirmar sem perguntar, ou --dry-run para ver o que seria removido
uso:  pkgctl remove <nome> [--yes] [--dry-run]
```

Falhar assim, em vez de perguntar, evita que agentes e pipelines fiquem pendurados (V-12).

## `--help` com exemplos primeiro (modelo)

```text
pkgctl remove: remove um pacote do registro local

Exemplos:
  pkgctl remove build-linux --dry-run     mostra o que seria removido
  pkgctl remove build-linux --yes         remove sem perguntar

Opções:
  --yes        confirma sem perguntar (obrigatório sem terminal)
  --dry-run    não altera nada; lista o efeito
  --json       resultado como objeto JSON
```

Descrição de flag em minúscula, curta e sem ponto final é estilo do Heroku (sinal C, V-64): adote só se o projeto não tiver convenção própria.

## Teste de contrato (exemplo ilustrativo em Python com pytest)

Fixa stdout, stderr e exit code. Adapte à linguagem do projeto; a ideia é testar o processo como o chamador o vê.

```python
import json
import subprocess
import sys


def run(*args):
    return subprocess.run(
        [sys.executable, "-m", "pkgctl", *args],
        capture_output=True, text=True, stdin=subprocess.DEVNULL,
    )


def test_show_inexistente_sai_com_3_e_erro_em_stderr():
    r = run("show", "nao-existe", "--json")
    assert r.returncode == 3
    assert r.stdout == ""
    assert json.loads(r.stderr)["error"]["code"] == "not_found"


def test_remove_sem_tty_e_sem_yes_falha_rapido_listando_a_flag():
    r = run("remove", "build-linux")
    assert r.returncode == 2
    assert "--yes" in r.stderr
```

Com `stdin=subprocess.DEVNULL` o segundo teste prova que a CLI não trava esperando entrada.

## Perguntas para a conversa com o autor da CLI

1. Já existe versão publicada com exit codes ou JSON consumidos por terceiros?
2. Quem chama a CLI em script ou CI, e com qual shell (PowerShell 5.1, Git Bash)?
3. Há operação longa que hoje bloqueia o chamador?
4. Algum comando apaga ou sobrescreve dados do usuário?
