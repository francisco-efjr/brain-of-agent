---
name: form-server-action-next
description: Mede se o plugin corrige um formulário Next.js com Server Action sem autenticação, com userId em campo hidden e validação só no cliente, devolvendo erros como estado, usando useActionState, ligando o erro ao campo por aria-describedby e rotulando versões.
tags: [web-frontend, forms-and-data, nextjs, server-actions, security, a11y]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Move a autenticação e a autorização para a primeira linha da action, obtém o usuário da sessão e não de hidden, valida com schema via safeParse no servidor, devolve erros como estado com useActionState, mostra erro ligado ao campo por aria-describedby, rotula as versões como premissa e não afirma ter executado."
model: sonnet
---
Next.js 16 com App Router e React 19. Este formulário de perfil funciona, mas um colega disse que é inseguro, e a validação some quando o JavaScript demora a carregar. Revisa e reescreve do jeito certo. Usamos Zod.

```tsx
// app/perfil/actions.ts
'use server';
import { db } from '@/lib/db';

export async function atualizarPerfil(formData: FormData) {
  const userId = formData.get('userId') as string;
  const email = formData.get('email') as string;
  if (!email) throw new Error('Informe o e-mail');
  await db.user.update({ where: { id: userId }, data: { email } });
}
```

```tsx
// app/perfil/PerfilForm.tsx
'use client';
import { atualizarPerfil } from './actions';

export function PerfilForm({ userId, emailAtual }: { userId: string; emailAtual: string }) {
  return (
    <form
      action={atualizarPerfil}
      onSubmit={(e) => {
        const email = new FormData(e.currentTarget).get('email') as string;
        if (!email.includes('@')) {
          e.preventDefault();
          alert('E-mail inválido');
        }
      }}
    >
      <input type="hidden" name="userId" value={userId} />
      <input name="email" placeholder="E-mail" defaultValue={emailAtual} />
      <button>Salvar</button>
    </form>
  );
}
```
