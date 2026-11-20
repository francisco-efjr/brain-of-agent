# Pedido em quatro partes: <título curto>

Data e hora: <AAAA-MM-DD HH:MM> · Responsável (decide e assina): <nome> · Executor: <agente>

## Problema real (questionar a pergunta)

<Uma frase: que problema o pedido resolve e para quem? Dá para resolver com menos software? Solução pronta pesquisada: <o que foi visto e por que serve ou não> (PED-07, ENG-06).>

## 1. O que eu quero

<Resultado, em palavras do usuário real, sem jargão. Número que deve mudar: <métrica atual → alvo> (PED-03, PED-09).>

## 2. Como, em linhas gerais

<Abordagem desejada, arquivos ou módulos a tocar, exemplo vivo a seguir ("faça como no módulo X"). Deixe o detalhe do código para o agente depois de dar o contexto (PED-P02).>

## 3. O que eu NÃO quero (restrições e pressupostos)

- <não mexer em X · não adicionar dependência Y · não alterar o contrato Z>
- <o que não pode quebrar>
- <idiomas, plataformas ou formatos: perguntar, não presumir (PED-P06)>

## 4. Como saber que deu certo

| Critério | Como medir (comando, medida, observação) | Quem escreve a verificação |
| --- | --- | --- |
| <critério 1> | <comando e saída esperada> | <outro agente ou humano> |

Para formalizar o oráculo, use `definir-oraculo`.

## O que a máquina não sabe

- Data e hora atuais: <...>. Dados ausentes: <lista>; "sem dado" ≠ "zero medido" (PED-11).
- Volumes que crescem: <...> · Latência-alvo: <...> · Dados sensíveis: <...>
- Operações que precisam ser idempotentes: <...> · Hardware e ambiente: <...>

## Comportamento em falha e sob restrição

| Situação | Comportamento esperado |
| --- | --- |
| Serviço externo fora | <retry com limite, degradar, alertar> |
| Cancelamento no meio | <...> |
| Dado corrompido ou arquivo movido | <...> |
| Carga e volume reais | <...> |

Exigências que o agente não faz por iniciativa: retry, timeout, segurança por classe de falha, vazamento de memória (PED-15).

## Funcionalidades que podem estar faltando

<Lista pedida ao agente: cota, erros, limites, termos, internacionalização (PED-08).>

## Plano (revisado antes de executar)

1. <passo> · verificação: <...>
2. <passo destrutivo ou irreversível> · [APROVAÇÃO HUMANA] · passa por `guardar-destrutivo`
3. <...>

## Suposições e decisões pendentes

| # | Suposição ou decisão | Dono | Rótulo (Suposição / Inferido / Não verificável) |
| --- | --- | --- | --- |
| 1 | <...> | <nome> | <...> |

Esforço calibrado: <experimento descartável | resultado que importa> (PED-18).
