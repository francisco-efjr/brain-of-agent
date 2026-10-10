# Relatório de deploy e checklist go/no-go de infraestrutura

<!--
Preencha antes (go/no-go) e depois (veredito) de uma mudança de infra autorizada. Não fabrique sucesso:
"comando retornou" e "HTTP 200" não são prova. Separe a evidência do DEPLOY da evidência da VERIFICAÇÃO.
Status: OK, PENDENTE, FALHOU ou N/A (com motivo). Itens com (*) são bloqueantes: PENDENTE ou FALHOU = NO-GO,
salvo aceite formal de quem decide, registrado no parecer. Risco residual em linguagem de negócio.
Base: checklist-release.md do brain-of-agent (MIT; seções de dados, observabilidade e rollback) e vereditos
inspirados em gstack land-and-deploy (MIT, Garry Tan; redação própria). Funcional, regressão e UX ficam em qa-testing.
-->

| Campo | Valor |
| --- | --- |
| Mudança / release | [IDENTIFICADOR] · PR: [LINK] |
| Alvo confirmado (comando de leitura) | [CONTA / CLUSTER / WORKSPACE] |
| Janela e dono | [DATA, FUSO] · [NOME] |
| Tipo | [completa / gradual (canary) / atrás de flag] |
| Decisores | [NOMES] |

## 1. Go/no-go

| # | Item | Status | Evidência | Risco residual |
| --- | --- | --- | --- | --- |
| D1 (*) | Migração ensaiada em cópia anonimizada com volume realista; duração medida | | | |
| D2 | Esquema compatível com a versão anterior do código (permite rollback sem perder dado) | | | |
| D3 | Reconciliação antes e depois definida: contagens, totais, amostras de casos especiais | | | |
| D4 | Backup recente e restauração testada | | | |
| D5 | Nenhum dado de teste em produção; nenhum dado de produção sem anonimização em teste | | | |
| O1 (*) | Painel com métricas técnicas (erros, latência) e de negócio do comportamento novo | | | |
| O2 | Alertas com limiar e dono definidos | | | |
| O3 | Logs estruturados com ID de correlação nos fluxos novos | | | |
| O4 | Monitoramento sintético do fluxo crítico ativo | | | |
| O5 | Linha de base registrada para comparar depois | | | |
| B1 (*) | Rollback (ou roll-forward) documentado e ensaiado; tempo medido | | | |
| B2 | Kill switch ou flag desliga a funcionalidade sem novo deploy | | | |
| B3 | Critério objetivo de rollback e quem decide (`plano-rollout-rollback.md`) | | | |
| B4 | Efeitos irreversíveis mapeados (e-mails, pagamentos, notas fiscais) com plano de correção | | | |
| I1 (*) | Plano de mudança aprovado com "sim" para o comando exato (`plano-mudanca-infra.md`) | | | |
| I2 | Credencial usada sem permissão além da necessária; segredos fora de logs e relatório | | | |

<!-- Itens D, O e B derivam das seções 5, 6 e 7 do checklist-release do brain-of-agent; I é específico de infra. -->

## 2. Evidência do deploy

| Comando exato executado | Autorização (trecho do "sim") | Saída essencial | Resultado |
| --- | --- | --- | --- |
| `[COMANDO]` | "[SIM DO USUÁRIO]" | [SAÍDA] | |

## 3. Evidência da verificação

| Verificação | Comando ou fonte | Resultado | O que prova |
| --- | --- | --- | --- |
| A revisão certa está no ar | [versão, SHA, header ou revisão do rollout] | | Identidade da versão |
| Saúde técnica | [rollout status, probes, taxa de erro] | | Alcance e estabilidade |
| Fluxo de negócio | [teste sintético ou consulta] | | Funcionamento ponta a ponta |

## 4. Veredito

Marque um:

- [ ] **Aplicado e verificado**: comando ok, prova da revisão e saúde ok.
- [ ] **Aplicado, não verificado**: comando ok; verificação ausente ou indisponível (motivo: [MOTIVO]).
- [ ] **Degradado**: a verificação falhou e o usuário aceitou continuar (quem e quando: [DADOS]).
- [ ] **Falhou ou pendente**: comando falhou ou estado desconhecido. Falha ao obter status é "desconhecido", não sucesso.
- [ ] **Revertido**: somente com rollback confirmado, por escolha explícita do usuário.
- [ ] **Rollback pendente**.

Regras: não inferir sucesso de "comando retornou" ou de HTTP 200; não corrigir sozinho em produção; reverter só após escolha explícita do usuário; nunca force-push nem burlar CI.

## 5. Parecer

**Recomendação:** [GO / GO com condições / NO-GO]
**Verificado:** [evidências principais]
**Não verificado:** [o que ficou de fora e por quê]
**Riscos residuais aceitos:** se [condição] então [consequência de negócio] · probabilidade: [Suposição] · detecção: [COMO] · contorno: [AÇÃO] · aceito por: [NOME, data]
**Condições para GO:** [condição verificável · dono]
**Plano pós-release:** [o que monitorar, por quanto tempo, checkpoints, critério de rollback]
