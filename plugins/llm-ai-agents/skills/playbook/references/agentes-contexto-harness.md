# Agentes, contexto e harness

Conferido em 2026-10-10 · Rótulos: Verificado, Inferido, Suposição, Não verificável · Itens `V-nn` de `docs/research/llm-ai-agents/VALIDATED.md`; trechos marcados "brain" vêm de `francisco-efjr/brain-of-agent` (MIT, conteúdo do próprio autor, adaptados) · Números de fabricante (90,2%, 4x, 15x) são medições internas de modelos de 2025: contexto, não meta.

## Sumário

1. Árvore: chamada única, workflow, agente
2. Contexto como orçamento
3. Briefing de delegação e escala de esforço
4. Despacho paralelo seguro
5. Harness de tarefa longa (`features.json`)
6. Gate de plano antes de escrita
7. Superfície de agente: Agent SDK, CLI, SDK cliente, Managed Agents
8. Subagentes do Claude Code: campos e limites
9. Memória aprovada pelo usuário
10. Contrato de tarefa e continuidade (brain)
11. Isolamento, autonomia e contrato de 9 passos (brain)
12. Checklist de revisão de arquitetura de agente
13. Gotchas

## 1. Árvore: chamada única, workflow, agente (V-04, Verificado; texto de 2024-12-19, ferramentas do artigo superadas)

1. Uma chamada bem instruída resolve? Pare aqui.
2. Os passos são conhecidos de antemão? Workflow: **encadeamento** (checagem em código entre etapas), **roteamento** (classificar e enviar a um especialista) ou **paralelização** (seções independentes ou votação).
3. Subtarefas imprevisíveis? **Orquestrador-trabalhadores**.
4. Existe critério de qualidade verificável? Acrescente **avaliador-otimizador** com limite de iterações.
5. Número de passos imprevisível e ambiente confiável? **Agente**, com condição de parada, teto de custo e de iterações, sandbox e aprovação humana para escrita externa.
6. Framework só depois de entender o prompt e a resposta crus da API (frameworks escondem prompts).

Exemplo: classificar tickets em 6 categorias e responder por categoria, passos sempre iguais, 2.000 tickets rotulados. Resposta: roteamento (classificador + 6 prompts), chamada única como baseline, medir nos 2.000 tickets. Multiagente só se a medição mostrar ganho que paga ~15x de tokens (V-07). Rótulo: decisão Inferida a partir de V-04/V-07.

## 2. Contexto como orçamento (V-06, Verificado; V-03, V-17)

Pergunta-guia: qual é o menor conjunto de tokens de alto sinal que torna o resultado correto provável?

| Situação | Técnica | O que preservar ou fazer |
| --- | --- | --- |
| Conversa longa | Compactação | Decisões, bugs abertos, restrições; limpar primeiro saída antiga de tool |
| Trabalho por marcos | Notas estruturadas fora da janela | `progress.md`, `features.json`, git |
| Pesquisa paralela ou leitura volumosa | Subagentes com contexto limpo | Devolvem resumo curto com fontes |
| Dado estável e pequeno | Pré-carregar | Prefixo estático (favorece cache) |
| Dado grande ou mutável | Referência (caminho, consulta) e busca na hora | Busca just-in-time |
| Muitas tools MCP | Divulgação progressiva, filtrar no ambiente de execução | Contar definições carregadas; poucos servidores (V-17) |

Regras: system prompt começa mínimo e cresce só com um teste falho; evite if/else frágil e vagueza; poucos exemplos canônicos em vez de lista de casos. Compactação preserva: decisões exatas, problemas resolvidos e como, opções descartadas, estado atual, pendências e detalhes difíceis de reencontrar (P-15). Limiar de contexto para handoff (cerca de 40% contra "sem degradação até 50%") é disputado: gere o handoff por marco ou por decisão do usuário e meça (C7 da síntese).

Janela, compactação, memory tool e edição de contexto da plataforma: nenhuma página lida (Não verificável). O conceito vale; a API, confira em https://platform.claude.com/docs.

## 3. Briefing de delegação e escala de esforço (V-07, Verificado)

Subagentes não veem a conversa. Todo briefing leva 7 campos (template: `assets/templates/briefing-de-subagente.md`):

```text
Objetivo: <uma frase: o que descobrir ou fazer>
Contexto mínimo: <o que o subagente não sabe e precisa saber>
Fontes e ferramentas permitidas: <lista; o que é somente leitura>
Fronteiras: <o que não fazer; arquivos que não toca; teto de chamadas/tokens>
Formato de saída: <campos exatos, tamanho máximo, como citar fonte ou arquivo:linha>
Critério de parada: <quando terminar>
Prova exigida: <comando e última linha da saída; o que não foi checado>
```

