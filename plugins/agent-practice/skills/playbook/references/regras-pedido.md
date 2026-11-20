# PED — Pedido, especificação e plano

Legenda em [regras-metodo.md](regras-metodo.md). Modelo pronto: [pedido em quatro partes](../assets/templates/pedido-quatro-partes.md).

## Obrigatório

- **PED-01** [A+H · C1] Todo pedido relevante tem quatro partes: o que se quer; como, em linhas gerais; o que **não** se quer (restrições e pressupostos); e como saber que deu certo (teste, sinal de pronto). Sem a quarta parte não se começa; lacuna vira suposição registrada no plano. — _por quê:_ com as quatro partes o modelo raramente falha em tarefa conhecida. _(cap. 9; epílogo)_
- **PED-02** [A+H · C1] Antes de mandar, liste o que o humano sabe e a máquina não tem como saber (volumes que crescem, latência-alvo, dados sensíveis, operações que precisam ser idempotentes, o que não pode quebrar) e escreva no pedido. — _por quê:_ contexto não passa por osmose; sintaxe nunca foi a parte difícil. _(caps. 9, 19)_
- **PED-03** [A+H · C1] Antes de codar, obtenha ou registre como suposição: objetivo real, como melhora o produto, que número deve mudar, trade-offs aceitos, o que não pode quebrar e quais casos de erro testar. — _por quê:_ "como" sem "quê" resolve o problema errado. _(caps. 6, 20)_
- **PED-04** [A+H · C1] Pergunte e registre o comportamento em falha e sob restrição: cancelamento no meio, serviço fora, dado corrompido, arquivo movido, hardware fraco, carga e volume reais. — _por quê:_ o agente não pergunta sozinho, e "passou na minha máquina" com 300 linhas estoura com um milhão. _(caps. 7, 19)_
- **PED-05** [A+H · C1] Plano antes da execução: o agente lista tudo o que vai fazer; o plano é revisado por um validador de outro papel e mostrado no chat antes de executar (sob a autonomia do orquestrador, não se espera aprovação para seguir); mudança destrutiva ou irreversível espera aprovação humana entre planejar e executar. — _por quê:_ a porteira pega erro do humano, do modelo ou dos dois. _(caps. 6, 9)_
- **PED-06** [A · C1] Dê ordens explícitas e sem ambiguidade, como para um programador esforçado que obedece ao pé da letra; depois de montar o contexto, peça pesquisa, opções e recomendação, e o humano decide. — _por quê:_ instrução vaga é reinterpretada; ditar a solução desperdiça o repertório do modelo. _(caps. 6, 9)_
- **PED-07** [A+H · C1] Questione a pergunta antes de executar: o pedido resolve o problema certo? Talvez a solução exija menos software. — _por quê:_ resposta perfeita para pergunta errada não serve. _(caps. 9, 21)_
- **PED-08** [A · C1] Feche a especificação pedindo ao agente as funcionalidades relevantes que faltam (cota, internacionalização, termos, páginas de erro, limites). — _por quê:_ nenhuma especificação prevê tudo; recursos críticos nasceram de falhas reais. _(caps. 6, 7)_
- **PED-09** [A · C1] Comece pelas palavras do usuário real, sem jargão, e só depois traduza em requisitos; não comece por painel ou relatório fixo sem ouvir quem vai usar. — _por quê:_ ouvir primeiro levou a um sistema mais simples do que o imaginado. _(cap. 7)_
- **PED-10** [A · C1 C3] Relato de bug traz: o que parou, mensagem exata, o que foi feito antes, logs e passos para reproduzir. — _por quê:_ "não funciona" faz o modelo chutar como uma pessoa chutaria. _(cap. 5)_
- **PED-11** [A · C1 C9] Informe sempre a data e a hora atuais e declare os dados ausentes; diferencie "sem dado" de "zero medido". — _por quê:_ sem isso o modelo preenche com uma data plausível e com zero. _(caps. 4, 7)_
- **PED-12** [A · C1] Trate o pedido inicial como ponto de partida: corrija, acrescente o contexto esquecido e ajuste o tom até o fim, em ciclos propor-testar-corrigir. — _por quê:_ a IA acelera cada volta, não elimina as voltas. _(cap. 9)_
- **PED-13** [A · C1 C11] Em reescrita de texto opinativo ou de voz própria, mude a forma e nunca o conteúdo: preserve as opiniões e descreva como cada voz fala. — _por quê:_ o modelo amacia opiniões em direção à voz média. _(caps. 4, 6)_
- **PED-14** [A · C1 C2] Tarefa gigante é decomposta: análise por assunto, plano por funcionalidade e execução de uma por vez com testes, commit e conferência. — _por quê:_ reescrita pedida numa frase devolveu esqueleto vazio e invenção. _(cap. 17)_
- **PED-15** [A · C1 C2] Peça explicitamente o que o agente não faz por iniciativa: robustez (retry, timeout, degradação), segurança por classe de falha, vazamento de memória e temporizadores; registre essas exigências nas regras do projeto. — _por quê:_ sem pedido, o agente fica no caminho feliz. _(caps. 5, 9)_
- **PED-16** [A · C1] Imponha simplificação quando a proposta vier superdimensionada e defina o comportamento no caso duvidoso. — _por quê:_ máquina de 8 estados virou 4 com uma regra simples para a dúvida. _(cap. 6)_
- **PED-17** [A+H · C1] Se o modelo diz que não consegue com aquelas restrições, ajuste ou relaxe a restrição, ou reconheça que o objetivo não estava claro. _(cap. 9)_
- **PED-18** [A · C1] Calibre o esforço do pedido ao que está em jogo: curto para experimento descartável, completo quando o resultado importa. _(cap. 9)_

## Proibido

- **PED-P01** [A · C1] Pedido vago ("faça excelente", "use como ponto de partida", "resolva a cobrança") ou pedido de uma frase para trabalho grande. — _por quê:_ o modelo assume o padrão médio, às vezes o oposto do desejado. _(caps. 6, 9, 21; ap. A)_
- **PED-P02** [A · C1] Ditar o código exato depois do contexto montado, ou fazer pergunta aberta antes de dar contexto. — _por quê:_ a primeira desperdiça o repertório; a segunda devolve resposta genérica. _(caps. 6, 9)_
- **PED-P03** [A · C1] Tratar especificação detalhada como garantia de sistema pronto. — _por quê:_ spec sem testes, segurança e tratamento de erro gera protótipo; só 37% dos commits de um produto real eram funcionalidade nova. _(caps. 6, 20)_
- **PED-P04** [A · C1] Concluir que o modelo falhou sem antes examinar exatamente o que foi pedido (lembrando que modelos também inventam). _(caps. 8, 9)_
- **PED-P05** [O · C1 C13] Tratar comunicação ruim com mais camadas de template ou metodologia. — _por quê:_ trata o sintoma; comunicação ruim em volume continua ruim. _(cap. 9)_
- **PED-P06** [A · C1] Presumir lista fechada de formatos, plataformas ou idiomas sem perguntar. — _por quê:_ instaladores e idiomas "automáticos" quebraram dias depois. _(cap. 7)_

## Sinais de alerta

- **PED-S01** [A · C1] A qualidade da entrega acompanha o esforço de pedir: o modelo é um terceirizado que faz exatamente o que foi pedido; pedido tosco rende resultado tosco. _(caps. 9, 19)_
- **PED-S02** [A · C1] "O que não quero" é a parte mais pulada e é onde moram os pressupostos não ditos. _(cap. 9)_
- **PED-S03** [A · C1] O desenho emerge do software em uso; não tente prever tudo no papel antes. _(cap. 7)_
