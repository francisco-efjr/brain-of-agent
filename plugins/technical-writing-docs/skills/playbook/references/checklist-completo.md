# Checklist completo de documentação

Validado em 2026-10-10. Cada linha: item, como verificar, severidade (**C** crítico: bloqueia a entrega; **I** importante: corrigir ou justificar; **S** sugestão). "Verificar" significa evidência observável (Grep, Glob, comando com saída, leitura citada); sem evidência, o item fica Não verificado. Fontes V-nn em [fontes](fontes.md).

## Sumário

A. Antes de escrever · B. README · C. Tutorial · D. How-to · E. Referência · F. Explicação · G. ADR · H. Runbook · I. Changelog · J. API · K. Docstring · L. Diagrama · M. CLAUDE.md e AGENTS.md · N. Skill e agente · O. Tom · P. Instruções aninhadas · Q. Documento pronto (três portões) · R. CI de docs

## A. Antes de escrever

| Item | Como verificar | Sev. |
| --- | --- | --- |
| Leitor, nível e objetivo declarados | Três linhas no topo do plano ou do documento | C |
| Quadrante ou tipo escolhido (um só) | Classificador de duas perguntas ([tipos-de-documento](tipos-de-documento.md)) | C |
| Fonte dos fatos lida (código inteiro, testes, contrato, diff) | Lista de arquivos lidos no plano | C |
| Convenções do projeto descobertas (guia de estilo, `.vale.ini`, framework de docs, ADRs numeradas) | Glob/Grep citados | I |
| Esboço de uma linha por seção aprovado (documento longo ou novo) | Aprovação do usuário registrada | I |
| Dúvida material perguntada (uma por vez); o resto como Suposição registrada | Seção "Suposições" | I |

## B. README

| Item | Como verificar | Sev. |
| --- | --- | --- |
| Decisão em 3 a 5 segundos: frase de valor na abertura | Leitura do primeiro bloco | I |
| Exemplo funcional nas primeiras ~5 linhas | Leitura; exemplo marcado executado ou "não executado" | I |
| Quick Start copiável (sem `$`) | Leitura; comando existe no manifesto (Grep) | C |
| Licença igual ao arquivo `LICENSE` | Leitura de `LICENSE` | C |
| Imagens e links relativos existem | Glob; lychee `--offline` se configurado | I |
| Sem palavras de enchimento | Grep da lista em [estilo-e-tom](estilo-e-tom.md) | S |
| README liga `docs/` e CONTRIBUTING | Leitura | I |

## C. Tutorial

| Item | Como verificar | Sev. |
| --- | --- | --- |
| Título diz o que será construído | Leitura | S |
| Destino mostrado no início | Leitura | I |
| Resultado visível a cada passo; primeiro até o passo 3 | Contagem de passos até o primeiro resultado | C |
| Comandos exatos, sem abstração ("execute o comando apropriado") | Leitura | C |
| Erros comuns avisados no passo | Leitura; vêm de testes ou tratamento de erro | I |
| Sem explicação no corpo (links) e sem trilhas alternativas | Leitura | I |
| Seção final "O que você construiu" com links | Leitura | S |

## D. How-to

| Item | Como verificar | Sev. |
| --- | --- | --- |
| Título descreve o objetivo/problema resolvido | Leitura | I |
| Pré-requisitos específicos (versões, ferramentas) | Leitura | I |
| Só ações; sem ensino | Nenhum parágrafo conceitual | I |
| Verificação ("como saber que funcionou") | Seção presente | C |
| Solução de problemas quando a tarefa pode falhar | Seção presente | I |
| Explicação e referência por link | Links resolvem | S |

## E. Referência

