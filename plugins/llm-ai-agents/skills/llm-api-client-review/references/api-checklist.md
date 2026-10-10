# Cliente da API Claude: trechos errado e certo

Base: V-37 (tool use, structured outputs, streaming), V-35 (citações), V-24 (prompt caching), V-38. Conferido em 2026-10-10. Os trechos são Python ilustrativo com o SDK `anthropic`; **nenhum foi executado**. Nomes de parâmetro e eventos vêm das páginas oficiais citadas em V-37; o SDK instalado pode expor nomes ligeiramente diferentes (por exemplo, parâmetro novo ainda só via `extra_body`): confira na versão do usuário. `MODELO` é o modelo-alvo informado; não invente identificador.

## 1. Prefill (obsoleto a partir da família 4.6)

Errado:

```python
resp = client.messages.create(
    model=MODELO, max_tokens=1024,
    messages=[
        {"role": "user", "content": "Classifique o ticket: ..."},
        {"role": "assistant", "content": "{"},          # prefill: não suportado nos modelos 4.6+
    ],
)
dados = json.loads("{" + resp.content[0].text)
```

Certo (saída estruturada; o formato é garantido pela API):

```python
SCHEMA = {
    "type": "object",
    "properties": {
        "categoria": {"type": "string", "enum": ["cobranca", "entrega", "outro"]},
        "urgente": {"type": "boolean"},
        "justificativa": {"type": "string", "description": "Explicação curta, 1 a 3 frases."},
    },
    "required": ["categoria", "urgente", "justificativa"],
    "additionalProperties": False,
}
resp = client.messages.create(
    model=MODELO, max_tokens=1024,
    messages=[{"role": "user", "content": "Classifique o ticket: ..."}],
    output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
)
if resp.stop_reason == "refusal":      # veredito de bloqueio, não falha técnica
    return bloquear(resp)
if resp.stop_reason == "max_tokens":   # saída possivelmente truncada
    return repetir_com_limite_maior()
texto = next(b.text for b in resp.content if b.type == "text")  # procure o bloco pelo tipo, não por posição
dados = json.loads(texto)
```

Pontos (V-37): `additionalProperties: false` obrigatório em objetos; sem schema recursivo; sem `minimum`/`maximum` nem `minLength`/`maxLength`; `minItems` só 0 ou 1; limites de 20 tools estritas, 24 parâmetros opcionais e 16 com `anyOf`/arrays de tipos; restrições que o schema não aceita vão para a descrição e para validação local; a gramática compilada é cacheada por 24 horas; mudar `output_config.format` invalida o cache de prompt; o parâmetro beta `output_format` está obsoleto (sem o header beta `structured-outputs-2025-11-13` ele retorna 400, e o SDK Python 1.0 ou superior o rejeita com `TypeError`; Verificado na página de saídas estruturadas em 2026-10-10). Campo `justificativa` curto: pedir raciocínio passo a passo pode causar recusa `reasoning_extraction`.

## 2. Loop de tool use

Errado (sem limite, sem tratamento de erro, ignora `tool_use_id`):

```python
while True:
    resp = client.messages.create(model=MODELO, max_tokens=2048, tools=TOOLS, messages=messages)
    for b in resp.content:
        if b.type == "tool_use":
            messages.append({"role": "user", "content": str(EXEC[b.name](**b.input))})
```

Certo:

```python
messages = [{"role": "user", "content": pedido}]
for _ in range(MAX_ITERACOES):                       # limite explícito
    resp = client.messages.create(
        model=MODELO, max_tokens=2048, tools=TOOLS, messages=messages,
    )
    if resp.stop_reason != "tool_use":
        break
    messages.append({"role": "assistant", "content": resp.content})
    resultados = []
    for bloco in resp.content:
        if bloco.type != "tool_use":
            continue
        try:
            saida = EXECUTORES[bloco.name](**bloco.input)
            resultados.append({"type": "tool_result", "tool_use_id": bloco.id, "content": str(saida)})
        except Exception as exc:                      # o modelo pode se corrigir com a mensagem
            resultados.append({"type": "tool_result", "tool_use_id": bloco.id,
                               "content": f"Erro: {exc}", "is_error": True})
    messages.append({"role": "user", "content": resultados})
else:
    raise RuntimeError("limite de iterações atingido")
```

Checklist (V-37, V-13, V-18):

- [ ] Todo `tool_use` do turno recebe um `tool_result` com o mesmo `tool_use_id`, no mesmo turno do usuário.
- [ ] Limite de iterações e, no Agent SDK, `max_turns`.
- [ ] Ação obrigatória: `tool_choice` (`auto`, `any`, `tool`, `none`); a instrução no prompt só aumenta a tendência. `any`/`tool` retornam 400 em Opus 5.5, Sonnet 5.5, Fable 5.1 e Mythos 5.1 e com thinking manual; nesses, `auto` + `strict: true` e checagem no código de que a tool veio. Onde forçar é aceito, o thinking é pulado (Verificado em 2026-10-10).
- [ ] Tool de escrita: `disable_parallel_tool_use` e confirmação humana antes de executar, aplicada no código (não só na descrição).
- [ ] `strict: true` quando a conformidade ao schema importa; parâmetro obrigatório faltante não deve ser inferido pelo modelo: valide no código.
- [ ] Conteúdo vindo de `tool_result` é dado (ver `agent-security-review`); instruções próprias não entram no resultado.
- [ ] Sobrecarga de tokens do prompt de sistema de tools: entre 286 e 675 tokens conforme o modelo (V-37).

