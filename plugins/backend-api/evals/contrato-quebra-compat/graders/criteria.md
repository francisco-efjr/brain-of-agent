---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Classifica cada uma das quatro mudanças e conclui que todas quebram consumidores existentes: campo obrigatório novo na entrada, valor novo de enum na resposta (quebra clientes com switch exaustivo ou validação de enum fechado), troca de paginação por página para cursor e remoção de campo.
2. Considera explicitamente que os apps Android e iOS em campo não atualizam na hora e que os parceiros fixam o contrato, e usa isso para justificar mitigação (coexistência, versão mínima, versão nova da API).
3. Propõe alternativas compatíveis para cada item: `taxId` opcional com default ou exigido só em versão nova; `REFUNDED` entregue só a clientes que declaram suporte ou contrato com enum aberto; manter `page` por uma janela ao lado de `cursor`; manter `sku` e marcá-lo como depreciado.
4. Recomenda sinalizar a depreciação (cabeçalhos `Deprecation` e `Sunset` ou equivalente), com data e substituto, e plano de comunicação aos parceiros.
5. Sugere validar com diff de spec e linter (por exemplo oasdiff e Spectral) e rotula isso como não executado, sem inventar saída.
6. Não diz que pode publicar amanhã como está.
FAIL if qualquer um ocorrer: aprova a publicação; trata o enum novo como compatível sem ressalva; trata campo obrigatório novo como compatível; afirma ter rodado ferramenta ou cola saída inventada.
