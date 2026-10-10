# Android nativo: traduzir princípios de motion e polimento

Conteúdo validado em 2026-10-10. As skills de motion vendorizadas cobrem web (`animate`, `apple-design`, `emil-design-eng`) e React Native/Expo (`animate-expo`). **Não há skill para Android nativo (Compose ou Views).** Este arquivo traduz os *princípios* e os *tokens* do design system da casa, sem copiar CSS. Na validação de 2026-10-10 foram abertas três páginas oficiais Android (F-10): "Customize animations" do Compose, o guia de acessibilidade de apps e a referência de `Settings.Global`. A documentação do Material 3 motion **não** foi aberta: o que depende dela segue Inferido ou Não verificável; confirme na documentação da versão do projeto antes de aplicar.

## Sumário

1. Regra de ouro
2. Princípios do Emil traduzidos
3. Tokens de motion do Mo baile para Compose
4. Reduzir movimento
5. Material motion: onde divergem os critérios
6. Componentes da plataforma antes de custom
7. Verificação em Android
8. O que não copiar

## 1. Regra de ouro

Herde a **regra** (propósito, frequência, curva, duração, interrupção, acessibilidade) e o **token** do design system ativo; troque a **mecânica** (CSS, `linear()`, `transform-origin`) pela da plataforma. Valor numérico que veio de outra plataforma entra rotulado. Se o projeto tem tema de Compose com motion, ele vence ([precedencia-e-adaptacao.md](precedencia-e-adaptacao.md)).

## 2. Princípios do Emil traduzidos

Os 10 padrões de `review-animations` (web) traduzidos para Compose. Os nomes de API do Compose são estáveis; o *efeito* de cada um deve ser conferido na versão do projeto (Inferido).

| # | Princípio (Emil) | Tradução para Android/Compose | Rótulo |
| --- | --- | --- | --- |
| 1 | Todo movimento tem justificativa | Igual: continuidade espacial, indicar estado, feedback, explicar. Sem movimento decorativo em tela vista dezenas de vezes por dia | Inferido |
| 2 | Frequência define a quantidade | Ações repetidas (digitar, rolar, alternar abas) sem animação ou muito curta | Inferido |
| 3 | Easing responde rápido | Entrada com curva de desaceleração (`FastOutSlowInEasing` ou `LinearOutSlowInEasing`); evite `LinearEasing` em UI. Saída: ver seção 5 | Inferido |
| 4 | UI abaixo de 300 ms | Transições de componente curtas (`tween`); transições de tela inteira ou container podem ser mais longas: rotule a escolha | Inferido |
| 5 | Origem coerente com o gatilho | Menu, popover e tooltip escalam do ponto de ancoragem (`TransformOrigin` em `graphicsLayer`); nunca partir de `scale = 0` | Inferido |
| 6 | Interruptível | Prefira `spring` e `Animatable.animateTo` (retargeta sem recomeçar do zero) a sequências que reiniciam; `animate*AsState` retargeta ao mudar o alvo | Inferido |
| 7 | Só propriedades baratas | Anime por `Modifier.graphicsLayer { translationX; scaleX; alpha }` em vez de `size`, `padding` e `offset` que disparam layout | Inferido |
| 8 | Reduzir movimento | Seção 4 | Inferido |
| 9 | Entrada e saída assimétricas | `animationSpec` diferente conforme o estado (pressionar lento, soltar rápido) | Inferido |
| 10 | Coesão | Tokens de motion no tema (um objeto ou `CompositionLocal`), nunca durações soltas pelo código | Inferido |

## 3. Tokens de motion do Mo baile para Compose

Origem: `design-systems/mo-baile/tokens/motion.css`. Os tokens declaram `stiffness` e `damping` com massa 1, e a fórmula do arquivo dá amortecimento `4π(1−bounce)/duração`. Fazendo o cálculo `damping / (2·√stiffness)`, o **dampingRatio** do Compose é `1 − bounce` (conferido por cálculo: 1,00, 0,85, 0,70 e 1,00 para `smooth-small`). `spring` do Compose recebe exatamente `dampingRatio` e `stiffness` (Verificado em "Customize animations"); que a mola do Compose use massa 1 é Inferido, e por isso os valores traduzem direto:

