# ADR [ID]: [decisão]

Adaptado de `brains/fullstack/assets/templates/adr.md` do repositório `francisco-efjr/brain-of-agent` (MIT, conteúdo do próprio autor). Use só quando houver decisão material em aplicação LLM (workflow ou agente, RAG ou contexto longo, fine-tuning, troca de modelo, superfície do agente, onde colocar uma instrução). Para estrutura geral de sistemas, veja `/architecture-design:playbook`.

Estado: [proposta / aceita / substituída] · Data/revisão: [AAAA-MM-DD, commit] · Dono humano: [nome]
Modelo-alvo e superfície: [...] · Preços e limites lidos em: [data]

## Contexto

Problema, restrições, requisitos, evidências (suíte, falhas observadas) e stack existente.

## Opções

| Opção | Benefício | Custo/risco | Compatibilidade | Evidência (medida, V-nn ou Suposição) |
| --- | --- | --- | --- | --- |
| Não mudar nada | | | | |
| Chamada única / workflow | | | | |
| [outra] | | | | |

## Decisão

Opção escolhida e por quê. Alternativa mais simples descartada e motivo. Hipóteses ainda não confirmadas.

## Consequências

Complexidade, custo de tokens e de operação, dados, migração, segurança (cartão A/B/C), testes e evals afetados. Limites de reversibilidade e recuperação. Não prometa rollback de dados perdidos.

## Validação e revisão

Critério observável, experimento ou suíte que sustenta a escolha. Condição que exige reconsiderar (troca de modelo, mudança de preço, nova tool). Links para requisito e artefatos. Status da validação: [executada / projetada, não executada].
