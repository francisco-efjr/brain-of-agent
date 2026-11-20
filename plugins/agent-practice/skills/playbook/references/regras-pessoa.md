# PES — Pesquisa com chatbot, aprendizado, privacidade e golpes

Legenda em [regras-metodo.md](regras-metodo.md). As regras de pesquisa (PES-01 a PES-11) valem para o agente sempre que ele pesquisa, checa fatos ou redige relatório (C11). As de aprendizado, privacidade e golpes são orientação à pessoa usuária: o orquestrador as aplica quando o pedido é sobre esses temas (C14) e as repassa quando o assunto aparece.

## Obrigatório — pesquisar e checar com chatbot

- **PES-01** [A · C11 C14] Pergunte sem embutir a opinião de quem pede: perguntas fechadas e estreitas por etapa (que falácias há, que contexto falta, o título bate com o corpo), argumentos a favor e contra, e a pergunta invertida numa conversa separada. — _por quê:_ o modelo prevê a resposta que você quer ouvir; se a resposta vira com a pergunta, o problema é a pergunta. _(cap. 4; ap. I)_
- **PES-02** [A · C11 C14] Assunto sério começa em conversa nova. — _por quê:_ o histórico empurra a resposta para o perfil presumido. _(cap. 4)_
- **PES-03** [A · C11 C14] Exija a referência e abra o documento; suba à primária (bula, estudo, contrato, dado oficial); veículos que repetem a mesma origem valem uma voz; não peça à IA que confirme a sua hipótese. — _por quê:_ link morto ou divergente contamina a resposta inteira. _(prefácio; caps. 4, 15)_
- **PES-04** [A · C11] Peça segunda opinião a modelo de outra empresa com a mesma pergunta neutra; em checagem séria use três juízes de empresas diferentes, com a fonte primária dando a palavra final. Independência é real só se as fontes forem diferentes. — _por quê:_ quando um alucina, os outros costumam discordar; três modelos lendo a mesma fonte ruim equivalem a repetir um único exame. _(cap. 4; ap. J)_
- **PES-05** [A · C11] Restrinja o modelo: cite só o material fornecido, marque o que não puder verificar, liste cada afirmação factual produzida e não cite lei ou dado que não foi fornecido. _(caps. 4, 9)_
- **PES-06** [A · C11] Liste as perguntas que o texto analisado deveria responder e não responde. — _por quê:_ a ausência é sinal forte de enquadramento. _(cap. 4)_
- **PES-07** [A · C11 C14] Cálculo com datas, juros ou prazos é pedido passo a passo e refeito em calculadora ou planilha. _(cap. 4)_
- **PES-08** [A · C11 C14] Contrato ou documento decisivo se lê inteiro. — _por quê:_ o resumo pode omitir justamente a cláusula decisiva. _(cap. 4)_
- **PES-09** [A+H · C11 C14] Em saúde, direito e finanças a decisão é de quem responde por ela (médico, advogado, contador); o chatbot traduz jargão e prepara perguntas, nunca define dose, diagnóstico ou troca de medicação. — _por quê:_ "acho que tenho X" faz o modelo achar sinais de X. _(cap. 4)_
- **PES-10** [P · C14] Use o campo de instruções permanentes do chatbot (profissão, tom, o que nunca inventar, como marcar incerteza) e guarde os resumos das conclusões num arquivo seu, colado no início de conversas novas. _(cap. 9; ap. G)_
- **PES-11** [A · C11] Ao indicar leituras, ordene por nível (leigo, pouca matemática, código), confira autor, editora, idioma e acesso gratuito legal, e comece pelo caminho mais curto. _(ap. C)_

## Obrigatório — aprender com IA do lado

- **PES-12** [P · C14] Use a IA para aprender mais rápido, não para pular a base: peça o porquê de cada mudança, tente sozinho antes (meia hora a uma tarde), peça pista e não solução, compare com a sua tentativa e leia a fonte original; iniciante escreve o teste antes do código e publica um problema resolvido sem tutorial. — _por quê:_ quem não conhece não sabe pedir o que desconhece. _(caps. 5, 8, 19; epílogo; ap. D)_
- **PES-13** [P · C14] Estude fundamentos duráveis (algoritmos e estruturas, como o computador funciona, matemática e estatística, o mecanismo dos modelos e o domínio do próprio ofício), do simples ao complexo, contando em anos. _(caps. 14, 19; epílogo; ap. D)_
- **PES-14** [P · C14] Prática deliberada: escreva o resultado esperado antes de consultar o agente, mude uma condição, preveja, compare e leve a divergência a quem conhece a regra; rode, quebre de propósito e mude parâmetros antes de pedir explicação; de vez em quando faça à mão o que costuma delegar. _(cap. 21; epílogo; ap. D)_
- **PES-15** [P · C14] Use o agente para gerar exemplos, alternativas e exercícios, conferindo as respostas, e use o tempo liberado para estudar justamente o trecho que você evitava. _(cap. 21)_
- **PES-16** [P · C13 C14] Defina-se pelo problema que resolve, não pela ferramenta da moda; suba de camada (menos digitação e formatação, mais julgamento, exceção e responsabilidade) e aprenda a próxima interface. _(cap. 19; ap. E)_

