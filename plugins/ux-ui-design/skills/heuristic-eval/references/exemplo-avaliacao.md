# Exemplo de avaliação heurística (resumido)

Caso sintético. O fluxo foi inventado para calibrar formato e profundidade; não descreve nenhum produto real.

## Material recebido

"Fluxo de recuperar senha de um app de finanças pessoais. Tela 1: campo 'E-mail' e botão 'Enviar'. Tela 2 (após enviar): texto 'Verifique seu e-mail.' sem botão. E-mail recebido: link que abre a tela 3 com dois campos de senha e botão 'Salvar'. Se o link expirou, a tela 3 mostra 'Erro 401'. Depois de salvar, volta ao login sem mensagem. Regra de segurança do produto: a tela 2 aparece mesmo se o e-mail não existe."

## Cabeçalho

Escopo: recuperar senha pelo e-mail · Usuário: cliente que esqueceu a senha, no celular · Tarefa: voltar a entrar na conta · Material: descrição textual (nada renderizado) · Passadas: 1. Todo achado é Inferido.

## Achados

| ID | Heurística | Local e evidência | Severidade | Justificativa | Correção |
| --- | --- | --- | --- | --- | --- |
| H-01 | 9 Recuperar de erros | Tela 3, texto "Erro 401" | 3 | frequência: todo usuário que abre o link expirado; impacto: não sabe que basta pedir outro; persistência: repete até descobrir | "Este link expirou. Peça um novo link" com botão "Enviar novo link" que leva à tela 1 |
| H-02 | 1 Visibilidade do estado | Tela 2, "Verifique seu e-mail." sem ação | 2 | frequência: todos; impacto: moderado (não sabe se o e-mail chegou nem para qual endereço); persistência: só no primeiro uso | mostrar o e-mail digitado (mascarado), orientar a checar a caixa de spam e oferecer "Reenviar" |
| H-03 | 1 Visibilidade do estado | Pós-salvar: volta ao login sem mensagem | 2 | frequência: todos; impacto: moderado (dúvida se salvou) | mensagem "Senha alterada. Entre com a nova senha." |
| H-04 | 5 Prevenção de erros | Tela 3, dois campos de senha sem regras visíveis | 2 | frequência: parte dos usuários; impacto: moderado (descobre as regras por erro) | exibir as regras antes da digitação e permitir mostrar a senha |
| H-05 | 3 Controle e liberdade | Tela 2 sem "Voltar" nem "Usei outro e-mail" | 2 | frequência: quem digitou o e-mail errado; impacto: moderado | link "Corrigir e-mail" |

Heurísticas 2, 4, 6, 7, 8 e 10: sem achados com o material recebido (não force achado para cobrir a lista).

## Trade-offs a validar

- **Tela 2 aparece mesmo se o e-mail não existe.** Escolha defensável de segurança (evita revelar quais e-mails têm conta). Isso reduz a visibilidade do estado (H-02), mas a regra é do produto. A tensão se resolve com texto que não confirma nem nega ("Se este e-mail tiver uma conta, enviaremos um link"). Testar com usuários se esse texto gera confusão. Rótulo: trade-off a validar, não defeito.

## Top 3

H-01 (severidade 3), depois H-02 e H-03 empatados em 2 e de correção barata.

## O que testar com usuários

1. Quantos entendem, sem ajuda, que o link expirou e como pedir outro (H-01, tarefa observada com 5 participantes do perfil).
2. Se o texto neutro da tela 2 é entendido sem criar a dúvida "meu e-mail não existe?".
3. Se a mensagem pós-salvar basta para voltar ao login sem hesitar.

Veja `user-research-plan` para montar a sessão.

## Limitações

Opinião de um único modelo sobre uma descrição textual; nenhuma execução, captura ou leitura de código. Severidades são estimativas de julgamento. Esta avaliação não substitui teste com usuários e não prevê taxa de conclusão.
