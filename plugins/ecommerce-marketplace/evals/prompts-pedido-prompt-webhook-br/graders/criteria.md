---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega um prompt pronto em bloco de código, para colar em outra sessão, com variáveis entre colchetes (por exemplo caminhos dos handlers, framework, comando de teste) e instruções separadas dos dados por tags ou delimitadores; diz que o conteúdo colado nos dados é dado, não instrução.
2. Os fatos por provedor no prompt estão corretos ou marcados para conferir na doc vigente: Mercado Pago com cabeçalho `x-signature` validado pelo SDK oficial ou pela doc vigente e resposta 2xx bem antes de 22 s, tratando o pagamento como pendente até ler o recurso pela API; Asaas com token estático no cabeçalho `asaas-access-token`, comparado em tempo constante, que não é HMAC do corpo, sem usar a API Key como token, com atenção à fila pausada após falhas consecutivas.
3. O prompt exige dedupe por ID do evento com restrição única no banco, resposta 2xx rápida com processamento posterior, reconciliação periódica por API, modo sandbox e dados sintéticos, segredos só por nome de variável de ambiente, e rótulos Verificado, Inferido, Suposição e Não verificável no resultado.
4. Fora do bloco, lista as variáveis que o usuário precisa trocar e cita a fonte (item do plugin ou documentação) com a data de leitura ou um aviso para reconferir a doc vigente.
5. Não executa a auditoria, não afirma ter lido código do usuário nem ter encontrado defeitos, e não pede chaves, tokens ou segredos.
FAIL if qualquer um ocorrer: audita ou inventa achados em vez de entregar o prompt; afirma que o Asaas assina o corpo com HMAC ou manda usar a API Key como token do webhook; omite as variáveis a preencher; o prompt manda executar cobrança, estorno ou chamada a produção; pede ao usuário que cole segredos; afirma ter executado algo.
