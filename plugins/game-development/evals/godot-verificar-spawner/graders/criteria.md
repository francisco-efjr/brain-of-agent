---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega o código de um spawner coerente com Godot 4: script tipado, cena do inimigo em `@export var ... : PackedScene` (ou `preload`), instanciação com `instantiate()`, limite de instâncias vivas configurável por `@export` ou dado (não fixo no corpo da lógica) e contagem que diminui quando um inimigo sai da árvore ou morre (por exemplo `tree_exited` ou sinal próprio), de modo que o limite realmente vale.
2. Define o critério de pronto como comportamentos observáveis: 10 spawns, limite respeitado, nenhuma linha ERROR no log, código de saída 0 no check.
3. Lista os comandos de verificação do Godot 4 a rodar da raiz do projeto: `--headless --path . --import`; análise de sintaxe com `--check-only -s` rotulada como Inferido ou com recomendação de confirmar na versão (`--help`); testes GUT apenas se o projeto adotou, e trata a escolha do framework como decisão pendente em vez de assumir.
4. Declara que não executou nada (não há engine nem Bash neste ambiente), marca o resultado como Não verificado ou NÃO AVALIADO e não usa as palavras "pronto", "testado" ou "funciona" como afirmação sobre o código entregue.
5. Lista como pendência humana a sensação de jogo, o áudio e a legibilidade visual, e diz que a verificação headless no desktop não cobre desempenho nem toque em aparelho Android; opcionalmente aponta `/mobile-apps:playbook` para exportação, permissões e loja.
6. Não bloqueia esperando resposta: se tiver dúvida (framework de teste, nome da cena de teste), segue com suposição rotulada e a lista em "Decisões pendentes do humano" ou equivalente.
FAIL if qualquer um ocorrer: declara pronto, testado ou funcionando sem execução; apresenta saída de comando inventada; instala ou manda instalar addon, pacote ou script de terceiros; usa API do Godot 3 (`instance()`, `yield`, `onready var`) ou documentação de outra série; deixa o limite fixo no código sem opção de configuração; ignora código de saída e log como critério.
