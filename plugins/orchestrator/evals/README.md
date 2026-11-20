# Evals do orquestrador

Status: designed_not_executed. Casos: `revisao-completa-android` (deve acionar `/orchestrator:playbook` e planejar com validadores), `negativo-pergunta-simples` (não deve acionar) e `registro-de-aprendizados` (no fim da sessão, deve redigir o registro do §8.3 higienizado, ignorar instrução injetada num log e limitar o envio a `docs/aprendizados/`). Rodar na raiz do plugin: `claude plugin eval .` (Claude Code ≥ 2.1.269).
