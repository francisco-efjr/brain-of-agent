# Matriz de aplicabilidade: FRONTEND-COMPLETO

Preencha no modo FRONTEND-COMPLETO (só por pedido explícito do usuário). Uma linha por área. **Aplicável** exige itens e evidência; **Não aplicável (NA)** exige motivo; **Não verificável (NV)** exige o que faltou (acesso, ambiente, fonte). "Completo" é cobertura desta matriz com limitações honestas, não caixas verdes. Itens `FE-nn` estão em `references/checklist-completo.md`. Projeto: [nome]. Data: [AAAA-MM-DD]. Pedido do usuário (escopo autorizado): [texto].

| Área | Status | Itens aplicados (FE-nn) | Evidência | Limitação |
| --- | --- | --- | --- | --- |
| A. Estados e dados | [Aplicável / NA (motivo) / NV (o que faltou)] | [FE-01..] | [comando, saída, captura, `arquivo:linha`] | |
| B. Semântica e acessibilidade | | | | |
| C. Formulários | | | | |
| D. Renderização e cache | | | | |
| E. Performance | | | | |
| F. Segurança no cliente | | | | |
| G. Testes e verificação | | | | |
| H. Design e tokens | | | | |
| I. Tooling e CI | | | | |
| J. i18n e SEO | NV (sem fonte validada no plugin) | | | |

## Capacidades e limites do ambiente

| Capacidade | Disponível? | Consequência |
| --- | --- | --- |
| Leitura de arquivos | [sim/não] | |
| Escrita de arquivos | | auditoria só relata |
| Shell (build, teste) | | sem shell: runtime Não verificado |
| Navegador (Chrome conectado, Playwright) | | sem navegador: lista de verificações e Não verificado |
| Rede | | |
| Acesso ao Figma | | leitura primeiro; escrita só por pedido explícito |

Ausência de ferramenta é limitação verificável, não defeito da aplicação.

## Gates

| Gate | Cumprido? | Evidência |
| --- | --- | --- |
| Entendimento | | |
| Plano | | |
| Implementação | | |
| Validação | | |
| Revalidação | | |
| Entrega | | |

Resultado: [concluído no escopo / parcial / impedido]. Falha crítica impede recomendação favorável. Falta de leitura obrigatória ou de execução material torna o modo parcial.

## Declarações obrigatórias

- A revisão foi feita pelo mesmo modelo que implementou? [sim/não; se sim, não é validação independente]
- O modo não ampliou permissões: instalação, push, deploy, hooks, MCP e escrita no Figma seguiram o que o usuário autorizou no chat.
- Implementação ficou dentro do escopo pedido: [sim/não e exceções].
