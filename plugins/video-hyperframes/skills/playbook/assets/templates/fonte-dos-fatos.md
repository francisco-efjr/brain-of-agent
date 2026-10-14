# TP-03 · `fonte-dos-fatos.md` (ledger de afirmações)

Uso: grave em `<pasta-do-video>\fonte-dos-fatos.md`. É a única fonte de números, nomes e afirmações do vídeo. O storyboard e o roteiro citam os **ids** daqui; o `fact-privacy-checker` compara cada texto de tela com este arquivo. Regra: nenhum número, nome ou cliente sem linha neste ledger; sem fonte, o slot fica `— figure —` e o dono é avisado (V-61, V-66). Não arredonde nem "melhore" valores.

## Cabeçalho

- Sistema ou tema: [nome público]
- Origem do material: [arquivos informados] · revisão ou commit: [hash curto ou "sem versionamento"] · data da leitura: [AAAA-MM-DD]
- Quem aprovou o texto-fonte: [dono] em [AAAA-MM-DD]

## Afirmações

| id | afirmação (atômica) | origem (arquivo:linha ou "informado pelo dono em AAAA-MM-DD") | status | pode aparecer? |
| --- | --- | --- | --- | --- |
| F-001 | [o roteador classifica o pedido em 3 níveis de prioridade] | [docs/roteamento.md:12] | Verificado | sim |
| F-002 | [pedidos que falham 3 vezes vão para a fila de mortas] | [src/worker.py:88] | Verificado | sim |
| F-003 | [o painel mostra a profundidade da fila em tempo real] | [informado pelo dono em AAAA-MM-DD] | Inferido | sim, com ressalva "informado" |
| F-004 | — figure — (ganho de latência do roteamento) | sem fonte | Não verificado | não até haver fonte |

Status: **Verificado** (li a origem e confere), **Inferido** (dedução de material lido), **Suposição**, **Não verificado** (sem origem). "Pode aparecer" decide sozinho o que vai ao vídeo: `não` ou `Não verificado` nunca vira texto de tela.

Regras de escrita: uma afirmação por linha; número com unidade e escopo ("3 tentativas por pedido", não "poucas tentativas"); contagem agregada em vez de dado individual; texto exato entre aspas quando for copy literal; um id novo a cada mudança de valor (o antigo fica riscado, não apagado).

## Não pode aparecer (classes; sem valores)

- Caminhos de máquina e nomes de usuário do sistema operacional
- E-mails, telefones, tokens, chaves, segredos e trechos de `.env`
- Nomes internos de aplicativo, branch, PR, repositório privado e cliente não autorizado
- Achados de segurança e vulnerabilidades ainda abertas
- Percentuais de uso de conta e dados de cobrança
- Prints reais de terminal, painel ou conversa
- Outros, por decisão do dono: [lista]

Autorização por item: se o dono liberar algo desta lista, registre a linha, o id e a data aqui; sem registro, vale a proibição.

## Lacunas e perguntas ao dono

| # | Pergunta | Recomendação | Bloqueia |
| --- | --- | --- | --- |
| 1 | [qual é o valor oficial de ...?] | [usar gancho qualitativo até haver fonte] | [quadro 5] |

Fonte da regra: HyperFrames (HeyGen, Apache-2.0), commit `bf4cf860` (`faceless-explainer.mdx`, `code-editorial/FRAME.md`: V-61, V-66); modelo de redação própria.
