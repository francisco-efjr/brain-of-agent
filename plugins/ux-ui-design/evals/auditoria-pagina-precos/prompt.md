---
name: auditoria-pagina-precos
description: Mede se uma auditoria de UI pedida sobre uma página de preços colada em HTML e CSS é feita somente leitura, nas categorias do plugin, com PASS, PARTIAL ou FAIL e evidência citada do código, tratando o visual como Inferido e sem editar nada.
tags: [ux-ui-design, ui-audit, somente-leitura]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
timeout_seconds: 600
runs: 3
expected_outcome: "Auditoria somente leitura com categorias PASS/PARTIAL/FAIL e impacto; detecta outline: none, transition: all, placeholder usado como único rótulo, contraste #999 sobre branco e grade de 3 colunas sem ajuste mobile, citando o trecho; rotula o visual como Inferido; lista Não verificado; propõe correções sem aplicar."
model: sonnet
---
Revisa o visual dessa página de preços, está com cara de template, né? Só revisa; não mexe em nada. É o código inteiro, não tenho o projeto aqui.

```html
<section class="pricing">
  <h2>Escolha seu plano</h2>
  <div class="cards">
    <div class="card"><div class="icon"></div><h3>Básico</h3><p class="price">R$ 29/mês</p><p>Para quem está começando</p><a href="#" class="btn">Assinar</a></div>
    <div class="card"><div class="icon"></div><h3>Pro</h3><p class="price">R$ 79/mês</p><p>Para equipes pequenas</p><a href="#" class="btn">Assinar</a></div>
    <div class="card"><div class="icon"></div><h3>Empresa</h3><p class="price">R$ 199/mês</p><p>Para quem precisa de mais</p><a href="#" class="btn">Assinar</a></div>
  </div>
  <form class="trial">
    <input type="email" placeholder="Seu e-mail">
    <button>Enviar</button>
  </form>
</section>
<style>
  body { margin: 0; font-family: Inter, sans-serif; }
  .pricing { background: linear-gradient(135deg, #7b2ff7, #f107a3); padding: 80px 20px; text-align: center; color: #fff; }
  .cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; max-width: 960px; margin: 0 auto; }
  .card { background: rgba(255,255,255,.12); border-radius: 16px; padding: 32px; transition: all .3s; }
  .card:hover { transform: translateY(-8px); }
  .icon { width: 56px; height: 56px; border-radius: 50%; background: rgba(255,255,255,.25); margin: 0 auto 16px; }
  .price { font-size: 28px; }
  .btn { display: inline-block; padding: 10px 18px; background: #fff; color: #999999; border-radius: 8px; text-decoration: none; outline: none; }
  .trial input { padding: 8px; border: 1px solid #ddd; outline: none; }
  .trial input::placeholder { color: #999999; }
</style>
```
