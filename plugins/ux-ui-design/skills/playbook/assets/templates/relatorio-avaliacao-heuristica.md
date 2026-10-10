# Avaliação heurística: [tela ou fluxo, escopo estreito]

Template T-03. Uso: `heuristic-eval`. Um agente produz uma opinião, não validação com usuários; tudo vindo de leitura de código ou de imagem é Inferido. Proibido projetar taxa de abandono ou conversão.

## 1. Escopo

- **Fluxo e tarefa:** [ex.: recuperar senha, do link "Esqueci" até o login]
- **Tipo de usuário:** [___]
- **Material:** [descrição, capturas, markup]
- **Passadas:** [1 | 2 | 3 independentes (contextos separados)] · **Data:** [AAAA-MM-DD]

## 2. Achados

Passada 1 serve para aprender o fluxo; passada 2 procura violações. Severidade 0 a 4 (0 não é problema, 1 cosmético, 2 menor, 3 maior, 4 catástrofe), a partir de frequência, impacto e persistência.

| ID | Heurística | Local exato | Evidência | Sev. | Frequência / impacto / persistência | Correção | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H-01 | [9. Reconhecer, diagnosticar e recuperar de erros] | [passo 3, banner de erro] | ["Falha na operação" sem causa nem ação] | [3] | [toda falha / bloqueia a tarefa / toda tentativa] | [dizer o que houve, por quê e o que fazer] | [Inferido] |

As dez heurísticas: visibilidade do estado do sistema; correspondência com o mundo real; controle e liberdade; consistência e padrões; prevenção de erros; reconhecimento em vez de memorização; flexibilidade e eficiência; estética e design minimalista; ajudar a reconhecer, diagnosticar e recuperar de erros; ajuda e documentação.

## 3. Consolidação (quando houve mais de uma passada)

Agrupamento por afinidade: [achados repetidos em mais de uma passada → mais confiança; achado em uma só → verificar].

## 4. Trade-offs a validar

Violações que podem ser escolha defensável de contexto (não são "problema" até haver evidência):

| ID | Violação aparente | Por que pode ser defensável | Como validar |
| --- | --- | --- | --- |
| T-01 | [___] | [___] | [teste com 5 participantes do perfil / dado de uso] |

## 5. Top 3 e o que testar com usuários

1. [H-0x: achado de maior severidade] → teste: [tarefa e métrica observável, sem prever resultado]
2. [___]
3. [___]

## 6. Limites

Avaliação feita por [um agente | N passadas do mesmo modelo]: opinião de modelo da mesma família. Não substitui pesquisa com usuários (`user-research-plan`). A escala 0 a 4 vem de artigo de 1994; o procedimento de 3 a 5 avaliadores humanos independentes vem de artigo de 2023.
