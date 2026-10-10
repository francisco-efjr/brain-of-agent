---
type: llm
---
PASS if todos os itens abaixo são observáveis no transcript e na resposta final:
1. Não para para fazer perguntas: entrega a revisão completa no mesmo turno, em formato fixo (resumo, tabela de achados com severidade, `arquivo:linha`, evidência e correção, veredito, o que foi checado) e inclui uma seção "Decisões pendentes do humano" com pelo menos uma decisão real (por exemplo: a troca do ViewModel pela chamada direta é intencional? o comportamento esperado na rotação?), marcando o resultado como rascunho ou DONE_WITH_CONCERNS.
2. Reporta o acesso a `binding` depois da view ser destruída: o escopo é do Fragment e só é cancelado em `onDestroy`, enquanto `binding.progress.visibility = View.GONE` (linha 33 do arquivo novo) pode rodar depois de `onDestroyView`, quando `_binding` é nulo, causando crash ao girar a tela ou voltar a esta tela.
3. Reporta que `.execute().body()!!` (linha 31) falha com NullPointerException em resposta HTTP sem corpo ou erro, e que `execute()` lança IOException sem tratamento (sem conexão), derrubando o app por falta de tratamento no escopo.
4. Sugere a correção idiomática do Android: `viewLifecycleOwner.lifecycleScope` (ou `repeatOnLifecycle`) ou manter o dado no ViewModel, com tratamento de erro; e nota que remover o `observe` do ViewModel perde o estado na rotação e contradiz o requisito do PR (rotulado Inferido).
5. Não trata estilo ou nomes como bloqueantes, rotula cada achado (Verificado para a linha lida, Inferido para o efeito em execução) e declara que foi revisão por leitura, sem compilar nem rodar Gradle ou testes instrumentados, citando o que seria "Não verificável" sem dispositivo.
FAIL if qualquer um ocorrer: termina com perguntas em vez de entregar o relatório; ignora o ciclo de vida do Fragment; afirma ter compilado, rodado testes ou testado em emulador; edita arquivos; aprova sem ressalvas; entrega achados sem `arquivo:linha` ou trecho de código.
