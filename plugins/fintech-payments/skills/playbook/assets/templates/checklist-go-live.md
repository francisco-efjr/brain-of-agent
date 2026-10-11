# Checklist de go-live com provedor de pagamentos

Base: V-14, V-15, V-41, V-62, V-63, V-67, V-70. **O plugin não executa nenhum passo em produção.** Cada item tem evidência (link, saída de comando, captura sem segredo) ou fica **Não verificado**. Quem aprova é uma pessoa; registre nome e data. Provedor: [ ] · Data: [ ] · Responsável: [ ].

## 1. Chaves e segredos

- [ ] Chaves de produção separadas das de teste; **restritas por serviço** (ex.: `rk_` na Stripe) e por ambiente. Evidência: [ ]
- [ ] Nenhuma chave de produção em app móvel ou cliente; só chave pública no cliente. Evidência: [ ]
- [ ] Chaves em cofre ou variável de ambiente; `.env` no `.gitignore`; nenhum segredo no histórico do Git. Evidência: [ ]
- [ ] Procedimento de rotação de chave testado em teste (chave exposta: girar na hora). Evidência: [ ]
- [ ] `permissions.deny` para `.env`/`secrets` no projeto; credenciais fora do contexto de agentes e subagentes. Evidência: [ ]

## 2. Webhooks e retornos

- [ ] Endpoint e segredo de webhook de **produção** próprios (não os de teste). Evidência: [ ]
- [ ] Assinatura confirmada com o provedor (**por escrito** quando não documentada; Pagar.me, Mercado Pago). Evidência: [ ]
- [ ] Verificação sobre corpo bruto, dedupe persistido, fila, releitura (roteiro hostil executado em teste). Evidência: [ ]
- [ ] HTTPS em `back_url`/`return_url` e `notification_url`. Evidência: [ ]
- [ ] Credenciais de teste e endpoints de sandbox **fora** do deploy de produção. Evidência: [ ]
- [ ] Allowlist de IP lida na página vigente do provedor em [data] (não copiada). Evidência: [ ]

## 3. Dinheiro, ledger e conciliação

- [ ] Idempotência em criação, captura, estorno e repasse; constraint no banco; teste que conta linhas. Evidência: [ ]
- [ ] Mínimos/máximos por moeda e meio de pagamento conferidos na tabela vigente em [data]. Evidência: [ ]
- [ ] Conciliação diária ativa nos dois sentidos, com alerta de divergência e de `INCOMPLETE_SOURCE`. Evidência: [ ]
- [ ] Cadência da conciliação menor que a menor janela de reenvio/retenção entre os provedores em uso (V-67). Evidência: [ ]
- [ ] Alerta de fila de webhook pausada (limiar do projeto: [ ]). Evidência: [ ]
- [ ] Plano de reversão (feature flag, desligar o meio de pagamento, estornos por lançamento). Evidência: [ ]

## 4. Segurança e privacidade

- [ ] CSP restritiva nas páginas de pagamento; campos hospedados do provedor; **origem de cada elemento da página listada** (V-62). Evidência: [ ]
- [ ] Triagem de escopo PCI respondida ou marcada "não verificado" (V-63); decisão do adquirente/compliance registrada. Evidência: [ ]
- [ ] Rate limiting e limite de tentativas de cartão em login e pagamento. Evidência: [ ]
- [ ] Logs sem PAN/CVV/token/chave (regex + Luhn nos logs de teste). Evidência: [ ]
- [ ] Limites de gasto e permissões como controle técnico (não só prompt). Evidência: [ ]
- [ ] Encarregado de dados (LGPD) identificado; runbook de incidente (`runbook-incidente-lgpd.md`) conhecido. Evidência: [ ]

## 5. Especificações e regulação

- [ ] Versão e **data de leitura** de cada especificação registradas e comparadas com a vigente (Pix, FAPI-BR, API do provedor) (V-70). Evidência: [ ]
- [ ] Datas ambíguas (DD/MM x MM/DD) confirmadas, não decididas. Evidência: [ ]
- [ ] Números regulatórios usados em código (limites, MED, prazos) com fonte vigente ou configuráveis e rotulados. Evidência: [ ]
- [ ] Itens KYC/AML e PCI aplicáveis tratados por compliance (o plugin não verifica norma). Evidência: [ ]

## 6. Aprovação

| Item | Resultado | Responsável | Data |
| --- | --- | --- | --- |
| Checklist completo, sem item "Não verificado" crítico | [aprovado / pendente] | [ ] | [ ] |
| Aprovação humana de go-live registrada | [ ] | [ ] | [ ] |

Itens "Não verificado" restantes e risco aceito: [ ]
