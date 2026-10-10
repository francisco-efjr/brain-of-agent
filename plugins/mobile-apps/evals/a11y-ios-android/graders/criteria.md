---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Cobre os dois lados (SwiftUI e Compose), com achados separados por plataforma.
2. iOS: aponta `onTapGesture` em uma imagem (sem papel de botão nem rótulo) e recomenda `Button` com rótulo acessível (por exemplo "Fechar"); cita alvo de 44x44 pt (mínimo absoluto 28 pt); aponta tamanho de fonte fixo (`.system(size:)`) como obstáculo a Dynamic Type e recomenda estilos de texto dinâmicos, citando Dynamic Type até 200% como alvo de teste.
3. Android: aponta o ícone clicável de 32.dp (elemento personalizado, não um `IconButton`) abaixo do mínimo de 48x48 dp e sugere ampliar a área de toque (por exemplo `sizeIn` com 48.dp) e declarar o papel de botão; aponta `contentDescription = "Botão fechar"` por repetir o tipo e sugere "Fechar"; aponta a altura fixa de 24.dp no texto como risco de corte com a fonte ampliada; não acusa `sp` como erro (o uso de `sp` está correto).
4. Contraste: sinaliza o cinza sobre fundo branco como risco de ficar abaixo de 4,5:1 para texto pequeno (3:1 só para texto grande ou negrito, nos limiares de cada plataforma) e diz que o valor exato precisa ser medido com a cor real, sem inventar a razão.
5. Informa que a passagem manual com VoiceOver e TalkBack, e o teste com a maior fonte, são verificações humanas que ficam como pendência; não afirma ter testado com leitor de tela.
6. Rotula Verificado, Inferido ou Suposição, e declara que a revisão foi por leitura do código.
FAIL if qualquer um ocorrer: declara que testou com VoiceOver ou TalkBack; usa números não oficiais para alvo ou contraste (por exemplo 20x20 pt como alvo); ignora uma das plataformas; recomenda remover o `contentDescription` de um elemento interativo; acusa falsamente `sp` como problema.
