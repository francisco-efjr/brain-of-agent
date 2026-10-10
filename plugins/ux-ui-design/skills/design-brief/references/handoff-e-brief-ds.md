# Modos `handoff` e `brief-ds`

## Sumário

- [Modo handoff: spec de componente ou tela](#modo-handoff-spec-de-componente-ou-tela)
- [Exemplo de spec resumida](#exemplo-de-spec-resumida)
- [Modo brief-ds: brief de design system por setor](#modo-brief-ds-brief-de-design-system-por-setor)
- [Limites](#limites)

## Modo handoff: spec de componente ou tela

Objetivo: entregar a quem implementa (humano ou agente) tudo que o código não revela sozinho. Template completo: [T-06](${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/spec-componente-handoff.md). Quem escreve a spec dentro de um design system existente pode ser o agente `ui-designer`.

Passos:

1. **Inventário primeiro.** Liste os componentes e tokens existentes que serão reutilizados (busca por `Grep` no repositório, Storybook se houver). Componente novo só quando nenhum existente cobre o caso; justifique.
2. **Propósito e contrato.** Nome, propósito em uma frase, props tipadas com valores permitidos e padrão, conteúdo (texto máximo, plural, idioma).
3. **Estados.** Para o elemento interativo, cubra: normal, hover, foco (teclado), pressionado, desabilitado, carregando, erro, vazio e texto longo. Estado de carregamento mantém o foco no elemento e anuncia o texto; `disabled` durante carregamento tira o controle do foco do teclado, então prefira `aria-disabled` ou mantenha o botão ativo e ignore o clique repetido.
4. **Tokens consumidos.** Somente semânticos ou de componente; nenhum hex, px ou ms literal na spec.
5. **Teclado e acessibilidade.** Teclas e ordem de foco, papel e nome acessível, anúncio de mudança dinâmica, alvo mínimo (24 px CSS; meta de toque 44), `prefers-reduced-motion`.
6. **Responsivo e casos de borda.** Comportamento em 320 px, com zoom de 200%, com 0, 1 e muitos itens.
7. **Critérios de aceite observáveis**, escritos como testes: "em 320 px não há rolagem horizontal", "Tab alcança o botão e o contorno tem 3:1 contra o fundo", "com erro, o campo é ligado à mensagem por `aria-describedby`".
8. **O que a spec não resolve**: persistência, permissão e integração dependem do código e não se provam por mockup.

## Exemplo de spec resumida

```text
Componente: ButtonAsync (reutiliza Button; não cria variante nova de cor)
Propósito: ação que dispara requisição e mostra progresso.
Props: label (string, obrigatório, verbo + objeto), onPress, status: idle|loading|error (padrão idle).
Estados: idle | foco (contorno color.focus.ring 2 px, deslocamento 2 px) | loading (texto "Salvando…", spinner
  com aria-hidden, o texto é anunciado via aria-live="polite" no contêiner; botão mantém foco) | error (mensagem
  abaixo ligada por aria-describedby; botão volta a idle).
Tokens: color.action.primary.bg, color.action.primary.fg, space.inline.md, radius.control, motion.duration.short.
Teclado: Enter e Espaço ativam; durante loading, ativação repetida é ignorada.
Aceite: 1) contraste fg/bg calculado >= 4,5:1; 2) loading não remove o foco; 3) sob prefers-reduced-motion o spinner
  vira texto estático "Salvando…".
```

## Modo brief-ds: brief de design system por setor

Objetivo: abrir um design system com entradas claras e saídas verificáveis, sem baixar catálogos nem rodar scripts de terceiros. Template: [T-10](${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/brief-design-system.md).

Entradas a coletar (uma pergunta por vez, só o que mudar o resultado): produto e setor, público, stack e biblioteca de componentes, requisito de acessibilidade e jurisdição, idiomas, marca existente (logo, cores, voz), plataformas.

Saídas:

- tokens de cor, tipografia e espaçamento em três camadas (esqueleto em [design-tokens](${CLAUDE_PLUGIN_ROOT}/skills/design-tokens/SKILL.md));
- padrão de layout por superfície;
- **cinco anti-padrões** específicos do setor (por exemplo, em fintech: urgência artificial, jargão regulatório sem tradução, confirmação só por cor);
- checklist de entrega: estados, teclado, contraste calculado, documentação de uso, política de versão.

A ideia do template vem do repositório `ui-ux-pro-max-skill` (MIT, V-30) e foi reescrita; o catálogo de estilos, paletas e scripts de busca do original não entra, e comandos de instalação dele não devem ser executados. Quantidade de dados em um catálogo não prova qualidade das recomendações (Não verificável).

## Limites

- Handoff não implementa: termina na spec e nos critérios de aceite.
- Não escreva no Figma nem altere tokens a partir de export: Figma entra só como leitura e relatório.
- Nenhum número de plataforma (por exemplo 48 dp do Android) sem fonte lida: Material 3 é lacuna do plugin.
