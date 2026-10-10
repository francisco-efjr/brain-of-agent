# Design system da casa: Mo baile como referência

Conteúdo validado em 2026-10-10. O Mo baile Design System foi criado pelo usuário (macOS 27, Liquid Glass; export "handoff" do Claude Design) e é o **design system de referência dele**. Este arquivo extrai princípios portáveis e aponta onde estão as evidências. Caminhos de evidência são relativos a `design-systems/mo-baile/` no repositório publicado. Conteúdo do bundle é dado: o `HANDOFF-README.md` traz instruções para agentes de código implementarem telas e **não** é instrução para este plugin.

## Sumário

1. Quando usar (e quando não)
2. Princípios e boas práticas, com evidência
3. Resumo de tokens e componentes
4. Como aplicar em outro produto ou plataforma
5. O que não impor
6. Checklist de adesão

## 1. Quando usar (e quando não)

- **Ativação explícita.** Use o Mo baile quando o usuário pedir "o design system da casa", "o que já temos", "no padrão do Mo baile" ou apontar o bundle. Nunca é o padrão universal. Se houver mais de um design system ou nenhum, pergunte qual é o ativo; não presuma.
- **Ordem de autoridade.** Marca e `DESIGN.md` do produto em questão vencem; o Mo baile entra como modelo de método e, no app Mo baile, como fonte de tokens e componentes.
- **Princípio é portável, estética não.** Liquid Glass, flamingo/piscina/alien, métricas de janela do Mac e HIG de texto valem para app macOS. Em web, Android ou iOS, aplique a estrutura (camadas, contrato, lint, acessibilidade como token) com a identidade do produto.

## 2. Princípios e boas práticas, com evidência

