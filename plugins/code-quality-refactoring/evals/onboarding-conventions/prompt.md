---
name: onboarding-conventions
description: "Mede o mapeamento de convenções com evidência por contagem: Result em dois módulos e exceções em um, rótulo Inferido para uma ou duas ocorrências, divergência reportada sem escolher lado, somente leitura."
tags: [code-quality-refactoring, codebase-onboarding, evidence, read-only]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Lista a convenção Result com arquivos de exemplo rotulada Inferido por ter apenas duas ocorrências nos arquivos colados, aponta a divergência em billing/charge.ts sem escolher lado, diz que quatro arquivos não provam uma convenção do projeto e não altera nada."
model: sonnet
---
Acabei de entrar no time e só tenho esses poucos arquivos aqui do serviço de pedidos (TypeScript). Quais as convenções de tratamento de erro daqui? Quero seguir o padrão certo no meu primeiro PR.

```text
src/
  shared/result.ts
  users/service.ts
  orders/service.ts
  billing/charge.ts
```

`src/shared/result.ts`:

```ts
export type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
export const ok = <T>(value: T): Result<T, never> => ({ ok: true, value });
export const err = <E>(error: E): Result<never, E> => ({ ok: false, error });
```

`src/users/service.ts`:

```ts
import { Result, ok, err } from '../shared/result';

export function findUser(id: string): Result<User, 'NOT_FOUND'> {
  const u = users.get(id);
  return u ? ok(u) : err('NOT_FOUND');
}
```

`src/orders/service.ts`:

```ts
import { Result, ok, err } from '../shared/result';

export function placeOrder(cmd: PlaceOrder): Result<Order, OrderError> {
  if (cmd.items.length === 0) return err({ kind: 'EMPTY_ORDER' });
  return ok(create(cmd));
}
```

`src/billing/charge.ts`:

```ts
export async function charge(orderId: string, cents: number): Promise<Receipt> {
  if (cents <= 0) throw new BillingError('INVALID_AMOUNT');
  const res = await gateway.charge(orderId, cents);
  if (!res.ok) throw new BillingError('GATEWAY_DECLINED');
  return res.receipt;
}
```
