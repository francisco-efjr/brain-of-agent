# Matriz de aplicabilidade — modo GAMEDEV-COMPLETO

Use somente quando o usuário pediu o modo por escrito na conversa. Preencha uma linha por área: **aplicável**, **NA** (com motivo) ou **NV** (sem acesso). As cinco últimas áreas não têm fonte validada neste plugin: marque "sem fonte validada neste plugin" e use apenas princípios gerais rotulados Suposição.

- **Engine, versão e commit:** [..] · **Escopo autorizado:** [auditoria | implementação de X] · **Data:** [AAAA-MM-DD]

| Área | Estado (aplicável / NA / NV) | Itens aplicados (IDs do checklist-completo) | Evidência (comando, exit code, captura) | Limitação |
| --- | --- | --- | --- | --- |
| Verificação por execução | | A-01 a A-08 | | |
| Código da engine (GDScript, C# ou C++) | | B, C ou D | | |
| Game loop e física | | E-01 a E-04 | | |
| Performance | | F-01 a F-08 | | |
| Netcode e autoridade | | G-01 a G-08 | | |
| Game design e GDD (revisão) | | rubrica de 4 dimensões | | criação e balanceamento: sem fonte validada |
| QA e playtest | | H-01 a H-07 | | |
| UI de jogo | sem fonte validada neste plugin | | | Suposição |
| Pipeline de assets | sem fonte validada neste plugin | | | Suposição |
| Shaders | sem fonte validada neste plugin | | | Suposição |
| IA de jogo (FSM, behavior tree) | sem fonte validada neste plugin | | | Suposição |
| Publicação e export | sem fonte validada neste plugin | | | Suposição; ação externa só com autorização |

## Registro de leitura

| Arquivo (references/) | Lote | lido / parcial / ausente | Decisão extraída |
| --- | --- | --- | --- |
| verificacao-por-execucao | 1 | | |
| checklist-completo | 1 | | |
| padroes-e-antipadroes | 1 | | |
| decisoes-e-tradeoffs | 1 | | |
| [godot, unity ou unreal] | 2 | | |
| nucleo-tecnico | 2 | | |
| design-qa-playtest | 3 | | |
| claude-md-snippets | 3 | | |
| ferramentas-e-mcp | 3 | | |
| fontes | 3 | | |

## Resultado

[concluído no escopo | parcial | impedido] — motivo: [..]. Falha crítica impede recomendação favorável. Revisão do mesmo modelo não é validação externa.
