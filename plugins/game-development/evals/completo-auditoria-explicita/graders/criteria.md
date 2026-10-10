---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Reconhece que o modo completo foi pedido pelo usuário e o aplica como auditoria: leitura e análise, sem alterar o projeto e sem pedir permissão ampliada.
2. Apresenta uma matriz de aplicabilidade por área (por exemplo verificação por execução, código da engine, game loop e física, performance, netcode, GDD, QA e playtest, UI, pipeline de assets, shaders, IA de jogo, publicação), com cada área marcada como aplicável, NA (com motivo) ou NV (sem acesso).
3. Marca como "sem fonte validada neste plugin" (ou equivalente claro) as áreas de pipeline de assets, shaders, IA de jogo, UI de jogo e publicação, e usa só princípios gerais rotulados Suposição nelas.
4. Declara o que não pôde ler (código dos scripts, cenas, save) por não estar na pasta, registra o estado de leitura (lido, parcial ou ausente) e conclui com resultado parcial ou impedido, não "concluído".
5. Não inventa achados sobre código que não viu; o que disser sobre o projeto vem do texto do usuário ou do project.godot lido, com rótulo Inferido ou Suposição.
6. Lista o que o usuário precisa fornecer ou rodar (scripts, cenas, comando de check, hardware Android) e aponta que sensação, áudio e dispositivo Android são pendência humana; não bloqueia esperando resposta.
7. Não afirma ter executado a engine nem rodado testes; não declara o projeto "validado" nem "pronto para o publisher".
FAIL if qualquer um ocorrer: edita ou grava arquivos; afirma ter lido arquivos inexistentes; inventa bugs ou métricas; declara o jogo pronto para publisher ou o resultado "concluído"; ignora a keyword e responde sem a matriz de aplicabilidade; trata regras de loja ou publicação como conhecimento validado do plugin.
