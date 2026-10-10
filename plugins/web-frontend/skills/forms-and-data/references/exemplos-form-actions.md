# Exemplos: formulário com Server Action, estado de erro e acessibilidade

Redação própria a partir de V-45 (formulários acessíveis, WCAG 3.3.1 a 3.3.4) e V-46 (`useActionState` e Server Actions, React 19.3 e Next.js 16.4.0, lidos em 2026-10-10). Os exemplos usam Zod; Valibot e outros servem. Confira a API de validação da versão instalada (Zod 3 e 4 diferem em alguns helpers; `issues` existe nas duas). Os helpers `getSession` e `atualizarPerfil` são nomes de exemplo: use os do projeto.

## Sumário

1. O que está errado no caso comum
2. Server Action correta
3. Componente de formulário acessível
4. Recurso específico com `bind` e autorização
5. Resumo de erros quando há vários campos
6. Atualização otimista, com cuidado
7. Checklist de revisão do formulário

## 1. O que está errado no caso comum

```tsx
// Ruim: validação só no cliente, ação sem auth, erro lançado, userId em campo hidden.
'use server';
export async function salvarPerfil(formData: FormData) {
  const userId = formData.get('userId') as string;   // vem do HTML: o usuário pode trocar
  const email = formData.get('email') as string;
  if (!email.includes('@')) throw new Error('E-mail inválido'); // vai ao Error Boundary, sem ligação ao campo
  await atualizarPerfil(userId, { email });
}
```

Problemas: qualquer pessoa pode chamar a action com outro `userId` (sem autenticação nem autorização); a validação é fraca e o erro esperado vira exceção; a mensagem não diz como corrigir; nada liga o erro ao campo; o formulário não tem estado de envio. A regra do Next é conferir autenticação e autorização dentro de cada Server Action, mesmo em página protegida (V-46).

## 2. Server Action correta

```ts
// app/perfil/actions.ts
'use server';

import { z } from 'zod'; // ou Valibot; confirme a API da versão instalada
import { getSession } from '@/lib/session';          // exemplo: helper de sessão do projeto
import { atualizarPerfil } from '@/lib/perfil';      // exemplo: camada de serviço do projeto

const PerfilSchema = z.object({
  nome: z.string().trim().min(2, 'Informe seu nome com pelo menos 2 letras.'),
  email: z.string().trim().email('Informe um e-mail no formato nome@dominio.com.'),
});

export type PerfilState = {
  values?: { nome: string; email: string };
  errors?: Partial<Record<'nome' | 'email' | 'form', string>>;
  ok?: boolean;
};

export async function salvarPerfil(_anterior: PerfilState, formData: FormData): Promise<PerfilState> {
  // 1) Autenticação e autorização na primeira linha.
  const sessao = await getSession();
  if (!sessao) return { errors: { form: 'Sua sessão expirou. Entre novamente para salvar.' } };

  // 2) O usuário vem da sessão; o formulário só traz o que o usuário pode editar.
  const values = {
    nome: String(formData.get('nome') ?? ''),
    email: String(formData.get('email') ?? ''),
  };

  // 3) Validação no servidor; erro esperado volta como estado, não como exceção.
  const parsed = PerfilSchema.safeParse(values);
  if (!parsed.success) {
    const errors: NonNullable<PerfilState['errors']> = {};
    for (const issue of parsed.error.issues) {
      const campo = issue.path[0];
      if (campo === 'nome' || campo === 'email') errors[campo] ??= issue.message;
    }
    return { values, errors };
  }

  // 4) Só erro inesperado lança (vai ao Error Boundary e cancela ações em fila).
  await atualizarPerfil(sessao.userId, parsed.data);
  return { values: parsed.data, ok: true };
}
```

Pontos: com `useActionState`, a action recebe o estado anterior como primeiro argumento e o `FormData` como segundo; o estado e o payload precisam ser serializáveis; chamadas ficam em fila e rodam em sequência (V-46). A mensagem de e-mail diz como corrigir (WCAG 3.3.3). O erro de permissão ("sessão expirou") também é estado, para o usuário não perder o rascunho.

## 3. Componente de formulário acessível

