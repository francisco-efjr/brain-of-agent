# Plano de UI: [nome da tela ou componente]

Use antes de escrever código para UI nova ou redesenho. Pule para correção localizada em que o diff cabe numa frase. Variáveis entre colchetes são preenchidas por quem usa o modelo. O brief do usuário, o `DESIGN.md` e os tokens do projeto vencem qualquer escolha estética padrão.

## 1. Brief (3 linhas)

- Assunto: [o que é o produto ou a página, em uma frase]
- Público: [quem usa, em que contexto e dispositivo]
- Tarefa principal: [o que a pessoa precisa conseguir fazer em menos de 1 minuto]
- Restrições do projeto: [stack e versão, tokens existentes, marca, componentes a reaproveitar]

## 2. Tokens

| Papel | Nome | Valor (hex ou oklch) | Por que (derivado do assunto) |
| --- | --- | --- | --- |
| [dominante] | [ex.: `--color-ink`] | [valor] | [motivo] |
| [acento] | | | |
| [superfície] | | | |

4 a 6 cores nomeadas. Papéis tipográficos (título, corpo, rótulo, dado): [família, tamanho, peso, uso]. Uma ou duas famílias; linhas de texto abaixo de cerca de 80 caracteres.

## 3. Layout

Conceito (uma frase por opção) e wireframe ASCII:

```text
[opção A: wireframe em ASCII]
```

Escolhida: [A ou B] porque [motivo].

## 4. Três princípios específicos do brief

1. [princípio ligado ao assunto, não genérico]
2. [princípio]
3. [princípio]

## 5. Revisão do plano contra o genérico

| Decisão que serve para qualquer página parecida | Mudei para | Porque |
| --- | --- | --- |
| [decisão] | [escolha derivada do assunto] | [motivo] |

Consulte a lista de saída genérica em `references/css-tokens-e-design-ui.md`. Se o usuário pediu um visual da lista, siga o pedido e diga o trade-off uma vez.

## 6. Piso de qualidade (critério de aceite verificável)

- [ ] 320 px sem rolagem horizontal (captura)
- [ ] Foco visível em todo controle (Tab)
- [ ] Contraste de texto normal de pelo menos 4,5:1, medido
- [ ] Contrapartida em `prefers-reduced-motion: reduce` para cada animação
- [ ] Estados cobertos: [inicial, carregando, vazio, erro, sucesso]
- [ ] Dados reais ou plausíveis, incluindo extremos
- [ ] Capturas em mobile e desktop anexadas; pelo menos um elemento decorativo removido na crítica

## 7. Fora do escopo

[o que este plano não cobre]

## 8. Aprovação

Plano aprovado por: [nome do humano] em [data]. Sem aprovação, não construir em escolha de arquitetura.
