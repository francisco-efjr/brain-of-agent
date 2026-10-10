---
name: mudanca-trivial-negativo
description: Caso negativo de proporcionalidade que mede sobredisparo, verificando que uma troca de cor de uma linha, com o diff cabendo numa frase, é feita direto, sem entrevista, sem spec e sem acionar skill ou agente do plugin.
tags: [product-discovery-specs, negative, proportionality]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Troca a cor do fundo do botão primário de #1d4ed8 para #2563eb, mostra o diff, não faz perguntas de requisitos, não cria spec nem PRD e não aciona skill do plugin."
model: sonnet
---
Em Button.tsx troque o fundo do botão primário de #1d4ed8 para #2563eb. Segue o arquivo:

```tsx
type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'secondary';
};

export function Button({ children, variant = 'primary', ...props }: ButtonProps) {
  const base = 'px-4 py-2 rounded-md font-medium';
  const styles = {
    primary: `${base} bg-[#1d4ed8] text-white hover:bg-[#1e40af]`,
    secondary: `${base} bg-gray-100 text-gray-900`,
  };
  return (
    <button className={styles[variant]} {...props}>
      {children}
    </button>
  );
}
```
