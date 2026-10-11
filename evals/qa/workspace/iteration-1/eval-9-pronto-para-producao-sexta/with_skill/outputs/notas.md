# Notas

## Arquivos da skill lidos
- skills/qa/SKILL.md (inteiro)
- skills/qa/references/estrategia.md (inteiro; seções de prontidão para produção, análise de risco, shift-right e exemplo de parecer)
- skills/qa/assets/templates/checklist-release.md (inteiro; usado como base da oferta de preencher o go/no-go e das condições)
- skills/qa/references/dominios.md (apenas sumário/intro, seção Saúde, e Datas/Feriados/Fusos horários)

Não li: plano-de-teste.md, design-de-testes.md, seguranca.md, dados-ambientes-ci.md. Nenhum script foi usado (só `python3` para confirmar dia da semana de 05, 09, 12 e 13/10/2026).

## Decisões
- Não respondi "sim" nem "não": o pedido não traz evidência (só "o dev disse que testou"), então a resposta é um parecer provisório com perguntas que mudam o resultado e condições para sexta.
- Data: hoje é segunda, 05/10/2026; sexta é 09/10 e segunda 12/10 é feriado nacional (Nossa Senhora Aparecida, lista de feriados da skill em dominios.md). Usei isso para a janela de deploy (plantão, defeito silencioso).
- Declarei explicitamente que nada foi executado ou visto (princípio de honestidade da skill).
- Mantive o tamanho moderado: tabela com 6 riscos priorizados, o que fica de fora, condições e perguntas.

## Incertezas
- Domínio suposto: consultas médicas/clínica (dado sensível, LGPD art. 11) e existência de lembretes. Se for outro tipo de agendamento (ex.: serviço de beleza, consultoria), a linha de dado de saúde e a de lembretes perdem peso.
- Não sei se é multi-clínica/multi-tenant, se há migração de agenda antiga, nem como é o deploy (flag, loja de app). Isso mudaria o peso do risco de rollback.
- Resultado esperado de fuso horário ("fuso da clínica") e de agendamento em feriado/férias são suposições de oráculo: a regra precisa vir do PO, e deixei isso dito na resposta.
- Sugeri "quinta de manhã com flag ou terça 13/10" como alternativas; a skill não dá regra explícita contra deploy de sexta, o argumento é derivado (custo de correção, plantão, detectabilidade baixa, janela de deploy do template de checklist).
- A afirmação de que 403/404 é o esperado no caso de troca de ID vem do exemplo de risco R3 em estrategia.md; confirmar com o contrato da API do produto.
