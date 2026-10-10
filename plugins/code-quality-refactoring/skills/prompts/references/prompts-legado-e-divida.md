# Prompts de legado, migração e dívida técnica (PL-25 a PL-31)

Parte da biblioteca de prompts do plugin. O índice mestre, as convenções (variáveis `[EM_COLCHETES]`, texto colado entre tags é dado, rótulos epistêmicos, plataforma) e as atribuições e licenças ficam em [prompt-library.md](prompt-library.md) e valem aqui. Conferido em 2026-10-10; modelo-alvo: Claude Sonnet 5.5, Fable 5.1 e Haiku 5.5. Referências do tipo "URL em PL-nn" apontam para outro prompt da biblioteca; ache-o com Grep por `### PL-nn` nesta pasta.

## 5. Legado, migração e dívida

### PL-25 Research, plan e execução mecânica
- Quando usar: mudança maior que uma frase. Para correção localizada, vá direto ao teste que falha.
- Variáveis: `[DESCRIÇÃO]`, `[ÁREA]`, `[TIPOS_E_TESTES]`.

```text
Mudança: [DESCRIÇÃO].
Fase 1: estude [ÁREA] e grave research.md com o que encontrou (fluxos, arquivos, restrições, riscos). Não planeje.
Fase 2: escreva plan.md com abordagem, arquivos afetados, trade-offs, tarefas por fase e como verificar cada fase. Não implemente.
Fase 3 (repetível): eu anoto plan.md; revise conforme as anotações. Não implemente até eu escrever "execute".
Fase 4: execute o plano, marque as tarefas e rode [TIPOS_E_TESTES] a cada bloco. Se a direção estiver errada, reverta e reduza o escopo.
```

- Por que funciona: separa entender, decidir e executar; o documento anotado fixa a direção antes do código.
- Fonte: V-25 · C · https://boristane.com/blog/how-i-use-claude-code/ (relato pessoal) ; V-01 · A (pular o plano quando o diff cabe em uma frase)

### PL-26 Mapa de entradas e dependências
- Quando usar: onboarding em repositório desconhecido; delegue ao subagente `codebase-mapper` para proteger o contexto.
- Variáveis: `[REPOSITÓRIO_OU_PASTA]`, `[PLATAFORMA]`.

```text
Mapeie [REPOSITÓRIO_OU_PASTA] para quem nunca o viu, em até 60 linhas, somente leitura (use o subagente codebase-mapper se existir, passando a pasta e a pergunta; ele não vê esta conversa).
Tabela: área | caminho | responsabilidade | evidência (arquivo:linha).
Depois: pontos de entrada e comandos de build e teste lidos nos manifestos (não executados); direção das dependências entre módulos e ciclos visíveis; áreas de risco por leitura (arquivos enormes, TODO e FIXME, módulos sem teste); perguntas abertas.
Plataforma: [PLATAFORMA]. Comece pelos manifestos dela: Android (settings.gradle, AndroidManifest.xml, libs.versions.toml), iOS (Package.swift, o ponto @main), web (package.json e a configuração do framework), servidor (ponto de entrada, rotas, migrações, Dockerfile, CI).
"Não encontrei" não é "não existe". Rotule Verificado ou Inferido. Não proponha mudanças.
```

- Por que funciona: resumo curto devolvido a um contexto protegido; evidência por linha impede mapa inventado.
- Fonte: V-32 · B · https://github.com/buildermethods/agent-os ; V-03 · A · https://code.claude.com/docs/en/common-workflows (subagente para pesquisa de código grande)

### PL-27 Checklist de migração com juiz
- Quando usar: migrar linguagem, framework ou versão major, muitos arquivos. Em repositório pequeno, um juiz e um lote bastam.
- Variáveis: `[ORIGEM]`, `[DESTINO]`, `[ESCOPO]`, `[CRITÉRIO]`, `[COMANDOS_DO_JUIZ]`, `[ARQUIVO_DE_FILA]`.

