---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Mantém o design system como autoridade: fonte do sistema, ícones Lucide, acento `--accent`, raio e sombra por token permanecem; não recomenda trocar para webfonts como Geist, Satoshi ou Newsreader, não recomenda trocar Lucide por outro conjunto, não muda o acento nem os raios. Se citar proibições de fonte ou ícone de skills de estética, diz que elas não sobrepõem o design system.
2. Propõe mudanças dentro do sistema, citando tokens pelo nome: hierarquia (títulos de seção, peso e cor de rótulos), ritmo de espaçamento na grade de 4 px, divisão do cartão grande em grupos, alinhamento rótulo e controle, densidade, estados (foco, hover), texto de ajuda, divulgação progressiva ou duas colunas em tela larga. Sem valores crus novos (hex, px fora da escala).
3. Declara a precedência em uma frase ou equivalente: design system do projeto primeiro; direções de gosto só sem sistema ou com pedido de nova direção.
4. Rotula como Suposição ou Inferido o que depende de tela não vista; não afirma ter renderizado nada.
5. Tamanho proporcional: uma proposta organizada, não uma auditoria completa nem código completo.
FAIL if qualquer um ocorrer: recomenda trocar fonte, ícones, acento, raios ou sombras; aplica regras de proibição de fonte/ícone como se valessem sobre o sistema; escreve implementação completa quando pediu proposta; afirma ter visto a tela; grava arquivos.