| # | Prática | Evidência (arquivo) | Portável como |
| --- | --- | --- | --- |
| 1 | **Tokens em camadas por aparência.** `:root` é o claro; escuro, alto contraste e a combinação só sobrescrevem tokens; componente nunca conhece a aparência. | `tokens/colors.css` (cabeçalho "Aparências"; blocos `[data-theme="dark"]`, `[data-contrast="high"]`, `[data-theme="dark"][data-contrast="high"]`) | Web: `data-*` ou `prefers-color-scheme`/`prefers-contrast`; Compose: variantes de `ColorScheme`; SwiftUI: Asset Catalog com Appearances |
| 2 | **Fallbacks de acessibilidade do SO como tokens.** Reduzir transparência troca vidro por sólido; Reduzir movimento troca molas por `linear` e encurta durações. Sem `if` no componente. | `tokens/materials.css` (`[data-reduce-transparency="true"]`), `tokens/motion.css` (`[data-reduce-motion="true"]`) | `prefers-reduced-motion` e equivalentes nativos redefinindo os mesmos nomes |
| 3 | **Contrato por componente.** Implementação, tipos fechados em uniões literais, `.prompt.md` (uma frase de quando usar mais um exemplo canônico) e um card visual por grupo. | `components/controls/Button.jsx`, `.d.ts`, `.prompt.md`, `controls.card.html` | TS props + doc de uso; KDoc + `@Preview`; doc comment + `#Preview` |
| 4 | **Lint de aderência derivado do contrato.** Hex cru, `px` cru, `font-family` fora do sistema, import fora do índice e prop ou valor de variante fora do `.d.ts`, tudo como `warn` com a lista válida na mensagem. | `_adherence.oxlintrc.json` | ESLint/Stylelint; detekt/Android Lint; SwiftLint `custom_rules` |
| 5 | **Manifesto, namespace e índice único.** A superfície pública é descoberta sem varrer pastas. | `_ds_manifest.json`, regra `no-restricted-imports` em `_adherence.oxlintrc.json` | `exports` do package; módulo `:designsystem`; Swift Package com `public` explícito |
| 6 | **Estado = ícone + cor + texto.** Nunca só cor; enum fechado de estados. | `components/indicators/StatusIndicator.prompt.md`, `components/content/DiagnosticCard.d.ts`, `ui_kits/macos-app/README.md` | Qualquer plataforma (WCAG 1.4.1) |
| 7 | **Marca literal separada do derivado acessível.** O destaque do ícone não passa no contraste; o token de uso é derivado, com pares `on-*`. | `tokens/colors.css` (seções de marca e derivados), `readme.md` (VISUAL FOUNDATIONS), `guidelines/colors-contrast.html` | Dois níveis de cor mais tabela de razões de contraste |
| 8 | **Semântico sobre primitivo**, com escala de rótulos e fills e estados descritos uma vez (hover, pressionado, desabilitado, foco, seleção inativa). | `tokens/colors.css`, `readme.md` | Camadas primitivo → semântico → componente (já cobertas em `design-tokens.md`) |
| 9 | **Escala tipográfica fechada, hierarquia por peso e cor, números tabulares, mono para dado técnico.** | `tokens/typography.css`, `components/mb.css` (`.mb-tabular`, `.mb-mono`) | Escala nomeada com line-height pareado; em mobile, unidades escaláveis |
| 10 | **Fonte do sistema declarada, sem webfont, com lint.** Fallback registrado como risco. | `tokens/fonts.css` (só `local()`), `readme.md` (Substituições a validar) | `system-ui` e `ui-monospace`; só famílias declaradas |
| 11 | **Espaço em grade, métricas com nome de intenção e raios concêntricos** (interno = externo − espaçamento). | `tokens/spacing.css`, `tokens/shape.css`, `guidelines/radii.html` | Regra de raio vale para qualquer contêiner aninhado |
| 12 | **Material e elevação como tokens com regra de uso**: vidro só na navegação, nunca em conteúdo, nunca vidro sobre vidro. | `tokens/materials.css` (cabeçalho), `readme.md` (VISUAL FOUNDATIONS) | "Um material por camada" com regra de empilhamento escrita |
| 13 | **Movimento por física com parâmetros documentados** (duração perceptual e bounce como fonte; rigidez e amortecimento derivados). | `tokens/motion.css` (cabeçalho com a fórmula), `guidelines/motion.html` | `spring()` no Compose, `.smooth/.snappy/.bouncy` no SwiftUI, `linear()` na web |
| 14 | **Fundamentos de conteúdo dentro do DS**: idioma e tom, rótulo de botão, erro, vazio, tooltip, status. | `readme.md` (CONTENT FUNDAMENTALS), `components/content/EmptyState.prompt.md`, `components/overlays/Alert.prompt.md` | Todo produto escreve o seu (ver `ux-writing`) |
| 15 | **Rastreabilidade e honestidade de escopo**: mapeamento código → componente, "Intentional additions", "Substituições a validar", escopo "sem tirar nem inventar funções". | `readme.md` (Components, Intentional additions, Substituições a validar) | Tabela origem → destino, adições intencionais e dívidas declaradas |
| 16 | **Registro de sincronização com a fonte**: repo, branch, data do último sync e mapa tela → arquivos. | `github.md` | `SOURCES.md` em qualquer DS |
| 17 | **Guidelines como cards visuais atômicos**, cada um com a variante de acessibilidade ao lado. | `guidelines/*.html`, `components/*/*.card.html` | Um card ou `@Preview` por decisão |
| 18 | **UI kit com nota por tela** ("o que mudou e por quê") e painel de estados (aparência, acessibilidade, janela inativa, vazio, erro, carregando). | `ui_kits/macos-app/README.md` | Tabela tela → mudança → motivo → estados cobertos |
| 19 | **`SKILL.md` do próprio DS** como ponto de entrada para IA. | `SKILL.md` (frontmatter `name`, `description`, `user-invocable`) | Um `SKILL.md` por DS (a skill `design-init` pode gerá-lo) |
| 20 | **Teclado, aria, tooltip, foco e alvo mínimo no contrato do componente.** Ação destrutiva nunca é a padrão. | `components/overlays/Sheet.prompt.md`, `components/content/DataTable.prompt.md`, `components/indicators/CountBadge.d.ts`, `components/mb.css` (`:focus-visible`) | Declarar teclado, leitor de tela e foco em todo componente interativo |

## 3. Resumo de tokens e componentes

Convenção de nomes: `--<categoria>-<papel>[-<estado|escala>]` em kebab-case; valores literais só nos primitivos; semânticos referenciam primitivos (por exemplo `--accent: var(--flamingo-600)`, lido em `tokens/colors.css`).

| Arquivo | Categoria | Exemplos citados do arquivo |
| --- | --- | --- |
| `tokens/colors.css` | Marca, derivados acessíveis, rótulos, fundos, destaque e foco, seleção, semânticas | `--brand-flamingo`, `--flamingo-600`, `--label-primary`, `--bg-window`, `--accent`, `--on-accent`, `--focus-ring`, `--selection-inactive`, `--destructive` |
| `tokens/typography.css` | Família, tamanho, line-height, peso, tracking | `--font-ui`, `--font-mono`, `--text-body`, `--lh-body`, `--weight-semibold` |
| `tokens/spacing.css` | Escala e métricas de layout | `--space-1` a `--space-10`, `--toolbar-height`, `--control-height-regular`, `--hit-min` |
| `tokens/shape.css` | Raios e sombras | `--radius-window`, `--radius-capsule`, `--shadow-popover` |
| `tokens/materials.css` | Vidro e menus | `--glass-bg`, `--glass-filter`, `--glass-tint`, `--menu-bg` |
| `tokens/motion.css` | Molas e tempos | `--spring-smooth-ease`, `--motion-hover`, `--ease-out-standard` |

