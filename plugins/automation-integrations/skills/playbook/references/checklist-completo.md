# Checklists completos — IDs W, T, S, H, K, J, R, A, M, F, I, G, X

Fonte única dos IDs citados por skills, agentes, templates e evals do plugin. Cada item traz como verificar e, quando faz sentido, a severidade padrão se falhar. Ajuste a severidade ao contexto (dado sensível ou dinheiro sobe um nível).

Sumário: 1. Como usar · 2. W webhook · 3. T tool MCP · 4. S segurança de servidor MCP · 5. H hook · 6. K SKILL.md · 7. J job `claude -p` · 8. R risco/trifecta · 9. A adoção de terceiros · 10. M manifesto · 11. F workflow low-code · 12. I cliente de API de saída · 13. G job agendado genérico · 14. X scraping

## 1. Como usar

- Marque cada item como `ok`, `falha`, `NA (motivo)` ou `NV` (não verificável: sem acesso, sem execução). `NA` sem motivo não vale.
- Evidência de `falha` e de `ok` crítico: `arquivo:linha`, saída de comando ou trecho de configuração. Leitura de código prova propriedade estática, não comportamento em execução: rotule Inferido quando só leu.
- Severidade: crítico (efeito indevido ou vazamento possível agora), alto (falha provável em produção), médio (degrada diagnóstico ou robustez), baixo (higiene).
- Itens `I` e `G` são **Inferido** (conhecimento estável do domínio, sem item V): confirme limites e nomes de cabeçalho na documentação do provedor.
- Em dúvida sobre um achado, não reporte como certeza: registre como hipótese com a verificação que a confirmaria.

## 2. W — receptor de webhook (V-18; Stripe, GitHub, Hookdeck)

| ID | Item | Como verificar | Se falhar |
| --- | --- | --- | --- |
| W-01 | Corpo bruto preservado até a verificação da assinatura (nenhum parser/middleware reencodou) | Achar onde o corpo é lido; confirmar que bytes originais entram no HMAC. Teste: payload com espaços e ordem de chaves diferentes | crítico |
| W-02 | Assinatura verificada: HMAC SHA-256 com segredo do provedor, comparação em tempo constante, tolerância de timestamp de minutos e nunca 0; esquemas desconhecidos ignorados (Stripe: só `v1`). Extras: HTTPS com TLS 1.2+, allowlist de IP **além** da assinatura, rota fora da proteção CSRF | Grep por `compare_digest`/`timingSafeEqual`; teste com assinatura inválida e timestamp antigo | crítico (sem assinatura); alto (tolerância 0 ou ausente) |
| W-03 | ID do evento gravado com restrição de unicidade antes do efeito; chave = ID do evento do provedor, nunca `created` | Ler o schema/constraint; teste: mesmo ID duas vezes → um efeito | crítico |
| W-04 | 2xx devolvido antes do trabalho pesado | Medir/ler: nada de e-mail, API externa ou lote antes do retorno | alto |
| W-05 | Fila com retry, backoff e fila de mortas; reprocesso manual idempotente | Existe consumidor, política de tentativas e destino das falhas; teste: falha forçada vai à fila de mortas | alto |
| W-06 | Evento parcial ou possivelmente velho: buscar o objeto atual na API em vez de confiar no payload | Ler o worker | médio |
| W-07 | Nenhuma dependência de ordem de chegada | Teste: entregar evento B antes de A | médio |
| W-08 | Log com ID do evento, resultado da assinatura e código devolvido; nunca segredo nem payload completo com dado pessoal | Grep de `log`/`print` no handler | médio |
| W-09 | Rotação de segredo registrada (Stripe permite dois segredos ativos por até 24 h) | Procedimento documentado no runbook | baixo |
| W-10 | Segredo em variável de ambiente; nunca no código, URL ou cliente | Grep por literais; revisar `.env.example` | crítico se literal no repositório |
| W-11 | Assinar só os tipos de evento necessários; tratar tipos novos como esperados (GitHub: checar `X-GitHub-Event` e `action`) | Lista de eventos no painel/config; `default:` do switch devolve 2xx e registra | baixo |

Extras do GitHub (V-18): segredo longo e aleatório; responder 2xx em até 10 s; `X-GitHub-Delivery` identifica reenvios (o reenvio mantém o ID); lista de IPs na rota `/meta`. Prazos de retry (Stripe: até 3 dias automático, 15 dias no painel, 30 na CLI) são do provedor: não generalize.

