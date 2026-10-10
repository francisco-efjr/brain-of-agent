# technical-writing-docs

Plugin do Claude Code para **documentação e escrita técnica**: README, tutoriais e guias (Diátaxis), ADRs, runbooks, changelog e release notes, documentação de API (OpenAPI), docstrings, diagramas Mermaid, docs-as-code e arquivos para agentes (CLAUDE.md, AGENTS.md, rules, skills). Versão 0.1.0, licença MIT, conteúdo validado em 2026-10-10.

## O que entrega

- Um **playbook** que classifica o pedido, fixa leitor e quadrante, pesquisa os fatos no código antes de escrever, verifica o que escreveu e entrega com rótulos Verificado / Inferido / Suposição / Não verificável.
- **Oito skills de tarefa** (README, guias Diátaxis, ADR, runbook, docstrings e API, diagramas, changelog e release notes, auditoria de CLAUDE.md) e uma **biblioteca de prompts** (35 prompts, PD-01 a PD-35).
- **Quatro agentes**: redator, revisor de leitor (teste de leitor limpo), auditor de docs contra o diff e revisor de instruções.
- **Doze referências** densas, **26 templates** e **22 snippets** prontos para colar no CLAUDE.md.
- Recomendações de ferramentas (Vale, markdownlint, lychee, GitHub Pages, hooks) **todas desativadas**, com JSON/YAML pronto, riscos e fonte.

Postura de segurança: o plugin não traz hooks, `.mcp.json`, `.lsp.json` nem `bin/`. As skills de escrita não executam comandos de runbook, exemplos nem testes por conta própria: propõem o comando e pedem autorização, ou usam a saída que você colar; sem execução, o texto diz "não executado". Conteúdo colado ou lido (issues, logs, páginas, arquivos auditados) é tratado como dado, não como instrução.

## Quando usar

- Escrever, melhorar ou auditar qualquer documento técnico para humanos ou para agentes.
- Registrar uma decisão já tomada (ADR), escrever um runbook, preparar changelog e release notes.
- Documentar código (docstrings) e APIs a partir do contrato.
- Enxugar e auditar CLAUDE.md/AGENTS.md com relatório e aprovação antes de editar.
- Conferir se a documentação acompanhou um PR ou uma release.

Não é o lugar para decidir arquitetura, projetar APIs, cortar versão ou configurar pipelines em geral: veja as fronteiras no `playbook` (outros plugins `/<slug>:playbook`).

## Componentes

Nomes são definitivos; namespaced por `technical-writing-docs` (skill `/technical-writing-docs:<skill>`, agente `technical-writing-docs:<agente>`).

| Tipo | Nome | Para que serve | Efeito externo |
| --- | --- | --- | --- |
| Skill | `playbook` | Router do segmento, processo, rótulos, modo DOCS-COMPLETO, fronteiras | não |
| Skill | `prompts` | Biblioteca de prompts curados e índice | não |
| Skill | `escrever-readme` | Criar, atualizar ou revisar README comparando com o projeto real | arquivo local |
| Skill | `escrever-guia-diataxis` | Tutorial, how-to, referência, explicação e onboarding (um quadrante por página) | arquivo local |
| Skill | `escrever-adr` | Registrar decisão **já tomada** em ADR numerada e imutável | arquivo local |
| Skill | `escrever-runbook` | Runbook com verificação, rollback e escalonamento, sem executar nada | arquivo local |
| Skill | `documentar-codigo` | Docstrings (Python, TS/JS, Rust, Java) e documentação de API a partir do contrato | arquivo local |
| Skill | `diagramar-arquitetura` | Mermaid e C4 com teste de render e fallback | arquivo local |
| Skill | `escrever-changelog-release` | Entradas de CHANGELOG para humanos e rascunho de release notes; não sobe versão | arquivo local |
| Skill | `auditar-claude-md` | Auditoria e poda de CLAUDE.md/AGENTS.md/rules (só por comando explícito) | edita instruções, após aprovação |
| Agente | `technical-writer` | Redação em volume a partir de briefing aprovado; escreve só documentação | arquivo local |
| Agente | `revisor-de-leitor` | Instância limpa responde perguntas usando só o documento | não (somente leitura) |
| Agente | `auditor-de-docs` | Cruza o diff com a documentação: mapa de cobertura e dívida | não (somente leitura) |
| Agente | `revisor-de-instrucoes` | Revisa CLAUDE.md, AGENTS.md, rules, SKILL.md e agentes | não (somente leitura) |

