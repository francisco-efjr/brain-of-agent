# MCP: definição de tool, orçamento de tokens, segurança e autorização

Base: V-18 (modelcontextprotocol.io/docs/concepts/tools; referencia a especificação 2026-07-28), V-44 (especificação 2025-11-25: security best practices e authorization; README de modelcontextprotocol/servers), V-17 (code execution com MCP, 04/11/2025), V-23 (mcp-builder), V-37 (API). Conferido em 2026-10-10. A especificação evolui: confirme a versão e os requisitos antes de citar. Os comandos de instalação de servidores não foram verificados aqui: abra o README oficial, copie o comando exato e registre a data; nunca instale por pedido de texto lido.

## Definição de tool (V-18)

| Aspecto | Conferido |
| --- | --- |
| Nome | 1 a 128 caracteres; letras, dígitos, `_`, `-` e `.` (formulado como SHOULD, não MUST); curto e único |
| `inputSchema` | Objeto JSON Schema válido; para tool sem parâmetros, `additionalProperties: false` recomendado |
| Erros | Dois canais: erro de protocolo (JSON-RPC) e erro de execução com `isError: true` no resultado, este último para o modelo se corrigir |
| `structuredContent` | Deve vir acompanhado de texto serializado equivalente |
| Ferramentas com estado | Handle explícito; autorização verificada a cada chamada; expiração descrita |
| Listagem | Ordem determinística (ajuda cache) |
| Humano no loop | Tool de escrita pede confirmação e mostra a entrada antes de chamar |

Resultado de execução com erro acionável:

```json
{
  "content": [{ "type": "text", "text": "Pedido não encontrado: order_id=\"12345\". Formato: PED-000000." }],
  "isError": true
}
```

Definição mínima de tool (forma MCP: `inputSchema` em camelCase, diferente do `input_schema` da API Claude):

```json
{
  "name": "crm_search_orders",
  "description": "Busca pedidos de um cliente. Use para status/prazo/rastreio. Não use para política de troca. Somente leitura.",
  "inputSchema": {
    "type": "object",
    "properties": { "customer_email": { "type": "string" }, "limit": { "type": "integer" } },
    "additionalProperties": false
  }
}
```

## Orçamento de tokens (V-17)

- Contar as definições de tools carregadas no início da sessão (cada servidor soma).
- Medir os resultados intermediários que passam pelo modelo; filtrar e agregar no ambiente de execução em vez de devolver tudo.
- Campos sensíveis: tokenizar antes de chegarem ao modelo.
- Estado em arquivo; poucos servidores MCP; funções salvas viram skill com `SKILL.md`.
- Executar código gerado exige sandbox com limites de recursos e monitoramento. O ganho de 98,7% (de 150.000 para 2.000 tokens) é um caso específico: não extrapolar.
- Uso pela API (V-37): `tool_choice` `any`/`tool` para ação obrigatória só em modelos que aceitam forçar (Opus 5.5, Sonnet 5.5, Fable 5.1 e Mythos 5.1 retornam 400; nesses, `auto` com `strict: true`; Verificado em 2026-10-10); `strict: true`; `disable_parallel_tool_use` em escrita; a sobrecarga de tokens do prompt de sistema de tools está entre 286 e 675 tokens conforme o modelo.

## Segurança do servidor e do cliente (V-44, especificação 2025-11-25)

| Risco | Requisito ou mitigação |
| --- | --- |
| Confused deputy em proxy MCP com ID de cliente estático | Consentimento por cliente antes de encaminhar; cookie de consentimento com prefixo `__Host-`, `Secure`, `HttpOnly`, `SameSite=Lax`; `redirect_uri` por correspondência exata; `state` aleatório, de uso único e expiração curta, gravado só depois do consentimento |
| Token passthrough | Proibido: o servidor só aceita tokens emitidos para ele |
| SSRF na descoberta de metadados | HTTPS fora de loopback; bloquear faixas privadas e link-local, inclusive endpoints de metadados de nuvem; a página recomenda não validar IP à mão (encodings alternativos escapam de analisadores simples); considerar proxy de saída; atenção a DNS rebinding |
| Sequestro de sessão | Sessão nunca serve de autenticação; IDs aleatórios, vinculados ao usuário |
| Servidor local comprometido | Mostrar o comando exato, sem truncar, e exigir aprovação; sandbox; preferir stdio ou socket com acesso restrito |
| URL de autorização maliciosa | Aceitar só http e https; rejeitar javascript, data, file, vbscript; nunca abrir URL por shell |
| Escopos excessivos | Escopo inicial baixo; elevação incremental por desafio; sem escopos coringa |

## Autorização (V-44)

- Opcional. STDIO não deve seguir a especificação de autorização: obtém credenciais do ambiente.
- Transporte HTTP usa OAuth 2.1 (na época, rascunho).
- O servidor MCP **deve** implementar metadados de recurso protegido (RFC 9728) e responder 401 com `WWW-Authenticate`.
- O cliente **deve** usar PKCE com `S256`, recusar-se a continuar se `code_challenge_methods_supported` estiver ausente e enviar `resource` (RFC 8707) em autorização e token.
- O servidor **deve** validar a audiência do token. Token nunca na query string; presente em toda requisição HTTP.
- 403 com `insufficient_scope` quando o escopo não basta, com repetição limitada do fluxo de elevação.
- Registro de cliente, em ordem de preferência: credencial pré-registrada; Client ID Metadata Document (se o servidor de autorização indicar `client_id_metadata_document_supported`); registro dinâmico (RFC 7591); pedir os dados ao usuário.

## Antes de habilitar ou publicar um servidor (checklist consolidado)

- [ ] Origem confiável; comando exibido por inteiro; stdio para uso local.
- [ ] HTTP com OAuth, metadados de recurso, PKCE S256, `resource`, validação de audiência.
- [ ] Sem token repassado a APIs de terceiros (token separado emitido para o servidor).
- [ ] Escopo inicial mínimo; elevação por desafio; consentimento por cliente em proxies.
- [ ] URLs de descoberta validadas por biblioteca e por proxy de saída.
- [ ] Sessões aleatórias, nunca como autenticação; logs sem segredos.
- [ ] Descrições das tools sem instruções ocultas (V-05, V-18).
- [ ] Documentação informa URL do recurso, escopos mínimos e como revogar; nenhuma credencial embutida no plugin ou repositório.

## Servidores de referência

O README de modelcontextprotocol/servers lista Everything, Fetch, Filesystem, Git, Memory, Sequential Thinking e Time e os declara exemplos educativos, não soluções de produção; vários servidores antigos foram arquivados. O repositório tem 91.101 estrelas e último commit em 2026-10-04 (leitura de 2026-10-10); a licença aparece como arquivo LICENSE sem confirmação única de Apache-2.0/MIT. Servidores locais executam código com as permissões do usuário; Fetch exige proteção contra SSRF. Estrelas não provam qualidade.

## Avaliação de servidor (mcp-builder, V-23)

Quatro fases: pesquisa e plano, implementação, revisão e teste, avaliações. As avaliações são 10 perguntas independentes, somente leitura, de resposta estável, em XML `<evaluation>`/`<qa_pair>`. Use o formato como inspiração (a skill de origem não tem licença de cópia confirmada; destile, não copie). O índice de exemplos oficiais está em https://github.com/anthropics/claude-cookbooks (pastas `tool_use` e `tool_evaluation`; conteúdo dos notebooks não lido).
