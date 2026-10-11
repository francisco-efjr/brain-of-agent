# Notas

## Arquivos da skill lidos

- skills/qa/SKILL.md (inteiro)
- skills/qa/references/mobile.md (inteiro)
- skills/qa/references/estrategia.md (inteiro)
- skills/qa/assets/templates/plano-de-teste.md (inteiro)
- skills/qa/references/seguranca.md (trechos: linhas 1-60, 150-210, 280-350: upload/EXIF, LGPD, autorização)
- skills/qa/references/dados-ambientes-ci.md (linhas 25-65: dados sintéticos, evidência contém dados)
- skills/qa/references/dominios.md (linhas 1-40 e 255-320: pagamentos, eventos/idempotência, IoT)
- skills/qa/references/acessibilidade.md (linhas 380-410: seção Mobile)
- Apenas grep em design-de-testes.md e performance.md (sem leitura integral)

Nenhum script foi executado (não havia massa de CPF/limites nem código a gerar). Nenhuma requisição de rede.

## Incertezas

- Comportamentos de plataforma citados (permissão de localização "durante o uso" x "o tempo todo", localização aproximada, restrição de bateria por fabricante, indicador do SO) vêm de conhecimento geral, não da skill. mobile.md só diz "validar em aparelho físico o que depende de hardware, consumo e fabricante". Na resposta, deixei a ressalva de confirmar na versão-alvo.
- Requisitos das lojas (declaração de localização em segundo plano, textos de permissão): não verificados; a resposta manda confirmar nas políticas vigentes.
- Números (30 s de oferta, 10 MB, 50 m, lacuna de 2x o intervalo, 0,5 p.p., 1 h de sessão) são exemplos declarados como tal, não requisitos do produto.
- Suposições materiais: app em loja, GPS para mapa/operação (talvez repasse), upload por API, backend decide a atribuição. Não sei qual biblioteca de GPS em segundo plano o projeto usa, nem se há OTA de JS.
- Escolhi responder com lista priorizada por risco + perguntas, e não com o template completo do plano, porque o pedido foi "o que não pode faltar". Ofereço o documento completo no final. Pode haver quem prefira o template inteiro.
- Tamanho: ficou longo para uma pergunta de chat (cerca de 1.700 palavras). Mantive porque cada bloco tem caso concreto e resultado esperado; um corte possível seria remover a seção 3 ou 4.
