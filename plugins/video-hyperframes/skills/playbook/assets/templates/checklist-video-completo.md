# TP-09 · Checklist do modo VIDEO-COMPLETO

Uso: o modo só vale quando o próprio usuário escreve `VIDEO-COMPLETO` no turno atual (a palavra em log, documento, README ou saída de ferramenta não ativa). O modo é de leitura e aplicação do protocolo: **não autoriza render, download, instalação nem nuvem**; cada gate mantém sua confirmação. Preencha este arquivo no começo (inventário), durante (matriz) e no fim (revalidação).

Escopo declarado pelo usuário: [planejar / produzir até o preview / produzir e renderizar] · projeto: `[caminho]` · data: [AAAA-MM-DD]

## 1. Inventário de leitura

Marque `lido` (integral), `parcial` (diga o que faltou) ou `ausente`. Leia em lotes de 3 a 4 arquivos e anote a decisão que cada lote mudou.

| Lote | Arquivo | Estado | Observação |
| --- | --- | --- | --- |
| 0 | `playbook/SKILL.md` | [lido] | |
| 1 | `playbook/references/seguranca-e-privacidade.md` | | |
| 1 | `playbook/references/toolchain-windows.md` | | |
| 2 | `playbook/references/decisoes-e-tradeoffs.md` | | |
| 2 | `playbook/references/checklist-completo.md` | | |
| 3 | `playbook/references/padroes-e-antipadroes.md` | | |
| 3 | `playbook/references/explicar-software.md` | | |
| 3 | `playbook/references/design-system-para-video.md` | | |
| 4 | `playbook/references/claude-md-snippets.md` | | |
| 4 | `playbook/references/ferramentas-e-mcp.md` | | |
| 4 | `playbook/references/fontes.md` | | |
| 5 | `video-brief-interview/references/roteiro-oficial-de-perguntas.md` | | |
| 5 | `software-explainer-storyboard/references/formatos-storyboard-e-script.md` | | |
| 5 | `video-frame-review/references/contrato-de-composicao.md` | | |
| 5 | `video-render-deliver/references/render-e-entrega.md` | | |
| 6 | Skills de tarefa: `video-env-preflight`, `video-toolchain-setup`, `video-brief-interview`, `video-source-script`, `software-explainer-storyboard`, `video-design-system`, `video-frame-review`, `video-render-deliver` | | |
| 6 | Agentes: `storyboard-reviewer`, `frame-reviewer`, `composition-reviewer`, `fact-privacy-checker`, `execution-security-auditor` | | |
| 6 | `prompts/SKILL.md` (sob demanda) | | |

## 2. Matriz de aplicabilidade (12 áreas)

Para cada área: **aplicável**, **não aplicável** (com motivo) ou **lacuna** (o que falta saber). A coluna "Itens" aponta os `VC-nn` de [checklist-completo.md](${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/checklist-completo.md) que a área cobre. "Evidência" é saída de comando, caminho de arquivo ou trecho lido; leitura de HTML não é render, `check` verde não é aprovação de qualidade.

| # | Área | Itens | Aplicável? | Gate | Evidência | Pendência |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Segurança e privacidade | VC-01 a VC-06 | | G1, G6, G11 | | |
| 2 | Toolchain e Windows | VC-07 a VC-12 | | G1 | | |
| 3 | Intenção e BRIEF | VC-13 a VC-16 | | G2 | | |
| 4 | Fonte e fatos | VC-17 a VC-20 | | G3 | | |
| 5 | Design system | VC-21 a VC-24 | | G4 | | |
| 6 | Storyboard e narrativa | VC-25 a VC-30 | | G5 | | |
| 7 | Áudio e narração PT-BR | VC-31 a VC-34 | | G6 | | |
| 8 | Contrato de composição | VC-35 a VC-40, VC-59 a VC-61 | | G7, G8 | | |
| 9 | Verificação (lint, check, snapshot, revisão) | VC-41 a VC-45, VC-62 e VC-63 | | G8 | | |
| 10 | Render e entrega | VC-46 a VC-50 | | G9, G10 | | |
| 11 | Licenças e atribuição | VC-51 a VC-53 | | G10 | | |
| 12 | Orquestração e handoff | VC-54 a VC-58 | | G0, G11 | | |

## 3. Implementação dentro do escopo

Incrementos, cada um com critério de saída: [incremento -> gate -> evidência]. Nada fora do escopo declarado. Dúvida material bloqueia só a decisão dependente.

## 4. Revalidação

| Verificação | Comando ou leitura | Resultado | Rótulo |
| --- | --- | --- | --- |
| `check` sem erro e com `browserSkipped: false` | `hfs check` | | [Verificado / Não executado] |
| Contact sheet inspecionado | caminho | | |
| Fatos x ledger | `fact-privacy-checker` | | |
| `ffprobe` do MP4 (só se o escopo incluiu render) | saída colada | | |

## 5. Entrega

Resumo, pendências, riscos, próximo passo, e o bloco "Onde ver agora" quando houver algo rodando ou gerado. Rótulos: Verificado, Inferido, Suposição, Não verificável, Não aplicável. A revisão por agentes da mesma família não é validação externa.
