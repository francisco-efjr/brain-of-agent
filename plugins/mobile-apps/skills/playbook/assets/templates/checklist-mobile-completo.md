# Checklist MOBILE-COMPLETO

Adaptado dos templates `checklist-fullstack-completo` e `checklist-qa-completo` do brain-of-agent (MIT, Francisco Edson). Preencha ao rodar o modo `MOBILE-COMPLETO` (somente por pedido explícito do usuário). O modo amplia a análise, não a autorização.

Projeto: [nome] · Pedido e escopo: [objetivo] · Revisão e ambiente: [commit, SO, emulador/aparelho] · Data: [AAAA-MM-DD]
Autorização: [análise / implementação local / ações externas específicas, se houver]

## 1. Leitura das referências

Estados: lido, parcial, ausente. Registre o ponto de retomada quando parcial.

| Lote | Arquivo (skills/playbook/references/) | Estado | Decisão extraída |
| --- | --- | --- | --- |
| 1 | checklist-completo.md | | |
| 1 | padroes-e-antipadroes.md | | |
| 1 | decisoes-e-tradeoffs.md | | |
| 2 | [ios-swift.md / android-compose.md / cross-platform-rn-flutter.md] | | |
| 3 | dados-push-permissoes-seguranca.md | | |
| 4 | qualidade-performance-a11y-testes.md | | |
| 5 | loja-release-ambiente.md | | |
| 5 | ferramentas-e-mcp.md | | |
| 5 | fontes.md | | |
| 5 | claude-md-snippets.md | | |

## 2. Capacidades do ambiente

| Capacidade | Disponível / indisponível | Limite | Evidência |
| --- | --- | --- | --- |
| Ler e editar arquivos | | | |
| Shell, build e testes (Gradle, npm, flutter) | | | |
| macOS, Xcode, simulador iOS | | | |
| Emulador Android ou aparelho físico | | | |
| Rede e contas de loja (somente ações do usuário) | | | |

## 3. Matriz de aplicabilidade

Aplicável (sim / não / não aplicável com motivo) · evidência (arquivo:linha) · status (conforme / lacuna / não verificável) · ação.

| Área | Plataforma | Aplicável | Evidência | Status | Ação | IDs do checklist |
| --- | --- | --- | --- | --- | --- | --- |
| Arquitetura e estado | | | | | | ARQ |
| Concorrência | | | | | | ARQ, ANT-07 a 10 |
| Dados offline e sync | | | | | | DAD, RDE |
| Push | | | | | | PSH |
| Permissões | | | | | | PRM |
| Deep links | | | | | | LNK |
| Segurança | | | | | | SEG |
| Performance e bateria | | | | | | PRF, BAT |
| Acessibilidade | | | | | | ACE |
| Testes | | | | | | TST |
| Release e loja | | | | | | IOS, AND, PIP |
| Ambiente e processo | | | | | | AMB |

## 4. Backlog rastreável

Estados: pendente, inferido, verificado, falhou, não autorizado, não aplicável, não verificável. Implementação concluída não é critério verificado.

| ID | Requisito ou risco | Oráculo | Análise | Implementação (arquivos) | Validação | Revalidação | Evidência | Pendência |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 5. Gates

- [ ] Versão do SDK e alvo mínimo lidos antes de qualquer recomendação.
- [ ] Arquitetura existente identificada e seguida.
- [ ] Implementação apenas dentro do escopo; bugs vizinhos viraram follow-up.
- [ ] Verificação executável com saída colada; o que não foi executado está dito.
- [ ] Revalidação após a última mudança relevante.
- [ ] Nenhuma ação externa (submissão, OTA em produção, certificados) sem ficha confirmada.
- [ ] Fatos voláteis com data de verificação.
- [ ] Passagens humanas (leitor de tela, aparelho físico) listadas como pendência.

Leitura: [integral / parcial] · Execução: [completa no escopo / parcial / não executada]
Resultado: [concluído no escopo / parcial / impedido] · Críticos abertos: [IDs] · Próximo passo: [texto]
Observação: revisão feita pelo mesmo modelo que implementou não é validação independente.
