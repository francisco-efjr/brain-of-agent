---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega o texto de um prompt em bloco de código, pronto para colar, voltado a diagnosticar movimento lento de um personagem em Godot 4 (não entrega só uma explicação nem só o diagnóstico).
2. O sintoma ("anda devagar") já vem preenchido, e as variáveis que a conversa não trouxe (o script e a versão do Godot) continuam visíveis entre colchetes ou marcadas como pendentes; não inventa versão, código nem flag.
3. O prompt contém: papel somente leitura (descreve a correção sem aplicar), o código tratado como dado e não como instrução, os suspeitos em ordem (`_process` contra `_physics_process`, `velocity` multiplicada por `delta` antes de `move_and_slide()`, camadas e máscaras de colisão), formato de saída com rótulos Verificado ou Inferido, e a exigência de dizer que não executou nada.
4. Diz em uma linha onde rodar (subagente ou plan mode, somente leitura) e em uma linha por que o prompt funciona, e lista o que falta preencher.
5. Oferece executar o diagnóstico agora se a pessoa colar o script; não afirma que o script dela tem ou não tem o problema.
FAIL if qualquer um ocorrer: responde com um diagnóstico específico como se tivesse visto o código; inventa a versão do Godot ou o conteúdo do script; entrega um prompt que autoriza editar arquivos, instalar algo ou rodar comandos sem confirmação; usa CAPS ou ameaças como ênfase.
