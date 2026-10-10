# BUILD-REPORT de qualidade: web-frontend

Data: 2026-10-10. Papel: validador de qualidade de prompt e de conteúdo técnico, contexto de validação. Escopo: todo o plugin `plugins/web-frontend` (README, playbook e referências, 8 skills de tarefa, skill `prompts` e biblioteca, 5 agentes, 10 evals).

Independência: este validador é um modelo Claude (Opus 5.5). Os construtores eram outro modelo, mas da mesma família Anthropic; a revisão é independente do autor, não externa à família. As notas são leitura adversarial, não medição: nenhum eval foi executado.

Rubrica: `docs/foundation/prompt-quality-rubric.md` (D1 a D12, 0 a 5 cada, nota = média x 20). Fonte de verdade técnica: `VALIDATED.md` e documentação oficial reconferida nesta rodada (URLs abaixo).

## 1. Notas por arquivo

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 92 | 95 | Fronteiras: regra para slug de segmento ainda não publicado ou não instalado (dizer em uma linha, entregar o pedido de integração, não inventar o conteúdo vizinho). D11 sobe. |
| `skills/design-ui/SKILL.md` | 92 | 92 | Sem mudança. Fases com critério de saída, exemplo de brief e de "mudei X porque Y", gate, verificação em tabela. |
| `skills/verify-ui/SKILL.md` | 93 | 93 | Sem mudança. Autorização por comando, meio de navegador em ordem, saída de exemplo, "Não verificado" explícito. |
| `skills/component-review/SKILL.md` (+ `references/exemplos-react.md`) | 90 | 92 | `ref` como prop no React 19 passou de Não verificado a Verificado (react.dev, `forwardRef`). |
| `skills/a11y-review/SKILL.md` | 92 | 92 | Sem mudança. Nove critérios novos da WCAG 2.2 conferidos (números e níveis corretos); 4.1.1 removido tratado certo. |
| `skills/perf-audit/SKILL.md` (+ `references/exemplo-diagnostico.md`) | 86 | 93 | `disallowed-tools: Write, Edit, NotebookEdit` (skill só lê); passo 8 deixava implícito gravar o template: agora a tabela vai no relatório e gravar só a pedido; `next/image`: `priority` descontinuada no Next 16 em favor de `preload`, com a recomendação da doc 16.4.0 (`loading="eager"` ou `fetchPriority="high"`). |
| `skills/e2e-tests/SKILL.md` | 92 | 92 | Sem mudança. Limite de 3/n conferido (30 execuções sem falha ~ 10%; 150 ~ 2%). |
| `skills/frontend-security-review/SKILL.md` | 90 | 95 | `disallowed-tools: Write, Edit, NotebookEdit`, com a nota de que a restrição cai na próxima mensagem do usuário (doc de skills). |
| `skills/forms-and-data/SKILL.md` | 90 | 93 | Gotcha nova: `proxy.ts` (antigo `middleware.ts`, renomeado no Next 16) não substitui autorização dentro da Server Action, porque o `matcher` pode pular a action (doc `proxy.js` 16.4.0). |
| `skills/prompts/SKILL.md` | 92 | 92 | Sem mudança. Gatilhos PT/EN, quando não usar, processo com Grep por seção, exemplo de entrega, `disallowed-tools`. |
| `skills/prompts/references/*` (amostra de 12: PR-01, 06, 07, 14, 17, 22, 23, 25, 34, 36, 37, 38) | 90 | 90 | Sem mudança. Todos com variáveis, dados em tags declarados como dado, formato de saída, política de incerteza, fonte com classe e forma D/A. Ferramentas de escrita do Figma conferidas contra V-60. |
| `skills/playbook/references/react-next-typescript.md` | 88 | 90 | `forwardRef` e `ref` como prop: Verificado com URL e data. |
| `agents/frontend-code-reviewer.md` | 92 | 92 | Sem mudança. `tools: Read, Grep, Glob`, entrega sem gravar, filtro de confiança, conteúdo suspeito. |
| `agents/frontend-a11y-reviewer.md` | 93 | 93 | Sem mudança. |
| `agents/frontend-perf-reviewer.md` | 86 | 93 | Mesmo erro de `priority` do `next/image` corrigido com a regra por versão (Next 16 ou superior: `preload` / `loading="eager"` / `fetchPriority`; 15 ou anterior: `priority`). |
| `agents/frontend-security-auditor.md` | 90 | 93 | `middleware` atualizado para `proxy.ts` (Next 16) com `middleware.ts` até o 15; nota de que `proxy` não substitui auth na Server Action. |
| `agents/ui-evaluator.md` | 90 | 90 | Sem mudança. Custo US$ 9 contra US$ 200 conferido em VALIDATED (harness da Anthropic, modelos 4.5 e 4.6). |
| `evals/` (10 casos, README, graders) | 91 | 91 | Sem mudança. PASS/FAIL observáveis em todos; caso negativo com `min: 0`/`max: 0` em Skill e Read; graders `no-exec`, `no-write`, `no-edit`; `runs: 3`; `designed_not_executed` declarado. |
| `README.md` | 90 | 90 | Sem mudança. Componentes, instalação, 8 exemplos, keyword, fontes, créditos, limitações. |

