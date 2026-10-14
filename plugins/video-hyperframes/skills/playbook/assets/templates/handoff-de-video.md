# TP-10 · Handoff de projeto de vídeo

Uso: gere ao fim de uma sessão, antes de a janela encher ou ao entregar para outra pessoa ou para o orquestrador. Quem retoma lê este arquivo, o `BRIEF.md` e o `STORYBOARD.md`; o estado do projeto manda (V-33). Não inclua segredos, valores de variáveis nem texto de roteiro desnecessário. Adaptado do template `handoff-checkpoint` do brain-of-agent (MIT, do mesmo autor deste plugin).

## Cabeçalho

- Projeto: `<pasta-do-video>` · rota: [..] · escopo autorizado: [planejar / até o preview / com render]
- Revisão do ambiente: CLI `hyperframes@0.8.154`; skills oficiais em [plugin / clone] no commit [hash]; data: [AAAA-MM-DD]
- Estado da árvore: [impressão digital SHA-256 de compositions, assets, index.html e frame.md, ou "sem versionamento"]

## Entregue

| Gate | Estado | Artefato | Evidência | Limitação ou próxima ação |
| --- | --- | --- | --- | --- |
| G2 especificação | [feito / pendente] | `DECISOES.md`, `projeto\BRIEF.md` | [caminho] | |
| G3 fonte e fatos | | `TEXTO-FONTE.md`, `fonte-dos-fatos.md` | | |
| G4 design | | `tokens.json`, `frame.md` | | |
| G5 storyboard (pausa 1) | | `STORYBOARD.md` | [aprovado em AAAA-MM-DD, versão do plano] | |
| G6 áudio | | `audio_meta.json` ou "mudo total" | | |
| G7 construção | | `compositions\frames\*.html`, `index.html` | | |
| G8 qualidade | | `relatorios\AAAA-MM-DD-revisao-de-quadros.md` | [`check` com `browserSkipped`: ..] | |
| G9 preview (pausa 2) | | [URL, PID] | [aprovado para a árvore de impressão digital ..] | |
| G10 render | | `renders\[nome].mp4`, `COMO-RENDERIZAR.md` | [saída do `ffprobe`] | |
| G11 auditoria | | `relatorios\AAAA-MM-DD-seguranca-da-execucao.md` (TP-08) | | |

## Verificado, Inferido, Suposição, Não verificável

- Verificado: [o que rodou nesta sessão, com a saída]
- Inferido: [..]
- Suposição: [..]
- Não verificável: [PT-BR de ponta a ponta, desempenho do render, ...]

## Decisões e fontes de verdade

[decisões tomadas e por quê; opções descartadas; arquivos que mandam: BRIEF, STORYBOARD, frame.md, ledger]

## Pendências, riscos e impedimentos

- Downloads aguardando "sim": [nome, origem, tamanho, destino]
- Perguntas ao dono: [..]
- Riscos: [..]
- Checks invalidados por mudanças posteriores: [..]

## Estado do que está rodando

Preview: [URL em 127.0.0.1, PID, como parar com `Stop-Process -Id <PID>` / encerrado]. Arquivos temporários ou caches a limpar: [..].

## Próxima ação concreta

[uma frase com o comando ou a pergunta exata]

## Ao retomar

Confirme a árvore do projeto (impressão digital ou datas) e o `BRIEF.md` antes de assumir que este estado continua válido. Aprovações dadas antes de uma mudança na árvore não valem para a versão nova: peça de novo. Rode o preflight de novo se a sessão for nova (as variáveis de sessão não persistem).
