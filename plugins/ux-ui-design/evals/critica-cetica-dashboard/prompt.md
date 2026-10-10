---
name: critica-cetica-dashboard
description: Mede se uma crítica cética pedida sobre um dashboard colado em HTML, com briefing e especificação, produz notas de 1 a 5 em quatro critérios com evidência localizável, não verificado onde falta evidência, achados P0 P1 P2 e veredito, sem elogio genérico, sem editar arquivos e rotulando Verificado e Inferido.
tags: [ux-ui-design, design-evaluator, critica, agente]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Task, Agent, Write, Edit]
timeout_seconds: 600
runs: 3
expected_outcome: "Tabela com os quatro critérios (design, originalidade, acabamento, funcionalidade) com nota 1 a 5 e evidência localizável do HTML; nota não verificado onde não há evidência; achados P0, P1 e P2 com local, evidência e correção; veredito retrabalhar ou aprovar com justificativa; rótulos Verificado e Inferido; declara limitação por não renderizar; não edita arquivos."
model: sonnet
---
Faz uma crítica cética desse dashboard, não quero elogio. Você pode usar um avaliador independente se achar que ajuda. Não tenho captura de tela, só o código; trata a limitação como parte da avaliação.

Briefing: painel para gerentes de loja de roupas acompanharem o mês, no desktop e às vezes no tablet.
Especificação: o KPI principal é a receita do mês; a ação primária é "Exportar relatório"; a tabela de pedidos precisa de estado vazio, carregando e erro.

```html
<!-- dashboard.html -->
<main>
  <h1>Painel</h1>
  <div class="kpis">
    <div class="kpi"><span>Receita</span><strong>R$ 48.230</strong></div>
    <div class="kpi"><span>Pedidos</span><strong>312</strong></div>
    <div class="kpi"><span>Ticket médio</span><strong>R$ 154</strong></div>
    <div class="kpi"><span>Novos clientes</span><strong>87</strong></div>
    <div class="kpi"><span>Reembolsos</span><strong>6</strong></div>
  </div>
  <img src="/charts/receita.png">
  <button class="export">Exportar relatório</button>
  <table id="orders"><thead><tr><th>Pedido</th><th>Cliente</th><th>Total</th></tr></thead><tbody id="rows"></tbody></table>
</main>
<script>
fetch('/api/orders').then(r => r.json()).then(orders => {
  document.getElementById('rows').innerHTML = orders.map(o => `<tr><td>${o.id}</td><td>${o.customer}</td><td>${o.total}</td></tr>`).join('');
});
</script>
<style>
.kpis { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; }
.kpi { background: #fff; padding: 16px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,.1); }
.kpi strong { font-size: 24px; display: block; }
.export { font-size: 12px; padding: 4px 8px; background: #eee; border: 0; }
</style>
```
