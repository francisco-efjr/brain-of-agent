# Plano de rollout e reversão — [MUDANÇA] — [data]

Template T-15. Base: seção "Plano de rollout e reversão" de `entrega-e-operacao.md` do brain-of-agent (conteúdo próprio, MIT) + canário com controle concorrente (V-09). Escreva **antes** de publicar. O plano descreve; a execução depende de autorização concreta: preparar release, publicar artefato, implantar, habilitar e verificar produção são ações distintas, e nenhuma é autorizada por este documento.

**Mudança:** [commit/build/imagem/config/schema/flag] · **Artefato promovido:** [o que passou nos testes; versões; lockfile] · **Dono:** [papel] · **Decisor de continuar/reverter:** [nome/papel]

## 1. Estratégia

[Canário (percentual, duração) / blue-green / flag / big-bang] e por quê. Condição verificada: [duas versões convivem? métricas por versão confiáveis?].

## 2. Sinais de interrupção (definidos antes de iniciar)

| Sinal | Fonte | Limiar | Janela | Ação |
| --- | --- | --- | --- | --- |
| [taxa de erro do canário vs controle] | [consulta] | [> [x]% por 2 checagens] | [..] | [pausar e chamar o decisor] |
| [p95 de latência] | [..] | [..] | [..] | [..] |
| [inconsistência de dados] | [..] | [..] | [..] | [..] |
| [saturação] | [..] | [..] | [..] | [..] |

Baseline capturado antes: [data/hora UTC, fonte]. Comparação com **controle concorrente**, não antes/depois.

## 3. Compatibilidade com schema e dados

| Item | Compatível com a versão anterior? | Observação |
| --- | --- | --- |
| [migração expand: coluna nova nullable] | [sim] | [contract só depois da remoção da versão anterior] |

Versão anterior × migração: [registrada]. Reverter o binário **não** desfaz dados já convertidos.

## 4. Feature flag (se houver)

| Flag | Dono | Valor seguro | Plano de remoção (data) |
| --- | --- | --- | --- |
| [nome] | [papel] | [off] | [AAAA-MM-DD] |

## 5. Efeitos irreversíveis

[E-mail enviado, cobrança, webhook, conversão de dado: o que não reverte e qual é o plano de compensação.]

## 6. Decisão: reverter ou corrigir para frente

| Condição | Decisão preferida | Quem decide |
| --- | --- | --- |
| [reversão segura e rápida] | reverter | [..] |
| [reversão insegura (schema/efeitos)] | corrigir para frente, com decisão explícita registrada | [..] |

## 7. Verificação pós-entrega

Confirme **fluxo e dado**, não só health check: [consulta/teste do fluxo crítico], SLI [nome] dentro da meta por [x] min. Relatório: T-11. Runbook de rollback: [link].
