# Plano de refatoração

Objetivo: [uma frase: o que melhora e o que NÃO muda]
Alvo: [arquivos/módulos]  ·  Data: [AAAA-MM-DD]  ·  Comando de testes: [comando]

## Usos e API pública

| Símbolo | Visibilidade | Chamadores (Grep) | Pode mudar? |
| --- | --- | --- | --- |
| | pública / interna | | não sem aprovação / sim |

## Rede de segurança

- Linha de base: [comando] -> [resultado colado]
- Cobertura do trecho: [testes existentes por nome] / lacunas: [entradas e bordas]
- Testes de caracterização a escrever: ver `characterization-test-log.md`
- Se não for testável: preservação só por leitura (Inferido); passos reduzidos.

## Passos (um por vez; testes após cada passo; se quebrar, desfazer o passo)

| # | Refatoração (nome do catálogo) | Escopo | Teste/comando | Desfazer | Risco |
| --- | --- | --- | --- | --- | --- |
| 1 | Replace Nested Conditional with Guard Clauses | `[arquivo:função]` | [comando] | reverter a edição | baixo |

## Commits (só com pedido do usuário)

- C1 refatoração pura: [passos 1–N]  ·  C2 comportamento (se houver): [...]  ·  Limiar de divisão: [~400 linhas / 10 arquivos, Suposição ajustável]

## Follow-ups (bugs e melhorias encontrados, não tratados aqui)

- [item, `arquivo:linha`, motivo]

## Riscos

- [risco e mitigação]

## Resultado (preencher ao final)

- Suíte antes: [saída]  ·  Suíte depois: [saída]  ·  Diff final conferido: [sim/não]  ·  Comportamento alterado: [nenhum / descrição]

Status: [DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT]
