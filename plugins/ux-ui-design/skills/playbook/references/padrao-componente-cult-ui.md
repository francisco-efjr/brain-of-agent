# Padrão de componente: contrato de código e de documentação (base cult-ui)

Conteúdo validado em 2026-10-11 contra `nolly-studio/cult-ui` (branch `main`, push de 2026-10-01, licença MIT, © Jordan Gilliam / Nolly Studio), lendo `registry.json` (307 itens), as 134 páginas MDX de componente, `mdx-components.tsx`, `scripts/check-registry.mts` e 141 arquivos de `registry/default/ui/`. Decisão do usuário: **os sistemas dele seguem a documentação do cult-ui no nível de componente**. Este arquivo transforma isso em contrato verificável e corrige as falhas observadas no próprio cult-ui. Redação própria; trechos de código curtos vêm do repositório MIT com atribuição.

## Sumário

1. Quando aplicar e precedência
2. Estrutura de arquivos e distribuição (registro shadcn)
3. Anatomia do componente (código)
4. Página de documentação (template)
5. Validação automática (CI)
6. O que não copiar do cult-ui
7. Checklist de aceite do componente
8. Adaptação para outras plataformas

## 1. Quando aplicar e precedência

- **Sempre** que o pedido for criar, especificar, documentar ou revisar um componente de UI em sistema do usuário. Vale para spec (`ui-designer`), para auditoria (`design-system-auditor`) e para o plugin de código quando ele implementar.
- O padrão define **forma** (arquivos, API, doc, validação), não **estética**. A estética vem do design system ativo ou da direção escolhida em [direcoes-de-estilo](direcoes-de-estilo.md).
- Precedência: tokens e marca do produto > este contrato de forma > padrões visuais do cult-ui (Halo, Texture), que são só uma das direções disponíveis.
- Stack de referência do cult-ui (Inferido como padrão, confirme no projeto): React 19, Next.js, Tailwind CSS v4 (`@theme inline`, `@custom-variant dark`), shadcn CLI 3 (`style: new-york`, `cssVariables: true`, `iconLibrary: lucide`), `motion` importado de `motion/react`, `class-variance-authority`, `clsx` + `tailwind-merge`, primitivos Radix ou Base UI. Projeto com outra stack: mantenha a forma, troque as bibliotecas.

## 2. Estrutura de arquivos e distribuição

Três arquivos por componente, sempre juntos (o cult-ui tem 154 itens de UI e 153 demos pareados):

```text
registry/<estilo>/ui/<nome>.tsx            implementação, um arquivo por componente (kit composto também)
registry/<estilo>/example/<nome>-demo.tsx  demo com export default XDemo; registryDependencies: ["<nome>"]
content/docs/components/<nome>.mdx         página de documentação (seção 4)
```

- **Nome:** arquivo em kebab-case; exports em PascalCase com o nome como prefixo (`HaloButton`, `TimerRoot`, `ChoicePollOption`).
- **Registro como código:** itens declarados em TypeScript (`registry/ui.ts`, `registry/examples.ts`) com `satisfies Registry`; um script gera `registry.json`, o índice lazy das previews e `public/r/<nome>.json` via `shadcn build`. Não edite JSON de registro à mão.
- **Campos do item:** `name`, `type` (`registry:ui` | `registry:component` | `registry:block`), `description`, `dependencies` (npm), `registryDependencies`, `files[{path,type}]`. Diferente do cult-ui, **declare `cssVars` e `css`** quando o componente precisar de keyframes, variantes ou utilitários próprios (ver seção 6).
- **Dependências:** componente base do shadcn sem prefixo (`"button"`); componente do próprio sistema com namespace (`"@<ns>/<nome>"`) ou URL completa.
- **Instalação:** `npx shadcn@latest add @<ns>/<nome>`, com `"registries": { "@<ns>": "https://<dominio>/r/{name}.json" }` em `components.json`. Instalar é decisão do usuário (fronteira de ações do plugin).
- **Renomear sem quebrar:** o nome antigo vira item alias com `files: []`, `registryDependencies` apontando para o novo e descrição "Deprecated alias for <novo>". Remova o alias só numa versão maior.
- **Para agentes:** publique `llms.txt`, `llms-full.txt` e a versão `.md` de cada página (`/docs/components/<nome>.md`). A regra para AGENTS.md é: instalar pelo registro, nunca recriar à mão, ler `<nome>.md` antes de usar.

