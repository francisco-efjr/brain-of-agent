---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Cobre o caminho feliz e, em comportamento observável, pelo menos quatro situações próprias da plataforma ou do contexto: permissão de localização negada ou concedida só como aproximada; GPS desligado ou com precisão ruim; falta de conexão com o registro guardado e enviado depois sem perder o horário original; app encerrado ou em segundo plano durante o registro; diferença entre a hora do aparelho e a do servidor ou mudança de fuso; registro duplicado por toque repetido.
2. Trata a localização como dado pessoal (LGPD): finalidade, retenção ou quem vê, como pergunta ou critério, sem afirmar o que a lei exige.
3. Os limites que o pedido não dá (raio de tolerância do local, precisão mínima, prazo máximo para sincronizar, janela de tolerância do horário) aparecem como pergunta aberta com dono ou como Suposição explícita, nunca como fato decidido.
4. Os cenários são declarativos (sem toque em botão, sem nome de tela) e há ao menos um caminho negativo com resultado observável e mensagem esperada.
5. Indica que detalhes de plataforma (ciclo de vida do app, permissões, trabalho em segundo plano, regras da loja) têm profundidade no plugin mobile-apps (`/mobile-apps:playbook`) ou diz que são pendentes de especialista, sem escrever código Android.
FAIL if qualquer um ocorrer: só caminho feliz; ignora permissão, offline e hora do aparelho; inventa raio, precisão ou prazo como fatos; cenários do tipo "toco no botão Registrar"; escreve código Kotlin, testes ou step definitions; afirma que a solução cumpre norma trabalhista sem fonte.
