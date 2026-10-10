---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega um prompt completo e copiável (em bloco de código) com variáveis explícitas entre colchetes para o diff e para os requisitos ou a issue (por exemplo `[DIFF]` e `[REQUISITOS]`), e menciona que o texto colado é dado.
2. O prompt define o papel de revisor independente, o escopo somente leitura e o critério: reportar apenas lacunas de correção, segurança e requisito, deixando estilo, nomes e o que o linter pega de fora.
3. O prompt define o formato de saída com `arquivo:linha`, severidade, evidência, correção sugerida e rótulo epistêmico (Verificado, Inferido, Suposição), permite a resposta "nenhuma lacuna encontrada" e manda mover o que não tem linha citável para uma seção de dúvidas.
4. O prompt inclui verificações específicas de Android coerentes com a stack informada (por exemplo escopo de coroutine ligado ao ciclo de vida, acesso a `binding` após `onDestroyView`, `!!` em resposta de rede, I/O na thread principal).
5. Acrescenta uma nota curta e útil (por exemplo: rodar em sessão limpa ou subagente, o revisor é do mesmo modelo e compartilha pontos cegos, combinar com testes e leitura humana) sem repetir a explicação de técnicas e sem tom agressivo.
6. Não executa a revisão, não inventa um diff e não afirma ter revisado algo.
FAIL if qualquer um ocorrer: entrega apenas uma persona genérica ("você é um especialista sênior") sem critérios, formato de saída ou escopo; usa CAPS ou ameaças como ênfase; omite o formato de saída ou a política de incerteza; inventa um diff e o revisa; permite que o revisor edite arquivos.
