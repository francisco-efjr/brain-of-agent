# Padrões e snippets acessíveis (web)

Snippets mínimos para especificar ou corrigir. Antes de aplicar em produto real, teste no navegador e na tecnologia assistiva do público: este arquivo é leitura de padrões, não teste executado. Conferir a versão de navegadores suportados do projeto; `<dialog>` é suportado nos navegadores atuais, mas confirme o suporte mínimo do seu público.

Fontes: padrão de diálogo modal do APG (https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/; V-10), anti-padrões de `a11y.instructions.md` do github/awesome-copilot (MIT; V-09), `prefers-reduced-motion` (https://web.dev/articles/prefers-reduced-motion; V-38), `acessibilidade.md` do brain-of-agent (MIT, do usuário). Código escrito para este plugin.

## Sumário

- [Diálogo modal](#diálogo-modal)
- [Formulário](#formulário)
- [Mensagens de status e alerta](#mensagens-de-status-e-alerta)
- [Pular para o conteúdo e foco não obscurecido](#pular-para-o-conteúdo-e-foco-não-obscurecido)
- [Movimento reduzido](#movimento-reduzido)
- [Alvos e foco visível](#alvos-e-foco-visível)
- [Antipadrões frequentes](#antipadrões-frequentes)

## Diálogo modal

Checklist de nove itens (APG e V-10):

1. O contêiner tem papel de diálogo (`<dialog>` já tem) e todo o conteúdo necessário é descendente dele.
2. Tem nome: `aria-labelledby` apontando para o título visível, ou `aria-label`.
3. O resto da página fica realmente bloqueado e visualmente obscurecido (`showModal()` faz o fundo inerte). `aria-modal="true"` só quando o bloqueio é real; num `div` feito à mão, sem bloqueio, declarar `aria-modal` é erro grave.
4. Tab e Shift+Tab circulam dentro do diálogo; nem o Tab nem o cursor virtual do leitor escapam para o fundo.
5. Esc fecha.
6. Há botão visível de fechar ou cancelar.
7. Foco inicial no primeiro elemento focável, ou, em conteúdo longo ou estruturado, num elemento estático com `tabindex="-1"` (por exemplo o título). Em ação irreversível, considere focar a ação menos destrutiva.
8. Ao fechar, o foco volta ao elemento que abriu (exceções documentadas pelo APG); navegadores atuais fazem isso com `<dialog>`; em modal feito à mão, é responsabilidade do código.
9. Nenhum `tabindex` positivo.

```html
<button type="button" id="abrir-exclusao">Excluir projeto</button>

<dialog id="exclusao" aria-labelledby="exclusao-titulo" aria-describedby="exclusao-texto">
  <h2 id="exclusao-titulo">Excluir o projeto "Loja Centro"?</h2>
  <p id="exclusao-texto">Serão apagados 14 relatórios e 3 convites. Esta ação não pode ser desfeita.</p>
  <form method="dialog">
    <button value="cancelar" autofocus>Manter projeto</button>
    <button value="excluir">Excluir projeto</button>
  </form>
</dialog>

<script>
  const dlg = document.getElementById('exclusao');
  document.getElementById('abrir-exclusao').addEventListener('click', () => dlg.showModal());
  dlg.addEventListener('close', () => {
    if (dlg.returnValue === 'excluir') { /* chamar a exclusão e anunciar o resultado em role="status" */ }
  });
</script>
```

O texto de exemplo nomeia o que se perde (confirmação destrutiva). O `autofocus` na ação menos destrutiva segue a recomendação do APG para ações irreversíveis. Os números do texto são ilustrativos.

## Formulário

```html
<label for="email">E-mail</label>
<input id="email" name="email" type="email" autocomplete="email" required
       aria-invalid="true" aria-describedby="email-dica email-erro">
<p id="email-dica">Usaremos para enviar a nota fiscal.</p>
<p id="email-erro">Informe um e-mail no formato nome@exemplo.com.</p>
```

- Rótulo visível e ligado por `for`/`id`; placeholder não é rótulo (some ao digitar).
- Obrigatório com `required` e indicação visível que não seja só cor nem asterisco sem legenda. `aria-invalid` só depois da validação.
- Erro diz como corrigir (3.3.3) e é ligado por `aria-describedby`. Ao enviar com erro, mova o foco para o primeiro campo inválido ou para um resumo com links para os campos.
- Grupos relacionados (rádios) em `fieldset` com `legend`.
- `autocomplete` correto em dados pessoais (1.3.5); não bloqueie colar nem gerenciador de senhas (3.3.8).
- Entrada redundante: preencha de novo o que o usuário já informou no mesmo processo (3.3.7), ou ofereça "mesmo endereço".
- No celular, campo com fonte de pelo menos 16 px evita o zoom automático do iOS (regra citada em V-27).

## Mensagens de status e alerta

A região precisa existir no DOM, vazia, **antes** da mensagem. Inserir a região junto com o texto faz muitos leitores calarem.

```html
<div id="aviso" role="status"></div>      <!-- educado: "Produto adicionado ao carrinho" -->
<div id="erro-global" role="alert"></div> <!-- interrompe: só para erro que bloqueia -->
```

- Toast com ação ("Desfazer") que some em 3 s falha em tempo (2.2.1). Dê tempo ou mantenha até a dispensa.
- Não coloque `aria-live` em região que muda a cada segundo.
- Estado de carregamento: mantenha o foco no botão e anuncie o texto ("Salvando…"); `disabled` durante o carregamento tira o botão do foco do teclado, então prefira `aria-disabled="true"` e ignore cliques repetidos. Spinner decorativo com `aria-hidden="true"` precisa de texto acessível em outro ponto.

## Pular para o conteúdo e foco não obscurecido

```html
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<main id="conteudo" tabindex="-1">…</main>
```

```css
.skip { position: absolute; inset-inline-start: 0; inset-block-start: -3rem; }
.skip:focus { inset-block-start: 0; }
html { scroll-padding-block-start: 4rem;   /* altura do cabeçalho fixo */
       scroll-padding-block-end: 5rem; }   /* altura da barra fixa inferior (2.4.11) */
```

Num SPA, ao trocar de rota mova o foco para o `h1` (ou anuncie o novo título); a falha clássica é o foco ficar na página que sumiu.

## Movimento reduzido

Padrão recomendado: aplicar a animação dentro de `no-preference`, de modo que quem não entende a consulta também não receba movimento.

```css
.cartao { transition: none; }
@media (prefers-reduced-motion: no-preference) {
  .cartao { transition: transform 200ms ease-out, opacity 200ms ease-out; }
}
```

```js
const reduz = window.matchMedia('(prefers-reduced-motion: reduce)');
function aplicar() { document.documentElement.toggleAttribute('data-sem-movimento', reduz.matches); }
reduz.addEventListener('change', aplicar); aplicar();   // animações em JS pararam em andamento ao mudar
```

Reduzir não é zerar tudo: movimento essencial (por exemplo, indicar progresso) pode permanecer, de forma mais sóbria. Duração e easing são regras de polegar (Inferido).

## Alvos e foco visível

```css
:where(a, button, input, select, textarea, summary, [role="button"]):focus-visible {
  outline: 2px solid var(--color-focus);   /* contraste de pelo menos 3:1 contra o fundo adjacente (1.4.11) */
  outline-offset: 2px;
}
.btn { min-block-size: 44px; min-inline-size: 44px; }   /* meta de toque; o piso normativo é 24 px CSS (2.5.8) */
```

Nunca `outline: none` sem substituto equivalente. Alvo de 24 px com espaçamento: um círculo de 24 px centrado em cada alvo não pode intersectar outro alvo (exceção prevista no 2.5.8).

## Antipadrões frequentes

| Antipadrão | Por que falha | Correção |
| --- | --- | --- |
| `<div onclick>` como botão | sem foco nem Enter/Espaço; sem papel (4.1.2, 2.1.1) | `<button type="button">` |
| `aria-hidden="true"` em elemento focável | foco cai em algo "inexistente" para o leitor | remover o atributo ou o foco (`inert`) |
| `aria-label` em `div` ou `span` sem papel | muitos leitores ignoram | usar elemento nativo ou dar papel |
| Nome acessível diferente do texto visível | controle por voz falha (2.5.3) | o nome acessível contém o texto visível |
| `role="presentation"` em tabela de dados | perde a estrutura (1.3.1) | usar `<table>` com `th` |
| Combobox sem nome | anunciado só como "caixa de combinação" | `aria-label` ou `aria-labelledby` |
| Abas usadas como filtro com `aria-controls` para painel inexistente | referência quebrada | grupo de botões com `aria-pressed` |
| `id` duplicado referenciado por `aria-labelledby` | quebra a relação (1.3.1, 4.1.2) | ids únicos |
| ID de teste (`btn_submit_01`) em `content-desc` no Android | o TalkBack lê em voz alta | usar `resource-id` ou `testTag` para automação |
