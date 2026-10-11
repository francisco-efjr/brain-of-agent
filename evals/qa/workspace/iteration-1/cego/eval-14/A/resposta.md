O que não pode faltar: provar, **em aparelho real, com o app em segundo plano e com rede ruim**, os quatro pontos onde esse tipo de app costuma falhar: rastreio contínuo, aceite sem duplicidade, comprovante que não se perde e tratamento de localização e foto como dado pessoal. O caminho feliz no emulador não cobre nenhum dos quatro.

Supondo que: o app fica em loja (correção lenta e cara, então pesa mais testar antes de publicar); a localização alimenta o mapa do cliente e a operação (talvez o repasse); a foto sobe por API para um storage; e o backend decide quem fica com a corrida. Nada disto foi executado: é análise a partir da sua descrição. Os números abaixo (30 s, 10 MB, 50 m) são exemplos para você trocar pelo requisito real.

## 1. Riscos que ordenam o plano

Escala 1 a 3 para probabilidade (P) e impacto (I). Alto é nota 6 ou 9.

| ID | Falha → efeito | P×I | Nível |
| --- | --- | --- | --- |
| R1 | O rastreio em segundo plano para (permissão rebaixada, SO ou fabricante matando o processo, economia de bateria) → cliente sem mapa, disputa de entrega, repasse errado | 3×3 | Alto |
| R2 | O comprovante se perde, vai para a corrida errada ou a entrega é concluída sem ele → contestação e estorno | 3×3 | Alto |
| R3 | Duas pessoas aceitam a mesma corrida, ou o aceite é repetido por retry → entrega duplicada ou sem ninguém | 2×3 | Alto |
| R4 | Resposta perdida depois de o servidor processar (aceitar, concluir, subir foto) e o app refaz a ação → efeito duplicado | 3×2 | Alto |
| R5 | Dado pessoal fora do lugar: rastreio fora da corrida, foto com rosto, endereço e GPS no EXIF, fila local que vaza entre contas, comprovante de outro entregador acessível pela API → LGPD e segurança | 2×3 | Alto |
| R6 | Turno longo drena bateria, esquenta ou dá ANR/crash em aparelho de entrada → entregador abandona o app | 2×2 | Médio |
| R7 | App antigo em campo contra backend novo, ou bug que só existe na build de release → falha que fica semanas com o usuário | 2×2 | Médio |
| R8 | Localização falsa ou foto reaproveitada para fraudar corrida ou repasse | 2×2 | Médio |

## 2. Casos que não podem faltar

**GPS em segundo plano (R1, R5, R8)**
- Permissão: primeira solicitação, "só durante o uso" (o app avisa que em segundo plano não funciona, conforme a regra do produto), "o tempo todo", recusa, localização aproximada no lugar da precisa, e **revogar nas configurações com a corrida em andamento**. Esperado: aviso claro, sem crash, e o backend sabe que o rastreio está degradado.
- Transições separadas, porque "fechei e abri" é ambíguo: ir para Home, bloquear a tela por 30 min, tirar dos recentes, forçar parada, reiniciar o aparelho, ligar a economia de bateria, abrir o app de navegação e voltar.
- Oráculo independente, não "o ponto aparece no mapa": uma rota conhecida (arquivo GPX no emulador/simulador serve para regressão) e, em campo, 30 min ou mais de trajeto real com um segundo aparelho gravando como referência. Esperado no backend: lacuna máxima entre pontos de, por exemplo, 2× o intervalo configurado; posição a no máximo 50 m da referência; ordem cronológica; sem pontos duplicados.
- Buffer offline (túnel, elevador, subsolo): os pontos sobem em ordem e sem duplicar ao reconectar.
- Início e fim: o rastreio começa na corrida e para ao concluir, cancelar ou sair do turno. Confira que o indicador do SO some e que não há mais requisição de localização. Isso vale para LGPD e para bateria.
- Hostil: localização simulada (mock location), salto impossível (2 km em 5 s) e relógio do aparelho errado.

**Aceite da corrida (R3, R4)**
- Duas contas sintéticas aceitando a mesma oferta ao mesmo tempo (script na API em paralelo, mais dois aparelhos). Esperado: exatamente um vencedor, mensagem clara para o outro e um único vínculo corrida × entregador no banco.
- Duplo toque; e **resposta perdida depois de o servidor aceitar** (proxy que derruba a resposta). Esperado: ao reconectar, o app consulta o estado em vez de aceitar de novo, e nunca mostra sucesso fictício.
- Oferta que expira ou é cancelada com a tela aberta; aceitar aos 29,9 s e aos 30,1 s (prazo de exemplo); relógio do aparelho adiantado 5 min (o prazo deve seguir o tempo do servidor).
- Estados: transições inválidas (concluir sem coletar, aceitar corrida cancelada, reabrir corrida concluída) são recusadas.
- Oferta por push com o app em segundo plano ou fechado: tocar abre a oferta certa. Teste o handler separado da entrega real do push.

