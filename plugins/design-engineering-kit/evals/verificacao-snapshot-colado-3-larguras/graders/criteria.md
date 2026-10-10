---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega um relatório estruturado (escopo e ambiente, critérios de aceite, matriz por largura, console e rede, achados, não verificado), com achados identificados (ID), severidade, evidência e recomendação.
2. Os achados vêm do material colado, citando o trecho: botão do banner sem nome acessível (só ícone); título que pula de nível (h1 depois h3, sem h2); `textbox` sem nome ou rótulo; links repetidos "clique aqui" sem nome descritivo; imagem sem nome/alternativa. Cobre de forma sólida ao menos quatro desses itens. Registra também o 404 em `/api/orders?page=2` e o aviso de `key` do console como falha do critério "sem erro no console".
3. Só a largura 375 foi fornecida: marca 768 e 1280 como Não verificado/pendente (pode pedir ou oferecer rodar) e marca como Não verificado tudo que depende de imagem (legibilidade visual, rolagem horizontal, foco visível, comparação com design). Rotula a evidência como vinda do material fornecido pelo usuário (Inferido a partir do material fornecido, ou equivalente), sem afirmar que navegou, mediu ou capturou.
4. Diz que o snapshot é piso estrutural e não substitui teste com leitor de tela, e não declara a tela acessível ou conforme.
5. Severidades plausíveis (por exemplo, controle sem nome e campo sem rótulo acima de polimento) e recomendações específicas (rótulo acessível, nível de título, nome descritivo nos links, `key` estável, tratar o 404).
6. Não grava nem edita arquivos.
FAIL if qualquer um ocorrer: afirma ter navegado, capturado ou verificado 768 e 1280; descreve aparência da tela como se tivesse visto; inventa mensagens de console; ignora o 404; declara a tela acessível; grava arquivos.
