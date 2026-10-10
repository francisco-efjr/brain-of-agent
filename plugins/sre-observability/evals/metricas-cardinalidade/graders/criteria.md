---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final e no transcript:
1. Aponta user_id e email como rótulos de alta cardinalidade e destaca que e-mail e identificador de usuário são dado pessoal, a ser removido dos rótulos (e não ser logado como alternativa).
2. Aponta path como problema quando contém IDs e recomenda usar o template da rota (por exemplo /pedidos/:id) ou limitar os valores.
3. Mostra a estimativa de séries com a conta (produto dos valores distintos dos rótulos, por exemplo 200 mil usuários x e-mails x 3.000 paths como limite superior, e multiplicação por buckets no caso de histograma) e cita que o guia do Prometheus é manter a cardinalidade por métrica baixa (abaixo de 10, reavaliar acima de 100 séries) como guia, não limite técnico.
4. Critica os nomes: prefixo de aplicação de uma palavra, unidade base no plural (seconds) e _total depois da unidade para contadores (por exemplo app_http_requests_total).
5. Diz que a latência deve ser um histograma em segundos (por exemplo app_http_request_duration_seconds) e não um medidor em milissegundos que guarda o último valor; e que rate() de medidor é inválido (rate/increase valem para contadores).
6. Propõe a correção mínima em trecho de código ou lista objetiva, e rotula achados como Verificado (visível no código) ou Inferido (efeito deduzido), sem afirmar que executou ou mediu algo.
FAIL if qualquer um ocorrer: aprova user_id ou email como rótulos; sugere registrar o e-mail em logs como alternativa; ignora rate() de medidor; deixa de mostrar a estimativa de séries; afirma ter executado o código ou medido a cardinalidade.
