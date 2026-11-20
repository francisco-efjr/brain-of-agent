"""Camada de SO da IA local: um servidor MCP que aplica as regras do core nas próprias ferramentas.

O modelo local escolhe a ferramenta; o servidor classifica o risco, observa, ensaia, faz backup,
pede a confirmação ao usuário numa janela do Windows, executa, verifica e registra.
Só biblioteca padrão (Python 3.10+). Nada sai da máquina.
"""

NOME = "ia-operador-so"
VERSAO = "1.0.0"
