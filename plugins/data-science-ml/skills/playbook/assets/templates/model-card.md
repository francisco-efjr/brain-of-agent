# Model card

Campos propostos pelo plugin (Inferido; a lista oficial de seções de Mitchell et al., arXiv 1810.03993, não foi lida). As funções Govern, Map, Measure e Manage do NIST AI RMF servem só de moldura para a seção de riscos; este modelo não gera requisitos do NIST (V-32). Preencha apenas o que foi medido; o resto fica "não medido".

- **Modelo:** [nome], versão [..], alias no registro [..], data [aaaa-mm-dd]
- **Responsável:** [pessoa/equipe]  **Run de origem:** [link/ID do run]  **Commit:** [sha] (sujo: [sim/não])

## 1. Uso
- **Uso pretendido:** [decisão, usuário, instante da decisão]
- **Uso não recomendado:** [..]

## 2. Dados
- Treino: fonte [..], janela [início–fim], n [..], hash [..]
- Avaliação: fonte [..], janela [..], n [..] (posterior ao treino quando há tempo)
- PII e consentimento: [..]

## 3. Desempenho
| Fatia (definida antes de ver o resultado) | n | Métrica | Intervalo | Baseline |
| --- | --- | --- | --- | --- |
| Global | [..] | [..] | [a, b] | [..] |
| [fatia] | [..] | [..] | [a, b] | [..] |
Calibração: [log loss/Brier; curva] · Limiar adotado e como foi escolhido: [validação, custo]

## 4. Limitações conhecidas
[distribuições onde falha; fatias pequenas; dependências; o que não foi testado]

## 5. Riscos e mitigação
| Risco | Função (Govern/Map/Measure/Manage) | Mitigação | Dono |
| --- | --- | --- | --- |
| [..] | [..] | [..] | [..] |

## 6. Operação
Monitoramento: [drift de entrada, predição, qualidade; dono e ação] · Rollback: [versão anterior] · Revisão periódica: [data]
