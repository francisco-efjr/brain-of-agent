# Exemplo de plano de design preenchido (modo `plano`)

Caso sintético para calibrar profundidade e formato. Não é marca real: a clínica, o bairro e os valores foram inventados para o exemplo. Não copie a paleta para outro projeto; copie a estrutura e o rigor (contraste calculado, trocas justificadas, suposições visíveis).

## Pedido

"Antes de eu codar, define a direção visual da landing da Clínica Vet Bairro Novo (clínica veterinária de bairro em Fortaleza, atende cães e gatos, agendamento por WhatsApp, tutores de 25 a 55 anos que acessam quase só pelo celular). Quero cores, fontes e layout, e que não pareça feito por IA."

## Pré-checagem

Nenhum `DESIGN.md`, token ou marca informados. Logo e nome existem, sem manual. Superfície: Persuade. Plataforma: web, mobile primeiro. Construtor: `web-frontend:design-ui` não verificado como instalado; a entrega é o plano.

## Brief

Landing de clínica veterinária de bairro para tutores de cães e gatos no celular; tarefa: agendar consulta pelo WhatsApp; lembrar: perto, cuidadosa e responde rápido.

## Tokens

Contrastes calculados com a fórmula WCAG ([contraste-wcag](${CLAUDE_PLUGIN_ROOT}/skills/design-tokens/references/contraste-wcag.md)), valores em 2026-10-10.

| Nome | Hex | Papel | Par de uso e razão |
| --- | --- | --- | --- |
| Tinta | `#14272B` | texto principal | sobre Areia 14,35:1 |
| Grafite | `#4A5D61` | texto secundário, legendas | sobre Areia 6,42:1; sobre Papel 6,93:1 |
| Musgo | `#0B5D4F` | ação primária, links, foco | branco sobre Musgo 7,80:1; Musgo sobre Areia 7,22:1 |
| Sol | `#FFC53D` | destaque decorativo (selo, marca-texto) | Tinta sobre Sol 9,82:1; Sol sobre Areia 1,46:1, por isso nunca texto nem borda única |
| Erro | `#B42318` | mensagem e borda de erro | sobre Papel 6,57:1 |
| Areia | `#F3F7F6` | fundo da página | superfície base |
| Papel | `#FFFFFF` | cartões e campos | superfície elevada |

Escala de espaçamento base 8 px (4, 8, 16, 24, 32, 48, 72). Raio: 12 px em cartões, 8 px em campos e botões, 999 px só em selos (hierarquia de raios, não um raio uniforme).

## Tipografia

- Títulos: Bricolage Grotesque, peso 700, escala 1,25 a partir de 18 px no celular.
- Corpo e interface: Atkinson Hyperlegible, 17 px no celular, linha 1,55, medida de 60 a 70 caracteres.
- Os dois nomes são famílias do Google Fonts; conferir licença e disponibilidade na data do uso (Inferido: conhecimento do domínio, não consultado nesta sessão). Auto-hospedar com `font-display: swap`.

## Layout

```text
[ Cabeçalho: logo | botão "Agendar" ]
[ Hero: foto real da equipe com um paciente + 1 frase + botão "Agendar pelo WhatsApp" ]
[ Faixa de confiança: horário, endereço, "responde em média…" apenas se o cliente fornecer o dado ]
[ Serviços: lista de 4 itens com pesos diferentes (consulta e vacina em destaque) ]
[ Como funciona: 3 passos numerados ]
[ Equipe: nomes e CRMV reais fornecidos pelo cliente ]
[ Onde estamos: endereço em texto + mapa com alternativa em texto ]
[ Rodapé ]
```

Barra fixa de ação no rodapé do celular. Ela pode cobrir o elemento focado: reserve `scroll-padding-bottom` igual à altura da barra para atender ao critério 2.4.11 (foco não obscurecido).

## Princípios

1. Proximidade antes de ornamento: foto real, endereço e horário acima da dobra.
2. Uma ação, em todo lugar: o botão do WhatsApp é a única cor de ação; Sol nunca vira botão.
3. Calor sem fofura forçada: nada de pegadas e ossos como moldura; o cuidado aparece em fotografia e texto.

## Estados obrigatórios

- Sem JavaScript ou sem WhatsApp instalado: o botão é um link `https://wa.me/…` com número real do cliente; se o aplicativo não abrir, mostrar o número em texto para copiar.
- Foto não carregou: bloco com cor Areia e `alt` descritivo.
- Nome de pet com 40 caracteres em formulário auxiliar: quebra de linha sem corte.
- Texto aumentado em 200% e viewport de 320 px: sem rolagem horizontal.

## Movimento

Um único momento: o hero entra com fade e deslocamento de 8 px em 300 ms, easing de saída. Tudo atrás de `@media (prefers-reduced-motion: no-preference)`. Faixa de duração e easing são regras de polegar (Inferido; não há diretriz oficial lida).

## Acessibilidade e idioma

WCAG 2.2 AA; `lang="pt-BR"`; alvo de toque de 44 px no celular (piso normativo 24 px CSS); foco com contorno Musgo de 2 px e deslocamento de 2 px; link do mapa com texto descritivo. Tratamento "você", tom acolhedor e direto (Suposição: não há guia de voz).

## Trocas na revisão contra o genérico

| Escolha inicial | Problema | Troca |
| --- | --- | --- |
| Gradiente roxo no hero | default de modelo, sem relação com o assunto | foto real sobre fundo Areia |
| Três cartões iguais com ícone em círculo | layout de template | lista de serviços com pesos diferentes |
| Creme com terracota | deriva conhecida do modelo | Areia fria com Musgo; Sol só decorativo |
| Depoimentos com estrelas | não há depoimentos reais fornecidos | removido até o cliente enviar nomes e falas reais |

## Suposições e pendências

- Suposição: tom e tratamento "você" (sem guia de voz).
- Pendência: fotos, CRMV, horário, endereço e prazo de resposta vêm do cliente; nada disso foi inventado.
- Não renderizado: este plano não foi aberto em navegador; a revisão visual acontece depois do build.
