---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"automation-integrations:'
min: 0
max: 0
arm: both
---
Caso negativo: nenhuma skill do plugin automation-integrations deve ser chamada. O input_match tem o prefixo do plugin para que uma skill de outro plugin instalado não reprove o caso por engano; arm both força a pontuação nos dois braços.
