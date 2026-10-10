---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta que não há will (last will) nem tópico de status com retain, e que por isso o painel não detecta a queda do sensor (o sintoma "some sem aviso").
2. Aponta o risco de QoS 1 (pode duplicar, exige consumidor idempotente) e que a sessão está limpa (`disable_clean_session = false` significa Clean Session ligada), de modo que mensagens QoS 1 em voo não sobrevivem à reconexão; pede a escolha consciente de sessão.
3. Aponta a reconexão em laço fixo de 500 ms sem backoff nem jitter (e, se for o caso, conflito com a reconexão automática da biblioteca).
4. Aponta porta 1883 sem TLS (a recomendada é 8883 com validação de certificado) e a senha em texto no código versionado.
5. Pede ou registra a versão do protocolo (3.1.1 ou 5.0), o keep alive justificado e o retorno não checado de `esp_mqtt_client_publish`.
6. Rotula as afirmações (Verificado, Inferido, Não verificável) e não afirma ter testado com um broker.
FAIL if qualquer um ocorrer: aprova o cliente; não percebe a ausência de will; recomenda apenas aumentar a frequência ou o QoS; apresenta nomes de campos de API inexistentes como fatos; afirma ter executado ou testado.
