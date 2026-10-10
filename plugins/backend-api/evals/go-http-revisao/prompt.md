---
name: go-http-revisao
description: Mede se o plugin revisa um handler Go confirmando a versão do go.mod e aplicando as convenções da stack (ServeMux com método e PathValue, erros tratados, cliente com timeout, corpo fechado, validação do id contra SSRF), sem afirmar execução.
tags: [backend-api, stack-conventions]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Confirma go 1.23 do go.mod, propõe ServeMux com padrão de método e PathValue, trata erros com %w, usa cliente com timeout, fecha o corpo, valida o id contra SSRF e injeção de caminho, propaga status adequado e cita gofmt, go vet, golangci-lint e go test como não executados."
model: sonnet
---
Revisa esse serviço Go pra mim. O `go.mod` diz `go 1.23`. É um proxy simples para uma API interna.

```go
package main

import (
	"io"
	"net/http"
	"strings"
)

func main() {
	http.HandleFunc("/posts/", func(w http.ResponseWriter, r *http.Request) {
		id := strings.TrimPrefix(r.URL.Path, "/posts/")
		resp, _ := http.Get("https://api.interno/" + id)
		b, _ := io.ReadAll(resp.Body)
		w.Write(b)
	})
	http.ListenAndServe(":8080", nil)
}
```

Não tenho o repositório aberto aqui; use só o que escrevi.
