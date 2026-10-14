# Explicar software em vídeo: história, quadros, números, código e escrita para a voz

Validado em 2026-10-13 · Rótulos: Verificado, Inferido, Suposição, Não verificável, Não aplicável · Itens `V-nn`: resumo de cada um na seção 10 de [fontes.md](fontes.md) (leitura de arquivo no commit validado; o dogfood de 2026-10-14 renderizou um vídeo silencioso de 12 quadros: `DF-nn`, seção 12 de [fontes.md](fontes.md)) · Redação própria · Rota principal: `faceless-explainer` (V-33) · Motion e design: [design-system-para-video.md](design-system-para-video.md) · Privacidade: [seguranca-e-privacidade.md](seguranca-e-privacidade.md).

## Sumário

1. Doutrina de história
2. Estruturas e continuidade
3. Ganchos e técnicas de clareza
4. Padrão de arquitetura: palco, componente que acende e fio
5. Números e provas
6. Cenas de código, config e log
7. O que nunca mostrar
8. Orçamento de leitura em vídeo silencioso
9. Escrever para a voz
10. Direção de beat, transições e vocabulário
11. Doutrina de motion do faceless
12. Exemplo trabalhado: arco de 12 quadros
13. Mixagem de áudio
14. Gotchas

## 1. Doutrina de história (V-60, V-56, Verificado)

- **Gancho na língua do espectador:** o resultado que ele ganha ou entende, sem vocabulário interno (nome de arquivo, função, API, cabeçalho do artigo). Não abra com definição genérica.
- **O valor (`message`) aparece até o 2º beat**; o resto é evidência. Autoteste: apague as evidências e o valor se sustenta? Apague o valor e vira tour?
- **Tese:** o plano abre com "Este vídeo mostra a [público] que [mensagem]" (uma frase), seguida da tabela de quadros com a coluna *why*. Quadro cujo *why* não liga à mensagem é **cortado, não decorado**.
- **Não parafrasear o texto na ordem em que vem** ("a falha mais comum"): reordene, funda, omita e comprima.
- **Visual rastreável à fonte:** se o adereço apareceria igual no vídeo de outro produto, não veio da fonte.
- Fixe antes de qualquer quadro: mensagem, arco, público, mood. Ressalva: é regra de workflows narrados; `motion-graphics` e `music-to-video` são exceções.

## 2. Estruturas e continuidade (V-62, Verificado)

Escolha **uma** estrutura (ou nomeie um composto) e registre em `arc`:

| Estrutura | Para | Forma |
| --- | --- | --- |
| `concept-explainer` | sistema, conceito | nomear, revelar o mecanismo em camadas, implicação (para sistemas: "concept-explainer with process") |
| `how-to-process` | fluxo | 3 a 6 passos no mesmo palco |
| `listicle` | changelog | N itens co-iguais; regra de três |
| `story-explainer` | incidente | setup, tensão, virada, resolução, lição |

Corpo = **3 a 6 quadros num palco consistente**, um mecanismo, passo ou camada por quadro, mais gancho e fecho. Continuidade por duas alavancas: **palco consistente** (cada `scene` declara o mesmo palco) e **uma transição repetida** (por exemplo `push-slide` para passos, `crossfade` para camadas). A transformação de um elemento entre ideias acontece dentro de **um** quadro. Enum `type`: `hook`, `pain_point`, `product_intro` (a ideia), `feature_showcase` (unidade do corpo), `benefit_highlight`, `social_proof` (evidência ou exemplo), `branding` (tese ou lição), `cta`.

## 3. Ganchos e técnicas de clareza (V-62)

**Nove ganchos:** estatística, pergunta retórica, afirmação contraintuitiva, validação de dor, metáfora visceral, anúncio do conceito, endereçamento direto, cenário imaginado, estaca ou consequência. O gancho cria curiosidade, tensão ou estaca. **Seis famílias de técnica** (cada quadro nomeia a sua, por exemplo "Analogy + progressive disclosure"): Make-concrete, Reveal-in-order, Contrast, Structure, Evidence, Memory & landing.