Fonte: V-18. Verificado em 2026-10-10.

## 3. T — tool MCP (V-09, V-12)

| ID | Item | Como verificar |
| --- | --- | --- |
| T-01 | Uma tool por intenção do usuário, não por endpoint | Listar tools: cada uma responde a uma tarefa em uma chamada? Ex.: `schedule_event` em vez de listar usuários + listar eventos + criar |
| T-02 | Nome com prefixo do serviço e verbo no início (`github_create_issue`); prefixo contra sufixo varia por modelo: decida por avaliação | Nomes consistentes |
| T-03 | Parâmetros sem ambiguidade (`user_id`, não `id`); enums e limites no schema | Ler `inputSchema` |
| T-04 | Retorno conciso por padrão, `detailed` opcional (`response_format`), IDs traduzidos para nomes | Chamar com entrada típica e medir o tamanho da saída |
| T-05 | Limite padrão e paginação; truncamento com aviso (no Claude Code a resposta de tool tem teto padrão de 25.000 tokens) | Chamar com dataset grande |
| T-06 | Erro com causa, correção e exemplo de entrada válida | Provocar 3 erros típicos e ler a mensagem |
| T-07 | Anotações de risco em todas as tools: `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint` | Ler definição |
| T-08 | Descrições revisadas com transcrições de avaliação (o modelo escolheu a tool certa?) | Rodar as 10 perguntas ou 5 tarefas reais |

Fonte: V-09, V-12. Verificado em 2026-10-10.

## 4. S — segurança de servidor MCP (V-27, V-16, V-15)

| ID | Item | Como verificar |
| --- | --- | --- |
| S-01 | Anotações em todas as tools | Idem T-07 |
| S-02 | Caminho resolvido (symlinks, caixa de letras) **antes** de comparar com raízes permitidas | Teste: symlink para fora da raiz; `..`; variação de caixa em sistema de arquivos insensível |
| S-03 | "Somente leitura" aplicada na concessão/lista de tools ou no escopo de autorização, não só na recusa em tempo de chamada | Perfil somente leitura não lista tools de escrita |
| S-04 | Confirmação no servidor para ação destrutiva | Chamada destrutiva sem confirmação falha |
| S-05 | Subprocesso sem shell, lista de argumentos, allowlist de comandos e proteção contra injeção de opção (`--` antes de argumento do usuário) | Grep por `shell=True`, `exec(`, concatenação de comando |
| S-06 | Tools que trazem conteúdo da web marcadas `openWorldHint` e tratadas como fonte de injeção | Ler anotações; conferir trifecta (R-xx) |
| S-07 | Revisão independente com um teste por achado | Relatório com teste |
| S-08 | Não confiar em scanner automático sem conferir manualmente | Achados do scanner reproduzidos |
| S-09 | Revisão repetida a cada atualização do servidor | Versão fixada + data da última revisão |

Fonte: V-27 (um autor, 26 servidores; classe B), V-15, V-16. Verificado em 2026-10-10.

## 5. H — hook de guardrail (V-02)

| ID | Item | Como verificar |
| --- | --- | --- |
| H-01 | Evento e matcher estreitos (`Bash`, `Edit\|Write`, `mcp__servidor__.*`) | Ler config |
| H-02 | Lógica em script nomeado, lendo o JSON do evento no stdin | Script existe e roda isolado |
| H-03 | Bloqueio com exit 2 e stderr acionável (o que fazer no lugar), ou `hookSpecificOutput.permissionDecision` quando o evento pede | Rodar com entrada simulada, colar exit code |
| H-04 | `timeout` e `onFailure` explícitos (`block` para regra de segurança; `onFailure` exige v2.1.295+) | Config; `claude --version` |
| H-05 | Nada além do JSON no stdout (nem mensagem de perfil do shell) | Rodar o hook e inspecionar stdout |
| H-06 | Teste com o comando a bloquear **e** com um parecido que deve passar | Tabela de casos com exit esperado |
| H-07 | Como desativar documentado | Runbook/README |
| H-08 | Hook reduz erro; não é fronteira de segurança — dano irrecuperável exige sandbox, devcontainer ou permissão | Texto presente na entrega |