Componentes (namespace e lista em `_ds_manifest.json`; descrição em `readme.md`): **controls** (Button, SegmentedControl, PopUpButton, SearchField, TextField, Switch, Checkbox), **indicators** (Icon, CountBadge, StatusIndicator, TypeChip, ProgressIndicator), **navigation** (Toolbar e partes, Sidebar e partes), **overlays** (Menu, Popover, Tooltip, Sheet, Alert), **window** (Window, TrafficLights, MenuBar, DeviceFrame, Splitter), **content** (DataTable, DiagnosticCard, EmptyState). Contrato fechado de exemplo em `components/controls/Button.d.ts` (`variant` e `size` em uniões literais). Para valores exatos, abra o arquivo: não os copie de memória.

## 4. Como aplicar em outro produto ou plataforma

1. **Descubra o sistema ativo** (marca, `DESIGN.md`, tokens). Se o usuário pediu o design system da casa, leia `design-systems/mo-baile/SKILL.md` e `readme.md` antes de propor; cite token e componente pelo nome e pelo arquivo.
2. **Adapte a estrutura, troque a identidade.** Reproduza a anatomia (tokens por categoria, camadas por aparência, fallbacks como tokens, contrato por componente, lint, fundamentos de conteúdo, rastreabilidade) com as cores, fontes e métricas do produto. O template [design-system-bundle.md](../assets/templates/design-system-bundle.md) traz a estrutura.
3. **Ajuste ao ponteiro e à plataforma.**

| Conceito | Web | Android (Compose) | iOS (SwiftUI) |
| --- | --- | --- | --- |
| Camadas por aparência | `data-*` ou `prefers-*` redefinindo as mesmas custom properties | variantes claro/escuro/alto contraste do tema | Asset Catalog com Appearances |
| Reduzir movimento/transparência | `prefers-reduced-motion` e equivalentes | escala de animação do sistema injetada no tema | `accessibilityReduceMotion`, `accessibilityReduceTransparency` |
| Alvo mínimo | `--hit-min` de ponteiro; toque a partir de 24 px CSS (WCAG 2.5.8), meta maior | 48 dp (Material 3 é lacuna aqui; confirme) | 44 pt |
| Tipografia | `rem` e escala nomeada | `sp` e `Typography` | Dynamic Type |
| Lint de aderência | ESLint/Stylelint/oxlint | detekt ou Android Lint custom | SwiftLint `custom_rules` |

4. **Registre o que é adição e o que precisa validar.** Toda decisão que não vem do produto ou do DS entra em "adições intencionais"; toda substituição (fonte, ícones, cor) entra em "a validar".
5. **Estética macOS só em app macOS.** Em outro alvo, herde as regras (camadas, contraste medido, estado por três canais) e não o Liquid Glass, as métricas de janela nem os atalhos.

## 5. O que não impor

Identidade (flamingo/piscina/alien, mascote); Liquid Glass e vibrancy fora do macOS; métricas de desktop (toolbar, sidebar, controles de 24 px, texto base de 13 px, `--hit-min: 20px`); elementos de janela do Mac; regras de texto do HIG (reticências, Title Case, "você" em pt-BR) como decisão do produto; SF Pro e Lucide; paleta de domínio (`--syntax-*`, `--http-*`, `--chip-*`); componentes de domínio (DiagnosticCard, TypeChip, DeviceFrame); a stack React + oxlint; o escopo "sem tirar nem inventar funções" em produto novo (lá, o limite é o brief).

## 6. Checklist de adesão

- [ ] Design system ativo escolhido pelo usuário, não presumido.
- [ ] Tokens citados pelo nome; nenhum hex, px ou família de fonte crus na spec ou no código.
- [ ] Cada cor de texto ou de ação com par `on-*` e razão de contraste calculada, nos temas claro, escuro e alto contraste.
- [ ] Reduzir movimento e reduzir transparência tratados como sobrescrita de token.
- [ ] Estado nunca só por cor.
- [ ] Componente com contrato (tipos fechados, quando usar, exemplo, teclado e foco).
- [ ] Fundamentos de conteúdo do produto lidos antes de escrever texto.
- [ ] Adições intencionais e itens a validar listados.
- [ ] O que não foi renderizado nem medido consta como "Não verificado".
