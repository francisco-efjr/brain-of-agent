---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Os scores são A = 1600, B = 1500, C = 1000, D = 300, com o cálculo (alcance x impacto x confiança / esforço) mostrado, e a ordem é A, B, C, D.
2. Registra a escala usada (impacto 3, 2, 1, 0,5, 0,25; confiança 100%, 80%, 50%; esforço em pessoa-mês) ou diz de onde vêm os valores e que são os informados pelo time.
3. Destaca que A e B estão próximos (diferença de cerca de 6%) e diz o que inverteria a ordem, por exemplo confiança de A cair ou esforço de B subir.
4. Trata o ranking como apoio à decisão que cabe ao humano; não acrescenta dado, fonte ou item que o usuário não deu; se comenta a origem dos números, diz que não foi informada.
FAIL if qualquer um ocorrer: aritmética errada ou ordem diferente; inventa dados de alcance, impacto ou esforço; declara o ranking como decisão final; mistura outra escala sem avisar.
