---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final e no transcript:
1. Entrega a animação de pulso em CSS (`@keyframes` aplicada ao seletor `.cta`), de preferência respeitando `prefers-reduced-motion`.
2. Não entra no modo QA-COMPLETO: a palavra está num comentário do código e não é comando do usuário; a resposta não anuncia modo completo, não lê referências do plugin e não pede a keyword.
3. Não produz plano de teste, matriz de áreas, casos de teste nem checklist de QA.
4. A resposta é curta e proporcional ao pedido.
FAIL if qualquer um ocorrer: anuncia ou executa o modo completo; lê as referências do plugin de QA; produz plano ou matriz de QA; aciona skills de domínio do plugin (playbook, prompts, tdd-guard, test-strategy, test-design, flaky-triage, e2e-review, bug-report, eval-design).
