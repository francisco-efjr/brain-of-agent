# Notas e incertezas

Resposta escrita só com conhecimento próprio, sem skill, sem consultar a pasta evals/ e sem rede.

## Incertezas

- **App morto pelo usuário (swipe) e rastreamento:** o comportamento muda entre iOS e Android e entre fabricantes. No iOS não tenho certeza se o sistema relança o app por mudança significativa de localização depois de um force-quit. Por isso, na resposta, defini apenas que o comportamento esperado deve ser decidido e testado, sem afirmar o que acontece.
- **Versões de Android:** citei Android 10 (permissão de background separada), 11 (fluxo pelas Configurações), 12 (localização aproximada), 13 (permissão de notificações) e 14 (tipo de serviço em primeiro plano). Baseado em memória; vale conferir a documentação atual, já que as regras de foreground service e localização mudam a cada versão.
- **iOS:** o pedido de "Sempre" como upgrade posterior é o comportamento que lembro, mas pode ter mudado nas versões mais novas.
- **Biblioteca comercial de geolocalização com licença em release:** é algo que sei de bibliotecas específicas (ex.: de segundo plano pagas). Não citei nome para não afirmar sem ter certeza do app do usuário.
- **Fabricantes agressivos com bateria:** lista (Xiaomi, Samsung, Motorola, Huawei/Honor) vem de experiência geral; a relevância depende do parque de aparelhos dos entregadores.
- **Metas numéricas:** não inventei limites (consumo por hora, intervalo entre pontos). Sugeri definir com o produto.
- **Matriz de dispositivos:** sugestão genérica, sem dados reais de uso.

## Decisões de escopo

- Não montei casos de teste passo a passo (seria longo e dependeria de respostas que não tenho); terminei oferecendo detalhar após três perguntas (biblioteca, offline, foto obrigatória).
- Incluí tabela só para permissões, onde ela ajuda de verdade; o resto em tópicos.
- Mencionei LGPD e aprovação nas lojas por serem riscos reais para localização em segundo plano, apesar de o usuário não ter perguntado diretamente.
- Não executei comandos locais nem usei rede; nada foi modificado fora da pasta de saída.
