# Modelo de brief de arquitetura de agente

Preencha só as seções que a decisão exige (proporcionalidade). O brief é projeto: nada nele afirma que o sistema foi construído ou testado.

## Modelo

```markdown
# Brief de arquitetura: <sistema>
Data: <AAAA-MM-DD> · Modelo-alvo: <modelo> (conferido em <data>) · Superfície: <Agent SDK | CLI | SDK cliente | Managed Agents>

## 1. Decisão
- Escolha: <chamada única | workflow (padrão) | orquestrador-trabalhadores | agente>
- Alternativa mais simples descartada: <qual> porque <evidência ou Suposição>
- O que muda a decisão: <medição ou fato que faria subir/descer de nível>

## 2. Diagrama (texto)
entrada -> [etapa 1: ...] -> [checagem em código] -> [etapa 2: ...] -> saída

## 3. Contexto
| Situação | Técnica | O que preservar |

## 4. Delegação (se houver)
| Agente | Responsabilidade | Arquivos que escreve | Briefing (link) | Prova exigida |
Teto de fan-out: N · Revisor somente leitura: <quem>

## 5. Parada e tetos
- Condição de parada: ...
- Teto de iterações: N · Teto de custo por tarefa: US$ X (Suposição) · Timeout: ...

## 6. Segurança (cartão A/B/C)
A: <sim/não, fonte> · B: <sim/não, dado> · C: <sim/não, ação> · Configuração: <AB|AC|BC|ABC>
Barreiras: <remover capacidade | separar agentes | aprovação no ponto de saída> · Aprovações humanas: ...

## 7. Plano de eval
Suíte: <N tarefas, origem> · Graders: <código primeiro> · Métricas: <sucesso por tentativa, custo, p50/p95>
Comparação: baseline (chamada única) × workflow × agente · Status: projetado, não executado

## 8. Riscos, limitações, não verificado
## 9. Próximo passo
```

## Exemplo resumido: triagem de tickets (ilustrativo)

```markdown
# Brief de arquitetura: triagem e resposta de tickets
Data: 2026-10-10 · Modelo-alvo: Sonnet 5.5 (Suposição: assumido; usuário não informou) · Superfície: SDK cliente

## 1. Decisão
- Escolha: workflow (roteamento + encadeamento). Não é agente.
- Alternativa mais simples descartada: chamada única que classifica e responde. Só será descartada
  se a medição nos 2.000 tickets rotulados mostrar confusão relevante entre categorias (Inferido).
- Alternativa pedida pelo colega: orquestrador com 6 agentes. Descartada: os passos são sempre os
  mesmos e o custo extra (ordem de grandeza de 15x tokens em medição interna do fabricante) não
  tem ganho demonstrado.
- O que muda a decisão: classe crítica com falso negativo acima do aceitável após 2 rodadas de ajuste de prompt.

## 2. Diagrama
ticket -> [classificar: 1 chamada, saída estruturada] -> [rota: modelo/prompt da categoria]
       -> [responder] -> [checar formato e tamanho em código] -> resposta (ou fila humana)

## 5. Parada e tetos
- 3 chamadas por ticket no máximo; falha de formato: 1 nova tentativa, depois fila humana.

## 6. Segurança
A: sim (texto do cliente) · B: sim (histórico de pedidos) · C: não (a resposta é só rascunho para
agente humano). Configuração: AB. Barreira: C restrito; envio só por humano.

## 7. Plano de eval
2.000 tickets: 1.400 desenvolvimento, 300 regressão, 300 validação reservada. Código: acerto da
categoria, matriz de confusão por classe (classe "reembolso" como falha crítica), formato válido.
Juiz LLM só para tom, binário, calibrado (eval-design). Baseline × workflow. Projetado, não executado.
```

Divisão 1.400/300/300 é Suposição ilustrativa; defina conforme o custo de rotular (ver `eval-design`).
