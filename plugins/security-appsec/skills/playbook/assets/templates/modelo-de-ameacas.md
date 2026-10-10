# Modelo de ameaças

Modelo para a skill `threat-model` (quatro fases, V-17: modelar o sistema, identificar e ranquear ameaças, responder, validar). Fronteira ou fluxo que o usuário não descreveu é **Suposição** e vai para a lista de confirmação. Nada de afirmar fatos sobre a arquitetura não descrita.

## 1. Escopo e ativos (acréscimo da skill; a fonte OWASP não traz esta etapa: Inferido)

- Feature ou sistema: <nome e objetivo>
- Ativos (o que vale proteger): <dados de clientes, tokens, dinheiro, disponibilidade>
- Atores: <usuário legítimo, usuário autenticado malicioso, tenant vizinho, administrador, conteúdo de terceiros, serviço interno>
- Stack e ambiente: <...>

## 2. DFD textual

- Entidades externas: <E1 navegador, E2 provedor X>
- Processos: <P1 API, P2 worker>
- Armazenamentos: <D1 banco, D2 bucket>
- Fluxos: <F1 E1 → P1 (HTTPS), F2 P1 → D1, F3 P2 → D2>
- Fronteiras de confiança: <B1 internet / aplicação, B2 aplicação / banco, B3 aplicação / fornecedor>
- Suposições sobre fronteiras: <S1 ...> (rotuladas **Suposição**)

## 3. STRIDE por fluxo que cruza fronteira

Uma pergunta por categoria (V-17):

| Categoria | Pergunta |
| --- | --- |
| Spoofing | Quem pode se passar por quem? |
| Tampering | O que pode ser alterado em repouso ou em trânsito? |
| Repudiation | Que ação fica sem rastro? |
| Information disclosure | Que dado vaza? |
| Denial of service | O que pode ser tornado indisponível (inclusive custo)? |
| Elevation of privilege | Como alguém ganha privilégio? |

Dados pessoais: acrescente LINDDUN (privacidade). Componentes LLM: acrescente as perguntas LLM01, 02, 05, 06, 07, 10 (`owasp-e-asvs.md`).

## 4. Ameaças, resposta e teste

| ID | Ameaça | Fluxo | Categoria | Prob. | Impacto | Resposta | Controle | Teste de verificação |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-01 | <ameaça> | <F1> | <STRIDE> | <A/M/B> | <A/M/B> | <mitigar | eliminar | transferir | aceitar> | <controle> | <teste que prova> |

Resposta "transferir" exige risco residual documentado. Fluxo sem categoria avaliada: listar como **não coberto**.

## 5. Risco residual

| ID | Risco residual | Quem aceita | Revisão em |
| --- | --- | --- | --- |
| T-0X | <descrição> | <nome ou papel> | <data ou gatilho> |

## 6. Suposições a confirmar

1. <S1: pergunta objetiva ao usuário>
2. <...>

## 7. Validação

<com quem foi revisado (interessados); data; o que mudou depois da revisão>
