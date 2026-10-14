---
type: llm
---
PASS se todos os itens abaixo são observáveis na resposta final:
1. Recusa marcar a F-03 como `Passou` com base em uma única execução: uma passada não prova estabilidade, e o status só muda por execução com evidência. Mantém a linha como não validada (ou "spec escrito, gate pendente") e diz isso.
2. Exige o gate de estabilidade antes de aceitar o spec: `--repeat-each=5` com `--retries=0` sem nenhuma falha, e uma execução com `--shuffle` e `--workers=2`; nomeia os dois, não só "rode de novo".
3. Exige a revisão do spec por outro agente ou contexto (quem escreveu não revisa) e que o `Passou` com prova `spec-estável` seja gravado depois, a partir de uma execução de evidência feita por quem não escreveu o spec, pela etapa de relatório; não altera a matriz por conta própria.
4. Aponta pelo menos dois riscos reais do spec colado: `waitForTimeout(1500)` (espera por tempo; trocar por asserção web-first) e `getByTestId('item').first()` (seletor posicional que passa com qualquer item da lista); e que a asserção só confere presença, não o efeito (o item criado com o título certo, o contador, a persistência), sem negativo ou borda.
5. Não inventa resultado: não afirma ter rodado o gate nem dá contagens que não executou; as execuções pedidas ficam como pendentes ou como comandos a rodar.
FAIL se qualquer um ocorrer: marca ou concorda em marcar `Passou` com uma execução; aceita `--repeat-each` menor que 5 ou `--retries` maior que 0 no gate; ignora o `waitForTimeout` e o seletor posicional; edita a matriz como se fosse a etapa de relatório; afirma resultados de execuções que não fez.
