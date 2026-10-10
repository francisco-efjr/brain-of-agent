# As dez heurísticas: perguntas de inspeção e escala de severidade

Fonte: heurísticas de usabilidade de Jakob Nielsen (lista de 1990 com Rolf Molich, refinada em 1994); nomes oficiais conferidos em https://www.nngroup.com/articles/ten-usability-heuristics/ (V-11). O texto abaixo é redação própria; as perguntas de inspeção são do plugin (Inferido: conhecimento estável do domínio, não extraídas do artigo).

## Sumário

- [Heurísticas e perguntas](#heurísticas-e-perguntas)
- [Escala de severidade](#escala-de-severidade)
- [Como combinar frequência, impacto e persistência](#como-combinar-frequência-impacto-e-persistência)
- [Consolidação de várias passadas](#consolidação-de-várias-passadas)

## Heurísticas e perguntas

| # | Heurística (nome oficial) | Perguntas de inspeção | Sinais comuns em UI gerada |
| --- | --- | --- | --- |
| 1 | Visibility of system status (visibilidade do estado do sistema) | O sistema diz o que está acontecendo, onde estou, se salvou, se terminou? Há retorno em até um tempo razoável? | botão sem estado de carregamento; "salvo" sem confirmação; passos sem indicador de progresso |
| 2 | Match between system and the real world (correspondência com o mundo real) | Os termos são os do usuário? A ordem das informações segue o modelo mental dele? | jargão interno, códigos de erro, rótulos técnicos |
| 3 | User control and freedom (controle e liberdade) | Dá para desfazer, cancelar, voltar, sair de um erro? | cupom inválido que apaga o carrinho; modal sem fechar; fluxo sem "voltar" |
| 4 | Consistency and standards (consistência e padrões) | O mesmo termo e a mesma ação têm o mesmo nome e lugar em todo o produto? Segue convenções da plataforma? | dois estilos de botão primário; "Excluir" e "Remover" para a mesma ação |
| 5 | Error prevention (prevenção de erros) | O design evita o erro provável (restrições, padrões, confirmação em ação destrutiva, preservar o que foi digitado)? | campo de data livre em vez de seletor; "Excluir conta" a um clique; formulário que perde dados ao falhar |
| 6 | Recognition rather than recall (reconhecimento em vez de memorização) | A informação necessária está visível ou acessível no ponto de uso? | exigir lembrar código de um passo anterior; filtros escondidos |
| 7 | Flexibility and efficiency of use (flexibilidade e eficiência) | Há atalhos e caminhos rápidos para quem repete a tarefa, sem atrapalhar iniciantes? | sem teclado, sem atalhos, sem ações em lote em tela de uso diário |
| 8 | Aesthetic and minimalist design (estética e design minimalista) | Cada elemento serve à tarefa? Há informação irrelevante competindo com a relevante? | texto de boas-vindas, cartões decorativos, múltiplas chamadas principais |
| 9 | Help users recognize, diagnose, and recover from errors (reconhecer, diagnosticar e recuperar de erros) | A mensagem diz o que houve, por quê e o que fazer? Está perto da origem? Linguagem simples? | "Falha na operação", "Erro 500", erro só em vermelho sem texto |
| 10 | Help and documentation (ajuda e documentação) | Se for preciso ajuda, ela é encontrável, curta, orientada à tarefa? | ajuda só em PDF externo; ausência de ajuda em fluxo complexo |

Observações de uso:

- A heurística 7 pesa menos em fluxo de uso raro (recuperar senha) e mais em ferramenta de trabalho diária.
- A heurística 10 raramente é a mais grave; não force um achado para "cobrir" cada heurística. Heurística sem violação é registrada como "sem achados".
- Um mesmo problema pode violar mais de uma heurística: registre uma vez, com a principal e a secundária.

## Escala de severidade

Escala de 0 a 4, de um artigo de Nielsen de 1994 (https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/; V-11):

| Nota | Significado | Ação sugerida |
| --- | --- | --- |
| 0 | Não é problema de usabilidade (discordância de avaliador, escolha defensável) | Registrar em "trade-offs a validar" ou descartar |
| 1 | Cosmético | Corrigir se sobrar tempo |
| 2 | Problema menor | Baixa prioridade |
| 3 | Problema maior | Alta prioridade; corrigir antes do próximo marco |
| 4 | Catástrofe de usabilidade | Corrigir antes do lançamento |

O artigo de procedimento de avaliação heurística (2023) não traz essa escala; não atribua a escala a ele.

## Como combinar frequência, impacto e persistência

Escreva uma linha por fator, sem fórmula numérica falsa:

- **Frequência**: todos, a maioria, uma parte, poucos que passam por esse ponto.
- **Impacto**: fácil, moderado ou difícil de superar quando acontece; perde dados ou dinheiro?
- **Persistência**: o usuário aprende o contorno na primeira vez ou tropeça de novo a cada uso?

Regra prática do plugin (Inferido): impacto difícil de superar com frequência alta e persistência alta é 4; impacto difícil com frequência baixa tende a 3; qualquer coisa fácil de contornar e que só atrapalha na primeira vez tende a 1 ou 2. Justifique a nota, não esconda o raciocínio.

## Consolidação de várias passadas

1. Junte os achados e agrupe por local e heurística (affinity). Dois achados no mesmo elemento com a mesma causa são um.
2. Para cada grupo, registre quantas passadas o apontaram e a faixa de severidade.
3. Achado visto por uma passada só e com evidência forte permanece; achado visto por uma passada só e sem evidência concreta vai para "a confirmar".
4. Lembre que as passadas são do mesmo modelo: concordância não equivale a validação independente.
