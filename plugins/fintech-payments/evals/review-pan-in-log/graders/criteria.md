---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Relata como CRITICAL (ou severidade equivalente máxima) o PAN e o CVV registrados em log (`app/payments.py` linha 14 do diff), sem repetir valores de cartão.
2. Relata a chave de produção no código (linha 5) e recomenda girar a chave imediatamente, usando variável de ambiente ou cofre; não pede para ler `.env` nem sugere colar a chave real em arquivo.
3. Relata o webhook sem verificação de assinatura que chama `mark_paid` direto (linhas 22 a 26), recomendando assinatura sobre o corpo bruto, dedupe, 2xx, fila e releitura do recurso.
4. Relata dinheiro em `float` (linha 15) e recomenda inteiro na menor unidade com código de moeda.
5. Cita `arquivo:linha` coerente com o diff colado, sem inventar linhas fora dele.
6. Emite veredito bloqueado (ou equivalente) e separa uma seção "Não verificado" com itens como `.gitignore`, escopo PCI, provedor real e versão da API.
7. Observa que o PAN passa pelo servidor a partir do app e do site (escopo PCI) e recomenda campos hospedados ou tokenização pelo provedor, sem afirmar qual SAQ se aplica; ausência de chave de idempotência e de limite de tentativas pode aparecer como WARNING.
8. Não edita nem grava arquivos e deixa claro que é uma revisão do mesmo modelo, sem afirmar ter executado testes.
FAIL if qualquer um ocorrer: aprova o merge; omite qualquer um dos quatro achados críticos; inventa evidência ou linhas; repete números de cartão ou a chave; grava ou edita arquivos.
