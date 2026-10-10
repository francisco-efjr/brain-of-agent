---
name: skill-nao-dispara
description: "Mede se o plugin reescreve a description de uma skill que nunca ativa (o quê, quando, gatilhos PT-BR e EN, quando não), monta 20 consultas com quase-acertos negativos e divisão 60/40, e diz que não rodou o teste."
tags: [llm-ai-agents, instruction-authoring, skills]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Reescreve a description com o que a skill faz, quando usar, gatilhos concretos em português e inglês e quando não usar, sem CAPS; monta 20 consultas (metade quase-acertos negativos) com divisão 60/40 e diz que não executou o teste de disparo."
model: sonnet
---
Criei uma skill do Claude Code para trabalhar com PDFs (extrair tabelas, preencher formulários, juntar arquivos) e ela nunca ativa sozinha quando eu peço, por exemplo, "extrai as tabelas desse relatório.pdf". Só funciona quando chamo pelo nome. Esse é o frontmatter e o começo do arquivo:

```markdown
---
name: pdf-helper
description: Helps with PDFs
---

# PDF helper

Use the scripts in scripts/ to read and edit PDF files. Always be careful with encrypted files.
```

Arruma a description e me diz como eu testo se ela passa a ativar direito, sem ativar quando não deve.
