# Juiz binário, vieses e estatística de avaliação

Apoio da skill `eval-design`. Leia ao escrever uma rubrica de juiz LLM, validar um juiz contra rótulos humanos, interpretar pass@k e pass^k ou conduzir a análise de erros antes de criar graders.

Rótulos: números de divisão e de tamanho de amostra são de V-12 (Husain e Shankar, página lida em 2026-10-10, publicada em 18/09/2026 e atualizada em 21/09/2026; o próprio texto se declara "opiniões fortes, não verdades universais"; Verificado, classe B). Vieses de juízes: V-13 (Eugene Yan, agosto de 2024, estudos de 2023 com modelos antigos: use como direção, não como medida atual). Definições e exemplo numérico de pass@k vs pass^k: V-03 (Verificado). As contas de TPR/TNR e a correção de taxa observada são estatística elementar, calculadas ao preparar este arquivo (Verificado por cálculo); a correção é Inferido quanto à adequação ao seu caso.

## Sumário

- [Rubrica binária](#rubrica-binária)
- [Checklist de vieses](#checklist-de-vieses)
- [Validar o juiz: TPR e TNR com conta](#validar-o-juiz-tpr-e-tnr-com-conta)
- [Divisão dos dados e tamanhos de amostra](#divisão-dos-dados-e-tamanhos-de-amostra)
- [Análise de erros antes de criar juiz](#análise-de-erros-antes-de-criar-juiz)
- [pass@k e pass^k](#passk-e-passk)
- [Quando a nota engana](#quando-a-nota-engana)

## Rubrica binária

Modelo (R8, redação própria baseada em V-04, V-12, V-13): um modo de falha por juiz, resposta apenas PASS ou FAIL, condições concretas e observáveis.

```text
Critério: <um modo de falha, descrito em uma frase>.
Responda apenas PASS ou FAIL, depois de escrever a justificativa em até 3 frases.
PASS quando <condição concreta e observável>.
FAIL quando <condição concreta e observável>.
Contexto fornecido: <só o trecho necessário>.
```

Exemplo preenchido (resumo de ticket):

```text
Critério: o resumo não inclui informação ausente do ticket.
PASS quando todo fato do resumo (valores, datas, nomes, causas) aparece no ticket original.
FAIL quando o resumo cita ao menos um fato, número ou causa que não está no ticket.
Contexto fornecido: ticket original e resumo gerado.
```

Por que binário: Likert de 1 a 5 esconde onde está a falha e produz médias sem decisão; subchecagens binárias dão progresso mensurável (V-12). A justificativa antes do veredito melhora a leitura do erro do juiz, não prova que o raciocínio é fiel (o raciocínio exibido nem sempre reflete o que determinou a resposta).

## Checklist de vieses

(V-13, direção e não medida; confirme no seu modelo)

- [ ] Código antes de juiz LLM: regex, existência de arquivo, ferramenta usada, teste.
- [ ] Um juiz por modo de falha.
- [ ] Modelo do juiz de família diferente do gerador (auto-preferência).
- [ ] Em comparação par a par, trocar a ordem e exigir resultado estável (viés de posição).
- [ ] Desconfiar de respostas mais longas ganhando por tamanho (viés de verbosidade).
- [ ] Testar paráfrases da rubrica e conferir se o veredito muda.
- [ ] Pairwise para tarefas subjetivas; binário para critérios objetivos.
- [ ] Painel de juízes pequenos e diversos como alternativa a um juiz grande (V-13); medir concordância (kappa de Cohen).
- [ ] Validar contra rótulos humanos (seção abaixo).
- [ ] Desconfiar de 100% de aprovação (V-12).

## Validar o juiz: TPR e TNR com conta

Defina com rótulos humanos como verdade: TPR = fração dos exemplos que o humano marcou PASS e o juiz também; TNR = fração dos que o humano marcou FAIL e o juiz também.

Exemplo (conjunto de dev com 40 exemplos rotulados por especialista: 20 PASS e 20 FAIL):

| | Juiz PASS | Juiz FAIL | Total |
| --- | --- | --- | --- |
| Humano PASS | 18 | 2 | 20 |
| Humano FAIL | 5 | 15 | 20 |

TPR = 18 / 20 = 90%. TNR = 15 / 20 = 75%. Leitura: o juiz erra mais para o lado leniente (aprova 5 de 20 falhas reais). Se a taxa de aprovação observada em produção é 70%, a estimativa corrigida da taxa verdadeira é (observada + TNR - 1) / (TPR + TNR - 1) = (0,70 + 0,75 - 1) / (0,90 + 0,75 - 1) = 0,45 / 0,65 = 69%. A correção só é confiável com amostra suficiente e quando TPR + TNR está bem acima de 1; se TPR + TNR for próximo de 1, o juiz é quase um sorteio e deve ser reescrito.

Ações quando o desempenho é insuficiente: leia os 7 erros (2 + 5), identifique o padrão (critério vago? contexto faltando? exemplo ambíguo?), reescreva a rubrica com PASS e FAIL mais concretos, rode de novo no **conjunto de dev**; só ao final meça no conjunto de teste, uma vez.

## Divisão dos dados e tamanhos de amostra

Números de V-12 (convenção dos autores, não lei):

| Conjunto | Fração dos rotulados | Uso |
| --- | --- | --- |
| Treino | 10 a 20% | exemplos curtos dentro do prompt do juiz |
| Dev | 40 a 45% | iterar a rubrica |
| Teste | 40 a 45% | medir TPR/TNR final, uma vez |

Tamanhos citados: 30 a 50 exemplos de PASS e de FAIL em dev e em teste; pelo menos 50 PASS e 50 FAIL ao depurar o juiz; 100 a 200 exemplos rotulados por modo de falha. Para um plugin pequeno esses números são inatingíveis no início: comece com o que tiver, declare a incerteza ("n = 12, TPR 83% com intervalo largo") e cresça com falhas reais.

## Análise de erros antes de criar juiz

Antes de qualquer grader `llm`, leia traces reais (V-12; V-03: ler transcrições separa erro do agente de erro do grader).

1. Amostre os traces (pelo menos 30 anotados; cerca de 100 para cobrir; pare quando nada novo aparecer: números de V-12).
2. Anote cada falha em linguagem livre, uma frase.
3. Agrupe em categorias de modo de falha (por exemplo "inventa dado", "ignora restrição", "ferramenta errada").
4. Para cada categoria, decida o grader: código se for verificável; juiz binário se não for.
5. Repita em ciclos (V-12 sugere pelo menos 100 traces a cada 2 a 4 semanas em produto vivo).

V-12 afirma que a análise de erros consome a maior parte do tempo de desenvolvimento (60 a 80%): o trabalho de ler traces é o trabalho, não um preâmbulo.

## pass@k e pass^k

(V-03.) Seja p a taxa de sucesso por tentativa independente.

- pass@k = 1 - (1 - p)^k: probabilidade de **pelo menos um** sucesso em k tentativas. Mede "consegue alguma vez".
- pass^k = p^k: probabilidade de **todos** os k sucessos. Mede consistência.

| p por tentativa | pass^1 | pass^3 | pass^5 | pass@3 |
| --- | --- | --- | --- | --- |
| 50% | 50% | 12,5% | 3,1% | 87,5% |
| 75% | 75% | 42,2% | 23,7% | 98,4% |
| 90% | 90% | 72,9% | 59,0% | 99,9% |

O exemplo do texto de V-03 (75% por tentativa dá cerca de 42% em três seguidas) confere. Use pass^k para o que o usuário espera que funcione sempre (revisão de segurança, gate de verificação); pass@k para tarefas em que várias tentativas são aceitáveis. Eval de regressão perto de 100% é esperado em comportamentos estáveis (V-03); eval de capacidade deve começar abaixo disso, ou não mede progresso.

## Quando a nota engana

| Sintoma | Suspeita | Verificação |
| --- | --- | --- |
| 100% de aprovação | eval fácil demais; juiz leniente | adicionar casos de falhas reais; medir TNR |
| Passa, mas Δ com/sem plugin negativo | juiz ou grader errado (V-02) | ler transcrições das duas arms |
| Nota muda entre execuções sem mudança | variância alta com n pequeno | mais execuções, mediana, pass^k |
| Skill dispara em pedido não relacionado | `description` ampla | caso negativo com `min: 0`/`max: 0` |
| Skill nunca dispara | gatilho fraco ou prompt irreal | revisar a `description`; checar o prompt do caso |
| Juiz concorda com tudo que o gerador escreve | auto-preferência | juiz de outra família; validar com rótulos humanos |
