# Handoff e checkpoint SRE

Template T-13. Adaptado de `brains/fullstack/assets/templates/handoff-checkpoint.md` do brain-of-agent (conteúdo próprio, MIT) com campos de incidente e de modo SRE-COMPLETO. Use em rodízio de plantão (a cada ~4 h em incidente longo), em sessão longa antes de a janela de contexto encher, ou ao encerrar. Não inclua segredos nem dados pessoais desnecessários. Estado pode estar desatualizado: quem assume confirma revisão, workspace e sistema antes de agir.

**Objetivo e escopo autorizado:** [o que foi pedido; o que não pode mudar; ações externas autorizadas e por quem]
**Ambiente e acesso:** [local/staging/produção; somente leitura / escrita; identidade usada; o que é Não verificável por falta de acesso]
**Revisão atual e workspace:** [commit/versão do serviço; arquivos alterados e preservados]
**Incidente (se houver):** [ID, severidade, IC/OL/CL atuais, próximo checkpoint UTC]
**Fontes de verdade e decisões:** [documentos, dashboards, decisões tomadas e por quem]

## Leituras e cobertura

| Referência/fonte | Estado (lido / parcial / ausente) | Decisão extraída |
| --- | --- | --- |
| [checklist-completo.md] | [lido] | [..] |

## Estado dos itens

| Item | Estado | Alteração | Evidência (comando/consulta e saída) | Limitação / próxima ação |
| --- | --- | --- | --- | --- |
| [hipótese H1] | [suportada] | [nenhuma] | [link/saída] | [testar H2 com consulta X] |

## Execução

Comandos e consultas executados, resultados e **primeira falha**: [..]
Dados/integrações usados e limpeza necessária: [..]
**Checks invalidados por mudanças posteriores:** [..]
Pendências, riscos e impedimentos: [..]
Mudanças aplicadas em sistemas (para reverter): [horário UTC, quem, como reverter]

## Próxima ação concreta

[Uma ação, com dono e prazo.]

## Confirmação firme de quem assume

- [ ] Quem sai: "Passo o comando de [papel] a [nome] às [HH:MM UTC]; o estado acima é o que sei."
- [ ] Quem assume: "Assumo o papel de [papel] às [HH:MM UTC]; confirmei a revisão, o workspace e o estado do sistema."

Ao retomar, confirme a revisão e o workspace antes de assumir que este estado continua válido.
