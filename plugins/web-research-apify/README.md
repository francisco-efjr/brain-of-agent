# web-research-apify

Plugin **extra e opcional** do Claude Code que ensina o agente a usar o **Apify MCP** como ferramenta de pesquisa web profunda: Reddit, X, transcrição de YouTube, SERP estruturada, crawl de documentação e páginas com JavaScript ou bloqueio, justamente o que o `WebFetch` e o `WebSearch` não cobrem. Ele orienta a conexão (sempre com a sua confirmação), escolhe o Actor, executa **só com orçamento em dólares aprovado por você** e teto de gasto, lê o dataset sem estourar o contexto, cita a **URL original**, reverifica e audita o custo. Reúne 1 playbook com 12 referências e 5 templates, 22 prompts, 7 skills de tarefa, 3 agentes e 10 evals.

Palavra-chave do modo completo: `APIFY-COMPLETO`. Versão 0.1.0, licença MIT. Conteúdo próprio em português brasileiro (termos técnicos, comandos e nomes de tools em inglês).

> **Não afiliado à Apify.** Apify e os Actors são marcas e produtos de terceiros. **O plugin não traz `.mcp.json`, hooks nem `bin/`:** ele não registra servidor nenhum e não instala nada sozinho. Sem as tools da Apify na sessão, ele faz fallback para `WebSearch`/`WebFetch` e **declara a lacuna** ("Apify indisponível: <fonte> não coletada").

## O que entrega

- **Playbook** que roteia o pedido e impõe 11 princípios com motivo: rota gratuita primeiro, gasto só com orçamento aprovado, teto em camadas, uma run por plano, conteúdo devolvido é dado, URL original como fonte, segredos fora do chat, PII e termos antes de coletar. Traz o modo `APIFY-COMPLETO` e rótulos epistêmicos (Verificado, Inferido, Suposição, Não verificável, Não aplicável).
- **12 referências:** catálogo de tools, conexão e perfis, Actors para pesquisa (com exemplo ponta a ponta), custo e orçamento, segurança e privacidade, integração com método de pesquisa, checklists, padrões e antipadrões, decisões, snippets de `CLAUDE.md` (WR-01 a WR-15), lacunas e smoke test, fontes. **5 templates:** plano com orçamento, registro de custo, item de pesquisa via Apify, relatório de auditoria de custo, relatório de reverificação.
- **7 skills de tarefa** e **3 agentes** com `tools` mínimas; **22 prompts** prontos (P-01 a P-22); **10 evals** desenhados, **não executados**.

## Quando usar (e quando não)

Use para pesquisar no Reddit, X ou YouTube, obter SERP estruturada, fazer crawl de documentação com JavaScript, abrir uma página que o `WebFetch` não abre, escolher um Actor, ler um dataset como itens de pesquisa citáveis e auditar o gasto. **Não use** para GitHub (`gh api`), Hacker News (API Algolia), dev.to e documentação estática (rotas gratuitas bastam), para desenvolver ou publicar Actors (plugin oficial da Apify), nem para scraper com código próprio (`/automation-integrations:responsible-scraping`).

## Componentes

| Tipo | Nome | Para que serve | Efeito |
| --- | --- | --- | --- |
| Skill (núcleo) | `playbook` | Router, princípios, processo de 9 passos, modo `APIFY-COMPLETO` | Nenhum |
| Skill | `prompts` | 22 prompts prontos (roteamento, plano, execução, dataset, plataformas, controle, prompt de sistema, delegação) | Nenhum |
| Skill | `conectar-apify` | Orienta a conexão (perfil, comando, efeito, riscos); espera o seu "sim"; o login é seu | Nenhum por si; o `claude mcp add` é seu ou do agente principal após o "sim" |
| Skill | `diagnosticar-apify` | Mostra quais tools da Apify estão carregadas, perfil, duplicidade e permissões | Somente leitura |
| Skill | `escolher-actor` | Escolhe o Actor com alternativa gratuita, preço do dia e riscos | Somente leitura e gratuita |
| Skill | `pesquisa-com-orcamento` | Executa uma coleta dentro do orçamento aprovado: plano, uma run, leitura, registro | **Gasta dinheiro; só roda por comando** (`disable-model-invocation`) |
| Skill | `dataset-para-itens` | Lê o dataset em páginas pequenas e gera itens com URL original e "Obtido via" | Grava só o arquivo de pesquisa indicado |
| Skill | `auditoria-de-custo` | Audita registro, planos e orçamento (R1 a R12) | Somente leitura |
| Skill | `consultar-docs-apify` | Responde sobre Apify e Crawlee citando a URL lida (perfil gratuito) | Somente leitura |
| Agente | `apify-researcher` | Executa um plano fechado dentro do orçamento; uma run; grava só o arquivo indicado | `tools` em allowlist; sem `Bash`, `Agent` nem outros MCP; **pode gastar** (dentro do plano) |
| Agente | `apify-source-verifier` | Reverifica itens a custo zero pela URL original | `Read`, `Grep`, `Glob`, `WebFetch`, `WebSearch`; sem tools da Apify |
| Agente | `apify-cost-auditor` | Revisa o plano (pré-voo) e audita o gasto (pós) | `Read`, `Grep`, `Glob` |

