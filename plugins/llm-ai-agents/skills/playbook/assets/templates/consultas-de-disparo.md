# Consultas de disparo (20) para otimizar a `description`

Fonte: V-23 (destilado do skill-creator da Anthropic; só destilar, sem cópia) e V-12. Objetivo: medir se a `description` de uma skill faz o modelo escolhê-la nos pedidos certos e deixá-la de lado nos quase-acertos. Quem roda é o usuário (consome cota; `claude -p` só existe no Claude Code). Status até rodar: **projetado, não executado**.

## Regras

- 20 consultas: ~10 que devem disparar e ~10 quase-acertos negativos (tema vizinho que NÃO deve disparar esta skill).
- Divida 60/40 (treino/teste); escolha a `description` pelo conjunto de **teste**; rode cada consulta mais de uma vez.
- Descarte consultas triviais de um passo, que raramente disparam skill.
- Escreva como o usuário escreveria, em PT-BR e EN, sem citar o nome da skill.

## Tabela

| # | Consulta | Deve disparar? | Conjunto (treino/teste) | Execuções | Disparou (n/N) | Observação |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [pedido realista positivo] | sim | treino | | | |
| 2 | [pedido realista positivo em EN] | sim | teste | | | |
| 11 | [quase-acerto: tema vizinho] | não (outra skill: [...]) | treino | | | |
| 12 | [quase-acerto em EN] | não | teste | | | |

(Complete até 20.)

## Exemplo para `llm-prompt-review` (ilustrativo)

Positivas: "Revisa este system prompt do meu assistente de suporte"; "meu prompt ignora a regra de não citar concorrentes"; "poda este prompt, vou migrar para o Sonnet 5.5"; "review my prompt, it keeps ignoring the JSON format".
Quase-acertos negativos: "enxuga meu CLAUDE.md" (vai para `instruction-authoring`); "revisa o código que chama messages.create" (vai para `llm-api-client-review`); "escreva uma função que ordena uma lista" (nenhuma skill do plugin).

## Leitura do resultado

Delta perto de zero com `tool_used: Skill` falhando ⇒ o modelo não escolhe a skill: reescreva a `description` com gatilhos concretos e cláusula "não use para…" (sem CAPS). Antes de culpar o plugin por queda brusca, descarte limite de uso estourado.