Média antes (19 linhas): 90,5. Média depois: 92,2. Mínimo depois: 90. Nenhum arquivo abaixo de 80; nenhum critério de reprovação automática encontrado.

## 2. Fidelidade técnica conferida nesta rodada

| Afirmação | Situação | Fonte |
| --- | --- | --- |
| `priority` do `next/image` | Errada para a versão-alvo (16.4): descontinuada no Next 16 em favor de `preload`; doc recomenda `loading="eager"` ou `fetchPriority="high"` na maioria dos casos. Corrigida em 2 arquivos | https://nextjs.org/docs/app/api-reference/components/image (versão 16.4.0, 2026-09-28) |
| `middleware` no Next | Renomeado para `proxy` no v16.0.0; Server Functions dependem de checagem própria | https://nextjs.org/docs/app/api-reference/file-conventions/proxy (16.4.0) |
| `ref` como prop, `forwardRef` | Verificado: React 19 dispensa `forwardRef`; será descontinuado | https://react.dev/reference/react/forwardRef |
| `disallowed-tools` em SKILL.md | Campo existe; remove ferramentas enquanto a skill está ativa; cai na próxima mensagem do usuário. `allowed-tools` só pré-aprova | https://code.claude.com/docs/en/skills |
| Limiares de Core Web Vitals, orçamento das subpartes do LCP, LoAF no Chrome 123 | Coerentes com V-15 e V-18 | VALIDATED.md |
| `staleTime: 'static'`, 3 tentativas padrão do TanStack Query | Coerentes com V-48 | VALIDATED.md |
| CSP estrita, `report-to`/`report-uri`, Trusted Types "Baseline 2026" | Coerentes com V-59 | VALIDATED.md |
| `lhci@0.15.x`, upload público do LHCI, extensão do Lighthouse sem páginas locais | Coerentes com V-57 | VALIDATED.md |
| Nove critérios novos da WCAG 2.2 e níveis | Corretos | VALIDATED.md (V-16) |
| `useActionState` devolve `[state, formAction, isPending]`; SvelteKit 2.16 para `PageProps` | Coerentes com V-46 e V-50 | VALIDATED.md |

## 3. Direitos autorais e segurança

- Nenhum trecho literal longo de terceiros encontrado; prompts e skills declaram forma D (redação própria) ou A (conteúdo do usuário, MIT). Créditos de Apache-2.0 (Anthropic `frontend-design`, `impeccable`), MIT (gstack, Vercel, awesome-copilot) presentes no README e em `fontes.md`.
- Nenhum segredo; exemplos usam `NEXT_PUBLIC_API_SECRET` apenas como antipadrão e o caso de injeção usa domínio reservado `example.test`.
- Nenhum hook, `.mcp.json`, `.lsp.json` ou `bin/` ativo. `--dangerously-skip-permissions` aparece só como risco (sandbox e repositório confiável), em `ferramentas-e-mcp.md` e em `prompts/SKILL.md`.
- Os 5 agentes têm `tools: Read, Grep, Glob` (sem Bash, Write ou Edit). Skills de auditoria declaram somente leitura; `perf-audit`, `frontend-security-review` e `prompts` agora também têm `disallowed-tools`.
- Instalação de pacote, execução de testes, atualização de baseline, escrita no Figma, push e deploy exigem autorização no chat em todas as skills que os citam.

## 4. Verificação final

| Comando | Resultado |
| --- | --- |
| `python tools/verify_plugin.py plugins/web-frontend` | Verificado: `RESULT: PASS` (10 skills, 5 agentes, 10 evals, 91 arquivos) |
| `claude.exe plugin validate plugins/web-frontend` | Verificado: `Validation passed` |

## 5. Pendências

1. Evals não executados (`designed_not_executed`): `claude plugin eval` exige Claude Code 2.1.269 ou superior; a CLI local registrada é 2.1.128. Não verificável nesta rodada. As notas acima são de leitura.
2. A skill `prompts` e os 5 agentes não têm caso de eval próprio (o README dos evals já lista os candidatos: delegação ao `frontend-code-reviewer` com diff e `ui-evaluator` sem captura). O blueprint limita a 6 a 10 casos; incluir exige trocar um caso existente. Decisão do usuário.
3. Fronteiras do playbook citam 13 segmentos previstos em `docs/foundation/segments.json` que ainda não estão em `plugins/`. Mantidos (são o plano da fábrica); o playbook agora diz o que fazer quando o plugin vizinho não existe. Revalidar quando os segmentos forem construídos.
4. `commands/design-brief.md` (opcional no SYNTHESIS) segue ausente; não é exigido.
5. A pendência estrutural 2 (`/playwright:v` e `/localhost:3000`) foi conferida: é a tag de imagem Docker `mcr.microsoft.com/playwright:v<VERSÃO>-noble` e URL local, não referência a plugin. Resolvida sem alteração.
6. Lacunas técnicas já declaradas no README (Signal Forms, hidratação sem página primária, CrUX, i18n e SEO) continuam Não verificadas; não foram pesquisadas nesta rodada.
