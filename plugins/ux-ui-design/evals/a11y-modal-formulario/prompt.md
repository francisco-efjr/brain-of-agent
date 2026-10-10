---
name: a11y-modal-formulario
description: Mede se, ao perguntarem se um modal de cadastro passa na WCAG, o plugin cita critérios coerentes com o código, recomenda HTML nativo e dialog com showModal, trata foco, rótulos e erro, não declara conformidade legal e lembra que automação não prova acessibilidade.
tags: [ux-ui-design, a11y-checklist, wcag]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Cita critérios WCAG 2.2 pertinentes ao código (2.1.1, 4.1.2, 3.3.2 ou 1.3.1, 1.4.1, 2.4.3 ou 2.4.7), recomenda dialog com showModal, foco devolvido ao gatilho, label associado e erro ligado ao campo; não declara conformidade legal; separa o que foi lido do que não foi testado."
model: sonnet
---
Isso passa na WCAG? O que eu corrijo? Quando fecho o modal o foco some, e o time de suporte reclamou que quem usa só o teclado não consegue se cadastrar. Meu chefe quer saber se, corrigindo isso, estamos em conformidade com a lei europeia de acessibilidade, já que vendemos para clientes lá.

```html
<div class="overlay" id="m">
  <div class="modal">
    <div class="close" onclick="closeModal()">X</div>
    <h3>Cadastre-se</h3>
    <input placeholder="Nome completo">
    <input placeholder="E-mail" id="email">
    <span style="color:red">E-mail inválido</span>
    <div class="btn" onclick="submitForm()">Enviar</div>
  </div>
</div>
<style>
  .overlay { position: fixed; inset: 0; background: rgba(0,0,0,.5); }
  .btn { background: #2d6a4f; color: #fff; padding: 10px 16px; outline: none; cursor: pointer; }
  input { outline: none; }
</style>
<script>
  function closeModal() { document.getElementById('m').style.display = 'none'; }
</script>
```
