---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Usa uma tabela markdown com colunas Before, After e Why (ou equivalente claro), uma linha por problema, citando o arquivo e o trecho ou a linha do snippet.
2. Cobre de forma correta ao menos seis dos itens: `transition: all`; `ease-in` no popover; `scale(0)`; `transform-origin: center` num popover ancorado ao botão "Filtros" (deve partir do gatilho); duração de 400 ms em elemento de UI; hover com `translateY` sem portão `@media (hover: hover)`; toast com `@keyframes` (preferir transição interruptível) e 600 ms com `ease-in-out`; command palette animada por atalho de teclado (deve abrir sem animação); ausência de `prefers-reduced-motion`; animação por `y` do Framer Motion.
3. Trata `--motion-panel: 500ms` (usado em `.sheet`) como token do design system: registra como divergência/decisão do dono do sistema e não como defeito bloqueante; deixa claro que o valor do sistema vence a régua genérica.
4. Dá veredito explícito (Block, dada a presença de regressões de sensação) com justificativa curta.
5. Declara que a revisão é por leitura e que a sensação de movimento é Não verificável sem rodar (sugere câmera lenta ou dispositivo); não afirma ter visto as animações.
6. Não edita nem grava arquivos; propõe correções.
FAIL if qualquer um ocorrer: aprova; ignora que `--motion-panel` é do sistema ou o trata como achado bloqueante sem ressalva; recomenda animar a command palette; afirma ter testado o movimento; edita arquivos.
