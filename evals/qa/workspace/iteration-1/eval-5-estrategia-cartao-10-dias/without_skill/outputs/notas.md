# Notas sobre a resposta (sem skill)

Respondi só com conhecimento próprio, sem Skill e sem ler skills/ ou evals/. Nenhum comando de rede.

## Incertezas e suposições

- **Stack e ferramentas desconhecidas.** Não sei a linguagem dos devs nem quais ferramentas de teste o time já usa; por isso a recomendação de automação ficou genérica ("o que o time já domina") com exemplos (Postman/Newman, pytest, Playwright API, REST-assured). Pode não ser a melhor escolha para o caso.
- **Natureza do cartão.** Assumi que pode haver processadora/BIN patrocinador externo e sandbox, mas não sei. Se o cartão for 100% simulado, parte dos testes de integração e certificação não se aplica.
- **Regulatório e certificação.** Mencionei PCI, LGPD, bandeira e regulador de forma genérica (pergunta 2) sem citar normas específicas (BACEN, limites de juros do rotativo etc.), porque não tenho certeza de quais se aplicam à fintech nem da versão vigente. Pode ser que a certificação seja o verdadeiro gargalo dos 10 dias.
- **Regras de negócio de juros, encargos, IOF, fechamento e vencimento.** Não afirmei fórmulas; mandei o usuário obtê-las com o negócio. Risco: o usuário pode esperar mais detalhe numérico.
- **Estimativas de tempo** (30-40% para reteste, distribuição dos dias, 1h de bug bash) são heurísticas minhas, não dados. O calendário assume que as features vão ficando prontas em staging ao longo dos dias; se tudo chegar só no dia 7, o plano precisa ser comprimido (e a resposta já sugere escrever casos/automação contra contrato ou mocks).
- **Papel dos devs.** Assumi que o time aceita escrever testes unitários e fazer bug bash; em uma fintech pequena isso pode exigir apoio do gestor/PO.
- **Critérios de go/no-go** são uma sugestão-base; o limite real de severidade depende da tolerância a risco da empresa.
- **Lançamento gradual** (feature flag, grupo restrito, limites baixos): sugeri sem saber se é viável tecnicamente ou aceitável pelo negócio.
- **Extensão.** A resposta ficou longa para um chat; optei por completude (módulo a módulo) em vez de enxugar. Se a avaliação preferir resposta mais enxuta ou com perguntas antes de recomendar, esta pode ser vista como excessiva.
- Não cobri em profundidade: antifraude/chargeback em detalhe, testes de carga reais, testes de conformidade PCI, notificações push/e-mail, ambiente de contingência.
