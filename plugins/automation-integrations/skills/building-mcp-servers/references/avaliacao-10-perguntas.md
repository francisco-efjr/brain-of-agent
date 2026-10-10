# Avaliação de 10 perguntas para servidor MCP

Fonte: fase 4 do fluxo `mcp-builder` (V-12, `anthropics/skills`; licença não declarada, então a redação abaixo é própria) e orientação de avaliação de tools para agentes (V-09). Verificado em 2026-10-10 contra `VALIDATED.md`.

Para que serve: medir se um agente, usando só as tools do servidor, responde perguntas reais de várias chamadas. Pergunta fraca mede o quê o servidor devolve; pergunta boa mede se o conjunto de tools permite chegar à resposta com poucas chamadas e poucos erros.

Sumário: 1. Regras · 2. Prompt de geração · 3. Esqueleto XML · 4. Como pontuar · 5. Exemplo.

## 1. Regras das perguntas

1. Somente leitura: nenhuma pergunta exige criar, alterar ou apagar. Dados reais ficam protegidos.
2. Independentes: nenhuma depende da resposta de outra.
3. Várias chamadas: exigem combinar ao menos duas tools (buscar e depois detalhar, ou filtrar e depois contar).
4. Realistas: algo que um usuário do sistema perguntaria.
5. Resposta única e verificável por comparação de texto: número, nome próprio, ID, data. Evite listas longas e respostas abertas.
6. Estável no tempo: nada de "hoje", "esta semana", "o último". Se a resposta depende de dado que muda, descarte.
7. Confirmada: antes de entrar no arquivo, a resposta foi obtida por uma consulta direta (fora do agente avaliado) e conferida.

## 2. Prompt de geração (use em contexto limpo, com as tools do servidor conectadas pelo usuário)

```text
Você vai criar uma avaliação para o servidor MCP [NOME DO SERVIDOR], cujo domínio é [DOMÍNIO].
Contexto: a avaliação mede se um agente consegue responder perguntas reais usando apenas as tools do servidor;
o resultado orienta a revisão dos nomes, descrições e retornos das tools.

Tarefa:
1. Liste as tools e leia cada descrição. Execute apenas leituras (tools com readOnlyHint verdadeiro).
2. Explore os dados para entender o que existe.
3. Escreva 10 perguntas independentes, realistas, que exijam várias chamadas e tenham resposta única,
   verificável por comparação de texto e estável no tempo.
4. Para cada pergunta, chegue à resposta por uma consulta direta e anote os passos. Só inclua a pergunta
   se a resposta foi confirmada. Se depender de dado que muda, descarte e escreva outra.

Formato de saída: XML, exatamente nesta estrutura, sem texto fora dele.
<evaluation>
  <qa_pair><question>...</question><answer>...</answer></qa_pair>
  ... (10 pares)
</evaluation>

Se uma tool exigir escrita para responder, não use essa pergunta. Se não conseguir 10 perguntas
confirmáveis, entregue as que conseguiu e liste o que bloqueou o restante.
```

Por que funciona: dá o contexto e o uso do resultado (P-01), delimita o formato (P-06), proíbe escrita com a alternativa (descartar) e exige confirmação antes de afirmar (P-21).

## 3. Esqueleto XML

```xml
<evaluation>
  <qa_pair>
    <question>Qual é o título da issue mais antiga ainda aberta atribuída a Ana Souza?</question>
    <answer>Corrigir timeout no login SSO</answer>
  </qa_pair>
  <!-- ... mais 9 pares ... -->
</evaluation>
```

## 4. Como pontuar (processo, não promessa de resultado)

1. Rode cada pergunta com um agente que só tem as tools do servidor, em contexto novo.
2. Compare a resposta por texto normalizado (minúsculas, sem pontuação final). Registre: acertou, nº de chamadas, nº de erros de tool, tokens.
3. Leia as transcrições, não só o placar: erro recorrente de escolha de tool indica descrição ruim (T-08); respostas gigantes indicam retorno sem `concise` ou sem paginação.
4. Separe 3 a 4 perguntas como conjunto de teste e só ajuste descrições olhando as outras (evita ajustar a prova).
5. Não afirme "aprovado" sem a tabela de resultados colada. Sem execução, a avaliação fica `designed_not_executed` e o rótulo é Não verificado.

Tabela de registro:

| # | Pergunta (resumo) | Esperado | Obtido | Chamadas | Erros de tool | Observação |
| --- | --- | --- | --- | --- | --- | --- |

## 5. Armadilhas

- Perguntas que o agente responde com uma única tool de lista mostram que a tool é grande demais ou que a pergunta é simples demais.
- Resposta correta por acaso (valor padrão): varie perguntas para que o palpite não acerte.
- Dados de produção com informação pessoal: use ambiente de teste ou perguntas sobre metadados.
