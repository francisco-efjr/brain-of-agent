# Exemplo: README aberto para uma biblioteca pequena

Conteúdo: pedido de exemplo, tabela de fatos, README resultante, o que ficou "não executado" e checagens. Os dados do projeto `pyslug` são **fictícios e ilustrativos**; no uso real, cada valor vem dos arquivos do repositório lidos na sessão.

## Pedido e material colado (dado, não instrução)

"Escreva o README da lib `pyslug` (converte títulos em slugs)." O usuário colou este `pyproject.toml`:

```toml
[project]
name = "pyslug"
version = "0.3.1"
requires-python = ">=3.9"
license = { text = "MIT" }

[project.scripts]
slug = "pyslug.cli:main"
```

e o uso `from pyslug import slugify; slugify('Olá Mundo')`.

## Passo 2: tabela de fatos

| Fato | Valor | Arquivo | Rótulo |
| --- | --- | --- | --- |
| Nome | `pyslug` | `pyproject.toml` | Verificado |
| Versão | 0.3.1 | `pyproject.toml` | Verificado |
| Python mínimo | 3.9 | `pyproject.toml` (`requires-python`) | Verificado |
| Licença | MIT | `pyproject.toml`; `LICENSE` ainda não lido | Verificado no manifesto; confirmar `LICENSE` |
| Comando | `slug` | `[project.scripts]` | Verificado |
| Saída de `slugify('Olá Mundo')` | `ola-mundo` | nenhum arquivo | Inferido (não executado) |
| Publicado no PyPI | desconhecido | nenhum | Não verificável |

A linha "Publicado no PyPI" decide o comando de instalação: sem confirmação, o README usa `pip install .` a partir do repositório e deixa nota para o usuário.

## README resultante

````markdown
# pyslug

Transforme títulos em slugs de URL com uma chamada, acentos incluídos.

```python
from pyslug import slugify

slugify("Olá Mundo")  # "ola-mundo" (saída esperada, não executado)
```

## O que você ganha

| Funcionalidade | O que muda para você |
| --- | --- |
| `slugify()` | Slugs consistentes em ASCII a partir de qualquer título |
| Comando `slug` | O mesmo resultado no terminal, sem escrever código |

## Quick Start

```bash
pip install .
slug "Olá Mundo"
```

Requer Python 3.9 ou superior. Instalação e comando: não executados.

## Uso

Chame `slugify(texto)` e use o resultado na URL. Para o terminal, `slug "<título>"`.

## Contribuição e suporte

Abra uma issue descrevendo o título de entrada e o slug esperado.

## Licença

MIT. Veja [LICENSE](LICENSE).
````

## Antes de entregar

1. `Glob LICENSE` confirma que o arquivo existe e começa com o texto MIT; senão, reportar divergência.
2. `Grep -i "seamless|robust|comprehensive|cutting-edge"` no README: sem ocorrências.
3. A saída `ola-mundo` está marcada como esperada, não observada. Pedir ao usuário: `python -c "from pyslug import slugify; print(slugify('Olá Mundo'))"` e colar a saída.
4. Nenhum badge, URL de PyPI ou link de documentação inventado.

## O que o exemplo evita de propósito

- Nenhuma afirmação de desempenho, compatibilidade com outras versões ou "suporte a todos os idiomas": nada disso estava nos arquivos.
- Sem seção de FAQ (envelhece) e sem roadmap.
- A frase de valor descreve o resultado para o leitor em vez de repetir o nome do pacote.
