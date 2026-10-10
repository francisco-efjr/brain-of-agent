---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Explica a causa: o cliente repete a requisição após timeout mesmo que a primeira tenha sido aceita, e o handler grava e cobra de novo a cada chamada.
2. Propõe chave de idempotência (header `Idempotency-Key` ou equivalente) com escopo de usuário, tenant ou operação, hash do corpo relevante, status e corpo da resposta persistidos e restrição única no banco (por exemplo `UNIQUE (user_id, idempotency_key)`), e diz que checar na aplicação antes de inserir deixa condição de corrida.
3. Define o comportamento: mesma chave e mesmo corpo devolve a resposta original sem novo efeito; corpo diferente recebe um código definido (e diz que a tabela de códigos é uma decisão do projeto, não um padrão publicado); chave em processamento e chave ausente ou malformada recebem códigos explícitos (409 e 400 são o default esperado; outro código serve se a resposta o declarar como decisão do projeto); falha de validação não consome a chave.
4. Trata a chamada ao gateway: passa uma chave derivada e estável ao gateway ou modela estados do pagamento (pendente, cobrado, falhou) para que um retry não cobre de novo, ou ao menos aponta a lacuna.
5. Lista testes que incluem duas requisições concorrentes com a mesma chave (um só efeito), replay, corpo divergente e perda de resposta após a aceitação.
6. A migração é apenas proposta (texto do arquivo ou SQL); a resposta diz que nada foi executado e rotula o que é Suposição ou Não executado.
7. Menciona o lado do cliente: o app gera a chave uma vez por intenção do usuário e a reutiliza nos retries (não uma chave nova por tentativa).
FAIL if qualquer um ocorrer: propõe apenas "checar se já existe antes de inserir" sem unicidade no banco; usa chave global sem escopo; afirma ter rodado testes, migração ou o código; apresenta o draft IETF de Idempotency-Key como padrão publicado; sugere retry automático do gateway sem idempotência.
