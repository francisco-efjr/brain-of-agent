---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Diz que não se copia o `linear()` do CSS e traduz a mecânica para a plataforma: mola do Compose (`spring`) com a rigidez dos tokens e `dampingRatio` igual a 1 menos o bounce (ou damping dividido por 2 vezes a raiz da rigidez: 1,0 para `smooth`, 0,85 para `snappy`), crossfade de 180 ms como `tween`. Apresenta o esboço em Kotlin como Inferido/a conferir na versão do projeto, sem afirmar que compilou.
2. Trata "Reduzir movimento" como ponto único no tema/objeto de tokens (sem `if` espalhados), ligado à preferência do sistema (escala de animação / remover animações), trocando deslocamento e escala por fade ou `snap`; rotula como Inferido ou a confirmar o comportamento exato do Compose com a escala do sistema.
3. Sugere usar `ModalBottomSheet` ou componente da plataforma antes de implementar um sheet custom, e trata durações, curvas e tokens do Material 3 como Não verificáveis aqui (a confirmar na documentação oficial), sem apresentá-los como fatos.
4. Não herda a estética macOS (Liquid Glass, vibrancy, métricas de janela, SF Pro) para o Android; herda estrutura e regra.
5. Sobre verificação: diz que o Playwright não verifica app Android nativo e indica `@Preview`, emulador ou dispositivo (por exemplo, escala de animação em 0 e em 10x); deixa claro que nada foi executado.
FAIL if qualquer um ocorrer: copia `linear()` ou CSS para Kotlin; afirma valores do Material 3 como verificados; afirma ter compilado ou testado; recomenda Playwright para verificar Android; ignora reduzir movimento; grava arquivos.
