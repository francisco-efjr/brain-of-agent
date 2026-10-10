# Protocolo de rodada, métricas, custo e relatório

Base: V-09, V-41, V-45, V-38 (preços), brain `qa/references/ia-e-llm.md` (protocolo de comparação, MIT) e `fullstack/references/agentes-e-ia.md`. Conferido em 2026-10-10.

## Congelar antes da rodada

Suíte e conjuntos, rubrica, versão do prompt/skill, modelo e configuração, ferramentas, limites de tempo e custo, regra de parada. Rode baseline e candidata nas mesmas condições, em ambiente limpo por tentativa. Salve saída integral, ações de ferramentas e o estado final permitido. Não dependa de acesso a raciocínio interno do modelo (raciocínio exibido não é prova; V-09, prompt-principles P-31).

## Métricas (com denominador sempre)

| Métrica | Fórmula | Para quê |
| --- | --- | --- |
| Sucesso por tentativa | sucessos / tentativas válidas | Taxa básica |
| Sucesso na primeira tentativa | sucessos na 1ª / casos | Dependência de retries |
| pass@k | ao menos 1 sucesso em k tentativas | "Existe solução?" (capacidade) |
| pass^k | todas as k tentativas têm sucesso | Consistência |
| Falhas críticas | contagem por tipo e por caso | Nunca diluir em média |
| Latência, custo | p50/p95; tokens ou US$ por tarefa concluída, incluindo retries e tools | Viabilidade |

Efeito de k: com 75% por tentativa, pass^3 = 0,75^3 ≈ 42% (valor citado em V-09). Com 90%: pass^3 ≈ 73% e pass^5 ≈ 59%. Com p = 0,5, pass@3 = 1 − 0,5^3 = 87,5%: o mesmo sistema parece ótimo em pass@k e frágil em pass^k. Escolha a métrica pelo uso: assistente que precisa acertar toda vez usa pass^k.

Dez reexecuções de uma mesma pergunta não equivalem a dez perguntas independentes. Temperatura zero não garante identidade entre infraestruturas, versões ou execuções. Reporte segmentos separadamente.

## Incerteza (brain `ia-e-llm`; conhecimento estável de estatística)

- 27 acertos em 30 são 90% **para aquela amostra e aquele avaliador**. O intervalo de Wilson de 95% é de cerca de 74% a 97% (calculado aqui: 0,744 a 0,965).
- 0 falhas em 30 tentativas não prova risco zero: sob independência, a regra aproximada 3/n dá limite superior perto de 10% (3/30).
- Com 45 acertos em 50, o intervalo de Wilson vai de cerca de 79% a 96%; com 90 em 100, de cerca de 83% a 94%.
- Dependência entre casos, seleção enviesada e muitos segmentos invalidam extrapolações ingênuas. Esses números mostram a margem; não definem o gate de aprovação.

## Verificações de validade da suíte (V-09)

- A tarefa é resolvível: existe solução de referência que passa nos graders. Muita falha numa só tarefa: suspeite da tarefa ou do verificador.
- O agente não burla o grader (checar atalhos que passam sem resolver).
- Cada tentativa em ambiente limpo; sem estado vazando entre execuções.
- Crédito parcial em tarefas de várias partes; avaliar o resultado, não o caminho.
- Registrar métricas além do acerto: tempo, chamadas de tool, tokens, erros de tool.

## Custo de uma rodada

Fórmula para `claude plugin eval` (V-41): casos × execuções × 2 braços + chamadas do juiz (3 chamadas curtas por grader `llm` e execução). Exemplo: 10 casos × 3 execuções × 2 braços = 60 execuções do agente, mais até 3 chamadas de juiz por grader `llm` por execução. Cada execução consome uso da conta; limite estourado no meio da suíte pontua 0 sem marcar a suíte como parcial (V-41).

Para suítes do seu produto via API: use Batch (metade do preço; expira se não concluir em 24 h; resultados disponíveis por 29 dias; `stream: true` não se aplica) e recontagem de tokens ao trocar de modelo (V-38). Preços e matriz de modelos mudam: ver `llm-decision-gates`.

## Ferramentas de apoio (V-45, lido em 2026-10-10, classe B)

| Ferramenta | Serve para | Ressalva |
| --- | --- | --- |
| promptfoo (MIT, 25.856 estrelas, commit de 2026-10-10) | Regressão de prompts em CI, red team, comparar provedores | README: passou a fazer parte da OpenAI; usar a mesma suíte em todos os provedores; "assertions" não consta no README, conferir na documentação |
| deepeval (Apache-2.0, 18.726 estrelas) | Métricas de RAG, agente, juiz | `deepeval login` envia casos à plataforma do fornecedor; `.env` carregado na importação |
| Inspect (MIT, 2.966 estrelas) | Avaliações de capacidade e segurança, mais de 200 avaliações prontas | Termos solver/scorer/sandbox não constam no README lido: não citar |
| DSPy (MIT, 38.577 estrelas) | Otimizar prompts depois que a suíte existe | Só com suíte própria e holdout |
| openai/evals (MIT, último commit 2026-04-14) | Referência de formato de registro | Manutenção mínima |

Em qualquer uma: asserções determinísticas antes de juiz, juiz calibrado contra rótulo humano, nenhuma instalação sem revisão. Adoção real citada nos READMEs não foi confirmada. Estrelas não provam qualidade.

## Relatório de avaliação (rubrica 0/1/2, brain `ia-e-llm`, adaptado)

| Dimensão | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Correção/oráculo | esperado errado ou circular | regra plausível, lacunas | esperado verificável e coerente com o requisito |
| Risco | ignora o dano principal | identifica sem priorizar | liga risco a verificações prioritárias |
| Evidência | inventa execução ou conclusão | distingue parcialmente | separa observado, inferido, suposição e não executado |
| Utilidade | conselhos impossíveis de aplicar | falta dado, sequência ou critério | alguém consegue executar a próxima ação |
| Escopo | desvia ou expande a autorização | esforço desproporcional | entrega o pedido com limites e esforço apropriados |

É um instrumento de revisão, não uma medição universal.

Estrutura do relatório de uma rodada: (1) pergunta e decisão que a rodada apoia; (2) o que foi congelado (versões, modelo, data, comando); (3) resultados por segmento com denominadores e intervalo; (4) falhas críticas por tipo; (5) leitura de transcrições: 3 falhas representativas e a classificação da causa; (6) riscos de validade; (7) status (`executado em <data>` ou `designed_not_executed`); (8) próxima mudança mínima.

## Rotulagem honesta

Sem execução de modelo: "caso projetado". Sem rótulo humano: "avaliação por IA". Benchmark preparado não significa modelo avaliado. Skills e instruções melhoram contexto e processo; não treinam pesos (brain `agentes-e-ia`).
