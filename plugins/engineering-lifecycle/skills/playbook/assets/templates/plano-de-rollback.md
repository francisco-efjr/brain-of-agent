# Modelo: plano de rollback

Use antes de qualquer deploy ou habilitação de flag (skill [shipping-and-launch](../../../shipping-and-launch/SKILL.md), seção Rollback Strategy; `/engineering-lifecycle:ship` exige o plano antes de qualquer GO). O plano é um **documento**: push, deploy, publicação e execução de reversão só com confirmação do usuário. Gatilhos, limiares e tempos abaixo são exemplos do autor (**Suposição** até medir no projeto); troque por números do serviço.

Um roteiro de canário por projeto (conflito C-7). Sem roteiro definido, a Suposição é 5%, 25%, 50%, 100% do upstream, com os limiares da tabela de decisão.

```markdown
# Plano de rollback: [FEATURE / RELEASE] · [AAAA-MM-DD]

Responsável pela decisão: [pessoa ou papel] · Quem executa: [pessoa ou papel] · Canal de aviso: [canal]

## 1. Gatilhos (reverter se qualquer um ocorrer)
- Taxa de erro > [2x] a linha de base ([valor da base], medida em [fonte])
- p95 de latência > [limite ou +50%] ([valor da base])
- Reclamações específicas: [tipo, quantidade, canal]
- Integridade de dados comprometida: [sinal]
- Falha de segurança descoberta
- Queima do orçamento de erro acima da base durante o canário: segurar; confirmada: reverter

## 2. Passos de reversão
1. Desligar a flag [nome da flag], se houver. Tempo: [< 1 min]
   **ou** reimplantar a versão anterior [identificador da versão]. Tempo: [< 5 min]
   (reverter por commit pressupõe deploy a partir do commit; ajuste ao seu pipeline)
2. Verificar: health check [URL ou comando] = [200]; taxa de erro volta à base; fluxo crítico [qual] funciona
3. Avisar: [time, canal, mensagem de uma linha]

## 3. Banco de dados
- Migração [ID] tem `down`: [comando ou runbook], **testado em [ambiente] em [data]**: [sim | não]
- Dados criados pela feature nova: [preservar | limpar], porque [motivo]; quem decide: [pessoa]
- Mudança de schema segue expand/contract: [fase atual]; `drop` em deploy separado depois de zerar o uso

## 4. Tempos esperados
| Caminho | Tempo |
| --- | --- |
| Flag | [< 1 min] |
| Redeploy da versão anterior | [< 5 min] |
| Banco de dados | [< 15 min] |

## 5. Ensaio
- Reversão ensaiada (ou "dry run" do mecanismo): [sim | não], em [ambiente], [data]. Se não: Não verificado, e o motivo.

## 6. Primeira hora após o deploy
- [ ] Health 200 · [ ] sem erro novo · [ ] latência normal · [ ] fluxo crítico ok · [ ] logs fluindo · [ ] reversão verificada como pronta
- Quem vigia: [pessoa], até [hora]

## 7. Flag e limpeza
- Dono: [pessoa] · Expira em: [data] · Remover flag e caminho morto até [2 semanas depois de 100%]
- Flags aninhadas: nenhuma · Testado com flag ligada e desligada no CI: [sim | não]
```

## Tabela de decisão do rollout (exemplos do autor; Suposição)

Aplique em cada estágio (equipe, 5%, 25%, 50%, 100%; janelas de 24 h, 24 a 48 h, 24 a 48 h e 1 semana no 100%).

| Métrica | Avançar | Segurar e investigar | Reverter |
| --- | --- | --- | --- |
| Taxa de erro | Até 10% acima da base | De 10% a 100% acima | Mais que 2x a base |
| Latência p95 | Até 20% acima | De 20% a 50% acima | Mais de 50% acima |
| Erros de JS no cliente | Nenhum tipo novo | Tipo novo em menos de 0,1% das sessões | Tipo novo em mais de 0,1% |
| Métricas de negócio | Neutra ou melhor | Queda menor que 5% (pode ser ruído) | Queda maior que 5% |

## Portão do orçamento de erro (se o serviço tem SLO)

Restante > 20%: lança normalmente. Entre 0 e 20%: só rollout lento, sem mudança de alto risco. Esgotado: congela features até a confiabilidade voltar.

## Checagem

- [ ] Gatilhos quantitativos com valor de base e fonte da medição
- [ ] Passos testados ou marcados Não verificado
- [ ] Destino dos dados novos decidido
- [ ] Tempos estimados; reversão ensaiada ou justificada
- [ ] Ninguém executa nada antes da confirmação do usuário