| Item | Como verificar | Sev. |
| --- | --- | --- |
| Cobre 100% da superfície pública | Lista da superfície (Grep nos exports) comparada com o documento | C |
| Tipos, padrões e restrições de cada item | Leitura; confronto com o código | C |
| Neutra: sem "por quê" e sem instruções | Leitura | I |
| Espelha a estrutura do produto | Ordem dos itens igual à do código/CLI | S |
| Exemplos reais, copiáveis | Executados ou "não executado" | I |

## F. Explicação

| Item | Como verificar | Sev. |
| --- | --- | --- |
| Começa pelo problema, não pela solução | Leitura | I |
| Trade-offs e alternativas nomeados | Seção presente | I |
| Escopo delimitado; sem instruções | Leitura | I |
| Link para a referência | Link resolve | S |

## G. ADR

| Item | Como verificar | Sev. |
| --- | --- | --- |
| Número novo, nunca reaproveitado | Glob da pasta de ADRs | C |
| Contexto descreve forças, não a solução | Leitura (pergunta 1 de Nygard) | I |
| Mínimo duas alternativas reais | Seção de opções | I |
| Decisão em voz ativa com o motivo | Leitura | I |
| Consequência negativa registrada | Seção não vazia | C |
| Status correto; substituição aponta a ADR nova | Leitura | I |
| Nenhuma ADR aceita editada além da linha de status | Diff | C |
| Sem segredo, token ou host interno | Grep | C |

## H. Runbook

| Item | Como verificar | Sev. |
| --- | --- | --- |
| Cabeçalho: quando usar, gravidade, acessos, responsável, data | Leitura | I |
| Todo passo tem comando, resultado esperado e ramo de falha | Leitura passo a passo | C |
| `[DESTRUTIVO]`/`[IRREVERSÍVEL]` nos passos certos, com confirmação humana | Leitura | C |
| Saídas aparecem como "esperada (não executado)" | Leitura | C |
| Verificação com critério mensurável | Seção presente | I |
| Rollback e ponto sem retorno | Seção presente | C |
| Escalonamento: quando, para quem, com que dados | Seção presente | I |
| Sem segredo nem host interno sensível | Grep | C |

## I. Changelog

| Item | Como verificar | Sev. |
| --- | --- | --- |
| Entradas só adicionadas; nenhuma antiga regenerada | Diff | C |
| Tipos corretos (Added, Changed, Deprecated, Removed, Fixed, Security) | Leitura | I |
| Quebra de compatibilidade marcada | Comparação com commits `!`/`BREAKING CHANGE:` | C |
| Datas ISO 8601 | Grep | S |
| Rastreio entrada → commit/PR a 100% | Tabela | I |
| `VERSION`/`package.json` não alterados; versão só recomendada | Diff | C |

## J. API

| Item | Como verificar | Sev. |
| --- | --- | --- |
| Uma única fonte da verdade identificada | Plano | C |
| Todo campo/operação tem descrição (checklist de campo) | Grep por campos sem `description` | C |
| `openapi: "3.2.1"` com aspas; `info.version` = versão do documento | Leitura | I |
| Deprecação com alternativa | Leitura | I |
| Exemplos reais ou marcados "ilustrativo" | Leitura | I |
| Validação de contrato proposta para CI | Texto | S |

## K. Docstring

| Item | Como verificar | Sev. |
| --- | --- | --- |
| Resumo de uma linha ≤ 80 caracteres com ponto (Python/Google) | Contagem | S |
| Não repete a assinatura | Leitura | I |
| Exemplo público é teste (doctest/`cargo test --doc`) | Comando proposto; executado com autorização ou "não executado" | C |
| `Raises` só as da interface | Leitura | S |
| Dialeto confere com a ferramenta que lê (JSDoc/TSDoc, JDK) | Config do projeto | I |
| Atualizada no mesmo commit que o código | Diff | I |

## L. Diagrama

