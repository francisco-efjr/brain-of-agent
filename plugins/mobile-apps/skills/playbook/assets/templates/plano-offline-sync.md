# Plano offline e sincronização: [app ou feature]

Base: V-59 (guia oficial Android), V-45 (reescrito), V-60 e V-61. Responda as perguntas de projeto **antes** de codar; o que não tiver resposta vira Suposição com dono. Não copie o código do exemplo de terceiros (V-45): a fila dele não é recarregada na inicialização, o listener de rede dispara processamento concorrente e descarta itens acima de 1000.

Plataforma e versões lidas: [ex.: Android Room, iOS SwiftData, RN, Flutter] · Data: [AAAA-MM-DD]

## 1. Perguntas de projeto

| Pergunta | Resposta | Rótulo (Verificado / Suposição) |
| --- | --- | --- |
| Quais dados ficam disponíveis offline e por quanto tempo? | | |
| Há edição concorrente (vários aparelhos, vários usuários)? | | |
| Qual a política de conflito por tipo de dado? | | |
| Qual a latência aceitável até o servidor refletir a mudança? | | |
| Alguma operação tem efeito financeiro ou irreversível (exige identidade de operação)? | | |

## 2. Desenho

- Fonte local canônica (Room / DataStore / SwiftData / outro): [escolha]; a UI lê só dela, por tipos observáveis.
- Modelos: rede, entidade, externo, com mapeadores.
- Estratégia de escrita por tipo de dado:

| Tipo de dado | Estratégia (online-only / enfileirada com backoff / preguiçosa) | Motivo |
| --- | --- | --- |
| | | |

- Sincronização: [pull / push (réplica local) / híbrida].
- Registro com timestamp ou versão: [campo; de preferência do servidor]. A hora local de dois aparelhos não dá ordem confiável.
- Política de conflito: [última escrita vence com a fonte do relógio/versão definida / recusar e pedir resolução / merge desenhado]. SwiftData com CloudKit: conflito sem fonte (Suposição).

## 3. Fila de operações

| Propriedade | Decisão |
| --- | --- |
| Persistência (banco local) | |
| Recarga na inicialização | Obrigatória |
| Ordem e serialização | Processamento em série; exclusão mútua com o listener de rede |
| Idempotência | Chave de operação enviada ao servidor |
| Backoff | Exponencial; limite de tentativas: [n]; erro permanente vai para [estado "falhou"] |
| Retenção | [política explícita; sem descarte silencioso] |
| WorkManager (Android) | Worker idempotente, nome único, restrição de rede, `retry` com política |

## 4. Estados de UI

Offline, sincronizando, pendente por item, falhou (com ação), conflito. Nenhum sucesso fictício.

## 5. Testes

| Caso | Resultado esperado | Camada |
| --- | --- | --- |
| Editar offline, reiniciar o app, voltar a rede | Uma operação enviada, na ordem | Integração |
| Resposta perdida após o servidor processar | Reconciliação pela identidade; um efeito | Integração |
| Edição concorrente em dois aparelhos | Política de conflito aplicada, sem perda invisível | Integração |
| Token expira durante a sincronização | Refresh coordenado; fila preservada | Integração |
| Troca de conta A para B | Sem vazamento | UI |
| Transição de rede (sem rede, volta, interrupção no envio) | Estado consistente | Manual / instrumentado |

## 6. Riscos e lacunas

[ex.: resolução de conflito do CloudKit sem fonte; restrições do WorkManager não lidas; push/permissões em RN e Flutter via módulos]
