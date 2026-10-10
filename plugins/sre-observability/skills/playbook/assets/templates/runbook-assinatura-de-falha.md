# Runbook — [ASSINATURA DE FALHA] (ex.: `5xx.md`, `latency.md`, `oom.md`)

Template T-07. Um arquivo por assinatura de falha, versionado no repositório, alterado por PR e carregado só quando relevante (V-18). Não existe fonte oficial de estrutura de runbook: esta é uma composição do plugin (Inferido). Cada passo traz comando exato, saída esperada e o que concluir. **Diagnóstico é somente leitura; mitigação é opção que exige decisão humana.** Nenhum segredo neste arquivo. Comandos de exemplo devem ser confirmados na sua versão e ambiente; o que não foi confirmado fica marcado "a confirmar pelo time".

**Dono:** [time/papel] · **Alerta que aponta para cá:** [nome da regra] · **Última revisão (PR):** [link, data] · **Serviço/ambiente:** [..]

## 1. Assinatura e impacto

Sintoma observável: [ex.: taxa de 5xx > [x]% por [y] min em `payments-api`]. Impacto no usuário: [..]. Severidade sugerida: [P?, exemplo; a organização define].

## 2. Diagnóstico (somente leitura)

| Passo | Comando/consulta exata | Saída esperada | O que concluir |
| --- | --- | --- | --- |
| 1 | [consulta do painel "Erros por rota", janela últimos 15 min] | [rota(s) com taxa acima da linha de base] | [se uma rota domina, vá ao passo 2; se todas, passo 4] |
| 2 | [consulta comparando erros por versão] | [v nova acima da antiga] | [correlação com deploy: registre como hipótese H1, não como causa] |
| 3 | [consulta do span lento / log do erro mais frequente] | [mensagem de erro dominante] | [..] |
| 4 | [verificar dependência: saúde, latência, limite de taxa] | [..] | [..] |

Se um comando não puder ser executado por falta de acesso: registre "Não verificável: sem acesso a [..]" e siga para a pergunta ao IC.

## 3. Mitigações (opções; exigem decisão humana)

| Opção | Pré-condição | Aprovador (papel) | Como reverter | Risco |
| --- | --- | --- | --- | --- |
| Reverter para a versão anterior | [migração compatível com a versão anterior] | [IC] | [reaplicar a versão nova] | [efeitos já produzidos (e-mail, cobrança) não revertem] |
| Reduzir tráfego/ativar degradação | [flag com valor seguro e dono] | [IC] | [desligar a flag] | [funcionalidade reduzida] |
| Escalar capacidade | [dentro dos limites do autoscaler] | [IC] | [voltar ao mínimo] | [pode amplificar carga na dependência] |

## 4. Quando escalar e para quem

| Condição | Escale para | Prazo |
| --- | --- | --- |
| [sem melhora em [x] min] | [papel de segundo nível] | [..] |
| [dado de cliente em risco] | [security / jurídico, conforme a organização] | [imediato] |

## 5. Confirmar recuperação

Critério: o SLI [nome] voltou ao normal por [x] min (não use CPU como critério). Consulta: [..]. Ao resolver, avalie o gatilho de postmortem (ver T-06).

## 6. Histórico e manutenção

Alterações apenas por PR. Registre aqui o incidente que motivou cada mudança: [data, ID].

## Lint (antes de aprovar o PR)

- [ ] Nenhum comando sem saída esperada
- [ ] Nenhum segredo/token/credencial
- [ ] Nenhum passo que dependa da memória de uma pessoa
- [ ] Mitigações separadas do diagnóstico e marcadas "exige decisão humana"
- [ ] Nada de "reiniciar" sem diagnóstico prévio