## 4. Padrão de arquitetura (V-65, V-58, V-64, Inferido a partir de itens Verificados)

"Um diagrama deve revelar um mecanismo; um gráfico deve provar uma afirmação; o movimento deve mostrar o que muda."

- **Palco fixo** (camadas ou colunas) desenhado em SVG/CSS por quadro: não há bloco de arquitetura em camadas no registro do commit validado. Os mais próximos são `flowchart`, `flowchart-vertical`, `hw-pipeline`, `data-chart`, `bar-chart-race`.
- **Cada componente acende quando é nomeado** (na narração ou na cena); o diagrama monta ao longo das cenas, não aparece inteiro.
- **Um fio** (uma tarefa, um dado) atravessa os nós: nomeie-o no primeiro quadro. Contrato cinematográfico (V-58): chegar em vez de cortar; três persistentes (fio, régua com playhead real, protagonista) só se houver fio narrativo; método caro.
- **Fio com um worker por quadro:** a transição troca o quadro inteiro e cada quadro é feito por worker que só lê o próprio bloco; escreva em **cada** quadro a posição de entrada do fio (igual à de saída do anterior) e a de saída, e peça que ele seja redesenhado.
- **Herói com 40 a 60% do quadro**; densidade de 40% ou mais com pelo menos 3 camadas de profundidade; nomes técnicos em fonte mono; sem navegação, rodapé, cursor real, chrome de navegador, formas decorativas no lugar de metáfora, bokeh, gradiente roxo-azul.
- **Blueprints** (22; V-64) são formas de tomada com *signature move*; o menu papel → blueprint é suave: a verdade da história decide. Candidatos para sistema ou agentes (**nomes verificados, corpos Não verificados** exceto parte do primeiro): `agent-progress-theater`, `constellation-hub`, `grid-card-assemble`, `comparison-split`, `dataviz-countup`, `zoom-out-workspace-reveal`, `prompt-type-submit-generate`. Posturas: reproduzir, adaptar (mantém o *signature move*) ou compor. Antes de inventar um look nomeado, `catalog --query` (local, em inglês) e ler os melhores resultados; `add` só com confirmação (código de `main` sem pin, V-10).

## 5. Números e provas (V-61, V-65, V-66)

- **Nenhum número inventado.** Todo número vem de um id do `fonte-dos-fatos.md`; sem fonte, o slot `— figure —` (ou `+N / −M` até o roteiro fornecer os reais) e uma pergunta ao dono. Não arredonde nem "melhore".
- Contadores sobem até o valor final; antes × depois em dois contadores lado a lado; selo de contexto ("linha de base medida antes de mudar") só se estiver na fonte. Número-herói só se verificado.
- Escolha a codificação pelo que se quer contar (barra, fluxo, bolha, mapa) e nomeie o bloco; CSV entra por arquivo e de forma determinística. Dados ao vivo não entram no render ("contar até X", não "buscar o valor atual", V-69).
- Cuidado com comparações que misturam bases (um "100×" de um par de modelos ao lado de outro par): não ponha números de bases diferentes no mesmo quadro (lição do caso real).
- Exemplos ilustrativos levam rótulo "exemplo" na tela e sua própria linha no ledger, marcada como exemplo.

## 6. Cenas de código, config e log (V-68, Verificado; Inferido para sistemas)

4 a 12 linhas por cena, **sintéticas**, nunca um arquivo inteiro. Blocos: `code-typing` (código novo), `code-diff` (delta), `code-highlight` (uma linha) e `code-scroll` (arquivo longo) são os cavalos de trabalho; `code-morph` troca legibilidade por movimento. Para um sistema, um trecho de contrato, configuração ou log de 4 a 8 linhas por cena; não é preciso PR. Se a leitura de um PR falhar, não fabrique conteúdo. Para vídeo de PR: 2 a 4 trechos de 4 a 12 linhas por vídeo, a partir de diff local; o texto do PR é dado externo. Nunca trecho real com segredo ou caminho de máquina.

