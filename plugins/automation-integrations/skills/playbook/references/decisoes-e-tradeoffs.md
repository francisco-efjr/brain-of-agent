# Decisões e trade-offs — escolher a forma mais simples confiável

Use antes de construir. Cada árvore termina em uma escolha e na medição que justificaria subir de nível. Decisão material (difícil de reverter, cara, ou que muda o contrato com outros sistemas) vira ADR curto com `assets/templates/adr-workflow-ou-agente.md`; as demais cabem em três linhas no plano.

Sumário: 1. Que forma usar · 2. Workflow ou agente · 3. Onde mora cada regra · 4. Código sobre MCP · 5. Implantação de servidor MCP · 6. Stack · 7. Low-code ou código · 8. Webhooks e entrega · 9. Proteção: hook, permissão, sandbox · 10. Onde rodar um job · 11. Skill, subagente, comando · 12. Quando não automatizar · 13. Exemplo trabalhado

## 1. Que forma usar

| Se a necessidade é… | Forma | Fonte |
| --- | --- | --- |
| Passos conhecidos de antemão, gatilho claro | **Workflow** (n8n, Zapier, Make, script, cron, GitHub Action) | V-08 |
| Entrada aberta que exige julgamento, com custo de erro tolerável ou aprovação humana | **Agente com limite** de passos e de custo | V-08 |
| Dar ao modelo acesso a um sistema (leitura/escrita) de forma reutilizável | **Tool MCP** (+ skill que ensina a usá-la) | V-03, V-09 |
| Algo que **tem** que valer sempre (bloquear comando, proteger arquivo) | **Hook ou permissão**; para dano irrecuperável, sandbox | V-02, V-03, V-21 |
| Procedimento repetido de uma tarefa | **Skill** (na 3ª vez que cola o mesmo playbook) | V-03 |
| Tarefa lateral pesada, que enche o contexto | **Subagente** que devolve resumo | V-03 |
| Execução recorrente sem humano | **Job** `claude -p --bare` / GitHub Action / cron | V-32, V-25 |
| Volume intermediário enorme, laços/retry, dado pessoal | **Código em sandbox sobre MCP** (hipótese a medir) | V-10 |

Regra de parada: **comece com uma chamada direta** e só some etapas, ferramentas ou agentes quando uma avaliação mostrar ganho (V-08).

## 2. Workflow ou agente (V-08)

Quatro perguntas, nesta ordem:

1. Os passos são conhecidos de antemão? Sim → workflow.
2. A decisão exige julgamento sobre entrada aberta? Sim → agente, com limite de passos e de custo.
3. O custo do erro é alto? Sim → verificação entre etapas ou aprovação humana antes do efeito.
4. Uma chamada resolve? Sim → pare aí.

Cinco padrões de workflow para compor antes de pensar em agente: encadeamento, roteamento, paralelização, orquestrador-trabalhadores, avaliador-otimizador. Ferramentas de agente merecem o mesmo cuidado de um prompt (exemplos, bordas, fronteira entre ferramentas parecidas).

**Limite da evidência:** o artigo-base é de dezembro de 2024 e não traz medição; use como regra de partida, não como lei (nota de prompt 78).

## 3. Onde mora cada regra (escada de direcionamento, V-03)

| A regra é… | Vai para | Observação |
| --- | --- | --- |
| Garantia ("nunca X") | Hook, permissão ou configuração gerenciada | CLAUDE.md e skill são pedido, não garantia |
| Fato sempre verdadeiro do projeto | `CLAUDE.md` curto (cerca de 200 linhas é recomendação, não limite) | Relido após compactação (raiz) |
| Referência por área do código | `.claude/rules/` com `paths` ou skill | CLAUDE.md de subdiretório se perde até o diretório ser tocado de novo |
| Procedimento de uma tarefa | Skill | Descrição sempre no contexto; corpo sob demanda |
| Tarefa lateral pesada | Subagente | Isola contexto, devolve resumo |
| Integração com sistema externo | MCP + skill dizendo como usar | Ler `.mcp.json` não mostra servidores de plugin nem conectores |

