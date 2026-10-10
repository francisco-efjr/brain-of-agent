# Orçamento de performance

Registre antes e depois, nas mesmas condições. Dado de campo no percentil 75 quando existir; laboratório (Lighthouse, DevTools) para diagnóstico. Limiares: web.dev (V-15), lidos em 2026-10-10; confira a página atual. Página ou fluxo: [URL ou rota]. Data: [AAAA-MM-DD].

## Condições da medição

- Origem do dado: [campo (RUM/CrUX) / laboratório]
- Build: [produção local / produção / desenvolvimento (não use desenvolvimento para medir)]
- Dispositivo ou emulação, CPU e rede: [ex.: viewport móvel, CPU 4x mais lenta, rede 4G emulada]
- Cache e autenticação: [limpo / aquecido; logado ou não]
- Ferramenta e versão: [Lighthouse x.y no Chrome n]
- Execuções: [n; usar a mediana]
- Arquivo da evidência: [caminho do JSON ou trace]

## Métricas

| Métrica | Bom | Ruim (acima de) | Antes | Depois | Origem | Passou? |
| --- | --- | --- | --- | --- | --- | --- |
| LCP | até 2,5 s | 4 s | [valor] | [valor] | [campo/lab] | [sim/não] |
| INP | até 200 ms | 500 ms | | | | |
| CLS | até 0,1 | 0,25 | | | | |

## Subpartes do LCP (diretriz de orçamento)

| Subparte | Orçamento aproximado | Medido |
| --- | --- | --- |
| TTFB | cerca de 40% | [valor] |
| Atraso de carregamento do recurso | abaixo de 10% | |
| Duração do download | cerca de 40% | |
| Atraso de renderização | abaixo de 10% | |

## Mudanças aplicadas e efeito

| Mudança | Arquivo:linha | Métrica afetada | Efeito medido | Validação |
| --- | --- | --- | --- | --- |
| [ex.: remover lazy-load da imagem do LCP] | [caminho] | LCP | [antes e depois] | [nova medição] |

## Limitações

Lighthouse 100 não é conformidade nem experiência real. Laboratório não é campo. Uma execução não prova nada. Dado de campo [existe / não existe]; se não existe, peça RUM ao usuário (`/sre-observability:playbook`).
