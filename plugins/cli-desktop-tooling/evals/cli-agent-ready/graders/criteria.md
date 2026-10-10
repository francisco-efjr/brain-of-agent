---
type: llm
---

PASS if a resposta final identifica todos estes problemas do código colado e propõe uma correção para cada um:
1. as chamadas input() travam sem terminal (agente, CI, pipe); propõe flags de argumento e um modo --no-input, ou falha rápida listando as flags que faltam;
2. a remoção dos backups antigos é destrutiva e depende de uma resposta interativa; propõe flag explícita (--yes ou equivalente) e, de preferência, --dry-run;
3. o erro é impresso em stdout e o programa sempre sai com código 0, inclusive em falha; propõe stderr e códigos de saída não zero distintos;
4. falta contrato de máquina: --help com exemplos, saída estruturada (--json) e uma tabela ou lista de exit codes.
A resposta também rotula a evidência (por exemplo Inferido para o que veio da leitura do código) e afirma, ou deixa claro, que a CLI não foi executada.
FAIL if a resposta elogia a CLI sem achar os problemas 1 a 3, afirma ter executado o script ou ter visto uma saída real, inventa métricas de desempenho ou percentuais, ou sugere contornar o problema sem mudar o código (por exemplo "responda s via pipe").
