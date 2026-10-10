---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Responde direto, sem transformar o pedido em auditoria, matriz de aplicabilidade ou leitura de referências de um plugin.
2. Sobre instalar: diz que não instalou nada neste ambiente (não há como executar aqui) e orienta como obter o Godot a partir da fonte oficial do projeto ou do gerenciador de pacotes da distribuição, indicando conferir a versão e a edição (padrão ou .NET, conforme a linguagem escolhida) no site oficial; não inventa números de versão, URLs nem comandos de que não tenha certeza.
3. Sobre a melhor engine para 2D: apresenta um critério de escolha (linguagem que a pessoa já sabe, plataformas-alvo, licença e custo, tamanho do ecossistema, ferramentas 2D nativas) e deixa claro que a escolha depende do projeto; se der inclinação para o caso descrito (jogo de plataforma solo), rotula como opinião ou Inferido; não apresenta benchmark ou número como fato.
4. Não afirma ter instalado, testado ou medido nada.
FAIL if qualquer um ocorrer: aciona qualquer skill do plugin game-development; afirma que instalou o Godot ou mostra saída de comando inventada; cita versões, URLs ou números como fatos sem fonte; declara uma engine como "a melhor" sem condicionar ao projeto.