## Obrigatório — privacidade e golpes

- **PES-17** [P · C14] Permissões de aplicativos: negue o que não é necessário (localização, contatos, microfone, câmera) ou libere só durante o uso; revise todo mês; resete o identificador de publicidade; prefira a versão web com bloqueador de rastreadores; não ative "encontrar amigos" sem pensar. _(cap. 18)_
- **PES-18** [P · C14] Abordagem inesperada que pede encontro, dinheiro ou dados deve ser tratada como golpe até se provar legítima; revogue aplicativos conectados desconhecidos na conta; agendamento legítimo não pede login social. _(cap. 18)_
- **PES-19** [P · C14] Pedido de dinheiro ou urgência se confirma por outro canal (número oficial, palavra-código combinada com a família); foto, vídeo e voz sozinhos não provam nada. — _por quê:_ vídeo e voz gerados já não se distinguem a olho. _(cap. 18; epílogo)_
- **PES-20** [P · C14] Desconfie de serviço gratuito cujo operador você não conhece, sobretudo se ele lê e-mail ou arquivos. _(cap. 18)_
- **PES-21** [P · C14] Para aplicativos que apagam, sincronizam ou organizam em massa: tenha cópia em outro lugar, saiba por quanto tempo há versões antigas e teste abrir arquivos do backup. _(cap. 16)_

## Proibido

- **PES-P01** [A · C11 C14] Tomar concordância fácil do modelo como validação, ou detector de "texto de IA" como prova de autoria. _(cap. 4)_
- **PES-P02** [P · C14] Usar o agente como muleta: aprovar o que não entende, confundir assistir à solução com saber resolver, deixar a máquina tirar toda a dificuldade. — _por quê:_ vira revisor incapaz, mais perigoso que o júnior de antes. _(caps. 19, 21; epílogo; ap. D)_
- **PES-P03** [P · C14] Supor imunidade ("a IA só substitui quem digita"), achar que formação encerra o aprendizado ou que expertise num domínio vale em outro. _(cap. 21)_
- **PES-P04** [P · C14] Usar erros de português como filtro de golpe. — _por quê:_ o modelo escreve e-mail perfeito em segundos. _(cap. 18)_
- **PES-P05** [A · C11 C14] Concluir "o app espiona" ou "está tudo bem" só pela lista de permissões, ou analisar pacote baixado de espelho não oficial. — _por quê:_ capacidade não é prova de uso; o espelho pode estar adulterado. _(cap. 18)_
- **PES-P06** [P · C14] Decidir sob medo ou empolgação: ignore anúncio de AGI ou extinção, disputa de ranking decidida por frações de ponto e vídeo de app feito em dez minutos. _(cap. 15; epílogo)_

## Sinais de alerta

- **PES-S01** [A · C11] Sinais de invenção: estudo de formato perfeito "provando o contrário", dado ausente que virou zero, data de outro ano, números redondos e plausíveis. _(cap. 4)_
- **PES-S02** [A · C11] Bajulação aparece em todos os modelos grandes; sem opinião para agradar, o modelo puxa para o meio morno. _(cap. 4; ap. B)_
- **PES-S03** [P · C14] Resposta pronta é só a introdução; quem não tem o mapa chega mais rápido ao lugar errado; se você só repete a explicação da ferramenta, achou o que estudar; receita não ensina a adaptar quando o ingrediente muda. _(cap. 21; ap. D)_
- **PES-S04** [P · C14] Quanto melhor a proposta, mais devagar responda; elogio sob medida, susto e pressa são alerta; se o coração acelera com um anúncio, pergunte quem lucra com isso. _(cap. 18; epílogo)_
- **PES-S05** [P · C14] Rastreamento se faz por combinação de sinais fracos (aparelho, sistema, tela, fuso, sensores) que sobrevive a reinstalar; vários SDKs de atribuição e serviços de fingerprint são alerta; tráfego só para domínios próprios e credenciais em cofre são bom sinal. _(cap. 18)_
- **PES-S06** [P · C14] A barreira caiu para todos: a mesma ferramenta que lê o aplicativo do banco escreve o golpe; análise assistida por IA não vê servidor nem tráfego e não abre código nativo. _(cap. 18)_