## 3. Streaming com tool use

Eventos (V-37): `message_start`, `content_block_start`, `content_block_delta` (deltas `text_delta`, `input_json_delta`, `thinking_delta`, `signature_delta`), `content_block_stop`, `message_delta`, `message_stop`, além de `ping` e `error` (`overloaded_error` equivale ao HTTP 529).

Errado (parseia JSON parcial a cada delta e executa):

```python
for ev in stream:
    if ev.type == "content_block_delta" and ev.delta.type == "input_json_delta":
        executar(json.loads(ev.delta.partial_json))        # JSON incompleto
```

Certo (se montar à mão; o SDK também oferece helper de stream que acumula a mensagem):

```python
blocos = {}
for ev in client.messages.create(model=MODELO, max_tokens=2048, tools=TOOLS,
                                 messages=messages, stream=True):
    if ev.type == "content_block_start":
        blocos[ev.index] = {"bloco": ev.content_block, "json": ""}
    elif ev.type == "content_block_delta" and ev.delta.type == "input_json_delta":
        blocos[ev.index]["json"] += ev.delta.partial_json
    elif ev.type == "content_block_stop":
        b = blocos.get(ev.index)
        if b and b["bloco"].type == "tool_use":
            entrada = json.loads(b["json"] or "{}")          # só aqui o JSON está completo
            enfileirar(b["bloco"].id, b["bloco"].name, entrada)
    elif ev.type == "error":
        tratar_erro_recuperavel(ev)                          # repetir com backoff
    # "ping": ignorar
# Executar as tools de escrita só depois de message_stop (Inferido: evita ação sobre mensagem incompleta)
```

## 4. Citações

Errado: documento sem `citations`, resposta exibida como fato, ponteiro de citação ignorado.

Certo (V-35):

```python
messages = [{
    "role": "user",
    "content": [
        {"type": "document",
         "source": {"type": "text", "media_type": "text/plain", "data": MANUAL_TEXTO},
         "title": "Manual do cliente", "citations": {"enabled": True}},
        {"type": "text", "text": "Qual o prazo de troca?"},
    ],
}]
```

- Resultado de busca próprio: blocos `search_result` com `source` e `title` obrigatórios e `content` (lista de blocos de texto); citações voltam como `search_result_location`.
- Tipos de localização: `char_location`, `page_location`, `content_block_location`, `search_result_location`; a interface precisa tratar os quatro.
- Regra de validação: afirmação factual sem bloco de citação é registrada como "não sustentada pelas fontes".
- `cited_text` não conta como token de saída; os blocos de citação gerados não são cacheáveis, mas o documento aceita `cache_control`.
- Ponteiro válido não prova fidelidade da afirmação: avalie com juiz calibrado (ver `eval-design`).

## 5. Prompt caching

Errado (prefixo muda a cada chamada):

```python
system = f"Hoje é {datetime.now().isoformat()}. Você é o assistente da loja. {INSTRUCOES_LONGAS}"
```

Certo (estático primeiro; dado variável depois do corte):

```python
system = [{"type": "text", "text": INSTRUCOES_LONGAS, "cache_control": {"type": "ephemeral"}}]
messages = [{"role": "user", "content": f"(data: {hoje}) {pergunta}"}]
```

Checklist (V-24):

- [ ] Ordem do prefixo: tools, system, messages; conteúdo estático primeiro.
- [ ] Sem timestamp, ID de requisição nem dado por usuário antes do ponto de corte.
- [ ] Ponto de corte no último bloco idêntico; no máximo 4 pontos explícitos (o quinto retorna erro 400).
- [ ] Nomes, descrições e ordem de tools estáveis (mudar invalida tudo adiante).
- [ ] Entradas de 1 hora antes das de 5 minutos (TTL de 1 hora: `"ttl": "1h"` em `cache_control`; confirmar sintaxe na página).
- [ ] Mínimo cacheável do modelo respeitado (512 tokens na família 5, 1.024, 2.048 ou 4.096 em outros; tabela em `llm-decision-gates`).
- [ ] Log dos dois campos de uso: `resp.usage.cache_creation_input_tokens` e `resp.usage.cache_read_input_tokens`. Ambos zero: abaixo do mínimo ou prefixo mudou.
- [ ] Mudar `output_config.format` invalida o cache.

## 6. Contagem de tokens e Batch (V-38)

- Contagem de tokens: gratuita, estimativa, não usa cache; limites por faixa (Start 5.000, Build 10.000, Scale 20.000 requisições por minuto); não aceita server tools (exceto advisor), conector MCP nem blocos de imagem/documento por URL ou arquivo.
- Batch: até 100.000 requisições ou 256 MB; expira em 24 horas; resultados por 29 dias; `stream: true` não se aplica; guardar `custom_id`; repetir o lote inteiro quando o prompt mudar.

## 7. Robustez geral do cliente

- [ ] Timeout e repetição com backoff para `overloaded_error`/HTTP 529 e erros de rede; sem repetir cegamente ações de escrita (idempotência).
- [ ] Chave de API só por variável de ambiente ou cofre; nunca no repositório nem no cliente (navegador/app).
- [ ] Log sem segredos; conteúdo de prompt apenas com consentimento (ver telemetria).
- [ ] Teste de contrato com resposta simulada (stub) para `refusal`, `max_tokens`, `tool_use` e `error`.
