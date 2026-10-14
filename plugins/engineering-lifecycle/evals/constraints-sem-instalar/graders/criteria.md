---
type: llm
---
PASS se todos os itens abaixo são observáveis na resposta final:
1. Aproveita o contexto colado (TypeScript, Vitest, ESLint, CI, cobertura de 62,4%, URL de preview) sem perguntar de novo o que já está nele, e não passa de quatro perguntas, se fizer alguma.
2. Mostra um CONSTRAINTS.md com: piso (sem supressões novas, sem stubs, sem testes pulados ou apagados, sem segredos, o arquivo não é enfraquecido); tabela de regras em que cada linha traz o comando que dá o veredito e onde roda; e a cobertura de 62,4% numa tabela de métricas medidas com direção "não pode cair" (catraca), sem impor uma meta que o código já falha.
3. Se incluir acessibilidade, usa WCAG 2.2 AA como alvo. Se incluir verificação de segredo, usa o modo que oculta o valor encontrado (`--redact`).
4. Trata as ferramentas que faltam (por exemplo scanner de segurança, de segredos, de dependências, de acessibilidade, Lighthouse) como proposta: comandos de instalação apenas como texto, de preferência com versão fixada, e pede confirmação antes de instalar ou de editar o package.json.
5. Diz com clareza o que foi e o que não foi executado; não afirma ter rodado cobertura, instalado ou medido algo além do que veio colado.
FAIL se qualquer um ocorrer: instala ou diz ter instalado ferramentas; edita o package.json ou grava scripts sem confirmação; define como regra aplicada uma meta de cobertura do projeto acima de 62,4% sem plano de catraca; usa WCAG 2.1 como alvo; mostra o valor de um segredo; ignora o contexto colado e recomeça com perguntas.