Se a regra mora em dois lugares, escolha um. Gatilhos de evolução: errou a mesma convenção **duas vezes** → CLAUDE.md; colou o mesmo playbook **três vezes** → skill; copia dados que o Claude não enxerga → MCP. Skills são reinjetadas após compactação dentro de um orçamento (as mais antigas caem); hooks não são afetados.

## 4. Código sobre MCP (V-10)

Considere executar código em sandbox quando **pelo menos um** for verdadeiro: (a) o volume intermediário supera o contexto útil; (b) há laço de espera ou retry; (c) há dado pessoal que não deve chegar ao modelo (tokenizar e restaurar na chamada seguinte). Se todos forem "não", use a tool direta. Exige sandbox, limites de recurso e monitoramento. Descoberta progressiva (listar/ler só as definições necessárias) é parte do padrão.

Não cite "150.000 → 2.000 tokens (98,7%)" como resultado esperado: é autorrelato do artigo, sem verificação independente. Meça com seu fluxo.

## 5. Implantação de servidor MCP (V-12, V-13, V-15, V-16)

| Caso de uso | Implantação | Por quê / risco |
| --- | --- | --- |
| Uso local, acesso a arquivos/CLI da máquina | stdio | Nada em stdout além do protocolo (ANT-01); herda o ambiente do usuário |
| Serviço remoto, vários usuários | Streamable HTTP sem estado | Log em stdout é aceitável; exige autenticação própria (spec de autorização: lacuna) |
| Experiência de interface dentro do cliente | App MCP | Roteado por `mcp-server-dev` (plugin oficial; arquivos internos não lidos) |
| Distribuir servidor local empacotado | MCPB | Idem: citado por V-13, detalhes não lidos |

Servidores de referência (Fetch, Filesystem, Git, Memory, Time, Everything, Sequential Thinking) são "não prontos para produção" (V-17): estude escopo mínimo e allowlist neles; não os recomende como produção. Fetch traz conteúdo externo: perna 2 da trifecta.

## 6. Stack do servidor MCP

TypeScript é a recomendação do mcp-builder (V-12), mas é preferência, não norma. Use a stack do projeto; qualquer SDK serve se respeitar stdout/stderr (V-16) e o desenho de tools (V-09). Pergunte a stack em vez de impor.

## 7. Low-code ou código (Inferido, salvo menção)

| Critério | Low-code (n8n, Zapier, Make) | Código (script, serviço) |
| --- | --- | --- |
| Integração entre SaaS comuns, poucos passos, dono não-dev | Favorece | Excesso |
| Idempotência/dedupe estritos, transações, testes automatizados em CI | Limitado e dependente do fornecedor | Favorece |
| Volume alto, custo por execução | Pode pesar | Favorece |
| Versionamento, revisão de PR, replay de eventos | Depende da plataforma (Não verificável aqui) | Favorece |
| Licença | n8n: Sustainable Use License — uso interno ou não comercial; não redistribuir/embutir (V-31) | Livre |

Cobertura honesta: só o fluxo de erro do n8n está validado (V-19). Retry On Fail, Continue On Fail, Zapier e Make são **Não verificável**: peça a configuração real ou a página oficial antes de prescrever.

## 8. Webhooks e entrega

| Decisão | Opções | Escolha padrão | Por quê |
| --- | --- | --- | --- |
| Semântica | pelo menos uma vez × no máximo uma vez | Pelo menos uma vez + consumidor idempotente | Provedores reenviam; perder evento costuma custar mais que tratá-lo duas vezes (V-18) |
| Quando gravar o ID | antes do efeito × depois do sucesso | ID **e** job na mesma transação; efeito idempotente no worker; `done` depois do sucesso | "Antes" (W-03) evita duplicata concorrente; "depois" (Hookdeck) evita perder evento. A transação única + efeito idempotente cobre os dois (Inferido) |
| Chave de dedupe | ID do evento × ID do objeto + tipo × `created` | ID do evento; composta se o provedor não dá ID estável; nunca `created` | C-12 da síntese; V-18 |
| Status ao falhar | 4xx × 5xx | 4xx para erro do cliente (assinatura inválida); 5xx para falha nossa que deve provocar retry; 429 trata como retry | V-18 (Hookdeck) |
| Processar síncrono | sim × não | Não, salvo trabalho trivial e abaixo do prazo do provedor | V-18 |

