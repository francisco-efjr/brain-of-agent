# Relatório de upgrade de OpenTelemetry — [PROJETO] — [data]

Template T-12. Estrutura de cinco seções destilada do skill `otel-upgrade` (ollygarden/opentelemetry-agent-skills, Apache-2.0, OllyGarden; V-28), redação própria, com atribuição. Valide em **cópia isolada** do repositório; este plugin não executa instaladores nem comandos de upgrade. Cada tipo de verificação prova pouco por si: resolução de dependência, compilação, aceitação de configuração e testes são evidências distintas.

**Data da consulta às fontes primárias:** [AAAA-MM-DD] (changelog/release notes: [links]). Cópia isolada: [caminho/branch/worktree].

## Versões (registrar separadamente)

| Componente | Atual | Última estável | Candidata validada | Observação |
| --- | --- | --- | --- | --- |
| Wrapper / bootstrap | [..] | [..] | [..] | |
| Distribuição | [..] | [..] | [..] | |
| Artefato (SDK/agente) | [..] | [..] | [..] | |
| Collector (se houver) | [..] | [..] | [..] | |

## 1. Recomendação

[Fazer upgrade para [versão] / adiar / não atualizar], por quê, em uma frase.

## 2. Achados

| ID | Achado | Uso real no repositório (arquivo:linha) | Impacto |
| --- | --- | --- | --- |
| F1 | [mudança de comportamento/atributo/convenção] | [..] | [..] |

Só entram mudanças que o código do repositório usa de fato.

## 3. Caminho proposto

[Passos em ordem; começar pela estável mais nova; se falhar, tentar versões menores; mudanças de configuração necessárias.]

## 4. Validação

| Verificação | Comando (na versão instalada) | Resultado real (colar) | O que prova | O que não prova |
| --- | --- | --- | --- | --- |
| Resolução de dependências | [..] | [..] | versões compatíveis | comportamento |
| Compilação | [..] | [..] | API compatível | telemetria correta |
| Aceitação da configuração | [..] | [..] | formato válido | semântica |
| Testes | [..] | [..] | comportamento coberto | o não coberto |

Se não houve execução: "Não verificável: [motivo]".

## 5. Risco residual

[O que pode divergir em produção; verificação sugerida pós-deploy (T-11); rollback.]
