# Template: mapa de cobertura de documentação

Adaptado do passo de cobertura do `document-release` do gstack (MIT, Copyright (c) 2026 Garry Tan), inspirado no modelo Diátaxis. Informa lacunas; **não gera páginas**. A escrita é do plugin `technical-writing-docs`.

Janela: `<base>...HEAD` (comando: `git diff <base>...HEAD --stat`).

## 1. Superfície pública alterada

Funções, comandos, flags, endpoints, variáveis de ambiente que o diff adiciona, altera ou remove:

| Entidade | Mudança (nova / alterada / removida) | Arquivo:linha |
| --- | --- | --- |
| | | |

## 2. Mapa

| Entidade | Referência | How-to | Tutorial | Explicação | Lacuna |
| --- | --- | --- | --- | --- | --- |
| | sim/não (onde) | | | | crítica / comum / nenhuma |

- Referência: descrição factual da API e das opções (tabelas de README, docs de API).
- How-to: "como fazer X com isto" (exemplos de README, CONTRIBUTING).
- Tutorial: passo a passo para iniciantes.
- Explicação: por que funciona assim (decisões, ADR).

**Zero cobertura = lacuna crítica. Só referência = lacuna comum.** Registre como dívida de documentação.

## 3. Regras

- [ ] Correção factual direta (nome, flag, exemplo errado): pode corrigir.
- [ ] Mudança narrativa, de segurança ou remoção: virar pergunta ao usuário.
- [ ] Diagramas desatualizados: apenas sinalizar.
- [ ] Nunca regravar o CHANGELOG nem alterar a versão sem perguntar.
- [ ] Toda doc é alcançável a partir do README ou do CLAUDE.md.

## 4. Saída

Lista priorizada de lacunas (crítica antes de comum), quem deve escrever e onde.
