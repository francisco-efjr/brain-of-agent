---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aplica o gate de contexto: uma base de ~120 páginas mais um FAQ provavelmente cabe no contexto (a referência é abaixo de cerca de 200 mil tokens, algo como 500 páginas), manda confirmar contando tokens com o modelo-alvo e recomenda, nesse caso, colocar o conteúdo no prompt com cache de prompt e sem RAG.
2. Diz que antes de qualquer investimento (RAG ou treino) é preciso uma suíte de avaliação própria (por exemplo 20 a 50 perguntas reais dos atendentes com resposta de referência), porque hoje não há como medir qualidade.
3. Sobre fine-tuning: aplica o gate (prompt e few-shot medidos primeiro; holdout; exemplos revisados; custo de manutenção quando o modelo base muda) e não afirma que existe fine-tuning direto de Claude na API; se mencionar, rotula como Não verificado e manda conferir a documentação oficial.
4. Se RAG ainda for necessário (base que crescer ou não couber), descreve medição em vez de configuração padrão: perguntas com trecho de referência, recall e precisão por chunk, chunking medido, `input_type` correto nos embeddings, citações.
5. Observa que a base muda duas vezes por ano: atualizar o prompt ou o arquivo é barato, enquanto retreinar não é; e que treinar não garante citar a fonte correta.
6. Rotula as afirmações (Verificado, Inferido, Suposição) e não cita preço ou limite de memória sem apontar a página oficial e a data.
FAIL if qualquer um ocorrer: projeta um pipeline completo de banco vetorial sem checar o gate de contexto; promete fine-tuning de Claude como opção disponível; inventa preços, limites ou números; recomenda construir sem plano de avaliação.
