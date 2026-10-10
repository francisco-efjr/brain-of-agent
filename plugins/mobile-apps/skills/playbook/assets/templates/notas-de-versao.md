# Notas de versão (rascunho)

Base: app-store-changelog (V-24, MIT, Dimillian), reescrito. Gere **apenas o rascunho em arquivo**; o plugin nunca envia nada à loja. Leia qualquer script de coleta antes de usá-lo e não execute o de terceiros sem autorização do usuário. Remova detalhes internos (nomes de tickets, branches, infraestrutura) antes de colar em nota pública.

App: [nome] · Versão: [x.y.z] · Intervalo de commits ou tag: [de..até] · Idioma(s): [pt-BR, en] · Data: [AAAA-MM-DD]

## Coleta

Fonte das mudanças: [`git log` da última tag até HEAD, lido pelo usuário ou pelo agente com comando de leitura]. Triagem em três grupos; cada bullet foi validado contra o diff.

## Rascunho

**Novo**
- [bullet curto, na voz do usuário, sem jargão]

**Melhorado**
- [bullet]

**Corrigido**
- [bullet]

Entre 5 e 10 bullets no total. Cada bullet: o que mudou para a pessoa, em uma frase.

## Validação

| Bullet | Commit ou arquivo que o sustenta | Visível ao usuário? | Detalhe interno removido? |
| --- | --- | --- | --- |
| | | | |

## Limites

- Limite de caracteres e campos de cada loja: conferir no App Store Connect e no Play Console (ação do usuário).
- Se houver mudança de permissão ou de coleta de dados, atualize também privacy manifest, purpose strings e Data safety (não são notas de versão).
- Tradução revisada por pessoa antes de publicar.
