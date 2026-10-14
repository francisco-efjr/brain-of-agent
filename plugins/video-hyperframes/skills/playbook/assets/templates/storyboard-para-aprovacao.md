# TP-07 · Storyboard para aprovação (pausa 1, gate G5)

Uso: a skill `software-explainer-storyboard` mostra este bloco no chat, preenchido, antes de construir qualquer quadro. É o "plano frame a frame" que o usuário aprova. Mostre também o `frame.md` resumido (fundo, tinta, acento, famílias, pisos). Nada é construído sem a resposta às duas perguntas do fim. Em modo companion ou com `storyboard: yes`, o "go" vale só para o plano exibido; mudou o plano, peça de novo.

## Plano

**Este vídeo mostra a [público] que [mensagem].**

- Rota e estrutura: [faceless-explainer] · [concept-explainer com processo / how-to-process / listicle / story-explainer]
- Palco: [descrição do palco único] · Fio persistente: [a tarefa ou o dado que atravessa as camadas, nasce no quadro N]
- Transição primária: [push-slide 0,4 s / crossfade] · acento (no máximo um): [onde]
- Duração total: ~[N] s (soma dos quadros: [N] s) · formato [1920x1080] · som: [mudo total / silencioso com SFX / voz local]
- Gancho: [tipo, na língua do espectador, nunca definição genérica]; o valor aparece até o 2º beat

| Quadro | Tempo | Título | Peças que entram (em ordem) | SFX | Por quê (liga à tese) |
| --- | --- | --- | --- | --- | --- |
| F01 | 0-8 s | [gancho] | [âncora; 2,2 s: linha 1; 4,5 s: linha 2] | [nenhum] | [abre a tensão] |
| F02 | 8-20 s | [...] | | | |

Conferências feitas: todo número vem do ledger (ids [..]); nada da lista "não pode aparecer"; cada linha de texto fica na tela >= 2,5 s; a última revelação de cada quadro entra até `duração - 2,5 s`.

**Riscos:** [quadros demais (acima de 8, revisado pelo `storyboard-reviewer`: sim/não); texto denso em vídeo mudo; número sem fonte (slot `— figure —` no quadro N)].

## Duas perguntas (respondidas juntas)

1. Aprova o plano ou quer mudar algo? (diga o quadro e o que muda)
2. Quer ver sketches primeiro (recomendado: layout confirmado sem movimento antes do build) ou pular para a construção?

Depois da resposta, as skills seguem o pipeline oficial; o render continua dependendo do seu ok ao preview (gate G9).
