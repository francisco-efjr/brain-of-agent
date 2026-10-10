# Exemplos de achados, correções e greps de apoio (a11y-review)

Base: V-58 (HTML nativo antes de ARIA), V-24 (APG), V-45 (formulários), V-17 e V-42 (molde de achado), brain-of-agent `acessibilidade.md` (MIT, conteúdo próprio, adaptado). Os exemplos são cenários nossos. Confirme sempre na versão e no navegador do projeto; o comportamento de leitor de tela citado aqui é Inferido até alguém observá-lo.

## Sumário

1. Greps de detecção (pistas, não provas)
2. Modal feito com `div` e a correção com `<dialog>`
3. Botão só com ícone
4. Formulário com erro ligado ao campo
5. Região viva (toast e erro)
6. Roteiro mínimo de teclado

## 1. Greps de detecção

Use a ferramenta Grep com `glob` restrito ao código do projeto (`src/**/*.{tsx,jsx,vue,svelte,html}`); nunca rode em `node_modules`, `dist` ou `.next`. Cada resultado é uma pista a confirmar lendo o arquivo. Falsos positivos são esperados.

Formato: pista, padrão entre crases, o que confirmar.

- Clique em elemento não interativo: `<(div|span|li|td)[^>]*onClick`. Tem `role`, `tabIndex` e teclado? Quase sempre deveria ser `<button>`.
- Papel redundante ou sobreposto: `<button[^>]*role=` e `<a[^>]*role="button"`. Link que faz ação deveria ser botão.
- `tabindex` positivo: `tabIndex=\{?["']?[1-9]` e `tabindex="[1-9]`. Quebra a ordem natural (2.4.3).
- Foco removido: `outline:\s*(none|0)` e `outline-none`. Existe substituto visível (`focus-visible:ring`, `box-shadow`, `outline` customizado)?
- Ocultar focável: `aria-hidden=["']true` e `role=["']presentation`. O elemento ou algum descendente é focável? Se sim, é defeito (regra 4 de V-58).
- Imagem sem alternativa: `<img(?![^>]*\balt=)`. Decorativa recebe `alt=""`; informativa recebe texto.
- Campo sem rótulo: `<input(?![^>]*aria-label)` cruzado com `placeholder=`. Placeholder não é rótulo; existe `<label for>` correspondente?
- Botão ou link só com ícone: `<button[^>]*>\s*<(svg|img|i)\b`. O botão tem `aria-label` ou texto oculto visualmente?
- Idioma ausente: `<html(?![^>]*\blang=)`. Critério 3.1.1; em Next, `lang` no `<html>` do layout raiz.
- Movimento sem alternativa: `animation|transition|@keyframes`. Existe `prefers-reduced-motion: reduce` correspondente (V-23)?
- Alvo pequeno: `\b(h|w|size)-[1-5]\b` em botões e ícones. No Tailwind padrão `h-6` vale 24 px CSS e `h-5` vale 20 px; abaixo de 24 px, confirme exceção ou espaçamento equivalente (2.5.8).
- Autenticação: `onPaste=` e `autoComplete=["']off` em campos de senha ou código. Bloquear colar ou autocomplete viola 3.3.8.

## 2. Modal feito com `div` e a correção com `<dialog>`

Entrada (cenário nosso):

```tsx
export function ConfirmModal({ open, onClose, children }: Props) {
  if (!open) return null;
  return (
    <div className="overlay" onClick={onClose}>
      <div className="modal">
        <div className="close" onClick={onClose}>x</div>
        {children}
      </div>
    </div>
  );
}
```

Achados: o botão de fechar é `div onClick` sem papel, sem foco e sem nome (2.1.1, 4.1.2, Crítico); o foco não entra no diálogo nem volta ao gatilho (2.4.3, Alto); o diálogo não tem nome (4.1.2, Médio); Esc não fecha (2.1.1, Alto); o fundo continua navegável por Tab (Alto); clicar no overlay fecha e clicar no `div` interno propaga o clique para o overlay (comportamento surpreendente, Baixo).

Correção mínima, HTML nativo antes de ARIA:

```tsx
'use client';
import { useEffect, useId, useRef } from 'react';

interface ConfirmDialogProps {
  open: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export function ConfirmDialog({ open, onClose, title, children }: ConfirmDialogProps) {
  const ref = useRef<HTMLDialogElement>(null);
  const titleId = useId();

  // Sincroniza com a API imperativa do DOM: uso legítimo de Effect.
  useEffect(() => {
    const dialog = ref.current;
    if (!dialog) return;
    if (open && !dialog.open) dialog.showModal();
    if (!open && dialog.open) dialog.close();
  }, [open]);

  return (
    <dialog ref={ref} aria-labelledby={titleId} onClose={onClose}>
      <h2 id={titleId}>{title}</h2>
      {children}
      <button type="button" onClick={onClose}>Fechar</button>
    </dialog>
  );
}
```

O que `showModal()` entrega: fundo inerte, Esc fecha (o evento `close` chama `onClose`), foco para dentro do diálogo. Verifique no navegador do projeto: foco inicial no primeiro controle útil, Tab circula dentro, e o foco volta ao botão que abriu (os navegadores atuais restauram o foco; em modal feito à mão, o código restaura). Se o projeto usa biblioteca de diálogo (Radix, Headless UI, React Aria), prefira a que já existe e valide os mesmos pontos.

Reteste: Tab e Shift+Tab não saem do diálogo; Esc fecha; foco volta ao gatilho; árvore de acessibilidade mostra o diálogo com nome.

## 3. Botão só com ícone

```tsx
// Defeito (4.1.2): anunciado só como "botão".
<button onClick={remover}><TrashIcon /></button>

// Correção: nome acessível no botão; ícone fora da árvore.
<button type="button" onClick={remover} aria-label={`Remover ${item.nome} do carrinho`}>
  <TrashIcon aria-hidden="true" focusable="false" />
</button>
```

O nome precisa conter o texto visível se houver texto (2.5.3). Depois de remover, o foco vai ao próximo item e um aviso em região viva informa o resultado.

## 4. Formulário com erro ligado ao campo

```html
<label for="email">E-mail</label>
<input id="email" name="email" type="email" autocomplete="email" required
       aria-describedby="email-dica email-erro" aria-invalid="true">
<p id="email-dica">Usaremos para enviar a nota fiscal.</p>
<p id="email-erro">Informe um e-mail no formato nome@exemplo.com.</p>
```

- "E-mail inválido" cumpre só 3.3.1; "Informe um e-mail no formato nome@exemplo.com" cumpre 3.3.1 e 3.3.3 (V-45).
- Com vários erros, um resumo único (quantidade e lista com links aos campos) em vez de vários `aria-live`.
- `aria-invalid` só depois de validar; foco no primeiro campo inválido ou no resumo ao enviar com erro; `autocomplete` correto em dados pessoais (1.3.5). Estes três são prática comum sem fonte primária lida (Não verificável nas fontes de VALIDATED): confirme no W3C.
- Cor nunca é o único sinal: prefixo "Erro:" ou ícone com texto.

## 5. Região viva (toast e erro)

```html
<div id="aviso" role="status"></div>      <!-- educado: "Produto adicionado ao carrinho" -->
<div id="erro-global" role="alert"></div> <!-- interrompe: só para erro que bloqueia -->
```

As regiões existem no DOM, vazias, antes da mensagem. `role="alert"` para o que bloqueia; `role="status"` para o resto. Mensagem que some em poucos segundos com ação ("Desfazer") falha em 2.2.1.

## 6. Roteiro mínimo de teclado

1. Primeiro Tab mostra "Pular para o conteúdo" e leva ao `main` (2.4.1).
2. A ordem de foco segue a ordem visual (2.4.3).
3. Foco sempre visível (2.4.7) e não coberto por cabeçalho fixo, banner ou chat (2.4.11).
4. Tudo que funciona com mouse funciona com teclado (2.1.1): menu em hover, tooltip, carrossel, arrastar, seletor de data.
5. Sem armadilha (2.1.2): sai de player, editor rico, mapa e iframe de pagamento.
6. Diálogo: foco entra, circula, Esc fecha, foco volta.
7. Conteúdo de hover ou foco sai com Esc e não some ao passar o ponteiro sobre ele (1.4.13).

No macOS, ative a navegação por teclado do sistema e, no Safari, "Pressionar Tab para destacar cada item"; senão o Tab pula links e você reporta defeito falso.