| Token Mo baile | Uso no design system | `dampingRatio` | `stiffness` |
| --- | --- | --- | --- |
| `--spring-smooth` (0,5 s, bounce 0) | Painéis e sheets (padrão) | 1,0 | 157,91 |
| `--spring-smooth-small` (0,3 s, bounce 0) | Variante menor da smooth (uso não detalhado no bundle) | 1,0 | 438,65 |
| `--spring-snappy` (0,35 s, bounce 0,15) | Cliques, segmentados, switches | 0,85 | 322,27 |
| `--spring-bouncy` (0,5 s, bounce 0,3) | Só manipulação direta; quase não aparece | 0,70 | 157,91 |
| `--motion-crossfade` 180 ms | Trocar de seção | `tween(180)` | n/a |
| `--motion-menu-fade-out` 150 ms | Menu some | `tween(150)` | n/a |
| Menus aparecem na hora; popover 95% para 100% com fade | Sobreposições | `tween` curto + `graphicsLayer` | n/a |

Esqueleto (Inferido, não compilado; a API deve ser conferida na versão do projeto):

```kotlin
object AppMotion {
    val Smooth = spring<Float>(dampingRatio = 1f, stiffness = 157.91f)
    val Snappy = spring<Float>(dampingRatio = 0.85f, stiffness = 322.27f)
    val Crossfade = tween<Float>(durationMillis = 180)
}
```

O hover de 60 ms do Mo baile não se aplica a toque. Sombra, vidro e métricas de janela do Mo baile são do macOS e não migram ([precedencia-e-adaptacao.md](precedencia-e-adaptacao.md)).

## 4. Reduzir movimento

O Mo baile trata "Reduzir movimento" como **sobrescrita de token**: molas viram `linear` e as durações encurtam, sem `if` nos componentes. No Android o equivalente é um único ponto no tema:

1. Leia a preferência do sistema: a escala de duração de animação (`Settings.Global.ANIMATOR_DURATION_SCALE`, padrão 1,0; com 0 as animações de Animator terminam na hora: Verificado na referência). Que o ajuste "Remover animações" de acessibilidade a zere é Inferido: confirme no aparelho.
2. Injete no tema (`CompositionLocal`) um `reduceMotion` e escolha, no objeto de tokens, `snap()` ou `tween` curto de fade em lugar de deslizamento, escala e mola.
3. Mantenha opacidade e cor (gentil, não zero), remova deslocamento e escala. O Compose pode já respeitar a escala do sistema em parte das animações: Não verificável aqui; teste com a escala em zero.
4. Teste: Opções do desenvolvedor, escalas de animação em 0 e em 10x (câmera lenta). Inferido.

## 5. Material motion: onde divergem os critérios

Valores de duração, easing e tokens de movimento do Material 3 são **Não verificáveis aqui**: consulte a documentação oficial de Material 3 motion e o Compose da versão do projeto. Pontos de atrito conhecidos (Inferido):

- Material tradicionalmente usa desaceleração na entrada e aceleração na saída; o Emil trata `ease-in` em UI como achado, porque atrasa o momento que o usuário observa. Decida pelo design system do projeto. Sem sistema: entrada com desaceleração, saída curta, e registre a escolha como Suposição.
- Padrões nomeados do Material (container transform, shared axis, fade through) existem nas bibliotecas de componentes do Material e, em Compose, em transições compartilhadas: use-os para navegação entre telas em vez de reinventar; o motion do Emil continua valendo para microinterações.
- Transições de tela inteira costumam passar de 300 ms: não é defeito, é outra categoria.

## 6. Componentes da plataforma antes de custom

`ModalBottomSheet`, `DropdownMenu`, `AlertDialog`, `Snackbar` e `NavHost` já trazem motion, foco e acessibilidade da plataforma. Reimplementar para "ficar como o Mo baile" só com pedido e com motivo. Estados: ícone + cor + texto (nunca só cor); alvo de toque de pelo menos 48 × 48 dp (Verificado no guia de acessibilidade Android; a página do Material 3 não foi aberta).

## 7. Verificação em Android

O Playwright MCP **não controla app Android nativo**. Use `@Preview`, emulador e dispositivo; capturas fornecidas pelo usuário; câmera lenta pelas Opções do desenvolvedor. Sem executar, escreva "revisado por leitura; execução Não verificável". Para build, Gradle e testes de Compose: `/mobile-apps:playbook`.

## 8. O que não copiar

CSS (`transition`, `linear()`, `@starting-style`), `transform-origin`, gates `@media (hover: hover)`, regras de `100dvh`, Liquid Glass e `backdrop-filter`, `prefers-reduced-motion`. Copie a intenção; reescreva a mecânica.
