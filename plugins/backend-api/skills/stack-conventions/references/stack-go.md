# Go (net/http): roteamento 1.22+, erros, clientes e testes

Fontes (Verificado em 2026-10-10): blog oficial "Routing enhancements for Go 1.22" (V-18, https://go.dev/blog/routing-enhancements, 13/02/2024) e `go.instructions.md` do awesome-copilot (V-18, MIT, destilado: checklist com redação própria; prompt-score do arquivo original 63). Código abaixo é redação própria. **A versão que vale é a do `go` no `go.mod` do projeto**: `grep -E '^go [0-9]+\.[0-9]+' go.mod` e `go version`. Frameworks (Chi, Gin, Echo) e autenticação não são cobertos pelas fontes: lacuna.

## Sumário

1. Checklist
2. Roteamento com o ServeMux novo
3. Handlers, erros e logs
4. Cliente HTTP e servidor com timeouts
5. Goroutines e contexto
6. Testes
7. Ferramentas e busca

## 1. Checklist

- [ ] `go >= 1.22` no `go.mod`? Então use o `ServeMux` com padrão de método e curingas (V-18). Abaixo disso, o comportamento antigo vale: não use sintaxe nova sem checar.
- [ ] Padrões de rota com método (`GET /posts/{id}`); `Request.PathValue("id")` para ler o segmento. `GET` também casa `HEAD`.
- [ ] Sobreposição de padrões sem precedência clara causa **pânico no registro** (na inicialização): rode o binário ou um teste que monte o mux.
- [ ] Erro checado logo após a chamada; nenhum `_` descartando erro de I/O.
- [ ] Erros envolvidos com `fmt.Errorf("...: %w", err)`; comparação com `errors.Is` / `errors.As`.
- [ ] Não logar **e** retornar o mesmo erro: registre na borda (middleware/handler) uma vez.
- [ ] `http.Client` com `Timeout` (ou contexto com prazo); `defer resp.Body.Close()` depois de checar o erro; corpo lido com limite.
- [ ] `http.Server` com `ReadHeaderTimeout` (e demais timeouts conforme o caso) e desligamento gracioso.
- [ ] Corpo de requisição com `http.MaxBytesReader`; JSON com `DisallowUnknownFields` se o contrato rejeita campo desconhecido.
- [ ] Toda goroutine tem caminho de saída (contexto cancelável, canal fechado).
- [ ] Testes table-driven com `httptest`.
- [ ] Entrada de caminho/URL validada antes de compor URLs de saída (SSRF e injeção de caminho); `url.PathEscape`.
- [ ] `gofmt`, `go vet`, `golangci-lint`, `go test` limpos.

## 2. Roteamento com o ServeMux novo

```go
mux := http.NewServeMux()
mux.HandleFunc("GET /posts/{id}", s.getPost)          // casa GET e HEAD
mux.HandleFunc("POST /posts", s.createPost)
mux.HandleFunc("GET /files/{path...}", s.getFile)     // {name...} captura o resto
mux.HandleFunc("GET /{$}", s.root)                    // {$} casa apenas a raiz exata
```

Regras relevantes (V-18): vence o padrão mais específico; dois padrões que se sobrepõem sem que um seja mais específico fazem `Handle`/`HandleFunc` entrar em pânico. Um padrão como `"/posts/"` (sem método, com barra final) casa a **subárvore inteira e todos os métodos**: é a forma antiga e frequentemente indesejada em código novo.

Método não permitido: o mux novo responde 405 com `Allow` automaticamente para padrões com método (comportamento da biblioteca; confirme na versão do projeto).

## 3. Handlers, erros e logs

```go
var ErrNotFound = errors.New("not found")

func (s *Server) getPost(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	if _, err := uuid.Parse(id); err != nil {              // valide o formato esperado
		writeProblem(w, http.StatusBadRequest, "invalid-id", "Invalid post id")
		return
	}
	post, err := s.store.Get(r.Context(), id)
	switch {
	case errors.Is(err, ErrNotFound):
		writeProblem(w, http.StatusNotFound, "post-not-found", "Post not found")
	case err != nil:
		s.log.Error("get post", "err", err, "id", id)       // loga aqui, uma vez
		writeProblem(w, http.StatusInternalServerError, "internal", "Internal error")
	default:
		writeJSON(w, http.StatusOK, post)
	}
}

func writeProblem(w http.ResponseWriter, status int, slug, title string) {
	w.Header().Set("Content-Type", "application/problem+json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(map[string]any{
		"type": "https://api.exemplo.com.br/problems/" + slug, "title": title, "status": status,
	})
}
```

(`uuid` aqui é um pacote qualquer; confirme que existe no `go.mod` com `go list -m` antes de importar.) A camada de armazenamento devolve `fmt.Errorf("get post %q: %w", id, err)`; o handler traduz, sem expor SQL nem caminho de arquivo.

Corpo JSON com limite e campos estritos:

```go
r.Body = http.MaxBytesReader(w, r.Body, 1<<20)        // 1 MiB
dec := json.NewDecoder(r.Body)
dec.DisallowUnknownFields()                            // só se o contrato rejeita campo extra
if err := dec.Decode(&in); err != nil { /* 400 (malformado) ou 413 (excedeu o limite) */ }
```

## 4. Cliente HTTP e servidor com timeouts

```go
var upstream = &http.Client{Timeout: 5 * time.Second}

func fetchUpstream(ctx context.Context, id string) ([]byte, error) {
	req, err := http.NewRequestWithContext(ctx, http.MethodGet,
		"https://api.interno/posts/"+url.PathEscape(id), nil)
	if err != nil {
		return nil, fmt.Errorf("build request: %w", err)
	}
	resp, err := upstream.Do(req)
	if err != nil {
		return nil, fmt.Errorf("call upstream: %w", err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("upstream status %d", resp.StatusCode)
	}
	return io.ReadAll(io.LimitReader(resp.Body, 1<<20))
}

srv := &http.Server{
	Addr:              ":8080",
	Handler:           mux,
	ReadHeaderTimeout: 5 * time.Second,   // valores ilustrativos: dimensione pelo serviço
	IdleTimeout:       60 * time.Second,
}
```

O `http.Get` do pacote usa o cliente padrão **sem timeout**: uma dependência lenta prende a goroutine e o descritor. Orçamento de timeout por salto: derive o `ctx` da requisição com prazo menor que o total do usuário. Desligamento gracioso: `srv.Shutdown(ctx)` ao receber sinal.

## 5. Goroutines e contexto

```go
g, ctx := errgroup.WithContext(r.Context())   // golang.org/x/sync/errgroup: confirme que está no go.mod
g.Go(func() error { return a.Load(ctx) })
g.Go(func() error { return b.Load(ctx) })
if err := g.Wait(); err != nil { /* trate uma vez */ }
```

Toda goroutine que espera I/O ou canal observa `ctx.Done()`. Goroutine "dispare e esqueça" dentro de handler vaza ao cancelar a requisição, a menos que tenha ciclo de vida próprio e documentado.

## 6. Testes

```go
func TestGetPost(t *testing.T) {
	tests := []struct {
		name   string
		path   string
		want   int
	}{
		{"id válido existente", "/posts/" + knownID, http.StatusOK},
		{"id malformado", "/posts/abc", http.StatusBadRequest},
		{"inexistente", "/posts/" + missingID, http.StatusNotFound},
	}
	srv := newTestServer(t)                       // monta o mux real: pega pânico de padrões
	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			rec := httptest.NewRecorder()
			srv.ServeHTTP(rec, httptest.NewRequest(http.MethodGet, tc.path, nil))
			if rec.Code != tc.want {
				t.Fatalf("status = %d, want %d; body=%s", rec.Code, tc.want, rec.Body)
			}
		})
	}
}
```

Teste de concorrência com `go test -race`. Contrato e autorização: casos negativos com dois usuários (ver `api-test-suite`).

## 7. Ferramentas e busca

```bash
gofmt -l .
go vet ./...
golangci-lint run
go test -race ./...
grep -rEn "http\.(Get|Post|Head)\(|http\.DefaultClient" --include=*.go .
grep -rEn ", _ :?= |_, _ = " --include=*.go . | head -50      # erros descartados (heurística)
grep -rEn "HandleFunc\(\"/[^ \"]*/\"" --include=*.go .       # padrões antigos de subárvore sem método
```

Confirme a versão do `golangci-lint` e a configuração do projeto (`.golangci.yml`) antes de apontar achados de lint.
