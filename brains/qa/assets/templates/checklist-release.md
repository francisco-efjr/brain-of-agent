# Checklist de go/no-go — <!-- release ou versão -->

<!--
COMO USAR ESTE TEMPLATE
- Preencha antes da reunião de go/no-go e leve o parecer (fim do arquivo) pronto.
- Status: OK, PENDENTE, FALHOU ou N/A. N/A exige motivo na coluna Evidência.
- Evidência: link ou ID verificável (execução do pipeline, relatório, print,
  ticket, painel). "Testado" sem evidência conta como PENDENTE.
- Risco residual: o que pode acontecer em produção se o item não estiver OK,
  em linguagem de negócio ("clientes do Norte não conseguem fechar pedido"),
  não em jargão ("2 bugs P2").
- Itens com (*) são bloqueantes: PENDENTE ou FALHOU = NO-GO, salvo aceite
  formal de quem decide, registrado no parecer.
- Remova o que não se aplica ao tipo de mudança e acrescente itens do seu
  domínio (pagamentos, saúde, fiscal…). Critérios e exemplos de parecer:
  references/estrategia.md.
-->

| Campo | Valor |
| --- | --- |
| Release / versão | |
| Data e janela de deploy | <!-- evite pico de uso e conflito com outras mudanças --> |
| Escopo | <!-- links para histórias, notas de versão --> |
| Tipo de liberação | <!-- completa / gradual (canary) / atrás de flag --> |
| Responsável pelo checklist | |
| Decisores | <!-- quem pode dizer GO e aceitar risco residual --> |

## 1. Funcional

| # | Item | Status | Evidência | Risco residual |
| --- | --- | --- | --- | --- |
| F1 (*) | Critérios de aceite das histórias da release verificados | | | |
| F2 (*) | Nenhum defeito crítico aberto no escopo | | | |
| F3 | Defeitos altos abertos têm contorno documentado e aceite de quem decide | | | |
| F4 | Fluxos críticos verificados nas plataformas-alvo (navegadores, versões de app, larguras de tela) | | | |
| F5 | Feature flags testadas ligadas **e** desligadas | | | |

<!-- Exemplo de linha preenchida:
| F3 | Defeitos altos abertos têm contorno… | OK | LOJA-240 (contorno: suporte reemite QR); aceite do PO em 12/10 | cliente com QR expirado precisa pedir novo ao suporte (estimado < 1% dos pedidos) |
-->

## 2. Regressão

| # | Item | Status | Evidência | Risco residual |
| --- | --- | --- | --- | --- |
| R1 (*) | Smoke verde em pré-produção com configuração equivalente à de produção (flags, integrações, volume de dados) | | | |
| R2 (*) | Regressão crítica verde, sem falha inexplicada | | | |
| R3 | Falhas intermitentes desta execução investigadas, não só reexecutadas | | | |
| R4 | Regressão por impacto das áreas tocadas, incluindo dependências por dado, evento e configuração | | | |

## 3. Não funcional

| # | Item | Status | Evidência | Risco residual |
| --- | --- | --- | --- | --- |
| N1 | Desempenho: p95 de telas e endpoints críticos dentro da meta com a carga esperada | | | |
| N2 | Capacidade verificada para o pico previsto (campanha, data sazonal) | | | |
| N3 | Acessibilidade dos fluxos novos: teclado, foco, leitor de tela, varredura automática sem violação grave | | | |
| N4 | Compatibilidade: versões mínimas de app e navegador; API retrocompatível com clientes antigos | | | |

## 4. Segurança

| # | Item | Status | Evidência | Risco residual |
| --- | --- | --- | --- | --- |
| S1 (*) | Autorização testada: cada perfil acessa só os próprios recursos, inclusive trocando IDs direto na API | | | |
| S2 | Varredura de dependências sem vulnerabilidade crítica ou alta sem tratamento | | | |
| S3 | Segredos fora do código e dos logs; dados pessoais mascarados em logs | | | |
| S4 | Entradas novas validadas no servidor, não só na tela | | | |
| S5 | LGPD: dado pessoal novo tem finalidade, base legal e prazo de retenção definidos | | | |

