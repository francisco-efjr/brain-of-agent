# Cartão A/B/C, configurações e padrões de projeto

Base: V-42 (Meta "Agents Rule of Two", 31/10/2025; arXiv 2506.08837; arXiv 2510.09023; resumo de Simon Willison), V-14 (trifecta letal, 16/06/2025, classe B), V-13. Conferido em 2026-10-10. Os PDFs dos artigos não foram lidos pelo validador; a contagem de seis padrões e os nomes vêm do post de Willison. Os dados do desafio de red team humano (500 participantes, US$ 20 mil) também vêm do post de Willison, sem confirmação no resumo do artigo: **Não verificado**.

## Cartão do agente

| Propriedade | Pergunta | Evidência a anotar |
| --- | --- | --- |
| A | O agente processa entrada que um terceiro pode controlar (e-mail recebido, página, issue, PDF, resultado de busca, nome de arquivo)? | Onde o texto entra; quem escreve |
| B | Acessa dados privados ou sistemas sensíveis (CRM, banco, segredos, arquivos do usuário, sessões)? | Quais dados; com qual credencial |
| C | Pode mudar estado ou comunicar para fora (enviar e-mail, gravar, chamar API de escrita, abrir URL, executar comando)? | Qual ação; irreversível? |

Regra (Meta): numa mesma sessão, no máximo duas das três; com as três, o agente não deve rodar de forma autônoma (supervisão humana, por exemplo aprovação, ou novo contexto). O agente pode mudar de configuração dentro da sessão: reexamine o cartão quando uma tool, uma fonte ou uma permissão nova entrar. A trifecta letal de Willison (dados privados, conteúdo não confiável, comunicação externa) é a mesma ideia com outra redação; V-42 a supera em rigor.

## Configurações e o que restringir

| Config | Significa | Restringir | Exemplos de barreira |
| --- | --- | --- | --- |
| AB | Lê entrada não confiável e acessa dados sensíveis, sem agir para fora | C (comunicação/estado) | Confirmar antes de enviar, reservar ou pagar; limitar requisições a URLs confiáveis; saída só em canal interno; sem render de imagens/links com dados |
| AC | Lê entrada não confiável e age para fora, sem dados sensíveis | B (acesso) | Sandbox restritivo; sem dados de sessão pré-carregados; credencial mínima e descartável |
| BC | Acessa dados sensíveis e age para fora, entrada só confiável | A (entrada) | Filtrar fontes por autoria; revisão humana do que entra |
| ABC | As três | Remover uma, separar ou aprovar | Humano aprova no ponto de saída, descrevendo o alcance; ou dois agentes com fronteira |

Escolha a barreira pelo menor custo de utilidade: remover C costuma custar menos do que remover A.

## Os seis padrões de projeto (nomes: post de Willison; descrições: redação própria)

| Padrão | Ideia | Reduz | Custo de utilidade |
| --- | --- | --- | --- |
| Action-Selector | O agente escolhe uma ação de uma lista fixa sem ler o retorno da tool | C e injeção por retorno | Sem encadeamento dinâmico |
| Plan-Then-Execute | O plano é fixado antes de ler conteúdo externo; o conteúdo lido não muda o plano | A (efeito sobre o plano) | Menos adaptação a surpresas |
| LLM Map-Reduce | Um leitor processa cada item não confiável isoladamente e só devolve dados limitados (campos, enum) | A (contaminação cruzada) | Perde nuance; precisa de schema |
| Dual LLM | Um modelo sem privilégios lê o conteúdo não confiável; o modelo com privilégios só vê referências/saídas restritas | A para o modelo com B/C | Complexidade e latência |
| Code-Then-Execute | O modelo gera código/plano executável a partir da tarefa; a execução é determinística | Variação em runtime | Exige sandbox para o código |
| Context-Minimization | Remove do contexto o texto original do usuário/dados não confiáveis quando não é mais necessário | Persistência da injeção | Perde histórico |

As colunas "Reduz" e "Custo de utilidade" são **Inferidas** a partir de V-42; o PDF do artigo não foi lido. O artigo de padrões analisa o equilíbrio entre utilidade e segurança e propõe padrões com resistência comprovável (resumo arXiv, V-42). Adote padrões como projeto, não como talismã: cada um tem um custo e uma condição de uso.

## Teste de defesa

Uma defesa só conta se resistir a um atacante que itera (V-42). Filtros de entrada/saída e a instrução "ignore comandos injetados" entram no plano como camada, com o rótulo "reduz risco, não é barreira". A pesquisa de 24/11/2025 descreve três camadas no produto de navegador da Anthropic (treino por reforço com injeções simuladas, classificadores sobre todo conteúdo não confiável, red team humano contínuo) e uma taxa de sucesso de ataque de 1% contra um atacante adaptativo Best-of-N com 100 tentativas por ambiente, que a própria Anthropic chama de risco ainda significativo (V-43). Esse 1% é de um ambiente de teste do fabricante: não vira meta do seu sistema.

## Perguntas rápidas para o interrogatório de um agente novo

1. Qual é a coisa mais danosa que a tool de maior alcance pode fazer? Ela exige confirmação?
2. Qual texto escrito por um terceiro chega ao contexto? Em que posição (system, usuário, `tool_result`)?
3. Quais credenciais o agente carrega? São as do usuário ou dedicadas e mínimas?
4. O que acontece se uma resposta de tool contiver instruções?
5. Existe limite de turnos, de custo e de chamadas externas por sessão?
6. A memória do agente é compartilhada entre clientes ou sessões?
7. Existe log do que o agente leu e fez, sem segredos?
8. Quem revoga o acesso e como?
