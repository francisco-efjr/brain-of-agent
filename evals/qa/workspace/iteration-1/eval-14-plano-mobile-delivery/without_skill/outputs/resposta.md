Num app de entregas, o caminho feliz (aceita, entrega, tira foto) é a parte que menos quebra. O que costuma dar problema em produção é o app sendo interrompido, o sistema matando o processo, a permissão negada pela metade e a rede ruim. Monte o plano em volta disso. Duas regras valem para tudo abaixo: teste em **aparelho real** (emulador não reproduz economia de bateria nem o sistema matando o app) e em **build de release** (o comportamento em debug engana, principalmente em React Native).

## 1. Permissões (matriz de estados)

Cada permissão pode estar em vários estados, e o app precisa se comportar bem em todos:

| Permissão | Estados que não podem faltar |
|---|---|
| Localização | Nunca perguntado, negado, negado com "não perguntar de novo", só "durante o uso", "sempre", aproximada em vez de precisa (Android 12+ e iOS 14+) |
| Câmera | Nunca perguntado, negada, negada em definitivo |
| Notificações (Android 13+, iOS) | Negada: o entregador ainda fica sabendo que tem corrida nova? |

Cenários obrigatórios:
- **Revogar a permissão nas Configurações com o app aberto ou em segundo plano.** O app deve detectar, avisar e levar o usuário à tela certa, sem travar nem continuar "rastreando" de mentira.
- **Android 10+:** localização em segundo plano é pedida separadamente. No Android 11+ o usuário é mandado às Configurações para escolher "Permitir o tempo todo". Teste esse fluxo inteiro, incluindo a tela explicativa que a Google Play exige antes do pedido.
- **iOS:** o "Sempre" costuma aparecer só depois, como upgrade. Se o entregador ficar em "Durante o uso", o que acontece com o rastreamento quando ele troca para o Waze ou bloqueia a tela?
- GPS do aparelho desligado, modo avião e economia de bateria ativados no meio da corrida.
- Textos de justificativa (iOS) e avisos de uso de localização em segundo plano (Android) corretos e em português.

## 2. GPS em segundo plano (o risco nº 1)

- **Continuidade:** o rastreamento segue funcionando com a tela bloqueada por 30 minutos ou mais, com o app em segundo plano e com o entregador usando outro app de navegação por cima. Confira no **servidor** que os pontos estão chegando, não só no app.
- **Android:** serviço em primeiro plano com notificação visível (obrigatório), tipo de serviço de localização declarado (Android 14+), Doze e economia de bateria. Teste em fabricantes que matam apps de forma agressiva (Xiaomi, Samsung, Motorola, Huawei/Honor) e com "otimização de bateria" ativa.
- **iOS:** modo de segundo plano de localização, indicador azul na barra, Atualização em Segundo Plano desligada, Modo de Pouca Energia.
- **App morto:** deslizar o app da lista de recentes, o sistema matar por falta de memória, o aparelho reiniciar no meio da corrida. O comportamento esperado precisa estar definido (retoma sozinho? avisa o entregador?) e é diferente entre iOS, Android e fabricantes.
- **React Native:** o JavaScript pode ser suspenso em segundo plano. Verifique que o envio de localização acontece de fato com o app em background e não depende de a tela estar aberta. Se usar biblioteca comercial de geolocalização, confirme que o build de release está licenciado.
- **Início e fim:** o rastreamento começa quando a corrida é aceita e **para** quando é concluída, cancelada ou o entregador sai do turno. Rastrear fora da corrida é problema de privacidade (LGPD) e de bateria.
- **Qualidade do dado:** frequência dos pontos, buracos longos (túnel, sinal ruim), saltos absurdos de posição, precisão ruim filtrada, pontos fora de ordem e duplicados após reconectar, fuso e horário do aparelho alterados.
- **Localização falsa:** ligar "localização simulada" no Android ou app de fake GPS. O app/servidor detecta ou ignora? É fraude clássica em entrega.
- **Teste de campo:** rota real de 30 a 60 minutos a pé, de moto ou de carro, com o aparelho no bolso. Simuladores de rota (GPX no Xcode, rota no emulador Android) ajudam no funcional, mas não substituem a rua.

## 3. Câmera e foto do comprovante

