# Esqueleto de DESIGN.md

Template T-04. Uso: `design-init` (só por `/ux-ui-design:design-init`, com confirmação antes de gravar). O formato é o do repositório google-labs-code/design.md (Apache-2.0), em **alpha**: especificação, schema e CLI mudam; fixe a versão do formato que adotar e confira o README do repositório. Este esqueleto segue a estrutura descrita na validação (front matter YAML de tokens e oito seções em ordem canônica); os nomes exatos das chaves do front matter devem ser conferidos no README da versão usada (Inferido).

Regras de preenchimento: use somente valores que existam no código ou que o usuário aprovou; nada de cor, fonte ou espaçamento inventado. Calcule o contraste dos pares pela fórmula WCAG; não copie a mensagem do linter (o exemplo da documentação é inconsistente). Nunca sobrescreva um `DESIGN.md` existente: proponha diff.

````markdown
---
# Front matter de tokens (conferir chaves no README da versão do formato)
name: [Nome do produto]
colors:
  text-default: "[#______]"
  surface-default: "[#______]"
  action-primary: "[#______]"
typography:
  body: { family: "[família]", size: "[17px]", lineHeight: "[1.5]" }
spacing:
  base: "[4px | 8px]"
rounded:
  control: "[__px]"
---

# Overview
[Assunto, público, tarefa principal, superfície (Persuade/Operate/Read/Experience) e "o que a pessoa deve lembrar". Por que as escolhas abaixo servem a isso.]

# Colors
[Papéis das cores, pares de contraste calculados (par, razão, estado), uso de cor para feedback, modo escuro como modo da coleção semântica.]

# Typography
[Famílias, escala, medida de linha, regras de títulos e números.]

# Layout
[Grade, breakpoints (320, 768, 1440), escala de espaçamento, densidade.]

# Elevation & Depth
[Como a profundidade é expressa; modo escuro por elevação.]

# Shapes
[Hierarquia de raios; raio interno = raio externo menos o intervalo.]

# Components
[Componentes existentes, estados obrigatórios (hover, foco, desabilitado, carregando, erro), tokens que cada um consome.]

# Do's and Don'ts
[Regras curtas, cada uma com motivo: ex.: "Não usar cor literal em componente: use token semântico, porque o tema muda sem renomear."]
````

## Bloco para o CLAUDE.md (somente com confirmação separada)

```markdown
## Direção de design
- Consulte DESIGN.md ao gerar ou alterar UI; não invente cores, fontes ou espaçamentos fora dele; mudanças de token passam por revisão.
- UI nova ou redesenho começa com brief de uma linha (assunto, público, tarefa) e plano de tokens, revisado contra escolhas genéricas, antes do código.
```
