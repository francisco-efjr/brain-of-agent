# Checklists de qualidade: pronto com evidência, escopo, revisão, debug, refatoração, migração, dívida e saúde

Uso: copie só o bloco da tarefa em curso. Cada item é verificável por leitura ou por comando. Itens V-nn apontam para `fontes.md`. Rótulos: Verificado, Inferido, Suposição, Não verificável, Não aplicável.

Sumário: 1 Pronto com evidência · 2 Escopo · 3 Revisão (agente e humano) · 4 Debug · 5 Refatoração · 6 Simplificação · 7 Migração e upgrade · 8 Dívida · 9 Saúde · 10 Revalidação em cinco passos · 11 Checklist de nove itens · 12 Matriz de aplicabilidade (QUALIDADE-COMPLETO)

## 1. Pronto com evidência (todas as tarefas)

- [ ] O check foi definido antes de mexer (teste, build, linter, typechecker, comparação de saída) e o comando está literal no relatório. (V-01)
- [ ] A saída do comando foi colada (final da saída e código de saída). "Testes passaram" sem saída não vale. (V-29, V-33)
- [ ] Sem check executável possível: o relatório diz "não verificado" e propõe qual check criaria. (V-01)
- [ ] A correção atua na causa raiz; nenhum teste foi desativado, nenhuma asserção afrouxada, nenhum aviso suprimido (`noqa`, `ts-ignore`, `eslint-disable`) para passar. (V-01, V-11, V-39)
- [ ] Cada afirmação tem rótulo epistêmico; leitura de código está marcada como Inferido. (V-01)
- [ ] Checks anteriores a uma mudança posterior foram refeitos ou declarados invalidados. (V-33)
- [ ] O status final é DONE, DONE_WITH_CONCERNS, BLOCKED ou NEEDS_CONTEXT, com razão.

## 2. Escopo

- [ ] O pedido (ou plano aprovado) está resumido em 2–3 linhas; o diff final não sai disso. (V-10)
- [ ] Bug pré-existente, otimização e comportamento não pedido aparecem como follow-up, não no diff. (V-10)
- [ ] Ambiguidade: foi implementada a leitura mais apoiada pelo texto e pelo código vizinho, com a suposição declarada. (V-10)
- [ ] Edição cirúrgica: nenhum arquivo reescrito por inteiro sem necessidade; sem abstração de uso único; sem tratamento de erro para cenário impossível; validação só nas fronteiras. (V-11)
- [ ] Testes novos só se pedidos ou se o repositório já mantém testes desse tipo, no tamanho dos vizinhos. (V-10)
- [ ] API pública, visibilidade e contratos não mudaram sem aprovação. (V-26)
- [ ] Ação destrutiva ou externa teve autorização explícita na conversa atual.

## 3. Revisão

### 3a. Versão de agente (padrão, sem estilo)

- [ ] Havia diff a revisar; caso contrário a resposta foi "nada a revisar". (V-06 passo 0)
- [ ] Regras do projeto (CLAUDE.md/AGENTS.md) que cobrem os arquivos foram localizadas; só regra citável vira checagem. (V-06, V-34)
- [ ] Linter e typechecker foram rodados; o que eles pegam ficou fora do relatório. (V-39)
- [ ] O diff foi resumido em até 5 linhas e comparado com a intenção declarada (commits, PR, plano): fora de escopo e requisito faltante marcados.
- [ ] Bugs no diff, segurança do código novo e conformidade com regras foram checados; entradas externas foram seguidas até o uso. (V-06, V-38)
- [ ] Se o diff adiciona valor de enum, status ou tipo, os consumidores fora do diff foram lidos.
- [ ] Cada achado passou por tentativa de refutação (`finding-validator`) e traz `arquivo:linha` existente e o texto da linha. (V-06)
- [ ] Filtro aplicado: fora pré-existente, estilo, o que linter pega, "pode ser problema se a entrada for X" sem evidência, código correto que parece bug, item silenciado de propósito. (V-06)
- [ ] Veredito: aprovar, aprovar com ressalvas ou bloquear (padrão do Google: aprovar o que melhora a saúde do código, mesmo imperfeito). (V-17)
- [ ] O relatório diz o que foi checado, o que não, e declara independência parcial (mesmo modelo). (V-35)
- [ ] Nada foi publicado em PR sem pedido explícito.

### 3b. Versão humana (lista completa, V-17)