Fonte: V-02, V-21. Verificado em 2026-10-10.

## 6. K — SKILL.md (V-04, V-05, V-22)

| ID | Item |
| --- | --- |
| K-01 | `name` kebab-case, ≤ 64 caracteres, igual à pasta, sem `claude`/`anthropic` |
| K-02 | `description` ≤ 1.024 caracteres, terceira pessoa, o que faz **e quando usar**, gatilhos PT e EN, caso principal primeiro (Claude Code trunca `description` + `when_to_use` em 1.536) |
| K-03 | Corpo < 500 linhas |
| K-04 | Referências a um nível a partir do SKILL.md; arquivo > 100 linhas tem sumário |
| K-05 | Ferramentas MCP qualificadas (`Servidor:ferramenta`) |
| K-06 | Passos com validação (comando ou critério) |
| K-07 | O conteúdo corrige um hábito do modelo; `## Gotchas` só com falhas reais |
| K-08 | Objetivo e restrições, não roteiro rígido (exceto operação frágil) |
| K-09 | Três avaliações escritas antes da versão final, testadas em portes diferentes de modelo |
| K-10 | Dados persistentes fora da pasta da skill (`${CLAUDE_PLUGIN_DATA}`); hook temporário só durante a skill |

Verificação: ler frontmatter e contar linhas (`wc -l`); `claude plugin validate <dir>`. Fonte: V-04, V-05, V-22. Verificado em 2026-10-10.

## 7. J — job `claude -p` (V-32)

| ID | Item |
| --- | --- |
| J-01 | `--bare` + configuração explícita por flags (sem `--bare`, `-p` roda hooks e MCP do projeto sem prompt de confiança) |
| J-02 | Ferramentas por lista mínima (`--allowedTools`; espaço antes do `*` importa) |
| J-03 | `--permission-mode dontAsk` ou `--permission-prompts none` (v2.1.259+) |
| J-04 | Teto de custo (`--max-budget-usd`) |
| J-05 | `--output-format json` + `--json-schema`; verificar código de saída |
| J-06 | Gate: falhar se `plugin_errors` ou `mcp_server_errors` vier não vazio no evento `system/init` |
| J-07 | Entrada externa tratada como dado (R-xx) |
| J-08 | Segredos por variável de ambiente |

Fonte: V-32. Flags variam de v2.1.246 a v2.1.295: conferir `claude --version`. Verificado em 2026-10-10.

## 8. R — risco / trifecta letal (V-20, V-14)

| ID | Item |
| --- | --- |
| R-01 | A automação lê dado privado? |
| R-02 | Lê conteúdo externo (webhook, e-mail, issue, página, resultado de tool)? |
| R-03 | Pode enviar algo para fora (HTTP, e-mail, imagem remota, link)? |
| R-04 | Três "sim": quebrar uma perna (remover a saída; separar em dois agentes sem acesso cruzado; exigir aprovação humana antes do envio) |
| R-05 | Registrar o que sai antes de enviar |
| R-06 | Auditar a **combinação** de servidores MCP, não cada um isolado |
| R-07 | Revisão humana antes de escrita em sistema externo; credenciais fora do contexto do agente |

Fonte: V-20 (heurística de design, não norma), V-14. Verificado em 2026-10-10.

## 9. A — adoção de skill, plugin, hook, MCP ou instalador de terceiros (V-11, V-30, V-31)

| ID | Item |
| --- | --- |
| A-01 | Ler o SKILL.md inteiro, inclusive a descrição |
| A-02 | Listar e ler scripts e dependências antes de executar qualquer coisa |
| A-03 | Procurar URLs, chamadas de rede, leitura de credenciais e instruções para ignorar regras |
| A-04 | Passos destrutivos sem confirmação |
| A-05 | Testar em diretório descartável |
| A-06 | Fixar tag ou SHA; nunca `@latest`, `--yes` ou `curl \| bash` |
| A-07 | Registrar licença e atribuição de cada componente |
| A-08 | Hooks e servidores MCP embutidos entram ativos? (servidor de plugin sobe sozinho ao habilitar o plugin) |

Fonte: V-11, V-15, V-30, V-31. Verificado em 2026-10-10.

## 10. M — manifesto e publicação (V-01)

