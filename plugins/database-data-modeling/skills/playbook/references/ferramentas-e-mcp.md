# Ferramentas, MCP e hooks recomendados (todos DESATIVADOS neste plugin)

Sumário: 1 Política · 2 Camadas de proteção · 3 Postgres MCP Pro em modo restrito · 4 MongoDB MCP · 5 Hook de guarda SQL · 6 permissions.deny · 7 Papel de banco somente leitura · 8 Hooks e subagentes de plugin · 9 Checklist de tools de banco · 10 Ferramentas de terceiros (só referência) · 11 Skills de terceiros

## 1. Política

O plugin não envia `hooks/`, `.mcp.json`, `.lsp.json` nem `bin/`. Tudo abaixo é material para você copiar para o seu projeto depois de ler os riscos. Instalar um servidor MCP executa código de terceiros com as permissões do seu usuário: revise o repositório, fixe versão e use credencial mínima. Rótulos: Verificado = conferido em fonte nesta fábrica (data 2026-10-10); Inferido/Suposição = confirme antes de usar.

## 2. Camadas de proteção (da mais forte à mais fraca)

1. Papel de banco sem privilégio de escrita, em réplica ou banco de dev (barreira real). Seção 7.
2. Credencial escopada por ambiente; produção fora da sessão (política da casa).
3. Sandbox e permissões do Claude Code (`permissions.deny`, modo de permissão). V-03.
4. Servidor MCP em modo restrito. V-34.
5. Hook `PreToolUse` (guardrail com falso negativo). V-02.
6. Texto em CLAUDE.md (orientação). V-04.

A página de segurança do Claude Code informa que um comando Bash aprovado ainda escreve onde o seu usuário pode escrever, e que o modo de permissão inicial padrão em sessões interativas passou a ser o auto mode (v2.1.283 ou superior; V-03). As skills deste plugin não assumem o modo ativo.

## 3. Postgres MCP Pro (crystaldba/postgres-mcp, V-34; B6; MIT)

O que faz (README, Verificado): 9 tools (`list_schemas`, `list_objects`, `get_object_details`, `execute_sql`, `explain_query`, `get_top_queries`, `analyze_workload_indexes`, `analyze_query_indexes`, `analyze_db_health`). `--access-mode=restricted`: transações somente leitura com limite de tempo, indicado para produção pela própria página; `unrestricted`: leitura e escrita, para desenvolvimento. Todos os exemplos do README usam `unrestricted`; a página não declara o padrão. Instalação por Docker, `pipx` ou `uv`; a URI vem da variável `DATABASE_URI`.

Configuração recomendada (forma do README reaberta em 2026-10-10; a expansão `${VAR}` em `.mcp.json` é Inferido, confirme na doc de MCP do Claude Code):

```json
{
  "mcpServers": {
    "postgres-ro": {
      "command": "uv",
      "args": ["run", "postgres-mcp", "--access-mode=restricted"],
      "env": { "DATABASE_URI": "${PG_REPLICA_RO_URI}" }
    }
  }
}
```

Riscos: código de terceiros; `execute_sql` roda SQL que o modelo escrever (o modo restrito reduz, não substitui o papel read-only); `get_top_queries` e saídas podem conter dados pessoais; a URI nunca vai para o arquivo, só a referência à variável de ambiente; use réplica ou dev, nunca produção. O plugin não instala nada.

## 4. MongoDB MCP

O SKILL.md `mongodb-schema-design` (Apache-2.0) cita a opção `--readOnly` e pede "yes" explícito antes de escritas (V-25). O nome do pacote e o comando do servidor MCP do MongoDB são Não verificados: abra a documentação oficial do servidor antes de configurar.

## 5. Hook de guarda de SQL destrutivo (V-02; Art. J)

