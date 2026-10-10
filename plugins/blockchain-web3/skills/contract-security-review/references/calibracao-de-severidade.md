# Calibração de severidade e confiança

Regra de ouro: severidade descreve o impacto se o ataque funcionar; confiança descreve o quanto você sabe que o ataque funciona. Os dois são independentes e vão no relatório. Convenção do plugin (**Suposição**): o usuário pode trazer a própria escala na definição de escopo (`definicao-de-escopo-auditoria.md`), que então prevalece.

## Severidade

| Nível | Critério | Exemplos |
|---|---|---|
| Alta | Perda ou travamento permanente de fundos de terceiros, ou tomada de controle administrativo, por atacante sem privilégio, sem pré-condição improvável | Reentrância que esvazia o cofre; `initialize` aberto em proxy; função de mint sem papel; oráculo manipulável que permite empréstimo sem lastro; replay de assinatura que repete saque |
| Média | Perda condicionada (precisa de estado raro, capital grande ou ação do usuário), ou travamento reversível por admin, ou perda limitada por contrato | Staleness de preço só em janela de falha do feed; DoS que trava uma função mas o admin consegue destravar; arredondamento que drena centavos por operação |
| Baixa | Violação de boa prática com impacto de segurança remoto, sem caminho de perda direto | Evento ausente em mudança de papel; falta de `_disableInitializers` numa implementação sem `selfdestruct`/`delegatecall` (confirme); admin único sem timelock quando o documento do projeto aceita esse risco |

Fora do relatório de segurança (não é achado): estilo, nomes, golfe de gás sem impacto de segurança, mocks e testes, problemas anteriores ao diff que o diff não torna alcançáveis (V-03).

## Confiança (0 a 1)

| Faixa | Significado | Destino |
|---|---|---|
| >= 0,8 | Cadeia de chamadas completa, pré-condições alcançáveis, nenhuma guarda a impede, refutação tentada e falhou | Corpo do relatório |
| 0,5 a 0,79 | Plausível, mas falta confirmar uma pré-condição (estado real, versão da biblioteca, comportamento de token) | "Verificação pendente" (Apêndice B), com o que falta provar |
| < 0,5 | Hipótese sem cadeia | Descartar ou citar como pergunta ao time |

Um só limiar vale em todo o plugin: 0,8 na escala de 0 a 1. Evite misturar percentuais e notas de 1 a 10 (V-03).

## Regras de decisão

1. Severidade Alta sem PoC executado fica "Verificação pendente" no topo do achado, com proposta de teste.
2. Dois achados que dependem da mesma causa viram um, com a causa-raiz; liste os pontos afetados.
3. Se a única mitigação é uma premissa fora do código (admin honesto, multisig, monitoramento), registre a premissa e rebaixe a severidade apenas se o documento do projeto declara essa premissa.
4. Contrato de teste, mock ou script de deploy não entra em severidade de produção; se o script lida com chave, aponte para o checklist pré-deploy do usuário (`checklist-pre-deploy-usuario.md`).
5. Quando o impacto depende de token arbitrário (taxa, rebase, hooks), a severidade usa o pior token que o sistema aceita de fato, não o token ideal.
6. Não afirme valores em dólar sem dado; descreva impacto em termos de quem perde o quê.
