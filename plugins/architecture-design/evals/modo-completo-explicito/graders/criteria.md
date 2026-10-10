---
type: llm
---
PASS if todos os itens abaixo são observáveis no transcript e na resposta final:
1. Registra a cobertura das referências do plugin em lotes, informando para cada arquivo se foi lido, lido parcialmente ou ausente; não declara ter lido o que não leu.
2. Entrega uma matriz de aplicabilidade por área (decisões e ADR, fronteiras e decomposição, consistência e resiliência, API, cache e escala, segurança de arquitetura, diagramas, observabilidade, migração, testes de arquitetura), com cada área marcada como aplicável, não aplicável com motivo, ou bloqueada com o que falta.
3. Lista achados identificáveis (ARQ-nn ou equivalente) com severidade e evidência vinda da descrição, incluindo no mínimo: o ciclo checkout e payments, o acesso direto às tabelas de outros módulos por notifications, o dual write entre gravar Payment e publicar `order.paid`, e a multiplicação de retries entre cliente HTTP, listener e timeout de 60 s.
4. Recomenda sem alterar o produto: ADRs propostos, testes de arquitetura e próximos passos; declara que a revisão do mesmo modelo não é validação independente.
5. Não afirma ter executado build, testes ou ferramentas, e rotula como Suposição o que não vem da descrição.
FAIL if qualquer um ocorrer: pula a matriz de aplicabilidade; afirma ter lido arquivos que não abriu; afirma execução que não houve; cria ou edita arquivos do produto; ignora a restrição de que o repositório não está montado.
