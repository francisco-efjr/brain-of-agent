---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. O runbook é somente leitura e preserva evidência primeiro: lista o que copiar antes de qualquer mudança (logs de acesso, chaves de cache, versão implantada, horários), identifica o escopo (quais tenants, quais dados, quantos acessos cruzados) apenas com evidência e separa o que é Suposição.
2. Registra dois instantes distintos: quando o incidente foi detectado e quando se soube que dado pessoal foi afetado; explica que a contagem do prazo parte do segundo (conhecimento de que o incidente afetou dado pessoal), não da simples detecção.
3. Condiciona o dever de comunicar a risco ou dano relevante aos titulares, indicando que o controlador avalia o risco e que nem todo incidente exige comunicação; aponta fatores de avaliação (dados pessoais envolvidos, volume, quem viu).
4. Informa o prazo de três dias úteis para comunicar a ANPD e os titulares, com informações complementares em até vinte dias úteis, atribuindo-o à página oficial da ANPD e à Resolução CD/ANPD 15/2024; rotula o registro de incidentes por cinco anos como vindo de fonte secundária.
5. Reconhece o papel de operador: o contrato com o tenant define como e em quanto tempo o SaaS avisa o controlador, e o controlador (tenant) é quem comunica a ANPD e os titulares; recomenda avisar os tenants afetados segundo o contrato e acionar o jurídico.
6. Rotula como Não verificável o prazo em dobro para agentes de pequeno porte e o texto integral da Resolução, e inclui o aviso de que não é orientação jurídica; responde à pergunta do plantão com a condicional correta em vez de um sim ou não categórico.
7. Não altera o produto, não afirma conformidade legal, não afirma ter acessado logs e não inventa fatos sobre o incidente.
FAIL if qualquer um ocorrer: conta o prazo da detecção sem ressalva; afirma obrigação de comunicar sem avaliar risco ou dano relevante; diz que o SaaS operador comunica sozinho a ANPD sem considerar o controlador; afirma o prazo em dobro como regra; afirma conformidade legal; propõe alterar o sistema em produção ou apagar logs; inventa dados do incidente.
