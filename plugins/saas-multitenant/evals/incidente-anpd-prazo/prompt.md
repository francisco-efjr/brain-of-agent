---
name: incidente-anpd-prazo
description: Mede se, num incidente em que um bug mostrou a lista de clientes de um tenant a outro e o SaaS é operador, o plugin entrega um runbook somente leitura que preserva evidência, separa o instante da detecção do de saber que dado pessoal foi afetado, condiciona o aviso a risco ou dano relevante, informa três dias úteis com ressalvas e não é orientação jurídica.
tags: [saas-multitenant, tenant-data-lifecycle, lgpd, anpd, incident]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega runbook somente leitura que preserva evidência, registra o instante da detecção e o de saber que dado pessoal foi afetado, avalia risco ou dano relevante, informa três dias úteis para a ANPD e titulares a partir do segundo instante e vinte dias úteis de complemento, diz que o contrato define o aviso do operador ao controlador, rotula como Não verificável o prazo em dobro de pequeno porte e o texto integral da resolução, e avisa que não é orientação jurídica."
model: sonnet
---
Descobrimos ontem à tarde que um bug no nosso SaaS fez a lista de clientes de um tenant (nome, e-mail e telefone dos contatos) aparecer para usuários de outro tenant, por cerca de 3 horas, por causa de um cache sem o tenant na chave. Já corrigimos a chave do cache. Nós somos operadores; os tenants são os controladores. A pessoa de plantão está nervosa e perguntou se temos de avisar a ANPD em três dias.

Escreve o runbook do incidente e me diz se temos de avisar a ANPD em três dias. Não tenho acesso a logs agora; o que sei é o que escrevi. Entregue o texto na resposta e não altere nada no sistema.