## 5. Dados e migração

| # | Item | Status | Evidência | Risco residual |
| --- | --- | --- | --- | --- |
| D1 (*) | Migração ensaiada em cópia anonimizada com volume realista; duração medida | | | |
| D2 | Esquema compatível com a versão anterior do código (permite rollback sem perder dado) | | | |
| D3 | Reconciliação antes e depois definida: contagens, totais, amostra de casos especiais | | | |
| D4 | Backup recente e restauração testada | | | |
| D5 | Nenhum dado de teste vai para produção; nenhum dado de produção sem anonimização em teste | | | |

## 6. Observabilidade

| # | Item | Status | Evidência | Risco residual |
| --- | --- | --- | --- | --- |
| O1 (*) | Painel com métricas técnicas (erros, latência) e de negócio (ex.: pedidos pagos por minuto) do comportamento novo | | | |
| O2 | Alertas com limiar e dono definidos | | | |
| O3 | Logs estruturados com ID de correlação nos fluxos novos | | | |
| O4 | Monitoramento sintético do fluxo crítico ativo, com contas de teste marcadas | | | |
| O5 | Linha de base registrada para comparar depois da liberação | | | |

## 7. Rollback e contingência

| # | Item | Status | Evidência | Risco residual |
| --- | --- | --- | --- | --- |
| B1 (*) | Rollback (ou roll-forward) documentado e ensaiado; tempo medido | | | |
| B2 | Kill switch ou flag desliga a funcionalidade sem novo deploy | | | |
| B3 | Critério objetivo de rollback definido (ex.: erro > 1% por 10 min) e quem decide | | | |
| B4 | Efeitos irreversíveis mapeados (e-mails, pagamentos, notas fiscais) com plano de correção | | | |

## 8. Comunicação e operação

| # | Item | Status | Evidência | Risco residual |
| --- | --- | --- | --- | --- |
| C1 | Suporte com roteiro para dúvidas e problemas conhecidos | | | |
| C2 | Notas de versão e comunicação a clientes, se o comportamento muda | | | |
| C3 | Plantão definido para a janela e as horas seguintes | | | |
| C4 | Áreas e parceiros dependentes avisados (financeiro, operações, outros times) | | | |
| C5 | Janela sem conflito com outras mudanças ou congelamentos | | | |

## Parecer

<!--
Comece pela recomendação. Separe o que foi verificado (com evidência) do que
não foi. Cada risco residual na forma "se… então…", com probabilidade, como
será detectado, contorno e quem aceitou. GO com condições precisa de condições
verificáveis e de um dono para cada uma.
-->

**Recomendação:** <!-- GO / GO com condições / NO-GO -->

**Resumo:** <!-- 2 ou 3 linhas para quem não vai ler o checklist -->

**Verificado:** <!-- principais evidências: suítes, ambientes, plataformas -->

**Não verificado:** <!-- o que ficou de fora e por quê -->

**Riscos residuais aceitos:**

| Risco (se… então…) | Probabilidade | Como detectamos | Contorno | Aceito por | Data |
| --- | --- | --- | --- | --- | --- |
| _Ex._ se o aviso do PSP atrasar mais de 10 min, o cliente vê o pedido como "aguardando" apesar de ter pago | baixa (2 casos em 400 pagamentos no sandbox) | alerta "pago e não liberado há 5 min" | consulta automática ao PSP a cada 2 min libera o pedido | PO | 12/10 |

**Condições para GO:** <!-- condição verificável + dono; ex.: "alerta O2 ativo antes do deploy — líder técnico" -->

**Plano pós-release:** <!-- o que monitorar, por quanto tempo, checkpoints e critério de rollback; ex.: "painel O1 por 2 h após cada etapa da flag; checkpoint às 14h e 18h" -->

**Decisão:**

| Decisor | Papel | Decisão | Data e hora |
| --- | --- | --- | --- |
| | | | |
