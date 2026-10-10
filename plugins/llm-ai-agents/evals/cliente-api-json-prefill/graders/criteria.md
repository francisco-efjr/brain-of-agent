---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Identifica o prefill (mensagem final do assistente com «{») como o problema de projeto: não é mais suportado a partir da família Claude 4.6 e não garante JSON válido; recomenda saída estruturada.
2. Propõe `output_config.format` com `json_schema`, com `additionalProperties: false` nos objetos (nome do cliente como string, valor como número, campos obrigatórios), em vez de depender do texto livre; avisa que o parâmetro beta antigo `output_format` está obsoleto e que o schema aceita só um subconjunto do JSON Schema (sem recursivo, sem `minLength`/`maxLength`; restrições vão para a descrição e para validação local).
3. Trata `stop_reason` antes do `json.loads`: `refusal` é um veredito de bloqueio (não falha técnica) e `max_tokens` pode produzir saída truncada (repetir com limite maior ou falhar de forma explícita); não faz `resp.content[0].text` sem checar o tipo e a existência do bloco.
4. Avisa que mudar `output_config.format` invalida o cache de prompt se houver cache, e que validar o resultado localmente (por exemplo com um modelo Pydantic) continua necessário.
5. Sugere medir o efeito (taxa de erro de parse antes e depois, em casos reais) e diz que não executou o código nem chamou a API.
6. Não inventa parâmetros do SDK nem afirma que o 2% de falhas será eliminado.
FAIL if qualquer um ocorrer: mantém o prefill como solução; recomenda forçar uma tool com `tool_choice` `any` ou `tool` como garantia do JSON no claude-sonnet-5-5 (a API rejeita com erro 400 nesse modelo); ignora `stop_reason`; inventa parâmetros ou nomes de campo; afirma ter executado o código ou garantido a correção; sugere guardar a chave de API no código.
