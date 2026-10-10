# Guia de segurança do projeto (template de `.claude/claude-security-guidance.md`)

Template para o plugin oficial `security-guidance` (V-02). O arquivo vai em `.claude/claude-security-guidance.md` (também aceito em `~/.claude/` e `.local.md`); teto combinado de 8 KB entre os arquivos de guia. Preencha, remova o que não se aplica, revise com o time. Este plugin não instala o `security-guidance`; ver `ferramentas-e-mcp.md` seção 7.

--- copie a partir daqui ---

# Guia de segurança deste repositório

## Modelo de ameaça
- Ativos: <dados de clientes, tokens, chaves>.
- Atacantes: <usuário autenticado malicioso, tenant vizinho, conteúdo de terceiros>.

## Regras verificáveis (exemplos; adapte)
- Rotas sob /admin chamam a checagem de papel antes de qualquer leitura no banco.
- Identificadores de cliente não entram em log de nível INFO ou superior.
- Comparação de tokens usa função de tempo constante.
- Toda consulta em código multi-tenant filtra por org_id vindo da sessão.
- Entrada de webhook tem a assinatura verificada antes de qualquer processamento.

## O que este guia não faz
- Regras aqui orientam o revisor; não bloqueiam escrita. Imposição real fica em hook de bloqueio, permissões ou CI.

--- fim ---

Notas:
- As regras do guia são aditivas: não suprimem classes de vulnerabilidade (V-02).
- Cada regra deve ser verificável por leitura de código; evite "escreva código seguro".
- Mantenha curto: o guia gasta contexto a cada revisão.
- Evite segredos e dados de cliente neste arquivo (V-33).
- Para regras por edição, veja `security-patterns.exemplo.json` nesta pasta. A estrutura exata do arquivo (nomes de campos além de `substrings`, `paths` e `reminder`, que a doc cita) é Não verificável aqui: confira https://code.claude.com/docs/en/security-guidance antes de usar. Limites documentados: até 50 regras, `reminder` até 1 KB, JSON sempre funciona (YAML exige PyYAML), evite regex com retrocesso pesado.
