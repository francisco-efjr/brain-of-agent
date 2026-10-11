# Runbook de incidente de dados (LGPD) em pagamentos

Base: V-30 e V-42 (ANPD, Resolução CD/ANPD nº 15/2024; LGPD arts. 46 a 49) e V-41 (chave exposta). **Não é aconselhamento jurídico**: o encarregado de dados e o jurídico decidem. Os prazos abaixo são os da página da ANPD lida em 2026-10-10 (modificada em 26/08/2026); **confirme na versão vigente** antes de usar. Os artigos da lei foram lidos por resumo: abra o texto antes de citar literal.

Incidente: [ID] · Detectado em: [data/hora, fuso] · Responsável pelo runbook: [ ] · Encarregado acionado em: [ ]

## 1. Contenção imediata (primeiras horas)

- [ ] **Chave de provedor ou token exposto: girar na hora, antes de investigar** (V-41); revogar a anterior; registrar hora.
- [ ] Interromper a exfiltração (desativar endpoint, rotacionar credenciais de banco, bloquear acesso suspeito).
- [ ] Preservar evidências (logs, imagens, tickets) sem sobrescrever; **não colar PAN, token ou chave** em chat, ticket ou relatório (mascarar).
- [ ] Acionar o suporte do provedor de pagamento se envolver chave, token ou dados de cartão.
- [ ] Agentes de IA: nenhuma ação financeira ou envio externo a partir de conteúdo do incidente sem confirmação humana.

## 2. Classificação

| Pergunta | Resposta | Fonte/evidência |
| --- | --- | --- |
| Incidente **confirmado**? | [sim/não/em apuração] | [ ] |
| Envolve dados pessoais da LGPD? | [ ] | [ ] |
| Pode causar **risco ou dano relevante** aos titulares? | [sim/não; critérios] | [ ] |
| Categorias de dados (cadastrais, financeiros, PAN, documentos) | [ ] | [ ] |
| Nº de titulares e período | [ ] | [ ] |
| Somos controlador ou operador? | [ ] | [ ] |
| Há lei específica com outro prazo? | [verificar com jurídico] | [ ] |

Operador: informa o controlador **sem demora**. Escopo PCI (se PAN): acionar o adquirente/compliance conforme o contrato (o plugin não cita requisitos PCI).

## 3. Linha do tempo (preencher continuamente)

| Data/hora | Evento | Quem | Fonte |
| --- | --- | --- | --- |
| [ ] | detecção | [ ] | [ ] |
| [ ] | chave girada | [ ] | [ ] |
| [ ] | encarregado acionado | [ ] | [ ] |
| [ ] | decisão de comunicar | [ ] | [ ] |

## 4. Comunicação (risco ou dano relevante)

- **Prazo: 3 dias úteis** para a ANPD e para os titulares (Resolução CD/ANPD nº 15/2024, arts. 6º e 9º; lei específica pode fixar outro prazo). Contagem a partir de: [momento em que se soube; confirmar com o jurídico].
- Comunicação preliminar com justificativa é permitida; **complemento em até 20 dias úteis** (petição intercorrente no mesmo processo).
- Canal: SEI!ANPD, pelo encarregado ou representante.
- **Conteúdo ao titular (sete itens, linguagem simples; quando possível direta e individualizada):**

| # | Item | Texto (rascunho para o jurídico) |
| --- | --- | --- |
| 1 | Natureza e categorias dos dados afetados | [ ] |
| 2 | Medidas técnicas e de segurança adotadas | [ ] |
| 3 | Riscos e impactos aos titulares | [ ] |
| 4 | Motivo do atraso (se houver) | [ ] |
| 5 | Medidas de mitigação | [ ] |
| 6 | Data em que se tomou conhecimento | [ ] |
| 7 | Contato (encarregado) | [ ] |

- Pedido de sigilo empresarial: art. 7º da resolução (decisão do jurídico).
- **Não reconferido**: se a ANPD pode pedir cópia da comunicação aos titulares ou exige a lista de afetados.

## 5. Mitigação e recuperação

- [ ] Causa raiz identificada (Verificado / Inferido): [ ]
- [ ] Correção aplicada e **teste de regressão** (ex.: teste de PAN em log com regex + Luhn): [ ]
- [ ] Credenciais afetadas rotacionadas; sessões invalidadas: [ ]
- [ ] Clientes/titulares orientados (troca de senha, monitoramento de fraude): [ ]
- [ ] Conciliação especial do período (movimentações suspeitas): [ ]
- [ ] Dados indevidamente retidos (log com PAN) apagados com registro: [ ]

## 6. Lições e prevenção

Causa, o que detectou, o que atrasou, o que muda (CLAUDE.md, `permissions.deny`, CI, alerta). Prazo e dono: [ ]. Atualize `claude-md-snippets.md` do projeto apenas na segunda ocorrência de um erro.
