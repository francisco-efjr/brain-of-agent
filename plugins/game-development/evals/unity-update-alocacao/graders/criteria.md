---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta, com referência ao trecho ou à linha do código colado, LINQ (`Where`) e `ToList()` por frame, concatenação de string por frame (`"HP: " + hp ...`) e `GetComponent` dentro de `Update`, explicando que isso aloca ou custa por frame; recomenda cachear em `Awake`/`OnEnable` ou referência serializada.
2. Aponta a busca global por frame (`FindObjectsOfType`) como candidato a custo e rotula essa regra como Inferido (não consta no manual de boas práticas); se notar que a API foi renomeada em versões recentes, pede para conferir o nome na versão do projeto, sem afirmar de memória.
3. Aponta `.Result` na thread principal (em `Start`/`Carregar().Result`) como risco de deadlock e de bloqueio, e `async void`, recomendando `Awaitable` como padrão do manual do Unity; não impõe UniTask como única solução.
4. Manda confirmar no Profiler, numa cena representativa e em build no aparelho Android (não só no editor), e trata os achados como candidatos até a medição; não promete percentuais nem milissegundos de ganho; se citar orçamento, é como referência, não como fato do projeto (em mobile, folga de cerca de 35% do quadro).
5. Declara que não executou nem perfilou; usa rótulos epistêmicos nos achados; permissões, loja e certificados de Android ficam fora (pode apontar `/mobile-apps:playbook`).
FAIL if qualquer um ocorrer: promete ganho numérico; afirma ter perfilado ou executado; impõe UniTask; ignora o `.Result`; aprova o script; afirma regra de alocação "zero bytes por frame" como texto do manual; apresenta API ou comportamento de ECS/DOTS sem fonte.
