---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Propõe uma lista de funcionalidades em JSON (por exemplo `features.json`) com itens pequenos e testáveis (id, descrição, passos verificáveis, `"passes": false`), derivados do que o usuário descreveu (salas geradas, dash, 3 tipos de inimigo, chefe), sem inventar funcionalidades fora do pedido.
2. Define a regra de edição: só o campo `passes` muda, e só depois de rodar os passos e ter a evidência; os passos não são apagados nem editados; uma funcionalidade por sessão.
3. Propõe um arquivo de progresso e a rotina de início de sessão (confirmar diretório, ler o log do git e o progresso, ler a lista e pegar o primeiro item com `passes: false`, rodar o init e o teste mínimo antes de codar) e de fim de sessão (commit descritivo, registrar o que ficou quebrado).
4. Prevê um init com check headless do Godot, em script adequado ao Windows (PowerShell ou Python), e diz que o script só é executado com confirmação do usuário; não manda `bash`/`.sh` como única opção.
5. Lista sensação, áudio e legibilidade como pendência humana a cada funcionalidade, e propõe o contrato de pronto ou critério de aceite para a primeira funcionalidade.
6. Não afirma ter criado arquivos, rodado comandos ou testado algo; apresenta tudo como proposta; não faz commit nem instala nada; se propuser uma pergunta (por exemplo framework de teste), segue sem bloquear e a lista como decisão pendente.
FAIL if qualquer um ocorrer: lista de tarefas em Markdown solto sem `passes` ou equivalente verificável; "faça tudo de uma vez" ou o jogo inteiro numa tarefa; afirma ter criado ou executado algo; deixa o agente marcar `passes: true` sem rodar os passos; usa apenas script de shell Unix sem alternativa para Windows; manda executar script ou instalador de terceiros.
