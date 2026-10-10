---
name: prompts
description: Biblioteca de mensagens prontas para acionar o orquestrador Brain of Agent em outro chat ou terminal (melhoria pronta, revisão completa, feature, bug, telas novas, auditoria de segurança, release). Use quando o usuário pedir "mensagem pronta", "prompt para orquestrar", "como peço para revisar meu projeto", "prompt para melhorar o sistema", "starter prompt".
---

# Prompts do orquestrador

Os prompts estão em [references/prompt-library.md](references/prompt-library.md). Escolha pelo tipo de demanda e preencha as variáveis `[EM_COLCHETES]`. Cada prompt já pede escopo, entrega e validação, para que o orquestrador não presuma permissões.

| Situação | Prompt |
| --- | --- |
| Primeira vez em outro chat, só com o link | O-01 |
| Revisão completa com relatórios por papel e commit local | O-02 |
| Feature nova de ponta a ponta | O-03 |
| Bug ou incidente | O-04 |
| Telas novas aplicando o design system | O-05 |
| Auditoria de segurança e LGPD | O-06 |
| Só planejar, sem executar | O-07 |
| Melhoria pronta feita pelos especialistas, com testes e COMO-TESTAR | O-08 |
