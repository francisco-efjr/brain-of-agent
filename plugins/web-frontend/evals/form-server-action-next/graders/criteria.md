---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta o risco principal: `userId` vem de um campo `hidden` controlável pelo cliente, então qualquer usuário pode alterar o e-mail de outro (falha de autorização); a correção obtém o usuário da sessão no servidor e não de `hidden`, e a verificação de autenticação e autorização fica na primeira linha da action, mesmo em página autenticada. Não inventa uma biblioteca de autenticação específica: usa um ponto genérico (por exemplo `getSession()` do projeto) ou pergunta.
2. Valida no servidor com schema Zod e `safeParse` (o usuário informou Zod); em falha devolve `{ errors }` como estado em vez de lançar; lança apenas para erro inesperado. Diz que a validação do cliente (`onSubmit` com `alert`) é só experiência e que `required` e `type="email"` nativos são preferíveis ao `alert`.
3. Reescreve o componente com `useActionState` (`[state, formAction, isPending]`), a action com assinatura `(prevState, formData)`, botão com `disabled={isPending}` e `type="submit"`.
4. Torna o erro acessível: `<label>` real para o campo (placeholder não substitui rótulo), mensagem de erro em texto que diz como corrigir, ligada ao campo por `aria-describedby`, e anunciada (região `aria-live="polite"` ou `role="status"`, ou resumo único).
5. Trata versão como premissa verificável: diz que as regras valem para Next 16.x e React 19.x conforme informado e manda conferir `package.json`; se mencionar comportamento antes da hidratação, rotula Suposição ou Não verificado.
6. Não afirma ter executado o projeto, o type-check ou os testes; indica o que falta verificar.
FAIL if qualquer um ocorrer: mantém a validação só no cliente; mantém o `userId` do `hidden` como fonte de autoridade; mantém o `throw` como forma de devolver erro de validação ao usuário; ignora a acessibilidade da mensagem de erro; afirma ter testado o formulário; usa API que não existe nas versões informadas sem avisar.
