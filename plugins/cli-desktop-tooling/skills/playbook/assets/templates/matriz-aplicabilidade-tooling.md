# Matriz de aplicabilidade (modo TOOLING-COMPLETO)

Preencha uma linha por área. Colunas finais: aplicável (sim, não ou não aplicável com motivo), evidência `arquivo:linha`, status (conforme, lacuna, não verificável) e ação. Falta de acesso é Não verificável, nunca "conforme". A matriz amplia a análise e não amplia autorização.

- Projeto: [NOME] · Tipo: [CLI | TUI | Electron | Tauri | .NET | Qt | scripts] · Data: [AAAA-MM-DD]
- Escopo autorizado: [somente análise | implementação em arquivos do repositório] · Ações externas autorizadas: [nenhuma | lista nomeada]

## Registro de leitura das referências

| Lote | Arquivos | Estado (lido / parcial / ausente) | Decisões extraídas |
| --- | --- | --- | --- |
| 1 | checklist-completo, padroes-e-antipadroes, decisoes-e-tradeoffs | | |
| 2 | cli-e-agentes, tui | | |
| 3 | desktop-stacks-e-seguranca | | |
| 4 | distribuicao-assinatura-update | | |
| 5 | scripts-powershell-e-shell, dx-e-claude-code | | |
| 6 | claude-md-snippets, ferramentas-e-mcp, fontes | | |

## Áreas (fontes por tipo de projeto)

| Área | CLI | TUI | Electron | Tauri | .NET | Qt | Scripts |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Design de CLI e agentes | V-13, V-11, V-12, V-64 | V-13 (subconjunto) | n/a | n/a | n/a | n/a | V-13 |
| Teclado, foco, teste de UI | n/a | V-30 a V-32 | lacuna | lacuna | V-33, V-35 | lacuna | n/a |
| Segurança de código e config | V-13 (segredos) | n/a | V-16, V-48 | V-19, V-47 | lacuna | lacuna | V-57, V-61 |
| Acessibilidade | n/a | lacuna declarada | lacuna | lacuna | V-35 | lacuna | n/a |
| Empacotamento e instalador | n/a | n/a | V-17, V-40 a V-43 | V-46, V-43 | V-36, V-40 | V-38 | n/a |
| Assinatura e notarização | n/a | n/a | V-17, V-44, V-45 | V-46, V-44, V-45 | V-44, V-40 | V-38, V-45 | n/a |
| Auto-update | n/a | n/a | V-18, V-49 | V-20, V-21 | V-40 | lacuna | n/a |
| Licença e distribuição | n/a | n/a | n/a | n/a | n/a | V-39 | n/a |
| Qualidade de script | n/a | n/a | n/a | n/a | n/a | n/a | V-14, V-15, V-57 a V-63 |
| DX e onboarding | V-22, V-64 | V-22 | V-22 | V-22 | V-22 | V-22 | V-22 |
| Claude Code (contexto, hooks, CI) | V-06 a V-10, V-51, V-52 | idem | idem | idem | idem | idem | idem |

"lacuna" nas colunas de stack significa: sem fonte validada; declare Não verificável.

## Resultado por área

| Área | Aplicável | Evidência (arquivo:linha) | Status | Ação |
| --- | --- | --- | --- | --- |
| [uma linha por área acima] | | | | |

## Implementação e revalidação (se autorizadas)

| Item | Alteração (antes e depois, arquivos) | Verificação executada (comando, saída) | Resultado | Invalidou evidência anterior? |
| --- | --- | --- | --- | --- |

## Resultado final

[Concluído no escopo | Parcial | Impedido]. Falta de leitura obrigatória, de acesso ou de execução material torna o resultado parcial. Falha crítica impede recomendação favorável.

## Não verificável e lacunas que afetam o projeto

[Lista de `fontes.md`, seção 5, aplicável ao projeto.]
