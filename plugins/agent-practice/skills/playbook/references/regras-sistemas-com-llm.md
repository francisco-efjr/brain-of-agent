# LLM — Sistemas que usam modelos de linguagem

Legenda em [regras-metodo.md](regras-metodo.md). Vale para produtos e automações que chamam LLM em produção (prompts de produto, agentes do produto, pipelines de texto, voz ou classificação).

## Obrigatório

- **LLM-01** [A · C9] Saída de LLM é entrada de usuário desconhecido: confira, limite, normalize e avise quando faltar dado. — _por quê:_ sistema com IA precisa se defender da própria IA. _(cap. 7)_
- **LLM-02** [A · C9] Toda saída de LLM num processo passa por checagem automática de estrutura (arquivo existe, número mínimo de itens, marcações obrigatórias, tamanho). — _por quê:_ pegou todos os erros de modelo (texto truncado, formato errado, seção faltando). _(cap. 6)_
- **LLM-03** [A · C9] Dados vêm de fontes reais (API, banco) e o LLM só redige; regras de decisão (limites, permissões, severidade) ficam no código e o modelo só transforma texto livre em fatos. — _por quê:_ o LLM inventava números de mercado; trocar por dado real melhorou e barateou. _(caps. 6, 13; ap. J)_
- **LLM-04** [A · C9] Todo prompt que lida com tempo recebe data e hora atuais; todo prompt com números diferencia vazio de zero, com o mesmo trecho de instrução reaproveitado; ao receber um número de assistente, pergunte se foi medido ou não encontrado. — _por quê:_ lembrete de "amanhã" foi para o ano errado; campo vazio virou zero. _(cap. 7)_
- **LLM-05** [A · C9] Regras de prompt ficam centralizadas em trechos únicos reaproveitados. — _por quê:_ dois prompts contraditórios sobre o mesmo caso geraram comportamento aleatório. _(cap. 7)_
- **LLM-06** [A · C9] Normalize os parâmetros das ferramentas (limite ao máximo, limpe nomes) em vez de devolver erro ao modelo. — _por quê:_ cada erro de parâmetro custa uma volta paga. _(cap. 7)_
- **LLM-07** [A · C9] Ajuste prompts lendo as saídas reais anteriores (fórmulas repetidas, tom que escorrega, humor por item). _(cap. 7)_
- **LLM-08** [A · C4 C9] Nos testes de integração em desenvolvimento, guarde em cache as respostas do LLM e só pague nova chamada por comando explícito. — _por quê:_ o LLM não é determinístico e cobra por chamada. _(ap. J)_
- **LLM-09** [A · C9] Detecção (fraude, phishing, triagem) usa várias camadas determinísticas; o LLM é uma voz com peso limitado, nunca o juiz único, e cada afirmação dele é conferida contra dados concretos. _(cap. 18)_
- **LLM-10** [A · C9 C10] Classificação e roteamento fechados usam modelo pequeno especializado, ajustado com dados próprios, calibrado e medido com casos próprios; não se configura "agir só com alta confiança" confiando na confiança de modelo pequeno. — _por quê:_ fazem o serviço por centavos sem inventar formato, mas a confiança declarada enganou. _(caps. 13, 22; ap. J)_
- **LLM-11** [A · C9] Mostre a saída do modelo numa forma que o usuário entenda (unidades do domínio em vez de porcentagem crua). _(interlúdio 2)_
- **LLM-12** [A · C9] Pipeline de mídia gerada (voz, vídeo) usa blocos curtos com fim natural de frase, rejeita saída com duração fora do esperado, guarda cache por bloco com manifesto e valida o texto final; mídia gerada é tratada como sujeita a invenção. — _por quê:_ bloco longo demais gerou minutos de áudio inventado. _(ap. J)_
- **LLM-13** [A · C9] O prompt de sistema de agentes do produto orienta: usar ferramenta quando melhora a correção, chamadas paralelas quando independentes, ferramentas próprias de leitura e busca, e dividir o que é divisível. _(cap. 3)_
- **LLM-14** [A · C9 C12] Cadeias de agentes têm verificação entre cada etapa; prefira harness simples, agente direto, testes e revisão. — _por quê:_ dez etapas com 90% de acerto cada dão cerca de 35% no fim. _(cap. 15)_
- **LLM-15** [A · C9 C10] Ao derivar ou publicar modelo ou acervo, credite toda a cadeia (base, mescla, destilação), preserve os avisos de licença e documente origem e licença de cada acervo reutilizado. _(cap. 12; interlúdio 2)_

## Sinais de alerta

- **LLM-S01** [A · C9] O LLM preenche vazio com o mais provável: data plausível, número redondo, zero para ausente; isso não é bug de código e precisa de trava no prompt e na checagem. _(cap. 7)_
- **LLM-S02** [A · C9] Temperatura baixa é previsível; alta é criativa ou errada; uma amostra não prova comportamento. _(cap. 1; ap. B)_
