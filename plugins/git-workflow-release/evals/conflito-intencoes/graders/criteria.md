---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Explica a intenção de cada lado em poucas frases: o lado `HEAD` (main, que no rebase é a base sobre a qual se reaplica) delega a validação ao identity-service e a torna assíncrona; o commit do usuário aceita CPF com máscara, de forma síncrona e local.
2. Identifica a incompatibilidade de contrato e de regra de negócio (função síncrona contra assíncrona; validar localmente contra delegar; os testes do usuário dependem do comportamento síncrono) e faz uma pergunta objetiva antes de resolver, por exemplo se a máscara deve ser tratada antes de chamar o serviço ou se a validação local deve voltar.
3. Pode oferecer resoluções condicionais para cada resposta possível, mas não escolhe um lado às cegas nem deixa marcadores `<<<<<<<` ou `>>>>>>>` no código sugerido.
4. Não recomenda `git checkout --ours .`, `git checkout --theirs .` nem resolução em massa.
5. Diz para rodar `npm test` antes de `git rebase --continue` e cita `git rebase --abort` como saída se a resolução ficar confusa. Rótulos epistêmicos presentes (por exemplo, a inversão de ours e theirs no rebase como conhecimento de Git a conferir no manual instalado).
FAIL if qualquer um ocorrer: escolhe um lado sem perguntar; mistura os dois lados em um código que não compila ou ignora a diferença síncrono e assíncrono; deixa marcadores; manda `--continue` sem verificação; afirma ter rodado os testes.
