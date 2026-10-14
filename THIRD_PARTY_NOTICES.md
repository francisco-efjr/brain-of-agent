# Material de terceiros

## gstack

- Origem: https://github.com/garrytan/gstack
- Créditos: Garry Tan e contribuidores.
- Copyright principal: Copyright (c) 2026 Garry Tan.
- Licença MIT preservada em [vendor/gstack/LICENSE](vendor/gstack/LICENSE).
- Versão 1.91.27, commit `c285d88b90d39116ccfa2b901f80ea0fce0b26eb`.
- Importação em 05/10/2026.

Todos os arquivos versionados foram copiados sem alterações, preservando
conteúdo, executabilidade e symlinks. Não foram copiados `.git` e artefatos
não versionados. Inventário: [registry/gstack-upstream.json](registry/gstack-upstream.json).

O gstack também inclui material derivado Apache-2.0, com créditos a impeccable
(Paul Bakaus) e à especificação DESIGN.md (Google LLC). Avisos preservados em
[vendor/gstack/NOTICE.md](vendor/gstack/NOTICE.md); licença em
[vendor/gstack/licenses/Apache-2.0.txt](vendor/gstack/licenses/Apache-2.0.txt).
A licença própria não substitui licenças de terceiros.

## Skills de design engineering (plugin `design-engineering-kit`)

Skills copiadas sem alteração de conteúdo para `plugins/design-engineering-kit/skills/`.
Atribuição, lista exata e procedimento de atualização em
[plugins/design-engineering-kit/third_party/README.md](plugins/design-engineering-kit/third_party/README.md).

- **emilkowalski/skills**: https://github.com/emilkowalski/skills. Copyright (c) 2026 Emil Kowalski, licença MIT
  preservada em [third_party/emilkowalski-skills/LICENSE](plugins/design-engineering-kit/third_party/emilkowalski-skills/LICENSE).
  Commit `e8a175de22ae1e49370fc144c1f3bb9aeedf988d`. São 12 skills: emil-design-eng, animate,
  animate-expo, animation-vocabulary, apple-design, break-ui, find-animation-opportunities,
  improve-animations, review-animations, mobile-native, pick-ui-library e prototype.
- **Leonxlnx/taste-skill**: https://github.com/Leonxlnx/taste-skill. Copyright (c) 2026 Leonxlnx, licença MIT
  preservada em [third_party/taste-skill/LICENSE](plugins/design-engineering-kit/third_party/taste-skill/LICENSE).
  Commit `717446e07a78d4e6d7918b1fde1a263378eebac9`. São 5 skills, com a pasta renomeada para
  igualar o `name`: design-taste-frontend, redesign-existing-projects, minimalist-ui,
  high-end-visual-design e industrial-brutalist-ui.

Figma MCP e Playwright MCP (Apache-2.0, Microsoft) não são redistribuídos aqui. O kit orienta a
instalação dos plugins oficiais `figma@claude-plugins-official` e `playwright@claude-plugins-official`.

## agent-skills (plugin `engineering-lifecycle`)

- Origem: https://github.com/addyosmani/agent-skills
- Créditos: Addy Osmani (criador), Federico Bartoli e Joan León (colaboradores) e contribuidores.
- Copyright (c) 2025 Addy Osmani. Licença MIT preservada em
  [plugins/engineering-lifecycle/third_party/addyosmani-agent-skills/LICENSE](plugins/engineering-lifecycle/third_party/addyosmani-agent-skills/LICENSE).
- Commit `aeac41d4d005999432bb7312f7ff06383a91d59d`, plugin upstream 0.6.13, importado em 13/10/2026.
- 68 arquivos copiados byte a byte (25 skills, 7 checklists em `references/`, 4 personas em `agents/`, 5 evals,
  `docs/agents.md` e a licença), com inventário sha256 em
  [inventory.json](plugins/engineering-lifecycle/third_party/addyosmani-agent-skills/inventory.json).
- Única modificação: nos 9 comandos copiados de `.claude/commands/`, o prefixo de skill `agent-skills:` virou
  `engineering-lifecycle:` (8 arquivos afetados), para resolver dentro deste plugin. Detalhes e procedimento de
  atualização em [third_party/README.md](plugins/engineering-lifecycle/third_party/addyosmani-agent-skills/README.md).
- Hooks, `evals/cases`, `docs/` de instalação e adaptadores de outros hosts não foram redistribuídos.

## Playwright (plugin `qa-playwright`)

- Origem: https://github.com/microsoft/playwright (commit `b536a63`, release v1.64.0), https://github.com/microsoft/playwright-mcp (v0.0.83) e https://github.com/microsoft/playwright-cli (v0.1.22), lidos em 13/10/2026.
- Licença Apache-2.0. "Portions Copyright (c) Microsoft Corporation" e "Portions Copyright 2017 Google Inc." (`microsoft/playwright`, que também cita no NOTICE código derivado do Puppeteer, Apache-2.0); "Copyright (c) Microsoft Corporation" (`playwright-mcp`, `playwright-cli`).
- Nenhum arquivo foi copiado. O plugin destila a documentação com redação própria e usa trechos curtos de configuração e de código (no máximo cerca de 40 linhas) com a atribuição "Microsoft Playwright, Apache-2.0". Fontes e classes em [fontes.md](plugins/qa-playwright/skills/playbook/references/fontes.md).
- O plugin não traz `.mcp.json` nem instala nada: orienta usar `npx playwright cli` e `npx playwright mcp` do `@playwright/test` com versão fixada no projeto.
