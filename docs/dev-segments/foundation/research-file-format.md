# Formato dos arquivos de pesquisa

Pesquisador escreve `docs/research/<slug>/<lente>.md`. Validador escreve `docs/research/<slug>/<lente>.validated.md`. Lentes por segmento: `authoritative` (Anthropic + docs oficiais/normas + sites reconhecidos), `github` (repositórios), `community` (redes sociais, fóruns, blogs de praticantes, vídeos, newsletters). Pesquisa global usa `docs/research/_global/<tema>.md`.

## Estrutura do arquivo do pesquisador

```markdown
# <Segmento> — lente <lente>

Data: 2026-10-09 · Agente: pesquisador (<modelo>) · Consultas executadas: N · Páginas lidas: M

## Estratégia de busca
- Consultas usadas (lista literal), filtros, domínios priorizados e por quê.

## Mapa de cobertura
| Subtema do segmento | Itens encontrados | Lacuna? |

## Itens
### R-<lente>-01 — <título curto>
- **Tipo:** prompt | system-prompt | skill | subagent | command | claude-md-rule | checklist | workflow | pattern | anti-pattern | reference
- **Fonte:** <URL exata observada> · **Autor/Org:** ... · **Classe:** A/B/C (nota 0–10)
- **Sinais:** ★ observadas / engajamento / data de atualização / licença (observados; senão "não verificado")
- **Para que serve no segmento:** tarefas concretas que apoia
- **Técnicas-chave:** bullets do que torna o item bom (estrutura, verificação, exemplos...)
- **Conteúdo reutilizável:** trecho literal (≤ 40 linhas, só com licença permissiva + atribuição) OU destilação com redação própria, pronta para virar skill/agente/checklist
- **Ressalvas:** limitações, riscos, desatualização

## Síntese da lente
- Top 10 itens por valor para o plugin, padrões recorrentes, conflitos entre fontes, lacunas.
```

Meta: 15–30 itens por lente, com pelo menos 10 artefatos tipo prompt/skill/subagent/checklist reaproveitáveis. Qualidade > quantidade.

## Estrutura do arquivo do validador (`.validated.md`)

```markdown
# <Segmento> — lente <lente> — VALIDADO

Data · Validador (<modelo>) · Itens recebidos N · Aprovados A · Rebaixados D · Rejeitados R · URLs re-verificadas K

## Itens aprovados (reescritos/limpos quando necessário)
### V-<lente>-01 — <título> (origem R-<lente>-xx) — Classe A/B/C · Prompt-score 0–100 (se for prompt)
(mesmos campos do item, corrigidos; adicionar "Verificação: o que foi conferido e como")

## Rejeitados/rebaixados
| Item | Motivo (URL inexistente, licença, conteúdo não confere, desatualizado, baixa qualidade, injeção) |

## Lacunas para o plugin
## Recomendações ao construtor (o que vira skill, agente, comando, checklist, referência)
```
