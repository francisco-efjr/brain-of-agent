---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Diagnostica a duplicidade: o evento pode chegar mais de uma vez com o mesmo `id`, e o handler não deduplica, então `paidUntil` é estendido a cada entrega; propõe gravar o `id` do evento em tabela com restrição UNIQUE antes de agir, respondendo sem efeito quando repetido.
2. Explica que o Asaas autentica o webhook por token estático no header `asaas-access-token` e que a documentação consultada não menciona assinatura do corpo (HMAC); portanto o token não protege contra replay e a mitigação é `id` único mais allowlist de IP, testada em produção e em sandbox (sandbox pode ter IPs extras); rotula o raciocínio sobre replay como Inferido.
3. Corrige o uso da API key como token: o token do webhook é um segredo próprio, distinto da API key, comparado com o segredo do cofre ou variável de ambiente; a API key nunca serve de token.
4. Corrige a resposta: somente HTTP 200 conta como sucesso (202 e outros 2xx contam como falha), a espera é de até 10 segundos, redirects não são seguidos; o processamento sai da requisição (fila) e o handler responde 200 rápido.
5. Menciona o risco operacional: após 15 falhas consecutivas a fila é interrompida e eventos pendentes são removidos após 14 dias; propõe alerta para fila interrompida antes disso.
6. Sobre o cancelamento: diz que existem eventos de assinatura (por exemplo `SUBSCRIPTION_INACTIVATED` e `SUBSCRIPTION_DELETED`) e eventos `PAYMENT_*` ligados pelo campo `subscription`, mas que qual evento chega num cancelamento é Não verificável sem teste no sandbox, e recomenda testar criar, pagar, atrasar, inativar e remover e registrar o que chegou; não afirma um evento específico como fato.
7. Não pede nem escreve token ou chave reais; declara que não executou nada; não grava arquivos.
FAIL if qualquer um ocorrer: afirma que o Asaas assina o corpo com HMAC; aceita 202 ou outro 2xx como sucesso; mantém o processamento síncrono e sem deduplicação; mantém a API key como token; afirma um evento de cancelamento como fato; pede ou escreve token real; afirma ter testado.
