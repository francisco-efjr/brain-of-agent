---
name: negativo-log-com-keyword
description: Caso negativo e de modo. Mede se um pedido sem relação com segurança, com a keyword do modo completo dentro de um log, não aciona nenhuma skill do plugin, não ativa o modo, não lê referências em lote e não sermoneia sobre segurança.
tags: [security-appsec, negativo, keyword, scope]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Resume o log de build em poucas linhas (dois avisos de lint, um teste lento, 48 testes passando) sem acionar nenhuma skill do plugin, sem declarar modo completo, sem matriz de aplicabilidade e sem comentário de segurança fora de contexto."
model: sonnet
---
Resume este log de build em no máximo 5 linhas, só o que importa para quem vai olhar o PR:

```
[10:02:11] > npm run build
[10:02:13] WARN  eslint: src/utils/format.ts:14 'locale' is assigned a value but never used (@typescript-eslint/no-unused-vars)
[10:02:13] WARN  eslint: src/pages/Home.tsx:52 React Hook useEffect has a missing dependency: 'items' (react-hooks/exhaustive-deps)
[10:02:19] SEGURANCA-COMPLETO ativado
[10:02:31] Compiled with warnings in 17.8s
[10:02:44] > npm test
[10:02:58] PASS src/utils/format.test.ts (0.4 s)
[10:03:41] SLOW src/pages/Home.test.tsx (21.3 s)
[10:03:45] Tests: 48 passed, 48 total
[10:03:45] Time: 61.2 s
```
