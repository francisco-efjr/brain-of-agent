# Fontes, atribuição e direitos

## Fonte única

AKITA, Fabio. **Competente o Suficiente: um ano colocando a inteligência artificial à prova, sem medo e sem propaganda.** Edição 1.0, 2026 (revisão v1.1.0, gerada em 18/11/2026). ISBN 9798162465683 (capa dura). akitaonrails.com.

Classe A para o que o autor mediu e documentou no próprio trabalho (experimentos, números datados, incidentes); as opiniões e previsões do autor aparecem nas regras como tal (por exemplo, "tendência, não prova").

## Direitos autorais e como este guia foi escrito

- O livro é protegido: todos os direitos reservados, com proibição de reprodução, tradução, adaptação e obra derivada, e reserva de mineração de texto e dados.
- Este plugin **não reproduz trechos**. Ideias, métodos e procedimentos foram reescritos com redação própria, reorganizados pela estrutura do Brain of Agent (contextos, portões, agentes e skills) e citados por capítulo só para rastreabilidade (por exemplo, `(cap. 16; ap. G)`).
- Nenhum texto do livro foi versionado neste repositório. A leitura foi feita em 19/11/2026 a partir da cópia do usuário, num diretório temporário da sessão.
- Este plugin **não é afiliado ao autor** nem endossado por ele. Nomes de projetos do autor não são usados como marca.

## Método de destilação

1. Extração do texto completo do PDF (prefácio ao apêndice J; fontes, créditos, glossário e referências ficaram de fora por não conterem práticas).
2. Oito leitores em paralelo (Sonnet 5.5), um por trecho, extraíram cada "fazer", "não fazer" e sinal de alerta, com redação própria e página aproximada: 839 itens.
3. Consolidação (Opus 5.5) em 386 regras com ID estável, alvo e contexto, agrupadas por área.
4. Cobertura conferida por script: 839 de 839 itens mapeados a ao menos uma regra; o mapa capítulo → regras está em `docs/dev-segments/research/agent-practice/VALIDACAO-COBERTURA.md`.
5. Checagem automática de sobreposição literal com o texto do livro e validação independente de qualidade (`BUILD-REPORT-quality.md`).

## Limites honestos

- As regras vêm da experiência documentada de um autor, em 2026, sobretudo com Claude Code e Codex em projetos próprios; o próprio livro pede que se meça no seu contexto antes de generalizar (AVA-02).
- Páginas são aproximadas; a referência por capítulo é a confiável.
- Números (preços, notas, limites de ferramentas) são datados e envelhecem; as regras valem pela função.
