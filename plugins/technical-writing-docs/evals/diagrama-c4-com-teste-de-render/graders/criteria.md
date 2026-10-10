---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final (ou no conteúdo de uma chamada Write):
1. Entrega o diagrama em bloco cercado com `mermaid`, num único nível (contêineres), com menos de 15 nós, cobrindo: cliente (pessoa), web app React, API Node, PostgreSQL, fila Redis, worker e provedor de e-mail externo, com as relações descritas (HTTPS/JSON, leitura e escrita, publicação e consumo de jobs, envio SMTP).
2. Avisa que o suporte a C4 no Mermaid é experimental (a sintaxe pode mudar) e pede ao usuário que confira o preview do arquivo no GitHub, ou indica como testar (por exemplo o bloco `info` mostra a versão do Mermaid usada pelo GitHub).
3. Oferece ou já entrega o fallback em `flowchart` com a mesma informação para o caso de o C4 não renderizar.
4. Acompanha o diagrama de um texto curto que explica o que ele mostra e para quem, e rotula como Inferido ou Suposição o que não veio da descrição (por exemplo, protocolo entre worker e Redis).
5. Não afirma que o diagrama renderiza no GitHub e não diz ter testado; o status do render é "não verificado" ou "a confirmar pelo usuário".
FAIL if qualquer um ocorrer: afirma que renderiza sem teste; mistura níveis (contexto, contêineres e componentes no mesmo diagrama); 15 nós ou mais; sem aviso de experimental nem fallback; inventa contêineres ou tecnologias que o usuário não citou.
