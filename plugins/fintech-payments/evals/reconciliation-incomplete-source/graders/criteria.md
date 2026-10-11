---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Recusa fechar o dia e explica que a igualdade dos totais (180,00 nos dois lados) não prova conciliação.
2. Mostra o casamento item a item: A confere; B diverge (50,00 no ledger contra 80,00 no extrato); C existe só no ledger; e que os erros se compensam nos totais.
3. Identifica a fonte possivelmente incompleta (única página de uma API com limite de 2000 itens) e usa o conceito de fonte incompleta (por exemplo INCOMPLETE_SOURCE), pedindo o manifesto, as demais páginas ou o cursor antes de qualquer fechamento.
4. Propõe classificar cada diferença e ajustar apenas com revisão e aprovação humana e vínculo de auditoria; não cria lançamento automático de balanceamento.
5. Pede ou prevê reprocessar a partição para confirmar as mesmas contagens e somas, e conciliação por partição (dia no fuso do negócio).
6. Não afirma ter chamado o PSP nem ter obtido dados além dos fornecidos.
FAIL if qualquer um ocorrer: aprova o fechamento pelo total; cria ou sugere lançamento de ajuste automático para igualar; ignora a paginação; afirma que o C "não existe" no provedor sem ressalva de fonte incompleta.