**Foto do comprovante (R2, R4, R5)**
- Câmera: primeira solicitação, recusa, "não perguntar de novo" (leva às configurações e volta ao fluxo), cancelar a captura sem perder a corrida.
- **App morto enquanto a câmera está aberta** (aparelho com pouca memória, ligação recebida): ao voltar, a corrida e o estado da entrega estão preservados.
- Upload: sem rede ao concluir, rede cai no meio, reiniciar o app e o aparelho com a foto na fila. Esperado: a foto não se perde, sobe uma vez só, vai para a corrida certa (teste com duas corridas seguidas) e o arquivo no servidor tem o mesmo tamanho e hash do original.
- Arquivo: 0 byte, acima do limite (exemplo: 10 MB), orientação retrato e paisagem, armazenamento cheio, arquivo que não é imagem (se houver galeria).
- Privacidade: EXIF com GPS removido ou usado por regra explícita; foto fora de log.
- Falta um oráculo: **pode concluir sem foto, ou com upload pendente?** Sem essa resposta, o esperado de R2 fica sem definição.

**Segurança e LGPD (R5)**
- Autorização direto na API, pulando a tela: o token do entregador A não aceita, não consulta, não envia localização nem anexa foto na corrida do B. Esperado: 403 ou 404. O mesmo vale para deep link e notificação de corrida de outra conta.
- Trocar de conta no mesmo aparelho: fila de fotos, pontos pendentes, cache e notificações não aparecem na conta B; o logout limpa.
- Evidência de teste (print, vídeo, log, HAR) com coordenadas, endereço ou foto precisa ser mascarada antes de anexar em ticket.
- Textos de permissão e declaração de uso de localização em segundo plano: as lojas revisam isso e podem reprovar a versão. Confirme nas políticas vigentes de cada loja; não deduzi os requisitos.

**Release e campo (R6, R7)**
- Teste na **build de release** (assinada, minificada), não em debug.
- Atualização sobre a versão anterior **com corrida em andamento e fila pendente**; app antigo ainda suportado contra o backend novo; política de atualização obrigatória.
- Sessão longa (1 h ou mais) com tela bloqueada em aparelho de entrada, comparando bateria e memória com uma baseline que você define.

## 3. Onde provar cada coisa

- **Emulador/simulador:** rota GPX, permissões, fluxo aceitar → foto → concluir, estados e fila. Retorno rápido e estado reproduzível.
- **Aparelho físico (obrigatório para R1, R2 e R6):** segundo plano real, comportamento de bateria do fabricante, câmera real, rede móvel real.
- **Lógica sem tela:** estados da corrida, fila offline, idempotência e deduplicação em teste unitário e de integração. Use a ferramenta de E2E que o projeto já tem; confirme se ela alcança diálogos de permissão do sistema antes de depender dela.
- **Matriz mínima:** Android na versão mínima suportada e numa versão atual da base; um aparelho de entrada (pouca RAM) e um de fabricante com gerenciamento agressivo de bateria; iOS na mínima suportada e numa atual, com um iPhone físico mais antigo. Escolha os modelos pela sua base real, não por uma lista genérica.
- O comportamento de permissão de localização e de bateria muda a cada versão do SO. Confirme na versão-alvo.

## 4. Depois de publicar

Como a correção passa pela loja, o plano precisa de liberação gradual e de métricas com limiar de aborto **definido antes**. Exemplo: aborta se a taxa de corridas com rastreio contínuo, o upload de comprovante concluído ou a sessão sem crash cair mais que 0,5 ponto percentual abaixo da linha de base. Sem isso, o que só aparece em fabricante ou aparelho que você não testou chega a todos de uma vez.

## 5. O que fica de fora e o risco que sobra

- **Todos os modelos e fabricantes:** entregadores com aparelho fora da matriz podem ter o rastreio interrompido. Detecta-se pela métrica do rollout gradual.
- **Precisão do GPS em área urbana densa e em túnel:** só se mede em campo, em poucas rotas.
- **Carga no backend de despacho e entrega real de push em todas as condições:** fora deste plano, a menos que você me diga o contrário.
- **Acessibilidade e ergonomia (fonte ampliada, uma mão, sol):** só exploração curta de 30 a 60 min no fluxo aceitar → foto → concluir. Risco médio, sem automação.

## 6. Perguntas que mudariam o plano

1. Dá para concluir a entrega sem foto, ou com upload pendente? (define o esperado de R2)
2. O GPS entra no cálculo de repasse ou é só mapa? (sobe ou desce R1 e R8)
3. A oferta vai para vários entregadores ao mesmo tempo ou a atribuição é direta? (muda a profundidade de R3)
4. Quais são os modelos e versões mais usados na sua base? (define a matriz)
5. Há atualização do JavaScript fora da loja (OTA)? (muda a estratégia de release e de compatibilidade)

Se me responder isso, transformo o plano em documento completo, com cronograma, ambientes e critérios de entrada e saída, ou escrevo os casos acima em formato de tabela com dados concretos.
