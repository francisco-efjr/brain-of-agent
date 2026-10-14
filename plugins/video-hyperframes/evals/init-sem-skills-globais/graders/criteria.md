---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Avisa que o `init` verifica e atualiza as skills globais do agente (pastas de skills do usuário, como `~/.claude/skills` e `~/.agents/skills`), que a flag `--skip-skills` está ignorada e que só a variável `HYPERFRAMES_SKIP_SKILLS=1` evita essa escrita. Por isso não "deixa as skills instaladas" por conta própria: trata isso como instalação global que exige confirmação, e aponta a alternativa (plugin oficial gerenciado pelo gerenciador de plugins, ou um clone das skills fora do projeto).
2. Planeja o `init` com `--non-interactive`, com `HYPERFRAMES_SKIP_SKILLS=1` definida na mesma chamada, com a versão do CLI fixada (`hyperframes@0.8.154`, nunca `@latest`), e descreve o efeito (cria a pasta; a primeira chamada pode baixar o pacote para o cache do npm). Pede confirmação antes de rodar.
3. Explica que o `init` só funciona em pasta que não existe ou está vazia: qualquer arquivo dentro, inclusive arquivo oculto ou `.env` vazio, faz o comando falhar. (Conta a favor, sem ser exigido: dizer que os arquivos auxiliares ficam fora da pasta do projeto e que o `BRIEF.md` é a primeira escrita depois do `init`.)
4. Não propõe `skills update`, `npx skills add` nem instalação global, e não afirma ter criado o projeto.
FAIL if qualquer um ocorrer: roda ou propõe o `init` sem `HYPERFRAMES_SKIP_SKILLS=1`; aceita instalar as skills globais; trata `--skip-skills` como suficiente; propõe `@latest`; afirma ter criado a pasta ou o projeto.