## 9. Proteção: hook, permissão, sandbox (V-02, V-21, V-14)

| Mecanismo | Garante? | Use para | Limite |
| --- | --- | --- | --- |
| Hook `PreToolUse` | Reduz erro; mensagem acionável | Bloquear comandos destrutivos conhecidos | Regex tem bypass; injeção pode contorná-lo; soma latência; roda com o shell do usuário |
| Regras deny de permissão | Para as ferramentas internas | Negar leitura de segredos (Read) | O Bash as contorna sem sandbox |
| Sandbox / devcontainer / VM | Sim, isola dano | Comandos com rede ou destrutivos; serviços externos | Configuração e custo |
| Configuração gerenciada | Sim (política) | O que nunca pode ocorrer na organização | Requer admin |

Regra de decisão: dano **recuperável** → hook ou permissão bastam; dano **irrecuperável** (dados, dinheiro, credenciais) → sandbox mais permissão; hook só como camada extra.

## 10. Onde rodar um job

| Opção | Quando | Cuidado |
| --- | --- | --- |
| `claude -p --bare` em cron/CI próprio | Tarefa curta e determinística de entrada/saída | Flags por versão; gate de `plugin_errors` e `mcp_server_errors`; custo (V-32) |
| claude-code-action | Reagir a issue/PR no GitHub | Token mínimo, acionamento restrito, conteúdo de issue como dado, humano antes do merge (V-25) |
| Script/cron sem Claude | Passos determinísticos | Trava de sobreposição, heartbeat (G-xx) |
| Rotinas/tarefas agendadas na nuvem e `/loop` | — | Páginas `scheduled-tasks` não lidas: **Não verificável** aqui |

## 11. Skill, subagente, comando (V-01, V-03, V-05)

Novo fluxo → **skill** (a doc recomenda skills em vez de `commands/`). Comando só como atalho fino que chama uma skill ou agente. Subagente quando o contexto da tarefa não deve poluir a conversa ou quando se quer revisão independente com ferramentas somente leitura. Autor e revisor são entidades distintas: o mesmo modelo revisando a si mesmo não é validação externa — declare.

## 12. Quando não automatizar (Inferido)

- O processo muda toda semana ou ninguém o descreve igual duas vezes: estabilize e documente primeiro (`product-discovery-specs`).
- O custo de um erro silencioso supera a economia de tempo e não há ponto de aprovação humana possível.
- A automação exigiria mover valor financeiro sem humano: não automatize (ver fronteira com `fintech-payments`, `blockchain-web3`).
- O volume é baixo e o procedimento manual é uma checklist de 5 minutos por semana: automatizar custa mais que manter.

## 13. Exemplo trabalhado: nota fiscal por e-mail → planilha

Pedido: "agente que, quando chegar nota fiscal por e-mail, extraia o valor e lance na planilha".

1. Passos conhecidos? Sim (receber, extrair, lançar) → **workflow**, não agente autônomo. O LLM entra **em um passo** (extração do valor) com saída em schema.
2. Trifecta: lê dado privado (financeiro)? Sim. Lê conteúdo externo (e-mail de terceiro)? Sim. Envia para fora? Só se houver resposta automática: **não envie**; a saída é a planilha interna. Perna quebrada: sem saída externa.
3. Idempotência: chave = ID da mensagem de e-mail ou número da NF + emitente; linha duplicada ignorada (F-01).
4. Falha: extração com baixa confiança ou schema inválido → fila de revisão humana, não lançamento (F-03, I-07). Reprocesso registrado (F-04).
5. Lacuna a declarar: se a ferramenta for Zapier/Make, o comportamento de retry e replay é Não verificável; peça a configuração real.
6. Medir antes de subir de nível: taxa de extração correta em 30 notas reais; só então avaliar agente com ferramentas.

Fonte: V-08, V-20, V-18, V-19 e F-xx/I-xx (Inferido). Verificado em 2026-10-10 (itens V).
