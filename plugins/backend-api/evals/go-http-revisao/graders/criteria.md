---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Registra que a versão informada (`go 1.23`, portanto maior ou igual a 1.22) permite o roteamento com método e curinga e sugere `mux.HandleFunc("GET /posts/{id}", ...)` com `r.PathValue("id")`, em vez de `TrimPrefix` manual no caminho.
2. Aponta os erros descartados com `_` em `http.Get` e `io.ReadAll`, e a possível desreferência de `resp` nulo; propõe tratar o erro logo após a chamada e envolver com `%w` quando propagar.
3. Aponta que `http.Get` usa o cliente padrão sem timeout e propõe um `http.Client` com `Timeout` (ou contexto com prazo); aponta a falta de `defer resp.Body.Close()` depois do teste do erro.
4. Aponta o risco de SSRF ou injeção de caminho ao concatenar o `id` na URL e propõe validar (formato esperado, por exemplo numérico ou regex) e escapar (`url.PathEscape`), e mencionar allowlist do destino.
5. Aponta que o status e o erro do upstream não são propagados (respostas 4xx e 5xx viram 200 com o corpo) e propõe traduzir para 502 ou 504 conforme o caso, com corpo de erro padronizado; também menciona limite de leitura do corpo (por exemplo `io.LimitReader`) ou servidor com timeouts.
6. Cita `gofmt`, `go vet`, `golangci-lint` e `go test` como verificações, rotuladas como não executadas, e declara que confirmou a versão pelo `go.mod` informado.
FAIL if qualquer um ocorrer: mantém os erros ignorados; não menciona timeout; ignora o `id` sem validação; recomenda a sintaxe nova de roteamento sem checar a versão; afirma ter compilado ou executado o código.
