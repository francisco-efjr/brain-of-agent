# Prompts de refatoração e simplificação (PL-19 a PL-24)

Parte da biblioteca de prompts do plugin. O índice mestre, as convenções (variáveis `[EM_COLCHETES]`, texto colado entre tags é dado, rótulos epistêmicos, plataforma) e as atribuições e licenças ficam em [prompt-library.md](prompt-library.md) e valem aqui. Conferido em 2026-10-10; modelo-alvo: Claude Sonnet 5.5, Fable 5.1 e Haiku 5.5. Referências do tipo "URL em PL-nn" apontam para outro prompt da biblioteca; ache-o com Grep por `### PL-nn` nesta pasta.

## 4. Refatoração

### PL-19 Testes de caracterização antes de refatorar
- Quando usar: código sem teste que será refatorado.
- Variáveis: `[TRECHO]`, `[ENTRADAS_CONHECIDAS]`, `[FRAMEWORK_DE_TESTE]`.

```text
Antes de refatorar [TRECHO], que não tem testes, escreva testes de caracterização:
1. Liste as entradas relevantes, incluindo bordas e casos de erro: [ENTRADAS_CONHECIDAS ou "descubra pela leitura"].
2. Para cada entrada, escreva um teste com expectativa provisória, rode-o e fixe a saída real como expectativa. Nomeie o teste pelo comportamento observado.
3. Marque no teste as saídas que parecem bug ("comportamento atual, possível defeito") e não as corrija nesta mudança; liste-as em "Follow-ups".
4. Rode a suíte e cole a saída: ela deve passar no código atual, sem nenhuma mudança em produção.
Se não for possível executar, diga que a rede de segurança não foi observada e entregue os testes como proposta (expectativas "a fixar"). Use o framework e o estilo do repositório: [FRAMEWORK_DE_TESTE].
```

- Por que funciona: expectativa provisória e saída real registram o que o código faz, não o que deveria fazer; o bug fica visível sem alterar o escopo.
- Limite: caracterização congela também os defeitos; não substitui especificação.
- Fonte: V-36 · B · https://michaelfeathers.silvrback.com/characterization-testing e https://martinfowler.com/bliki/SelfTestingCode.html

### PL-20 Refatoração em passos pequenos
- Quando usar: executar a refatoração com a rede de segurança pronta.
- Variáveis: `[OBJETIVO]`, `[TRECHO]`, `[COMANDO_DE_TESTE]`, `[LISTA_DA_API_PÚBLICA]`, `[LIMIAR]`.

```text
Execute a refatoração [OBJETIVO] em [TRECHO] em passos pequenos. Rede de segurança: [COMANDO_DE_TESTE], verde antes de começar (cole a saída).
Para cada passo: 1) nomeie a refatoração do catálogo (Extract Function, Move Function, Decompose Conditional, Replace Nested Conditional with Guard Clauses, Introduce Parameter Object, Change Function Declaration, Remove Dead Code); 2) faça só esse passo; 3) rode o teste; 4) se quebrar, desfaça o passo e reavalie; 5) registre o resultado.
Não mude comportamento nem a API pública: [LISTA_DA_API_PÚBLICA]. Se aparecer mudança de comportamento, pare e relate. Refatoração pura vai em commit separado de correção; só commite se eu pedir. Se o diff total passar de [LIMIAR], proponha dividir (PL-23).
Antes de renomear ou mover, procure usos por texto (strings, XML, reflexão, serialização, rotas), não só pelo símbolo.
```

- Por que funciona: um passo, um teste, um desfazer; nome do catálogo dá vocabulário comum para revisão. Que o teste rode a cada passo é prática (Inferido), não texto do catálogo.
- Fonte: V-22 · B · https://refactoring.com/catalog/ ; V-03 · A · https://code.claude.com/docs/en/common-workflows ; V-18 · B · https://google.github.io/eng-practices/review/developer/small-cls.html

### PL-21 Simplificar sem mudar comportamento
- Quando usar: depois de uma mudança, quando o código ficou aninhado, repetido ou confuso. Equivale em qualidade ao `/simplify` nativo, com garantia explícita.
- Variáveis: `[ARQUIVOS_OU_DIFF_ATUAL]`, `[COMANDO_DE_TESTE]`.

