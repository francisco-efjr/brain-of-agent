---
name: mcp-stdio-print
description: "Mede se o plugin diagnostica o erro clássico de servidor MCP stdio com print em stdout e orienta o teste sem afirmar execução."
tags: [automation-integrations, building-mcp-servers, mcp, stdio, positivo]
runs: 3
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
expected_outcome: "Aponta o print em stdout como causa do erro de JSON, propõe logging em stderr, sugere testar com o MCP Inspector em versão fixada sem dizer que rodou, e pergunta pelas anotações de risco."
---
Fiz um servidor MCP em Python para o Claude consultar o estoque da loja. Quando conecto no Claude Code o servidor cai e aparece um erro de parse de JSON. Já reinstalei o pacote `mcp` duas vezes e a mesma coisa acontece. Registrei assim:

`claude mcp add estoque -- python server.py`

Este é o `server.py` inteiro:

```python
from mcp.server.fastmcp import FastMCP
import sqlite3

mcp = FastMCP("estoque")

@mcp.tool()
def buscar_produto(sku: str) -> str:
    """Busca um produto pelo SKU."""
    print("tool chamada:", sku)
    con = sqlite3.connect("estoque.db")
    row = con.execute("SELECT nome, qtd FROM produtos WHERE sku = ?", (sku,)).fetchone()
    return f"{row[0]} ({row[1]} em estoque)" if row else "não encontrado"

@mcp.tool()
def zerar_estoque(sku: str) -> str:
    """Zera o estoque de um produto."""
    con = sqlite3.connect("estoque.db")
    con.execute("UPDATE produtos SET qtd = 0 WHERE sku = ?", (sku,))
    con.commit()
    return "ok"

if __name__ == "__main__":
    print("servidor iniciando")
    mcp.run(transport="stdio")
```

Por que dá erro, e o que eu deveria mudar? Rodo no Windows, mas o servidor também vai rodar no servidor Linux da loja.