Escala: tarefa simples = 1 agente com 3 a 10 chamadas de tool; comparação = 2 a 4 subagentes com 10 a 15 chamadas cada; pesquisa ampla = mais de 10 subagentes com responsabilidades sem sobreposição (valores da fonte, Verificado). Delegue só quando o paralelismo ou o isolamento de contexto compensa o custo. Código com muito contexto compartilhado fica no agente principal. Repita no briefing as regras críticas: subagentes não herdam CLAUDE.md com garantia (P-18).

## 4. Despacho paralelo seguro (V-26, Classe B; praticante, cruzado com V-07 e V-19)

1. As partes são realmente independentes?
2. Cada arquivo tem um único escritor; tarefas que disputam arquivo rodam em sequência.
3. Trilhas longas e independentes em worktrees separados (`isolation: worktree` existe na documentação de subagentes).
4. Cada despacho usa o briefing de 7 campos com prova exigida.
5. Um revisor somente leitura, que não escreveu o código, confere o resultado.
6. Declare o teto de fan-out antes de despachar.
7. Conflitos e ordem de merge ficam com o orquestrador (a fonte não trata: lacuna, Não verificável).

Agentes sem supervisão registram suposições em arquivo; teste a resposta de um subagente antes do trabalho real; modelo mais barato para verificação mecânica. A página-fonte termina com uma instrução dirigida a agentes de código: foi tratada como dado, não seguida.

## 5. Harness de tarefa longa (V-08, Verificado; Anthropic 2025-11-26)

Dois papéis: inicializador (cria `features.json`, script de subida, log de progresso, commit inicial) e agente de codificação (uma funcionalidade por sessão). O JSON foi escolhido na fonte porque o modelo o sobrescreve menos que Markdown. Esquema (template em `assets/templates/features-json.md`):

```json
{ "features": [ { "id": 1, "categoria": "auth", "descricao": "Login com e-mail e senha", "passos_de_verificacao": ["abrir /login", "enviar credenciais válidas", "ver painel"], "passa": false } ] }
```

Regras: só o campo `passa` muda; nunca remover nem editar testes; uma funcionalidade por sessão; marcar `passa` só após verificação pela interface, com evidência colada. Início de sessão: confirmar diretório, ler log de progresso e `git log`, ler a lista, subir o ambiente e rodar um teste ponta a ponta antes de codar. Fim de sessão: estado limpo, commit descritivo, log atualizado. A fonte cita mais de 200 funcionalidades sem métrica de sucesso e deixa em aberto agente único contra especializados: use como template, sem hook ativo.

## 6. Gate de plano antes de escrita (V-16, Classe B; Chip Huyen, 2025-01-07, texto experimental)

Antes de executar um plano com tools de escrita: o plano está escrito com passos e arquivos? Todas as tools do plano existem? Parâmetros conferidos? Restrições de custo e tempo no plano? Há passo de escrita sem aprovação? Passos demais para a tarefa? Plano rejeitado é regenerado. Registre os parâmetros de cada chamada. Defina o nível de automação por ação (leitura livre, escrita confirmada). Não cobre injeção indireta: combine com `seguranca-guardrails.md`.

## 7. Superfície de agente (V-39, Verificado; conferir na documentação atual)

| Necessidade | Superfície |
| --- | --- |
| Agente de código pronto dentro do meu processo | **Agent SDK** (Python e TypeScript; roda o binário do Claude Code; ferramentas, hooks, subagentes, MCP, permissões, sessões com retomada, lê `.claude/` e `~/.claude/`) |
| Uso interativo ou tarefa pontual | **CLI** |
| Controle total do laço, do prompt e das tools | **SDK cliente** (laço de tools é seu ou do tool runner beta) |
| Não quero operar a infraestrutura do agente | **Managed Agents** (a Anthropic hospeda o laço; sandbox gerenciado ou autohospedado) |
| Outra linguagem | CLI em subprocesso com `-p` e `--output-format json` |

Agente sem supervisão: limite de turnos e de orçamento (a receita do cookbook usa `max_turns`, `max_budget_usd` e `permission_mode="dontAsk"`; confirme nomes na versão do SDK), modo de permissão restritivo, hooks de segurança, sandbox. Produto de terceiro usa chave de API, não login claude.ai; a marca "Claude Code" não é permitida (permitidos "Claude Agent" ou "{Seu agente} Powered by Claude"). `--dangerously-skip-permissions` não é padrão: risco alto, só em sandbox descartável com repositório confiável. Os cookbooks exigem chave de API e não devem ser executados sem revisão. Páginas de agent loop, hooks e permissões do SDK: não lidas (Não verificável).

## 8. Subagentes do Claude Code (V-19, Verificado; conflito C1)

