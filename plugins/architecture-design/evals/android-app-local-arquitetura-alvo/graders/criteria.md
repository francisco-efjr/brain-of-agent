---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Recomenda uma arquitetura proporcional ao app (monólito modular em módulo único, sem backend, sem multimódulo e sem framework de injeção de dependência como Hilt ou Dagger, ou os apresenta apenas como alternativas descartadas com gatilho de reavaliação), e reutiliza a interface `ContractDraftStore` existente em vez de criar uma nova.
2. Entrega ANTES e DEPOIS lado a lado (tabela ou dois diagramas), e uma tabela por camada com as colunas hoje, proposto, por quê e achado que resolve, em que cada linha cita um dos fatos confirmados.
3. Entrega o plano de migração em fatias, cada uma com pronto quando, testes, risco e rollback; nenhuma fatia depende de uma decisão humana pendente sem dizer isso.
4. Propõe fitness functions e usa o padrão catraca para as violações já existentes (lista de violações conhecidas que só encolhe, em vez de exigir zero de imediato) e sugere buscar também o nome qualificado, não só linhas de `import`, por causa do ciclo `model` e `util`.
5. Cobre riscos próprios de Android além do checklist de servidor: cast para `Application` e fábrica de `ViewModel`, estado de tela que se perde ao girar ou com a morte do processo, teste JVM contra instrumentado no CI, e apagar o PDF logo após compartilhar (rotulado como risco a verificar, com a mitigação de apagar depois ou por limpeza posterior), sem afirmar que o app falha.
6. Não reproduz valores de dado pessoal (nenhum CPF, nenhum nome de pessoa); trata a exposição de `locadores.json` versionado como ação imediata não arquitetural e cita a chave e a linha.
7. Rotula Verificado, Inferido, Suposição ou Proposta; marca comandos e verificadores como não executados; lista decisões que dependem do humano com dono.
FAIL if qualquer um ocorrer: propõe servidor ou backend sem gatilho; propõe Hilt, multimódulo ou reescrita para outra tecnologia como recomendação; cria uma nova interface no lugar de `ContractDraftStore`; exige zero violações já na primeira fatia; reproduz valor de CPF ou nome de pessoa; afirma ter compilado, rodado testes ou lido arquivos do repositório; deixa de dar uma recomendação única.