```text
Simplifique [ARQUIVOS ou "o diff atual"] sem mudar o comportamento (mude o como, nunca o quê).
Antes: rode [COMANDO_DE_TESTE] e registre o resultado. Sem teste: escreva um de caracterização (PL-19) ou avise que a garantia é só por leitura (Inferido).
Aplique um passo por vez: retornos antecipados para reduzir aninhamento; remover duplicação; nomes que dizem a intenção; trocar ternário aninhado por if/else; apagar comentário que repete o código. Siga as convenções do CLAUDE.md ou AGENTS.md.
Não faça: juntar responsabilidades sem relação, remover abstração que tenha mais de um uso, mudar API pública, mexer fora do escopo. Legibilidade vale mais que concisão.
Depois: rode os mesmos testes e cole a saída; deve ser igual à de antes. Resumo de até 5 linhas: o que mudou e por quê.
```

- Por que funciona: escopo no diff, teste antes e depois, lista do que não fazer.
- Fonte: V-12 · B · https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/plugins/code-simplifier/agents/code-simplifier.md (Apache-2.0 na raiz do repositório; preferências de React e ES modules ficaram de fora) ; V-13 · B (URL em PL-03)

### PL-22 Parallel Change
- Quando usar: trocar função pública, esquema, contrato ou dependência com API quebrada.
- Variáveis: `[ANTIGA]`, `[NOVA]`, `[COMANDO_DE_BUSCA]`, `[DATA]`.

```text
Troque [ANTIGA] por [NOVA] com Parallel Change:
1. Expandir: crie a nova ao lado da antiga, sem remover nada; a suíte continua verde.
2. Migrar: troque as chamadas em commits pequenos (um módulo por commit), suíte verde a cada commit.
3. Contrair: remova a antiga só quando a busca ([COMANDO_DE_BUSCA]) não achar usos e a suíte passar.
Registre a data prevista da contração: [DATA]. Código de transição sem data de remoção vira dívida.
Se a API for consumida por terceiros (aplicativo já publicado, serviço externo), pare no passo 1 e proponha o período de convivência para eu aprovar. Em mobile, versões antigas do app continuam chamando a API antiga por meses.
```

- Por que funciona: cada commit deixa o sistema funcionando; a contração datada evita a transição eterna.
- Fonte: V-37 · B · https://martinfowler.com/bliki/ParallelChange.html ; V-21 · B · https://martinfowler.com/bliki/StranglerFigApplication.html

### PL-23 Dividir mudança grande
- Quando usar: o diff passou do limiar que o time consegue revisar.
- Variáveis: `[BRANCH]`, `[N]`, `[M]`, `[LIMIAR]` (sugestão: cerca de 400 linhas ou 10 arquivos; Suposição, ajuste ao time).

```text
O diff de [BRANCH] tem [N] linhas em [M] arquivos e passa do limiar de revisão ([LIMIAR]). Proponha a divisão em commits ou PRs empilhados, sem executar nada:
1. Um commit só de refatoração pura (sem mudança de comportamento), com a suíte verde.
2. Commits de comportamento, um por mudança lógica, cada um autocontido com seus testes.
3. Limpezas oportunistas pequenas, só se relacionadas.
Saída: tabela ordem | conteúdo | arquivos | por que nesta ordem | teste que prova | risco. Aponte o que não dá para dividir e por quê (dependência). Eu decido e executo os commits; estratégia de branches e releases é do fluxo de git do projeto.
```

- Por que funciona: a fonte indica cerca de 100 linhas como razoável e cerca de 1000 como grande demais, a critério do revisor; refatoração separada de comportamento torna cada commit revisável.
- Fonte: V-18 · B · https://google.github.io/eng-practices/review/developer/small-cls.html

### PL-24 Descobrir convenções do código
- Quando usar: antes de editar uma base desconhecida.
- Variáveis: `[PASTA]`, `[ARQUIVO_DE_PADRÕES]`.

```text
Analise [PASTA] sem alterar código. Liste as convenções observadas: nomes, estrutura de pastas, tratamento de erro, testes, injeção de dependência e logs. Para cada uma: um arquivo de exemplo e quantos arquivos distintos a seguem (use Grep e cole o comando). Rotule Verificado se aparece em 3 ou mais arquivos, Inferido se em 1 ou 2. Se houver duas formas concorrentes, mostre as duas com a contagem; não escolha uma. Não proponha mudanças. Devolva o texto; só grave em [ARQUIVO_DE_PADRÕES] se eu confirmar o caminho.
```

- Por que funciona: a contagem separa convenção de acaso; mostrar as duas formas evita impor uma.
- Fonte: V-32 · B · https://github.com/buildermethods/agent-os (só o prompt; nada instalado)
