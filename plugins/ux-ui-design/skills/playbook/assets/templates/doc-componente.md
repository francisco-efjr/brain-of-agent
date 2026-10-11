# Página de documentação de componente (padrão cult-ui)

Template T-14. Uso: `ui-designer` (spec que vira doc), `design-system-auditor` (conferir doc existente) e o plugin de código ao publicar o componente. Regras e porquês em [padrao-componente-cult-ui](../../references/padrao-componente-cult-ui.md). Substitua cada `[___]`; seção opcional sem conteúdo real sai da página. Salve como `content/docs/components/<nome>.mdx`, ao lado de `registry/<estilo>/ui/<nome>.tsx` e `registry/<estilo>/example/<nome>-demo.tsx`.

````mdx
---
title: [Nome Do Componente]
description: [O que é] para React e shadcn/ui [com recursos-chave], [para casos de uso].
component: true
links: {}
---

<ComponentPreview name="[nome]-demo" description="[Todas as variações]" />

[NomeDoComponente] é um componente React de [tipo] para shadcn/ui feito com [Motion | Base UI | Radix]. Use para [caso 1], [caso 2] e [caso 3].

## Installation

<CodeTabs>
<TabsList>
  <TabsTrigger value="cli">CLI</TabsTrigger>
  <TabsTrigger value="manual">Manual</TabsTrigger>
</TabsList>
<TabsContent value="cli">

```bash
npx shadcn@latest add @[ns]/[nome]
```

</TabsContent>
<TabsContent value="manual">
<Steps>
<Step>Instale as dependências:</Step>

```bash
npm install [motion class-variance-authority]
```

<Step>Copie e cole o código no seu projeto.</Step>
<ComponentSource name="[nome]" />
<Step>Ajuste os caminhos de import ao seu projeto.</Step>
</Steps>
</TabsContent>
</CodeTabs>

## Usage

```tsx
import { [Nome], [NomeRoot], [NomeItem] } from "@/components/ui/[nome]"
```

### Uso básico

```tsx
<[Nome] />
```

### Composto

```tsx
<[Nome].Root defaultValue="[a]">
  <[Nome].Item value="[a]">[Rótulo real]</[Nome].Item>
</[Nome].Root>
```

### Controlado

```tsx
const [value, setValue] = useState("[a]")
<[Nome].Root value={value} onValueChange={setValue}>…</[Nome].Root>
```

## API Reference

### [NomeRoot] Props

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `value` | `string` | - | Valor controlado |
| `defaultValue` | `string` | - | Valor inicial não controlado |
| `onValueChange` | `(value: string) => void` | - | Chamado quando o valor muda |
| `variant` | `"[a]" \| "[b]"` | `"[a]"` | [___] |
| `className` | `string` | - | Classes adicionais (aplicadas por último) |

### [useNome] Hook

#### Options

| Option | Type | Default | Description |
| --- | --- | --- | --- |

#### Return

| Key | Type | Description |
| --- | --- | --- |

## Accessibility

- Papel e elemento: [`button` nativo | padrão ARIA APG: ___].
- Teclado: [Tab, Enter, Espaço, setas, Home, End, Esc].
- Foco: [anel `--ring`; para onde vai ao abrir e fechar].
- Estado anunciado: [`aria-selected` | `aria-expanded` | `aria-busy` | `role="status"`].
- Movimento reduzido: [o que muda com `prefers-reduced-motion`].
- Não testado: [leitor de tela X, plataforma Y].

## Features

- [Recurso curto e verificável]

## Customization

### [Receita]

## Troubleshooting

### [Sintoma]

[Causa e correção.]

## References

<Citations>
  <CitationTitle>Inspiração</CitationTitle>
  <CitationList>
    <CitationItem>
      <CitationLink href="[url]" target="_blank" rel="noopener noreferrer">[Fonte]</CitationLink>
    </CitationItem>
  </CitationList>
</Citations>
````

## Checklist antes de publicar

- [ ] `description` com 120 a 160 caracteres na fórmula do frontmatter.
- [ ] Demo `[nome]-demo` existe no registro e usa conteúdo plausível, sem lorem ipsum.
- [ ] Toda prop pública na tabela, com tipo e padrão; hook com Options e Return.
- [ ] Seção Accessibility preenchida, com "Não testado" honesto.
- [ ] Nenhum nome citado na página fora do registro (CI).