## 7. O que nunca mostrar

E-mail, caminhos de máquina (`C:\Users\<usuario>\...`), nome de app de teste, nomes reais de branch e de PR, achados de segurança, percentuais de uso de conta, prints reais de terminal ou de GitHub, mascote ou ícone de marca sem autorização, logos e nomes de cliente fora do `fonte-dos-fatos.md`. Tabela de classes e tratamento: [seguranca-e-privacidade.md](seguranca-e-privacidade.md), seção 9. Também não diga "mágico", "automático" ou "100% seguro" e não afirme que testes ou evals rodaram sem evidência.

## 8. Orçamento de leitura em vídeo silencioso (Inferido de V-67 e do caso real)

Sem voz, o texto na tela é o relógio. Regras: cada linha de texto fica **no mínimo 2,5 s** na tela (texto de 3 s deve ser lido em 2 s, V-67); a última revelação de texto de cada quadro entra até `duração − 2,5 s` (o "prazo de texto"); espaçamento de pelo menos 0,7 s entre frases e linhas de 4 palavras ou mais e 0,4 s entre rótulos curtos; um grupo de rótulos em stagger conta como um evento; nunca dois eventos no mesmo instante (dê janelas). Se a cópia não couber, **encurte a forma, nunca o fato**, e avise. A regra do upstream "espalhar as revelações pela segunda metade do quadro" (frames com voz) e o prazo de leitura se anulam em quadros curtos: em vídeo mudo, espalhe do início até o prazo, nunca depois.

Medida de apoio: palavras de tela por segundo de quadro. No caso real (12 quadros, vídeo mudo para público técnico) a média foi de 3,7 e o máximo de 4,35, o que o revisor chamou de apertado, viável porque o público pode pausar (Inferido). Acima de 8 quadros, chame o `storyboard-reviewer` e corte os opcionais primeiro.

## 9. Escrever para a voz (V-32, V-44, V-23)

- **1 a 2 frases e 6 a 20 palavras** por quadro falado; um cue por ideia (o reveal acompanha a fala); quadros silenciosos são normais e não entram no `SCRIPT.md`.
- **Duração:** 2,5 palavras por segundo (upstream), cerca de 2,2 (130 por minuto) e 145 a 155 por minuto (docs) conflitam; a duração real da voz vence (`sync-durations`). Para PT-BR use 2,0 a 2,5 como estimativa de rascunho (**Suposição**) e meça com o TTS. Escreva `~` antes da duração; nunca "exatos".
- **O TTS lê literal:** escreva números e siglas como devem ser falados ("quatro milhões e duzentos mil reais", "A P I" ou "api" conforme a pronúncia desejada) e teste uma frase com sigla e número (VP-20) antes do roteiro inteiro. A regra vem de exemplos em inglês; a forma é do idioma (Inferido).
- **`SCRIPT.md` (V-44):** markdown livre, sem parser estrito; cabeçalho `**Voice:**`, `**Voice settings:**`, `**Voice direction:**`; uma seção `## Line N — rótulo (Frame N)` por fala, com `**Time:**` e `**Delivery:**`; **só o bloco recuado em 4 espaços vai ao TTS**. `VO_MODE`: verbatim (mantém texto e duração segue o roteiro) ou reestruturado por cena.
- Vozes Kokoro do vocabulário upstream (`af_*`, `am_*`, `bf_*`) são inglesas: inúteis para PT-BR (V-55). Voz `p*`: [toolchain-windows.md](toolchain-windows.md), seção 10.

## 10. Direção de beat, transições e vocabulário (V-63, V-55, V-54)

