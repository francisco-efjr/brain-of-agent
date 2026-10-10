# Frontend, profiling e gate de regressão

## Sumário

1. Core Web Vitals: metas, medição e ações
2. Orçamentos e Lighthouse CI como regressão
3. Flame graphs
4. Gate de regressão com baseline próprio

## 1. Core Web Vitals (V-19)

| Métrica | Bom (Verificado em web.dev, p75) | Ruim (Inferido; não está no texto do web.dev) |
| --- | --- | --- |
| LCP (maior elemento visível) | até 2,5 s | acima de 4 s |
| INP (resposta a interações) | até 200 ms | acima de 500 ms |
| CLS (estabilidade visual) | até 0,1 | acima de 0,25 |

Regras de medição:

- Os limiares valem para o **percentil 75** das visitas reais, **separando mobile e desktop**.
- **Campo primeiro** (RUM com a biblioteca `web-vitals`, CrUX); laboratório (Lighthouse) é diagnóstico e regressão.
- No modo de navegação padrão o Lighthouse não interage com a página e **não mede INP**: usa TBT (Total Blocking Time) como proxy. O modo timespan (fluxos de usuário) mede o INP de laboratório das interações roteirizadas; ainda assim não substitui o dado de campo. Quem apresenta "INP do Lighthouse" sem dizer o modo confundiu as métricas; peça a origem e o dado de campo.
- O Lighthouse emula por padrão celular com rede lenta e CPU mais lenta, o que é adequado a públicos com Android intermediário.

Ações por métrica (checklist do V-19; confira compatibilidade de navegador atual antes de recomendar APIs recentes):

| Métrica | Ações |
| --- | --- |
| LCP | Imagem principal priorizada e pré-carregada; sem `loading="lazy"` acima da dobra; CSS crítico; scripts com `defer` ou `async`; reduzir TTFB do servidor |
| INP | Dividir tarefas longas; code splitting; trabalho pesado em worker; evitar re-renderizações caras no handler |
| CLS | Dimensões em imagens e iframes; `font-display` adequado; espaço reservado para conteúdo injetado |

O arquivo `performance-optimization.instructions.md` do awesome-copilot (MIT) tem regras úteis, mas pontos contestáveis que **não** devem ser copiados: cache de página inteira sem checar dados por usuário, suporte de navegador datado, estabilidade de signals do Angular, barrel imports como problema universal, `Intl.DateTimeFormat` como substituto de moment.

## 2. Orçamentos e Lighthouse CI (brain `performance.md`, MIT, adaptado)

- **Orçamentos** (peso de JS, imagens, número de requisições) são o gate mais estável. Parta do estado atual e aperte aos poucos; os 300 KB do exemplo do brain são ilustrativos.
- Lighthouse CI com 3 execuções por URL (usa a mediana); não use armazenamento público temporário em sistema interno (publica o relatório). A execução (`npx @lhci/cli autorun`) fica a cargo do usuário; a skill não a recomenda como passo.

Exemplo de `lighthouserc.json` (rascunho, valores ilustrativos):

```json
{
  "ci": {
    "collect": { "url": ["https://staging.exemplo.test/"], "numberOfRuns": 3 },
    "assert": {
      "assertions": {
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }],
        "total-blocking-time": ["warn", { "maxNumericValue": 200 }],
        "resource-summary:script:size": ["error", { "maxNumericValue": 300000 }]
      }
    },
    "upload": { "target": "filesystem", "outputDir": "./lhci-relatorios" }
  }
}
```

Laboratório reprova regressão, não prova experiência real: a decisão de "bom" continua no p75 de campo.

## 3. Flame graphs (V-25, Brendan Gregg)

- O eixo x **não é tempo**: é a população de pilhas, ordenada; a **largura** indica presença nas amostras.
- Procure platôs largos perto do topo (funções que consomem CPU diretamente).
- Tipos: CPU, off-CPU (espera), memória e diferencial (compara dois perfis). Flame **chart** (eixo x é tempo) é outra coisa.
- A qualidade das pilhas depende do profiler (símbolos, frames inlined).
- Procedimento ao receber um perfil: tipo de perfil e janela; função mais larga no topo; chamador que a explica; pergunta que o perfil responde e a que não responde.
- **Lacuna**: profilers por linguagem e consulta lenta de banco sem fonte de classe A. Rotule **Não verificável** e peça a documentação da linguagem ou do banco (ex.: o plano de execução de consulta é assunto de `database-data-modeling`).

## 4. Gate de regressão (V-20, destilado de garrytan/gstack `benchmark`, MIT)

Princípios (sem fixar números como regra):

1. Compare com **baseline próprio**, capturado no mesmo ambiente; não sobrescreva o baseline durante a comparação.
2. **Ausência é ausência**: métrica que não veio (ex.: LCP ausente) é "N/A", nunca zero. Baseline zero gera variação N/A.
3. **Falha de carga é falha**, não lentidão.
4. Ruído: uma passada varia; repita 3 a 5 vezes e use a **mediana** quando o ambiente for ruidoso (no gstack a mediana de 3 é opcional).
5. Prefira gates determinísticos: consultas SQL por requisição, tamanho de bundle, número de requisições.

Limiares do autor, usados só como **exemplo (Suposição)**: tempo acima de 50% ou 500 ms é regressão e acima de 20% é aviso; bundle e transferência acima de 25% é regressão e acima de 10% aviso; contagem de requisições acima de 30% só aviso. Orçamentos de exemplo do mesmo autor (FCP < 1,8 s, LCP < 2,5 s, 500 KB de JS, 2 MB totais, 50 requisições) também são exemplo.

Não reproduzido do gstack: preâmbulo `gstack-*`, telemetria, daemon de navegador e `./setup`.

No CI: no PR, teste pequeno e estável (carga baixa e fixa por 1 a 3 min, limiares folgados que pegam regressão grosseira); a carga completa roda à noite ou antes do release em ambiente representativo; compare com a mediana das últimas execuções (ex.: p95 20% acima da mediana das últimas 5, tolerância combinada pelo time).