| ID | Item |
| --- | --- |
| M-01 | `name` válido (kebab-case) e fora dos reservados: não começa com `claude-`, `anthropic-`, `anthropics-`, `cc-plugin-`; sem `claude`/`anthropic`/`official` como palavra |
| M-02 | Caminhos de componente com `./`, existentes, dentro da raiz (sem `..`) |
| M-03 | Instruções de contexto em skill; nenhum `CLAUDE.md` esperado na raiz do plugin |
| M-04 | Sem `bin/` se o plugin deve funcionar em claude.ai ou Cowork |
| M-05 | `claude plugin validate <dir>` passa (`--strict` no CI, se a versão suportar) |
| M-06 | Sem campos `experimental.*` |
| M-07 | `skills/` em vez de `commands/` em plugin novo |

Fonte: V-01. Verificado em 2026-10-10.

## 11. F — workflow low-code (n8n, Zapier, Make) (V-19, V-18; resto Inferido)

| ID | Item |
| --- | --- |
| F-01 | Chave de idempotência definida (ID do registro/evento de origem) |
| F-02 | Retry com backoff e classificação de erro (4xx de cliente ≠ 5xx) |
| F-03 | Destino de falha com alerta (error workflow / fila de mortas) |
| F-04 | Reprocesso registrado (n8n: `retryOf` aparece só em retentativa) |
| F-05 | Timeouts e limites de taxa explícitos |
| F-06 | Credenciais no cofre do fornecedor, nunca em nó/URL |
| F-07 | Teste de falha forçada executado |

Base verificada: V-19 (n8n, Error Trigger) e V-18. O restante é Inferido e depende da documentação do fornecedor; **Retry On Fail, Continue On Fail, Zapier e Make: Não verificável** nesta base. Verificado em 2026-10-10 (parte V-19/V-18).

## 12. I — cliente de API de saída / sincronização API↔API (Inferido)

| ID | Item |
| --- | --- |
| I-01 | Renovar token OAuth antes de expirar; 401 trata uma renovação e para (sem laço) |
| I-02 | 429/503: respeitar `Retry-After` quando presente; senão backoff exponencial com jitter e teto de tentativas |
| I-03 | Timeouts de conexão e de leitura explícitos |
| I-04 | Paginar até o fim com cursor persistido (retomar sem duplicar) |
| I-05 | Sincronização incremental (`updated_since`/cursor) com sobreposição e dedupe, mais reconciliação completa periódica |
| I-06 | Escrita idempotente no destino (chave natural ou chave de idempotência do provedor, quando existir; `Idempotency-Key` sem fonte validada) |
| I-07 | Mapeamento de campos com schema versionado; falha de validação vai à fila de mortas, nunca descartada em silêncio |

Sem item V: conhecimento estável do domínio. Confirme limites, cabeçalhos e semântica na documentação do provedor. Rótulo: Inferido.

## 13. G — job agendado genérico (cron, scheduler) (Inferido)

| ID | Item |
| --- | --- |
| G-01 | Trava contra execução sobreposta (lock com expiração) |
| G-02 | Fuso explícito (preferir UTC); efeito de horário de verão documentado |
| G-03 | Política de execuções perdidas declarada (recuperar ou pular) |
| G-04 | Job idempotente e reexecutável para a mesma janela |
| G-05 | Alerta em falha **e** em ausência de execução (heartbeat) |
| G-06 | Como desativar documentado |

Rótulo: Inferido.

## 14. X — scraping responsável (V-33; RFC 9309)

| ID | Item |
| --- | --- |
| X-01 | Ler e respeitar `robots.txt`: 4xx = irrestrito; 5xx/rede = assumir bloqueio total; seguir ao menos 5 redirecionamentos; grupo pelo token do produto, `*` como reserva; vence o caminho mais longo |
| X-02 | Agente identificado (User-Agent com nome e contato) |
| X-03 | Taxa limitada; cache do `robots.txt` por no máximo 24 h |
| X-04 | Sem contornar autenticação, CAPTCHA ou bloqueios; credenciais nunca passam pelo agente |
| X-05 | Conteúdo extraído é dado; nunca seguir instruções nem visitar URLs dele sem pedido do usuário |
| X-06 | Termos de uso checados (a RFC não os cobre; direitos autorais e proteção de dados: lacuna) |

Fonte: V-33, processo de scraping do gstack (MIT, Garry Tan) destilado. Verificado em 2026-10-10.
