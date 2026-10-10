# Relatório de revisão de UI: [escopo revisado]

Modelo para auditoria e revisão de frontend (somente leitura: a revisão não altera o produto). Revisor: [agente ou pessoa]. Se a revisão foi feita pelo mesmo modelo que escreveu o código, declare: não é validação independente. Data: [AAAA-MM-DD].

## Escopo e premissas

- Arquivos ou rotas revisados: [lista]
- Fora do escopo: [lista]
- Versões lidas: [framework, React, Tailwind, etc., do `package.json`]; o que não foi lido: [lista]
- Critério de reporte: apenas lacunas de correção ou requisito; preferência de estilo não entra. Limiar de confiança: [7 de 10; Suposição configurável]

## Achados

| ID | Severidade | Confiança (1-10) | Arquivo:linha | Cenário concreto | Ação |
| --- | --- | --- | --- | --- | --- |
| UI-01 | [Crítico / Alto / Médio / Baixo] | [n] | [caminho:linha] | [quem faz o quê e o que dá errado] | [correção mínima] |

Severidade: Crítico = tarefa impossível, perda de dado ou brecha de segurança; Alto = confunde, prende o foco, esconde erro ou quebra em fluxo principal; Médio = atrito com contorno; Baixo = polimento. Se não há achados acima do limiar, escreva "sem lacunas" explicitamente.

## O que está bom

[pontos que devem ser preservados, curtos]

## Não relatado (abaixo do limiar ou fora do escopo)

[itens vistos e descartados, com motivo, para o leitor não repetir a busca]

## Verificado, Inferido e Não verificado

| Item | Rótulo | Evidência ou limitação |
| --- | --- | --- |
| [afirmação] | [Verificado / Inferido / Suposição / Não verificável] | [comando e saída, captura, `arquivo:linha`, ou o que faltou] |

Leitura de código não é teste executado. Comportamento de leitor de tela que não foi observado é Inferido.

## Pendências e próximo passo

[o que depende de decisão humana, o que exige teste manual, o próximo passo concreto]
