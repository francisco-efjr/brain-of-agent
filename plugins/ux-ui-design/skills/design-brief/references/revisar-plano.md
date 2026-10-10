# Modo `revisar-plano`: nota 0 a 10 por dimensão

Use quando já existe um plano, spec ou mockup descrito, sem implementação. A revisão avalia o plano, não o código. Método adaptado do workflow `plan-design-review` do gstack (MIT, Garry Tan), com redação própria: o arquivo de passadas detalhadas daquele workflow não estava disponível no snapshot, então as dimensões abaixo são adaptação do plugin (Inferido), não cópia.

## Sumário

- [Procedimento](#procedimento)
- [Dimensões](#dimensões)
- [Exemplo de uma dimensão](#exemplo-de-uma-dimensão)
- [Saída](#saída)

## Procedimento

1. Leia o plano inteiro e o brief. Sem brief de uma linha, escreva um e peça confirmação.
2. Para cada dimensão: dê nota de 0 a 10, descreva em uma frase o que seria um 10 naquele contexto, liste a correção recomendada.
3. Para cada lacuna que exige decisão do usuário, faça **uma** pergunta com recomendação e alternativa. Não aplique correções em lote.
4. Termine com as três decisões abertas de maior impacto e a nota média informada sem falsa precisão (média simples das dimensões aplicáveis; dimensão sem material fica "sem dados", não zero).

A nota é uma opinião de modelo da mesma família que gerou o plano; não é validação com usuários.

## Dimensões

| # | Dimensão | O que procurar |
| --- | --- | --- |
| 1 | Hierarquia e arquitetura de informação | uma zona primária por tela; ponto de entrada claro; o que vem primeiro responde à tarefa; navegação responde onde estou e para onde posso ir |
| 2 | Estados e casos de borda | vazio, carregando, erro, texto longo, zero resultados, permissão negada, offline; cada um com texto e ação |
| 3 | Jornada e emoção | como a pessoa chega, hesita e sai; momentos de ansiedade (pagamento, exclusão) com reforço e saída |
| 4 | Risco de visual genérico | escolhas que coincidem com defaults de modelo; elementos que servem à decoração e não à tarefa |
| 5 | Sistema de design | tokens e componentes existentes reutilizados; valores novos justificados; nada de cor literal fora do plano |
| 6 | Responsivo e acessibilidade | 320 px, teclado, foco, contraste calculado, alvos, movimento reduzido, idioma |
| 7 | Decisões em aberto | o que o plano deixa para o desenvolvedor adivinhar; copy ausente; dados desconhecidos |

## Exemplo de uma dimensão

```text
2. Estados e casos de borda: 4/10
   Hoje: o plano desenha lista com resultados e o formulário de filtro.
   Seria um 10: lista vazia ("Nenhum pedido neste período" + botão "Limpar filtros"),
   carregando (esqueleto do mesmo formato da linha), erro de rede (causa + "Tentar de novo",
   filtros preservados), nome de cliente com 47 caracteres (quebra sem esconder o status).
   Correção: acrescentar os quatro estados à seção Estados do plano, com texto.
   Decisão sua: ao falhar a rede, mantemos os dados antigos na tela com aviso, ou limpamos a lista?
   Recomendo manter com aviso, porque evita perder o contexto da tarefa.
```

## Saída

Tabela (dimensão, nota, o que seria um 10, correção), seguida das decisões abertas numeradas e do rótulo: "Opinião de modelo, não validada com usuários. Nada foi renderizado."