## 3. Anatomia do componente (código)

Siga a **geração 2** do cult-ui (kit Halo, polls, heroes, 2025–2026). A geração 1 (forwardRef + tipos repetidos) é legado.

| Regra | Como | Por quê |
| --- | --- | --- |
| C-01 Cliente explícito | `"use client"` na primeira linha só quando há estado, efeito ou animação | RSC por padrão (`rsc: true`) |
| C-02 Props nativas | `ComponentProps<"button">` ou as props do primitivo (`SwitchPrimitive.Root.Props`); `ref` como prop (React 19), sem `forwardRef` | Herdar atributos e aria sem redeclarar |
| C-03 `className` por último | `cn(variants({ variant, size }), className)` | O consumidor sempre vence |
| C-04 Variantes tipadas | `cva` + `VariantProps<typeof x>`; uniões literais fechadas; padrão em `defaultVariants`; exporte `xVariants` | Contrato fechado que o lint pode checar |
| C-05 `data-slot` em cada parte | `data-slot="choice-poll-option"`, mais `data-state`, `data-selected`, `data-disabled` | Estilo por estado sem prop extra; convenção shadcn v4 |
| C-06 Composto com contexto | `createContext(null)` + hook que lança erro fora do Root ("X components must be used within X.Root") | Falha cedo e com mensagem útil |
| C-07 Exports duplos | objeto namespace (`ChoicePoll.Root`, `.Option`) **e** exports nomeados planos | Ergonomia e tree-shaking |
| C-08 Estado controlável | `value` / `defaultValue` / `onValueChange` com `useControllableState` | Funciona controlado e não controlado |
| C-09 Polimorfismo | `asChild` via `Slot` (Radix) ou `render` (Base UI); evite `as` genérico | Semântica certa sem wrapper |
| C-10 Customização em kits grandes | `render*` props (`renderCta(defaultCta)`), objetos de override parciais (`ctaProps`), hook `useX()` e um `X` montado como padrão | Troca uma parte sem ejetar o kit |
| C-11 Movimento como constante | no topo do módulo: `const layoutSpring = { type: "spring", bounce: 0.12, damping: 34, stiffness: 420 }`, `const LABEL_STAGGER_SEC = 0.018`; compartilhe entre componentes irmãos | Sensação coerente e ajuste num lugar só |
| C-12 Movimento reduzido sempre | `const reduceMotion = useReducedMotion() ?? false`; durações e deslocamentos vão a 0; loops CSS só com `!reduceMotion`; `motion-reduce:` nas classes | WCAG 2.3.3 e conforto; o cult-ui faz isso em 28 de 141 arquivos, aqui é obrigatório |
| C-13 Tokens, não cores cruas | `var(--card)`, `--border`, `--input`, `--muted(-foreground)`, `--ring`, `--accent`, `--destructive`, `--radius`; transparência com `color-mix(in oklch, var(--card) 82%, transparent)`; cor que o tema não cobre vira variável com escopo (`[--x-fg:var(--primary-foreground)]`) | Tema claro, escuro e alto contraste sem tocar o componente |
| C-14 Raio concêntrico | interno = externo − padding (`rounded-[calc(var(--radius)-1px)]`) | Mesma regra do Mo baile |
| C-15 Foco e alvo | `focus-visible:ring-2 focus-visible:ring-ring/30`; alvo `min-h-11 min-w-11` ou hit area estendida com pseudo-elemento | WCAG 2.4.7, 2.5.8 |
| C-16 Carregando | `aria-busy` no controle, spinner `aria-hidden`; prefira `aria-disabled` a `disabled` quando o foco precisa ficar (regra do `ui-designer`) | Leitor de tela entende o estado |
| C-17 Banners de seção | `/* ---- Types ---- */`, `Context`, `Variants`, `Components`, `Export` | Arquivo único fica navegável |
| C-18 JSDoc nas props | uma linha por prop pública e nos tipos exportados do hook (`UseTimerOptions`, `UseTimerReturn`) | Alimenta a tabela de API |

