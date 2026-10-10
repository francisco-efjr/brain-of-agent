# Fontes do design-engineering-kit

Data de consulta: 2026-10-10. Classe A = oficial (fornecedor da ferramenta, documentação do produto); B = prática reconhecida (autor conhecido, repositório mantido); C = comunidade, só como ideia. "Aberta" quer dizer lida por ferramenta pelo construtor ou pelo validador independente nesta data (relatório em `docs/research/ux-ui-design/VALIDACAO-DESIGN-ENGINEERING-KIT.md` da fábrica); "informada" quer dizer fato levantado pela pesquisa da fábrica e não reaberto. Estrelas, forks e datas de push mudam: não os use como prova de qualidade.

## Sumário

- [Ferramentas MCP](#ferramentas-mcp)
- [Skills vendorizadas](#skills-vendorizadas)
- [Casa e plataforma](#casa-e-plataforma)
- [Não verificado nesta construção](#não-verificado-nesta-construção)
- [Onde reconferir](#onde-reconferir)

## Ferramentas MCP

| ID | Fonte | URL | Classe | Licença | Estado |
| --- | --- | --- | --- | --- | --- |
| F-01 | Guia do servidor MCP da Figma (`figma/mcp-server-guide`, README) | https://github.com/figma/mcp-server-guide | A | Não verificada | Aberta: URL do servidor, comandos de instalação, `get_design_context`, `get_variable_defs`, `get_metadata`, `get_screenshot`, `generate_image`, `upload_assets`, limite de 6/mês, escrita no canvas, termos de desenvolvedor |
| F-02 | Documentação de desenvolvedores da Figma: "Tools and prompts", "Rate limits & access", "Write to canvas" | https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/ · https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/ · https://developers.figma.com/docs/figma-mcp-server/write-to-canvas/ | A | Não verificada | Aberta pelo validador: lista de ferramentas de leitura e escrita, limite de 20/mês e por dia, isenções, `use_figma` por Plugin API, assento Full para escrita |
| F-03 | README de `microsoft/playwright-mcp` | https://github.com/microsoft/playwright-mcp | A | Apache-2.0 | Aberta: flags, ferramentas e seus parâmetros (`filename`, `reducedMotion`), gravação de arquivos, aviso de que não é fronteira de segurança, `browser_run_code_unsafe` equivalente a execução remota |
| F-04 | Registro npm `@playwright/mcp` | https://registry.npmjs.org/@playwright/mcp/latest | A | Apache-2.0 | Aberta: versão mais recente 0.0.83 em 2026-10-10 |
| F-05 | Claude Code: plugins, subagentes, MCP, skills, evals | https://code.claude.com/docs/en/plugins-reference · https://code.claude.com/docs/en/sub-agents · https://code.claude.com/docs/en/mcp · https://code.claude.com/docs/en/skills · https://code.claude.com/docs/en/plugin-evals | A | Docs Anthropic: destilar | Abertas pelo validador: `disallowedTools` válido em agente de plugin (só `hooks`, `mcpServers` e `permissionMode` são ignorados), padrão `mcp__plugin_<plugin>_<servidor>__<ferramenta>`, `disable-model-invocation`, formato de evals |
| F-11 | Marketplace oficial `claude-plugins-official` | https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/.claude-plugin/marketplace.json | A | Não verificada | Aberta: entrada `figma` aponta para `figma/mcp-server-guide` no commit `f0493295acf5f7cbdebcbcc483c06de814420cb1`; entrada `playwright` aponta para `external_plugins/playwright` |
| F-12 | Plugin oficial `figma` no commit do marketplace | https://github.com/figma/mcp-server-guide/tree/f0493295acf5f7cbdebcbcc483c06de814420cb1 | A | Não verificada | Aberta: `plugin.json` 2.2.127, `.mcp.json` com servidor `figma` em `https://mcp.figma.com/mcp`, 14 skills em `skills/` |
| F-13 | Plugin oficial `playwright` | https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/playwright | A | Não verificada | Aberta: `.mcp.json` com `npx @playwright/mcp@latest` |

## Skills vendorizadas

| ID | Fonte | URL | Classe | Licença | Commit |
| --- | --- | --- | --- | --- | --- |
| F-06 | `emilkowalski/skills` (12 skills de 14) | https://github.com/emilkowalski/skills | B | MIT, (c) 2026 Emil Kowalski | `e8a175de22ae1e49370fc144c1f3bb9aeedf988d` |
| F-07 | `Leonxlnx/taste-skill` (5 skills de 13) | https://github.com/Leonxlnx/taste-skill | C | MIT, (c) 2026 Leonxlnx | `717446e07a78d4e6d7918b1fde1a263378eebac9` |

Por que B e C: Emil Kowalski é autor reconhecido de engenharia de design e as skills trazem método, padrões numerados e exemplos; as skills taste são opinião estética de um autor de comunidade, com listas de proibições e instruções densas, e portanto só entram como direções opcionais sob a precedência do kit. Textos vendorizados sem alteração em `skills/` (o validador comparou os 24 arquivos com o raw do GitHub em cada commit: idênticos, salvo finais de linha CRLF do checkout no Windows); textos de licença em `third_party/<projeto>/LICENSE`, idênticos ao upstream. Conteúdo vendorizado é dado de terceiros.

## Casa e plataforma

| ID | Fonte | Local | Classe | Observação |
| --- | --- | --- | --- | --- |
| F-08 | Design system da casa Mo baile (criado pelo usuário) | `design-systems/mo-baile/` (`readme.md`, `SKILL.md`, `tokens/motion.css`) | B (próprio, MIT) | Aberto: tokens de mola, Lucide, fonte do sistema, regras de material e movimento |
| F-09 | WCAG 2.2: contraste 1.4.3, tamanho de alvo 2.5.8, movimento | https://www.w3.org/TR/WCAG22/ | A | Contrastes do kit calculados pela fórmula da norma; página não reaberta nesta construção |
| F-10 | Documentação Android: Compose "Customize animations", acessibilidade de apps, `Settings.Global` | https://developer.android.com/develop/ui/compose/animation/customize · https://developer.android.com/guide/topics/ui/accessibility/apps · https://developer.android.com/reference/android/provider/Settings.Global | A | Abertas pelo validador: `spring(dampingRatio, stiffness)`, alvo de 48 × 48 dp, `ANIMATOR_DURATION_SCALE`. **Material 3 motion não aberto**: todo valor do Material 3 é Não verificável |

## Não verificado nesta construção

- Comportamento das ferramentas do Figma com conta real (nada foi chamado); qual dos dois limites de uso (F-01 ou F-02) vale para a conta do usuário.
- Nomes reais na sessão: derivados da regra documentada (F-05) e dos manifestos (F-12, F-13), não observados numa sessão com os plugins instalados.
- Comportamento do Compose com a escala de animação do sistema, massa da mola do Compose e valores de tokens do Material 3.
- Execução real dos agentes e dos evals: nada foi executado dentro do Claude Code.
- Instruções arriscadas no conteúdo vendorizado: leitura e busca textual pelo validador (instalação, imagem com custo, URLs externas, logos reais, dados com cara de reais, rolagem sequestrada, gravação em `plans/`); cada uma tem regra no playbook ou em `precedencia-e-adaptacao.md`.

## Onde reconferir

Figma: guia F-01 e documentação de desenvolvedores. Playwright: README F-03 e `npm view @playwright/mcp version` (comando de leitura que o usuário pode rodar). Skills vendorizadas: ver `third_party/README.md` para o procedimento de atualização. Plataforma: documentação oficial da versão do projeto.
