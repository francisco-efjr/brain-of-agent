---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta pelo menos 4 problemas reais, cada um com referência às linhas do bloco colado (arquivo:linha ou trecho) e severidade: (a) `test_aplicar_cupom` com asserção fraca (`is not None`); (b) `test_total_com_desconto` com oráculo circular (o esperado usa `aplicar_desconto` do próprio código) e import ausente de `aplicar_desconto`, o que faria o teste falhar por `NameError`; (c) `test_cupom_expirado_e_recusado` que só confere a chamada do mock e não o retorno, enquanto o código aceita cupom expirado (`validar_cupom` devolve verdadeiro), um defeito de produção que o teste não pega e cujo nome promete mais do que verifica; (d) `test_cupom_nao_acumula_com_vip` desligado com `skip` sem justificativa útil e sem exercitar VIP.
2. Faz um mutation check mental: indica uma mudança realista no código de produção (por exemplo fazer `validar_cupom` devolver sempre verdadeiro ou sempre falso) e diz que nenhum teste ativo a derrubaria.
3. Ordena os achados por dano (falso verde e defeito não coberto à frente de estilo) e dá um veredito (Precisa de ajuste ou equivalente).
4. Diz que não executou os testes e rotula o que é Verificado (lido no código), Inferido ou Suposição; declara que a revisão é feita por modelo que pode ter escrito o código e não é validação independente.
5. Não escreve nem edita arquivos e não reescreve a suíte inteira; as correções aparecem como recomendações curtas.
FAIL if qualquer um ocorrer: aprova os testes; afirma que os testes passam ou falham como se tivesse executado; comenta só estilo; escreve ou edita arquivos; não identifica o teste de expiração que não protege nada.
