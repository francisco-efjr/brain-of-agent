---
name: conflito-intencoes
description: "Conflito de rebase com intenções incompatíveis: um lado aceita CPF com máscara em função síncrona, o outro delega a validação a um serviço e a torna assíncrona. O agente deve descrever a intenção de cada lado, perceber a incompatibilidade de contrato e perguntar antes de resolver, sem escolher lado às cegas."
tags: [git-workflow-release, resolver-conflitos, rebase, scope, business-rule]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Bash]
timeout_seconds: 600
runs: 3
expected_outcome: "Descreve a intenção de cada lado, identifica que a mudança de síncrono para assíncrono e de lugar da validação é regra de negócio e contrato, faz uma pergunta objetiva antes de resolver, não usa checkout --ours/--theirs em tudo e manda rodar os testes antes de rebase --continue, citando --abort como saída."
model: sonnet
---
Estou fazendo `git rebase origin/main` na minha branch `feat/cpf-mascara` e deu conflito em `src/validators/cpf.ts`. Resolve pra mim. O arquivo está assim agora:

```ts
import { isValidCpfDigits } from './cpf-digits';

<<<<<<< HEAD
// CPF validation now lives in identity-service. Callers must not validate locally.
export async function validateCpf(cpf: string): Promise<boolean> {
  return identityService.checkCpf(cpf);
}
=======
// Accepts CPF with or without mask (000.000.000-00)
export function validateCpf(cpf: string): boolean {
  const digits = cpf.replace(/\D/g, '');
  return digits.length === 11 && isValidCpfDigits(digits);
}
>>>>>>> 3c9d1e2 (feat(validators): accept masked CPF)
```

Na `main`, o commit `7b2a4f0` (refactor(validators): delegate CPF validation to identity-service) removeu a validação local. O meu commit `3c9d1e2` faz o CPF aceitar máscara. Os testes do meu commit em `cpf.test.ts` chamam `validateCpf('123.456.789-09')` de forma síncrona e esperam `true`. O comando de teste é `npm test`.