| # | Dimensão | Pergunta |
| --- | --- | --- |
| 1 | Design | A mudança pertence a este código e este é o momento certo? |
| 2 | Funcionalidade | Faz o que o autor quer e serve ao usuário? |
| 3 | Complexidade | Entende-se rápido, sem generalização especulativa? |
| 4 | Testes | Existem, estão corretos e falhariam se o código quebrasse? |
| 5 | Nomes | Dizem a intenção sem ficar longos? |
| 6 | Comentários | Explicam o porquê, não o quê? |
| 7 | Consistência | Segue o guia de estilo e depois o código vizinho? |
| 8 | Documentação | README e referência foram atualizados? |

Complementos: ler cada linha alterada, olhar o contexto ao redor e registrar o que foi bem feito (só quando real). Preferência de estilo vai com o prefixo `nitpick`. (V-17, V-19)

## 4. Debug

- [ ] Sintoma registrado: esperado x observado, build/versão, ambiente, dados redigidos, passos mínimos. (V-33)
- [ ] Reprodução por um comando, ou justificativa de por que não foi possível, com evidência coletada. (V-03, V-33)
- [ ] Erro e stack trace lidos inteiros; mudanças recentes olhadas (`git log`/`git diff` do trecho). (V-04)
- [ ] Em sistema com camadas, entrada e saída registradas em cada fronteira; valor errado seguido até a origem. (V-04)
- [ ] Código parecido que funciona foi comparado.
- [ ] Hipóteses uma por vez, cada uma com o comando que a confirma ou refuta e a saída dele. (V-23)
- [ ] Teste de regressão visto falhando sem a correção e passando com ela. (V-04, V-26)
- [ ] Uma única correção, na causa; sem refatoração junto; correção que toca mais de 5 arquivos parou para perguntar sobre o raio de impacto. (gstack `/investigate`, ideia)
- [ ] Reprodução original rodada contra a correção; suíte afetada verde. (V-33)
- [ ] Intermitente: frequência medida (N execuções), espera por condição em vez de `sleep`, retry visível. (V-33)
- [ ] Escalada respeitada: 2 correções falhas = recomeçar com pedido melhor; 3 hipóteses refutadas = rever o desenho. (V-01, V-04)
- [ ] Relatório de debug com sintoma, causa raiz, correção, evidência, teste de regressão, prevenção, relacionado, status.

## 5. Refatoração

- [ ] Usos do trecho mapeados (Grep) e API pública afetada listada. (V-36)
- [ ] Testes existentes rodados e resultado registrado como linha de base. (V-03)
- [ ] Sem testes: testes de caracterização escritos (entradas relevantes, bordas, erros; saída real fixada; nome pelo comportamento). Saída que parece bug marcada "comportamento atual, possível defeito" e não corrigida. (V-36)
- [ ] Sem possibilidade de testar: o relatório declara que a preservação é só por leitura (Inferido) e o passo foi reduzido.
- [ ] Cada passo cita o nome da refatoração do catálogo; um passo por vez; testes após cada passo; passo que quebra é desfeito. (V-22)
- [ ] Mudança de API/dependência por Parallel Change, com data de contração. (V-37)
- [ ] Refatoração pura em commit próprio; diff acima do limiar configurável (Suposição: ~400 linhas ou 10 arquivos) teve proposta de divisão. (V-18)
- [ ] Mesma suíte, mesma saída antes e depois; nenhuma mudança de comportamento (se apareceu, parou e relatou).
- [ ] Testes que protegem regra de negócio ficaram; os que só prendem detalhe de implementação foram propostos para remoção, não removidos sem aprovação. (V-36)

## 6. Simplificação

- [ ] Escopo é só o diff atual ou os arquivos indicados. (V-12)
- [ ] Testes do trecho rodados antes; sem teste, caracterização ou aviso de garantia só por leitura. (V-12, V-36)
- [ ] Passos aplicados um por vez: retorno antecipado, remoção de duplicação, nomes de intenção, if/else no lugar de ternário aninhado, remoção de comentário que repete o código. (V-12)
- [ ] Não juntou responsabilidades sem relação, não removeu abstração com mais de um uso, não mudou API pública. (V-12)
- [ ] Mesmos testes depois, saída igual; resumo de até 5 linhas.

## 7. Migração e upgrade