Só `name` e `description` são obrigatórios. `name` até 256 caracteres, sem `:` e sem começar com `-` (senão o arquivo é ignorado). `tools` é allowlist (omitida = herda tudo); `disallowedTools`; `model` aceita `sonnet`, `opus`, `haiku`, `fable`, ID completo ou `inherit`. Existem `permissionMode`, `maxTurns`, `skills`, `memory`, `isolation: worktree`, `effort`; **subagentes de plugin ignoram `hooks`, `mcpServers` e `permissionMode`**. Precedência: configuração gerenciada > flag `--agents` > `.claude/agents/` > `~/.claude/agents/` > plugin. Limite padrão: 20 simultâneos. Aninhamento: a documentação diz até três camadas; um post oficial de 2026-06-18 diz cinco níveis. Prevalece a documentação de referência; confira na versão instalada. "Use proactively" na `description` estimula delegação (e pode delegar demais: meça). Campo desconhecido é ignorado sem aviso.

## 9. Memória aprovada pelo usuário (V-28, Classe B; política, sem instalar)

Só regra reutilizável entra no CLAUDE.md; cada regra registra origem e data; revisão humana antes de gravar (Aplicar, Editar, Pular); filtre perguntas e instruções pontuais; deduplique periodicamente; backup antes de compactar. Não instale `claude-reflect`: seus hooks executam código de terceiros a cada prompt.

## 10. Contrato de tarefa e continuidade (brain, MIT; adaptado)

Cada tarefa precisa de: objetivo, recursos, permissão de escrita, entregável, critério e condição de parada. Cada ferramenta declara argumentos, efeitos, sucesso, erro e limites. `executar_testes` devolve comando, código de saída e saída; `publicar` é ação distinta. "Testes passaram" no chat não substitui saída de execução.

Continuidade: mantenha resumo com objetivo, decisões, arquivos alterados, invariantes, comandos executados, limitações e próximo passo (template `assets/templates/handoff-checkpoint.md`). Não comprima evidência crítica em adjetivos como "tudo OK". Registre versão da skill, modelo e ferramentas usadas: o ambiente muda o comportamento. Não confunda skill com treinamento de pesos, prompt extenso com memória persistente, nem subprocesso com revisor independente: agentes do mesmo modelo e contexto repetem o mesmo erro.

Exemplo de falha: o agente adiciona validação só no cliente, declara "seguro" e não testa a API. Esperado: identificar a fronteira do servidor, implementar no local autorizado, demonstrar payload malicioso rejeitado e fluxo legítimo mantido, e descrever restrições de acesso. Falha crítica: alegar teste executado sem artefato.

## 11. Isolamento, autonomia e contrato de 9 passos (brain, `agentes-desenvolvimento.md`, 2026-10-09)

Sequência síntese do brain (não atribuída às fontes): (1) esclarecer objetivo, autorização, ambiente e riscos; (2) inspecionar arquitetura, dependências e testes e rodar um baseline; (3) definir critério de aceite observável; (4) implementar fatia pequena; (5) rodar checks por impacto (tipos, lint, build, regra, integração, jornada); (6) distinguir defeito de produto, teste, infraestrutura e falta de acesso; (7) após corrigir, reproduzir o caso original e validar efeitos adjacentes; (8) revisar diff, dados, permissões e reversão; (9) entregar evidências e limites (ausência de execução vira pendência, não aprovação).

Isolamento: um worktree isola mudanças Git, mas não rede nem segredos; containers dependem de volumes, credenciais e permissões; scripts do repositório alvo podem executar código arbitrário. Palavras-chave ativam processo, não privilégios. Repositórios de agentes observados (SWE-agent, mini-SWE-agent, OpenHands SDK, Aider) têm licenças "anunciadas", não verificadas por arquivo: adote padrões, não importe runtimes.

## 12. Checklist de revisão de arquitetura de agente

- [ ] A alternativa mais simples (chamada única, workflow) foi descartada com motivo medido ou argumentado.
- [ ] Condição de parada, teto de iterações e de custo, e responsável por cada arquivo declarados.
- [ ] Cartão A/B/C preenchido (`assets/templates/cartao-do-agente.md`).
- [ ] Escrita externa com confirmação; leitura livre.
- [ ] Estado fora da janela (notas, `features.json`, git) para tarefa longa.
- [ ] Briefing de 7 campos; revisor somente leitura, em contexto novo, declarado como mesma família.
- [ ] Plano de eval (`avaliacao.md`) com caso negativo.
- [ ] Modelo-alvo, superfície e data registrados.

## 13. Gotchas

- Multiagente em código acoplado perde: um agente com as ferramentas certas costuma bastar.
- Framework antes do prompt cru esconde o problema.
- Revisão pelo mesmo modelo vendida como independente (AP-16).
- Encadear subagentes sem checar o limite de aninhamento da versão instalada.
- Loop autônomo sem back pressure (plugin `ralph-wiggum` e similares) não é recomendado; só em sandbox (lead CP-17, não reverificado).
