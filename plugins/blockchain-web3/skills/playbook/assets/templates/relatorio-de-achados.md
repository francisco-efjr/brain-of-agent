# Relatório de achados

Preencha só com o que foi lido ou executado nesta sessão. Estados de evidência: `PoC-passed`, `PoC-failed`, `apenas-rastro-de-código`, `needs-execution`, `Verificação pendente`. Rótulos: Verificado · Inferido · Suposição · Não verificável · Não aplicável. Revisão pelo mesmo modelo não é auditoria externa.

## Sumário

- Escopo: [contratos, commit/tag, modo diff|full]
- Versões: compilador [ ] · OpenZeppelin [ ] · Foundry [ ] (ausente = Não verificável)
- Executor de PoC: [disponível | indisponível: tudo abaixo é não verificado]
- Contagem por severidade: Alta [n] · Média [n] · Baixa [n] · Verificação pendente [n]
- Conclusão: [uma frase; nunca "seguro"]

## Verificação pendente (Alta sem PoC executado)

[Candidato, cadeia de ataque completa, teste proposto e o que falta para executar.]

## Achados

### [arquivo:linha] — [título]

- Severidade: [Alta|Média|Baixa] · Categoria: [ ] · Confiança: [0–1] · ID: [W3-…] · Classe: [OWASP-SCnn; swc_id opcional]
- Pré-condições do atacante: [ ]
- Cenário (passo a passo, com cadeia de chamadas): [ ]
- Impacto (quem perde o quê): [ ]
- Correção mínima: [ ]
- Evidência: [estado] — comando: `[ ]` — saída: [trecho real] — ver `registro-de-poc.md` [ID]

## Remediação priorizada

| Ordem | Achado | Correção | Teste de regressão | Dono |
| --- | --- | --- | --- | --- |

## Apêndice A — Descartados e falsos positivos

| Candidato | Motivo | Teste ou guarda que refutou |
| --- | --- | --- |

## Apêndice B — Pendentes, não verificados e etapas não concluídas

| Item | O que faltou | Próximo passo |
| --- | --- | --- |

## Cobertura

- Lido: [arquivos e linhas]
- Executado: [comandos com versão]
- Não executado ou fora do escopo: [ferramentas indisponíveis, áreas fora da cobertura: Solana parcial, MEV, pontes, indexação, Hardhat]
- Citações conferidas por busca: [sim/não]

Ausência de achado não prova segurança. Este relatório não substitui auditoria humana externa nem fuzzing.

Ao concluir o relatório com todas as etapas executadas, acrescente a linha `<!-- W3_STATUS: COMPLETE -->`. Se alguma etapa ficou incompleta, não escreva o marcador e liste as etapas no Apêndice B.