- [ ] Tipo escolhido: uplift, transform ou reimagine (padrão: uplift ou strangler). (V-15, V-21)
- [ ] Build do original com prova (comando e saída); guia oficial de migração da versão lido (fonte por framework: Não verificado nesta pesquisa). (V-15)
- [ ] Juiz definido, rodado nos dois lados e provado contra código quebrado de propósito. (V-14)
- [ ] Rulebook, mapa de dependências e inventário de comportamento implícito escritos (nessa ordem). (V-14)
- [ ] Receita determinística (codemod, OpenRewrite, Dependabot) usada onde existir; ferramenta instalada só a pedido. (V-40)
- [ ] Plano aprovado pelo usuário antes de construir; legado em somente leitura. (V-15)
- [ ] Piloto de 3–5 arquivos descartado e regras ajustadas; lotes retomáveis em disco. (V-14)
- [ ] Erro repetido corrigido na regra e lote regenerado, sem remendo arquivo a arquivo. (V-14)
- [ ] Veredito de paridade por módulo: PROVADO, PARCIALMENTE PROVADO ou NÃO PROVADO. (V-15)
- [ ] Bump pequeno (patch/minor sem breaking change): changelog lido, suíte antes e depois, saídas coladas. (proporcionalidade)

## 8. Dívida técnica

- [ ] Candidatos coletados com comando mostrado (TODO/FIXME/HACK, funções longas, duplicação, acoplamento). (V-20)
- [ ] Frequência de mudança por arquivo medida em janela declarada (Suposição: 6 meses) ou "frequência não medida". (V-20)
- [ ] Cada item classificado em quadrante (prudente/imprudente x deliberada/inadvertida). (V-20)
- [ ] Ordem por frequência x dor; código estável e feio no fim; dívida deliberada com dono e prazo. (V-20)
- [ ] Auditoria de testes (se pedida): cartão de evidência por item; nenhuma remoção sem aprovação. (V-30)
- [ ] Cada item de topo tem ação, tamanho do passo e a skill que a executa.

## 9. Saúde do código

- [ ] Comandos vieram da seção `## Health Stack` do CLAUDE.md ou foram detectados e propostos, sem gravar sem pedido. (gstack `/health`, ideia)
- [ ] Cada ferramenta rodou separada, com saída completa e código de saída; relatório da ferramenta não foi substituído por análise própria.
- [ ] Nota composta calculada em código; categoria indisponível redistribui o peso; comando que rodou e falhou nunca vira "pulado".
- [ ] Cobertura declarada; nenhuma checagem rodou = "N/A", nunca 10/10.
- [ ] Tendência só entre rodadas com a mesma cobertura.
- [ ] Nada foi corrigido (portão somente leitura).

## 10. Revalidação em cinco passos (V-33, base própria)

1. Executar a reprodução original contra a correção.
2. Executar casos adjacentes da regra e fronteiras de acesso.
3. Rodar as verificações afetadas: tipos, lint, build e testes relevantes.
4. Validar contrato ou jornada real quando a mudança cruza camadas.
5. Conferir o diff final e o artefato testado; alteração posterior invalida a evidência pertinente.

Pare de ampliar a suíte quando as verificações adequadas passaram sem nova mudança ou preocupação concreta.

## 11. Checklist de nove itens (adaptado do brain-of-agent, `testes-e-debugging.md`, MIT)

- [ ] Riscos e invariantes ligados a casos e camadas.
- [ ] O teste falharia diante da regressão conhecida (ou de uma mutação pertinente).
- [ ] Dados, relógio, dependências e isolamento controlados.
- [ ] Caminhos negativos, concorrência e falha parcial incluídos quando aplicáveis.
- [ ] Mocks identificados e limitações de integração declaradas.
- [ ] Falha intermitente não escondida por retries.
- [ ] Comandos, códigos de saída, versão e resultados registrados.
- [ ] A evidência distingue executado, revisado, inferido e bloqueado.
- [ ] Pendências com impacto e próximo passo, sem inventar aprovação de QA.

## 12. Matriz de aplicabilidade (modo QUALIDADE-COMPLETO)

Preencha uma linha por área. Estado: aplicável, não aplicável (motivo) ou bloqueada (o que falta). Check: o comando ou a leitura que cobre a área.

| Área | Estado | Motivo ou bloqueio | Check que cobre | Evidência | Rótulo |
| --- | --- | --- | --- | --- | --- |
| Revisão | | | | | |
| Debugging | | | | | |
| Refatoração | | | | | |
| Simplificação | | | | | |
| Migração/upgrade | | | | | |
| Dívida técnica | | | | | |
| Análise estática/saúde | | | | | |
| Compreensão de código | | | | | |
| Segurança do diff | | | | | |
| Documentação | | | | | |

Exemplo de linha preenchida: `Refatoração | aplicável | — | pytest tests/test_frete.py (antes e depois) | 14 passed nos dois lados | Verificado`.
