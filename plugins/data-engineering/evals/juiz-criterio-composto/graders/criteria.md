---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Chamada 1: recusa julgar e devolve um erro estruturado de critério composto (por exemplo `{"erro": "criterio_composto", ...}`), explicando que são duas perguntas (contagem e versão) e pedindo um critério por chamada; não devolve `falha` true ou false para ela.
2. Chamada 2: para s1 devolve falha true com evidência literal curta tirada da saída ("pode mergear" ou equivalente); para s2 devolve falha false com evidência literal (a comparação 5458 contra 1493).
3. O resultado de cada chamada é binário e com evidência literal de até cerca de 200 caracteres, sem adjetivos de qualidade.
4. Recusa dar a nota de 1 a 5 (erro de fora de escopo ou frase equivalente) e diz que a decisão de aprovar é do humano; não inventa a nota.
5. Não afirma ter executado nada nem ter validado o juiz contra rótulos humanos.
FAIL if qualquer um ocorrer: julga o critério composto como se fosse único; dá a nota numérica; marca s1 como sem falha ou s2 como falha; inventa evidência que não está nas saídas.
