# Fontes do engineering-lifecycle

Data de consulta: 2026-10-13. Classe A = oficial ou mantenedor de referência (nota 8 a 10 na rubrica de fonte da fábrica); B = prática reconhecida; C = só como ideia. "Verificado" quer dizer lido por ferramenta no clone do upstream pela pesquisa da fábrica (`docs/research/engineering-lifecycle/VALIDATED.md`); "informado" é fato levantado pelo orquestrador via API do GitHub em 2026-10-13 e **não reaberto nesta construção**. Estrelas, forks e datas mudam: não são prova de qualidade.

## 1. Fonte principal

| Campo | Valor |
| --- | --- |
| Projeto | `addyosmani/agent-skills` |
| URL | https://github.com/addyosmani/agent-skills |
| Autor | Addy Osmani (mantenedor); colaboradores creditados em `third_party/addyosmani-agent-skills/README.md` |
| Commit vendorizado | `aeac41d4d005999432bb7312f7ff06383a91d59d` (Verificado: `git log -1` no clone; 2026-10-13T16:21:06-04:00, "chore(release): bump plugin manifests to 0.6.13") |
| Versão do plugin upstream | 0.6.13 |
| Licença | MIT, "Copyright (c) 2025 Addy Osmani" (Verificado: arquivo `LICENSE`, preservado em `third_party/addyosmani-agent-skills/LICENSE`) |
| Estrelas e forks | 106.171 estrelas, 11.068 forks (informado, 2026-10-13) |
| Atividade | Push e release no próprio dia 2026-10-13; repositório criado em 2026-02-15; 116 issues abertas (informado) |
| Conteúdo | 25 skills, 7 checklists em `references/`, 4 personas, 9 comandos (`.claude/commands/`), 5 evals de plugin, docs e hooks (Verificado por listagem) |
| Importado em | 2026-10-13, 68 arquivos, sha256 em [inventory.json](../../../third_party/addyosmani-agent-skills/inventory.json) |

**Classe A, 10 de 10** pela rubrica `source-quality-rubric.md`:

| Critério | Peso | Nota | Base |
| --- | --- | --- | --- |
| Autoridade | 3 | 3 | Autor reconhecido e mantenedor do repositório |
| Evidência de uso | 2 | 2 | Evals no CI do upstream existem; os números de resultado do README **não foram reproduzidos** (Verificado: `evals/README.md` linhas 53 e 55) |
| Atualidade | 2 | 2 | Push e release no dia da consulta |
| Sinal comunitário | 2 | 2 | Mais de 5 mil estrelas (informado) |
| Licença | 1 | 1 | MIT |
| **Total** | **10** | **10** | **Classe A** |

As heurísticas numéricas do autor (100, 300 e 1000 linhas; 75% da janela; pirâmide 80/15/5; três rodadas de dúvida; limiares de rollout) **não rebaixam a classe**: ficam como ponto de partida e Suposição até medir no projeto.

## 2. Arquivos do upstream por grupo

Link permanente: `https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/<caminho>`. Os arquivos vendorizados estão neste plugin, byte a byte, exceto o namespace dos comandos.

| Grupo | Caminho no upstream | Onde fica aqui |
| --- | --- | --- |
| Skills (25) | `skills/<nome>/SKILL.md` (+ `references/`, `examples.md`, `frameworks.md`, `refinement-criteria.md`, `scripts/idea-refine.sh`) | `skills/<nome>/` |
| Checklists (7) | `references/` (accessibility-checklist, definition-of-done, observability-checklist, orchestration-patterns, performance-checklist, security-checklist, testing-patterns) | `references/` na raiz do plugin |
| Personas (4) | `agents/{code-reviewer,security-auditor,test-engineer,web-performance-auditor}.md` | `agents/` |
| Comandos (9) | `.claude/commands/{spec,plan,build,test,review,code-simplify,constraints,webperf,ship}.md` | `commands/` (troca `agent-skills:` por `engineering-lifecycle:`) |
| Evals de plugin (5) | `evals/plugin/<caso>/` | `evals/<caso>/` |
| Licença | `LICENSE` | `third_party/addyosmani-agent-skills/LICENSE` |
| Lidos, não vendorizados | `docs/agents.md`, `docs/skill-anatomy.md`, `docs/advanced-per-agent-configuration.md`, `hooks/`, `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md` | Destilados em PT-BR nas referências desta camada |

