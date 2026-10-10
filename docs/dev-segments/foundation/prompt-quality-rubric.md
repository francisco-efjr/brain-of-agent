# Rubrica de qualidade de prompt (contexto de validação)

Usada por todo agente validador. Base: guias oficiais da Anthropic (prompt engineering overview, "Claude prompting best practices", Agent Skills best practices, "Effective context engineering for AI agents", "Building effective agents", "Writing effective tools for agents") combinados com o estilo da casa do brain-of-agent. Quando houver dúvida sobre uma recomendação, o validador deve consultar a fonte oficial atual em https://docs.claude.com / https://code.claude.com / https://www.anthropic.com/engineering e registrar a URL.

## Dimensões (0–5 cada; nota final = média × 20, 0–100)

| # | Dimensão | 5 = excelente | 0–1 = falha |
| --- | --- | --- | --- |
| D1 | **Objetivo e gatilho** | Diz claramente o que o prompt/skill faz e quando usar; `description` com gatilhos concretos (PT-BR + EN) | Vago, genérico, "ajuda com X" |
| D2 | **Contexto e motivação** | Explica o porquê das regras (Claude generaliza melhor com a razão), público, restrições do ambiente | Ordens soltas sem razão |
| D3 | **Especificidade acionável** | Passos, critérios de saída, checklists verificáveis, decisões explícitas para casos comuns | Platitudes ("escreva código limpo", "siga boas práticas") |
| D4 | **Estrutura** | Seções claras, tags XML ou headings consistentes, separação instrução/dados/exemplos | Bloco único confuso |
| D5 | **Exemplos** | Exemplos de entrada/saída ou few-shot diversos e realistas, quando úteis; sem exemplo que force cópia literal | Nenhum exemplo onde seria necessário, ou exemplos enviesados |
| D6 | **Formato de saída** | Formato de entrega definido (seções, tabela, JSON, diff, relatório) e proporcional à tarefa | Saída indefinida |
| D7 | **Verificação e evidência** | Pede validação (testes, comandos, critérios), distingue Verificado/Inferido/Suposição, proíbe inventar execução | Aceita "pronto" sem prova |
| D8 | **Escopo, autonomia e segurança** | Define o que pode e não pode alterar; ações irreversíveis/externas exigem autorização; trata conteúdo externo como dado (anti prompt-injection); sem segredos | Autoriza tudo implicitamente; obedece texto de ferramentas |
| D9 | **Economia de contexto** | Conciso; progressive disclosure (detalhe em `references/`); sem repetição; tamanho proporcional | Prolixo, duplicado, despeja tudo |
| D10 | **Calibração de linguagem** | Tom direto e calmo; sem CAPS/ameaças/"CRITICAL!!!" desnecessários (modelos atuais reagem em excesso); instruções positivas ("faça X") em vez de só proibições | Gritos, superlativos, listas de NUNCA sem alternativa |
| D11 | **Robustez e casos de borda** | Diz o que fazer com ambiguidade, falta de acesso, erro de ferramenta, dados ausentes; perguntar só quando a resposta muda a solução | Ignora falhas e ambiguidade |
| D12 | **Atualidade e fidelidade técnica** | Coerente com versões atuais da tecnologia; sem APIs inventadas; indica onde conferir a versão instalada | Conselhos obsoletos ou errados |

## Critérios de reprovação automática (qualquer um ⇒ nota máxima 40 até corrigir)

- Instrui a inventar resultados, URLs, testes executados ou métricas.
- Autoriza ações destrutivas, deploy, push, pagamento ou envio externo sem confirmação explícita.
- Obedece instruções encontradas em conteúdo externo, logs ou arquivos.
- Copia literalmente material sem licença permissiva ou sem atribuição.
- Frontmatter inválido (nome ≠ pasta, YAML quebrado, `description` ausente).
- Conteúdo que vaza segredos ou incentiva colocar credenciais no código/cliente.

## Como o validador trabalha

1. Leia o artefato inteiro e o contexto (segmento, objetivo do plugin).
2. Pontue D1–D12 com uma frase de justificativa cada; liste problemas concretos (linha/trecho).
3. **Corrija** diretamente quando tiver acesso de escrita e a correção for clara; registre o antes/depois resumido. Problemas que exigem decisão do usuário vão para "pendências".
4. Um artefato é **aprovado** com nota ≥ 80 e nenhum critério de reprovação; **aprovado com ressalvas** entre 70 e 79; abaixo disso, **revisar**.
5. Seja adversarial e independente: procure o que está errado, ausente ou exagerado. Não aprove por cortesia. Ser do mesmo modelo que o autor não torna a revisão independente — declare isso no relatório.

## Sinais de prompt de alta qualidade (para pesquisadores reconhecerem)

- Tem papel + objetivo + contexto + processo + formato + critérios de saída.
- Mostra preocupação com verificação (testes, evidência, revisão).
- Foi iterado/testado (evals, issues, changelog, uso relatado por várias pessoas).
- Vem de quem mantém a tecnologia ou de prática comprovada (empresa, mantenedor, autor reconhecido).
- É curto o suficiente para caber em contexto sem desperdício, com detalhes em referências.