Exemplo mínimo de forma (adaptado do padrão `choice-poll.tsx`, MIT):

```tsx
"use client"
const PollContext = createContext<PollContextValue | null>(null)
function usePoll() {
  const ctx = useContext(PollContext)
  if (!ctx) throw new Error("Poll components must be used within Poll.Root")
  return ctx
}
function PollOption({ value, className, ...props }: ComponentProps<"button"> & { value: string }) {
  const { selected, select } = usePoll()
  const isSelected = selected === value
  return <button type="button" role="option" aria-selected={isSelected} data-slot="poll-option"
    data-state={isSelected ? "on" : "off"} className={cn(optionVariants({ selected: isSelected }), className)}
    onClick={() => select(value)} {...props} />
}
export const Poll = { Root: PollRoot, Option: PollOption }
export { PollRoot, PollOption }
```

## 4. Página de documentação (template)

Template pronto: [doc-componente](../assets/templates/doc-componente.md) (T-14). Estrutura fixa, igual nas 134 páginas do cult-ui:

1. **Frontmatter:** `title`, `description` (fórmula: "<o que é> para React e shadcn/ui <com recursos-chave>, <para casos de uso>.", 120 a 160 caracteres), `component: true`, `links: {}` (`doc`, `api` opcionais).
2. **Preview:** `<ComponentPreview name="<nome>-demo" description="..." />` com abas Preview e Code.
3. **Introdução em duas frases:** "X é um componente React de <tipo> para shadcn/ui feito com <lib>. Use para <três casos concretos>."
4. **Installation:** abas CLI e Manual. CLI = `npx shadcn@latest add @<ns>/<nome>`. Manual = `Steps`: instalar dependências (só se houver) → colar o código (`<ComponentSource name="<nome>" />`) → ajustar imports.
5. **Usage:** bloco de import com todos os exports; depois H3 por caso: Uso básico, Composto, Controlado, Estilo customizado.
6. **API Reference:** um H3 por parte (`### TimerRoot Props`) com a tabela `Prop | Type | Default | Description`; hook com `#### Options` e `#### Return`; kits com tabela `Export | Type | Description` antes das props.
7. **Opcionais, nesta ordem quando existirem:** Features (bullets curtos), Examples, Customization, How It Works, Performance Notes, Troubleshooting (H3 por sintoma), References/Credits com `<Citations>`.
8. **Acessibilidade:** no cult-ui é opcional (14 de 134 páginas). **Aqui é obrigatória** e traz teclado, papel ARIA, foco, movimento reduzido e o que não foi testado com leitor de tela.

Componentes MDX que o site de docs precisa ter: `ComponentPreview` (`name`, `align`, `hideCode`, `description`, `type`), `ComponentSource` (código do registro, colapsável depois de 24 linhas), `CodeTabs` + `Tabs*`, `Steps`/`Step`, `Callout`, `Citations*`. Página com ação "copiar como markdown" e anterior/próximo.

## 5. Validação automática (CI)

Recrie a checagem do `check-registry.mts` (é o melhor do cult-ui) e acrescente o que falta:

