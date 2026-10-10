# Bloco `## Deploy Configuration` para o CLAUDE.md do projeto

<!--
Modelo para a skill deploy-infra (passo 0) e para o SN-08. Regras:
1. Proponha o bloco ao usuário, mostre o que foi detectado e peça confirmação ANTES de gravar.
2. O CLAUDE.md do projeto é a fonte de verdade; não crie arquivo de configuração separado.
3. Nenhum segredo, token, chave ou senha no bloco. Use "none" quando o projeto não faz deploy.
4. Os comandos de status e health check são repetidos nos dois lugares (campos e "Custom deploy hooks")
   com o mesmo valor.
5. CLIs de plataforma são opcionais: sem a CLI, use verificação por URL de saúde.
6. Idempotente: gravar de novo substitui o bloco anterior.
Inspirado em gstack setup-deploy (MIT, Garry Tan); redação própria, sem cópia em bloco.
-->

Bloco a propor (preencha com o que foi detectado ou confirmado pelo usuário):

```markdown
## Deploy Configuration
- Platform: [plataforma de deploy do projeto, ex.: AWS ECS Fargate | Kubernetes (cluster X) | Fly.io | none]
- Production URL: [URL ou none]
- Deploy workflow: [arquivo de workflow, ex.: .github/workflows/deploy.yml | "auto-deploy on push" | none]
- Deploy status command: [comando de leitura, ex.: kubectl rollout status deploy/api -n app | "HTTP health check"]
- Merge method: [squash | merge | rebase]
- Project type: [web app | API | CLI | library | infra]
- Post-deploy health check: [URL ou comando que prova a REVISÃO no ar]

### Custom deploy hooks
- Pre-merge: [comando ou none]
- Deploy trigger: [comando ou "automatic on push to <branch padrão>"]
- Deploy status: [mesmo valor de "Deploy status command"]
- Health check: [mesmo valor de "Post-deploy health check"]
```

Como detectar a plataforma (somente leitura): arquivos de configuração presentes (`fly.toml`, `render.yaml`, `vercel.json`, `netlify.toml`, `Procfile`, `railway.json`, `Dockerfile`, `charts/`, `*.tf`), workflows em `.github/workflows` e o tipo do projeto. Branch padrão: `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`.

Verificação após gravar (somente leitura): o health check configurado responde e **identifica a versão** (não apenas HTTP 200). Se a URL não responder, registre "UNREACHABLE" e pergunte; não invente valores.

Por que fixar a plataforma: o modelo tem preferência por padrão (na pesquisa Amplifying, fev/2026, escolheu Vercel em 86 de 86 respostas de frontend); registrar a plataforma evita sugestões de migração não pedidas (V-26).
