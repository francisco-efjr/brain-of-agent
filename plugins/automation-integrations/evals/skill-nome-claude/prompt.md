---
name: skill-nome-claude
description: "Mede se o plugin diagnostica uma skill que nunca dispara (nome reservado, description vaga, corpo grande, sem referências, efeito colateral sem proteção) e propõe calibração."
tags: [automation-integrations, authoring-plugin-skills, skill, description, positivo]
runs: 3
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
expected_outcome: "Aponta nome com palavra reservada, description sem gatilho, corpo acima de 500 linhas sem references, sem seção de gotchas e efeito de deploy sem disable-model-invocation, e propõe description em português e inglês com calibração de 20 consultas."
---
Criei uma skill chamada `claude-helper` para o meu time e ela nunca dispara sozinha, só funciona quando eu digito o comando. O arquivo `.claude/skills/claude-helper/SKILL.md` tem 700 linhas e todo o conteúdo está nele, não existe pasta de referências. O começo é este:

```markdown
---
name: claude-helper
description: Ajuda com automações
---

# Claude Helper

Você é um assistente muito útil. Sempre faça o melhor trabalho possível.

## Como funciona
1. Entenda o que o usuário quer.
2. Gere o script de automação.
3. Rode `./deploy.sh producao` para publicar o resultado.
4. Avise o usuário.

(... mais 680 linhas de exemplos de scripts de automação, regras de estilo e listas de ferramentas ...)
```

A skill também não tem nenhuma seção de problemas conhecidos. O que está errado e como eu faço ela disparar quando alguém do time pede para automatizar algo? Pode mostrar como deveria ficar o começo do arquivo.
