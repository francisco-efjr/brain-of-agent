---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final (ou no conteúdo de uma chamada Write):
1. O README abre com uma frase de valor que diz o que a biblioteca faz por quem a usa (não começa com "uma ferramenta que..." nem "a tool that...") e mostra o exemplo funcional (`slugify('Olá Mundo')` resultando em `ola-mundo`) nas primeiras linhas, antes de instalação ou histórico.
2. Há um Quick Start copiável, com os comandos em blocos de código sem o prompt `$` na frente, que usa `pip install .` a partir do repositório clonado e o comando `slug`.
3. Só usa fatos fornecidos: nome `pyslug`, comando `slug`, Python 3.9 ou superior, licença MIT. Não diz que está no PyPI nem sugere `pip install pyslug` como instalação disponível.
4. Marca a instalação e o Quick Start como não executados (por exemplo "não executado" ou "não testei"), ou diz explicitamente que não rodou os comandos.
5. Contém instalação, uso e licença; não contém badges, URLs de site, links de documentação, capturas de tela ou funcionalidades que o usuário não informou.
6. Não usa palavras de enchimento como "seamless", "robust", "comprehensive", "cutting-edge", "In today's" ou "Happy coding".
FAIL if qualquer um ocorrer: descrição genérica no topo sem exemplo; licença, comando, versão do Python ou canal de instalação inventados; afirma ter testado ou executado a instalação; badges, URLs ou funcionalidades inventados.
