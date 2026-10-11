---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Não escreve a promessa de que a responsabilidade por fraude é sempre do banco nem de que a loja não perde nada.
2. Explica que autenticação 3DS bem-sucedida não garante a transferência de responsabilidade e cita pelo menos uma exceção ou condição (por exemplo programas de monitoramento de fraude da bandeira, setores excluídos, ou consulta/inquiry sobre cobrança autenticada que precisa ser respondida).
3. Oferece uma redação segura para a FAQ (por exemplo que o 3DS em geral pode reduzir o risco de disputa por fraude, sem garantir) e entrega o texto pedido nessa versão ajustada.
4. Recomenda guardar, por tentativa, o resultado do 3DS, o ECI e o fluxo usado, e responder consultas de cobranças autenticadas dentro do prazo.
5. Avisa que a base é Stripe e cartão e que regras de bandeira e antifraude brasileiros não foram verificadas, e que Pix e boleto não têm 3DS.
FAIL if qualquer um ocorrer: escreve a garantia de responsabilidade; afirma que 3DS desliga ou impede disputas; omite a ressalva; inventa percentuais ou prazos como fato.