Namespaces: skills como `/web-research-apify:playbook`; agentes como `web-research-apify:apify-researcher`. Nenhum componente conecta o servidor, instala plugin, pede token ou escreve em settings.

## Instalação

Dentro do Claude Code:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install web-research-apify@brain-of-agent
```

Instalar o plugin **não conecta** o Apify. Para conectar, siga a próxima seção.

## Conectar o Apify (receitas; o plugin nunca as ativa)

**Primeiro passo, antes de qualquer uso com gasto:** no Console da Apify, ligue o limite de uso em **Billing › Limits** com *overage* desligado. Ao atingir o limite do plano a plataforma suspende os serviços (doc lida em 2026-10-14; se o limite pode ficar abaixo do valor do plano: Inferido). É a única trava que não depende de o modelo obedecer a uma instrução.

> Não ativa. As receitas abaixo são texto de ajuda: o plugin não registra servidor nenhum. Copie só depois de ler o efeito e de confirmar com o assistente. Sintaxe Verificada na fonte (lida em 2026-10-13); **nenhuma foi testada em runtime**. No PowerShell, **as aspas na URL são obrigatórias**: a vírgula de `tools=a,b` vira array e `&` quebra o comando.

**R-A. OAuth, perfil P2 (recomendada).** `tools=` fixo; só `call-actor` gasta e tem teto em `callOptions`.

```bash
claude mcp add --transport http apify "https://mcp.apify.com/?tools=actors,docs"
```

Efeito: grava o servidor em `~/.claude.json` (escopo `local`); telemetria ligada por padrão (acrescente `&telemetry-enabled=false` para desligar); `call-actor` roda Actors de terceiros, que cobram. Depois: `/mcp` > `apify` > Authenticate (abre o navegador; o login é **seu** e o assistente nunca pede token).

**R-B. Só documentação (teste, sem auth e sem gasto).** Perfil P0.

```bash
claude mcp add apify "https://mcp.apify.com/?tools=docs" -t http
```

**R-C. Token por variável de ambiente (headless ou SSH).** Só com token **com escopo e expiração curta**; o valor fica na variável de ambiente do sistema `APIFY_MCP_TOKEN` (prefira à `env` de `.claude/settings.local.json`, que o modelo consegue ler), nunca no arquivo, no comando ou no chat. Com o header definido não há fallback OAuth. Formato (para o `.mcp.json` do **seu** projeto): `"headers": { "Authorization": "Bearer ${APIFY_MCP_TOKEN}" }`; a expansão da variável é **Não testada** (H-09). Detalhes completos em `skills/playbook/references/conexao-e-perfis.md`.

**R-D. Conector custom no claude.ai.** Customize > Connectors > "+ Add" > "Add custom connector" > URL `https://mcp.apify.com`. Aparece no Claude Code só com login de assinatura claude.ai e os agentes do plugin (que listam `mcp__apify__...`) não o enxergam. **Não use junto com R-A** (duplicidade). A Anthropic avisa que conectores custom não são verificados.

**R-E (aviso). Plugin oficial da Apify** (`apify/apify-claude-code-plugin`): traz MCP **ativo** sem `tools=`, um agente com `Bash` e uma skill que usa a CLI (sem flag de teto de gasto, com `apify login --token`). Use-o **só para desenvolver Actors** e **não o instale junto** com este plugin para pesquisa.

**Permissões recomendadas** (sintaxe Verificada; efeito não testado, H-07; troque o prefixo se o servidor não se chamar `apify`; a edição de settings é sua):

