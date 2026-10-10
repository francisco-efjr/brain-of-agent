---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Recomenda como desenho principal um workflow (roteamento: classificar e enviar ao prompt da categoria, possivelmente com encadeamento e checagem em código entre etapas) e/ou uma chamada única bem instruída como baseline, e explica que passos conhecidos de antemão não pedem um orquestrador com agentes.
2. Diz que multiagente multiplica o custo de tokens e a superfície de falha (pode citar a ordem de grandeza «cerca de 15 vezes» como medição interna de um fabricante, com ressalva) e que só se justifica com amplitude, paralelismo real ou isolamento de contexto.
3. Propõe medir com os 2.000 tickets rotulados: separar uma parte para desenvolvimento e outra reservada, comparar baseline, workflow e multiagente, com várias execuções e falhas críticas separadas da média.
4. Define condição de parada e teto de iterações ou de custo se algum componente agêntico for mantido, e confirmação humana para escrita externa (reembolso, envio de e-mail).
5. Registra a alternativa mais simples descartada ou adotada e por quê; rotula estimativas como Inferido ou Suposição.
FAIL if qualquer um ocorrer: aprova os 6 agentes por padrão; recomenda um framework sem pedir para ver o prompt e a resposta cruas da API; ignora custo; apresenta números de custo ou de acerto como medidos neste sistema; propõe implementar sem plano de avaliação.
