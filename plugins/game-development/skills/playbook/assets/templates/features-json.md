# features.json — lista de funcionalidades do projeto

Uso: projeto de várias sessões. O modelo sobrescreve menos JSON que Markdown (Anthropic Engineering, 26/11/2025). Salve como `features.json` na raiz.

```json
[
  {
    "id": "dash-01",
    "categoria": "gameplay",
    "descricao": "Dash consome stamina e respeita colisão com paredes",
    "passos": [
      "abrir a cena de teste",
      "acionar dash via sonda de input (--drive tests/dash.drive)",
      "ler stamina e posição no log (--probe)"
    ],
    "passes": false
  }
]
```

## Regras de edição

1. Só o campo `passes` muda, e só depois de rodar os `passos` e colar a saída no relatório.
2. Nunca apague nem edite `passos` ou `descricao`; mudança de requisito vira item novo.
3. Uma funcionalidade por sessão: o primeiro item com `passes: false`.
4. Item sem sonda possível fica `false`, com nota em `progresso-sessao` (pendência humana).

Campos opcionais úteis: `"depende_de": ["id"]`, `"humano": ["sensação do dash"]`.
