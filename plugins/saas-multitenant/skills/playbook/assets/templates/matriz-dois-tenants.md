# Matriz de testes de dois tenants

> Base: seção "SaaS multi-tenant B2B" de `brains/qa/references/dominios.md` do brain-of-agent (conteúdo próprio do usuário, MIT), reproduzida com adaptação: colunas de rótulo, teste e status; linhas de V-49 e V-55 acrescentadas; **inciso da LGPD corrigido** (art. 18, II é acesso; V é portabilidade a outro fornecedor, V-27). O cabeçalho do arquivo original pede reconferir normas e números na fonte antes de usar como resultado esperado. "404 em vez de 403" é prática, não norma (V-23, V-11, V-12).

O defeito que encerra contrato é vazamento entre clientes. Todo teste de isolamento precisa de **dois tenants** com dados de nomes parecidos (por exemplo "Acme Ltda" e "Acme Ltd"), usuários por papel em cada um e objetos em cada um. Dados sintéticos; nunca dado real. Testes de banco rodam com a **role da aplicação**.

Rótulo por linha: Verificado (teste executado, saída colada), Inferido, Suposição, Não verificável (com motivo). Status: `a fazer | escrito | executado-ok | executado-falha`.

| ID | Risco | Caso | Esperado | Teste associado | Rótulo | Status |
| --- | --- | --- | --- | --- | --- | --- |
| M-01 | Isolamento por ID | usuário do tenant A chama `GET /api/faturas/{id}` com ID do tenant B | 404 (não 403, que confirma a existência) | | | |
| M-02 | Isolamento indireto | busca, autocomplete, exportação CSV, relatório, anexos por URL, notificações, websockets, cache | nada do tenant B aparece; URL de arquivo é assinada e expira | | | |
| M-03 | Jobs em lote | job noturno processa os dois tenants | cada saída usa só os dados do próprio tenant (contexto do tenant perdido em worker é clássico) | | | |
| M-04 | Papéis | matriz papel × ação (admin, gestor, membro, leitor, cobrança) | cada célula testada pela API, não só pela tela escondendo o botão | | | |
| M-05 | Escalada | membro altera o próprio papel no corpo da requisição | ignorado ou recusado | | | |
| M-06 | Plano e limites | plano com 5 assentos: convidar o 5º e o 6º | 5º aceito; 6º bloqueado com oferta de upgrade | | | |
| M-07 | Downgrade | sair do plano com 10 usuários para o de 5 | regra explícita (bloqueia ou desativa); nunca apaga dados | | | |
| M-08 | Cobrança | upgrade no meio do ciclo, falha de cartão, fim do trial, webhook duplicado do provedor | proporcionalidade correta; tentativas e aviso; acesso conforme a regra; webhook idempotente | | | |
| M-09 | Convites | convite expirado, reutilizado, e-mail com caixa diferente, convidado já é de outro tenant | expirado e reutilizado recusados; mesma pessoa em dois tenants com troca de contexto clara | | | |
| M-10 | SSO | SAML/OIDC: domínio não verificado, provisionamento no primeiro login, usuário removido no IdP | não entra; recebe o papel padrão; perde acesso | | | |
| M-11 | SCIM | desativar usuário via SCIM (`active=false`) | sessões e tokens revogados na hora, não no próximo login; vínculos de grupo preservados; token do tenant A não toca o tenant B (V-55) | | | |
| M-12 | Exportação | exportar todos os dados do tenant | completa, legível por máquina, só do tenant (acesso: LGPD art. 18, II; portabilidade: art. 18, V) | | | |
| M-13 | Migrações | migração de schema em 1.000 tenants, um falha no meio | falha isolada, reexecutável; nenhum tenant em estado misto | | | |
| M-14 | Auditoria | ações de admin | log por tenant, imutável para a role da aplicação, visível ao admin do cliente (visibilidade: Suposição de produto) | | | |
| M-15 | RLS sem contexto | consulta com a role da aplicação sem `set_config` | falha fechada: zero linhas ou erro explícito, conforme a policy, nunca linhas (V-65) | | | |
| M-16 | RLS escrita cruzada | tenant B insere ou atualiza linha com `tenant_id` do A | rejeitado (`WITH CHECK`) (V-58) | | | |
| M-17 | Pool de tamanho 1 | requisição do tenant A, depois do B, depois sem contexto, na mesma conexão | cada uma vê só o seu; a terceira vê nada (V-34) | | | |
| M-18 | Cache | mesmo recurso lido por usuários de tenants (ou permissões) diferentes | chave contém tenant (e permissão); sem resposta cruzada (V-49) | | | |
| M-19 | URL assinada | assinar URL de objeto de outro tenant; reutilizar URL expirada | assinatura só após autorizar objeto e operação; expirada recusada (V-49) | | | |
| M-20 | Restauração de um tenant | restaurar backup do tenant A | em recurso separado; tenants B... ausentes; evento de auditoria registrado (V-49) | | | |
| M-21 | Tentativa cruzada | tenant A tenta N IDs do tenant B | negado, registrado como evento de segurança e alerta por limiar (V-49) | | | |
| M-22 | Suporte do SaaS | sessão de suporte do tenant A tenta ler o B | negado; sessão com motivo, escopo e prazo; evento de auditoria (Inferido) | | | |
| M-23 | Escrita em lote | importação ou otimização em massa com dois tenants | cada linha gravada no tenant correto (Inferido) | | | |
| M-24 | IA com dados de tenant | assistente com tenant fixado na sessão recebe pedido de "todos os clientes" | só dados do próprio tenant; sem saída externa sem confirmação (V-17) | | | |

Armadilhas (brain): testar o retry sem verificar o efeito no banco (conte as linhas, não a resposta); esquecer que o webhook do provedor também chega duplicado e fora de ordem.
