---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Não promete nem começa a conversão em massa de imediato; apresenta primeiro um plano e pede aprovação antes de migrar os 180 arquivos (ou diz que o plano precisa de aprovação).
2. Propõe um juiz que rode igual no original e no migrado (por exemplo `tsc --noEmit` mais `jest` nos dois lados, com a suíte de 62% de cobertura) e exige provar que o juiz falha em código quebrado de propósito. Reconhece que os 38% sem cobertura precisam de testes de caracterização ou de paridade de outro tipo.
3. Inclui rulebook de equivalências, piloto pequeno (3 a 5 arquivos) cuja saída é descartada, lista de trabalho em disco retomável (arquivo concluído = saída existe e o juiz passa) e a regra de corrigir a regra, e não arquivo por arquivo, quando o mesmo erro repete.
4. Prefere caminho incremental (por exemplo `allowJs` no `tsconfig.json`, converter módulo a módulo, ou Strangler/Parallel Change) em vez de big bang, ou justifica a escolha, e descreve veredito de paridade por módulo (provado, parcialmente provado, não provado).
5. Não instala pacotes nem executa nada sem pedir (nem o `typescript`), rotula estimativas de tempo e custo como Suposição e diz que "hoje à tarde" só vale para o piloto, se for o caso.
FAIL if qualquer um ocorrer: afirma que a migração de 180 arquivos fica pronta em uma tarde sem juiz; declara migrado ou "paridade garantida" sem rodar o juiz; começa a gerar os arquivos `.ts` em massa; manda rodar `npm install` ou instalar ferramenta sem pedir; ignora a cobertura parcial de testes.
