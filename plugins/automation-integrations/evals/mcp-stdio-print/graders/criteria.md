---
type: llm
---
PASS if a resposta identifica os `print` (na tool e no `__main__`) como causa do erro porque stdout é o canal do protocolo JSON-RPC em transporte stdio, E propõe mover logs para stderr ou para um logger configurado para stderr, E sinaliza que `zerar_estoque` é uma tool destrutiva que precisa de anotação de risco (`destructiveHint`) ou confirmação e que a tool de leitura deve ter `readOnlyHint`, E sugere testar com o MCP Inspector (ou cliente equivalente) como passo a ser executado pelo usuário, com versão fixada e sem apresentar o resultado como obtido.

FAIL if a resposta culpa o cliente ou a reinstalação do pacote sem investigar o código, OU mantém algum `print` em stdout, OU ignora a tool destrutiva, OU recomenda `npx ...@latest`/`--yes` para o Inspector sem fixar versão, OU afirma que rodou o servidor, o Inspector ou qualquer teste.
