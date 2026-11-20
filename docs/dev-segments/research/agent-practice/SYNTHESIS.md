# SYNTHESIS — agent-practice (guia obrigatório de prática com agentes)

Data: 2026-11-19. Pedido do dono do repositório: transformar todo o "fazer" e "não fazer" do livro *Competente o Suficiente* (Fabio Akita, 2026) em regras obrigatórias do Brain of Agent, aplicadas pelo orquestrador em toda invocação conforme o contexto, com uma skill de invocação.

## Decisões de desenho

| # | Decisão | Por quê | Alternativa descartada |
| --- | --- | --- | --- |
| D1 | Plugin `agent-practice` na fábrica, publicado por `publish_brain.py` | Mesmo caminho de todo conhecimento adquirido (tag, catálogo, marketplace, validação); instalável no Claude Code e legível por link | Brain próprio em `brains/`: exigiria mudar `tools/verify.py` e testes, que têm alterações locais não commitadas do dono |
| D2 | Obrigatório pelo `ORCHESTRATOR.md` §0.1, não só por tag | A tag só dispara quando o pedido fala do tema; o pedido é que o guia valha sempre | Só tag curada |
| D3 | 386 regras com ID estável por área (MET, PED, CTX, ENG, VER, REV, SEG, OPS, LLM, AVA/CUS, ORG, PES), alvo `[A] [H] [A+H] [O] [P]` e contextos C0–C14 | "Tudo à risca" precisa de item verificável um a um; o alvo diz quem cumpre; o contexto diz quando | Resumo por capítulo (reproduziria a estrutura do livro e não diz quando aplicar) |
| D4 | Matriz contexto → regras gerada a partir das próprias regras | Fonte única; nenhuma regra fora da matriz | Matriz escrita à mão |
| D5 | Núcleo C0 com 34 regras; demais por contexto, com contexto dinâmico | Equilibra rigor e custo de contexto; ação destrutiva no meio do trabalho ativa o C6 na hora | Carregar as 386 regras sempre (custo e diluição de atenção, contra CTX-14) |
| D6 | Portões G0–G6, com G4 (destrutivo) bloqueante | Transforma regras em listas de conferência com saída; o livro mostra que a falha grave veio de premissa não conferida | Regras soltas sem ponto de checagem |
| D7 | `CONFORMIDADE.md` + linha no chat + `conformance-auditor` | Aplica ao próprio guia o método do livro: quem faz não confere a si mesmo | Autodeclaração de conformidade |
| D8 | Regra `[H]` nunca é dada como atendida pelo agente | O §0 dá autonomia, mas aprovação humana não se simula; vira decisão pendente sem travar o resto | Bloquear todo o trabalho até o humano responder |
| D9 | O guia não amplia permissões; precedência do §2 B e §5 | Coerência com o protocolo e com o estilo da casa | Guia com permissões próprias |
| D10 | Redação própria, referência por capítulo, notas dos leitores não publicadas, checagem automática de sobreposição literal | O livro proíbe reprodução e obra derivada; ideias e métodos podem ser reescritos com atribuição | Publicar resumos por capítulo ou citações |
| D11 | Leitura em 8 trechos por leitores Sonnet e síntese em Opus; construção de skills, agentes, prompts e evals por 2 construtores Sonnet; validação de qualidade independente | Gestão de tokens pedida pelo dono e padrão da fábrica (modelos por camada) | Um único contexto lendo ~250 mil tokens |

## Componentes

- `skills/playbook` (invocação; router, princípios, processo G0→G6, bloco do guia para subagentes, mapa de conhecimento, modo `PRATICA-COMPLETO`) e 20 referências: 12 arquivos de regras, matriz, portões, decisões, snippets para `AGENTS.md`, fontes e três índices do blueprint (listas de conferência, padrões e antipadrões, ferramentas).
- 9 skills de tarefa: `especificar-pedido`, `definir-oraculo`, `guardar-destrutivo`, `kit-seguranca-agente`, `memoria-do-projeto`, `revisar-codigo-de-ia`, `avaliar-modelo`, `checar-conformidade`, `adotar-ia-no-time`; mais `prompts`.
- 5 agentes: `conformance-auditor`, `destructive-ops-guard`, `oracle-designer`, `claims-verifier`, `agent-environment-auditor`.
- 6 templates: conformidade, pedido em quatro partes, plano destrutivo, passagem de turno, `AGENTS.md` de projeto, relatório de avaliação de modelo.
- 10 evals (`designed_not_executed`).

## Integração

- `ORCHESTRATOR.md`: cabeçalho, novo §0.1, linha no mapa (§1), item 7 do bloco de limites (§2 B), passos 2, 4, 6 e 7 do §3, §3.1 (oráculo antes e `CONFORMIDADE.md`), §4, §5, §6 (item 6 e linha do guia na mensagem final) e §7. Cópia idêntica em `plugins/orchestrator/skills/playbook/references/protocolo.md`.
- Plugin `orchestrator` 0.5.0: playbook, `demand-router`, prompt O-08 e README.
- Tags curadas: `pratica-com-agentes`, `operacao-destrutiva`, `kit-seguranca-agentes`, `avaliacao-de-modelos`; rotas de fundamentos acrescentadas em `contexto-agente` e `revisao-de-codigo`.
- Raiz do brain: `SKILL.md`, `CLAUDE.md`, `AGENTS.md`, `README.md`, `THIRD_PARTY_NOTICES.md`.

## Validação

- Primeira rodada da validação independente (Opus, `BUILD-REPORT-quality.md`): reprovado por um bloqueio (`allowed-tools` com `Bash` livre em `revisar-codigo-de-ia`), com 1 defeito alto, 9 médios e 15 baixos; fidelidade de 24 em 24 regras amostradas contra o livro.
- Os 25 defeitos foram corrigidos (escopo do C6, `.env` nunca aberto, aprovação só citada do chat, conformidade proporcional e no chat sem autorização de escrita, semântica de `[A+H]`, kit de sete peças único, linhas `Guia:` canônicas) e devolvidos ao mesmo validador para revalidação (seção 13 do relatório).
- Checagem determinística de sobreposição literal: nenhuma sequência de 7 ou mais palavras idêntica ao livro, fora o título na citação bibliográfica e uma fórmula genérica de 7 palavras num grader.

## Riscos e limites

- Regras de um autor e de 2026; o próprio guia manda medir antes de generalizar (AVA-02) e datar números (MET-07).
- Rigor maior aumenta o custo por tarefa; mitigação: contextos por proporcionalidade e núcleo C0 enxuto.
- Evals não executados; nenhuma taxa de acerto pode ser alegada.
- A validação é feita por modelos (autor Opus, construtores Sonnet, validador independente); não houve revisão humana do conteúdo.
