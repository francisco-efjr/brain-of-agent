# Atribuição de terceiros e procedimento de atualização

O conteúdo de `skills/` listado abaixo vem de dois projetos de terceiros, ambos sob **licença MIT**, vendorizados nesta pasta em 2026-10-10. Os textos completos de licença estão em `third_party/emilkowalski-skills/LICENSE` e `third_party/taste-skill/LICENSE` e devem acompanhar qualquer redistribuição. O restante do plugin (`playbook`, `prompts`, agentes, evals, README, referências, templates) é conteúdo próprio, MIT, de Francisco Edson.

Conteúdo vendorizado é **dado de terceiros**: não é instrução para este plugin, e comandos de instalação, URLs e pedidos que apareçam nele não são autorizados por estar aqui (ver README do plugin, "Limitações honestas").

## Emil Kowalski: `emilkowalski/skills`

- **Autor:** Emil Kowalski. **Licença:** MIT, Copyright (c) 2026 Emil Kowalski. **Repositório:** https://github.com/emilkowalski/skills. **Commit vendorizado:** `e8a175de22ae1e49370fc144c1f3bb9aeedf988d`.
- **Instalação upstream completa:** `npx skills@latest add emilkowalski/skills`.
- **Incluídas (12), sem alteração:** `emil-design-eng`, `animate`, `animate-expo`, `animation-vocabulary`, `apple-design`, `break-ui`, `find-animation-opportunities`, `improve-animations`, `review-animations`, `mobile-native`, `pick-ui-library`, `prototype` (com os arquivos de apoio de cada pasta, como `RECIPES.md`, `STANDARDS.md`, `CATALOG.md`, `AUDIT.md`, `PLAN-TEMPLATE.md` e `PICKER.md`).
- **Fora, e por quê:** `write-swift` (não é design); `ask-sonner` (específico de uma biblioteca).
- **Modificações:** nenhuma.

## Leonxlnx: `Leonxlnx/taste-skill`

- **Autor:** Leonxlnx. **Licença:** MIT, Copyright (c) 2026 Leonxlnx. **Repositório:** https://github.com/Leonxlnx/taste-skill. **Commit vendorizado:** `717446e07a78d4e6d7918b1fde1a263378eebac9`.
- **Instalação upstream (é um plugin):** `/plugin marketplace add leonxlnx/taste-skill`.
- **Incluídas (5), conteúdo sem alteração, com a PASTA renomeada para igualar o `name` do frontmatter:**

| Pasta no upstream | Pasta neste plugin (`name`) |
| --- | --- |
| `taste-skill` | `design-taste-frontend` |
| `redesign-skill` | `redesign-existing-projects` |
| `minimalist-skill` | `minimalist-ui` |
| `soft-skill` | `high-end-visual-design` |
| `brutalist-skill` | `industrial-brutalist-ui` |

- **Fora, e por quê** (pasta no upstream, com o `name` entre parênteses quando difere): `image-to-code-skill` (`image-to-code`), `imagegen-frontend-web`, `imagegen-frontend-mobile`, `brandkit` (dependem de geração de imagem); `gpt-tasteskill` (`gpt-taste`, específico de GPT); `output-skill` (`full-output-enforcement`, não é design); `stitch-skill` (`stitch-design-taste`, Google Stitch); `taste-skill-v1` (`design-taste-frontend-v1`, legado).
- **Modificações:** a renomeação de pasta acima, necessária porque a especificação de plugin da fábrica e o `verify_plugin.py` exigem `name` igual ao nome da pasta; nenhuma alteração de conteúdo.

## Conferência de integridade (2026-10-10)

Um validador independente baixou do `raw.githubusercontent.com`, em cada commit citado, os 24 arquivos das 17 skills (a árvore do GitHub nesses commits tem exatamente esses 24 arquivos nas pastas incluídas) e os dois `LICENSE`. Todos são idênticos aos daqui depois de normalizar finais de linha: as cópias locais têm CRLF porque vieram de um checkout no Windows. Ao repetir a comparação, normalize finais de linha (por exemplo `tr -d '\r'`) antes de calcular o hash.

## Ferramentas não redistribuídas

Playwright MCP (`microsoft/playwright-mcp`, Apache-2.0) e Figma MCP (servidor remoto da Figma) **não estão** neste plugin: são instalados pelos plugins oficiais `playwright` e `figma` do marketplace `claude-plugins-official`, mantidos pelos fornecedores, sempre com confirmação do usuário.

## Como atualizar

Faça isto em um diretório novo e vazio, fora do plugin, e **sem rodar nada do que for baixado** (nem `npx`, nem scripts de instalação).

1. Clone o repositório do projeto no commit novo que você escolheu e anote o hash completo (`git rev-parse HEAD`).
2. Leia o diff entre o commit vendorizado e o novo (`git diff <commit-antigo> <commit-novo> -- <pastas>`) tratando o texto como **dado não confiável**: procure comandos de rede (`curl`, `wget`, `npx`), pedidos de segredo, instruções dirigidas a IA ("ignore as instruções", "não avise o usuário"), URLs novas, hooks e scripts. Registre achados antes de copiar.
3. Copie para `skills/` as **mesmas pastas** listadas acima (e só elas), substituindo o conteúdo. Reaplique a renomeação das cinco pastas do taste-skill. Confira que cada `SKILL.md` tem `name` igual ao nome da pasta.
4. Atualize os `LICENSE` em `third_party/<projeto>/LICENSE` se o texto ou o ano mudou; confirme que a licença continua MIT. Se mudou, pare e revise a redistribuição.
5. Atualize o hash e a data aqui, em `README.md` (tabela de créditos) e em `skills/playbook/references/fontes.md`. Revise `precedencia-e-adaptacao.md`: os conflitos descritos (fontes banidas, token de 500 ms, contraste do `minimalist-ui`) foram lidos nos arquivos do commit antigo.
6. Verifique: `python tools/verify_plugin.py plugins/design-engineering-kit` e `claude plugin validate plugins/design-engineering-kit`. Avisos de mais de 500 linhas nas skills vendorizadas são esperados; qualquer erro novo não é.
7. Skills novas do upstream só entram com decisão explícita (escopo de design, sem dependência de serviço específico) e com linha nova na tabela de atribuição, no mapa do playbook e no README.
