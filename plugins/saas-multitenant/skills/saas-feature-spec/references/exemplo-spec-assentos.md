# Exemplo: spec de convites com limite por plano e downgrade

Exemplo ilustrativo (caso de eval `spec-downgrade-assentos`). Os limites (Free 3, Pro 10, Business 50) vêm do pedido do usuário no caso, não de medição. Mostra a forma, o nível de detalhe e o gate; troque tudo pelo seu contexto. Conferido em 2026-10-10.

---

# Spec 0007: convites com limite de assentos por plano

Status: **bloqueada** (G4 aberto, ver Gate) · Autor: [nome] · Data: AAAA-MM-DD

## Problema e pagante

Administradores de tenants precisam convidar colegas, e a cobrança é por plano com teto de assentos. Quem paga: o tenant, pelo plano (Free 3 assentos, Pro 10, Business 50). Hoje não há limite aplicado nem tratamento de downgrade (Suposição: confirmar no código).

## Tenant e papéis

Dados de tenant: membros, convites, assentos usados. Papéis: `owner` e `admin` convidam e removem; `billing` altera plano; `member` e `viewer` não convidam. Dado global: catálogo de planos.

## Requisitos

- **REQ-01 Isolamento.** Convites e membros pertencem a um tenant; toda leitura e escrita é escopada pelo tenant do contexto. Convite de outro tenant, consultado pelo ID ou pelo token, responde 404 igual a "não existe". Verificação: teste de integração com dois tenants (V-23, V-32).
- **REQ-02 Autorização.** Apenas `owner` e `admin` criam, reenviam e revogam convites; o papel do convidado vem da regra do plano e do convite, nunca do corpo do aceite. Verificação: matriz papel × ação pela API (V-12 AZ4/AZ5).
- **REQ-03 Billing.** O número de assentos faturados é a quantidade de assentos ocupados; a atualização no provedor usa chave de idempotência derivada de `tenant + operação + versão` e é reconciliada por job diário. A mudança de plano chega por webhook e reconcilia o estado, nunca pela resposta da chamada (V-02, V-04, V-37).
- **REQ-04 Limites e downgrade.**
  - Assento ocupado = membro `active` + convite pendente não expirado [NEEDS CLARIFICATION: convite pendente conta como assento? Suposição: sim, para evitar corrida].
  - O limite vale sob concorrência: dois convites simultâneos com 4 de 5 ocupados resultam em um aceito e um recusado.
  - Convite além do limite responde `409 seat_limit_reached` com oferta de upgrade ao `owner` e ao `billing`.
  - Downgrade com uso acima do novo limite: o sistema bloqueia a troca e lista o excesso, ou aceita e exige que o admin desative membros até o novo limite em [N] dias [NEEDS CLARIFICATION: decisão de produto]. Em nenhum caso apaga dados; membros desativados mantêm papel e conteúdo (V-31, V-38).
- **REQ-05 Auditoria.** Eventos `invite.created`, `invite.revoked`, `invite.accepted`, `member.deactivated`, `plan.changed` com `tenant_id`, `actor_id`, recurso, resultado, instante UTC e origem; sem e-mail do convidado em texto no log (V-41).
- **REQ-06 Dados do titular.** O e-mail do convidado é dado pessoal: convite expirado ou revogado tem o e-mail removido ou anonimizado após [prazo] [Suposição: definir com o jurídico]; exportação do tenant inclui convites pendentes (V-29).
- **REQ-07 Métricas.** "Assento ocupado" e "expansão por assentos" entram no dicionário; MRR segue a definição da Stripe (V-40).
- **REQ-08.** Não aplicável (sem serviço tributável novo).

## Fora de escopo

SSO e provisionamento por SCIM (outra spec; contam como assento da mesma forma). Convites em lote por CSV. Preço por uso. Cada item adiado tem motivo: reduzir o risco desta entrega.

## Critérios de aceite

1. **Dado** os tenants A (Acme Ltda, Pro, 9 de 10 assentos) e B (Acme Ltd, Free, 3 de 3), **quando** o `admin` de A convida `x@acme-ltda.test`, **então** o convite é criado, A fica com 10 de 10, o evento `invite.created` é gravado no tenant A e B não muda. Controle positivo: B continua listando os 3 membros.
2. **Dado** A com 10 de 10, **quando** o `admin` de A convida outra pessoa, **então** a resposta é `409 seat_limit_reached` e nenhum convite novo existe.
3. **Dado** A com 9 de 10 e duas requisições simultâneas de convite, **então** exatamente uma é aceita e a contagem final é 10.
4. **Dado** o `member` de A, **quando** chama `POST /invites` ou envia `role: "owner"` no corpo do aceite, **então** a ação é negada ou o campo ignorado.
5. **Dado** o `admin` de A, **quando** pede `GET /invites/{id do convite de B}`, **então** recebe 404 idêntico ao de ID inexistente.
6. **Dado** A no plano Pro com 8 membros, **quando** pede downgrade para Free (3 assentos), **então** [regra decidida]: o sistema [bloqueia e lista 5 excedentes | aceita e mantém todos ativos até o fim do prazo], e nenhum dado é apagado em nenhum caminho.
7. **Dado** o webhook de mudança de plano entregue duas vezes e fora de ordem, **então** o limite final é o do plano atual e há um único efeito.
8. **Dado** um convite expirado, **quando** alguém usa o link, **então** o aceite é recusado e o assento é liberado.
9. **Passo final de verificação de ponta a ponta:** com dois tenants sintéticos, percorrer convite, aceite, limite, downgrade e reversão, e colar a saída da suíte e a consulta de contagem de assentos.

## Critérios de sucesso

- SC-01: 0 leituras de dado de B por usuários de A nos testes de isolamento.
- SC-02: o limite nunca é excedido em 100 pares de requisições simultâneas no limite (teste de concorrência).
- SC-03: nenhuma linha de dado é removida por downgrade (contagem antes e depois).

## Gate

| Item | Resultado |
| --- | --- |
| G1 isolamento com teste negativo de dois tenants | sim (aceites 1, 5) |
| G2 idempotência e fora de ordem | sim (REQ-03, aceite 7) |
| G3 reversão sem destruir dados | sim (REQ-04, aceite 6) |
| G4 sem `[NEEDS CLARIFICATION]` em isolamento, billing, dado do titular, exclusão | **não**: convite pendente conta? regra de downgrade? prazo do e-mail do convite |
| G5 verificação e dono por requisito | sim, exceto Suposições abaixo sem dono |

Resultado: bloqueada até as três perguntas de G4 terem decisão.

## Suposições

| Suposição | Dono | Data |
| --- | --- | --- |
| Convite pendente conta como assento | [produto] | [data] |
| Prazo de retenção do e-mail do convite | [jurídico] | [data] |
| Hoje não existe limite aplicado no código | [engenharia] | [data] |

## Perguntas abertas

1. Convite pendente conta como assento? 2. Downgrade bloqueia ou desativa excedentes? 3. Qual o prazo de retenção do e-mail de convite expirado?

Rótulos: requisitos de isolamento e billing seguem V-nn citados (Verificado nas fontes); a política de convite pendente, o código `409` e os prazos são decisões de produto (Suposição).
