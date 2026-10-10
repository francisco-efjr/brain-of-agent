# Regras de negócio: [sistema ou módulo]

Uma regra por **decisão de negócio**, não por ramo do código. Formato inspirado no plugin `code-modernization` da Anthropic (Apache-2.0), reescrito. Use quando o comportamento atual vive no código e precisa virar requisito. A extração por modelo não é determinística: toda regra passa por revalidação de um segundo agente em contexto novo. Não execute scripts de provas de terceiros; registre a evidência à mão.

### RULE-001: [nome da regra]

- **Fonte:** `[arquivo:linha-inicial-linha-final]`
- **Prioridade:** P0 (dinheiro, segurança, obrigação legal) / P1 / P2
- **Given** [estado ou condição]
- **When** [evento]
- **Then** [resultado observável]
- **Exceções e bordas:** [casos conhecidos]
- **Revalidação:** [agente e data] · **Veredito:** PROVEN (evidência encontrada) / PARTLY PROVEN / NOT PROVEN · **Evidência:** [trecho ou comando]
- **Dúvidas:** [pergunta, dono]

## Checklist de revisão de regra

- [ ] Tem fonte `arquivo:linha`.
- [ ] Representa uma decisão de negócio, não um ramo técnico.
- [ ] Condição e resultado são observáveis.
- [ ] Prioridade atribuída e justificada.
- [ ] Revalidada por segundo agente; incerteza marcada.
- [ ] Nenhum dado pessoal real nos exemplos.
