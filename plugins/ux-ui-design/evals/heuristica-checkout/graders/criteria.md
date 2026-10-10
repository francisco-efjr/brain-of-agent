---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Estrutura os achados por heurísticas de Nielsen nomeadas (por exemplo visibilidade do estado do sistema para a falta de indicador de progresso; controle e liberdade para o carrinho esvaziado e a perda do endereço; prevenção de erros e ajuda para reconhecer, diagnosticar e recuperar erros para "Falha na operação", "Erro" e formulário que volta vazio; consistência e padrões para o botão "Enviar" repetido), com local exato (passo e elemento) e evidência tirada da descrição.
2. Atribui severidade de 0 a 4 a cada achado, com justificativa que cite frequência, impacto e persistência (pelo menos para os de severidade 3 ou 4); o cupom inválido que esvazia o carrinho e a perda de dados na recusa do cartão aparecem entre os mais graves.
3. Separa o que é violação do que é escolha defensável, rotulando-a "trade-off a validar" (por exemplo exigir telefone fixo ou campos obrigatórios por motivo de negócio ou fiscal não informado), em vez de tratar toda violação como problema.
4. Declara que a avaliação feita por um agente é uma opinião (leitura de descrição, rótulo Inferido), não validação com usuários, e propõe o que testar com usuários reais, ligando ao menos os achados de severidade 3 ou 4 a uma tarefa de teste.
5. Fecha com os 3 achados mais graves e uma recomendação proporcional para a reunião, sem decidir pelo time se refaz o fluxo.
6. Cobre o contexto mobile (formulário longo no celular, teclado, CEP sem preenchimento automático) sem inventar capturas ou medições.
FAIL if qualquer um ocorrer: prevê taxa de abandono, conversão, receita ou prazo como fato; atribui nota sem justificar; trata toda violação como problema sem considerar contexto; declara o fluxo "validado" ou afirma o que "os usuários vão fazer"; confunde "3 a 5 avaliadores" com "5 participantes"; inventa dados do sistema além da descrição.
