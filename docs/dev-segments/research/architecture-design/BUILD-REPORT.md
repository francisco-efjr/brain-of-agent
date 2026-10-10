# BUILD-REPORT: architecture-design

Data: 2026-10-10 · Plugin: `plugins/architecture-design` · Gate final consolidado.

## Resultado

| Verificação | Resultado |
| --- | --- |
| `python tools/verify_plugin.py plugins/architecture-design` | `RESULT: PASS` (sem ERROS) |
| `claude plugin validate plugins/architecture-design` | `Validation passed` |

Nenhuma correção nova foi necessária nesta rodada do gate: ambas as validações passaram sem edições no plugin.

## Contagens

Contagens obtidas por `verify_plugin.py` e por leitura direta dos arquivos (Verificado):

| Componente | Quantidade | Observação |
| --- | --- | --- |
| Skills (`skills/*/SKILL.md`) | 10 | 8 de tarefa, `playbook` e `prompts` de apoio |
| Agentes (`agents/*.md`) | 5 | `adr-writer`, `architecture-blueprint`, `architecture-reviewer`, `boundary-mapper`, `skeptic-architect` |
| Prompts na biblioteca (`prompt-library.md`) | 28 | entradas PR-01 a PR-28 |
| Blocos de código cercados na biblioteca | 31 | 62 linhas de cerca, em pares; inclui modelos e exemplos que não são prompts completos |
| Casos de eval (`evals/*/prompt.md`) | 11 | inclui caso negativo (`negativo-limitrofe`) |
| Arquivos de referência (`skills/*/references/*.md`) | 30 | Contagem por leitura de arquivos |
| Templates (`skills/playbook/assets/templates/*.md`) | 16 | |
| Arquivos totais do plugin | 104 | saída do verificador |

Nota: o relatório de qualidade citava "12 referências" como número do blueprint. A contagem real dos arquivos em `references/` é 30, e a diferença fica registrada aqui como Verificado pela contagem atual, não como divergência do plugin.

## Relatório de qualidade (resumo)

Fonte: `BUILD-REPORT-quality.md` (validador de prompt, rubrica D1–D12). Julgamento por leitura, não medição. Nenhum eval foi executado.

- Média antes ≈ 81,0; média depois ≈ 83,9; mínimo depois = 86; 21 unidades pontuadas.
- Correções de fidelidade técnica com fonte: `allowed-tools` não restringe ferramentas (pré-aprova só no turno de invocação; para remover existe `disallowed-tools`); regra de permissão correta é `Edit(/docs/.../**)`, não `Write(...)`; códigos Idempotency-Key 400/422/409 conferidos no rascunho IETF rev. 07 (status expirado).
- Segurança: revisores e arquitetos somente leitura; só `adr-writer` tem Write, sob pedido explícito; skills com efeito usam `disable-model-invocation: true`.
- Direitos autorais: literais de template e mensagem inicial são do brain-of-agent (MIT, Francisco Edson), com atribuição; OWASP aparece só destilado.

## Pendências

1. `BUILD-REPORT-structural.md` não existe em `docs/research/architecture-design/`. O relatório estrutural não foi encontrado; não é possível confirmar se o validador estrutural rodou. Verificado pela listagem da pasta.
2. Evals em estado `designed_not_executed`. O `claude plugin eval` exige versão do Claude Code mais recente que a instalada na época da revisão de qualidade (2.1.128). Não verificado nesta rodada qual versão está instalada.
3. `disallowed-tools` conferido na documentação, não testado em sessão real. Versões antigas podem ignorar o campo (Não verificado).
4. Regras `Edit(/docs/adr/**)` e o hook de exemplo não foram testados integrados ao Claude Code.
5. Não há caso de eval próprio para `adr-write`, `architecture-plan` nem para os agentes. São 11 casos; manter ou cortar fica com o dono do plugin.
6. Lacunas de fonte primária (Inferido): Clean Architecture, Evans/Vernon, fitness functions, load shedding, STRIDE da Microsoft e o status "experimental" do C4 no Mermaid.
7. `graphify update .` não foi executado nesta rodada: nenhum arquivo de código foi alterado.

## Saídas resumidas das validações

```
verify_plugin.py: Plugin: architecture-design {'skills': 10, 'agents': 5, 'commands': 0, 'evals': 11, 'files': 104}
verify_plugin.py: RESULT: PASS
claude plugin validate: Validation passed
```
