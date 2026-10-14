# Orquestrador Brain of Agent (`orchestrator`)

Coordena os plugins por segmento do marketplace `brain-of-agent`. A partir de uma demanda, ele classifica o trabalho, escolhe agentes e skills, despacha subagentes com validação independente e entrega relatórios por papel, mais um consolidado.

## Instalação

```bash
claude plugin marketplace add francisco-efjr/brain-of-agent
claude plugin install orchestrator@brain-of-agent
```

Instale também os plugins dos segmentos que você usa. A lista está em `docs/dev-segments/CATALOGO.md` do repositório.

## Componentes

| Componente | Uso |
| --- | --- |
| `/orchestrator:playbook [demanda]` | Orquestra a demanda (protocolo em `skills/playbook/references/protocolo.md`) |
| `skills/playbook/references/conhecimento.md` | Registro de conhecimento por tag (gerado): gatilhos → plugin líder, fundamentos, apoio, validador e status. É por ele que a demanda vira especialista |
| `skills/playbook/references/catalogo.md` | Catálogo de plugins, skills e agentes (gerado), para o que não casar com tag |
| `/orchestrator:prompts` | Mensagens prontas para acionar o orquestrador (O-01 a O-08) |
| Agente `orchestrator:demand-router` | Classifica a demanda, casa com as tags e devolve o plano, sem executar |

## Sem instalar

Mande o link do repositório num chat com a mensagem O-01 (`skills/prompts/references/prompt-library.md`). A IA segue o `ORCHESTRATOR.md` da raiz.

## Limitações

- Subagentes não abrem outros subagentes. Quem orquestra é a sessão principal, via skill.
- Os resultados dependem dos plugins instalados. Plugins "em construção" aparecem como lacuna.
- Os evals estão em `designed_not_executed`. `claude plugin eval` exige Claude Code 2.1.269 ou superior.
