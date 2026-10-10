# Cartão do agente (A/B/C)

Fonte: Regra de Dois da Meta e gate de ações (V-42, V-13), redação própria. Preencha antes de liberar o agente e reexamine quando uma tool, fonte de dados ou permissão entrar. Rótulos: Verificado, Inferido, Suposição, Não verificável.

- **Nome e objetivo (uma frase):** [...]
- **Modelo-alvo, superfície (API / Agent SDK / CLI / Managed Agents) e data de conferência:** [...]
- **Quem usa e quem autoriza efeitos externos:** [...]

## Ferramentas e fontes

| Ferramenta ou fonte | Lê conteúdo que terceiros controlam? (A) | Acessa dados privados ou sistemas sensíveis? (B) | Muda estado ou comunica para fora? (C) | Confirmação humana? | Evidência |
| --- | --- | --- | --- | --- | --- |
| [ex.: caixa de e-mail de suporte] | sim | não | não | n/a | [arquivo:linha ou descrição] |
| [ex.: CRM] | não | sim | não | n/a | [...] |
| [ex.: envio de e-mail] | não | não | sim | sim, mostra o alcance | [...] |

## Configuração resultante

Marcas presentes na mesma sessão: [A / B / C]. Configuração: [AB / AC / BC / A+B+C].

| Se | Barreira aplicada | Quem verifica |
| --- | --- | --- |
| AB | Restringir C: confirmar antes de agir; saída só para destinos confiáveis | [...] |
| AC | Restringir B: sandbox restritivo, sem dados de sessão pré-carregados | [...] |
| BC | Restringir A: filtrar fontes por autoria; revisão humana | [...] |
| A+B+C | Remover uma capacidade, separar em dois agentes com fronteira, ou aprovação humana no ponto de saída descrevendo o alcance | [...] |

## Controles

- Política de conteúdo não confiável no prompt (camada, não barreira): [sim/não]
- Conteúdo externo em `tool_result` com origem declarada: [sim/não]
- Privilégio mínimo e sandbox: [...]
- Tetos: `max_turns` [..], orçamento [..], tempo [..]
- Triagem de saída de tool de fonte de alto risco: [modelo pequeno com saída estruturada / não]
- Teste adversarial (documentos e e-mails com injeção): [data, resultado ou "projetado, não executado"]

## Revisão

Próxima revisão quando: nova tool, nova fonte, mudança de permissão, mudança de modelo. Dependências desta decisão: [...]. Limites: um filtro ou frase de prompt não conta como barreira; defesa só vale se resistir a atacante que itera.
