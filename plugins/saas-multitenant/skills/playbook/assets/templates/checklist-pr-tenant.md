# Checklist de PR: dados de tenant

Cole no template de PR. Base: `V-11`, `V-12`, `V-21`, `V-34`, `V-49`. Marque com evidência (linha ou saída de comando); item que não se aplica leva "n/a" e o motivo.

- [ ] O `tenant_id` vem do token ou da sessão validados, nunca do corpo, da URL ou de header livre. Evidência: `arquivo:linha`.
- [ ] Toda leitura e escrita confere o tenant **na consulta** (`WHERE id = $1 AND tenant_id = $2`) e passa pelo repositório ou helper de contexto.
- [ ] Rota nova tem policy de autorização explícita (deny by default); nenhum `role`, `tenant_id` ou `isAdmin` aceito do corpo (lista explícita de campos).
- [ ] Objeto de outro tenant responde 404; 403 só para papel insuficiente no próprio tenant.
- [ ] Tabela nova com `tenant_id`: `ENABLE` + `FORCE` RLS, policy com `USING` e `WITH CHECK`, `UNIQUE (tenant_id, ...)`, FK composta, índice começando por `tenant_id`.
- [ ] Contexto por `set_config(..., true)` em transação (leituras incluídas); nenhum `SET` de sessão.
- [ ] Job, worker e fila: a mensagem carrega `tenant_id`; uma transação por tenant; sem contexto global.
- [ ] Cache: tenant na chave; URL assinada só após autorizar objeto e operação.
- [ ] Busca, exportação, anexos, notificações e websockets filtram por tenant.
- [ ] Webhook de billing (se tocado): corpo bruto, assinatura, `event.id` UNIQUE, worker relê o objeto, acesso por webhook.
- [ ] Chamada de saída com efeito usa chave de idempotência da operação.
- [ ] Logs e auditoria com `tenant_id` e `actor_id`; sem PII, token ou corpo de requisição.
- [ ] Teste de dois tenants (nomes parecidos) incluído e **executado com a role da aplicação**; saída colada na descrição do PR.
- [ ] Nenhum dado real de cliente em fixture, seed ou prompt; nenhum segredo no diff.
