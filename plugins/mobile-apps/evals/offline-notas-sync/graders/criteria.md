---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Não encerra apenas com perguntas: formula as perguntas de projeto (quais dados ficam offline, política de conflito para edição concorrente, latência aceitável) e assume respostas explícitas e rotuladas como Suposição, entregando o desenho até o fim e listando "Decisões pendentes" ou equivalente.
2. Usa o Room como fonte de verdade canônica, lida por tipos observáveis (Flow), com a UI sem ler a rede diretamente; escrita local primeiro.
3. Separa modelos de rede, entidade e externo (ou de domínio), com mapeadores.
4. Descreve fila de escritas pendentes persistida no banco, recarregada na inicialização, processada em série e ordenada, com chave de idempotência por operação e backoff exponencial; trata erro permanente e limite de tentativas.
5. Usa WorkManager (ou equivalente adiável) para o envio em segundo plano e diz que ele serve a trabalho adiável, sem prometer horário exato.
6. Coloca timestamp ou versão no registro e trata o conflito como decisão de produto: cita "última escrita vence" apenas como uma opção, recomenda que a ordem venha do servidor ou de versão, e avisa (rotulado Inferido) que o relógio local de dois aparelhos não dá ordem confiável por si só.
7. Inclui plano de teste de transição de rede e de resposta perdida depois de o servidor processar (uma operação, um efeito) e um indicador de offline na UI.
8. Entrega só o desenho (nenhum código de produção extenso) e marca como Não verificável tudo que depende de execução.
FAIL if qualquer um ocorrer: fila apenas em memória; impõe última escrita vence como única opção ou usa o relógio do aparelho como ordem final sem ressalva; ignora duplicação de operações; copia código de checklist de terceiros; afirma que testou ou compilou.