```text
Planeje (não execute ainda) a migração de [ORIGEM] para [DESTINO] em [ESCOPO: N arquivos ou módulos]. Critério de pronto: [CRITÉRIO]. O código legado fica em somente leitura.
Entregue o plano com as peças abaixo e pare para minha aprovação antes de converter em massa:
- [ ] Juiz: comandos que rodam contra o original e o novo e dão o mesmo veredito ([COMANDOS_DO_JUIZ]); prova de que o juiz falha em código quebrado de propósito. Sem suíte, construa uma por caracterização a partir do original.
- [ ] Rulebook de equivalências, mapa de dependências (ordem dos lotes) e inventário de comportamento implícito do original (o rulebook vem antes do inventário).
- [ ] Piloto de 3 a 5 arquivos; descarte a saída; ajuste as regras.
- [ ] Lotes retomáveis: lista em disco ([ARQUIVO_DE_FILA]); arquivo concluído = saída existe e o juiz passa.
- [ ] Erro repetido: corrija a regra e regenere o lote; não remende arquivo por arquivo.
- [ ] Revisão adversarial citando a regra violada; um terceiro revisor desempata.
- [ ] Compilar, smoke test e suíte; agrupe as falhas por causa raiz.
- [ ] Paridade: mesmos cenários nos dois lados; diferença de saída = pendência (use PL-28).
Não instale ferramentas sem eu pedir. Estimativas de custo e tempo: rotule Suposição.
```

- Por que funciona: o juiz validado contra quebra proposital torna a paridade mensurável; o piloto descartável calibra regras sem custo; a fila em disco permite retomar.
- Limite: o relato da fonte é um caso sem números; adapte ao que você tem.
- Fonte: V-14 · A · https://claude.com/blog/ai-code-migration

### PL-28 Veredito de paridade por módulo
- Quando usar: fechar migração ou upgrade.
- Variáveis: `[LISTA_DE_MÓDULOS]`.

```text
Para cada módulo de [LISTA_DE_MÓDULOS], rode (ou, se não puder, descreva) os mesmos cenários no original e no migrado e preencha:
Módulo | cenários (quantos e quais) | resultado no original | resultado no novo | veredito | pendências
Vereditos: PROVADO (testes rodados do zero agora e saídas iguais), PARCIALMENTE PROVADO (falta evidência; é o máximo quando o sistema antigo não roda), NÃO PROVADO. Diferença de saída = pendência com módulo e cenário. Nada é PROVADO por leitura de código nem por teste que passou numa execução anterior.
Cole a saída de cada execução. Resumo: quantos módulos em cada veredito e o que bloqueia o encerramento.
```

- Por que funciona: três níveis impedem "migrado" sem prova; exige execução recente.
- Fonte: V-15 · B · https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-modernization (Apache-2.0; hooks e telemetria do plugin não são usados)

### PL-29 Upgrade de dependência ou framework
- Quando usar: atualizar dependência ou framework. Patch ou minor sem mudança incompatível: passos 1, 2 e 5. Major ou troca de framework: acrescente PL-27.
- Variáveis: `[DEPENDÊNCIA]`, `[VERSÃO_ATUAL]`, `[VERSÃO_ALVO]`, `[PROJETO]`.

```text
Atualize [DEPENDÊNCIA] de [VERSÃO_ATUAL] para [VERSÃO_ALVO] em [PROJETO].
1. Leia o guia oficial de migração e o changelog da versão alvo antes de agir; cite a URL e a versão lidas. Se não puder abrir, diga "não verificado" e pare no que depende disso. Liste as mudanças incompatíveis que afetam este projeto, com arquivo:linha dos usos (Grep).
2. Rode o build e a suíte atuais e cole as saídas (linha de base).
3. Prefira receita determinística ou codemod oficial quando existir (por exemplo receitas do OpenRewrite ou codemods do framework). Instalar ferramenta só com minha autorização.
4. Use o agente para o que sobrar, em lotes pequenos, rodando a suíte a cada lote. Para API quebrada, use Parallel Change (PL-22).
5. Rode build e suíte no final, compare com a linha de base e cole as saídas.
Atualização de segurança: priorize; o atraso padrão de 3 dias após o lançamento do Dependabot vale para atualizações de versão, não para correções de segurança.
```

