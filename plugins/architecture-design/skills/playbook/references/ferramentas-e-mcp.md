# Ferramentas, hooks e MCP recomendados (todos DESATIVADOS)

Validado em 2026-10-10 · Modelo-alvo: Claude 4.x/5.x · Rótulos: Verificado, Inferido, Suposição, Não verificável.
Política do plugin: nada deste arquivo está ativo. O plugin não contém `hooks/hooks.json`, `.mcp.json`, `.lsp.json` nem `bin/`. Cada item abaixo traz JSON ou texto pronto para o usuário copiar conscientemente, o risco e a fonte. Sintaxes de configuração mudam entre versões do Claude Code: confira em https://code.claude.com/docs/en/settings e https://code.claude.com/docs/en/hooks e teste em um repositório descartável antes de adotar (Não verificado nesta fábrica).

## Sumário

1. Resumo e ordem de adoção
2. Regra de permissão para escrever só em docs/
3. Hook PreToolUse que bloqueia escrita fora de docs/
4. Teste de arquitetura no CI
5. Lint de OpenAPI e mock
6. Validação de Mermaid
7. Output style `arquiteto`
8. Usar os agentes com permissões do projeto
9. MCP: nenhum recomendado
10. Itens de terceiros que não devem ser adotados
11. Gotchas

## 1. Resumo e ordem de adoção

| # | Item | Para quê | Risco | Fonte | Ativar? |
| --- | --- | --- | --- | --- | --- |
| 1 | Regra de permissão em `docs/adr/**` e `docs/plans/**` | Reduzir prompts onde a escrita é esperada | Sintaxe não testada; permissões são da sessão, não do agente | V-04 | Opcional |
| 2 | Hook `PreToolUse` | Garantia em vez de frase | Hook executa shell com suas permissões; regex não é fronteira de segurança | V-04, AP-11 | Só após revisar o script |
| 3 | Teste de arquitetura no CI | Fronteiras verificáveis | Pacotes de terceiros se instalados | V-24, V-28, V-45 | Recomendado (grep primeiro) |
| 4 | Lint de OpenAPI | Critério de saída de contrato | `npx` executa código de terceiros | V-40 | Opcional, em sandbox |
| 5 | Validação de Mermaid | Parse como critério de entrega | Nome do pacote não verificado | V-23 | Opcional |
| 6 | Output style `arquiteto` | Diagrama primeiro, trade-offs | Estilo é instrução, não garantia | V-06 | Opcional |

Ordem sugerida: CI com grep (3), depois permissões (1), depois hook (2) se a regra de escrita precisar de garantia.

## 2. Regra de permissão para escrever só em docs/

Objetivo: a escrita em `docs/adr/` e `docs/plans/` não pede confirmação em cada arquivo; qualquer outra escrita continua pedindo (modo padrão). `tools` de agente não escopa diretório (V-04), por isso a regra mora no projeto. Em `.claude/settings.json` do projeto:

```json
{
  "permissions": {
    "allow": [
      "Edit(/docs/adr/**)",
      "Edit(/docs/plans/**)"
    ]
  }
}
```

Para uma sessão de auditoria (nenhuma alteração de produto), acrescente um bloco de recusa:

```json
{
  "permissions": {
    "deny": [
      "Edit(/src/**)"
    ]
  }
}
```

Sintaxe conferida em https://code.claude.com/docs/en/permissions em 2026-10-10 (Verificado na documentação; comportamento não testado nesta fábrica): o Claude Code checa permissões de arquivo só contra regras `Edit(caminho)` e `Read(caminho)`; uma regra de caminho para `Write` é aceita mas nunca consultada (a doc manda usar `Edit(docs/**)` no lugar de `Write(docs/**)`; o aviso de inicialização exige v2.1.210 ou superior). Os padrões seguem a sintaxe do gitignore: `/caminho` é relativo à origem da configuração (em `.claude/settings.json` do projeto, à raiz do projeto), `caminho` sem barra é relativo ao diretório atual. Confira na versão instalada (`claude --version`). Risco: `allow` amplo demais pré-aprova escrita; mantenha os caminhos estreitos. Não use `--dangerously-skip-permissions` para contornar prompts: é risco alto, só aceitável em sandbox descartável com repositório confiável, e nunca ao revisar conteúdo não confiável.

