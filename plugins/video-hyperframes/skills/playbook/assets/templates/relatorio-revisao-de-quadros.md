# TP-04 · Relatório de revisão de quadros

Uso: preenchido pela skill `video-frame-review` no gate G8, com os achados do `frame-reviewer`, do `fact-privacy-checker` e, só se houver sintoma, do `composition-reviewer`. O agente principal grava em `<pasta-do-video>\relatorios\AAAA-MM-DD-revisao-de-quadros.md` (sufixo `-r2`, `-r3` por rodada; fora de `projeto\`, de `renders\` e de `.hyperframes\`, que o CLI pode limpar). Os agentes não gravam: devolvem o relatório com `Caminho sugerido` e `Status`, e o agente principal os consolida aqui. O relatório não edita nada: as correções são feitas depois, pelo agente principal, pela menor edição segura. Cada achado tem evidência (`arquivo:linha` ou caminho do PNG); movimento e timing não se julgam por imagem estática.

## Cabeçalho

```text
Caminho sugerido: <pasta-do-video>\relatorios\AAAA-MM-DD-revisao-de-quadros.md
Status: concluído | rascunho | não revisado
```

- Projeto: `<pasta-do-video>\projeto` · data: [AAAA-MM-DD] · rodada: [1 de até 3]
- CLI: `hyperframes@0.8.154` · skills oficiais: [plugin / clone] no commit [hash] · invólucro: `hfs`
- `check`: comando [`hfs check` / `hfs check --strict`] · erros [N] · avisos [N] · **`browserSkipped`: [true/false]** · seções de layout e contraste: [preenchidas / vazias]
- `check` com `browserSkipped: true` ou seções vazias **não é limpo**: corrija o lint e rode de novo antes de seguir.
- Snapshots: id [..] · pontos médios e fim − 0,3 s de cada quadro [t1, t2, ...] · contact sheet: `<pasta>\projeto\.hyperframes\artifacts\snapshots\<id>\contact-sheet.jpg`
- Impressão digital da árvore avaliada (compositions, assets, index.html, frame.md): [SHA-256] (o `video-render-deliver` compara com a árvore no momento do render)

## Achados por quadro

Classe: **bloqueante** (impede preview ou render), **importante** (corrigir antes da entrega), **menor** (opcional).

| Quadro | Achado | Evidência | Classe | Ação mínima |
| --- | --- | --- | --- | --- |
| [03] | [número "3 níveis" no quadro difere de F-001 do ledger] | [compositions/frames/03-roteador.html:41; fonte-dos-fatos.md F-001] | [bloqueante] | [corrigir o texto para o valor do ledger] |

Sem achados num quadro, escreva "sem achados" com o que foi conferido (texto, números, cores, tamanhos, zona da legenda, fio, lista negativa).

## Checklist de entrega (11 itens, V-61)

| # | Item | Estado | Evidência |
| --- | --- | --- | --- |
| 1 | A abertura cria pergunta, tensão ou surpresa | [ok / falha / Não verificável] | [quadro e trecho] |
| 2 | A ideia principal está clara até a segunda cena | | |
| 3 | Cada cena avança um mecanismo, passo ou exemplo | | |
| 4 | Número e fato batem com a fonte; nenhum número inventado | | [ids do ledger] |
| 5 | O fecho diz a frase que o público deve lembrar | | |
| 6 | Nenhum quadro despeja tudo nos primeiros 25% e congela | | [timeline] |
| 7 | O último segundo não é quadro congelado por falta de plano (faceless: jitter sutil, não respiração) | | [timeline] |
| 8 | Nenhum texto abaixo do piso de legibilidade do destino | | [px estimados] |
| 9 | Negativos da direção respeitados (bokeh, gradiente roxo-azul, chrome de navegador, cursor real, loops infinitos) | | |
| 10 | Snapshots e contact sheet inspecionados | | [ids] |
| 11 | Render só depois de aprovação explícita (gate seguinte) | pendente | |

## Falsos positivos conhecidos

- `text_box_overflow` de 1 a 4 px em `#caption-word-*` ou `.caption-line`: só aja se o achado citar elemento de quadro (`#el-NN-*`).
- Outros descartados nesta rodada: [id do achado, motivo].

## Movimento e timing (pela timeline, não pela imagem)

[janelas por cena de `hfs timeline --json`; reveals espalhados; selagem do último quadro. Onde faltar dado: "Não verificável".]

## Veredito

[pronto para preview / não pronto, com N bloqueantes] · correções feitas nesta rodada: [lista] · restante: [lista]. Após 3 rodadas sem sucesso, pare e reporte o que falta.

## Verificado, Inferido, Não verificável

- Verificado: [o que tem saída de comando ou leitura de arquivo nesta sessão]
- Inferido: [estimativas visuais de cor e tamanho, rotuladas]
- Não verificável: [animação, ritmo, legibilidade em tela real]

Independência: revisão feita por agentes da mesma família do autor; não é validação externa.