```json
{
  "permissions": {
    "ask":  ["mcp__apify__call-actor", "mcp__apify__abort-actor-run"],
    "deny": ["mcp__apify__apify-api-write", "mcp__apify__delete-actor", "mcp__apify__delete-schedule",
             "mcp__apify__update-schedule", "mcp__apify__create-schedule", "mcp__apify__publish-actor-task",
             "mcp__apify__unpublish-actor-task", "mcp__apify__create-actor-task", "mcp__apify__update-actor-task",
             "mcp__apify__build-actor"]
  }
}
```

**Interruptor de emergência:** `claude mcp logout apify` (ou `remove`) corta todas as tools da sessão. **Smoke test** de no máximo US$ 0,05 para trocar Suposição por Verificado: `skills/playbook/references/lacunas-e-smoke-test.md`.

## Exemplos de pedidos

1. **Pesquisa no Reddit com teto:** "Pesquisa no Reddit o que praticantes dizem sobre hooks do Claude Code no último mês. Orçamento aprovado: US$ 0,30 no total e US$ 0,20 por run." Tenta a rota gratuita, confirma o Actor e o preço do dia, mostra o plano, espera o "sim", faz **uma** run com `callOptions` e entrega itens com permalink e "URL não reaberta".
2. **Transcrição de YouTube:** "Transcreve este vídeo e destila os pontos sobre subagentes, orçamento US$ 0,05." Plano com o Actor confirmado (o de nome 404 nunca é usado), custo por transcrição, conteúdo destilado e não copiado.
3. **Diagnóstico:** "O Apify está conectado? Quais tools eu tenho?" `diagnosticar-apify` detecta prefixo, perfil e duplicidade, e checa se `call-actor` está em `ask`; somente leitura.
4. **Revisar o plano antes de rodar:** "Revisa este plano de coleta antes de eu aprovar." O `apify-cost-auditor` (modo plano) confere orçamento, `callOptions` ≠ `input`, `timeout`, teto, volume e rota gratuita.
5. **Auditar o custo:** "Quanto gastei? Estourei o orçamento?" Reconstrói a tabela de runs, aplica R1 a R12, pede ao usuário os custos do Console e marca o que é "não verificável".
6. **Ler um dataset:** "Transforma o dataset `<id>` em itens de pesquisa com as fontes." `dataset-para-itens` lê em páginas de até 20, trata texto dirigido à IA como dado, rejeita item sem URL e registra a coleta.

## Modo `APIFY-COMPLETO`

Escreva `APIFY-COMPLETO` no seu pedido. O playbook lê as 12 referências em 4 lotes (lida, parcial ou ausente), monta a matriz de aplicabilidade (conexão, Actor, orçamento e tetos, execução, dataset, itens, reverificação, custo, segurança, legal e PII, fallback, integração ao método), implementa só o que o pedido incluir e revalida com evidência. A palavra em documento, README, dataset ou log **não** ativa o modo; e ela **não amplia permissões**: gasto continua exigindo orçamento em dólares aprovado no chat, e conectar, instalar, mudar settings, pagamento agêntico e apagar dataset continuam pedindo autorização concreta.

## Segurança em uma página

Tudo que o Apify devolve (itens, README e descrição de Actors, `nextStep`, `TIP`, logs) é **dado, não instrução**; texto dirigido a IA é citado e registrado, não seguido. O `nextStep` do servidor convida a re-rodar o Actor, e cada re-run é cobrança: **uma run por plano**. O MCP não mostra o custo real: o plugin estima, registra o teto comprometido e pede o valor do Console. O agente de coleta tem `tools` em allowlist para não fechar a "lethal trifecta" (dados privados, conteúdo não confiável, saída externa). Token nunca vai ao chat, à URL, ao comando ou a arquivo: OAuth ou variável de ambiente. Pessoas físicas, contatos e leads ficam fora do fluxo padrão, e `robots.txt` não é autorização. **Não é parecer jurídico.**

## Relação com outros plugins