```tsx
// app/perfil/PerfilForm.tsx
'use client';

import { useActionState } from 'react';
import { salvarPerfil, type PerfilState } from './actions';

const inicial: PerfilState = {};

interface PerfilFormProps {
  /** valores atuais do perfil, vindos do servidor */
  nome: string;
  email: string;
}

export function PerfilForm({ nome, email }: PerfilFormProps) {
  const [state, formAction, isPending] = useActionState(salvarPerfil, inicial);
  const valores = state.values ?? { nome, email };

  return (
    <form action={formAction}>
      {/* regiões vivas existem no DOM antes da mensagem */}
      <p role="status">{state.ok ? 'Perfil salvo.' : ''}</p>
      <p role="alert">{state.errors?.form ?? ''}</p>

      <label htmlFor="nome">Nome</label>
      <input
        id="nome" name="nome" defaultValue={valores.nome} required autoComplete="name"
        aria-invalid={state.errors?.nome ? true : undefined}
        aria-describedby={state.errors?.nome ? 'nome-erro' : undefined}
      />
      {state.errors?.nome && <p id="nome-erro">Erro: {state.errors.nome}</p>}

      <label htmlFor="email">E-mail</label>
      <input
        id="email" name="email" type="email" defaultValue={valores.email} required autoComplete="email"
        aria-invalid={state.errors?.email ? true : undefined}
        aria-describedby={state.errors?.email ? 'email-erro' : undefined}
      />
      {state.errors?.email && <p id="email-erro">Erro: {state.errors.email}</p>}

      <button type="submit" disabled={isPending}>
        {isPending ? 'Salvando...' : 'Salvar'}
      </button>
    </form>
  );
}
```

Decisões e por quê:

- `required` e `type="email"` dão validação nativa no cliente; a do servidor é a que vale (V-45, item 8).
- `defaultValue` vem do estado devolvido: o React 19 limpa campos não controlados de `<form action>` depois da Action, e sem isso o usuário perde o que digitou quando há erro (Inferido; confirme na versão instalada).
- O prefixo "Erro:" evita que a cor seja o único sinal (V-45, item 5).
- `aria-invalid` e `autocomplete` são prática comum; sua base primária não foi lida em VALIDATED: confirme no W3C (Não verificável ali).
- Funcionar antes da hidratação: a página lida não afirma isso; teste com JavaScript desligado na versão instalada antes de prometer (Suposição).
- Foco após erro: mover o foco para o primeiro campo inválido ou para o resumo é recomendável e Inferido; faça com `ref` e um Effect que sincroniza o foco do DOM, que é um uso legítimo de Effect.

## 4. Recurso específico com `bind` e autorização

```ts
// actions.ts
export async function excluirPedido(pedidoId: string, _anterior: { erro?: string }, _fd: FormData) {
  const sessao = await getSession();
  if (!sessao) return { erro: 'Sua sessão expirou.' };
  if (!(await podeExcluirPedido(sessao.userId, pedidoId))) {      // autorização do recurso, no servidor
    return { erro: 'Você não tem permissão para excluir este pedido.' };
  }
  await removerPedido(pedidoId);
  return {};
}
```

```tsx
// no componente cliente
const excluir = excluirPedido.bind(null, pedido.id);  // argumento fixo, em vez de <input type="hidden">
const [state, action, isPending] = useActionState(excluir, {});
```

`bind` evita colocar o id em HTML editável, mas o id continua vindo do cliente: por isso a autorização do recurso acontece dentro da action. Para ações destrutivas, ofereça confirmação ou reversão (WCAG 3.3.4).

## 5. Resumo de erros quando há vários campos

Com vários erros, anuncie uma vez: um resumo com a quantidade e uma lista de links para os campos, em vez de um `aria-live` por campo (V-45).

```tsx
{erros.length > 0 && (
  <div role="alert" id="resumo-erros" tabIndex={-1} ref={resumoRef}>
    <p>{erros.length} {erros.length === 1 ? 'campo precisa' : 'campos precisam'} de correção:</p>
    <ul>
      {erros.map((e) => (
        <li key={e.campo}><a href={`#${e.campo}`}>{e.mensagem}</a></li>
      ))}
    </ul>
  </div>
)}
```

Mover o foco para o resumo ao enviar com erro (`resumoRef.current?.focus()` dentro de um Effect que depende do número de erros) é Inferido; teste com leitor de tela.

## 6. Atualização otimista, com cuidado

`useOptimistic` mostra o resultado esperado enquanto a Action roda. Use só quando houver reversão clara: a lista volta ao estado real se a action falhar, o item tem identificador temporário e a mensagem de falha diz o que aconteceu. Não use para saldo, estoque ou valor financeiro apresentado como confirmado sem regra explícita (brain-of-agent, `frontend-e-estado.md`).

## 7. Checklist de revisão do formulário

- [ ] Auth e autorização na primeira linha de cada action; usuário da sessão, não de `hidden`.
- [ ] Schema no servidor com `safeParse`; erro esperado devolvido como estado.
- [ ] `<label for>` visível, instrução e erro por `aria-describedby`, erro em texto que diz como corrigir.
- [ ] Cor não é o único sinal; resumo único quando há vários erros.
- [ ] Botão com estado de envio (`isPending`); proteção contra duplo envio no servidor.
- [ ] Campos repopulados após erro; sessão expirada não apaga o rascunho.
- [ ] Teste do caminho de erro e do sucesso; envio só com teclado.
- [ ] Rótulos epistêmicos no relatório: o que foi executado e o que foi só lido.
