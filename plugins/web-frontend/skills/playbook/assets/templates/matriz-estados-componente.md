# Matriz de estados por componente

Preencha uma linha por estado de cada componente tocado e anexe a evidência (captura ou teste). Base: matriz de componente e roteiro de `apple-design.md` do brain-of-agent (MIT), adaptada à web. Componente: [nome], arquivo: [caminho].

## Matriz

| Elemento | Estados a verificar | Cobertos? | Evidência |
| --- | --- | --- | --- |
| Campo | vazio, foco, preenchido, inválido, somente leitura, desabilitado, texto longo | [sim / não / NA com motivo] | [captura ou teste] |
| Ação (botão) | normal, foco, pressionado, processando, indisponível, erro | | |
| Lista | vazia, carregando, resultados, seleção, erro, grande volume e paginação | | |
| Diálogo | foco inicial, tabulação contida, validação, fechar e devolver o foco | | |
| Navegação | item atual, teclado, voltar e deep link, overflow em tela estreita | | |
| Dado remoto | inicial, carregando, sucesso, vazio, erro, atualizando, desatualizado após erro | | |

## Roteiro de 7 passos

1. Concluir a tarefa principal com entrada pertinente.
2. Repetir o passo 1 só por teclado.
3. Usar dados extremos (nome muito longo, 10 mil itens, texto de outro idioma).
4. Interromper a requisição ou a transição no meio.
5. Provocar erro e recuperar.
6. Confirmar a persistência (recarregar e rever; o estado vem do servidor?).
7. Avaliar tema e preferências suportadas (escuro, movimento reduzido, zoom 200%).

Meça o contraste no estado e no fundo reais; não estime números pela imagem.

## Resultado

- Estados sem cobertura: [lista e decisão: implementar, adiar com motivo, NA]
- Comportamentos inferidos (não observados): [lista]