- [ ] Cada item valida contra o schema `registry-item` do shadcn.
- [ ] Import `@/components/ui/x` sem `x` em `registryDependencies` = erro.
- [ ] Item do próprio sistema declarado sem namespace = erro.
- [ ] Import npm sem entrada em `dependencies` = erro (react, react-dom, next e builtins isentos).
- [ ] `public/r/<nome>.json` ausente ou desatualizado = erro; caminho de arquivo inexistente = erro.
- [ ] MDX citando nome fora do registro = erro.
- [ ] **Acréscimo:** todo `<nome>.tsx` tem `<nome>-demo.tsx` e `<nome>.mdx`.
- [ ] **Acréscimo:** classe ou variante usada (`fine-hover:`, `animate-*` próprio) sem `css`/`cssVars` no item = erro.
- [ ] **Acréscimo:** lint de aderência do design system ativo (hex e px crus, `transition-all`, `font-family` fora do sistema), como no `_adherence.oxlintrc.json` do Mo baile.
- [ ] **Acréscimo:** componente animado sem `useReducedMotion` ou `motion-reduce:` = aviso.

## 6. O que não copiar do cult-ui

Observado no código em 2026-10-11 (Verificado por leitura, não por execução):

| Falha no cult-ui | Regra aqui |
| --- | --- |
| `fine-hover:` (50 usos em 9 arquivos) e keyframes como `cosmic-spin` usados sem ir no registro | Todo CSS necessário vai em `css`/`cssVars` do item |
| `transition-all` em 25 arquivos, apesar da regra do próprio site | Liste as propriedades (`transition-[transform,opacity]`) |
| `motion.div onClick` e `div role="button"` como gatilho (FamilyButton, Expandable) | `<button type="button">` com `aria-expanded` |
| Abas sem `role="tab"`, `aria-selected` nem setas (DirectionAwareTabs) | Primitivo Radix/Base UI ou padrão ARIA APG de tabs |
| Conteúdo revelado só no hover (ShiftCard) | Mesmo conteúdo em `:focus-visible` e toque |
| `<div>` dentro de `<button>` (TextureButton) | Só conteúdo de frase dentro de botão (`<span>`) |
| Anel de foco com cor crua (`#adfa1b`) | `--ring` sempre |
| Cores fixas da geração 1 (indigo, stone, neutral) | Tokens semânticos (C-13) |
| Acessibilidade opcional na doc | Seção obrigatória (seção 4) |

## 7. Checklist de aceite do componente

- [ ] Três arquivos: `<nome>.tsx`, `<nome>-demo.tsx`, `<nome>.mdx`; item no registro com dependências completas.
- [ ] Regras C-01 a C-18 atendidas ou desvio justificado na doc (seção Notes).
- [ ] Estados do template de handoff (T-06) cobertos, inclusive carregando, erro e desabilitado.
- [ ] Tema claro, escuro e alto contraste sem cor crua; contraste calculado com os tokens reais.
- [ ] Movimento reduzido testado (ou "Não verificado" declarado).
- [ ] Doc com as seções da seção 4, incluindo Acessibilidade e tabela de API completa (tipo e padrão).
- [ ] CI da seção 5 verde.

## 8. Adaptação para outras plataformas

O contrato de forma vale fora do React; a stack muda.

| Ideia | SwiftUI | Jetpack Compose |
| --- | --- | --- |
| Um arquivo + demo + doc | `View` + `#Preview` + DocC | `@Composable` + `@Preview` + KDoc |
| Variantes fechadas | `enum` com `ButtonStyle` | `enum class` + `object XDefaults` |
| Composto com contexto | `@Environment` com valor padrão que falha em debug | `CompositionLocal` com `error()` padrão |
| Estado controlável | `Binding` opcional + `@State` interno | `value`/`onValueChange` + `rememberSaveable` |
| Movimento reduzido | `@Environment(\.accessibilityReduceMotion)` | `Settings.Global.ANIMATOR_DURATION_SCALE` / `LocalReduceMotion` próprio |

Implementação nessas plataformas fica com `/mobile-apps:playbook`; aqui fica a spec.
