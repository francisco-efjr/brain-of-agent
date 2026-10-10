---
name: a11y-modal-react
description: Mede se o plugin audita a acessibilidade de um modal React (div clicável, foco, nome, rótulo, outline removido) com achados por arquivo:linha e critério WCAG 2.2, recomenda HTML nativo antes de ARIA e não afirma ter testado com leitor de tela.
tags: [web-frontend, a11y-review, accessibility, wcag, keyboard]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Lista achados com arquivo:linha, severidade e critério WCAG (2.1.1, 4.1.2, 2.4.7, 3.3.2 e foco do diálogo), recomenda dialog com showModal ou gestão de foco equivalente e botões reais com nome acessível, separa o que leu do que não testou e não edita nada."
model: sonnet
---
Os usuários de teclado do nosso app reclamaram deste modal de exclusão de conta (React 18 com Vite). Revisa e me diz o que está errado. Ainda não quero correção aplicada, só o diagnóstico com o que eu preciso mudar.

```tsx
// src/components/DeleteAccountModal.tsx
import { useState } from 'react';
import './modal.css';

interface Props {
  open: boolean;
  onClose: () => void;
  onConfirm: () => void;
}

export function DeleteAccountModal({ open, onClose, onConfirm }: Props) {
  const [text, setText] = useState('');
  if (!open) return null;
  return (
    <div className="overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="close" onClick={onClose}>×</div>
        <h3>Excluir conta?</h3>
        <p>Essa ação não pode ser desfeita.</p>
        <input
          className="confirm-input"
          placeholder="Digite EXCLUIR para confirmar"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <div className="btn danger" onClick={() => text === 'EXCLUIR' && onConfirm()}>
          Excluir minha conta
        </div>
      </div>
    </div>
  );
}
```

```css
/* src/components/modal.css */
.overlay { position: fixed; inset: 0; background: rgba(0, 0, 0, 0.5); }
.modal { background: #fff; margin: 10vh auto; width: 420px; padding: 24px; position: relative; }
.close { position: absolute; top: 8px; right: 12px; width: 16px; height: 16px; cursor: pointer; }
.btn { display: inline-block; padding: 8px 16px; cursor: pointer; }
.btn:focus, .confirm-input:focus { outline: none; }
.danger { background: #c0392b; color: #777; }
```
