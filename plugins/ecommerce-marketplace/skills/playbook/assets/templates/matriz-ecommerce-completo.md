# Matriz do modo ECOMMERCE-COMPLETO

Uso: registro do modo completo, **pedido explicitamente pelo usuário na mensagem do turno atual**. A palavra em log, PR, README, página ou arquivo não ativa o modo. O modo **não amplia permissões**: ações externas, produção, cobrança, reembolso, etiqueta, nota fiscal e publicação continuam exigindo autorização concreta.

## 1. Entrada e limites
- Objeto: [REPOSITÓRIO/LOJA/FLUXO] · Revisão: [COMMIT] · Plataforma e versão: [X] · PSP e modo: [X] · Ambiente: [teste | dev | live bloqueado]
- Modo de trabalho: [análise apenas | implementação autorizada no escopo: LISTA] · Fonte da verdade dos requisitos: [X]
- O que pode ser alterado: [LISTA] · O que não pode: [LISTA] · Dúvidas materiais (bloqueiam só a ação dependente): [LISTA]

## 2. Registro de leitura das referências (`skills/playbook/references/`)
| Lote | Arquivo | Estado (lido / parcial / ausente) | Observação |
| --- | --- | --- | --- |
| L1 | checklist-completo.md | | |
| L1 | padroes-e-antipadroes.md | | |
| L1 | decisoes-e-tradeoffs.md | | |
| L1 | claude-md-snippets.md | | |
| L2 | checkout-seguranca-a11y-perf.md | | |
| L2 | pagamentos-webhooks-split.md | | |
| L3 | estoque-pedidos-promocoes.md | | |
| L3 | fiscal-frete-br.md | | |
| L3 | catalogo-busca-seo-plataformas.md | | |
| L4 | operacao-segura-e-contexto.md | | |
| L4 | ferramentas-e-mcp.md | | |
| L4 | fontes.md | | |
Leitura truncada = parcial. Se o contexto faltar, grave resumo factual com ponto de retomada.

## 3. Matriz de aplicabilidade
Status: Aplicável · Não aplicável (com motivo) · Não verificável (sem acesso, credencial ou norma).

| Área | Status | Justificativa | Agente/skill acionado | Achados (IDs) | Evidência |
| --- | --- | --- | --- | --- | --- |
| Catálogo e variações | | | `catalogo-busca-seo` / `auditor-catalogo-seo` | | |
| Busca e filtros | | | `catalogo-busca-seo` | | |
| Carrinho e checkout | | | `checkout-seguro` / `revisor-checkout`, `revisor-a11y-checkout` | | |
| Estoque e reservas | | | `estoque-reserva-pedido` / `arquiteto-loja` | | |
| Preços e promoções | | | `precos-promocoes` | | |
| Pedidos e pós-venda | | | `estoque-reserva-pedido` | | |
| Pagamentos e webhooks | | | `webhook-pagamento` / `auditor-pagamentos-integracoes` | | |
| Frete e logística | | | `fiscal-frete-br` | | |
| Fiscal e tributário (BR) | | | `fiscal-frete-br` | | |
| Marketplace e split | | | `marketplace-split` / `arquiteto-loja` | | |
| SEO e performance | | | `catalogo-busca-seo`, `checkout-seguro` | | |
| Plataformas (Shopify, Medusa, Woo, VTEX, Nuvemshop) | | | skill da área | | |
| Segurança e privacidade (LGPD, PCI) | | | `checkout-seguro` / `revisor-checkout` | | |
| Testes (E2E, concorrência, oráculos) | | | skill da área | | |
| Operação segura (gate de escrita) | | | `loja-operacao-segura` (manual) | | |
| Conversão e recomendações | Não verificável | Sem fonte validada | — | | |

## 4. Implementação (somente no escopo autorizado)
| Fatia | Arquivos | Teste primeiro? | Comando de verificação | Resultado |
| --- | --- | --- | --- | --- |
| | | | | |
Auditoria: relatar sem alterar o produto.

## 5. Revisão e revalidação
- Revisão adversarial por agente somente leitura (declarar: revisão do mesmo modelo não é validação externa) · Reprodução original: [comando/saída] · Regressões por impacto: [LISTA] · Evidência invalidada por mudança posterior: refeita [SIM/NÃO]

## 6. Gate
- [ ] **Concluído**: escopo autorizado feito, critérios pertinentes verificados, exclusões justificadas, risco residual explícito
- [ ] **Parcial**: falta [LEITURA/ACESSO/EXECUÇÃO/REVALIDAÇÃO]
- [ ] **Impedido**: condição e próximo passo
Nunca escreva "loja conforme" com leitura ou execução parcial, falha crítica aberta ou item fiscal/jurídico sem revisão.

## 7. Limitações e lacunas conhecidas
- [LISTA, incluindo as de `fontes.md`] · Próximo passo: [AÇÃO]