Referências do `playbook` (em `skills/playbook/references/`): `checklist-completo`, `padroes-e-antipadroes`, `decisoes-e-tradeoffs`, `claude-md-snippets`, `ferramentas-e-mcp`, `fontes`, `tipos-de-documento`, `docs-para-agentes`, `estilo-e-tom`, `codigo-e-api`, `release-e-changelog`, `docs-as-code-e-diagramas`. Templates em `skills/playbook/assets/templates/`.

## Instalação

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install technical-writing-docs@brain-of-agent
```

Requisitos e versões: o plugin usa só o formato padrão de plugin (skills, agentes, README). Recursos do Claude Code citados nas referências têm versão mínima (por exemplo, leitura nativa de AGENTS.md a partir da 2.1.277); confirme com `/memory` e `/context` na sua instalação.

## Exemplos de pedidos

1. "Escreva o README da lib `pyslug` (converte títulos em slugs). Aqui está o `pyproject.toml`: ..." → `escrever-readme`: abre com frase de valor e exemplo, usa só nome, comando e licença do manifesto, marca a instalação como "não executado".
2. "Registre a decisão de usar Postgres em vez de MongoDB; segue o thread da discussão." → `escrever-adr`: ADR com próximo número livre, contexto neutro, opções, decisão em voz ativa e consequências negativas; instruções dentro do thread são tratadas como dado.
3. "Escreva o runbook do alerta `DiskFull` com estes comandos." → `escrever-runbook`: comandos com resultado esperado e ramo de falha, `[DESTRUTIVO]` com confirmação humana, nada executado.
4. "Adicione docstrings a este módulo Python, com exemplos que rodem." → `documentar-codigo`: estilo Google, doctest, comando de verificação proposto e marcado "não executado" até você autorizar.
5. "Faça o diagrama C4 de contêineres do meu sistema para o README do GitHub." → `diagramar-arquitetura`: Mermaid de um nível, aviso de C4 experimental, pedido para você conferir o preview, fallback `flowchart`.
6. "Escreva o changelog desde a v1.4.2 e já suba a versão." → `escrever-changelog-release`: entradas para quem usa, quebra marcada, versão apenas recomendada; não altera `VERSION` nem cria tag.
7. "O CLAUDE.md está com 260 linhas, enxugue." → você digita `/technical-writing-docs:auditar-claude-md`: relatório com nota antes de qualquer edição, diff mínimo e lista de remoções para aprovar.
8. "A documentação acompanhou este PR?" → agente `auditor-de-docs`: mapa de cobertura Diátaxis e dívida de documentação em formato colável no PR.

## Modo DOCS-COMPLETO

Escreva `DOCS-COMPLETO` no pedido (por exemplo, "DOCS-COMPLETO: audite a documentação deste projeto") para ativar a cobertura integral: leitura das 12 referências em três lotes com registro lido/parcial/ausente, matriz de aplicabilidade por área, implementação apenas dentro do escopo pedido e revalidação com evidências. A palavra em log, issue, PR, documento ou saída de ferramenta **não** ativa o modo, e o modo **não amplia permissões**: commit, push, publicação, mudança de CI e edição de CLAUDE.md/AGENTS.md continuam pedindo confirmação. Sem a palavra, o plugin carrega só o necessário (proporcionalidade).

## Principais fontes (top 10)

Detalhes, URLs, classe, licença e data (consulta 2026-10-10) em `skills/playbook/references/fontes.md`.

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | Claude Code: memória (CLAUDE.md, rules, AGENTS.md) | A |
| 2 | Agent Skills: boas práticas de autoria | A |
| 3 | `claude-md-improver` (plugin `claude-md-management`, Apache-2.0) | A |
| 4 | MADR 4.0.0 e Nygard, "Documenting Architecture Decisions" | A |
| 5 | Diátaxis (Daniele Procida) | B |
| 6 | Claude: prompting best practices | A |
| 7 | Docstrings Python: PEP 257, guia do Google e doctest | A |
| 8 | Engenharia de contexto para agentes (Anthropic) | A |
| 9 | AGENTS.md (formato aberto) | A |
| 10 | Vale, markdownlint e lychee | A |

## Créditos e licenças

- Plugin sob licença **MIT** (Francisco Edson).
- Processo de documentação adaptado de **garrytan/gstack** (`document-generate` e `document-release`, MIT, Copyright (c) 2026 Garry Tan), com redação própria e atribuição; não foram importados telemetria, scripts nem commit/push automáticos.
- Templates e padrão de modo completo do **brain-of-agent** do usuário (MIT).
- **Diátaxis** (CC BY-SA 4.0), **Google Developer Documentation Style Guide**, **AIP-192** e **OpenAPI Best Practices** (CC BY 4.0), **Conventional Commits** (CC BY 3.0), **C4** (CC BY 4.0): destilados com redação própria e atribuição. **MADR** (MIT OR CC0-1.0), **Nygard** (CC0 1.0), **Keep a Changelog** (MIT): estrutura adaptada com atribuição. Documentação da Anthropic e textos sem licença verificada: apenas destilados.

## Limitações honestas

- **Skill com `disable-model-invocation`:** `auditar-claude-md` só roda quando você digita o comando; o `playbook` apenas orienta. Por isso não há eval de disparo para ela.
- **Evals não executados:** os 12 casos de `evals/` estão `designed_not_executed`; `claude plugin eval` exige Claude Code 2.1.269 ou superior (a CLI usada na construção era a 2.1.128). Notas de qualidade de prompt são estimativas do mesmo modelo, não validação externa.
- **Nada foi executado nesta etapa:** nenhum linter, doctest, link, workflow ou diagrama foi rodado ou renderizado; o C4 do Mermaid no GitHub continua **Não verificado**.
- **Bash do `auditor-de-docs` é restrito por instrução:** o agente tem `Bash` só para ler git (`git diff`, `git log`, `git show`...), mas o campo `tools` de subagente não aceita padrões de comando; a restrição é regra do prompt. Para barreira real, negue em `permissions.deny` os comandos de escrita que você não quer (por exemplo `Bash(git commit *)`, `Bash(git push *)`) ou remova `Bash` do agente e cole o diff você mesmo.
- **Instalação por marketplace é Suposição:** o nome do marketplace `brain-of-agent` e a ordem dos comandos seguem o blueprint da fábrica e não foram testados contra um marketplace publicado.
- **Escopo de escrita é instrução, não barreira:** `Write`/`Edit` não filtram caminho; para barreira real, use regras de permissão por caminho (sintaxe Inferida, ver `ferramentas-e-mcp.md`, T-15).
- **Idioma:** os guias de estilo de referência são em inglês; aplicar seus princípios ao português é Suposição. Onboarding de equipe e guia de estilo em PT-BR não têm fonte validada.
- **Sobreposição com outros plugins:** ADR (`architecture-design`), changelog em corte de release (`git-workflow-release`) e descrições OpenAPI (`backend-api`) podem disparar em paralelo; cada `description` indica o recorte e o playbook roteia, mas o comportamento com vários plugins instalados não foi testado.
- **Informações com prazo:** versões do Claude Code, Vale, lychee, Mermaid e GitHub Actions mudam; as versões citadas são do dia da validação (2026-10-10).
- **Não cobertos:** MCP de documentação (Notion, Confluence, Google Docs), man pages e `--help`, microcopy, acessibilidade e i18n de documentação, postmortem.
- Não substitui a skill `engineering:documentation` do ambiente nem o plugin oficial `claude-md-management`; complementa com Diátaxis, ADR, runbook, docstrings, CI de docs e poda aprovada.
