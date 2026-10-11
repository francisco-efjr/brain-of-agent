# Checklist de go-live com o provedor de pagamentos

Sumário: 1. Como preencher · 2. Checklist (template `checklist-go-live.md`) · 3. Verificações locais que o usuário pode rodar · 4. Notas por provedor · 5. Decisão

Origem: V-14 (Paymob: segurança de escrita e go-live), V-15 (piso de 9 do mp-review), V-41 (security.md da Stripe), V-37 e V-50 (webhook sem assinatura), V-62 e V-63 (PCI), V-67 (cadência), V-70 (versão da especificação). Texto e estrutura próprios. Conferido em 2026-10-10; cada provedor muda interface e regras: leia a página vigente. O plugin não executa nenhum passo em produção.

## 1. Como preencher

Para cada item: **Status** (`atendido`, `não atendido`, `Não verificado`, `Não aplicável`) e **Evidência** (caminho `arquivo:linha`, saída de comando colada pelo usuário, captura de configuração, link do ticket com o fornecedor). Sem evidência o status é `Não verificado`. Um item `Não verificado` ou `não atendido` em categoria bloqueante impede a recomendação "pronto". Nunca peça nem registre valores de chave; registre apenas nomes de variáveis e onde ficam.

## 2. Checklist

| # | Item | Bloqueante | Status | Evidência | Fonte |
| --- | --- | --- | --- | --- | --- |
| 1 | Chaves de produção diferentes das de teste; uma por serviço e ambiente; restritas por serviço (Stripe: `rk_` com menor privilégio em vez de `sk_`) | sim | | | V-41 |
| 2 | Nenhuma chave de produção em app móvel ou cliente (chaves efêmeras ou só a chave pública) | sim | | | V-14, V-41 |
| 3 | Chave só em cofre ou variável de ambiente; nunca em código, log, erro ou cliente; `.env` no `.gitignore` e `.env.example` fora dele | sim | | | V-15, V-41 |
| 4 | Endpoint de webhook e segredo de produção próprios (segredo por endpoint e por modo) | sim | | | V-03 |
| 5 | Assinatura de webhook verificada no código e confirmada com o provedor; quando não documentada, confirmação por escrito e tratamento como não autenticado | sim | | | V-37, V-50 |
| 6 | Credenciais de teste e endpoints de sandbox fora do deploy de produção | sim | | | V-15 |
| 7 | HTTPS em `back_url`, `notification_url` e retornos | sim | | | V-15 |
| 8 | Status do pedido confirmado no servidor depois do redirecionamento (nunca pelo redirecionamento) | sim | | | V-14, V-15 |
| 9 | Chave de idempotência em toda mutação financeira; referência externa em todo pedido | sim | | | V-01, V-15 |
| 10 | Conciliação diária ativa, bilateral, por partição, com alerta de divergência; cadência menor que a menor janela de reenvio ou retenção entre os provedores em uso (Inferido) | sim | | | V-08, V-67 |
| 11 | Alertas de fila de webhook pausada e de falhas de entrega (limiar do projeto: Suposição) | não | | | V-51, V-67 |
| 12 | Páginas de pagamento com CSP restritiva e campos hospedados do provedor; triagem de escopo PCI respondida ou "não verificado" (decisão do adquirente ou compliance) | sim | | | V-41, V-62, V-63 |
| 13 | Nenhum PAN, CVV, token, senha ou chave em logs (busca por regex mais Luhn nos logs de teste) | sim | | | V-23 |
| 14 | Limites de gasto e permissões como controle técnico (chave restrita, somente leitura quando possível, sem credencial de produção em subagentes) | sim | | | V-14, V-16 |
| 15 | Rate limiting e limite de tentativas em login, cartão e pagamento | sim | | | V-22 |
| 16 | Versão e data de leitura de cada especificação (Pix, FAPI-BR, API do provedor) registradas e comparadas com a vigente; datas ambíguas (DD/MM ou MM/DD) confirmadas | não | | | V-70 (Inferido) |
| 17 | Números regulatórios do projeto (limites do Pix, MED, prazos de bandeira) vêm de configuração com fonte lida, não de constantes herdadas | não | | | V-33, V-44 |
| 18 | Plano de reversão (feature flag, desligar canal, cancelar cobranças pendentes) e dono nomeado | sim | | | V-14 |
| 19 | Procedimento de rotação de chave e de resposta a vazamento escrito (ver `runbook-incidente-lgpd.md`) | sim | | | V-41, V-30 |
| 20 | Aprovação humana de ida para produção registrada (quem, quando, o quê) | sim | | | V-17 |

## 3. Verificações locais que o usuário pode rodar (somente leitura)

Estes comandos listam **nomes de arquivos**, não valores, para não imprimir segredo no terminal. Rode no repositório do projeto; o Claude não os executa em produção.

```text
git check-ignore -v .env                       # confirma que .env está ignorado
git ls-files | grep -i "\.env"                 # arquivos .env versionados (o esperado é só .env.example)
git grep -l -I -E "(sk|rk)_live_|whsec_|BEGIN (RSA |EC )?PRIVATE KEY"   # só os nomes dos arquivos com padrão de segredo
git log --all -S"whsec_" --oneline | head      # há segredo de webhook no histórico? (mostra commits, não valores)
```

Se algum padrão de segredo aparecer em arquivo versionado ou no histórico, trate a chave como exposta: rotação imediata (runbook) e só depois a investigação. Escaneamento contínuo de segredos e auditoria de dependências no CI são escolha do projeto (Suposição quanto à ferramenta).

## 4. Notas por provedor

- **Stripe:** chaves restritas (`rk_`) por serviço; dois segredos de webhook ativos por até 24 h na rotação; permitir apenas os IPs do provedor é defesa em profundidade e a lista vem da página vigente, não copiada; CSP em todo app que carrega Stripe.js; em Connect o dono da plataforma responde por fraude e disputas das contas Express e Custom (Standard minimiza) (V-41). O plugin não usa as skills `stripe-pay`, `stripe-projects` nem `stripe-directory` e não embute comandos de instalação (V-32, V-41).
- **Mercado Pago:** use o SDK para validar `x-signature` (manifesto não documentado, **Não verificável**); `X-Idempotency-Key` obrigatório em Payments e Refunds (V-57); piso de 9 itens do mp-review aplicado na revisão; não instale o marketplace nem os hooks de terceiros.
- **Pagar.me:** assinatura de webhook, idempotência e eventos do Pix não documentados nas páginas lidas: peça ao fornecedor, por escrito, antes do go-live (V-37, V-38, V-68); TLS 1.2 ou 1.3; faixas de IP lidas da página de Segurança no momento da configuração.
- **Adyen:** assinatura no corpo para webhooks padrão; aceitar a chave anterior por um tempo ao gerar nova (V-47); idempotência com validade de 7 a 14 dias (V-01).
- **Asaas:** token compartilhado em `asaas-access-token`; fila pode pausar após 15 falhas; eventos guardados por 14 dias (V-51).
- **Pix via PSP:** mTLS no webhook; certificado fora do código e do log; rotação de certificado planejada (V-44, V-53).
- **Paymob:** callback HMAC-SHA512; a documentação ao vivo prevalece sobre a skill (V-14); links de onboarding levam parâmetro `partner`, não os use.

## 5. Decisão

Resumo para quem decide: itens bloqueantes atendidos X de Y; pendências com dono e data; riscos aceitos (quem aceitou); recomendação (`pronto`, `pronto com pendências não bloqueantes`, `bloqueado`). A recomendação é do plugin, a decisão é humana e deve ser registrada com data e nome.