## 3. Hook PreToolUse que bloqueia escrita fora de docs/

Garantia, não frase (P-26): o hook recusa `Write`/`Edit` em caminhos fora de `docs/`. Em `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/guard-docs-write.py\""
          }
        ]
      }
    ]
  }
}
```

E o script `.claude/hooks/guard-docs-write.py` (escrito para este plugin; o script isolado foi testado em 2026-10-10 com JSON via stdin para `docs/adr/a.md` (libera), `src/x.ts`, `docs/../src/y.ts`, outro drive, caminho vazio e `docsx/a.md` (bloqueiam); a integração com o Claude Code não foi testada):

```python
#!/usr/bin/env python3
"""Bloqueia Write/Edit fora de docs/ (guarda-corpo, não fronteira de segurança)."""
import json
import os
import sys

data = json.load(sys.stdin)
path = (data.get("tool_input") or {}).get("file_path", "")
root = os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))
try:
    rel = os.path.relpath(os.path.realpath(path), root).replace("\\", "/")
except ValueError:  # outro drive no Windows: bloqueia em vez de liberar
    rel = path
if path and rel.startswith("docs/"):
    sys.exit(0)
print(f"Escrita bloqueada fora de docs/: {rel}. Peça autorização ao usuário.", file=sys.stderr)
sys.exit(2)
```

Riscos: o hook roda comandos com as suas permissões; leia o script antes de ativar; o script resolve caminhos relativos e links simbólicos com `realpath`, mas `Bash` (que escreve por redirecionamento) e `NotebookEdit` não passam por este matcher, então não é uma fronteira de segurança (AP-11). O código de saída 2 para bloquear e a leitura do JSON por stdin seguem o comportamento documentado de hooks de Claude Code conforme o conhecimento geral (Inferido): confirme na documentação da sua versão. Agentes de plugin não podem declarar hooks (V-04): este hook é do projeto.

## 4. Teste de arquitetura no CI

Comece pelo script de grep de `fronteiras-e-decomposicao.md` (seção 8), sem dependências. Exemplo de workflow do GitHub Actions (Inferido; fixe a ação por SHA de commit conforme a política de supply chain do projeto):

```yaml
name: architecture-boundaries
on: [pull_request]
jobs:
  boundaries:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4   # fixe por SHA no seu repositório
      - run: bash tools/check-boundaries.sh
```

Ferramentas específicas de linguagem citadas na pesquisa (dependency-cruiser e madge para JavaScript, ArchUnit para JVM) não foram executadas nem avaliadas (V-45; ArchUnit é lacuna de fonte). Instalar pacote de terceiros é decisão do usuário; confira licença, manutenção e versão.

## 5. Lint de OpenAPI e mock

Comandos citados por V-40 (Jeffallan/claude-skills, MIT):

```bash
npx @redocly/cli lint openapi.yaml
npx @stoplight/prism-cli mock openapi.yaml
```

Risco: `npx` baixa e executa pacotes de terceiros no momento da chamada. Este plugin não os executa. Se o usuário decidir rodar: ambiente isolado, versão fixada, sem credenciais no ambiente, revisão do pacote. O argumento `mock openapi.yaml` do segundo comando é uso geral do Prism, não confirmado na fonte (Não verificado).

## 6. Validação de Mermaid

Critério de entrega: parse válido. Opções do usuário: editor ao vivo do Mermaid, renderização do GitHub (mostra erro), ou o CLI do Mermaid em ambiente controlado. O nome do pacote do CLI e sua invocação são conhecimento geral e não foram verificados nesta fábrica (V-23): confira a documentação oficial antes de instalar. Sem validação, entregue com a nota "parse não validado".

## 7. Output style `arquiteto` (V-06; nunca forçado)

Arquivo `.claude/output-styles/arquiteto.md` do projeto ou do usuário (campos `name`, `description`, `keep-coding-instructions` conferidos em V-06):

