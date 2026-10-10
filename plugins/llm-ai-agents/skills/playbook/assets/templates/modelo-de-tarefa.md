# Modelo de tarefa com critério verificável

Fonte: V-20 (Claude Code best practices), redação própria. Use para pedir implementação, correção ou revisão a um agente. Pule o plano se o diff cabe em uma frase.

```text
Objetivo: [resultado, em uma frase]
Arquivos ou áreas envolvidos: [caminhos]
Fora de escopo: [o que não tocar]
Critério de aceite: [comando que retorna passa/falha e o resultado esperado]
Entrega: mostre a saída do comando e o que ficou sem verificar; não declare concluído sem essa evidência.
Se algo for ambíguo: assuma a leitura mais direta e declare a suposição; pergunte só se mudar a solução.
```

## Campos opcionais

- **Modelo-alvo e data:** [...]
- **Ações que exigem confirmação:** apagar, force push, publicar, enviar mensagem, gastar, tocar produção
- **Revisão:** subagente somente leitura em contexto novo, só lacunas de correção e de requisito
- **Escalada:** após 3 hipóteses ou correções falhas, pare e reporte

## Tarefa grande (entrevista e SPEC.md)

1. O agente entrevista uma pergunta por vez até ter requisitos testáveis.
2. Escreve `SPEC.md` autocontido: arquivos, interfaces, fora de escopo, verificação ponta a ponta.
3. A implementação começa em sessão nova só com a spec.
4. Revisão do diff por subagente em contexto novo.

## Exemplo preenchido

```text
Objetivo: a função parse_order() rejeita datas ISO sem fuso.
Arquivos ou áreas envolvidos: src/orders/parse.py, tests/orders/test_parse.py
Fora de escopo: formatação de outros módulos; dependências
Critério de aceite: pytest tests/orders/test_parse.py -q termina com 0 falhas e o novo teste test_rejects_naive_datetime falha antes da correção
Entrega: cole a última linha da saída do pytest antes e depois; liste o que não verificou
Se algo for ambíguo: assuma a leitura mais direta e declare
```
