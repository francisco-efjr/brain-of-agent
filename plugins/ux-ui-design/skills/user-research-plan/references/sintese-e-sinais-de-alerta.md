# Síntese de pesquisa, teste do insight e sinais de alerta

Fontes: seis fases, sinais de alerta e teste do insight da skill `ux-research` do rampstackco/claude-skills (MIT; autoridade baixa, sem evals; V-16); crítica de design em equipe do NN/g (Sarah Gibbons, 2016-10-23; V-18). As regras numéricas ("6 de 8", "7 para agendar 5") são heurísticas do autor, não normas: rotuladas Inferido. Redação própria. Este arquivo só vale para notas que o usuário forneceu: sem notas, não há síntese.

## Sumário

- [Procedimento de síntese](#procedimento-de-síntese)
- [Teste do insight](#teste-do-insight)
- [Sinais de alerta](#sinais-de-alerta)
- [Formato da síntese](#formato-da-síntese)
- [Crítica de design em equipe (30 min)](#crítica-de-design-em-equipe-30-min)

## Procedimento de síntese

1. **Inventário das notas.** Liste o que foi fornecido (participantes P1..Pn, sessões, ferramentas). Se algum participante não tem notas, ele não conta.
2. **Extrair observações.** Uma observação por linha, com origem (P2, minuto 14) e citação literal quando houver. Não parafraseie quando for atribuir fala à pessoa.
3. **Agrupar por afinidade.** Observações parecidas viram um tema; dê ao tema um nome descritivo (o que acontece, não o que fazer).
4. **Contar.** Para cada tema, informe em quantos participantes ele aparece **nas notas fornecidas** (por exemplo "4 de 5"). Não extrapole para a população.
5. **Interpretar e recomendar.** Em colunas separadas: observação (o que se viu), interpretação (por que acreditamos que acontece) e recomendação (o que mudar ou testar).
6. **Aplicar o teste do insight** aos temas candidatos.
7. **Declarar limites.** Tamanho da amostra, perfil, o que não foi observado, vieses de condução.

## Teste do insight

Um insight vale a pena quando:

1. **surpreende** (não é o que o time já sabia);
2. **explica o porquê**, não só o que acontece;
3. **sugere uma ação** ou decisão;
4. **aparece em mais de um dado** (várias pessoas ou fontes);
5. **cabe em uma ou duas frases**.

Se falha em 2 ou mais, volta ao agrupamento. Insight que só confirma a crença do time merece suspeita: procure evidência contrária nas notas antes de registrar.

Heurística de sinal (autor, Inferido): um padrão em 6 de 8 participantes é sinal forte; um padrão em 1 de 8 é provável ruído, a menos que o impacto seja grave (por exemplo, perda de dinheiro ou dado), caso em que vale investigar. Nada disso dá significância estatística.

## Sinais de alerta

| Sinal | Por que é problema | O que fazer |
| --- | --- | --- |
| Pesquisa sem decisão associada | resultado não muda nada | definir a decisão antes de recrutar |
| Pergunta direcionada | produz o que o time quer ouvir | reescrever e treinar o moderador |
| Recrutar amigos ou colegas | viés de simpatia e de conhecimento | recrutar do perfil real |
| Pular a síntese | falas soltas viram "insights" | agrupar, contar e testar o insight |
| Insight que só confirma a crença | viés de confirmação | buscar evidência contrária |
| Apresentar n pequeno como prevalência | induz decisão errada | declarar limites; indicar quando precisa de dado quantitativo |
| Misturar observação e interpretação | recomendação sem base | separar em colunas |
| Citação inventada ou "limpa" demais | fabricação | só citação literal das notas |

## Formato da síntese

```text
Estudo: <pergunta> · Decisão apoiada: <...> · Amostra: n=<...> (perfil) · Fontes: <notas fornecidas>
Temas (ordenados por impacto e contagem)
  T1 <nome descritivo> | aparece em 4 de 5 | observações (com origem) | citações literais | interpretação | recomendação
Insights que passam no teste: <lista, 1 a 2 frases cada>
Decisões sugeridas · O que o estudo não responde · Vieses e limites · Próximo passo
```

Citações aparecem entre aspas, com a origem (P3), exatamente como estão nas notas.

## Crítica de design em equipe (30 min)

Para quando o artefato é uma sessão de crítica com a equipe, não pesquisa com usuários (V-18).

| Papel | Função |
| --- | --- |
| Apresentador | expõe o contexto, os objetivos e o que quer de retorno |
| Críticos | comentam em relação às metas do usuário e do produto |
| Facilitador (rotativo) | controla o tempo e a distribuição da fala |
| Anotador | registra comentários e itens de ação |

Roteiro: (1) escopo e objetivos (3 min); (2) apresentação (5 min); (3) discussão estruturada (15 min), por rodadas ou com cota de comentários positivos e negativos, reformulando comentários impositivos como perguntas ligadas às metas ("E se…?", "O que acontece quando…?"); (4) fechamento com notas e itens de ação (5 min); (5) acompanhamento por escrito.

Erros comuns: não ter personas ou objetivos definidos; sessão longa; levar para o lado pessoal; tentar resolver na hora; falar só dos pontos negativos. Comece pequeno, por exemplo uma sessão semanal de 30 minutos. O artigo é de 2016, atemporal para sessões síncronas e não trata de crítica assíncrona.
