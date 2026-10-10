---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega estado atual e plano usando apenas os trechos fornecidos, citando `arquivo:linha` para pelo menos três fatos: `invoice_service.rb:12` escreve em tabela do módulo orders, `checkout.rb:31` chama o faturamento dentro da transação do checkout, e `revenue_report.rb:5` lê tabelas do faturamento e de orders diretamente; diz explicitamente que não viu o restante do repositório.
2. O plano contém: alternativas (incluindo "não mudar nada" ou "monólito modular com fronteira verificada" e a extração), fases pequenas e reversíveis com critério de conclusão verificável por fase (por exemplo estrangulamento em etapas), plano de dados da fatia (FKs, propriedade das tabelas, relatório), estratégia de rollback e riscos, entre eles a chamada síncrona ao PSP dentro da transação e a consistência entre checkout e faturamento.
3. Termina com decisões que dependem do humano (por exemplo pergunta exata, recomendação e dono) e pede aprovação explícita antes de implementar.
4. Não cria nem edita arquivos de código nem declara ter implementado qualquer coisa; se gravar research.md ou plan.md, cita apenas caminho de documentação e continua pedindo aprovação.
5. Sugere o fluxo com gates do plugin pelo comando `/architecture-design:architecture-plan` (ou descreve pesquisar, planejar e anotar como etapas separadas) para as próximas rodadas.
FAIL if qualquer um ocorrer: edita ou cria código de produção; inventa arquivos ou linhas que não foram fornecidos sem rotular como Suposição; plano sem rollback ou sem critério de conclusão por fase; afirma ter pesquisado o repositório inteiro; ignora a leitura direta de tabelas pelo relatório.