`docs/agents.md` e os demais arquivos de `docs/` foram lidos pela pesquisa; o upstream não aceita traduções, então esta versão PT-BR é **derivada**, não contribuição. Não apresente o derivado como versão do upstream.

## 3. Normas e fontes citadas pelo upstream

**Citadas pelo upstream; não consultadas nesta construção.** Os números e afirmações abaixo são do texto do upstream. Confira na fonte antes de tratar como regra.

| Norma ou fonte | Onde o upstream cita | Uso | Estado |
| --- | --- | --- | --- |
| OWASP Top 10 (ordenação de 2021) | `references/security-checklist.md`, `security-and-hardening` | Base mínima de segurança | Citada; não consultada |
| OWASP Top 10 for LLM Applications (2025) | `security-and-hardening`, `security-checklist.md` | Aplicações com LLM | Citada (genai.owasp.org); não consultada |
| Core Web Vitals (web.dev) | `performance-checklist.md`, `performance-optimization` | LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1 | Citada; limiares **não conferidos** em web.dev |
| WCAG 2.1 AA | `frontend-ui-engineering`, `shipping-and-launch`, `accessibility-checklist.md` | Acessibilidade | Citada. **O brain usa WCAG 2.2 AA** (precedência, item 1) |
| Software Engineering at Google (SWE Book) e guia de práticas de engenharia do Google | README do upstream | Hyrum's Law, Beyoncé Rule, pirâmide de testes, tamanho de mudança, Chesterton's Fence, trunk-based, Shift Left | Citados; não consultados |
| "Lost in the middle" (Liu et al., 2023) | `context-engineering` | Conteúdo crítico por último | **Não verificável** aqui |
| DORA e desenvolvimento baseado em tronco | `git-workflow-and-versioning` | Correlação com desempenho de entrega | Afirmação sem link; **Não verificável** |
| Documentação oficial de gerenciadores de pacote (npm, pnpm, yarn) | `security-checklist.md` | Scripts de instalação, aprovação de builds | Citada; matriz é um snapshot com versões; **verifique na documentação oficial**, não copie como fixa |

## 4. Fontes da casa e da fábrica

| Fonte | Local | Uso |
| --- | --- | --- |
| Pesquisa validada | `docs/research/engineering-lifecycle/VALIDATED.md` (V-01 a V-37, conflitos C-1 a C-17) | Base de todo o crosswalk |
| Síntese e contrato | `docs/research/engineering-lifecycle/SYNTHESIS.md` | Decisões de desenho |
| Protocolo do orquestrador | `publish/ORCHESTRATOR.md` | Limites, profundidade 1, tags |
| Registro de tags | `docs/foundation/knowledge/*.json`, `knowledge-registry-spec.md` | Papéis líder, fundamentos e apoio |
| Estilo da casa | `docs/foundation/house-style.md`, `plugin-blueprint.md` | Rótulos, proporcionalidade, modo completo |

## 5. Não verificado nesta construção

- Todas as normas da seção 3 (nenhuma página foi aberta).
- Os números do README de evals do upstream (por exemplo "2 de 4 com o plugin contra 0 de 3 sem"): repo-reportados, nenhum eval foi executado.
- Os 25 `SKILL.md` foram lidos pela pesquisa por amostragem e por lentes, não integralmente pelo validador; esta camada leu por inteiro `using-agent-skills` e `constraint-driven-development`, trechos de `interview-me`, `context-engineering`, `doubt-driven-development`, `source-driven-development`, `shipping-and-launch` e `browser-testing-with-devtools`, e a seção Common Rationalizations das 24 skills que a têm.
- Como o Claude Code resolve um `subagent_type` sem prefixo quando duas personas têm o mesmo nome.
- Regras de plataforma do upstream (subagentes não criam subagentes, campos ignorados no frontmatter, Agent Teams): só pela documentação do próprio upstream.
- Execução de qualquer skill, comando, persona ou eval deste plugin: nada foi executado.

## 6. Onde reconferir

Upstream: repositório e as releases no GitHub; procedimento de atualização em [atualizacao-upstream.md](atualizacao-upstream.md). Normas: páginas oficiais (OWASP, web.dev, W3C, documentação do gerenciador de pacotes da versão do projeto). Plataforma Claude Code: https://code.claude.com/docs/en/plugins-reference e https://code.claude.com/docs/en/sub-agents.
