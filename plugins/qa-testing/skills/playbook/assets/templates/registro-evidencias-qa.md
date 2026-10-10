# Registro de evidências QA

Como usar: uma linha por evidência no resumo e um bloco por execução. Registre data, comando ou roteiro, ferramentas e versão, estado inicial, esperado e a fonte do oráculo, estado observado e a saída relevante. Referencie logs, traces, screenshots e registros persistidos. Oculte segredos e minimize dados pessoais (`<REDACTED>`). Adaptado do brain-of-agent (MIT).

| ID | Item ou caso | Método | Ambiente e revisão | Dados sanitizados | Resultado | Artefato | Limitação |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Execução

- **ID:** <id> · **Caso:** <id> · **Tentativa:** <n> · **Data:** <AAAA-MM-DD hh:mm UTC>
- **Método:** <execução / análise estática / revisão por IA / revisão humana>
- **Comando ou roteiro:** `<literal>` · **Versão das ferramentas:** <...>
- **Estado inicial:** <dados, flags, ambiente>
- **Esperado e fonte:** <resultado observável e de onde vem>
- **Obtido:** <saída real relevante, truncada; caminho do log>
- **Estado:** <passou / falhou / não executado / não verificável>
- **Artefatos:** <caminhos ou IDs>
- **Limitação e alcance da conclusão:** <o que esta evidência não prova>
- **Rótulo epistêmico:** <Verificado / Inferido / Suposição / Não verificável>

## Mudança e revalidação

- **Achado original:** <id> · **Correção e revisão:** <arquivos e commit>
- **Revalidação:** <casos, evidências, resultados> · **Regressões:** <escopo e resultados>
- **Primeira falha preservada:** <sim, onde> · **Pendências:** <o que falta>

Análise estática verifica o que é estático e não valida runtime; acessibilidade automática não substitui avaliação manual; avaliação por IA não equivale a revisão humana independente.