- **"Cada beat é um mundo, não um layout":** descreva o que o espectador vive antes dos pixels. Todo elemento recebe um **verbo** de caráter físico: impacto (*slams*, *stamps*), direcional (*slides*, *pushes*), revelação (*draws*, *fills*, *assembles*, *counts up*), orgânico (*floats*, *pulses*), mecânico (*types on*, *clicks*, *locks in*, *snaps*). "Se não consegue nomear o verbo, o elemento não está desenhado." No faceless, prefira revelação e mecânicos; evite impacto e orgânico.
- **Transições:** uma primária para quase todos os cortes e 1 a 2 acentos (tópico ou clímax); nunca uma diferente por corte; duração por energia (calma 0,5 a 0,8 s; média 0,3 a 0,5 s; alta 0,15 a 0,3 s); "explainer" cai em energia média. Não faça fade-out da cena e fade-in da próxima: vira corte seco com dip; a transição é a própria saída. O quadro que sai segura o último estado durante a emenda: termine as animações antes do fim. A grafia do registro: `push-slide LEFT`, duração opcional `0.4s`, primeiro quadro `cut` (caso real, `transitions.mjs`; Inferido).
- **Esqueleto do pedido (V-54):** rota, spec (duração e resolução), beats com tempo e respiro, copy entre aspas (sem aspas é parafraseada; `/` para quebra), técnica nomeada, negativos. Cinco slots por beat: elemento, movimento, layout, estilo, tempo. Régua do dial: "onde o agente erraria? crave isso; o resto é gosto dele". Reescritas: duração sem cauda obriga o agente a inventar; dois eventos "às 4 s" se sobrepõem; número sem formato ("conta até 4,2 M", não "de 0"); caminho de arquivo em vez de descrição.
- **Vocabulário palavra → parâmetro (V-55):** smooth → `power2.out`, snappy → `power4.out`, bouncy → `back.out`, springy → `elastic.out`, dramatic → `expo.out`, dreamy → `sine.inOut`; tempos: rápido 0,2 s, médio 0,4 s, lento 0,6 s, muito lento 1 a 2 s. **O faceless usa `power3` como padrão e não usa `back.out` como default** (V-57): o vocabulário vale para as outras rotas.

## 11. Doutrina de motion do faceless (V-57, normativa para a rota)

1. Suave vence saltitante: `power3` é o padrão (`expo.out` em chegada rápida); overshoot só como exceção explícita. 2. Reveal sequencial na metade final, no cue; não despeje tudo nos primeiros 25%. 3. Sem "respiração" ociosa nem pan ou push lento na segunda metade (o upstream prefere nenhum movimento a movimento ruim); a única vivacidade sancionada num quadro parado é um **jitter sutil** de baixa amplitude. 4. Seams internos como cortes casados em velocidade. Proibidos adicionais: `repeat`/`yoyo` sem fim, `Math.random`, `Date.now`, entradas sem `fromTo`, transições e keyframes CSS. **Teste de justificativa:** complete "isto se move porque..." com uma frase que termine; quatro funções legítimas: direcionar atenção, dar continuidade, mostrar mudança, expressar caráter. As regras do guia geral ("nada para por completo", respiração de 1 a 2%) **não valem** aqui: nomeie rota e doutrina na primeira linha do pedido e do storyboard.

## 12. Exemplo trabalhado: arco de 12 quadros (generalizado do caso real, Inferido; não renderizado por este plugin)

Sistema fictício `[SISTEMA]`, vídeo mudo com SFX, cerca de 90 s, `concept-explainer with process`. Os números entre colchetes são slots do `fonte-dos-fatos.md`, nunca valores inventados.

