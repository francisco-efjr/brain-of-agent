# Testes, investigação, regressão e evidência

## Planejar pelo risco

Associar regra/risco a técnica e camada. Unidade cobre cálculo e transição; integração cobre serialização, persistência e adapters; contrato cobre consumidor/provedor; E2E cobre jornada entre camadas. Não duplicar todos os cenários em todas as camadas: escolher a menor que detecta a falha e manter jornadas críticas integradas.

Usar particionamento, limites, tabelas de decisão, transições e propriedades. Para desconto: testar abaixo/no/acima do limite, arredondamento, moeda, validade e composição. Propriedade possível: aplicar desconto válido nunca aumenta valor; ela complementa exemplos com valores esperados independentes.

## Investigação reproduzível

Registrar esperado/observado, build, ambiente, dados redigidos, timestamp e passos mínimos. Formular hipóteses que podem ser refutadas. Alterar uma causa por vez quando possível; correlacionar logs e estados. Antes de corrigir, obter reprodução ou explicar por que não foi possível.

Exemplo: pedido duplicado pode nascer em duplo clique, retry de gateway, reprocessamento de fila ou falta de constraint. Corrigir debounce apenas porque a UI dispara duas vezes deixa outros caminhos vulneráveis. Seguir identificador de operação entre camadas.

## Teste que protege a regra

Antes: mock retorna `true`; assert verifica que função foi chamada. Isso não detecta cobrança duplicada.

Depois: duas tentativas usam mesma chave; observar uma operação persistida e resultado consistente; tentativa com payload diferente produz conflito definido; teste de concorrência coordena execução e confere constraint. Mock continua útil para falha externa, mas não substitui persistência real quando atomicidade é a questão.

Evitar oráculo calculado pela mesma função sob teste. Se o resultado esperado é gerado usando a lógica errada da implementação, ambos podem concordar. Mutation testing pode investigar capacidade de detecção quando custo e stack justificam, sem impor percentuais universais.

## Browser e intermitência

Playwright recomenda isolamento de testes, locators ligados à experiência do usuário e assertions que aguardam condição; isso reduz dependência de timing arbitrário. [Fonte: Playwright Best Practices](https://playwright.dev/docs/best-practices).

Usar espera pela condição correta em vez de sleep fixo. Controlar relógio e aleatoriedade onde adequado; registrar seed. Repetir execução serve para observar frequência no ambiente, não provar determinismo. Retry que transforma primeira falha em verde precisa permanecer visível para investigação.

## Revalidação completa

1. Executar reprodução original contra correção.
2. Executar casos adjacentes da regra e fronteiras de acesso.
3. Rodar verificações afetadas: tipos, lint, build e testes relevantes.
4. Validar contrato/jornada real quando a mudança cruza camadas.
5. Conferir diff final e artefato testado; alteração posterior invalida evidência pertinente.

Não ampliar suite indefinidamente depois que verificações adequadas passaram sem nova mudança ou preocupação concreta.

## Checklist

- [ ] Riscos e invariantes ligados a casos e camadas.
- [ ] Teste falharia diante da regressão conhecida ou mutação pertinente.
- [ ] Dados, clock, dependências e isolamento controlados.
- [ ] Caminhos negativos, concorrência e falha parcial incluídos quando aplicáveis.
- [ ] Mocks identificados; limitações de integração declaradas.
- [ ] Falha intermitente não escondida por retries.
- [ ] Comandos, códigos de saída, versão e resultados registrados.
- [ ] Evidência distingue executado, revisado, inferido e bloqueado.
- [ ] Pendências possuem impacto e próximo passo, sem inventar aprovação QA.

Consultar também o brain QA para aprofundar técnicas; o desenvolvedor verifica sua implementação e QA mantém perspectiva crítica. Passar suite não autoriza declarar ausência de bugs.

Fonte consultada em 2026-10-09. Procedimentos e exemplos adicionais são recomendações próprias.
