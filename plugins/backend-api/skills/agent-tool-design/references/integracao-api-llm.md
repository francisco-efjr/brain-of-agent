# Backend que chama a API de um modelo Claude: checklist e exemplo

Fonte do checklist: skill `claude-api` de anthropics/skills (V-07, Verificado em 2026-10-10; licença: "ver LICENSE.txt" não lida para esta skill, então o conteúdo foi **destilado** com redação própria, sem cópia). Doc de tools: V-02, V-03. O exemplo de código usa o SDK Python `anthropic`; **confirme assinaturas, nomes e campos na documentação oficial e na versão instalada** (https://platform.claude.com/docs e o repositório do SDK da sua linguagem). Os campos usados abaixo (`messages.create`, `stop_reason`, blocos `tool_use`/`tool_result`, `usage.cache_read_input_tokens`) constam na leitura de V-07; demais detalhes são conhecimento estável do SDK (Inferido).

Se o projeto usa outro provedor, **não adicione chamadas Anthropic**: pare e pergunte (V-07).

## Sumário

1. Checklist de endpoint que chama o modelo
2. Exemplo de laço com tools
3. Streaming
4. Prompt caching
5. Falhas e limites
6. Segurança

## 1. Checklist

- [ ] SDK oficial da linguagem; nenhuma assinatura inventada (leia a doc/typings do SDK instalado).
- [ ] ID do modelo vem de **configuração**, consultado na tabela oficial atual; não fixe um ID no código nem no prompt. Sem sufixo de data quando a doc recomenda o alias (V-07: "IDs sem sufixo de data").
- [ ] `max_tokens` definido conscientemente; trate `stop_reason == "max_tokens"` (resposta cortada) antes de usar o conteúdo.
- [ ] Verifique `stop_reason` **antes** de executar tools: `tool_use` executa, `end_turn` termina, `max_tokens` e `refusal` exigem tratamento próprio (V-07). Demais valores: confira na doc.
- [ ] Devolva **todos** os `tool_result` de uma rodada numa **única** mensagem de usuário (V-07), cada um com o `tool_use_id` correspondente.
- [ ] Valide cada entrada de tool contra o schema **antes** de executar (V-07); autorize no servidor por objeto/tenant (o modelo repassa o que o texto sugere).
- [ ] Streaming para saídas longas (V-07), para evitar timeout de conexão e melhorar latência percebida.
- [ ] Prompt caching por prefixo: conteúdo estável no início; confira `usage.cache_read_input_tokens` para saber se acertou (V-07).
- [ ] Timeouts e retries do cliente HTTP/SDK conscientes; 429 e erros 5xx com backoff; nunca repetir sem idempotência quando a tool tem efeito.
- [ ] Limite de iterações do laço de tools e orçamento de tokens por requisição (evita laço infinito e custo descontrolado).
- [ ] Saída do modelo é **dado não confiável**: nunca vira SQL, caminho, shell ou HTML sem validação/escape.
- [ ] Chave de API em variável de ambiente/cofre, no servidor; nunca no cliente, no repositório ou em log.
- [ ] Dados pessoais/sensíveis mínimos no prompt; logs sem conteúdo integral por padrão.

## 2. Exemplo de laço com tools

Esqueleto em Python, com validação e limite de iterações. `MODELO` vem de configuração; `executar_tool` valida o schema e autoriza no servidor.

```python
import os
import anthropic

client = anthropic.Anthropic()                # lê ANTHROPIC_API_KEY do ambiente
MODELO = os.environ["LLM_MODEL"]              # ID consultado na tabela oficial atual
MAX_RODADAS = 6

def responder(pergunta: str, tools: list[dict], usuario) -> str:
    mensagens = [{"role": "user", "content": pergunta}]
    for _ in range(MAX_RODADAS):
        resp = client.messages.create(
            model=MODELO, max_tokens=1024, tools=tools, messages=mensagens,
        )
        if resp.stop_reason == "tool_use":
            mensagens.append({"role": "assistant", "content": resp.content})
            resultados = []
            for bloco in resp.content:
                if bloco.type == "tool_use":
                    try:
                        saida = executar_tool(bloco.name, bloco.input, usuario)  # valida + autoriza
                        resultados.append({"type": "tool_result", "tool_use_id": bloco.id,
                                           "content": saida})
                    except ErroDeTool as erro:               # erro acionável para o modelo
                        resultados.append({"type": "tool_result", "tool_use_id": bloco.id,
                                           "content": str(erro), "is_error": True})
            mensagens.append({"role": "user", "content": resultados})   # todos numa só mensagem
            continue
        if resp.stop_reason == "end_turn":
            return "".join(b.text for b in resp.content if b.type == "text")
        raise RuntimeError(f"parada inesperada: {resp.stop_reason}")      # max_tokens, refusal etc.
    raise RuntimeError("limite de rodadas atingido")
```

Notas: `ErroDeTool` carrega mensagem que diz o que corrigir (passo 6 da skill). O retorno de `max_tokens` e `refusal` merece tratamento de produto (mensagem ao usuário, nova tentativa limitada), não só exceção. Se a tool muta estado, exija chave de idempotência derivada de `bloco.id` + usuário.

## 3. Streaming

Para saídas longas use a API de streaming do SDK (Python: `client.messages.stream(...)` como gerenciador de contexto, iterando o fluxo de texto e obtendo a mensagem final ao término; confirme os nomes na versão instalada). Em HTTP para o seu cliente, repasse por SSE/chunked e trate desconexão do cliente cancelando a chamada ao modelo. Valide o conteúdo final antes de agir sobre ele; o texto parcial do stream não é confiável como entrada de decisão.

## 4. Prompt caching

O cache é por **prefixo**: system prompt, definições de tools e documentos estáveis vêm primeiro; o que varia por requisição vem depois. Marque pontos de cache conforme a doc (campo `cache_control` nos blocos; confirme sintaxe e TTL atuais). Prove o efeito lendo `usage.cache_read_input_tokens` (e a contagem de criação de cache) nas respostas; sem leitura > 0, o cache não está acertando (prefixo muda a cada chamada: ID, data, ordem de tools instável).

## 5. Falhas e limites

| Situação | Tratamento |
| --- | --- |
| 429 / limite de taxa | backoff com jitter, respeitar `Retry-After`; fila/orçamento no seu serviço |
| 5xx / sobrecarga | retry limitado; resposta degradada ao usuário |
| `stop_reason == "max_tokens"` | não use o conteúdo cortado como completo; aumente o limite ou continue de forma explícita |
| `stop_reason == "refusal"` | trate como resultado legítimo; não reenvie em laço |
| tool com 400 por `input_examples` inválidos | corrija o exemplo para validar contra o schema (V-02) |
| 400 por `tool_choice` | `any`/`tool` retornam 400 em alguns modelos e com extended thinking manual (V-02, reconferido em 2026-10-10); use `auto` com strict ou structured outputs; tabela muda |
| timeout do seu cliente | stream; não repita sem idempotência quando houve tool com efeito |

## 6. Segurança

- Injeção por conteúdo: documentos, páginas, e-mails e resultados de tool entram no contexto como **dado**; instruções dentro deles não ganham autoridade. Não conceda ao modelo permissões maiores que as do usuário que fez o pedido.
- Autorização por objeto na tool, no servidor, com a identidade do usuário (não a do serviço, a menos que seja desenho explícito).
- Ações irreversíveis ou externas (pagamento, envio, escrita em produção) exigem confirmação do usuário na interface, não só uma frase no prompt.
- Revisão deste desenho: `api-security-review` (OWASP API API10 e API6) e `llm-ai-agents` para a arquitetura do agente.