Estrutura confirmada na página de hooks em 2026-10-10 (evento → grupo com `matcher` → handler `type: command`). `onFailure: "block"` exige Claude Code v2.1.295 ou superior; sem ele, falha do hook não bloqueia. Salve em `.claude/settings.json` do projeto (decisão sua):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "node \"${CLAUDE_PROJECT_DIR}/.claude/hooks/db-guard.js\"",
            "onFailure": "block"
          }
        ]
      }
    ]
  }
}
```

Script do projeto (`.claude/hooks/db-guard.js`, Node para funcionar também no Windows; redação própria, MIT; revise antes de ativar):

```js
// Lê o JSON do hook em stdin; sai com 2 (bloqueia) se o comando parece destrutivo.
let raw = '';
process.stdin.on('data', d => (raw += d));
process.stdin.on('end', () => {
  let cmd = '';
  try { cmd = String(JSON.parse(raw).tool_input?.command ?? ''); } catch { process.exit(1); }
  const destrutivo = /\b(drop\s+(table|database|schema)|truncate)\b/i.test(cmd)
    || (/\b(delete\s+from|update)\b/i.test(cmd) && !/\bwhere\b/i.test(cmd));
  if (destrutivo) {
    console.error('Bloqueado: comando SQL destrutivo. Rode antes um SELECT COUNT(*) equivalente, '
      + 'mostre a contagem ao usuário e peça confirmação explícita.');
    process.exit(2);
  }
  process.exit(0);
});
```

Verificado em V-02: saída 2 bloqueia e o stderr vira o motivo; qualquer outro código diferente de zero (inclusive 1) não bloqueia, a menos que `onFailure: "block"` esteja ativo; timeout em PreToolUse não bloqueia sem `onFailure`; JSON em stdout não vence a saída 2. Escolha um só modo de bloqueio por hook.

Riscos: falso positivo, porque `update` sem `WHERE` também casa `npm update`, `apt update` e `git update-index` (restrinja o regex aos clientes de banco, por exemplo comandos que contêm `psql`, `mysql` ou `sqlite3`); falso negativo, porque regex falha com SQL ofuscado, em arquivos `.sql` executados por cliente, em ORMs e em variáveis; roda com as suas permissões, então o script é código seu a revisar; a doc recomenda o sistema de permissões para regras rígidas. Teste com um comando inofensivo (`echo drop table x`) antes de confiar. O `if` e `matcher` têm sintaxe própria: confira a página de hooks da sua versão.

## 6. permissions.deny (V-03; sintaxe reaberta em 2026-10-10)

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./secrets/**)",
      "Bash(curl *)",
      "Bash(wget *)"
    ]
  }
}
```

`Read(./.env)` bloqueia as ferramentas de arquivo do Claude; a doc avisa que regras de Bash que restringem argumentos são frágeis e não casam variações do comando (`/usr/bin/curl`, `sh -c '...'`). Isso é camada, não barreira. Para clientes de banco (`psql`, `mysql`) contra hosts de produção, a regra por argumento é igualmente contornável: a barreira é a credencial.

## 7. Papel de banco somente leitura

Exemplo conceitual PostgreSQL em `operacao-e-seguranca-de-dados.md` (seção 7). Adapte ao SGBD. `SELECT` em tabelas sensíveis expõe dados pessoais: conceda views/colunas mínimas.

## 8. Hooks e subagentes de plugin (V-01, V-02)

- O frontmatter de subagentes de plugin ignora `hooks`, `mcpServers` e `permissionMode`. Por isso os agentes deste plugin só declaram `tools: Read, Grep, Glob` (sem Bash, Write, Edit): a garantia é a allowlist.
- Hooks configurados no próprio plugin ou no projeto também disparam em chamadas de ferramenta de subagentes (a entrada traz `agent_id`). A regra da casa continua: o plugin não distribui hook que execute shell.
- `allowed-tools` em skill só pré-aprova; não impede o usuário de aprovar Bash. A garantia "não executa SQL" nas skills é instrução; nos agentes, é técnica.

## 9. Checklist de tools de banco (Art. O; V-05)

Ver `checklist-completo.md`, seção 12. Resumo: consolidar em poucas tools com namespace; nomes legíveis; `response_format` concise/detailed; paginação e truncamento (25 mil tokens por resposta no Claude Code); erros acionáveis; descrição como para um novo colega; avaliar com tarefas realistas.

## 10. Ferramentas de terceiros (só referência; não instalar pelo plugin)

| Ferramenta | Uso | Fonte | Risco |
| --- | --- | --- | --- |
| strong_migrations | lista de operações perigosas (Ruby, conceito portável) | V-18, MIT | não detecta backfill perigoso |
| gh-ost | migração online de MySQL via binlog, sem triggers; `--test-on-replica` | V-17, MIT | exige binlog/réplica; usar releases |
| pgroll | migrações expand/contract em PG com schemas versionados | V-21, Apache-2.0 | triggers e views têm custo; só PG |
| NoSQL Workbench (AWS) | modelagem DynamoDB | V-26 | |
| gstack `/careful`, `/freeze` | ideia de confirmação antes de destrutivo e restrição de edição | V-40, MIT | o `./setup` instala hooks e Chromium e contorna o sistema de permissões: não recomendado |

## 11. Skills de terceiros (apontar, não instalar)

supabase/agent-skills (V-31, MIT, 73 pontos), redis/agent-skills (V-28, MIT, 67), neondatabase/agent-skills (V-35, Apache-2.0, 70; recomenda instalação sem prompt `-y`: evite), mongodb/agent-skills (V-25, Apache-2.0, 77), dbt-labs/dbt-agent-skills (V-41, Apache-2.0; fronteira com data-engineering). Média de 65/100 nas skills de terceiros avaliadas, sem evals publicadas (L-10): este plugin destila a documentação oficial em vez de copiar essas skills.
