# Triagem de teste flaky: <teste ou arquivo>

Como usar (saída da skill `flaky-triage`): retry detecta, não corrige. Preserve a primeira falha, meça a taxa, classifique a causa **antes** de mexer, corrija a causa, valide com repetição. Valores numéricos abaixo são iniciais e ajustáveis (convenção de uma fonte classe C, V-37, cruzada com V-19, V-21, V-24). Confirme editar CI, config ou marcar `skip` com o usuário.

- **Teste e comando de execução:** `<comando>` · **Ambiente e versão:** <...>
- **Primeira falha preservada** (log, trace; segredos mascarados): <caminho>
- **Taxa antes** (mesmo comando, execuções repetidas, ex.: `--repeat-each=30 --workers=1 --retries=0`): <falhas ÷ execuções> · **Só falha em paralelo?** <sim/não>
- **Causa** (uma das sete): ☐ timing/espera · ☐ dependência de dados · ☐ ambiente · ☐ dependência de ordem · ☐ sensibilidade a tempo/relógio · ☐ renderização visual · ☐ serviço externo
- **Evidência da causa** (o que as falhas têm em comum e as passagens não): <...>
- **Mudança** (corrige a causa; não apenas aumenta timeout, retries ou espera fixa): <...>
- **Taxa depois** (mesmo comando): <valor inicial de referência: 50 execuções seguidas sem falha; ajuste ao custo> · **Diff conferido:** <nenhuma asserção removida ou afrouxada>
- **O que não foi validado:** <...>
- **Quarentena** (só se não houver correção agora; fora do gate): ticket <ID> · dono <nome> · data de entrada <AAAA-MM-DD> · prazo <valor inicial: 14 dias> · risco coberto por <alternativa>. Fração da suíte em quarentena: <valor inicial de alerta: 5%; acima disso, problema de processo>
- **Política de retry:** no máximo uma retentativa como sinal; resultado "flaky" abre ticket com dono e prazo.
