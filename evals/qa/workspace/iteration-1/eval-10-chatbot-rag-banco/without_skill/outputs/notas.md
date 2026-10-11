# Notas e incertezas

- **Contexto desconhecido**: assumi um bot só de texto que responde com base no FAQ. Não sei a stack, se o bot executa ações (bloquear cartão etc.) nem se há fluxo autenticado. Perguntei no fim da resposta, mas entreguei o plano completo sem esperar a resposta.
- **Limiares são heurísticas minhas** (95% fidelidade, 90% hit@k, 100 a 200 casos, 3 a 5 repetições, 5% de canário). Não são padrão de mercado nem exigência regulatória. Disse isso na resposta.
- **Regulação citada de memória, sem verificar** (sem rede): Decreto 11.034/2022 (SAC, acesso a atendente humano) e LGPD. Escrevi "pelo que me lembro" e mandei validar com o jurídico. Não citei artigos.
- **Harness**:
  - Checagem por substring é frágil: uma resposta correta, escrita com outras palavras, pode reprovar em "fato obrigatório". Mitiguei com alternativas por fato e com o juiz LLM, mas o juiz não foi executado.
  - `juiz_llm.py` é um stub (sem rede): o prompt e o parser JSON não foram testados contra um modelo real.
  - A regex de cartão (13 a 19 dígitos) pode dar falso positivo com protocolos ou números longos; a de CPF casa qualquer número de 11 dígitos.
  - `hit@k` exige que o pipeline exponha os IDs dos trechos recuperados; se não expõe, precisa instrumentar.
  - Injeção de prompt indireta (instrução dentro de documento indexado) está descrita na resposta, mas não há caso nem checagem no harness.
  - O canário `canario-7f3a` é um valor de exemplo; precisa estar de fato no prompt de sistema real.
- **Bot de exemplo**: FAQ, valores (R$ 1.000, 2%, R$ 6,50...) e banco são fictícios. As falhas que aparecem (juros de mora usado como resposta de juros de empréstimo, eco de CPF, multi-turno sem histórico, paráfrase sem match) foram provocadas pelo desenho ingênuo do mock, não dizem nada sobre o bot real. Ajustei dois casos (multi-turno e eco-cpf) depois da primeira rodada para que cada um isolasse uma falha só. Resultado final com o mock: 9/16 aprovados, 3 portões reprovados, saída 1. Rodado com Python 3.14, só stdlib; também rodei com `--repeticoes 3`.
- **Não cobri em profundidade**: teste de carga, acessibilidade do widget de chat, canal de voz/áudio, métricas de custo de tokens, idiomas além de português. Só citei latência e fallback de passagem.
- **Tamanho da resposta**: optei por um plano completo em sete blocos mais o harness; pode estar longa para um chat. Se fosse cortar, cortaria os itens 6 e 7 para um parágrafo cada.