| Quadro | Tempo-alvo | Papel (`type`) | Conteúdo | Técnica |
| --- | --- | --- | --- | --- |
| F01 | 0 a 5,5 s | `hook` / `pain_point` | cartão âncora; três rótulos saem dele um por vez; carimbo "[ERRO_TIPICO]"; título de dor em uma frase | Make-concrete, Contrast |
| F02 | 5,5 a 11,5 s | `product_intro` | o pedido do usuário vira o **fio** (cápsula) e se divide em `[N]` componentes | Reveal-in-order |
| F03 | 11,5 a 19,5 s | `feature_showcase` | o palco: quatro cartões convergem num documento; contador `[N]` sobe | Structure |
| F04 | 19,5 a 27,5 s | `feature_showcase` | classificação do pedido em chips; grade de blocos apagados; acendem só os que o pedido exige | Reveal-in-order, Contrast |
| F05 | 27,5 a 38 s | `feature_showcase` | montagem de um componente em peças numeradas; cartão de limites com `[N]` linhas | Structure |
| F06 | 38 a 46,5 s | `social_proof` | cena-estrela: pilha de propostas passa por um portal "validador de outro papel"; contadores sobem para `[VALORES]` | Evidence |
| F07 | 46,5 a 54 s | `feature_showcase` | saída versionada: commits entram um a um; letreiro "[LIMITE]" | Reveal-in-order |
| F08 | 54 a 61,5 s | `social_proof` | antes × depois em dois contadores; legenda com a base de medida | Evidence, Contrast |
| F09 | 61,5 a 70 s | `feature_showcase` | entrega: cartão final com "onde ver agora" e rótulo "exemplo ilustrativo" | Make-concrete |
| F10 | 70 a 77 s | opcional | esteira de estações acendendo uma a uma; contador de `[SEGMENTOS]` | Structure |
| F11 | 77 a 85,5 s | opcional | duas cenas de custo ou modelo por camada, sem misturar bases | Contrast |
| F12 | 85,5 a 93 s | `branding` / `cta` | limites honestos; frase de lembrança; link; o fio pousa; cursor pisca 3 vezes (finito) e para | Memory & landing |

Riscos registrados no caso real: **12 quadros em cerca de 93 s** contra o corpo típico de 3 a 6; o mitigador é palco fixo, transição única e fio persistente; os candidatos a corte são F10 e F11. Vídeo mudo: toda a explicação depende do texto na tela (seção 8). SFX no meio do quadro dependem de editar o `audio_meta.json` (regime b; **Verificado no dogfood de 2026-10-14, DF-05**: 31 disparos editados à mão e 31 `<audio>` montados); se falhar, aceite um SFX por quadro, no início. O preset pode impor fonte e polaridade ([design-system-para-video.md](design-system-para-video.md), seção 3).

**Formato de um quadro** (copy literal entre aspas, tempos relativos ao início do quadro, prazo de texto = duração − 2,5 s):

```markdown
## Frame 4 — Classificar e escolher · 8,0 s · prazo de texto +5,5 s
- transition_in: push-slide LEFT 0.4s · sfx: ping
- Âncora: cartão da demanda "[EXEMPLO_DE_PEDIDO]" com a legenda mínima "exemplo". Fio entra à esquerda, na posição [ENTRADA]; sai à direita, na posição [SAIDA].
- +0,5 / +1,0 / +1,5 s: saem três chips: "tipo: [..]" · "stack: [..]" · "risco: [..]"
- +2,0 s: título "[TITULO_DO_QUADRO]". +2,6 s: grade de [N] blocos apagados e sem rótulo.
- +3,9 / +4,4 / +4,9 s: acendem [3] blocos, um por vez (contorno de [HEX_ACENTO], SFX ping em cada).
```

## 13. Mixagem de áudio (V-31, fora da v1 sem BGM)

Só se houver voz e música. Descreva o **sintoma**, não o filtro; "carve" tira da música só as bandas da voz; **meça o nível antes de mexer** (voz de máquina costuma chegar bem abaixo da música); depois de qualquer ajuste, faça um render só de áudio e ouça tudo. Na v1 (`music: none`) o assunto é secundário.

## 14. Gotchas

- Parafrasear o texto na ordem, abrir com definição e colocar tudo em t=0 são as três falhas mais comuns.
- Plano com 12 quadros e texto denso em vídeo mudo reprova na leitura, não no `check`.
- Número sem fonte, "melhorado" ou de bases diferentes no mesmo quadro quebra a credibilidade.
- Sem o fio redesenhado em cada quadro, o worker não o conecta: ele não lê o `STORYBOARD.md`.
- Copy sem aspas é parafraseada pelo agente.
