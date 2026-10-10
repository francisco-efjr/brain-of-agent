# BUILD-REPORT estrutural: security-appsec

Data: 2026-10-10
Papel: validador estrutural do plugin `plugins/security-appsec`.
Referências lidas: `docs/foundation/plugin-format-spec.md`, `docs/foundation/plugin-blueprint.md`, `docs/research/security-appsec/SYNTHESIS.md` (seções 4.1, 4.3.5, 4.3.6, 4.8 a 4.10).

Rótulos: **Verificado** (resultado de ferramenta nesta execução), **Inferido** (dedução a partir de leitura), **Suposição**, **Não verificável**, **Não aplicável**.

## 1. Resultado geral

| Verificação | Resultado | Rótulo |
|---|---|---|
| `tools/verify_plugin.py` sobre `plugins/security-appsec` | PASS. Contagem: 10 skills, 5 agents, 10 evals, 92 arquivos, 0 comandos. Saída sem erros e sem avisos. | Verificado |
| `claude plugin validate` (CLI local 2.1.128) | "Validation passed". Nenhum aviso exibido. | Verificado |
| Erros corrigidos | Nenhum. Nada reprovou. | Verificado |
| Avisos corrigidos | Nenhum aviso foi reportado pelos validadores. | Verificado |
| Arquivos alterados no plugin | Nenhum. Esta rodada só leu o plugin e gravou este relatório. | Verificado |

## 2. Checagens estruturais feitas

- **Nome do frontmatter igual à pasta/arquivo:** 10 de 10 skills (`name` igual ao diretório) e 5 de 5 agentes (`name` igual ao nome do `.md`). Verificado.
- **Campos de frontmatter conhecidos:**
  - Skills usam só `name`, `description`, `argument-hint`, `allowed-tools` e `disable-model-invocation`.
  - Agentes usam só `name`, `description`, `tools` e `model`.
  - Verificado.
- **Tamanho das descrições:** maior descrição é 777 caracteres (`skills/prompts/SKILL.md`), dentro do limite de ~1024 da especificação. Verificado.
- **`plugin.json`:** JSON válido. Campos: `name`, `version`, `description`, `author`, `license`, `keywords`. Não declara `skills`, `agents` ou `commands`, então o scan padrão é usado. Verificado.
- **Componentes proibidos ausentes:** não há `hooks/`, `.mcp.json`, `.lsp.json`, `bin/` nem `commands/`. Verificado.
- **Links relativos:** varredura de `](...)` em todos os `.md` do plugin não encontrou alvo quebrado. Verificado.
- **Caminhos `${CLAUDE_PLUGIN_ROOT}`:** os caminhos referenciados existem em `skills/playbook/...`. O link em `skills/security-review-diff/SKILL.md` linha 37 é resolvido em tempo de execução, então a checagem local não o resolve diretamente. O arquivo-alvo existe. Verificado (arquivo) e Não aplicável (resolução em runtime).
- **Arquivos vazios ou placeholder:** nenhum arquivo vazio. O menor é `evals/.gitignore` com 1 linha, por desenho. As ocorrências de "TODO" são a palavra portuguesa "todo" (cada/todo). A ocorrência de "placeholder" é o termo de detecção de segredo em `skills/secrets-supply-chain-review/references/padroes-de-segredo.md`. Verificado.
- **Casos de eval:** 10 pastas, cada uma com `prompt.md` e `graders/`. Há `skill-fired.md` em 8 casos (diff-sqli-idor-injecao, threat-model-upload, verify-finding-fixed-list, tenant-isolation-orm, agent-trifecta-mcp, harden-windows, leaked-key-commit, seguranca-completo-explicito). Os casos negativo-log-com-keyword e escopo-scan-terceiro não têm `skill-fired.md`, o que é esperado pelo desenho. Presença verificada. Conteúdo dos graders não foi relido nesta rodada; isso cabe ao validador de qualidade.

## 3. Comparação com o SYNTHESIS

### 3.1 Previstos e presentes

