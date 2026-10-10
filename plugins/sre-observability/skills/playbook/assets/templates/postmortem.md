# Postmortem — [título] · [data do incidente] · Severidade [..] · Autores (papéis) [..]

Template T-06. Seções destiladas do capítulo "Postmortem Culture" do SRE Book (V-07); a seção de linha do tempo é sugestão do plugin (o capítulo não a lista). Blameless: foco em causas contribuintes de sistema e processo; presumir boa-fé; **ações têm dono**. Compartilhe sem informação que identifique usuário final. **Rascunho de IA só é publicado após revisão humana.** Participantes por papel (IC, OL), nunca por nome.

**Status:** [rascunho / em revisão / aprovado] · **Gatilho que justifica o postmortem:** [indisponibilidade/degradação acima de [limiar]; perda de dados; intervenção do plantão; tempo de resolução acima de [limiar]; falha de monitoramento; pedido de stakeholder] · **Incidente:** [ID/link do registro T-04]

## Resumo (3 linhas)

[O que aconteceu, quanto durou, impacto, como foi resolvido.]

## Impacto

| Dimensão | Valor | Fonte do número | Rótulo |
| --- | --- | --- | --- |
| Usuários afetados | [..] | [consulta/painel] | [Verificado / Suposição (estimativa)] |
| Duração (UTC) | [início–fim] | [alerta, painel] | [..] |
| Dados | [perdidos/atrasados/nenhum] | [..] | [..] |
| Custo / SLO | [budget consumido: x% da janela] | [conta] | [..] |

## Linha do tempo (UTC; cada evento com fonte)

| Horário UTC | Evento | Fonte/link | Rótulo (Verificado / Inferido se de memória) |
| --- | --- | --- | --- |
| [..] | [deploy da v3.2 iniciado] | [link do pipeline] | Verificado |
| [..] | [primeiro alerta] | [link] | Verificado |

Conflitos entre fontes (horários divergentes): [lista].

## O que foi feito para mitigar

[Ações em ordem, com horário, executor (papel) e decisão que as autorizou.]

## Causas contribuintes (sistema e processo, sem nomes)

| Contribuinte | Evidência | Candidata/confirmada | Quem confirmou (humano) |
| --- | --- | --- | --- |
| [ex.: o pipeline permite promover sem o teste de migração] | [link] | [candidata proposta pela IA / confirmada] | [papel, data] |

Causa raiz (hipótese a confirmar pelos humanos): [..]. Evite "5 porquês" que terminem em pessoa.

## O que funcionou e o que não funcionou

| Detecção | Resposta | Comunicação | Ferramentas e runbooks |
| --- | --- | --- | --- |
| [funcionou: ..; falhou: ..] | [..] | [..] | [..] |

## Ações de acompanhamento (humanos aprovam)

| ID | Ação | Dono | Prazo | Prioridade | Ticket | Critério de conclusão | Tipo (prevenir / detectar / mitigar) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | [..] | [papel/nome] | [data] | [P0–P3] | [link] | [verificável] | [..] |

## Não sabemos ainda

[Lista de perguntas abertas, com quem investiga e até quando.]

## Lições

[2–5 linhas: o que mudaria o comportamento do sistema ou do processo.]

## Checklist de revisão (5 perguntas do capítulo + privacidade)

- [ ] Dados do incidente coletados
- [ ] Impacto completo
- [ ] Causa raiz suficientemente profunda
- [ ] Ações priorizadas, com dono e prazo
- [ ] Resultados compartilhados com os stakeholders
- [ ] Sem dado pessoal de usuário final nem segredo
- [ ] Lint blameless: zero nomes próprios e zero verbos de culpa ("errou", "esqueceu", "falha de [pessoa]")
- [ ] Todo horário tem fonte; estimativas marcadas como Suposição
