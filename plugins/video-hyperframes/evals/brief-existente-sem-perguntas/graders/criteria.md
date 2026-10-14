---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Não faz pergunta de brief que o BRIEF já responde (ângulo, duração, destino, formato, idioma, público, se há storyboard, se é automação). No máximo pede algo que realmente falta, como o arquivo `fonte-dos-fatos.md` citado em Assets, que não está no ambiente, ou faz uma pergunta de roteamento.
2. Reconhece que `flow: automation` com `storyboard: yes` leva ao modo colaborativo: o plano (storyboard) é mostrado e aprovado pelo usuário antes de construir os quadros.
3. Lista os próximos passos em ordem coerente: verificar o ambiente (preflight), garantir fonte e fatos (ledger, sem número inventado), definir o design (`frame.md` e tokens), montar o storyboard para aprovação, construir e revisar os quadros (`check`, `snapshot`, contact sheet), preview e só então o render com o ok do usuário. Como `narration: no`, trata o vídeo como sem voz (texto na tela) e não propõe narração.
4. Responde à pergunta do usuário (o próximo passo e o seguinte) de forma concreta, sem repetir o conteúdo do BRIEF por extenso e sem afirmar ter criado, lido ou executado arquivos do projeto que não existem no ambiente.
FAIL if qualquer um ocorrer: refaz a entrevista (pergunta angle, length, destination, storyboard ou flow); pula o gate de aprovação do storyboard; propõe renderizar sem preview e ok; propõe narração apesar de `narration: no`; afirma ter criado o projeto ou arquivos.