| Item | Como verificar | Sev. |
| --- | --- | --- |
| Um nível por diagrama; menos de 15 nós | Contagem | I |
| Tipo adequado à necessidade | Tabela em [docs-as-code](docs-as-code-e-diagramas.md) | S |
| Render confirmado no destino ou "render não verificado" | Declaração explícita | C |
| C4 do Mermaid com aviso de experimental e versão | Leitura | I |
| Texto explica o que mostra, para quem e a data | Leitura | I |
| Fatos Inferidos listados | Seção | I |

## M. CLAUDE.md e AGENTS.md

| Item | Como verificar | Sev. |
| --- | --- | --- |
| Menos de 200 linhas | `wc -l` ou contagem | I |
| Só o que não se descobre lendo o repo | Teste de cinco perguntas | I |
| Comandos copiáveis, incluindo teste único; existem no manifesto | Grep | C |
| Cada proibição com alternativa | Leitura | I |
| Cada regra com motivo e data | Comentários presentes | S |
| Sem segredos; sem CAPS generalizado | Grep | C |
| Sem contradição entre arquivos; AGENTS.md × CLAUDE.md coerente | Leitura | I |
| `@imports` ≤ 4 saltos; `paths:` casam arquivos | Glob | I |

## N. Skill e agente

| Item | Como verificar | Sev. |
| --- | --- | --- |
| `name` casa `^[a-z0-9]+(-[a-z0-9]+)*$`, ≤ 64, igual ao diretório, sem "claude"/"anthropic" | Regex | C |
| `description` 1 a 1.024 caracteres, 3ª pessoa, o que faz + quando usar, 3 a 5 frases de disparo | Contagem | C |
| Corpo < 500 linhas; referências a um nível; sumário em referência > 100 linhas | `wc -l` | I |
| `allowed-tools`/`tools` coerentes com os passos | Confronto | C |
| Revisor sem Write/Edit; sem `Bash(npx:*)`/`Bash(git:*)` irrestritos | Frontmatter | C |
| `## Gotchas` presente | Leitura | I |
| Skill com efeito persistente usa `disable-model-invocation: true` | Frontmatter | I |

## O. Tom

| Item | Como verificar | Sev. |
| --- | --- | --- |
| Segunda pessoa; imperativo em procedimentos | Leitura | S |
| Sem "simplesmente/fácil/rápido" em passos | Grep | S |
| Sem exclamações, gíria, enchimento | Grep | S |
| Títulos em caixa de frase; um h1; sem pular nível | Leitura | S |
| Voz ativa por padrão | Leitura | S |
| Lido em voz alta | Autoverificação declarada | S |

## P. Instruções aninhadas (após editar, V-26)

| Item | Como verificar | Sev. |
| --- | --- | --- |
| Linha de "arquivo não carregado" ausente na transcrição | Observação pelo usuário | I |
| Tarefa no subdiretório com a ferramenta Read carrega a regra | Teste pelo usuário | I |
| Versão do Claude Code ≥ 2.1.293 registrada | `claude --version` | S |

## Q. Documento pronto: três portões (GS-gen Step 8, adaptados)

**Acurácia:** exemplos rodam (ou "não executado"); descrições batem com as assinaturas; comandos produzem a saída descrita; nenhuma referência a entidade renomeada. **Completude:** referência cobre a superfície; how-tos cobrem as três tarefas principais; explicação nomeia trade-offs; tutorial chega a um resultado até o passo 3. **Voz:** escrito para leitor inteligente que não viu o código; jargão glosado no primeiro uso; voz ativa, substantivos concretos, frases curtas.

## R. CI de docs

| Item | Como verificar | Sev. |
| --- | --- | --- |
| `pull_request` (não `pull_request_target`) em PR de fork | Leitura do YAML | C |
| `permissions` mínimas por job | Leitura | C |
| Actions de terceiros fixadas por SHA | Leitura | I |
| Link externo fora do job de PR | Leitura | I |
| Deploy só no branch padrão | Leitura | C |
| O que rodou e o que não rodou, sem afirmar que passou | Relato | C |
