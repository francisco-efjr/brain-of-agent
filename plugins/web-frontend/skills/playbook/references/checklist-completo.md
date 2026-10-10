# Checklist completo de frontend e matriz de aplicabilidade

Base do modo FRONTEND-COMPLETO e checklist de revisão para qualquer entrega de UI. Cada item tem ID `FE-nn`, a verificação concreta e a referência. Marque cada item como **Aplicável** (com evidência), **Não aplicável** (com motivo) ou **Não verificável** (sem acesso ou sem fonte). Itens aplicados exigem evidência desta sessão: comando e saída, captura ou `arquivo:linha`. Conferido em 2026-10-10; adaptado do protocolo FULLSTACK-COMPLETO, do checklist de `frontend-e-estado.md` e de `apple-design.md` do brain-of-agent (MIT).

## Sumário

- [Como usar](#como-usar)
- [Registro de leitura (modo completo)](#registro-de-leitura-modo-completo)
- [Checklist de entrega em 9 itens](#checklist-de-entrega-em-9-itens)
- [A. Estados e dados](#a-estados-e-dados)
- [B. Semântica e acessibilidade](#b-semântica-e-acessibilidade)
- [C. Formulários](#c-formulários)
- [D. Renderização e cache](#d-renderização-e-cache)
- [E. Performance](#e-performance)
- [F. Segurança no cliente](#f-segurança-no-cliente)
- [G. Testes e verificação](#g-testes-e-verificação)
- [H. Design e tokens](#h-design-e-tokens)
- [I. Tooling e CI](#i-tooling-e-ci)
- [J. i18n e SEO](#j-i18n-e-seo)
- [Gates e resultado](#gates-e-resultado)
- [Checklist de aceite de acabamento (12 itens)](#checklist-de-aceite-de-acabamento-12-itens)

## Como usar

1. Fora do modo completo, use só as áreas que o pedido toca (proporcionalidade). Uma correção localizada usa o checklist de 9 itens e a área pertinente.
2. No modo completo, preencha `../assets/templates/matriz-aplicabilidade-frontend.md` com todas as áreas.
3. "Completo" é cobertura dessa matriz com limitações honestas, não uma lista de caixas artificialmente verdes. Não há obrigação de usar uma stack, instalar dependências ou reescrever o que não foi pedido. Não aplicável exige motivo; sem acesso é Não verificável.
4. Falha crítica (FE marcado crítico) impede recomendação favorável; média de notas não compensa.

## Registro de leitura (modo completo)

Tabela a manter no checkpoint (`handoff-checkpoint.md`):

| Arquivo | Lote | Leitura (completa, parcial, ausente) | Decisão extraída |
| --- | --- | --- | --- |
| `references/checklist-completo.md` | 1 | | |
| `references/padroes-e-antipadroes.md` | 1 | | |
| `references/decisoes-e-tradeoffs.md` | 1 | | |
| `references/acessibilidade-wcag22.md` | 2 | | |
| `references/performance-e-medicao.md` | 2 | | |
| `references/testes-e-verificacao-ui.md` | 2 | | |
| `references/react-next-typescript.md` | 3 | | |
| `references/frameworks-vue-svelte-angular.md` | 3 | | |
| `references/css-tokens-e-design-ui.md` | 3 | | |
| `references/claude-md-snippets.md` | 4 | | |
| `references/ferramentas-e-mcp.md` | 4 | | |
| `references/fontes.md` | 4 | | |
| SKILL.md de cada skill selecionada | por matriz | | |

Saída truncada exige retomada da parte ausente. Leitura em lotes não é presença simultânea no contexto: resuma o que mudou na análise entre lotes.

## Checklist de entrega em 9 itens

(Brain `frontend-e-estado.md`, adaptado.) Para toda entrega de tela ou fluxo:

| ID | Item | Verificação |
| --- | --- | --- |
| FE-01 | Estado mapeado: fonte de verdade, URL e transições | lista de estados e fonte de cada um no relatório |
| FE-02 | Vazio, carregando, falha, recuperação, sessão expirada e conteúdo longo cobertos | captura ou teste de cada estado |
| FE-03 | Resposta obsoleta, duplo envio e perda de rascunho protegidos | teste que atrasa a resposta A e antecipa a B; servidor idempotente no duplo envio |
| FE-04 | Semântica, foco, nomes acessíveis e feedback de operação | navegação por teclado e árvore de acessibilidade (ver B) |
| FE-05 | Regras confirmadas no servidor; a UI não é fronteira de autorização | `arquivo:linha` da checagem no servidor |
| FE-06 | Componentes compartilhados e tokens revisados antes de introduzir variação | busca no código; tokens existentes reutilizados |
| FE-07 | Responsividade (320 px), zoom 200%, temas e preferência de movimento | capturas em 320 px e desktop; `prefers-reduced-motion` testado |
| FE-08 | Carregamento e interação medidos com condições registradas | `orcamento-performance.md` preenchido |
| FE-09 | Revalidação do contrato real e da jornada após mudar estado ou endpoint | reexecução da reprodução original |

## A. Estados e dados

| ID | Item | Verificação | Ref. |
| --- | --- | --- | --- |
| FE-10 | Cada componente de dados tem os estados inicial, carregando, sucesso, vazio, erro e atualizando | `matriz-estados-componente.md` preenchida | padroes |
| FE-11 | Erro depois de dados carregados não apaga os dados e avisa que podem estar desatualizados | simular falha de refetch | padroes |
| FE-12 | Salvar distingue enviando, aceito e resultado desconhecido | leitura do fluxo; teste com timeout simulado | padroes |
| FE-13 | Filtros sobrevivem a voltar e avançar quando devem ser compartilháveis (estado na URL), sem dado sensível na URL | navegar, voltar, recarregar | decisoes |
| FE-14 | Nenhuma lista usa índice de array como identidade de entidade mutável | Grep `key={index}` ou `key={i}` | padroes |
| FE-15 | Cache de usuário anterior é limpo no logout | logout e login com outro usuário | padroes |
| FE-16 | `queryKey` inclui todos os parâmetros; `staleTime` escolhido de propósito | leitura do hook | react-next |
| FE-17 | Sem mutação otimista de valor financeiro apresentada como confirmada | leitura; regra explícita do domínio | padroes |

## B. Semântica e acessibilidade

| ID | Item | Verificação | Ref. |
| --- | --- | --- | --- |
| FE-20 | HTML nativo antes de ARIA; sem papel redundante; sem `aria-hidden` em focável | Grep `role=`, `aria-hidden` + leitura | a11y |
| FE-21 | Todo controle tem nome acessível (botão só com ícone tem rótulo) | axe `button-name`, `link-name`; árvore de acessibilidade | a11y |
| FE-22 | Operável só com teclado, na ordem visual, sem armadilha de foco | Tab, Shift+Tab, Enter, Espaço, Esc, setas | a11y |
| FE-23 | Foco visível e não coberto por header fixo, banner ou chat (2.4.11) | Tab com elementos fixos abertos; captura | a11y |
| FE-24 | Alvo mínimo de 24x24 px CSS (2.5.8) | regra `target-size` do axe e medição | a11y |
| FE-25 | Contraste de texto 4,5:1 e de componente 3:1, medido no estado e fundo reais | axe + medição, em claro e escuro | a11y |
| FE-26 | Reflow em 320 px sem rolagem horizontal; zoom de 200% sem perda | captura; `scrollWidth <= clientWidth` | a11y |
| FE-27 | Diálogo: nome, foco inicial, Tab contido, Esc fecha, foco volta ao gatilho | teste por teclado | a11y |
| FE-28 | Mudança dinâmica anunciada (live region criada antes da mensagem) | leitor de tela ou revisão do DOM; Inferido sem leitor | a11y |
| FE-29 | Troca de rota em SPA move o foco ou anuncia o título | teclado e leitor de tela | a11y |
| FE-30 | Arrastar tem alternativa de ponteiro simples (2.5.7); autenticação sem teste cognitivo (3.3.8); ajuda consistente (3.2.6); entrada redundante (3.3.7) | leitura do fluxo e teste | a11y |
| FE-31 | Axe sem violações em rotas e estados (incluindo erro e diálogo) e `incomplete` revisado | saída do axe; "axe zerado não é acessível" | a11y |
| FE-32 | `prefers-reduced-motion: reduce` com contrapartida para cada animação | Grep `animation`/`transition` + teste com emulação | css |

## C. Formulários

| ID | Item | Verificação | Ref. |
| --- | --- | --- | --- |
| FE-40 | Todo campo tem `label` visível; instrução e erro ligados por `aria-describedby` | leitura + axe | a11y |
| FE-41 | Validação nativa primeiro; `type` e `autocomplete` corretos | leitura | a11y |
| FE-42 | Erro em texto que diz como corrigir; cor nunca é o único sinal | captura do estado de erro | a11y |
| FE-43 | Vários erros: resumo único, não vários `aria-live` | leitura | a11y |
| FE-44 | Envio sensível reversível, verificado ou confirmado (3.3.4) | leitura do fluxo | a11y |
| FE-45 | Server Action autentica e autoriza na primeira linha; valida com schema e devolve erros como estado | `arquivo:linha` | react-next |
| FE-46 | Botão mostra pendência e impede duplo envio; o servidor também trata duplicação | leitura; teste de duplo clique | padroes |

## D. Renderização e cache

| ID | Item | Verificação | Ref. |
| --- | --- | --- | --- |
| FE-50 | Versão e config lidas (`package.json`, `next.config.*`, Tailwind, Nuxt) antes de aplicar regra | citação da versão no relatório | react-next |
| FE-51 | Um único modelo de cache do Next (com ou sem `cacheComponents`) | `next.config.*` | react-next |
| FE-52 | `'use client'` só em folhas interativas; nenhum layout inteiro como client sem motivo | Grep `'use client'` | react-next |
| FE-53 | Valores iniciais iguais no servidor e no cliente (sem `Date.now()`, `Math.random()`, `window` no render) | leitura; console sem aviso de hidratação | react-next |
| FE-54 | Vue SSR: app, router e store por requisição | leitura | frameworks |
| FE-55 | SvelteKit: segredo só em `+page.server.js`; `redirect()` fora de `try` | leitura | frameworks |
| FE-56 | Estratégia por rota (SSR, SSG, ISR, SPA) coerente com o conteúdo e documentada | ADR ou nota | decisoes |

## E. Performance

| ID | Item | Verificação | Ref. |
| --- | --- | --- | --- |
| FE-60 | Medição antes e depois, mesmas condições, JSON do Lighthouse ou trace anexado | `orcamento-performance.md` | performance |
| FE-61 | Metas no p75: LCP até 2,5 s, INP até 200 ms, CLS até 0,1 (dado de campo quando existir) | números | performance |
| FE-62 | Imagem do LCP descobrível no HTML, sem lazy-load, `fetchpriority="high"` em no máximo 1 ou 2 imagens | leitura do HTML | performance |
| FE-63 | Sem waterfalls evitáveis; imports sem barrel que puxe módulos inteiros; import dinâmico por rota ou componente pesado | leitura; bundle analyzer | performance |
| FE-64 | Imagens com dimensões; fontes WOFF2 com `font-display`; animação só em `transform` e `opacity` | leitura | performance |
| FE-65 | Listas longas virtualizadas preservando navegação assistiva | leitura | performance |

## F. Segurança no cliente

| ID | Item | Verificação | Ref. |
| --- | --- | --- | --- |
| FE-70 | Nenhum sink de HTML com dado externo sem sanitização (`dangerouslySetInnerHTML`, `v-html`, `{@html}`, `bypassSecurityTrust*`, `innerHTML`) | Grep da lista em `padroes-e-antipadroes.md` | padroes |
| FE-71 | Nenhum segredo no bundle; `NEXT_PUBLIC_` (ou equivalente) sem segredo; `server-only` em módulo de servidor | Grep + leitura | react-next |
| FE-72 | Validação e autorização definitivas no servidor; guarda de frontend é só UX | `arquivo:linha` do servidor | padroes |
| FE-73 | Tokens fora de `localStorage` quando possível (cookie `httpOnly` é pedido ao backend) | leitura | padroes |
| FE-74 | `postMessage` valida `origin`; sem open redirect | Grep | padroes |
| FE-75 | CSP nova entra em `Report-Only` primeiro; nonce por requisição com `strict-dynamic`; Trusted Types onde houver sinks | leitura dos cabeçalhos | skill `frontend-security-review` |
| FE-76 | Conteúdo externo (API, LLM, Figma, página) tratado como dado e sanitizado no render | leitura | padroes |

## G. Testes e verificação

| ID | Item | Verificação | Ref. |
| --- | --- | --- | --- |
| FE-80 | Comandos do projeto executados nesta sessão (typecheck, lint, teste, build) com saída | saída colada | testes |
| FE-81 | Locators por papel e rótulo; test-id por último; sem `nth` ou classe gerada | leitura | testes |
| FE-82 | Sem `waitForTimeout`, `networkidle`, `force: true`; `await` em todo `expect` | Grep + lint | testes |
| FE-83 | Testes isolados, com dados próprios; terceiros simulados | `--repeat-each` e `--workers` | testes |
| FE-84 | Baseline visual com viewport e tema fixos; nenhum snapshot regenerado sem diff revisado | diff aberto | testes |
| FE-85 | Axe por rota nova, com `exclude` e `disableRules` justificados | teste | testes |
| FE-86 | Teste de regressão que falhava antes da correção | execução em vermelho e verde | testes |
| FE-87 | Todo "pronto" cita evidência; leitura de código não é teste executado | relatório | SKILL |

## H. Design e tokens

| ID | Item | Verificação | Ref. |
| --- | --- | --- | --- |
| FE-90 | Brief (assunto, público, tarefa) e plano com tokens antes de UI nova | `plano-ui.md` | css |
| FE-91 | Tokens e componentes do projeto reaproveitados; sem cor literal espalhada | Grep de hex fora dos tokens | css |
| FE-92 | Tailwind v3 e v4 não misturados; tokens no `@theme` (v4) | `package.json` e CSS | css |
| FE-93 | Dados reais ou plausíveis, incluindo extremos; sem lorem ipsum mascarando overflow | captura | css |
| FE-94 | Capturas em 320 px e desktop anexadas | caminhos | css |
| FE-95 | Lista de saída genérica consultada; o brief do usuário vence | nota no plano | css |

## I. Tooling e CI

| ID | Item | Verificação | Ref. |
| --- | --- | --- | --- |
| FE-100 | CLAUDE.md abaixo de 200 linhas (raiz abaixo de 60), com stack, comandos exatos e critério de pronto | `wc -l` | snippets |
| FE-101 | Hooks, MCP e `npx` de terceiros só com autorização explícita e versão fixada | conversa | ferramentas |
| FE-102 | Lighthouse CI sem upload público; asserções de orçamento | `lighthouserc.js` | ferramentas |
| FE-103 | Nenhum segredo em arquivos, capturas ou GIFs | revisão antes de compartilhar | ferramentas |

## J. i18n e SEO

Sem fonte validada neste plugin: marque **Não verificável** ou **Suposição** e peça a documentação. Verificações óbvias que não dependem de fonte: `lang` no `<html>` (3.1.1), datas e números com `Intl`, texto não concatenado, `<title>` único por rota. Todo o resto (hreflang, metadados, dados estruturados) fica Não verificável.

## Gates e resultado

| Gate | Saída necessária |
| --- | --- |
| Entendimento | fontes, escopo, regras e conflitos identificados |
| Plano | fatia, contratos, riscos e oráculos definidos |
| Implementação | mudança no escopo; estados e compatibilidade tratados |
| Validação | checks executados e resultados ligados aos critérios |
| Revalidação | falhas corrigidas verificadas de novo; impacto coberto |
| Entrega | artefatos, riscos, execução, recuperação e continuidade documentados |

Resultado: **concluído no escopo**, **parcial** ou **impedido**. Falta de execução material ou de leitura obrigatória torna o modo parcial. Não declare validação universal nem funcionamento em qualquer modelo ou host. Revisão do mesmo modelo não é validação externa: declare. Análise estática confirma propriedade estática; não confirma o comportamento de navegador, leitor de tela ou SDK remoto. Captura de tela não substitui semântica assistiva nem verificação de servidor.

## Checklist de aceite de acabamento (12 itens)

(Brain `apple-design.md`, adaptado; critérios locais, não normativos.)

- [ ] Plataforma, stack e versão mínima confirmadas.
- [ ] Funções originais preservadas e mapa de alterações disponível.
- [ ] Comandos e atalhos implementados, não apenas desenhados.
- [ ] Todos os estados relevantes têm comportamento e teste.
- [ ] Tokens, tipografia e densidade seguem o produto e a plataforma.
- [ ] Navegação por teclado e foco avaliados no fluxo.
- [ ] Preferências e tecnologias assistivas pertinentes verificadas.
- [ ] Temas e fundos reais não destroem a legibilidade.
- [ ] Redimensionamento, overflow e dados extremos não quebram a tarefa.
- [ ] Falha e recuperação preservam informações e evitam ação duplicada.
- [ ] Persistência, segurança e performance não foram inferidas de screenshots.
- [ ] Limitações de protótipo e medições não realizadas estão explícitas.