- Fluxo normal: foto tirada, pré-visualização, refazer, confirmar, envio, corrida concluída só depois do sucesso do envio (ou conforme a regra de negócio).
- **Interrupções com a câmera aberta:** ligação, notificação, app indo para segundo plano, bloqueio de tela. Em Android com pouca memória o processo pode ser morto enquanto a câmera nativa está aberta e o resultado da foto se perde. O app precisa recuperar o estado da corrida e não perder a entrega.
- Câmera ocupada por outro app, aparelho sem armazenamento livre, pouca memória.
- Qualidade: baixa luz, sol forte, flash, foto tremida, orientação (retrato/paisagem, foto aparecendo girada), foto muito grande (compressão e tamanho do arquivo) em aparelho simples.
- **Envio:** rede fraca ou caindo no meio do upload, retentativa, retomada, foto enviada em duplicidade, foto presa na fila quando o app é fechado, comportamento ao reabrir.
- Regras de negócio: pode escolher da galeria ou só tirar na hora? A foto carrega data, hora e localização (e isso bate com o endereço)? Quem pode ver a foto depois? Rosto e fachada de casa são dado pessoal.

## 4. Aceite da corrida

- **Concorrência:** dois entregadores aceitam a mesma corrida ao mesmo tempo, e o servidor deve garantir um único vencedor, com mensagem clara ao outro.
- Toque duplo no botão, aceite com rede caindo (o app sabe se o aceite foi registrado?), corrida cancelada ou expirada enquanto a tela estava aberta, aceite depois do tempo limite.
- Chegada da oferta com o app aberto, em segundo plano, fechado e com a tela bloqueada (push). Atraso e notificações perdidas em Android e iOS.
- **Retomada:** fechar e reabrir o app, ou fazer logout/login, no meio da corrida. O estado da corrida (aceita, a caminho, coletada, entregue) é restaurado corretamente?
- Sessão expirando ou token renovando enquanto o app está em segundo plano.
- Entregador com duas corridas, mudança de status fora de ordem, tentativa de concluir sem foto.

## 5. Rede e modo offline

- Sem internet, 2G/3G lento, troca de Wi-Fi para 4G, túnel e elevador. Use o limitador de rede do aparelho ou de um proxy.
- Definir e testar o que fica em fila local (pontos de GPS, foto, mudança de status), por quanto tempo e como sincroniza na volta, sem duplicar nem perder.
- Consumo de dados do pacote móvel durante um turno inteiro.

## 6. Ciclo de vida e interrupções

Ligação recebida, outro app de navegação em primeiro plano, tela dividida, rotação, alarme, bateria baixa e desligamento, mudança de data e hora, atualização do app no meio do turno, atualização do sistema operacional.

## 7. Bateria e desempenho

- Teste longo de turno (4 a 8 horas) com a tela apagada: consumo de bateria por hora, aquecimento, memória, crescimento da fila local.
- Aparelhos de entrada com pouca RAM, que é o que muito entregador usa.
- Defina com o produto metas mensuráveis (por exemplo, intervalo máximo aceitável entre pontos e consumo máximo por hora). Sem número, ninguém consegue dizer que passou.

## 8. Privacidade, segurança e lojas

- LGPD: consentimento e transparência sobre rastreamento, coleta só durante a corrida, retenção dos dados.
- Tráfego só por TLS, foto e localização não acessíveis por URL pública, token fora de log.
- Aprovação nas lojas: justificativa de localização em segundo plano (Google Play e App Store) e textos de permissão. Teste a partir de TestFlight e da faixa de teste interno da Play, não só em build local.

## 9. Matriz de dispositivos

Mínimo razoável: 2 a 3 versões de Android (incluindo 14 ou superior e uma mais antiga que você ainda suporta), 3 a 4 fabricantes, pelo menos um aparelho simples; no iOS, as duas ou três últimas versões e um iPhone mais antigo. Priorize pelos dados reais de uso dos seus entregadores.

## 10. O que automatizar e o que fica manual

- **Automatizar:** regras de aceite e máquina de estados da corrida (unitário e API), fila offline e sincronização, fluxos de tela com Maestro ou Detox, regressão em nuvem de aparelhos.
- **Manual em aparelho real:** permissões do sistema, GPS em segundo plano, app morto, câmera interrompida, bateria, campo.
- Monitoramento em produção (crash, buracos de GPS, falha de upload) ajuda a descobrir o que o plano não previu.

## Se o tempo for curto, priorize

1. Rastreamento contínuo com tela bloqueada e outro app em primeiro plano, em Android (com fabricantes agressivos) e iOS.
2. Fluxo completo de permissões, incluindo negar, revogar depois e "só durante o uso".
3. Foto do comprovante com interrupção e rede ruim, sem perder a entrega.
4. Aceite concorrente e retomada da corrida depois de fechar o app.
5. Teste de turno longo (bateria) em aparelho simples.

Se você me disser três coisas, eu transformo isso em casos de teste detalhados: qual biblioteca de geolocalização o app usa, se existe modo offline (e o que a regra de negócio manda fazer sem rede) e se a foto do comprovante é obrigatória para concluir a entrega.
