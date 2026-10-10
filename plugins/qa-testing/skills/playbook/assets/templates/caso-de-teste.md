# Caso de teste: <ID e comportamento verificado>

Como usar: um comportamento por caso; o título diz o comportamento ("Recusa transferência acima do limite diário"), não "Teste 3". Dados concretos ("R$ 5.000,01"), nunca "um valor inválido". Esperado observável (mensagem, estado, registro, valor) com a **fonte** da regra; esperado ambíguo vira pergunta, não palpite. Uma classe inválida por caso. Adaptado do brain-of-agent (MIT).

- **Requisito ou risco:** <fonte e dano coberto>
- **Técnica:** <partição, valor-limite (3 valores), tabela de decisão, transição de estados, pairwise, suposição de erro>
- **Prioridade:** <alta / média / baixa e motivo ligado ao risco>
- **Pré-condições:** <estado, permissões, ambiente e versão>
- **Dados:** <valores concretos e sintéticos>
- **Oráculo:** <regra ou cálculo independente que define o esperado>

| Passo | Ação | Resultado esperado observável |
| --- | --- | --- |
| 1 | <ação> | <estado, valor, mensagem ou efeito persistido> |

**Execução:** <não executado / passou / falhou / bloqueado>
**Resultado observado e evidência:** <preencher somente após executar; comando e saída reais>
**Limpeza:** <dados criados e como remover no ambiente de teste>

Versão em tabela para planilha: `ID | Cenário | Pré-condição | Passos | Dados | Esperado | Prioridade | Técnica`.

Exemplo: `FRT-03 | Frete grátis no limite exato | cliente sem VIP, sem cupom | adicionar itens somando R$ 199,00; ir ao checkout | subtotal 199,00; CEP 01310-100 | frete R$ 0,00 (regra: grátis a partir de R$ 199,00, inclusive) | Alta | valor-limite`
