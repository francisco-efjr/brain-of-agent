# Notas e incertezas

- Não tenho acesso ao código, aos testes nem ao ambiente do usuário (nem existe repositório git aqui). Não consegui verificar se a feature realmente foi testada; a resposta trata "o dev disse que testou" como afirmação sem evidência, não como falsa.
- Não sei o domínio exato. Assumi que "consultas" é consulta médica/clínica (dado de saúde, LGPD, risco de agendamento duplicado). Se for outro tipo de consulta (jurídica, de consultoria), alguns itens (dado sensível) pesam menos, mas a lógica de concorrência/cancelamento/fuso continua válida.
- Não sei se existe feature flag, ambiente de homologação, CI com testes automatizados ou rollback fácil. A resposta pergunta isso em vez de supor.
- Data: hoje é segunda, 05/10/2026 (confirmado com python). Sexta é 09/10/2026. Segunda 12/10/2026 é feriado nacional (Nossa Senhora Aparecida), de memória; não verifiquei em fonte externa (sem rede) e a empresa pode não seguir o feriado ou ter calendário próprio. Usei isso como argumento extra, não como o principal.
- Não sei se há pressão real de prazo para sexta. A resposta cobre o caso "tem que ser sexta" com condições mínimas, em vez de proibir.
- Escolhi dar uma recomendação clara (não subir assim) em vez de só devolver uma checklist, porque o usuário perguntou sim/não. Risco: pode soar mais firme do que as informações permitem; por isso o texto deixa explícito que a feature pode estar boa, só não foi verificada.
- Não usei skills nem li evals, conforme instruído. A lista de casos de teste vem de conhecimento geral sobre sistemas de agendamento.
