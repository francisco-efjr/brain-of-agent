# Backend, contratos e integrações

## Contrato antes da integração

Inventariar consumidores, métodos, schemas, códigos de resposta, autenticação, autorização, limites, paginação, ordenação e políticas de compatibilidade. Um exemplo JSON não é contrato completo. Definir ausência versus null, limites numéricos, representação monetária, timezone, precisão e campos desconhecidos.

OpenAPI documenta interfaces HTTP e pode alimentar verificações; usar a versão compatível com ferramentas do projeto em vez de atualizar apenas por ser a mais recente. Schema válido não garante regra de negócio. [Fonte: OpenAPI Specification](https://spec.openapis.org/oas/latest.html).

## Semântica e erros

Métodos HTTP têm propriedades distintas; idempotência de método não significa resposta idêntica, nem substitui chave de operação de negócio. Evitar ação destrutiva em GET. [Fonte: HTTP request methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods).

Se adequado ao sistema, RFC 9457 oferece formato de erro estruturado com identificador de tipo e campos para contexto. Preservar significado do status HTTP e impedir vazamento de stack trace, SQL ou segredo em detalhes. [Fonte: RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html).

## Idempotência verificável

Cenário: cliente recebe timeout após pagamento aceito e tenta de novo. Antes: cada POST cobra novamente. Depois: persistir chave com escopo de usuário/tenant/operação, fingerprint dos parâmetros relevantes e resultado; reutilização com payload diferente recebe conflito definido. Garantia precisa ser atômica e cobrir corrida: cache ou consulta seguida de inserção sem unicidade permite duas cobranças.

Definir expiração e comportamento após janela. Uma chave global previsível pode permitir colisão ou descoberta entre tenants. Retry automático só é seguro depois de compreender semântica, limites e aceitação desconhecida.

## Dependências externas

Distribuir orçamento de timeout por salto; não permitir que cada chamada consuma o prazo inteiro do usuário. Limitar tentativas, aplicar backoff/jitter quando justificável, evitar retry de erros permanentes e respeitar orientação do fornecedor. Circuit breaker não resolve inconsistência; apenas limita tentativas durante falha.

Processar webhooks com assinatura, janela/replay conforme contrato e deduplicação persistente. Considerar ordem invertida de eventos e estados terminais. Emitir resposta conforme compromisso assumido: aceitar enfileiramento não é concluir processamento.

## Evolução e paginação

Avaliar compatibilidade semântica: tornar um campo obrigatório, alterar enum, remover valor, mudar ordenação ou significado pode quebrar cliente mesmo com JSON válido. Para lista mutável, definir cursor estável e desempate; offset pode duplicar/pular registros sob inserção concorrente. Documentar consistência esperada.

## Checklist

- [ ] Consumidores e contratos existentes identificados.
- [ ] Schemas cobrem erro, sucesso, vazio e limites; serializers reais verificados.
- [ ] Autorização por objeto, tenant e ação ocorre no servidor.
- [ ] Chave idempotente tem escopo, fingerprint, atomicidade e política de expiração.
- [ ] Timeouts e retries possuem limite e classificação de erro.
- [ ] Webhook/fila suporta duplicação, ordem e falha de processamento.
- [ ] Mudança compatível ou migração de consumidores planejada.
- [ ] Integração real em ambiente permitido difere de mock explicitamente.
- [ ] Evidência mostra regra correta, e não apenas HTTP 200.

Revalidar: enviar payload antigo/novo, chamada duplicada concorrente, perda de resposta após aceitação, tenant errado, limite de paginação, fornecedor lento e evento repetido. Não executar carga ou mutações contra sistemas externos sem escopo autorizado.

Fontes consultadas em 2026-10-09. Header de idempotência e códigos de conflito do exemplo são escolhas de contrato, não padrão universal obrigatório.
