# Esqueletos de servidor MCP (Python e TypeScript)

Rótulo geral: **Inferido**. Os esqueletos são redação própria a partir do padrão descrito em V-09, V-12 e V-16 e do conhecimento estável dos SDKs oficiais; não foram executados durante a construção do plugin (o pacote `mcp` não estava instalado e a política da casa proíbe instalar pacotes de terceiros). Antes de usar, confirme nomes de classes e parâmetros na versão instalada (`pip show mcp`, `npm ls @modelcontextprotocol/sdk`) e na documentação oficial do SDK.

Sumário: 1. Python · 2. TypeScript · 3. Erro acionável · 4. Ficha de tool preenchida · 5. Servidor HTTP remoto.

## 1. Python (SDK oficial, FastMCP)

```python
import logging
import sys
from typing import Literal

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

# V-16: stdio => stdout é só protocolo. Logs vão para stderr.
logging.basicConfig(stream=sys.stderr, level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("tracker-mcp")

mcp = FastMCP("tracker")

# Cliente compartilhado: um só lugar para auth, erro, paginação e formatação.
from tracker_client import TrackerClient, TrackerError   # módulo do projeto
client = TrackerClient.from_env()                         # segredo via variável de ambiente


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def tracker_search_issues(
    query: str,
    limit: int = 10,
    cursor: str | None = None,
    response_format: Literal["concise", "detailed"] = "concise",
) -> str:
    """Busca issues por texto no tracker e devolve as mais relevantes.

    Use quando o usuário quer encontrar issues por assunto, autor ou estado.
    Para abrir uma issue conhecida use tracker_get_issue. `query` aceita
    palavras e filtros como `state:open author:ana`. `limit` vai de 1 a 50.
    `concise` devolve id, título e estado; `detailed` inclui descrição e comentários.
    Se houver mais resultados, a resposta traz `next_cursor`: passe-o em `cursor`.
    """
    if not 1 <= limit <= 50:
        raise ValueError("limit deve estar entre 1 e 50; exemplo válido: limit=10")
    try:
        page = client.search_issues(query=query, limit=limit, cursor=cursor)
    except TrackerError as err:
        log.warning("busca falhou: %s", err)              # stderr, sem segredo
        raise ValueError(f"A busca falhou ({err.kind}). {err.hint}") from err
    return page.render(detailed=(response_format == "detailed"))


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False,
                                      idempotentHint=False, openWorldHint=False))
def tracker_create_issue(title: str, body: str, project_id: str) -> str:
    """Cria uma issue no projeto indicado. Não é idempotente: duas chamadas criam duas issues."""
    ...


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

Notas de revisão:
- O parâmetro `annotations` e a classe `ToolAnnotations` existem nas versões recentes do SDK; em versões antigas o decorador não aceita (confira).
- Levantar `ValueError` com mensagem acionável vira resultado de erro da tool no SDK (comportamento a confirmar na versão instalada).
- `tracker_client` é do projeto: ele nunca imprime; erros carregam `kind` e `hint` (o que fazer).

## 2. TypeScript (SDK oficial)

```ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const log = (...a: unknown[]) => console.error("[tracker-mcp]", ...a); // stderr, nunca console.log

const server = new McpServer({ name: "tracker", version: "0.1.0" });

server.registerTool(
  "tracker_search_issues",
  {
    description:
      "Busca issues por texto e devolve as mais relevantes. Para uma issue conhecida use tracker_get_issue. " +
      "limit vai de 1 a 50; use cursor para a próxima página.",
    inputSchema: {
      query: z.string().min(1).describe("Palavras ou filtros, ex.: 'state:open author:ana'"),
      limit: z.number().int().min(1).max(50).default(10),
      cursor: z.string().optional().describe("next_cursor da página anterior"),
      response_format: z.enum(["concise", "detailed"]).default("concise"),
    },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  async ({ query, limit, cursor, response_format }) => {
    try {
      const page = await client.searchIssues({ query, limit, cursor });
      return { content: [{ type: "text", text: page.render(response_format === "detailed") }] };
    } catch (err) {
      log("busca falhou", String(err));
      return { isError: true, content: [{ type: "text", text: "A busca falhou. Verifique o filtro; exemplo válido: 'state:open'." }] };
    }
  },
);

await server.connect(new StdioServerTransport());
```

Notas: o `await` no nível superior exige módulo ES (`"type": "module"` no `package.json`); a assinatura de `registerTool` e o formato de `inputSchema` mudaram entre versões do SDK; confirme. `console.error` escreve em stderr; `console.log`, `console.info` e `console.debug` escrevem em stdout e corrompem o protocolo.

## 3. Erro acionável (T-06)

Ruim: `Error 400`. Bom: causa, correção e exemplo.

```text
Não encontrei o projeto "tracker-web" (project_id inexistente).
Use tracker_list_projects para ver os IDs válidos. Exemplo de chamada: tracker_create_issue(project_id="PRJ-12", title="...", body="...").
```

Regra: o erro diz o que o modelo deve fazer a seguir; stack trace vai para o log em stderr, nunca para a resposta.

## 4. Ficha de tool preenchida (molde: `ficha-de-tool-mcp.md` do playbook)

| Campo | Valor |
| --- | --- |
| Intenção do usuário | "ache as issues abertas da Ana sobre login" |
| Nome | `tracker_search_issues` (prefixo do serviço + verbo) |
| Parâmetros | `query` (texto/filtros), `limit` 1..50 (padrão 10), `cursor`, `response_format` |
| Retorno | concise: id, título, estado (~1/3 dos tokens do detailed, ordem de grandeza do exemplo do artigo V-09; meça no seu caso); detailed: + descrição, comentários |
| Limite e paginação | 50 por página; `next_cursor` |
| Erros | filtro inválido (mostra exemplo), cota (diz quando tentar de novo) |
| Anotações | `readOnlyHint: true`, `openWorldHint: false` |
| Risco | leitura; conteúdo de issue é dado de terceiros (injeção): o servidor não executa nada do texto |
| Tarefa de avaliação | "Quantas issues abertas da Ana mencionam login e quem comentou por último na mais antiga?" |

## 5. Se o servidor for HTTP remoto

- Streamable HTTP sem estado (V-12). Em HTTP, log em stdout é aceito (V-16), mas continue sem segredo no log.
- Autenticação: siga a especificação de autorização do MCP na versão datada do SDK (a página de autorização não foi lida na pesquisa: Não verificado). Sem autenticação, não exponha o servidor fora de `127.0.0.1`.
- Cliente que consome: segredos em cabeçalho via `${VAR}` ou `headersHelper` (script que expira em 10 s e só roda após confiança no projeto, V-15); nunca literal em `url`.
- Uma tool com efeito destrutivo exige confirmação do lado do servidor (S-04), porque o cliente pode estar em modo sem prompts.