```markdown
---
name: arquiteto
description: Respostas de arquitetura com diagrama primeiro, trade-offs explícitos e a lista do que não foi verificado.
keep-coding-instructions: true
---
Ao tratar de arquitetura:
1. Abra com um diagrama Mermaid de até 15 nós (`flowchart TD` para estrutura, `sequenceDiagram` para fluxo).
2. Depois, prosa curta com trade-offs e a alternativa mais simples, incluindo "não mudar nada".
3. Quando a decisão for humana, termine com as opções e a pergunta exata.
4. Liste o que não foi verificado e rotule Suposições.
```

Notas: não use `force-for-plugin` sem decisão do usuário, pois sobrescreve a escolha dele. Estilo é instrução, não garantia (garantia é hook). Estilos não mudam subagentes, só a conversa principal. `keep-coding-instructions` só tem efeito no prompt de sistema completo (V-06). Eficácia não medida. Este plugin não traz `output-styles/` ativado.

## 8. Usar os agentes com permissões do projeto

Plugins ignoram `hooks`, `mcpServers` e `permissionMode` em arquivos de agente (V-04). Para usar `permissionMode` ou um hook por agente, o usuário copia o arquivo do agente para `.claude/agents/` do projeto e edita lá, por decisão própria. Mantenha revisores somente leitura (`Read, Grep, Glob`); o `adr-writer` com `Write` só deve rodar sob a regra da seção 2 ou o hook da seção 3 (Inferido).

## 9. MCP: nenhum recomendado

A pesquisa do segmento não encontrou servidor MCP que justifique ativação por padrão. Servidores de diagramas e modelagem C4 (Composer, Structurizr) foram rebaixados a classe C: a documentação do fornecedor não sustenta os ganhos atribuídos, MCP de terceiros pode vazar contexto do repositório e alguns exigem Docker. Se o usuário decidir adotar um MCP por conta própria, registre o servidor no escopo do projeto, revise as permissões, evite enviar código proprietário e adicione-o a uma lista de revisão trimestral. O plugin não fornece `.mcp.json`.

## 10. Itens de terceiros que não devem ser adotados como dependência

| Item | Motivo |
| --- | --- |
| code-modernization (Apache-2.0, anthropics/claude-plugins-official) | Telemetria ligada por padrão (desliga com `CODE_MODERNIZATION_TELEMETRY=0` ou `DISABLE_TELEMETRY=1`, conforme V-11); aqui só o método foi destilado |
| gstack (MIT) | Skill de 705 linhas acoplada a binários `gstack-*`, telemetria e escrita em `~/.gstack` (V-19); só o processo foi destilado, com atribuição |
| everything-claude-code (MIT) | Instalador do pacote não foi lido; não rodar (V-16) |
| Bundle de renderização do gstack `diagram` | Executa `bun` e scripts locais (V-23) |
| Scripts de capacidade (`botec.py`) de system-design-skills | Não executados: a conta vai no texto (V-41) |

## 11. Gotchas

- Hooks e permissões variam por versão: o CLI usado na especificação da fábrica é 2.1.128 e `claude plugin eval` exige 2.1.269 ou superior (conferir `claude --version`).
- Hook que bloqueia escrita não impede `Bash` com redirecionamento; combine com revisão e permissões.
- Regra de permissão `allow` não restringe agentes individualmente; vale para a sessão.
- Em skill, `allowed-tools` não restringe nada: só pré-aprova as ferramentas listadas durante o turno que invoca a skill, e a concessão cai quando o usuário envia a próxima mensagem. Para tirar ferramentas do alcance enquanto a skill está ativa existe `disallowed-tools`, cuja restrição também cai na próxima mensagem (https://code.claude.com/docs/en/skills, conferido em 2026-10-10). As skills somente leitura deste plugin declaram `disallowed-tools: Write, Edit, NotebookEdit` como reforço; depois da primeira resposta do usuário, o limite volta a ser instrução.
- `npx` e instaladores executam código de terceiros: nunca como parte automática de um fluxo do plugin.
- Estrelas de repositório não provam segurança nem qualidade (AP-20).