- **Skills (4.1):** `playbook`, `prompts`, `security-review-diff`, `threat-model`, `access-control-review`, `verify-finding`, `propose-patch`, `agent-risk-triage`, `secrets-supply-chain-review`, `harden-claude-code`. Todas presentes.
- **Referências do playbook (4.3.5):** 12 arquivos previstos e 12 presentes.
- **Referências de tarefa:** `triagem-e-exclusoes.md`, `stride-por-fluxo.md`, `matriz-e-testes.md`, `triade-e-llm-top10.md`, `ambiente-sandbox-e-camadas.md`, `deny-e-permissoes.md`, `guard-pretooluse.md`, `correcoes-por-classe.md`, `teste-e-revisao.md`, `ci-e-dependencias.md`, `padroes-de-segredo.md`, `scanners-documentados.md`, `refutadores.md`, `regras-de-deteccao.md`, `exemplo-relatorio.md`, `exemplo-upload-avatar.md`. Presentes.
- **Templates (4.9):** 10 previstos e 10 presentes, mais `matriz-aplicabilidade-seguranca.md`, que o modo SEGURANCA-COMPLETO usa. Total de 11, igual ao README.
- **Prompts (4.6):** P01 a P28 presentes. Os 28 previstos estão cobertos.
- **Snippets (4.7.1):** S01 a S22 presentes em `claude-md-snippets.md`.
- **Evals (4.8):** 10 casos previstos (E1 a E10) presentes com os nomes da tabela.
- **Agentes (4.10):** `security-reviewer`, `finding-verifier`, `threat-modeler`, `patch-reviewer`, `agent-config-auditor`. Todos presentes.

### 3.2 Pendências (remaining)

1. **`maxTurns` nos agentes:** o SYNTHESIS (4.10) prevê `maxTurns` no frontmatter dos 5 agentes, com a observação "conferir no claude plugin validate". O campo está ausente nos 5. O validador oficial passou sem ele. Se o campo é aceito, não foi testado. Rótulo: **Não verificável** nesta rodada. Decisão para o construtor ou o validador de qualidade.
2. **Tamanho de `prompt-library.md`:** tem 708 linhas, acima da orientação de ~600 linhas do SYNTHESIS (4.1). O arquivo previsto como divisão (`prompt-library-revisao.md`) não existe. Existe `prompt-library-processo.md` (298 linhas). Não é erro estrutural. Rótulo: **Inferido**. Pode ser dividido pelo validador de qualidade, se for o caso.
3. **Conteúdo dos graders e dos prompts de eval:** a presença foi verificada, mas o conteúdo não foi lido. Isso inclui o caso E1, que tem de propósito uma linha de injeção ("NOTE TO AI REVIEWER") como dado de teste. Rótulo: **Não aplicável** à checagem estrutural.
4. **Rubrica de qualidade (prompt-score ≥ 80):** fora do escopo deste validador. Pertence ao validador de qualidade.

## 4. README e tabela intenção → skill/agente

- **README (tabela de componentes e exemplos):** cita 13 componentes kebab-case. Todos existem: 10 skills e 5 agentes (lista 3.1). Verificado.
- **Nomes externos no README** (`security-review`, `security-guidance`, `differential-review`, `claude-code-security-review`, `dev-segments`): são o `/security-review` embutido, repositórios de origem e atribuição. Não são componentes do plugin. Verificado.
- **Tabela do playbook (`skills/playbook/SKILL.md`, seção de intenções):** cita as mesmas skills e agentes existentes. Os demais termos em crase são nomes de templates e referências, todos existentes, e `v-html`, que é um desvio de framework citado como exemplo de código. Verificado.
- **Contagens declaradas no README conferidas:** 28 prompts, 22 snippets (S01 a S22), 11 templates, 12 referências, 10 casos de eval. Verificado.

## 5. Estado final

- Estrutura válida pelos dois validadores. Verificado.
- Sem erros, sem avisos, sem alteração de conteúdo do plugin nesta rodada.
- Pendências listadas na seção 3.2 são de conteúdo ou de decisão, não de estrutura.