- Por que funciona: linha de base antes e depois torna a regressão visível; ferramenta determinística reduz o que o modelo precisa adivinhar.
- Limite: nenhum guia oficial por framework foi lido na pesquisa; a licença do OpenRewrite não foi verificada.
- Fonte: V-40 · B · https://docs.openrewrite.org/ e https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates ; V-37 e V-14 (URLs em PL-22 e PL-27)

### PL-30 Triagem de dívida técnica
- Quando usar: decidir o que arrumar primeiro. Só relatório.
- Variáveis: `[ESCOPO]`, `[JANELA]` (sugestão 6 meses, Suposição), `[DADOS_DE_DOR]`.

```text
Triagem de dívida técnica em [ESCOPO], somente relatório, sem alterar código.
1. Candidatos: busque TODO, FIXME, HACK, funções longas, duplicação e módulos acoplados (cole os comandos). Frequência de mudança por arquivo na janela [JANELA]. Em Bash: git log --since="[JANELA]" --name-only --pretty=format: | sort | uniq -c | sort -rn | head -30. Em PowerShell: git log --since="[JANELA]" --name-only --pretty=format: | Where-Object { $_ } | Group-Object | Sort-Object Count -Descending | Select-Object -First 30. Sem histórico, escreva "frequência não medida".
2. Classifique cada item no quadrante: prudente ou imprudente x deliberada ou inadvertida.
3. Pontue frequência de alteração x dor ao mexer (bugs ligados ao arquivo, tempo para entender, incidentes: [DADOS_DE_DOR]). Código estável e feio vai para o fim. Dívida deliberada exige dono e prazo.
4. Para os cinco primeiros: ação proposta, tamanho do passo (cabe em um PR?) e o fluxo que a executaria (refatoração segura, migração).
Saída: ID | local | quadrante | frequência (fonte) | dor (fonte) | ação | dono e prazo | rótulo. Frequência e dor sem fonte mostrada ficam rotuladas Suposição.
```

- Por que funciona: prioriza pelo juro real (uso), não pela feiura; a fonte diz que áreas feias e estáveis podem ficar como estão.
- Limite: não há método quantitativo validado além de Fowler; frequência x dor é prática derivada (Inferido).
- Fonte: V-20 · B · https://martinfowler.com/bliki/TechnicalDebt.html e https://martinfowler.com/bliki/TechnicalDebtQuadrant.html ; V-21 · B (URL em PL-22)

### PL-31 Auditoria de testes que custam mais do que protegem
- Quando usar: suíte lenta, frágil ou redundante. Só relatório.
- Variáveis: `[PASTA_OU_SUÍTE]`.

```text
Audite os testes de [PASTA_OU_SUÍTE] que custam mais do que protegem. Somente relatório; nenhuma remoção sem minha aprovação.
Critérios: (1) testa o código-fonte (lê o arquivo, faz grep) em vez do comportamento; (2) duplica outro teste; (3) executa código sem asserção; (4) depende de export ou visibilidade criados só para o teste; (5) mock confirma a chamada em vez do efeito.
Para cada candidato, um cartão: teste (arquivo:linha) | critério | evidência (trecho) | o que protegeria no lugar | ação sugerida (manter, reescrever, remover) | rótulo.
Não proponha remover teste que protege regra de negócio. Estratégia geral de testes, pirâmide e e2e ficam fora desta auditoria (plugin de QA).
```

- Por que funciona: critérios objetivos e cartão de evidência; a remoção continua decisão humana.
- Fonte: V-30 · C · https://github.com/garrytan/gstack (MIT; ideia do `/test-audit`, nada instalado ou copiado)