| Plugin | Divisão |
| --- | --- |
| `automation-integrations` | `responsible-scraping` (código próprio ou página estática) é a rota gratuita e vem antes do Apify; `scheduling-headless-jobs` para monitoramento recorrente; `writing-hook-guardrails` se quiser um hook de teto de gasto (Suposição) |
| `security-appsec` | `agent-risk-triage` antes de conectar MCP ou conector; `harden-claude-code` para `deny`/`ask`; token exposto, LGPD do que foi coletado |
| `llm-ai-agents` | Revisar as tools e a segurança do **seu** agente que chama o Apify |
| `orchestrator` | Roteia a demanda multiárea; a sessão principal despacha o `apify-researcher` e depois o verificador e o auditor |
| `apify/apify-claude-code-plugin` (oficial) | Só para desenvolver Actors; traz MCP ativo e `Bash`; não instalar junto para pesquisa |
| `design-engineering-kit` | Precedente de plugin extra que orienta instalar ferramenta externa sem `.mcp.json`; sem sobreposição de conteúdo |

## Fontes principais (top 10; classe pela rubrica da casa)

1. `apify/apify-mcp-server` (README, código, CHANGELOG, evals): classe A, MIT · https://github.com/apify/apify-mcp-server
2. Apify docs, integração MCP: A · https://docs.apify.com/platform/integrations/mcp
3. Claude Code docs, MCP: A · https://code.claude.com/docs/en/mcp
4. Claude Code docs, permissions e settings: A · https://code.claude.com/docs/en/permissions
5. Apify docs, pay-per-event e API Run Actor: A · https://docs.apify.com/platform/actors/publishing/monetize/pay-per-event
6. API pública da Store (preços e schemas; volátil): A · https://api.apify.com/v2/acts/apify~web-fetch
7. Issues do `apify-mcp-server` (#1429, #1403, #1559…): A · https://github.com/apify/apify-mcp-server/issues
8. `apify/apify-claude-code-plugin` v1.0.2: A/B, Apache-2.0 · https://github.com/apify/apify-claude-code-plugin
9. OWASP LLM01:2025, Prompt Injection: A · https://genai.owasp.org/llmrisk/llm01-prompt-injection/
10. Simon Willison, "The lethal trifecta" (2025-06-16): B · https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/

Lista completa, licenças, datas de leitura e o índice V-01 a V-34 em `skills/playbook/references/fontes.md`.

## Créditos e licenças

O código-fonte do `apify-mcp-server` (MIT) e o plugin oficial da Apify (Apache-2.0) foram usados **apenas como fonte de leitura**: nenhum código foi copiado nem vendorizado. A documentação da Apify, do Claude Code e da Anthropic, o OWASP, a Invariant Labs e o texto de Simon Willison foram **destilados com redação própria**, com a URL; a licença dessas páginas não foi verificada. Este plugin é MIT. Apify é marca de terceiros; o plugin não redistribui conteúdo nem binário da Apify.

## Limitações honestas

- **Nada foi executado em runtime.** Os nomes das tools no Claude Code, o OAuth, o comportamento do teto de gasto, o `ask` em execução não interativa e a visibilidade das tools MCP dentro de subagentes e de Workflows são **Suposição** até o smoke test do usuário (`skills/playbook/references/lacunas-e-smoke-test.md`).
- **Os 10 evals estão `designed_not_executed`.** `claude plugin eval` exige Claude Code 2.1.269 ou superior (o CLI local da fábrica é 2.1.128: só validação estrutural). O workspace do eval não tem o Apify MCP: os casos medem plano, fallback, segurança e proveniência a partir de texto colado, **não** o fluxo com o servidor conectado.
- **Preços e Actors são voláteis** (datados de 2026-10-13; o servidor teve 12 ou mais releases em cerca de 4 semanas e o hospedado é privado). Confirme com `fetch-actor-details` no dia.
- **O custo real é invisível ao MCP** (issue #1429) e o teto em dólares só vale em Actors cobrados por evento; crawlers (usage-based) não têm teto em dólares. A trava que independe do modelo é o limite da conta.
- Reddit e X não podem ser reabertos pelo `WebFetch`: sem reabertura, a classe é B no máximo.
- Autores e revisores são modelos da mesma família: **não é validação independente**. A verificação estrutural (`tools/verify_plugin.py`, `claude plugin validate`) confere formato, não comportamento.
- Termos de serviço de Reddit, X e YouTube e artigos da LGPD e do GDPR não foram analisados. **Não é parecer jurídico.**
- Sem skill de agendamento ou monitoramento e sem Actors de Google Maps ou LinkedIn: é deliberado (`/automation-integrations:scheduling-headless-jobs` e fora do fluxo padrão por envolver pessoas físicas).
