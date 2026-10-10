# Sistemas, embarcados e IoT — consolidado das lentes authoritative, github e community — VALIDADO

> Atualização 2026-10-10: o ADENDO no fim deste arquivo valida o complemento `gapfill.md` (itens V-30 a V-63, estatísticas, mapa de cobertura e lacunas atualizados). Total acumulado: 63 V-itens (V-01 a V-63) após a rodada final; veredito final: pass_with_gaps.

Data: 2026-10-10 · Validador: claude-sonnet-5-5 (modelo diferente do pesquisador, claude-haiku-5-5; a independência vem do modelo distinto e de re-leitura das fontes com ferramentas, não de cortesia) · Itens recebidos: 63 · URLs/endpoints re-verificados: cerca de 65 (única limitação: o limite de WebSearch do turno estava esgotado, então não houve busca nova; os gaps abaixo viram trabalho de nova rodada).

Rótulos: Verificado (lido por mim nesta execução) · Inferido · Suposição · Não verificável.

## Estatísticas por lente

| Lente | Recebidos | Aprovados (inclui fundidos) | Rebaixados | Rejeitados | Re-verificados (itens) | Cobertura de re-verificação |
| --- | --- | --- | --- | --- | --- | --- |
| authoritative | 24 | 21 | 3 (A-10, A-19, A-24) | 0 | 24 de 24 (A-15 só pela página MathWorks) | 100% |
| github | 16 | 12 | 4 (G-04, G-05, G-08, G-10) | 0 | 16 de 16 (metadados de 4 repositórios ficaram sem API: 403) | 100% |
| community | 23 | 14 | 7 (C-03, C-05, C-09, C-10, C-11, C-12, C-22) | 2 (C-13, C-23) | 21 de 23 (C-05 e C-10 só em parte) | 91% |
| **Total** | **63** | **47** | **14** | **2** | **61 de 63** | **97%** (mínimo exigido: 40%; todos os itens classe A re-verificados) |

Os 47 itens aprovados se fundem em **29 itens validados (V-01 a V-29)** após deduplicação entre lentes (13 classe A, 11 classe B, 5 classe C). V-24 (MCUboot) foi adicionado pelo validador para cobrir a lacuna de OTA; não conta nos 63 recebidos.

Verificação de classe A: todas as fontes Anthropic oficiais (best-practices, hooks-guide, plugins-reference, code-intelligence, harnesses, compilador C, sandboxing) foram lidas e as afirmações conferidas uma a uma. Todos os pontos principais conferem. Metadados GitHub conferidos por API: anthropics/skills 180.246★, push 2026-10-09, licença nula; PatrickJS/awesome-cursorrules 40.891★, CC0-1.0, push 2026-05-30; zhinkgit/embeddedskills 734★, MIT, push 2026-09-03; agodianel/esp32-claude-workbench 79★, MIT, push 2026-03-31; im-hashim/automotive 199★, MIT; adamlipecz 12★, sem licença; github/awesome-copilot 39.881★, MIT; garrytan/gstack 135.780★, MIT. Via página HTML: claude-plugins-official 37,6 mil★ e Apache-2.0; SensorsIot 188★ MIT; atillab1 5★ MIT; stm32-mcp 25★ MIT; jko-claude-plugins 11★ MIT; embedded-systems-architect 5★ MIT. API recusou (403) para claude-plugins-official, mcuboot e outros; nesses casos a data de push ficou Não verificável.

## Correções adversariais importantes (o que os pesquisadores erraram ou exageraram)

1. **R-community-06 (Ronacher):** atribui à fonte "timeout em tudo" e "exit code claro". O post **não** trata de timeouts nem de códigos de saída (Verificado). Diz que travar é pior que falhar, pede ferramenta rápida e silenciosa, pidfile, log em arquivo e botões de verbosidade. Timeout e exit code são Suposição de design da fábrica.
2. **R-community-07 (Bitcraze):** o "padrão de CLI" `daemon start|stop`, `console --since N`, `param get|set` e "máximo de linhas por comando" é invenção do pesquisador. O post lista capacidades (flash, reset, console, parâmetros, variáveis de log) sem sintaxe de CLI (Verificado). Marcado Suposição.
3. **R-github-02 vs R-github-07 ("conflito de heap"):** o workbench diz para usar heap em buffers acima de 512 bytes e evitar buffers grandes na pilha. Não é um "limite de heap"; é regra de pilha versus heap, coerente em ESP-IDF, que usa heap por padrão. A regra "sem heap" do STM32 vale para bare metal sem permissão do projeto. Não há conflito real; há contexto diferente.
4. **R-community-02 / R-github-03 (ESP32):** o workbench lista como especiais os GPIO 0, 1, 2, 3, 12, 15, 6–11 e 34–39. A documentação ESP-IDF (Verificado) diz que GPIO 6–11 **e 16–17** costumam estar ligados a flash/PSRAM do módulo; a doc remete ao datasheet para os pinos de strapping (a lista de strapping do ESP32 clássico inclui também o GPIO 5, Inferido do conhecimento do validador; conferir no datasheet). "320 KB de SRAM" não aparece na doc ESP-IDF consultada; o ESP32 clássico tem 520 KB de SRAM (Inferido), dos quais só parte é heap de dados. Mínimos de pilha 2048 e 4096 bytes são números do autor do workbench, não do ESP-IDF.
5. **R-community-20 (jlink `operation_mode`):** o exemplo de config traz o valor **1 (executar direto)**; o padrão seguro 3 (confirmar) é recomendação nossa, não da fonte. Flash, write-mem e reset são classificados como alto risco (Verificado). Workflow `build-flash` encadeado sem gate (Verificado).
6. **R-community-04 (Embedder):** o thread existe (113 pts, 52 comentários, 2025-08-15, Verificado) e mostra alucinação de registradores/HAL e datasheet como contexto; um comentarista postou o prompt do agente, que exige citação. A preocupação com NDA/retenção é de comentaristas e os fundadores responderam; **não repetir como fato sobre a empresa**.
7. **R-authoritative-13:** "critical sections curtas" não é conselho literal do livro; ele só nota que aumentam latência e jitter (Verificado). Recomendação mantida como Inferido.
8. **R-authoritative-17 (FreeRTOS):** a documentação oficial no site não pôde ser lida (páginas truncadas ou 404). Conferi a semântica de `pxHigherPriorityTaskWoken` no fonte oficial `FreeRTOS-Kernel/include/semphr.h` (MIT, Amazon): a função define o flag quando desbloqueia tarefa de prioridade maior e o ISR deve pedir troca de contexto antes de sair; a macro de yield é **específica de porta** (Verificado). Regra de prioridade `configMAX_SYSCALL_INTERRUPT_PRIORITY` é Inferido (conhecimento do validador; conferir na documentação da porta).
9. **R-authoritative-20 (Snyk):** as estatísticas (36% e 13%) têm link para a pesquisa ToxicSkills da própria Snyk; o pesquisador disse "sem link". São dados do próprio vendor, sem metodologia na página. Das sete skills de embarcados citadas, uma tem 8.055★ (ARM Cortex Expert), duas têm 459★, o resto 0–2.
10. **R-authoritative-11:** a versão lida era v4.4.8; reconferi na versão atual (latest) e as regras citadas se mantêm (assert só para erro interno irrecuperável, sem efeito colateral em assert, `(void)`, `#pragma once`, 4 espaços, 120 colunas, astyle, `s_` em estáticas). Código desativado só com comentário explicando.
11. **R-authoritative-09 (Zephyr):** o item cita regras sem número, o que é seguro. Ao conferir: a página se descreve como subconjunto de MISRA-C 2012; Dir 4.12 (sem alocação dinâmica) está na lista, mas as regras adicionais A.4/A.5 permitem `malloc` e correlatos no kernel e C11 no código; a página não reconcilia (Verificado). O "Rule 8.7" não existe na página (é 8.8) e "sem código comentado" é Dir 4.4 (não Rule 4.4). Não citar número de regra sem reler a versão.
12. **R-authoritative-14 (CERT):** o wiki antigo redireciona (301) para `cmu-sei.github.io/secure-coding-standards/...`. SIG31-C reconferida na URL nova (exceções: `volatile sig_atomic_t` e atômicos lock-free). DCL22-C não reconferida.
13. **R-community-12/13:** `cpp-language-service-tools` depende de ferramentas específicas (`*_CppTools`) e tem contradições internas (Verificado); `cmake-vcpkg` não trata de cross-compilação nem embarcado (Verificado). Rebaixado/rejeitado.
14. **R-authoritative-21 e R-github-13:** a correção dos pesquisadores ao atlas está certa: Bitcraze não fala de autorização para gravar, datasheet, exit codes nem timeouts (Verificado).

## Itens aprovados

### V-01 — CLAUDE.md curto, verificação e revisão adversarial (origem R-authoritative-01, R-community-17) — Classe A (9)
- **Lente:** authoritative + community · **Tipo:** claude-md-rule · checklist · workflow
- **Fonte:** https://code.claude.com/docs/en/best-practices · **Autor/Org:** Anthropic · **Sinais:** documentação oficial, existe; licença não aplicável (destilar)
- **Para que serve no segmento:** estrutura do CLAUDE.md de firmware, ciclo de verificação e revisão de diff por subagente.
- **Técnicas-chave (Verificado):** teste de corte por linha ("remover esta linha faria o Claude errar?"); incluir comandos de build/flash, gotchas de hardware, variáveis de ambiente; excluir o que se lê no código; dar um check com passa/falha e pedir evidência (saída de teste, comando executado); explorar, planejar, implementar, commitar, e pular o plano se o diff cabe em uma frase; conhecimento ocasional vai para skills, regra sem exceção vai para hook; subagente para investigação; depois de duas correções falhas, `/clear` e prompt melhor; revisor adversarial em contexto novo que relata lacunas de requisito, não estilo (a página avisa que revisor "acha" algo mesmo quando o trabalho está bom, então pedir só lacunas que afetam correção).
- **Conteúdo reutilizável (redação própria):**
  - Regra de CLAUDE.md: "Build: `<comando>`. Teste no host: `<comando>`. Gravar na placa, apagar flash e acionar atuadores: somente com confirmação explícita do usuário na conversa."
  - Prompt de revisão: "Revise o diff contra PLAN.md em contexto novo. Verifique cada requisito e cada caso de borda listado, e se algo fora do escopo mudou. Relate apenas lacunas que afetam correção ou requisitos; marque o resto como opcional."
- **Ressalvas:** texto geral; a página se declara ponto de partida e muda com o tempo.
- **Verificação:** página lida na íntegra nesta execução; todas as oito afirmações conferem.
- **Prompt-score:** não se aplica à fonte (documentação). Os dois trechos reescritos acima: 84 (D1 4, D2 4, D3 5, D4 4, D5 2, D6 4, D7 5, D8 5, D9 5, D10 5, D11 3, D12 4).

### V-02 — Harness de longa duração: initializer, lista JSON e protocolo de sessão (origem R-authoritative-02, R-github-12, R-community-15) — Classe A (9)
- **Lente:** authoritative + github + community · **Tipo:** workflow · pattern
- **Fonte:** https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents · Justin Young, Anthropic, 26 nov. 2025 (Verificado)
- **Sinais:** publicação oficial; licença não aplicável.
- **Para que serve:** bring-up de placa, migração de HAL, port de MCU, suítes de teste que levam várias sessões.
- **Técnicas-chave (Verificado):** agente inicializador e agente de codificação; lista de funcionalidades em JSON em que o agente só altera o campo de status (`passes`), porque o modelo altera menos JSON que Markdown; uma funcionalidade por sessão; arquivo de progresso + git; `init.sh`; marcar concluído só após teste ponta a ponta.
- **Conteúdo reutilizável (redação própria):** template `features.json` para firmware com `id`, `descricao`, `hw_necessario` (booleano), `comando_teste_host`, `evidencia` e `passes`. Regra: `passes` só vira `true` com saída de teste de host ou log de bancada anexado; sessão começa com orientação (git log, progresso), build e smoke test; termina em estado limpo e commitado.
- **Ressalvas:** exemplo é web; em firmware, o teste ponta a ponta exige bancada e autorização humana (Suposição do plugin). A Anthropic lista como questão aberta se o padrão generaliza.
- **Verificação:** artigo lido; autor, data, JSON/`passes`, uma funcionalidade por sessão, `init.sh`, teste ponta a ponta conferidos.
- **Prompt-score:** o template reescrito: 82 (D1 4, D2 4, D3 5, D4 5, D5 3, D6 5, D7 5, D8 4, D9 4, D10 5, D11 3, D12 4).

### V-03 — Saída de ferramenta e verificador quase perfeito (origem R-authoritative-03, R-github-11, R-community-16) — Classe A (8)
- **Lente:** authoritative + github + community · **Tipo:** checklist · pattern
- **Fonte:** https://www.anthropic.com/engineering/building-c-compiler · Nicholas Carlini, 5 fev. 2026 (Verificado)
- **Técnicas-chave (Verificado):** quase 2.000 sessões, cerca de US$ 20 mil, 16 agentes; verificador quase perfeito ou o agente resolve o problema errado; imprimir poucas linhas e logar o resto em arquivo; `ERROR` e motivo na mesma linha; estatísticas pré-calculadas; `--fast` com amostra aleatória determinística por agente; CI contra regressão; GCC como oráculo com delta debugging; aviso de que software autônomo sem verificação humana traz riscos reais e que passar nos testes raramente prova que acabou.
- **Para que serve:** scripts de build/flash/teste que um agente executa; isolar bug por oráculo (por exemplo, build de host contra build de alvo).
- **Conteúdo reutilizável (redação própria):** checklist de ferramenta de bancada: saída padrão cabe em 20 linhas? erro tem prefixo fixo e motivo na mesma linha? log completo em caminho fixo? existe modo rápido determinístico? existe oráculo de referência?
- **Ressalvas:** caso de compilador; o limite de "20 linhas" é nossa Suposição (a fonte diz "poucas linhas").
- **Verificação:** lido; autor, data, números e dez afirmações conferidos.
- **Prompt-score:** checklist reescrito 80.

### V-04 — Autoria de skills: descrição como gatilho e divulgação progressiva (origem R-authoritative-04) — Classe A (9)
- **Lente:** authoritative · **Tipo:** reference · checklist
- **Fonte:** https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md · repositório https://github.com/anthropics/skills
- **Sinais:** 180.246★, push 2026-10-09, licença nula na API (Verificado). Reuso só destilado.
- **Técnicas-chave (Verificado):** "quando usar" na `description`; corpo abaixo de 500 linhas; referências acima de 300 linhas com índice; `scripts/`, `references/`, `assets/`.
- **Conteúdo reutilizável:** checklist de autoria (descrição com gatilhos PT-BR + EN, corpo curto, referências por MCU, modelo de saída). Nome do plugin e das skills sem prefixo `claude-`/`anthropic-` (ver V-06).
- **Verificação:** SKILL.md lido; as quatro afirmações conferem; metadados por API.

### V-05 — Hooks determinísticos: PostToolUse e PreToolUse como gate (origem R-authoritative-05, R-community-18) — Classe A (9)
- **Lente:** authoritative + community · **Tipo:** reference (hook documentado, não ativo)
- **Fonte:** https://code.claude.com/docs/en/hooks-guide (referência: https://code.claude.com/docs/en/hooks)
- **Técnicas-chave (Verificado):** matcher `Edit|Write` ou `Bash`; exit 2 bloqueia e devolve stderr; JSON com `permissionDecision: "deny"` e motivo dentro de `hookSpecificOutput`; com vários hooks vale o mais restritivo (`deny`, `defer`, `ask`, `allow`); `continueOnBlock` devolve o motivo ao Claude e segue; **PreToolUse com deny bloqueia mesmo em `bypassPermissions`** (útil para gate de gravação); campos no nível errado são ignorados sem erro (usar `claude --debug`).
- **Conteúdo reutilizável (redação própria):** gate de hardware: hook `PreToolUse` com matcher `Bash` que nega comandos de gravação, erase, unlock e escrita de memória (`flash`, `erase`, `openocd ... program`, `JLinkExe` com escrita, `esptool write_flash`, `st-flash`) até haver confirmação; a lista de padrões fica em arquivo separado. Aviso: filtro por texto é guarda, não sandbox; um comando alternativo escapa (Inferido).
- **Ressalvas:** hooks executam shell com permissões do usuário; **não ativar em `hooks/hooks.json` do plugin**; documentar em `references/` com comando de instalação.
- **Verificação:** guia lido (trechos de exit 2, deny, precedência, bypass e `continueOnBlock` localizados por busca no texto).

### V-06 — Plugins: manifest, validação, nomes reservados e LSP para C/C++ e Rust (origem R-authoritative-06, R-community-14) — Classe A (9)
- **Lente:** authoritative + community · **Tipo:** reference
- **Fonte:** https://code.claude.com/docs/en/plugins-reference e https://code.claude.com/docs/en/plugins/code-intelligence
- **Técnicas-chave (Verificado):** `claude plugin validate` é a verificação autoritativa; só `name` é obrigatório no manifest; caminhos começam com `./`, devem existir e ficar dentro do plugin; `lspServers`: `command` e `extensionToLanguage` obrigatórios, objetos estritos; `CLAUDE.md` na raiz do plugin não é carregado e a validação avisa; `bin/` entra no PATH do Bash; nomes iniciados em `claude-`, `anthropic-`, `anthropics-`, `cc-plugin-` são erro, e nome com `official` junto de `claude` ou `anthropic` também; plugins oficiais `clangd-lsp` (binário `clangd`) e `rust-analyzer-lsp` (binário `rust-analyzer`); instalar o binário antes (`Executable not found in $PATH` na aba Errors de `/plugin`); LSP não roda em sessões de nuvem. Comando: `/plugin install clangd-lsp@claude-plugins-official`.
- **Ressalvas:** o README do `clangd-lsp` (lido) só exige o binário `clangd` e **não** menciona `compile_commands.json`; que clangd precisa dele em projeto CMake é conhecimento geral (Inferido).
- **Verificação:** duas páginas e o README do clangd-lsp lidos. Correção: URL `/docs/en/code-intelligence` é 404; a correta é `/docs/en/plugins/code-intelligence`.

### V-07 — Marketplace oficial: política de confiança para plugins de terceiros (origem R-authoritative-07) — Classe A (8)
- **Lente:** authoritative · **Tipo:** checklist
- **Fonte:** https://github.com/anthropics/claude-plugins-official
- **Sinais:** 37,6 mil★, Apache-2.0 (Verificado na página); data de push Não verificável (API 403).
- **Conteúdo reutilizável:** antes de instalar plugin de terceiros: quem mantém? há hook ou MCP que executa shell? pede credencial, porta serial ou rede da bancada? versão fixada? Cada plugin do marketplace tem a própria licença.
- **Verificação:** página lida; `plugins/clangd-lsp` existe (README e LICENSE).

### V-08 — Sandbox de sistema de arquivos e rede para agentes (origem R-authoritative-23) — Classe A (9)
- **Lente:** authoritative · **Tipo:** pattern · reference
- **Fonte:** https://www.anthropic.com/engineering/claude-code-sandboxing · 20 out. 2025 (Verificado)
- **Técnicas-chave (Verificado):** precisa de isolamento de arquivos **e** de rede; bubblewrap (Linux) e seatbelt (macOS); `/sandbox`; redução de 84% nos prompts de permissão (relato interno); research preview.
- **Conteúdo reutilizável (redação própria):** perfil de bancada: escrita só no repositório e na pasta de build; rede só para registries e toolchain; porta serial, probe e credenciais de gravação fora da allowlist por padrão (Inferido: a página não trata de serial).
- **Verificação:** lido; seis afirmações conferem.

### V-09 — Regras de C embarcado do Zephyr (subconjunto de MISRA-C 2012) (origem R-authoritative-09) — Classe A (8)
- **Lente:** authoritative · **Tipo:** checklist
- **Fonte:** https://docs.zephyrproject.org/latest/contribute/coding_guidelines/index.html
- **Técnicas-chave (Verificado):** sem alocação dinâmica (Dir 4.12) mas com exceção para o kernel nas regras adicionais (contradição não reconciliada pela página); liberar recursos; testar informação de erro e `errno`; usar retorno de função; não remover `const`/`volatile` por cast; `static` para linkage interno (Rule 8.8); sem recursão; `else` final e `default` em switch; protótipos; sem código comentado ou inalcançável; macros com parênteses; include guard.
- **Conteúdo reutilizável (redação própria):** checklist de 15 itens para revisão de C, cada um com a razão em uma frase e a opção "rastrear regra" que lê a versão atual da página antes de citar número.
- **Ressalvas:** MISRA é pago e o plugin nunca reproduz o texto; licença da página Não verificada nesta execução (o projeto Zephyr é Apache-2.0, Inferido).
- **Verificação:** 16 regras conferidas na página, com os dois desvios de numeração acima.
- **Prompt-score:** checklist reescrito 81.

### V-10 — ESP-IDF Style Guide (origem R-authoritative-11) — Classe A (8)
- **Lente:** authoritative · **Tipo:** checklist
- **Fonte:** https://docs.espressif.com/projects/esp-idf/en/latest/esp32/contribute/style-guide.html
- **Técnicas-chave (Verificado na versão latest):** erro recuperável retorna código; `assert` só para erro interno irrecuperável e sem efeito colateral; `ESP_ERROR_CHECK` para `esp_err_t` irrecuperável; `(void)` para variável não usada; `#pragma once`; 4 espaços, 120 colunas, astyle; sem código comentado; `s_` em estáticas.
- **Ressalvas:** não cobre ISR/IRAM. Licença não verificada.
- **Verificação:** versão atual lida; todas as dez afirmações conferem.

### V-11 — no_std: panic handler (origem R-authoritative-12, R-github-14) — Classe A (8)
- **Lente:** authoritative + github · **Tipo:** checklist
- **Fonte:** https://docs.rust-embedded.org/book/start/panicking.html (livro: https://docs.rust-embedded.org/book/)
- **Técnicas-chave (Verificado):** `#[panic_handler]` com `fn(&PanicInfo) -> !`, exatamente uma vez no grafo de dependências; crates `panic-halt`, `panic-abort`, `panic-itm`, `panic-semihosting`; `use panic_halt as _;`; escolha por perfil com `cfg(debug_assertions)`; breakpoint em `rust_begin_unwind`. `extern crate` é estilo pré-2018.
- **Ressalvas:** livro: texto em CC-BY-SA (Inferido, API 403), então só destilar.
- **Verificação:** página lida; tudo confere.

### V-12 — Rust embedded: concorrência com interrupções (origem R-authoritative-13) — Classe A (8)
- **Lente:** authoritative · **Tipo:** checklist
- **Fonte:** https://docs.rust-embedded.org/book/concurrency/index.html
- **Técnicas-chave (Verificado):** `static mut` tocado por interrupção perde atualização em leitura-modificação-escrita; `Mutex<RefCell<Option<T>>>` com token de critical section; inicializar antes de habilitar a interrupção; atômicos (Cortex-M0/M0+ só load/store, M3+ com CAS, `Relaxed` basta em núcleo único); handler que espera lock da thread principal pode travar; critical section não protege entre núcleos; RTIC e Embassy mencionados.
- **Conteúdo reutilizável (redação própria):** checklist "dado compartilhado com ISR": protegido por seção crítica, atômico ou fila? inicializado antes da habilitação? seção crítica curta (Inferido, a fonte só cita latência e jitter)? núcleo duplo? Conferir a versão atual de RTIC/Embassy antes de recomendar.
- **Verificação:** lido; oito de nove afirmações conferem (a "curta" é inferência).

### V-13 — clang-tidy com compile_commands.json (origem R-authoritative-16) — Classe A (8)
- **Lente:** authoritative · **Tipo:** command · config
- **Fonte:** https://clang.llvm.org/extra/clang-tidy/
- **Técnicas-chave (Verificado):** `-p` e `CMAKE_EXPORT_COMPILE_COMMANDS=ON`; `-checks=` com globs e prefixo `-`; `-list-checks`; famílias `bugprone-`, `cert-`, `misc-`, `cppcoreguidelines-`, `readability-`; `-warnings-as-errors`; `--fix`/`--fix-errors`; `NOLINT*`.
- **Ressalvas:** a página não trata de embarcado (relevância Inferida). Verificar se o clang-tidy do host entende o toolchain cruzado (`--sysroot`, `--target`) é pendência de nova rodada.
- **Verificação:** lido; oito afirmações conferem.

### V-14 — CERT C (sinais e volatile) e matriz MISRA C:2023 (origem R-authoritative-14, R-authoritative-15) — Classe B (7)
- **Lente:** authoritative · **Tipo:** checklist · reference
- **Fonte:** https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/signals-sig/sig31-c e https://www.mathworks.com/help/bugfinder/misra-c-2023-reference.html
- **Técnicas-chave (Verificado):** SIG31-C: em handler só `volatile sig_atomic_t` e atômicos lock-free; para portabilidade o handler só marca flag e retorna. MISRA C:2023 consolida C:2012 com corrigenda 1 e 2 e emendas 1 a 4; categorias mandatory, required, advisory; Dir e Rule listadas separadamente; texto oficial é pago.
- **Conteúdo reutilizável:** matriz de configuração: "qual edição, quais categorias, quais regras desviadas e por quê"; checklist de `volatile`: é para ISR/registrador? é leitura-modificação-escrita (então atômico ou seção crítica)? há cast removendo `volatile`?
- **Ressalvas:** numeração CERT muda entre versões (DCL22-C/DCL34-C); `volatile` sozinho não garante atomicidade, nem em ISR. Em C embarcado o "handler de sinal" é analogia com ISR (Inferido).
- **Verificação:** SIG31-C e página MathWorks lidas; DCL22-C não reconferida.

### V-15 — Revisão de ISR com FreeRTOS (origem R-authoritative-17) — Classe B (7), rebaixada de C por verificação no fonte oficial
- **Lente:** authoritative · **Tipo:** checklist
- **Fonte:** https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/semphr.h (MIT, Amazon, Verificado no cabeçalho); página da API: https://www.freertos.org/a00124.html (existe; conteúdo truncado na leitura)
- **Técnicas-chave:** API `FromISR` dentro de ISR; `pxHigherPriorityTaskWoken` é definido se uma tarefa de prioridade maior foi desbloqueada, e o ISR deve pedir troca de contexto antes de sair com a macro da porta (varia por porta, Verificado); sem tempo de bloqueio em ISR (Inferido); ISR mínimo e trabalho em tarefa (consenso, Inferido); limite de prioridade `configMAX_SYSCALL_INTERRUPT_PRIORITY` (Inferido, conferir na doc da porta).
- **Conteúdo reutilizável (redação própria):** checklist: só `FromISR` no handler? flag de tarefa acordada repassado ao yield da porta? nenhum bloqueio? prioridade do ISR dentro do limite da porta? trabalho pesado movido para tarefa ou fila? chamada de API do kernel dentro de seção crítica (Não verificado)?
- **Verificação:** cabeçalho oficial lido; as 3 páginas de documentação adivinhadas deram 404; ver lacuna.
- **Prompt-score:** checklist reescrito 76 (D12 3: parte Inferida).

### V-16 — Regras de firmware STM32 HAL em .mdc (origem R-authoritative-18, R-github-07, R-community-08) — Classe B (6)
- **Lente:** authoritative + github + community · **Tipo:** claude-md-rule · checklist
- **Fonte:** https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/embedded-stm32-hal.mdc · repositório https://github.com/PatrickJS/awesome-cursorrules (40.891★, CC0-1.0, push 2026-05-30)
- **Verificação:** arquivo lido; **30 regras conferidas**; sem linha de autoria ou licença própria (a CC0 é do repositório); sem texto de IA embutido; nada de comando perigoso.
- **Técnicas-chave:** camadas BSP/drivers/middleware/app/testes; código gerado do CubeMX separado; hardware atrás de interface estreita; documentar clock, pinos, dono de periférico, prioridades; init de periférico em um lugar; checar retorno do HAL e timeout em toda espera; DMA com dono e tempo de vida; `volatile` só para ISR/registrador; ISR curta e sem alocação; seções críticas, atômicos, filas; tabelas `const`; inteiros de largura fixa; watchdog desde o início; stack de ISR e tarefas; teste de lógica no host e HIL para periférico; fault handler que registra motivo de reset, registradores de falha e versão do build.
- **Conteúdo reutilizável (reescrito, ver prompt-score):** regras agrupadas em 6 blocos, cada uma com a razão em uma linha, um bloco "antes de mexer em periférico" (ler o manual de referência e a errata da variante; nomes de registrador e função HAL vêm de header ou datasheet citado) e um formato de saída de revisão (achado, regra, arquivo:linha, gravidade, como verificar). Acrescentar a nuance que a fonte omite: `volatile` não torna o acesso atômico nem ordena memória; para dado multi-palavra compartilhado usar seção crítica ou atômico.
- **Ressalvas:** regras genéricas, sem avaliação de uso. Hardware real exige datasheet e autorização de bancada.
- **Prompt-score:** original 52 (D1 3, D2 1, D3 4, D4 4, D5 0, D6 0, D7 2, D8 2, D9 4, D10 5, D11 2, D12 4); reescrito 82.

### V-17 — Template de CLAUDE.md para firmware (origem R-authoritative-08, R-github-16) — Classe B (6)
- **Lente:** authoritative + github · **Tipo:** claude-md-rule · template
- **Fonte:** https://www.beningo.com/why-claude-code-for-firmware-development-matters/ · Jacob Beningo, 20 nov. 2025, atualizado 10 dez. 2025 (Verificado)
- **Técnicas-chave (Verificado):** começar com cerca de 20 linhas; 13 seções (plataforma, tempo real, arquitetura, toolchain e build, padrões, "não faça" crítico, bibliotecas permitidas, orçamento de energia e de memória, estratégia de teste, errata e contornos, estrutura de arquivos, notas para a IA); o autor diz que a ferramenta não conhece embarcados em especial, mas entende desenvolvimento de software a fundo.
- **Conteúdo reutilizável (redação própria):** template curto (alvo, RTOS ou bare metal, memória, build/teste/flash com a regra de confirmação, padrões, proibições com razão, definição de pronto) mais regra: "cada proibição vira linha de CLAUDE.md e, quando possível, teste ou hook". Ficar abaixo de 60 linhas e linkar o restante.
- **Ressalvas:** blog de praticante; licença não declarada, só destilar.
- **Prompt-score (template reescrito):** 83.

### V-18 — Vetar skills de terceiros para embarcados (origem R-authoritative-20) — Classe B (5)
- **Lente:** authoritative · **Tipo:** checklist de segurança
- **Fonte:** https://snyk.io/articles/claude-skills-embedded-systems-engineers/ · Stephen Thoemmes, 8 abr. 2026 (Verificado)
- **Técnicas-chave (Verificado):** ler SKILL.md e scripts antes de instalar; escolher fonte mantida; revisar `allowed-tools` e dar atenção a skill com shell; escanear scripts com SAST; usar skill para boilerplate, não para timing, energia ou quirks de hardware.
- **Ressalvas:** blog de vendor; números (36%, 13%) da pesquisa da própria Snyk, sem metodologia na página.
- **Verificação:** página lida; passos e estatísticas conferidos.

### V-19 — Loop de hardware: daemon mais comandos curtos (origem R-authoritative-21, R-github-13, R-community-07) — Classe B (6)
- **Lente:** authoritative + github + community · **Tipo:** workflow · pattern
- **Fonte:** https://www.bitcraze.io/?p=14780 · Arnaud, 13 abr. 2026 (Verificado); ferramenta citada: ataffanel/crazyflie-agent-cli (não oficial, não lida)
- **Técnicas-chave (Verificado):** daemon mantém o link com estado; comandos avulsos conversam com ele; capacidades flash, reset, console, parâmetros e variáveis de log; skill companheira com o fluxo; "o humano precisa continuar no circuito".
- **Conteúdo reutilizável:** ciclo compilar, gravar, observar console, comparar, corrigir. A sintaxe de CLI, exit codes e limites de linhas são **Suposição de design da fábrica**, não da fonte.
- **Ressalvas:** experimento único; o artigo não trata de autorização para gravar.

### V-20 — Princípios de ferramentas para agentes (Ronacher) (origem R-authoritative-22, R-community-06) — Classe B (6)
- **Lente:** authoritative + community · **Tipo:** checklist
- **Fonte:** https://lucumr.pocoo.org/2025/6/12/agentic-coding/ · 12 jun. 2025 (Verificado)
- **Técnicas-chave (Verificado):** rápida e silenciosa; travar é pior que falhar; erro claro; alvo `make dev` e pidfile contra segunda instância; log em arquivo e no terminal; verbosidade ajustável; observabilidade desde a primeira versão.
- **Ressalvas:** o texto não fala de timeout nem exit code (ver correção 1); post com 16 meses.
- **Prompt-score:** não se aplica (artigo).

### V-21 — embeddedskills: ciclo build-flash-debug e gate `operation_mode` (origem R-github-01, R-community-01, R-community-20, R-community-21) — Classe B (6)
- **Lente:** github + community · **Tipo:** skill (conjunto) · workflow
- **Fonte:** https://github.com/zhinkgit/embeddedskills (734★, MIT, push 2026-09-03; Verificado) · arquivos: `workflow/SKILL.md`, `jlink/SKILL.md`
- **Técnicas-chave (Verificado):** 12 pastas de skill (can, eide, gcc, jlink, keil, net, openocd, probe-rs, serial, ssh, terminal, workflow); resolução de backend por flag, depois config, depois descoberta; estado em `.embeddedskills/state.json`; gate de ambiguidade (lista candidatos em vez de escolher); tabela de status testado/pendente; `operation_mode` 1 executa direto, 2 mostra resumo de risco, 3 pede confirmação; flash, write-mem e reset classificados como alto risco; `.bin` exige endereço explícito.
- **Conteúdo reutilizável (redação própria, melhora a fonte):** regra de plugin: toda operação que grava, apaga, reseta ou escreve memória exige confirmação explícita **por padrão** (equivale a modo 3; o exemplo da fonte usa 1, inseguro), `.bin` sem endereço falha, ambiguidade de projeto ou probe para e lista opções, resultado de cada estágio em JSON (`stage`, `ok`, `backend`, `error`, `next_commands`; campos são nossa Suposição porque o workflow não nomeia os campos).
- **Ressalvas:** workflow encadeia build-flash sem confirmação (anti-pattern); aviso do Windows sobre trocar o driver do J-Link para WinUSB pode quebrar as ferramentas da SEGGER; scripts não lidos; evidência de testes é auto-declarada. Não copiar código além do permitido pela MIT com atribuição.
- **Prompt-score:** original (SKILL jlink/workflow, leitura parcial) 66; regra de gate reescrita 86 (D8 5, D7 4).

### V-22 — Depuração com causa raiz antes da correção (gstack /investigate) (origem R-community-19) — Classe B (6)
- **Lente:** community · **Tipo:** skill
- **Fonte:** https://raw.githubusercontent.com/garrytan/gstack/main/investigate/SKILL.md (135.780★, MIT; Verificado)
- **Técnicas-chave (Verificado):** nenhuma correção sem causa raiz; reproduzir, hipótese testável, confirmar com log ou assert temporário; parar após três hipóteses falhas e perguntar; correção com o menor diff; teste de regressão que falha sem a correção; perguntar antes se a correção tocar mais de cinco arquivos; relatório final com status (DONE, DONE_WITH_CONCERNS, BLOCKED).
- **Conteúdo reutilizável (redação própria):** checklist de bug em firmware: (1) reproduzir ou registrar motivo de reset e registradores de falha; (2) `git log` do que mudou; (3) hipótese; (4) confirmar com log, assert ou captura de barramento; (5) corrigir a causa, não o sintoma (aumentar pilha ou timeout só entra com justificativa); (6) teste de host ou log de bancada como prova; (7) parar em três hipóteses.
- **Ressalvas:** o frontmatter original traz hooks de escopo, telemetria e "preamble" próprios do gstack; **não copiar o arquivo**, só a metodologia.
- **Prompt-score:** original 73 (D9 2 por maquinário do gstack); destilado 85.

### V-23 — Checklist "datasheet primeiro" (origem R-community-04) — Classe B (5)
- **Lente:** community · **Tipo:** checklist · anti-pattern
- **Fonte:** https://news.ycombinator.com/item?id=44915206 (113 pts, 52 comentários, 15 ago. 2025; Verificado)
- **Técnicas-chave (relatos do thread):** agentes genéricos inventam registradores e chamadas HAL de outra família; ancorar em datasheet e manual de referência; um comentarista postou o prompt do agente com citação obrigatória e plano numerado.
- **Conteúdo reutilizável (redação própria):** antes de escrever código de periférico: (1) nomes de registrador e de função HAL vêm de header, SVD ou datasheet **citado com seção**; (2) sem fonte, parar e perguntar; (3) variante exata do chip e revisão do silício confirmadas; (4) documento proprietário ou sob NDA não sai da máquina sem decisão do usuário; (5) relatar o que foi compilado, simulado e testado em hardware.
- **Ressalvas:** discussão de um produto comercial; não tratar alegações de privacidade do thread como fato.
- **Prompt-score:** checklist reescrito 80.

### V-24 — OTA seguro com MCUboot (adicionado pelo validador para cobrir lacuna) — Classe B (7)
- **Lente:** authoritative (lacuna) · **Tipo:** reference · checklist
- **Fonte:** https://docs.mcuboot.com/design.html · integração Zephyr: https://docs.zephyrproject.org/latest/services/device_mgmt/mcumgr.html (diz que hoje só MCUboot é suportado para upgrade de imagem)
- **Sinais:** documentação do projeto; estrelas/licença do repositório Não verificadas (API 403; MCUboot é Apache-2.0, Inferido).
- **Técnicas-chave (Verificado):** slots primário e secundário; modos swap, overwrite-only, direct-XIP e RAM-load; verificação de hash e assinatura com chave pública casada por hash; swap de teste que reverte no reset se a imagem não se confirmar; downgrade por versão (só overwrite-only) ou por contador de segurança em armazenamento confiável; resultados FAIL e PANIC interrompem o boot.
- **Conteúdo reutilizável (redação própria):** checklist de revisão de OTA: imagem assinada e verificada antes do boot? há confirmação após autoteste, com reversão automática? há proteção contra downgrade? o modo de upgrade (swap, overwrite, XIP) casa com o caminho de recuperação? a chave de assinatura nunca vai para o repositório? Para o agente: nunca gerar comando executável que queime fuse, chave ou proteção de leitura sem confirmação (ver V-27).
- **Ressalvas:** só o documento de design foi lido; guias por plataforma (ESP-IDF, nRF) ficam para nova rodada.

### V-25 — Regras operacionais para projeto ESP32 (esp32-claude-workbench) (origem R-github-02, R-community-02) — Classe C (4)
- **Lente:** github + community · **Tipo:** claude-md-rule · workflow
- **Fonte:** https://github.com/agodianel/esp32-claude-workbench (79★, MIT, push 2026-03-31) · CLAUDE.md raw
- **Técnicas-chave (Verificado):** contrato antes do código (escopo, riscos, testes, reversão) aceito antes de implementar; definição de pronto (testes executados com resultado registrado, lacunas declaradas, missão atualizada, PR com racional, testes e riscos); stack mínima 2048 e 4096 bytes (afirmação do autor); `ESP_ERROR_CHECK` só em inicialização fatal; nenhuma alocação em ISR; comandos `/scout`, `/contract`, `/hw-check`, `/pin-audit`, `/arch-review`, `/test-plan`, `/triage-log`, `/review-crash`, `/prcraft`; 148+ testes pytest declarados (não vistos).
- **Conteúdo reutilizável (redação própria):** modelo "contrato + definição de pronto" e regra de registro de teste (casos, comando, resultado com evidência, o que não foi testado). Números de pilha, pinos e memória **não** entram sem conferir na documentação da variante (ver correção 4).
- **Ressalvas:** o CLAUDE.md não diz nada sobre gravação nem confirmação humana (Verificado). Classe C: poucas estrelas, evidência auto-declarada.
- **Prompt-score:** original 58 (D3 4, D7 4, D8 2, D12 2, D5 0); reescrito 80.

### V-26 — Auditoria de pinos ESP32 (esp32_pin_audit) (origem R-github-03) — Classe C (4)
- **Lente:** github · **Tipo:** checklist · skill
- **Fonte:** https://raw.githubusercontent.com/agodianel/esp32-claude-workbench/main/.claude/skills/esp32_pin_audit/SKILL.md
- **Técnicas-chave (Verificado):** coleta por grep de macros de pino e Kconfig; classes de pino reservado; tabela de alocação; divergência entre código e documentação.
- **Conteúdo reutilizável (reescrito, corrigido):** violações a procurar: pino de flash ou PSRAM do módulo em uso (GPIO 6–11, e 16–17 em módulos com PSRAM, conforme doc ESP-IDF); strapping usado sem justificativa de boot (lista conforme datasheet da variante; no ESP32 clássico inclui GPIO 5 e 12, Inferido); saída em pino só de entrada (GPIO 34–39, sem pull interno, Verificado na doc); mesmo pino em dois periféricos; I2C só com pull-up interno; entrada flutuante; ADC2 com Wi-Fi no ESP32 clássico (Inferido, não reconferido na doc nesta execução); código divergente do mapa de pinos. Formato: tabela (GPIO, função, componente, direção, pull, notas) mais lista de achados com gravidade.
- **Ressalvas:** vale só para ESP32 clássico; para S2, S3, C3, C6 o mapa difere e exige o datasheet da variante.
- **Prompt-score:** original 62 (D12 2, D8 2, D11 2); reescrito 82.

### V-27 — Níveis de evidência e portões de operação irreversível (embedded-systems-architect) (origem R-github-06) — Classe C (3)
- **Lente:** github · **Tipo:** skill · checklist
- **Fonte:** https://github.com/Zachariah9420/embedded-systems-architect (5★, MIT; Verificado na página e no README)
- **Técnicas-chave (Verificado):** cinco níveis (confirmado, inferência de engenharia, estimativa, a verificar, dados insuficientes); dados faltantes nunca inventados; spec citada pelo usuário vale "a verificar"; resultados negativos registrados com versão da ferramenta, comando e log; operações irreversíveis (eFuse/OTP, chaves de secure boot, criptografia de flash, proteção permanente, anti-rollback) não geram comandos copiáveis; escrita no dispositivo só com caminho de recuperação confirmado; gravação com dry-run e leitura de verificação por padrão.
- **Conteúdo reutilizável (redação própria):** mapa para os rótulos da fábrica (Verificado, Inferido, Suposição, Não verificável) e checklist de portão: caminho de recuperação confirmado? dry-run executado? leitura de verificação prevista? operação irreversível bloqueada sem confirmação explícita no chat?
- **Ressalvas:** 5 estrelas e 5 commits; as avaliações em `docs/evaluation.md` não foram abertas; validação declarada só em Codex. SKILL.md e scripts não lidos (README apenas).
- **Prompt-score:** provisório 83 (somente README).

### V-28 — Princípios de revisão de ESP32 por contexto de execução (esp32-expert) (origem R-github-09) — Classe C (4)
- **Lente:** github · **Tipo:** skill · checklist
- **Fonte:** https://raw.githubusercontent.com/johnkozaris/jko-claude-plugins/main/plugins/esp32-cpp/skills/esp32-expert/SKILL.md · repositório: 11★, MIT (Verificado na página), data de push Não verificada
- **Técnicas-chave (Verificado):** identificar chip, framework, versão e configuração antes de agir; julgar pelo comportamento em campo (semanas de uptime, OTA, reconexão, baixa tensão); contexto de execução (tarefa, ISR, timer, event loop) limita as operações; limites explícitos para pilhas, filas, retries, esperas e alocações; ownership e troca de mensagem em vez de estado compartilhado; escolha deliberada da região de memória; falha transitória, configuração e hardware tratadas separadamente, com watchdog como último recurso; diagnosticar causa; relatar o que foi compilado, simulado e testado em hardware; 8 arquivos de referência por tema.
- **Conteúdo reutilizável (redação própria):** checklist de 6 perguntas por achado (contexto de execução, limite, dono do dado, região de memória, classe de falha, consequência em campo) e o rótulo de evidência "compilado, simulado, em hardware".
- **Ressalvas:** referências não lidas; sem avaliação de uso.
- **Prompt-score:** original 72; reescrito 82.

### V-29 — Harness de firmware com hardware real (SensorsIot/Embedded-AI-Harness) (origem R-github-15) — Classe C (4)
- **Lente:** github · **Tipo:** workflow · reference
- **Fonte:** https://github.com/SensorsIot/Embedded-AI-Harness · 188★, MIT, push 2026-10-09 (API e página; Verificado)
- **Técnicas-chave (Verificado no README):** o agente escreve, compila, grava num ESP32 real e roda testes até passar; bancada com Raspberry Pi expõe placas por HTTP e serial de rede; MCP com cerca de 70 ferramentas; skills em `.claude/skills/` (`/define`, `/harness`, `/commission`, `/build` e de ESP-IDF, PlatformIO, WiFi, BLE, MQTT, depuração, CI); proveniência de artefato (grava binário do CI com toolchain fixa); gerenciador de slot que recusa pedidos conflitantes; único ato só humano: publicar a tag.
- **Ressalvas de segurança (Verificado):** o README diz que a API HTTP da bancada **não tem autenticação**; rodar só em rede confiável. Skills e CLAUDE.md não lidos (404 na tentativa do pesquisador; não há CLAUDE.md na raiz). Pista para nova rodada: ler as skills de BLE, MQTT e ESP-IDF, que cobrem lacunas de protocolo.
- **Uso no plugin:** só como referência de desenho; nada instalado.

## Rejeitados e rebaixados

| Item | Decisão | Motivo |
| --- | --- | --- |
| R-authoritative-10 (BARR-C:2018) | Rebaixado a referência de consulta | Licença do documento proíbe postar o PDF e compartilhar fora da empresa; o kit no GitHub é MIT mas não cobre o padrão (Verificado). Usar só a estrutura de capítulos, sem texto. |
| R-authoritative-19, R-github-08, R-community-09 (C++ do awesome-cursorrules) | Rebaixado a C (sinal) | Arquivo lido: é C++ de desktop (SOLID, `std::filesystem`, `std::thread`, exceções, `std::expected` que exige C++23); sem conteúdo de embarcado. A checklist "C++ para firmware" precisa ser escrita pelo construtor a partir de documentação de toolchain, não derivada deste arquivo. |
| R-authoritative-24 (CISA Secure by Design) | Rebaixado a referência de política | Três princípios gerais confirmados (revisão 25 out. 2023); não trata de IoT nem de firmware; o PDF não foi lido. |
| R-github-04, R-community-22 (automotive-claude-code-agents) | Rebaixado a C (3) | MIT e 199★, mas README afirma 39 agentes, mais de 75 categorias de skill e 31 regras, sem resultados de teste visíveis (sinal de conteúdo gerado em massa). Mantém só o padrão de instalador (prefixo, manifest, sem tocar `settings.json`) e a lista de normas como pista. |
| R-github-05 (embedded-ai-workspace) | Rebaixado a C (3) | 5★, 10 commits, "verified end-to-end" auto-declarado sem logs ou métricas (Verificado na página). Mantém os estágios de HIL como ideia genérica. |
| R-github-10 (esp32-firmware-engineer-skill) | Rebaixado | Sem licença (Verificado, API); 12★. Só destilação (pré-condições: variante do chip, versão do framework, reprodução mínima), sem reproduzir texto. |
| R-community-03 (stm32-mcp) | Rebaixado a referência de segurança | Correção: README declara MIT (o pesquisador disse sem licença), 25★, Show HN com 1 ponto. Útil só pela nota "não é sandbox; pode gravar e sobrescrever memória". Nunca ativar `.mcp.json` por padrão. |
| R-community-05 (Ask HN, 461 pontos) | Rebaixado a C (3) | Relatos gerais (C#, Python, TypeScript), não de embarcados; data só "8 meses atrás". Úteis como sinal: warnings como erro, testes antes, agentes escrevendo testes vazios, commit antes de cada tarefa. Só 100 mil dos 391 mil caracteres foram lidos. |
| R-community-10, R-community-11 (awesome-copilot catálogo e agent-safety) | Rebaixados | Repositório 39.881★, MIT. `agent-safety` confirmado (fail closed, allowlist, aprovação humana, filtro de argumentos, JSON Lines) mas **não menciona hardware** e a checklist de "porta de hardware" é do pesquisador, não da fonte. A lacuna de embarcados no catálogo foi vista só nas 100 primeiras entradas. |
| R-community-12 (cpp-language-service-tools) | Rebaixado | Depende de ferramentas `*_CppTools` específicas e tem contradições internas (batching, `read_file`, fallback) — Verificado. Para refatoração usar o LSP clangd (V-06). |
| R-community-13 (cmake-vcpkg) | Rejeitado | Foco em vcpkg e desktop; sem cross-compilação; a "presets host-test e cross" era Suposição do pesquisador. |
| R-community-23 (dev.to, cluster ESP32-S3) | Rejeitado | Prova de conceito sem prompt ou regra reaproveitável; modelo gera tokens aleatórios, segundo a própria página. |

Segurança e copyright (varredura): nenhum arquivo lido continha instruções dirigidas à IA, links encurtados ou pedido de execução de instalador. Riscos registrados: workflow do embeddedskills grava sem gate; `jlink` com `operation_mode` 1 no exemplo; API da bancada do SensorsIot sem autenticação; frontmatter do gstack com hooks e telemetria; instalação de qualquer MCP de hardware pode gravar e sobrescrever memória. Nenhum trecho literal de fonte sem licença permissiva foi mantido; os textos reutilizáveis acima são redação própria. As três ocorrências HN "spyware" citadas pelo pesquisador de comunidade não foram abertas por mim e continuam Não verificadas (fora do escopo).

## Mapa de cobertura do escopo

| Subtema | Itens validados | Cobertura |
| --- | --- | --- |
| Workflow de agente, CLAUDE.md, verificação, subagentes | V-01, V-02, V-03, V-17, V-22 | Boa |
| Skills, hooks, plugins, LSP, segurança de extensões | V-04, V-05, V-06, V-07, V-08, V-18 | Boa |
| C/C++ embarcado: estilo, erros, ISR, heap, volatile | V-09, V-10, V-13, V-14, V-15, V-16 | Boa para C; fraca para C++ de firmware (sem fonte de qualidade) |
| Rust embedded e no_std | V-11, V-12 | Parcial (sem Embassy/RTIC v2, probe-rs, defmt, embedded-hal; nenhuma skill ou AGENTS.md de Rust) |
| RTOS: FreeRTOS e Zephyr | V-15, V-09, V-24 | Parcial (FreeRTOS só pelo fonte do kernel; Zephyr sem kernel/threads/devicetree) |
| Firmware STM32 / ESP32 / Arduino | V-16, V-10, V-25, V-26, V-28, V-29 | ESP32 boa; STM32 média; Arduino e PlatformIO sem fonte |
| Protocolos (I2C, SPI, UART, CAN, MQTT, BLE) | nenhum | **Lacuna total** |
| Drivers a partir de datasheet | V-23 (checklist) | Fraca (sem fonte primária; SVD/CMSIS e embedded-hal não lidos) |
| Depuração com hardware e loop build-flash-observar | V-19, V-21, V-22, V-27, V-29 | Boa |
| Testes em host e HIL | V-02 (parcial), V-16, V-29 | **Fraca** (Unity, CMock, Ceedling, ztest/twister, pytest-embedded não lidos) |
| Análise estática | V-13, V-14 | Parcial (cppcheck, sanitizers, -fanalyzer, análise de pilha não lidos) |
| OTA e atualização segura | V-24 | Parcial (só MCUboot design; ESP-IDF OTA/secure boot não lido) |
| Consumo de energia | nenhum | **Lacuna total** |
| Segurança embarcada e IoT | V-24, V-27, V-18 | Fraca (OWASP IoT Top 10 2018 só confirmado como projeto, lista não lida; sem NIST/ETSI) |
| Segurança funcional (IEC 61508, ISO 26262, DO-178C) | nenhum validado | **Lacuna** (só menção rebaixada) |
| Interrupções e concorrência | V-12, V-15, V-14, V-16 | Boa |

## Lacunas objetivas para nova rodada (pesquisáveis)

1. **Protocolos:** documentação oficial de I2C, SPI, UART e CAN no Zephyr (`docs.zephyrproject.org` APIs de periféricos) e no ESP-IDF (drivers I2C/SPI/TWAI); MQTT 3.1.1 e 5.0 (OASIS) e boas práticas de cliente MQTT embarcado; BLE (Zephyr Bluetooth, NimBLE no ESP-IDF). Meta: pelo menos 6 itens com regras de revisão (pull-up, clock stretching, arbitragem CAN, QoS/LWT/reconexão MQTT, MTU BLE).
2. **Testes de firmware:** Unity/CMock/Ceedling (ThrowTheSwitch, conferir licença MIT), ztest e twister no Zephyr, Unity no ESP-IDF, pytest-embedded; padrão de teste em host com HAL falsa; HIL.
3. **Energia:** gerenciamento de energia do Zephyr, modos de sleep e light/deep sleep do ESP-IDF, guias de otimização de fabricante (Nordic, ST); medição de corrente como critério de pronto.
4. **Segurança IoT e OTA:** OWASP IoT Top 10 (PDF 2018) e ISVS/FSTM, NIST IR 8259A, ETSI EN 303 645; secure boot, flash encryption e OTA do ESP-IDF; guias de plataforma do MCUboot (conferir estrelas, licença e data pela página do repositório).
5. **Drivers a partir de datasheet:** CMSIS-SVD, `svd2rust`, `embedded-hal` (traits, versão 1.0), PAC/HAL/BSP; como ancorar registradores em SVD.
6. **Zephyr:** threads, ISR, workqueue, devicetree, Kconfig e `west`; verificar licença Apache-2.0 do projeto na página oficial.
7. **FreeRTOS oficial:** páginas de ISR, detecção de estouro de pilha, `configASSERT` e prioridades (as URLs `Documentation/02-Kernel/...` testadas deram 404; localizar o caminho atual a partir do índice do site).
8. **Rust embedded:** Embassy, RTIC v2, probe-rs, defmt, Embedonomicon; pelo menos um AGENTS.md ou skill de Rust `no_std` com licença clara.
9. **Arduino e PlatformIO:** documentação oficial (PlatformIO unit testing e `pio check`, guia de estilo Arduino).
10. **Análise estática e análise de pilha:** cppcheck (addon MISRA), `-fanalyzer`, `-fstack-usage`, sanitizers em host, análise de pilha do Zephyr.
11. **Segurança funcional:** visão geral pública de IEC 61508, ISO 26262 e DO-178C e como o Zephyr documenta seu processo de safety; não buscar texto de norma paga.
12. **Comunidade (nenhum sinal social):** Reddit (r/embedded, r/ClaudeCode), X e YouTube não foram alcançados; refazer com busca quando houver orçamento de WebSearch (ou elevar `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`). Também ler no GitHub: skills de `SensorsIot/Embedded-AI-Harness` (BLE, MQTT, ESP-IDF), `embeddedskills` (keil, gcc, openocd, probe-rs), referências de `esp32-expert`, e `trailofbits/claude-code-config` (403 antes).
13. **Metadados GitHub pendentes (API 403):** claude-plugins-official (push), mcu-tools/mcuboot, rust-embedded/book, atillab1, Zachariah9420, SensorsIot (licença conferida pela página, data de push pela API do pesquisador).

## Recomendações ao construtor

Princípios do plugin (seguro por padrão): nenhum hook, MCP ou `bin/` ativo; qualquer gravação, erase, reset, escrita de memória e acesso serial exige confirmação explícita no chat; instruções vão em skills, não em `CLAUDE.md` na raiz do plugin; nomes sem `claude-`/`anthropic-`.

| Artefato | Origem | Tipo |
| --- | --- | --- |
| `firmware-review` (checklist C/C++: erro, assert, recursos, volatile, cast, macros, switch) | V-09, V-10, V-13, V-14, V-16 | skill |
| `isr-safety` (dado compartilhado com ISR, FromISR, yield, seção crítica) | V-12, V-14, V-15, V-16 | skill |
| `rust-no-std` (panic handler, concorrência com interrupção) | V-11, V-12 | skill |
| `hw-bench-loop` (compilar, gravar, observar, corrigir; gate de confirmação por padrão; níveis de evidência) | V-19, V-20, V-21, V-27, V-29 | skill |
| `firmware-root-cause` (causa raiz, três hipóteses, teste de regressão) | V-22 | skill |
| `datasheet-first` (registrador e HAL só com fonte citada) | V-23, V-16 | skill |
| `esp32-review` e `esp32-pin-audit` (variante exata; pinos conforme datasheet) | V-10, V-25, V-26, V-28 | skills |
| `ota-update-review` (assinatura, confirmação, rollback, downgrade) | V-24, V-27 | skill (marcar fontes de plataforma como pendentes) |
| `firmware-reviewer` (subagente somente leitura: Read, Grep, Glob; saída por regra com arquivo:linha, gravidade e verificação) | V-01, V-03, V-16 | agente |
| Protocolo de sessão longa e `features.json` | V-02 | checklist/template em `references/` |
| Checklist de saída de ferramenta de bancada | V-03, V-20, V-19 | checklist |
| Vetting de skill/plugin de terceiros | V-18, V-07, V-08 | checklist |
| Hook de gate de gravação e hook de formatação/clang-tidy | V-05, V-13 | referência em `references/`, **não ativo** |
| Perfil de sandbox para bancada | V-08 | referência |
| Recomendação de `clangd-lsp` e `rust-analyzer-lsp` via marketplace oficial (sem `lspServers` próprio) | V-06 | referência |
| Modelo de CLAUDE.md de firmware (abaixo de 60 linhas) | V-17, V-01 | exemplo em `references/` |
| Prompt da biblioteca "revisão adversarial de diff" e "checklist datasheet primeiro" | V-01, V-23 | prompts da biblioteca |
| Regra de CLAUDE.md: "Build e teste de host livres; gravar, apagar e acionar atuador só com confirmação explícita" | V-01, V-21, V-27 | regra de CLAUDE.md |

Não incluir: texto do BARR-C ou do MISRA; arquivos copiados do gstack; regras numéricas de ESP32 do workbench sem conferência na documentação da variante; qualquer MCP de hardware ativo. Resolver antes de publicar a skill de FreeRTOS a lacuna 7, e antes de qualquer skill de protocolo ou de OTA os itens 1 e 4.

Veredito da rodada anterior (superado pelo adendo no fim do arquivo, que traz o veredito final **pass_with_gaps**): **needs_more**. A base de workflow de agente, extensões, ISR/concorrência e C/Rust está sólida (29 itens validados, 13 classe A), mas protocolos, energia, testes de firmware, segurança IoT, drivers a partir de datasheet e Zephyr/FreeRTOS oficiais seguem sem fonte de qualidade, e a lente de comunidade não alcançou redes sociais.


---

# ADENDO — rodada gapfill (complemento `gapfill.md`) — VALIDADO

Data: 2026-10-10 · Validador: claude-sonnet-5-5 (pesquisador do complemento: claude-haiku-5-5; independência vem do modelo distinto e da re-leitura das fontes com ferramentas) · Itens recebidos: 35 (R-gap-01 a R-gap-34 e R-gap-34b) · Aprovados: 32 (fundidos em 34 itens V-30 a V-63, incluindo 6 itens que o validador acrescentou por leitura nova) · Rejeitados como item autônomo: 3 (R-gap-21, R-gap-26, R-gap-34b) · URLs/endpoints re-verificados: cerca de 90 · Limitações: orçamento de WebSearch do turno esgotado (nenhuma busca possível, então Reddit/X/YouTube e AGENTS.md de Rust no_std seguem sem cobertura); API do GitHub recusou (403 no WebFetch; limite de taxa em chamada direta e `gh` sem login), então datas de push continuam Não verificáveis; estrelas e licenças vêm das páginas HTML.

Rótulos: Verificado (lido por mim nesta execução) · Inferido · Suposição · Não verificável.

## Estatísticas do adendo

| Item | Valor |
| --- | --- |
| Recebidos (gapfill) | 35 |
| Aprovados (inclui fundidos e rebaixados de classe) | 32 |
| Rebaixados de classe ou de uso | 6 (R-gap-06 e R-gap-07 para B5 como referência; R-gap-14 para B5; R-gap-15 para B6; R-gap-30 para referência; R-gap-34 para B6) |
| Rejeitados como item autônomo | 3 (R-gap-21 fundido em V-46 por ser comparação Inferida; R-gap-26 substituído por leitura nova em V-52; R-gap-34b é só metadado, absorvido na tabela abaixo) |
| Itens classe A (todos re-verificados) | R-gap-01, 02, 03, 04, 05, 09, 13, 16, 17, 18, 19, 20, 22, 24, 25, 32, 33: 17 de 17 (100%) |
| Re-verificação total | 32 de 35 itens com leitura da fonte (91%); não re-lidos: R-gap-08 e R-gap-21 (derivados, conferidos por consistência com as fontes lidas) e R-gap-12 em parte (data) |
| Itens novos do validador | V-32, V-38, V-43, V-51, V-61, V-63 e partes de V-48, V-50, V-52, V-57, V-59, V-62 |
| Média Prompt-score do conteúdo reutilizável reescrito | 79,9 (34 itens; 28 com 80 ou mais; 6 abaixo de 80 e usados só como referência, não como prompt) |

Todas as fontes classe A foram conferidas afirmação por afirmação. Nenhuma URL do complemento era inexistente; 2 URLs que o complemento citava de forma indireta falharam (ver "Correções adversariais").

## Correções adversariais importantes (o que o pesquisador errou, exagerou ou deixou frouxo)

1. **R-gap-13 (sleep do ESP-IDF):** o complemento diz que Wi-Fi e Bluetooth "não sobrevivem ao deep-sleep". A página diz mais: os periféricos de rádio ficam desligados em **light-sleep e em deep-sleep**, e a conexão não é mantida mesmo sem chamar stop/deinit; para manter conexão, usar modem-sleep com light-sleep automático (Verificado). O pulso de wake-up de "3 ciclos do RTC slow clock" vem da nota de `esp_sleep_enable_gpio_wakeup_on_hp_periph_powerdown()`, não é regra geral de todas as fontes; o tempo do ciclo depende de `CONFIG_RTC_CLK_SRC` (cerca de 7,4 µs no RC_SLOW e 30,5 µs no XTAL32K, segundo a página). `esp_pm_lock` de fato não aparece (confirmado).
2. **R-gap-25 (interrupções do Zephyr):** "zero-latency só em Cortex-M" é impreciso. A página diz que o zero-latency está "currently implemented" no Cortex-M, mas não diz "somente"; ISR direta depende de `CONFIG_ARCH_HAS_DIRECT_INTERRUPTS` e o build falha onde não há suporte; zero-latency exige ainda `CONFIG_ZERO_LATENCY_IRQS`, `IRQ_ZERO_LATENCY` e proibe `ISR_DIRECT_PM`. `k_sem_give` não aparece (confirmado). A preferência por `k_irq_enable()`/`k_irq_lock()` está correta (a página chama os nomes sem prefixo de "legacy").
3. **R-gap-19 (secure boot v2):** o complemento diz que a página "recomenda assinatura remota". O texto é mais fraco: "can be good practice to use a remote signing server". Para o modo de download pela UART a página diz "It is recommended to disable"; JTAG e o interpretador BASIC aparecem na lista de boas práticas, e o JTAG já é desabilitado por padrão via eFuse quando o secure boot liga. A página cobre só o ESP32 (v3.0 em diante) e não usa "irreversível" nem "one-time" (confirmado). A chave pública RSA-3072 tem digest em eFuse; a página exige bit de proteção de escrita ligado e **proteção de leitura desligada**.
4. **R-gap-02 (I2C do ESP-IDF):** a frase "funcionalidade experimental" vale para a **transação assíncrona do mestre**, não para o driver inteiro. A página tem uma inconsistência interna (cita `on_recv_done` no texto e `on_trans_done` na estrutura). O controlador do ESP32 não faz clock stretching quando é escravo, e `scl_wait_us` é o tempo de espera do mestre (0 usa o padrão de registrador); o "cerca de 12 ms" é dito como "possível" pela página, não como limite.
5. **R-gap-03 (TWAI):** a página diz "129 consecutive recessive bits (11 bits each)". A redação é ambígua entre 129 sequências de 11 bits e 129 bits; o complemento escolheu uma leitura sem avisar. Tratar como Não verificável o número exato e usar a regra "a aplicação chama `twai_node_recover()` de uma task e espera `on_state_change`". A página é multi-alvo e documenta API de FD (`fdf`, `brs`, `data_timing`), embora diga que o controlador do ESP32 interpreta frames FD como erro; não generalizar para outras variantes. `twai_node_recover()` devolve `ESP_ERR_INVALID_STATE` se o nó **não** está em bus-off.
6. **R-gap-33 (`-fstack-usage`):** `dynamic` significa que a função também ajusta a pilha dentro do corpo; `bounded` indica que o compilador conseguiu limitar o ajuste, e então o segundo campo é o limite superior total. Sem `bounded`, o valor cobre só a parte estaticamente limitada. O complemento disse "sem limite conhecido", o que é uma simplificação aceitável, mas a regra correta é: valor de `dynamic` sem `bounded` é piso, não teto.
7. **R-gap-26 (FreeRTOS):** as páginas `freertos.org/Documentation/...` **existem** (os títulos "FreeRTOS stack usage and stack overflow checking" e "FreeRTOS Kernel Developer Docs" voltam), mas o corpo é renderizado no cliente e não pôde ser lido. A lacuna foi fechada por outra rota: o repositório oficial `FreeRTOS/FreeRTOS-Kernel-Book` (capítulos 7, 12 e 13 lidos) e o cabeçalho `stack_macros.h` do kernel (MIT). Discrepância: o Book diz que o método 2 confere "os últimos 20 bytes" da pilha; o cabeçalho confere as quatro primeiras palavras `0xa5a5a5a5`. Não citar o número de bytes.
8. **R-gap-15 (OWASP IoT):** o link do PDF "OWASP IoT Top 10 2018" listado pela página do projeto (`www.owasp.org/images/1/1c/OWASP-IoT-Top-10-2018-final.pdf`) retorna **404** (domínio antigo). As dez categorias continuam não lidas e não devem ser citadas. A página do projeto é "Lab Project", licença MIT, sem data de versão (Verificado). ISVS está em **release candidate 1.0.0-RC2** e se declara "not yet a finalized standard" (Verificado); licença CC BY-SA 4.0 (destilar).
9. **R-gap-16 e R-gap-17 (NIST):** a URL da Rev. 1 foi localizada e lida: https://csrc.nist.gov/pubs/ir/8259/r1/final, "Foundational Cybersecurity Activities for IoT Product Manufacturers", publicada em abril de 2026 (histórico: 20/04/2026, Final). A página da Rev. 1 **não enumera** as atividades; não atribuir "seis atividades" a ela sem abrir o PDF. A página da 8259A lista a Rev. 1 entre as partes da série.
10. **R-gap-18 (MCUboot):** o modo swap-using-scratch "não é recomendado" e a página sugere swap-using-offset ou swap-using-move (Verificado); a página tem uma tabela de custódia de chave em que a chave privada de produção fica em "HSM, signing ceremony, release team only". Os dois nomes de Kconfig para a chave seguem sem esclarecimento na página (conferir na árvore do Zephyr).
11. **R-gap-12 e R-gap-11 (Ceedling e CMock):** o README do Ceedling diz que a versão mais recente é 1.1.10 (sem data); o gem local instala as dependências e `ceedling new --local` copia Unity, CMock e CException em `vendor/`. O CMock em zip exige Unity e CException; o uso de Ruby é confirmado pela página de unit tests do ESP-IDF ("CMock requires Ruby, Linux or macOS"), não pela página do CMock.
12. **R-gap-27 (Embassy):** licença resolvida: o README diz "licensed under either of Apache 2.0 or MIT, at your option"; a documentação fica em CC-BY-SA (arquivo LICENSE-CC-BY-SA). "Apache-2.0 and 2 other licenses" é o rótulo do GitHub.
13. **R-gap-14 (Zephyr PM):** a página mostra "Last source update: Apr 04, 2022", fonte antiga para o assunto, confirmando a ressalva do complemento. Rebaixado para B (5). Não há seção de medição de energia.
14. **R-gap-34 (safety do Zephyr):** o índice não cita norma, mas a subpágina **Safety Overview cita IEC 61508**: o projeto declara como **objetivo** obter certificação IEC 61508 (SIL 3 / SC 3) para um escopo limitado de código, com o escopo ainda "TBD"; guidelines de código estão no estágio I concluído e o estágio II em andamento. É meta, não certificação obtida. O complemento afirmou "não declara norma"; isso valia só para o índice.
15. **R-gap-09 (ztest):** a página não diz que `--seed` exige `CONFIG_ZTEST_SHUFFLE`; diz que o embaralhamento imprime a seed e que ela pode ser repassada ao Twister em builds do native simulator. O texto "só Linux" é literal: "Running unit tests is therefore only supported for Linux."
16. **R-gap-06 (Bluetooth do Zephyr):** a URL do complemento (`/latest/connectivity/bluetooth/index.html`) é só um redirecionamento ("Page has moved here"); a URL final `/latest/services/connectivity/bluetooth/index.html` foi lida (índice com Supported features, Qualification, Stack Architecture, LE Host, LE Audio, LE Controller, Application Development, API, Tools, Shell). Não menciona Mesh.
17. **Metadados GitHub (R-gap-34b):** a API recusa; os números abaixo vêm das páginas HTML lidas por mim. Datas de push continuam Não verificáveis para todos.

| Repositório | Estrelas | Licença | Observação (Verificado na página) |
| --- | --- | --- | --- |
| ThrowTheSwitch/Unity | 5,4 mil | MIT | 1.474 commits; sem releases listados |
| ThrowTheSwitch/CMock | 844 | MIT | 991 commits |
| ThrowTheSwitch/Ceedling | 856 | MIT | 3.349 commits; README cita 1.1.10 |
| mcu-tools/mcuboot | 2,2 mil | Apache-2.0 | 3.091 commits; README cita 2.5.0-rc1 |
| embassy-rs/embassy | 9,9 mil | MIT ou Apache-2.0 (README); docs CC-BY-SA | 17.927 commits |
| rust-embedded/svd2rust | 860 | Apache-2.0 e MIT | 1.550 commits; tópico `cmsis-svd` |
| rust-embedded/book | 1,3 mil | texto CC-BY-SA-4.0; código MIT e Apache-2.0 | 594 commits |
| anthropics/claude-plugins-official | 37,6 mil | Apache-2.0 | 4.379 commits; `/plugins` (Anthropic) e `/external_plugins` (terceiros) |
| FreeRTOS/FreeRTOS-Kernel | 4,5 mil | MIT | 3.680 commits; README cita V11.1.0 (LTS 202406.00) |
| FreeRTOS/FreeRTOS-Kernel-Book | 592 | CC BY-SA 4.0 (LICENSE) e MIT-0 para exemplos | capítulos `ch01.md` a `ch13.md` |
| OWASP/IoT-Security-Verification-Standard-ISVS | 161 | CC BY-SA 4.0 | v1.0 RC2; badge de data: outubro de 2025 |
| scriptingxss/owasp-fstm | 498 | CC BY-SA 4.0 | 58 commits; metodologia de 9 estágios |
| trailofbits/claude-code-config | 2,1 mil | **não exibida na página** (tratar como sem licença: só destilar) | 36 commits |
| Zachariah9420/embedded-systems-architect | 5 | MIT | 5 commits; SKILL.md na raiz |
| SensorsIot/Embedded-AI-Harness | 188 (rodada anterior) | MIT | 18 skills em `.claude/skills` |

`atillab1` não foi tentado de novo: o repositório não tem uso em nenhum item aprovado.

## Itens aprovados (continuação da numeração)

### V-30 — I2C: timeout, NACK, pull-up, ISR e thread safety (origem R-gap-01, R-gap-02) — Classe A (9)
- **Lente:** gapfill · **Tipo:** checklist · reference
- **Fontes:** https://docs.zephyrproject.org/latest/hardware/peripherals/i2c.html e https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/i2c.html
- **Sinais:** documentação oficial, existe; Zephyr é Apache-2.0 (Inferido); licença da página do ESP-IDF não verificada.
- **Técnicas-chave (Verificado):** Zephyr: timeout por controlador em `zephyr,transfer-timeout-ms`, depois `CONFIG_I2C_TRANSFER_TIMEOUT_MS`, depois `K_FOREVER` se o valor for 0 (alguns drivers que gravam o timeout direto no hardware rejeitam 0 no build); erro `-ETIMEDOUT`; API de controller estável e de target experimental; terminologia NXP I2C Rev 7.0. ESP-IDF: pull-up externo de 1 kΩ a 10 kΩ (2 kΩ a 5 kΩ preferido, não abaixo de 1 kΩ), pull-up interno insuficiente para alta velocidade; SCL de mestre até 400 kHz; `xfer_timeout_ms` de -1 espera indefinidamente (desaconselhado no probe); erros `ESP_ERR_INVALID_RESPONSE` (NACK), `ESP_ERR_TIMEOUT`, `ESP_ERR_NOT_FOUND`; callbacks em ISR sem bloqueio e com APIs `FromISR`; criação de barramento e as transferências do mestre são thread safe, as demais funções exigem mutex; modo assíncrono é experimental e só um dispositivo por barramento.
- **Conteúdo reutilizável (redação própria, reescrito):**
  - Papel: revisor de driver I2C. Entrada: arquivos do driver e a página do SoC citada. Para cada chamada I2C, verifique: (1) `-ETIMEDOUT`/`ESP_ERR_TIMEOUT` e NACK têm caminho de erro explícito; (2) o timeout cobre o pior caso do dispositivo (ciclo de escrita interno de EEPROM, clock stretching do escravo) e não usa espera infinita sem justificativa; (3) pull-up externo está dimensionado e foi medido na placa (o interno não vale em 400 kHz); (4) callback de ISR não bloqueia; (5) acesso concorrente ao mesmo barramento tem mutex. Saída: tabela com achado, regra, arquivo:linha, gravidade e como verificar; marque cada afirmação sobre o chip como Verificado, Inferido ou Não verificável; sem fonte do datasheet, pare e pergunte.
- **Ressalvas:** nenhuma das duas páginas trata de bus recovery; recuperação de barramento travado é Inferido. Valores de timeout e pull-up vêm do datasheet e da medição.
- **Verificação:** as duas páginas lidas por mim; 14 afirmações conferidas; correção 4 acima.
- **Prompt-score:** 83 (D1 4, D2 4, D3 5, D4 4, D5 3, D6 4, D7 5, D8 4, D9 4, D10 5, D11 4, D12 4).

### V-31 — CAN no ESP-IDF (TWAI): estados de erro, bus-off e filtros (origem R-gap-03) — Classe A (8)
- **Fonte:** https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/twai.html
- **Técnicas-chave (Verificado):** Error Active (contadores abaixo de 96), Error Warning (96 a 127), Error Passive (128 ou mais), Bus Off (TEC de 256 ou mais; só o TEC define bus-off); `twai_node_recover()` só de task, a recuperação não é imediata e termina em `on_state_change`; `twai_node_transmit()` devolve `ESP_ERR_INVALID_STATE` em bus-off; um filtro de máscara no ESP32 (bit 1 deve coincidir, bit 0 é ignorado; ID e máscara 0 aceita tudo), modo dual com dois filtros de 16 bits (em ID de 29 bits só os 16 bits altos são filtrados); `twai_node_config_mask_filter()` com nó desabilitado; transceiver externo obrigatório (exemplo TJA105x), salvo teste de nó único com TX e RX em curto.
- **Conteúdo reutilizável (redação própria):** regra: todo nó CAN registra `on_state_change`, trata Bus Off e agenda a recuperação em task com limite de tentativas e atraso; o buffer de transmissão assíncrona fica válido até `on_tx_done`; o filtro de máscara é configurado com o nó desabilitado e testado com IDs dentro e fora da máscara. Taxa de bits, terminação de 120 ohm e transceiver vêm do datasheet do transceiver e do barramento (Não verificável nesta fonte).
- **Ressalvas:** correção 5 (129 bits ambíguo; API de FD é multi-alvo).
- **Verificação:** página lida; sete afirmações conferidas, duas com nuance.
- **Prompt-score:** 82 (D5 2).

### V-32 — SPI e UART: drivers do ESP-IDF e do Zephyr (adicionado pelo validador; lacuna 1 do complemento) — Classe A (8)
- **Fontes:** https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/spi_master.html, https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/uart.html, https://docs.zephyrproject.org/latest/hardware/peripherals/uart.html, https://docs.zephyrproject.org/latest/hardware/peripherals/spi.html
- **Técnicas-chave (Verificado):**
  - SPI mestre ESP-IDF: buffers em memória interna compatível com DMA e alinhados a 32 bits (comprimento múltiplo de 4); buffer desalinhado força cópia temporária; `max_transfer_sz` padrão 4092 com DMA e, sem DMA, o tamanho do FIFO (normalmente 64 bytes); transação por polling termina antes e prende a CPU, por interrupção libera a CPU e demora mais, e a página recomenda um só tipo por dispositivo; thread safe só se cada dispositivo tem uma task, senão mutex; só o ISR fica em IRAM por padrão e callbacks com `ESP_INTR_FLAG_IRAM` precisam estar em IRAM; limites típicos de clock no ESP32: 80 MHz (IO_MUX) e 26 MHz (GPIO matrix); `cs_ena_pretrans` é incompatível com as fases de comando e endereço em full-duplex.
  - UART ESP-IDF: buffer RX maior que o FIFO de hardware; `UART_BUFFER_FULL`, `UART_FIFO_OVF`, `UART_FRAME_ERR`, `UART_PARITY_ERR` e `UART_BREAK` chegam como eventos na fila; não passar `ESP_INTR_FLAG_IRAM` ao instalar o driver; fluxo de controle por hardware (RTS/CTS) ou software (XON 0x11, XOFF 0x13); a página não declara garantia geral de thread safety.
  - UART Zephyr: três APIs (polling, interrupt-driven, assíncrona com DMA); interrupt-driven e assíncrona **não** devem ser usadas ao mesmo tempo no mesmo periférico (`CONFIG_UART_EXCLUSIVE_API_CALLBACKS` ligado por padrão); `uart_poll_out()` bloqueia. A página SPI do Zephyr é só terminologia (controller/peripheral; nomes master/slave deprecados desde a v4.5, remoção prevista na v5.0) e remete ao Doxygen para a API.
- **Conteúdo reutilizável (redação própria):** checklist de SPI e UART: erro de FIFO, quadro e paridade tem tratamento; buffers DMA alinhados e em RAM interna; um só estilo de transação por dispositivo; um dono por dispositivo ou mutex; ISR e callbacks sem bloqueio e, se o flash puder ser escrito durante a operação, em IRAM; UART com buffer de RX dimensionado para a taxa e política para `BUFFER_FULL`.
- **Ressalvas:** a API de SPI do Zephyr (campos de `spi_config`, `spi_transceive`, retorno `-errno`) não foi lida; fica para consulta no Doxygen. Falta Linux, Arduino e outros SoCs.
- **Verificação:** quatro páginas lidas; a de SPI do Zephyr não trouxe a API (registrado).
- **Prompt-score:** 82.

### V-33 — MQTT 3.1.1 e 5.0 (OASIS) (origem R-gap-04, R-gap-05) — Classe A (9)
- **Fontes:** https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html (OASIS Standard, 29/10/2014) e https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html (OASIS Standard, 07/03/2019)
- **Técnicas-chave (Verificado, com número de regra):**
  - 3.1.1: Keep Alive: o cliente envia PINGREQ se não há outro pacote [MQTT-3.1.2-23]; o servidor desconecta após 1,5 vez o intervalo [MQTT-3.1.2-24]; zero desliga o mecanismo. Will QoS 0 quando will flag é 0 [MQTT-3.1.2-13]; Will é publicado em desconexão anormal e descartado após DISCONNECT. CleanSession 1 descarta sessão [MQTT-3.1.2-6]; 0 retoma ou cria sessão [MQTT-3.1.2-4]. Packet Identifier não zero em SUBSCRIBE, UNSUBSCRIBE e PUBLISH com QoS maior que 0 [MQTT-2.3.1-1], mesmo identificador no reenvio, DUP em 1 no reenvio [MQTT-3.3.1-1]. QoS 1: PUBACK com o mesmo identificador [MQTT-4.3.2-2]. QoS 2: PUBLISH, PUBREC, PUBREL, PUBCOMP, sem reenviar o PUBLISH depois do PUBREL [MQTT-4.3.3-1]. Reenvio obrigatório só ao reconectar com CleanSession 0 [MQTT-4.4.0-1]. Curingas só em filtros, `#` por último e sozinho, `+` ocupa um nível inteiro, filtros com curinga não casam tópico começado por `$` [MQTT-4.7.x]. Violação de protocolo fecha a conexão [MQTT-4.8.0-1]. Segurança (capítulo 5, não normativo): TLS, porta 8883, evitar cifra NULL, autenticação e autorização no servidor.
  - 5.0: Server Keep Alive no CONNACK substitui o do cliente [MQTT-3.1.2-21]; Will Delay Interval: se a sessão reconecta antes do atraso, o will não sai [MQTT-3.1.3-9]; Clean Start 1 descarta sessão; Session Expiry Interval 0xFFFFFFFF significa sem expirar; Topic Alias Maximum zero ou ausente proíbe alias; pacote acima do Maximum Packet Size é Protocol Error com DISCONNECT 0x95.
- **Conteúdo reutilizável (redação própria, reescrito):** checklist de cliente MQTT para dispositivo: (1) versão do protocolo registrada (3.1.1 ou 5.0); (2) keep alive justificado pela rede e pela bateria, com PINGREQ tratado; (3) will com tópico de status e retain definido; (4) sessão (CleanSession ou Clean Start e Session Expiry) escolhida de forma consciente, sabendo que mensagens QoS 1 e 2 só persistem com sessão; (5) QoS 1 pode duplicar, então o consumidor é idempotente; (6) reconexão com backoff e jitter; (7) TLS na porta 8883 com validação de certificado, credenciais fora do firmware versionado; (8) buffer de recepção dimensionado para o Maximum Packet Size (Inferido). Saída: tabela por item com Verificado, Inferido ou Não verificável.
- **Ressalvas:** a leitura do MQTT 5.0 cobriu as primeiras 100 mil de 206 mil caracteres (seções de QoS e reenvio do 5.0 não lidas); as regras de QoS acima são do 3.1.1. Cuidado: o 3.1.1 não exige que o cliente **nunca** reenvie fora da reconexão; só impõe DUP e a regra do QoS 2.
- **Verificação:** as duas páginas lidas; 3.1.1 lido até o capítulo 5; ver a ressalva acima.
- **Prompt-score:** 83.

### V-34 — Bluetooth LE: índice do Zephyr e NimBLE no ESP-IDF (origem R-gap-06, R-gap-07) — Classe B (5), rebaixado de B (7) como fonte de regra
- **Fontes:** https://docs.zephyrproject.org/latest/services/connectivity/bluetooth/index.html e https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/bluetooth/nimble/index.html
- **Técnicas-chave (Verificado):** Zephyr tem pilha BLE completa "from application to radio hardware" e partes do host Classic (BR/EDR), com subpáginas Supported features, Qualification, Stack Architecture, LE Host, LE Audio, LE Controller, API, Tools e Shell; NimBLE (Apache MyNewt) é a pilha BLE configurável e qualificável pelo Bluetooth SIG, host portado ao FreeRTOS, controller acessado por VHCI (`esp_nimble_hci_init()`), thread do host criada em `nimble_port_freertos_init` e substituível; "most features of NimBLE including BLE Mesh are supported".
- **Conteúdo reutilizável:** item de decisão (qual pilha, qual papel, qual controller, versão) em vez de regra. Nenhuma regra de MTU, conexão ou segurança BLE tem fonte validada. Para esses, a pista é ler `LE Host` do Zephyr e as skills `testbench-ble` (V-61).
- **Ressalvas:** só índices; sem footprint, sem roles. Não use como fonte para MTU ou parâmetros de conexão.
- **Prompt-score:** 68 (referência, não prompt).

### V-35 — Checklist de revisão de barramento e protocolo (origem R-gap-08) — Classe B (6)
- **Fonte:** síntese de V-30, V-31, V-32 e V-33 (fontes oficiais lidas por mim).
- **Conteúdo reutilizável (redação própria, reescrito):** "Antes de aprovar driver de barramento ou cliente de rede, responda para cada item com Verificado, Inferido ou Não verificável e cite a fonte: (1) todo erro (timeout, NACK, bus-off, FIFO overflow, desconexão) tem caminho explícito e teste; (2) timeouts cobrem o pior caso do periférico; (3) elétrica (pull-up, terminação, transceiver) foi medida e vem do datasheet; (4) recuperação de bus-off e de barramento travado roda em task, com limite de tentativas e atraso (I2C: Inferido); (5) callbacks de ISR não bloqueiam; (6) DMA com buffer alinhado e em RAM válida; (7) acesso concorrente tem dono único ou mutex; (8) protocolos de rede têm keep alive, will, sessão e reconexão justificados; (9) o caminho de erro é exercitado em teste de host com HAL falsa ou em bancada. Saída: tabela com achado, item, arquivo:linha, gravidade e como verificar. Se faltar o datasheet, pare e pergunte."
- **Ressalvas:** SPI e UART agora têm fonte (V-32); pull-up de linha CAN e terminação continuam sem fonte.
- **Prompt-score:** original 62; reescrito 85 (D1 4, D2 4, D3 5, D4 4, D5 3, D6 5, D7 5, D8 4, D9 4, D10 5, D11 4, D12 4).

### V-36 — Testes no Zephyr: ztest e twister (origem R-gap-09) — Classe A (9)
- **Fonte:** https://docs.zephyrproject.org/latest/develop/test/ztest.html
- **Técnicas-chave (Verificado):** `ZTEST_SUITE` com predicate, setup, before, after e teardown; `ZTEST`, `ZTEST_F` (fixture), `ZTEST_P` (parametrizado), `ZTEST_USER`; `zassert_*` interrompe, `zexpect_*` registra e continua, `zassume_*` pula; `native_sim` constrói o SO completo para o host; `unit_testing` constrói só o código testado e o Ztest (`type: unit`) e funciona **só em Linux**; Twister com `--seed` para reproduzir a ordem embaralhada; teste inaplicável usa `ztest_test_skip()` ou `Z_TEST_SKIP_IFDEF`.
- **Conteúdo reutilizável (redação própria):** regra: lógica de domínio no modo `unit_testing` com stubs; driver em `native_sim` ou na placa; em Windows ou macOS, rodar `unit_testing` em container ou VM Linux; teste inaplicável é skipped, não omitido.
- **Ressalvas:** correção 15. Não citar a sintaxe do `testcase.yaml` sem reler a versão.
- **Prompt-score:** 83.

### V-37 — Unity, CMock e Ceedling (origem R-gap-10, R-gap-11, R-gap-12) — Classe B (7)
- **Fontes:** https://github.com/ThrowTheSwitch/Unity (5,4 mil estrelas, MIT, "Simple unit testing for C"), https://github.com/ThrowTheSwitch/CMock (844, MIT, "Mock/stub generator for C"), https://github.com/throwtheswitch/ceedling (856, MIT, "Unit testing and build system for C projects")
- **Técnicas-chave (Verificado):** Unity: asserções de inteiros de largura fixa, hex, arrays, floats, strings, ponteiros, memória e sufixo `_MESSAGE`; CMock gera mocks de headers C e funciona com Unity; Ceedling une Unity e CMock, instala dependências no gem local e copia para `vendor/` com `ceedling new --local`; página do ESP-IDF confirma que CMock requer Ruby.
- **Conteúdo reutilizável (redação própria):** padrão "HAL falsa no host": a interface do driver é um header; CMock gera o mock; o teste verifica a sequência de chamadas e os retornos de erro; uma asserção por comportamento, com mensagem própria quando o caso não é óbvio.
- **Ressalvas:** datas de commit Não verificáveis; Ceedling com toolchain cruzado é Inferido (confirmar na documentação de configuração).
- **Prompt-score:** 78.

### V-38 — Testes no ESP-IDF: Unity, CMock no host e pytest-embedded (adicionado pelo validador) — Classe A (8)
- **Fontes:** https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/unit-tests.html e https://docs.espressif.com/projects/pytest-embedded/en/latest/
- **Técnicas-chave (Verificado):** testes em alvo usam Unity (`TEST_CASE("nome", "[modulo]")` em arquivos `test_*.c`, `unity` em `REQUIRES`); testes no host Linux usam mocks (CMock) e só alguns componentes suportam; `TEST_CASE_MULTIPLE_DEVICES` (até cinco DUTs) e `TEST_CASE_MULTIPLE_STAGES` (etapas que atravessam reset, como o motivo do reset após deep sleep); preferir macros de capacidade de `soc_caps.h` a nomes de chip; a página recomenda pytest-embedded para CI. pytest-embedded 2.x: serviços `serial`, `esp`, `idf` (grava o binário automaticamente), `qemu` e `wokwi`; fixture `dut` com `expect`; fixar `pytest-embedded~=2.0`.
- **Conteúdo reutilizável (redação própria):** definição de pronto de teste de firmware ESP-IDF: caso de host (mock) para a lógica; caso em alvo para periférico; caso multi-estágio para sleep e reset; execução em CI com pytest-embedded; **gravar na placa e rodar em bancada exige confirmação do usuário** (o serviço `idf` grava sozinho).
- **Ressalvas:** a página do pytest-embedded não diz licença nem usa o termo HIL; HIL é o uso com o serviço `idf` e placa real (Inferido).
- **Prompt-score:** 85.

### V-39 — Sleep modes do ESP-IDF (origem R-gap-13) — Classe A (9)
- **Fonte:** https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/sleep_modes.html
- **Técnicas-chave (Verificado):** light-sleep: periféricos digitais e CPUs com clock gating e tensão reduzida, estados internos preservados; deep-sleep: CPUs, a maior parte da RAM e os periféricos digitais desligados, ficam RTC controller, ULP e RTC FAST e SLOW; rádio (Wi-Fi/BT) desligado em **ambos**; para manter conexão, modem-sleep com light-sleep automático; fontes de wake-up: timer, touchpad, ext0, ext1, ULP, GPIO, UART (só light-sleep); `rtc_gpio_isolate()` antes de `esp_deep_sleep_start()` evita corrente por pull interno.
- **Conteúdo reutilizável (redação própria):** critério de energia: a tabela ativo/light/deep tem corrente **medida na própria placa** com instrumento adequado (multímetro de precisão ou analisador de consumo), com a firmware real, e o valor entra na definição de pronto; antes do deep-sleep, rádio parado, pinos isolados, dados que sobrevivem em memória RTC marcados e wake-up configurado.
- **Ressalvas:** correção 1. Sem valores de corrente nem tempos de wake-up na página.
- **Prompt-score:** 82.

### V-40 — Power management do Zephyr (índice) (origem R-gap-14) — Classe B (5), rebaixado de B (7)
- **Fonte:** https://docs.zephyrproject.org/latest/services/pm/index.html
- **Técnicas-chave (Verificado):** seções System PM, Device PM (estados, shell, busy, wakeup), Device Runtime PM, Power Domain e APIs; irmãs: CPU Frequency Scaling, Power off; rodapé "Last source update: Apr 04, 2022".
- **Conteúdo reutilizável:** checklist de configuração (qual camada controla cada periférico, quem precisa de wakeup, quais ficam sob runtime PM). Sem guia de medição.
- **Prompt-score:** 67 (referência).

### V-41 — OWASP IoT: projeto, ISVS e FSTM (origem R-gap-15) — Classe B (6)
- **Fontes:** https://owasp.org/www-project-internet-of-things/, https://github.com/OWASP/IoT-Security-Verification-Standard-ISVS, https://github.com/scriptingxss/owasp-fstm
- **Técnicas-chave (Verificado):** projeto Lab, MIT, recursos listados (Top 10 2018 em PDF com link quebrado, ISTG, FSTM, ISVS, IoTGoat v1.0); ISVS v1.0 RC2, CC BY-SA 4.0, capítulos V1 Ecossistema, V2 Aplicação de espaço de usuário, V3 Plataforma de software, V4 Comunicação, V5 Plataforma de hardware; FSTM de nove estágios (reconhecimento, obtenção do firmware, análise do firmware, extração do sistema de arquivos, análise do conteúdo, emulação, análise dinâmica, análise em execução, exploração de binários), CC BY-SA 4.0.
- **Conteúdo reutilizável (redação própria):** usar os cinco capítulos do ISVS como índice de perguntas de projeto (ecossistema, aplicação, plataforma, comunicação, hardware), sem copiar texto; FSTM é metodologia de ataque a firmware de terceiros e não deve virar skill sem aviso de uso autorizado.
- **Ressalvas:** correção 8. Top 10 2018 não lido, não citar categorias. ISVS ainda é RC.
- **Prompt-score:** 68 (referência).

### V-42 — NIST IR 8259, 8259A e Rev. 1 (origem R-gap-16, R-gap-17) — Classe A (9)
- **Fontes:** https://csrc.nist.gov/pubs/ir/8259/a/final (IR 8259A, "IoT Device Cybersecurity Capability Core Baseline", Final, 29/05/2020), https://csrc.nist.gov/pubs/ir/8259/final (IR 8259 retirado em 20/04/2026, substituído pela Rev. 1) e https://csrc.nist.gov/pubs/ir/8259/r1/final (IR 8259 Rev. 1, "Foundational Cybersecurity Activities for IoT Product Manufacturers", abril de 2026, Final)
- **Técnicas-chave (Verificado):** a 8259A define capacidades de dispositivo como ponto de partida e se usa com a 8259 (hoje Rev. 1); a Rev. 1 descreve atividades que o fabricante deve considerar antes de vender; a 8259A não contém as seis atividades; a página da Rev. 1 não as lista.
- **Conteúdo reutilizável (redação própria):** nota de vigência: "NISTIR 8259 (2020) foi retirado em 20/04/2026; usar a Rev. 1." Checklist por capacidade do Core Baseline como pergunta de produto: o dispositivo tem identificação, configuração, proteção de dados, controle de acesso lógico, atualização de software e consciência de estado? (os rótulos são os temas tradicionais da série; **conferir no PDF da 8259A antes de publicar o texto**, Inferido).
- **Ressalvas:** correção 9; 8259B e perfil federal não lidos.
- **Prompt-score:** 82.

### V-43 — ETSI EN 303 645 V2.1.1: requisitos de linha de base para IoT de consumo (adicionado pelo validador) — Classe A (8)
- **Fonte:** https://www.etsi.org/deliver/etsi_en/303600_303699/303645/02.01.01_60/en_303645v020101p.pdf (34 páginas, junho de 2020; o texto foi extraído localmente com PyMuPDF a partir do PDF salvo pela ferramenta; o WebFetch sozinho não decodifica)
- **Técnicas-chave (Verificado):** 13 provisões: 5.1 sem senha padrão universal, 5.2 gestão de relatos de vulnerabilidade, 5.3 manter o software atualizado, 5.4 armazenar parâmetros sensíveis com segurança, 5.5 comunicar com segurança, 5.6 minimizar superfície exposta, 5.7 garantir integridade do software, 5.8 proteger dados pessoais, 5.9 resiliência a quedas, 5.10 examinar telemetria, 5.11 facilitar apagar dados do usuário, 5.12 facilitar instalação e manutenção, 5.13 validar entradas. Exemplos de força: 5.1-1 diz "shall" (senhas únicas por dispositivo ou definidas pelo usuário); 5.3-1 diz "should" (componentes atualizáveis com segurança); 5.3-5 diz que o dispositivo "should" verificar atualizações após a inicialização e periodicamente; 5.5-8 exige gestão segura de parâmetros críticos.
- **Conteúdo reutilizável (redação própria):** checklist de 13 perguntas de produto, uma por provisão, distinguindo "shall" de "should" apenas quando o item cita o número da provisão; nunca reproduzir o texto da norma.
- **Ressalvas:** o ETSI se reserva todos os direitos; só títulos e paráfrase. Vale para IoT de **consumo**; conformidade legal não é afirmada pelo plugin.
- **Verificação:** PDF baixado pela ferramenta (867 KB) e lido por extração de texto; títulos e três provisões conferidos.
- **Prompt-score:** 80.

### V-44 — MCUboot no Zephyr: habilitar, assinar e custodiar chaves (origem R-gap-18; atualiza V-24) — Classe A (9)
- **Fontes:** https://docs.mcuboot.com/readme-zephyr.html e repositório https://github.com/mcu-tools/mcuboot (2,2 mil estrelas, Apache-2.0, 3.091 commits, README cita 2.5.0-rc1)
- **Técnicas-chave (Verificado):** `CONFIG_BOOTLOADER_MCUBOOT` no `prj.conf` ou `SB_CONFIG_BOOTLOADER_MCUBOOT` no sysbuild; partições `boot_partition`, `slot0_partition`, `slot1_partition` e `scratch_partition` (só no modo swap com scratch, "not recommended"; preferir swap-using-offset ou swap-using-move); assinatura automática com a chave configurada ou `scripts/imgtool.py`; chaves de exemplo do repositório "should never be used for production"; chave privada de produção em HSM e nunca sai dele.
- **Conteúdo reutilizável (redação própria):** regra de revisão: o build de produção falha se a chave de desenvolvimento estiver configurada; a chave privada nunca entra no repositório nem no `prj.conf`; partições e modo de swap estão no devicetree e casam com o plano de recuperação; **gerar chave de produção, assinar imagem de produção e gravar são ações humanas**.
- **Ressalvas:** correção 10. Guias por plataforma (nRF, STM32) ainda não lidos.
- **Prompt-score:** 85.

### V-45 — Secure Boot v2 do ESP-IDF: portão de produção (origem R-gap-19) — Classe A (9)
- **Fonte:** https://docs.espressif.com/projects/esp-idf/en/latest/esp32/security/secure-boot-v2.html
- **Técnicas-chave (Verificado):** RSA-PSS; a ROM verifica o bootloader de segundo estágio, que verifica cada app; digest da chave pública RSA-3072 em eFuse; bit de proteção de escrita ligado e **proteção de leitura desligada**; `CONFIG_SECURE_BOOT_V2_ALLOW_EFUSE_RD_DIS` mantém a possibilidade de proteger leitura de eFuse depois; "can be good practice" usar servidor de assinatura remoto; desabilitar o modo de download pela UART é "recommended"; JTAG desabilitado por padrão quando o secure boot liga; suportado no ESP32 v3.0 em diante.
- **Conteúdo reutilizável (redação própria):** portão: "habilitar secure boot só com plano de recuperação, chave fora do repositório, assinatura remota ou HSM e checklist de eFuse aprovado por um humano; o agente não gera nem executa comando de queima de eFuse". Nunca reproduzir comando de queima.
- **Ressalvas:** correção 3. Não use "irreversível" como se estivesse na página; o fato é "permanente na prática" (Inferido a partir da proteção de escrita).
- **Prompt-score:** 83.

### V-46 — OTA do ESP-IDF e comparação com MCUboot (origem R-gap-20, R-gap-21) — Classe A (9)
- **Fonte:** https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/ota.html (comparação com V-44: Inferida)
- **Técnicas-chave (Verificado):** duas partições OTA (`ota_0`, `ota_1`) mais `otadata` de dois setores (0x2000 bytes); estados NEW, PENDING_VERIFY, VALID, INVALID, ABORTED (e UNDEFINED); `esp_ota_mark_app_valid_cancel_rollback()` confirma; partição de fábrica não sofre rollback; confirmação automática é o padrão (`CONFIG_BOOTLOADER_APP_ROLLBACK_CONFIRM_ON_STARTUP`) e acontece após a inicialização dos componentes, pouco antes de `app_main`; `ESP_ERR_OTA_ROLLBACK_FAILED` quando não há app válida na outra partição; **anti-rollback** por versão de segurança em eFuse (`CONFIG_BOOTLOADER_APP_ANTI_ROLLBACK`), que exige confirmação controlada pela aplicação.
- **Conteúdo reutilizável (redação própria):** checklist de OTA: confirmação controlada pela app (autoteste de rede, sensores e barramentos principais antes de confirmar)? rollback testado em bancada? partição de fábrica mantida como recuperação? anti-rollback decidido de propósito, sabendo que usa eFuse (V-45: ação humana)? imagem assinada (V-45)? Tabela de decisão por plataforma: MCUboot usa slots no devicetree e swap com reversão (V-44, design em V-24); ESP-IDF usa `otadata` e estados de rollback (Inferido nas semelhanças).
- **Ressalvas:** a página não trata de assinatura da imagem OTA (coberta em V-45).
- **Prompt-score:** 87 (D1 4, D2 4, D3 5, D4 4, D5 3, D6 4, D7 5, D8 5, D9 4, D10 5, D11 4, D12 5).

### V-47 — embedded-hal 1.0 (origem R-gap-22) — Classe A (8)
- **Fonte:** https://docs.rs/embedded-hal/latest/embedded_hal/
- **Técnicas-chave (Verificado):** versão 1.0.0, MIT ou Apache-2.0; módulos `delay`, `digital`, `i2c`, `pwm` e `spi` (bloqueantes); `embedded-hal-async` (async/await) e `embedded-hal-nb` (polling com `nb`).
- **Conteúdo reutilizável (redação própria):** regra de driver: o driver é genérico sobre os traits (`I2c`, `SpiDevice`, `OutputPin`, `DelayNs`), não sobre o tipo de um HAL; testes usam implementação falsa dos traits; registre a versão do crate.
- **Ressalvas:** a versão pode ter avançado; conferir `latest`.
- **Prompt-score:** 80.

### V-48 — SVD, CMSIS-SVD e svd2rust (origem R-gap-23 mais leitura nova) — Classe B (7)
- **Fontes:** https://github.com/rust-embedded/svd2rust (860 estrelas, Apache-2.0 e MIT, 1.550 commits) e https://open-cmsis-pack.github.io/svd-spec/main/index.html
- **Técnicas-chave (Verificado):** svd2rust gera structs de mapa de registradores a partir de SVD; CMSIS-SVD formaliza os registradores mapeados em memória, campos de bits e interrupções de dispositivos Arm Cortex, mantido pelos fabricantes e distribuído em Device Family Packs; usos: visão de periférico no depurador e headers CMSIS.
- **Conteúdo reutilizável (redação própria):** regra "datasheet-first": nome de registrador, campo e interrupção vem do SVD da variante exata, com versão e origem do arquivo registradas; divergência entre SVD e manual de referência é achado, não decisão do modelo.
- **Ressalvas:** a página do SVD não declara licença nem versão; a página do svd2rust mal descreve o SVD.
- **Prompt-score:** 80.

### V-49 — Threads do Zephyr (origem R-gap-24) — Classe A (9)
- **Fonte:** https://docs.zephyrproject.org/latest/kernel/services/threads/index.html
- **Técnicas-chave (Verificado):** valor numérico menor tem precedência; cooperativas de `-CONFIG_NUM_COOP_PRIORITIES` a -1, preemptivas de 0 a `CONFIG_NUM_PREEMPT_PRIORITIES - 1`; meta-IRQ via `CONFIG_NUM_METAIRQ_PRIORITIES` na ponta mais alta do espaço cooperativo; `K_THREAD_STACK_DEFINE`; `k_thread_stack_space_get()` exige `CONFIG_INIT_STACKS` e `CONFIG_THREAD_STACK_INFO`; `CONFIG_THREAD_RUNTIME_STACK_SAFETY` com limiar por thread e handler.
- **Conteúdo reutilizável (redação própria):** checklist: prioridade justificada por escrito; pilha medida no pior caso com `k_thread_stack_space_get()` em build de teste; limiar de alerta ligado; padrões e faixa de prioridades conferidos no Kconfig da versão (a página não traz os padrões).
- **Prompt-score:** 83.

### V-50 — Interrupções e workqueue do Zephyr (origem R-gap-25 mais leitura nova) — Classe A (9)
- **Fontes:** https://docs.zephyrproject.org/latest/kernel/services/interrupts.html e https://docs.zephyrproject.org/latest/kernel/services/threads/workqueue.html
- **Técnicas-chave (Verificado):** ISR roda em contexto de interrupção; com IRQ lock só funções "isr-ok"; `IRQ_CONNECT` seguido de `irq_enable()` (nomes `k_irq_*` preferidos em código novo); `irq_connect_dynamic()` exige `CONFIG_DYNAMIC_INTERRUPTS`; ISR direta e zero-latency dependem de suporte de arquitetura (correção 2); trabalho demorado vai para thread auxiliar ou work item. Workqueue: o item reenfileirado enquanto pendente roda uma vez; a fila do sistema tem prioridade cooperativa a mais baixa por padrão e um handler bloqueante atrasa os demais; `k_work_cancel()` explicitamente seguro em ISR; `k_work_schedule()` e `k_work_reschedule()` podem ser chamados de ISR; `k_work_flush()`, `k_work_cancel_sync()` e `k_work_queue_drain()` só em thread; checar retorno e não "otimizar" com `k_work_is_pending()`.
- **Conteúdo reutilizável (redação própria):** checklist de ISR Zephyr: só chamar API marcada isr-ok (conferir na terminologia do Zephyr, que não foi lida); trabalho demorado vai para `k_work` ou thread; handler de work não bloqueia sem caminho de saída; direct ISR só com justificativa e medição de latência.
- **Ressalvas:** a lista isr-ok não foi lida; `k_sem_give` não confirmado.
- **Prompt-score:** 85.

### V-51 — Kconfig e west no Zephyr (adicionado pelo validador; devicetree fica pendente) — Classe A (8)
- **Fontes:** https://docs.zephyrproject.org/latest/build/kconfig/tips.html, https://docs.zephyrproject.org/latest/build/kconfig/index.html, https://docs.zephyrproject.org/latest/develop/west/index.html, https://docs.zephyrproject.org/latest/develop/west/build-flash-debug.html
- **Técnicas-chave (Verificado):** Kconfig: usar `depends on`, `select` só para símbolos auxiliares sem dependências (exceção para driver de barramento que seleciona o driver do barramento), `imply` para padrão desabilitável, nunca usar Kconfig para pino, nome de dispositivo ou barramento fixo (isso é devicetree), símbolos "presos" em `.config`, atribuições a símbolos sem prompt são ignoradas, `scripts/kconfig/lint.py` para símbolos inalcançáveis. West: `west build -b <BOARD>` (`-p` para pristine), `west flash` e `west debug` reconstroem por padrão e usam `--runner`; `--erase` apaga a flash antes e a página não traz aviso de perda de dados; `west flash -H` lista os runners.
- **Conteúdo reutilizável (redação própria):** regra: após mudar `prj.conf`, conferir o `.config` final para ver se o símbolo foi aplicado (símbolo com dependência não satisfeita é ignorado sem erro; Inferido a partir da página de dicas); hardware fixo vive no devicetree; `west flash`, `west debug` e `--erase` são ações de gravação e exigem confirmação do usuário.
- **Ressalvas:** a página de devicetree tentada (`/latest/build/dts/intro-input-and-output.html`) é 404; devicetree fica como lacuna. Nenhuma página de west lida cobre `west twister`.
- **Prompt-score:** 83.

### V-52 — FreeRTOS: ISR, prioridades, pilha e configASSERT (origem R-gap-26 substituído por leitura nova) — Classe B (7)
- **Fontes:** https://github.com/FreeRTOS/FreeRTOS-Kernel-Book (capítulos `ch07.md`, `ch12.md`, `ch13.md`; CC BY-SA 4.0; 592 estrelas), https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/stack_macros.h (MIT, Amazon) e https://github.com/FreeRTOS/FreeRTOS-Kernel (4,5 mil estrelas, MIT)
- **Técnicas-chave (Verificado):** só funções com `FromISR` dentro de ISR (7.2); `xHigherPriorityTaskWoken` iniciado em `pdFALSE`, definido em `pdTRUE` quando acorda tarefa de prioridade maior e passado a `portYIELD_FROM_ISR()` ou `portEND_SWITCHING_ISR()` (alguns portes só aceitam no fim da ISR); `configMAX_SYSCALL_INTERRUPT_PRIORITY` (nome novo `configMAX_API_CALL_INTERRUPT_PRIORITY`) é a maior prioridade de interrupção que pode chamar a API; acima dele a ISR não pode chamar nenhuma função do FreeRTOS; no Cortex-M valor numérico baixo é prioridade lógica alta, bits de prioridade alinhados à esquerda e o limite não pode ser 0 (7.8.1, 13.2); 13.2 diz que prioridade de interrupção é a fonte mais comum de pedidos de suporte e que `configASSERT()` costuma detectar; pilha: `uxTaskGetStackHighWaterMark()` (menor folga desde o início), `configCHECK_FOR_STACK_OVERFLOW` com métodos 1 e 2 que não garantem detecção, método 3 só em alguns portes; o hook roda em contexto de interrupção e não há forma confiável de recuperar; `configASSERT()` definido em `FreeRTOSConfig.h`, recomendado em desenvolvimento, com custo de tamanho e velocidade (12.2); `stack_macros.h` confirma os métodos e que portes com MPU pulam a checagem.
- **Conteúdo reutilizável (redação própria):** checklist FreeRTOS: ISR só com `FromISR`; o flag de tarefa acordada vai ao yield do porte; prioridade da ISR dentro do limite (e conferida com `configASSERT`); `configASSERT` definido nas builds de desenvolvimento e de teste; `configCHECK_FOR_STACK_OVERFLOW` ligado e `uxTaskGetStackHighWaterMark()` registrado; o hook de overflow só registra e para (sem recuperar). Substitui a nota de V-15 (que dependia de fonte indireta).
- **Ressalvas:** correção 7. O Book é texto CC BY-SA 4.0: só destilar e atribuir. As páginas freertos.org não foram lidas.
- **Prompt-score:** 83.

### V-53 — Embassy (origem R-gap-27) — Classe B (7)
- **Fonte:** https://github.com/embassy-rs/embassy (9,9 mil estrelas, 17.927 commits, licença MIT ou Apache-2.0 à escolha, documentação CC-BY-SA) e https://embassy.dev/
- **Técnicas-chave (Verificado):** "Modern embedded framework, using Rust and async"; executor que suspende o núcleo sem trabalho; múltiplos executores com prioridades; módulo de tempo; HALs async para STM32, nRF, RP e outros.
- **Conteúdo reutilizável (redação própria):** regra de revisão de código async: sem espera bloqueante dentro de tarefa; executor e prioridades documentados; versão do crate registrada.
- **Ressalvas:** sem lista de versões; "sem alocação dinâmica" é declaração do projeto.
- **Prompt-score:** 73 (referência).

### V-54 — RTIC v2 (origem R-gap-28) — Classe B (7)
- **Fonte:** https://rtic.rs/2/book/en/ e https://docs.rs/rtic/latest/rtic/ (versão 2.3.1, MIT OR Apache-2.0 segundo a rodada anterior)
- **Técnicas-chave (Verificado):** "RTIC v2.x"; tarefas de hardware ligadas a interrupções (o NVIC escolhe pela prioridade), tarefas de software em executores async, uma por prioridade; Stack Resource Policy com teto calculado em compilação; execução até o fim em uma pilha única, sem deadlock; arquitetura explícita: Cortex-M (e menciona RISC-V com CLIC).
- **Conteúdo reutilizável (redação própria):** regra: recurso compartilhado entre tarefas de prioridades diferentes passa pelo mecanismo de recursos do RTIC e não por `static mut`; prioridades justificadas.
- **Ressalvas:** licença do livro não declarada na página; tamanho da cobertura de portes não verificado.
- **Prompt-score:** 73 (referência).

### V-55 — probe-rs e defmt (origem R-gap-29) — Classe B (7)
- **Fontes:** https://probe.rs/docs/ e https://defmt.ferrous-systems.com/
- **Técnicas-chave (Verificado):** probe-rs grava e depura ARM e RISC-V por SWD ou JTAG (memória, run/halt, breakpoints, reset), RTT para logs, integração com VS Code, ferramentas `probe-rs`, `cargo-flash` e `cargo-embed`; defmt formata no host, usa strings internadas e quadros binários, níveis `error`, `info`, `warn`, `debug` e `trace`, transporte `defmt-rtt` (suportado pelo probe-rs), `defmt-itm`, `defmt-semihosting` (para QEMU).
- **Conteúdo reutilizável (redação própria):** gate: `probe-rs download`, `flash`, `erase`, `reset` e escrita de memória são operações de escrita e exigem confirmação do usuário; leituras (`list`, `info`, `read-mem`, `rtt`) são livres. Nada é instalado nem executado a partir dessas páginas.
- **Ressalvas:** nenhuma das páginas declara licença; `DEFMT_LOG` não foi lido.
- **Prompt-score:** 82.

### V-56 — Embedonomicon (origem R-gap-30) — Classe B (6), referência
- **Fonte:** https://docs.rust-embedded.org/embedonomicon/
- **Técnicas-chave (Verificado):** constrói aplicação `#![no_std]` do zero para Cortex-M; layout de memória por linker e linker script; como funcionam `cortex-m-rt`, `msp430-rt` e `riscv-rt`; sem licença na página.
- **Conteúdo reutilizável:** guia de depuração de arranque e de linker, não receita de produção.
- **Prompt-score:** 68 (referência).

### V-57 — PlatformIO: testes e `pio check` (origem R-gap-31 mais leitura nova) — Classe B (7)
- **Fontes:** https://docs.platformio.org/en/latest/advanced/unit-testing/index.html e https://docs.platformio.org/en/latest/core/userguide/cmd_check.html
- **Técnicas-chave (Verificado):** testes rodam no host (native), na placa ou nos dois; frameworks: Doctest, GoogleTest, Unity e Custom. `pio check`: Cppcheck é a ferramenta padrão; `-e`, `-f/--src-filters`, `--flags`, `--severity`, `--json-output`, `--fail-on-defect`, `--skip-packages`, `-s`, `-v`; por padrão só `src_dir` e `include_dir` são checados; sem `--fail-on-defect` o código de saída é o da ferramenta.
- **Conteúdo reutilizável (redação própria):** regra: lógica testada em native; driver na placa; em CI `pio check --fail-on-defect high --skip-packages` (**conferir as severidades aceitas na versão instalada**, Inferido).
- **Ressalvas:** a página `pio test` e o guia de estilo do Arduino não foram lidos (a página do Arduino voltou vazia).
- **Prompt-score:** 82.

### V-58 — cppcheck: addon MISRA (origem R-gap-32) — Classe A (8)
- **Fonte:** https://cppcheck.sourceforge.io/misra.php
- **Técnicas-chave (Verificado):** cobre quase todas as regras do MISRA C 2012 "including the amendments"; as regras 1.1 e 1.2 não são tratadas e devem ser verificadas pelos compiladores (gcc, MSVC, o do alvo); a página não traz o comando do addon, nem a licença do texto das regras, nem MISRA C:2023.
- **Conteúdo reutilizável (redação própria):** matriz de configuração: quais regras o cppcheck cobre, quais o compilador cobre, quais o time desvia e por quê; o texto da MISRA é pago e não entra no plugin.
- **Prompt-score:** 80.

### V-59 — GCC: `-fstack-usage`, `-fanalyzer` e sanitizers (origem R-gap-33 mais leitura nova) — Classe A (9)
- **Fontes:** https://gcc.gnu.org/onlinedocs/gcc/Developer-Options.html, https://gcc.gnu.org/onlinedocs/gcc/Static-Analyzer-Options.html, https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html
- **Técnicas-chave (Verificado):** `-fstack-usage` gera `.su` com nome, bytes e qualificadores `static`, `dynamic`, `bounded` (correção 6); `-fanalyzer` faz execução simbólica interprocedural, "neither sound nor complete", mais cara que os outros avisos e "only suitable for use on C code in this release"; avisos `-Wanalyzer-*` (null-dereference, use-after-free, double-free, malloc-leak, out-of-bounds, fd-leak, uso de valor não inicializado); sanitizers de host: `-fsanitize=address`, `undefined` e `thread` (ASan não combina com TSan), compilar com `-g` e `-O0/-O1/-Og`, não combinar `-Werror` com sanitizers; `-fstack-protector` e variantes.
- **Conteúdo reutilizável (redação própria):** "Orçamento de pilha": rodar `-fstack-usage` no build, somar o caminho de chamada mais profundo (incluindo ISR com pilha própria), tratar `dynamic` sem `bounded` como piso, confirmar na placa com `k_thread_stack_space_get()` (V-49) ou `uxTaskGetStackHighWaterMark()` (V-52); no host, rodar a lógica com ASan e UBSan em CI; `-fanalyzer` como complemento, nunca como prova.
- **Ressalvas:** `-Wstack-usage=` não está nas páginas lidas (pode estar em Warning Options, não consultada). Os valores do `.su` são estimativa do compilador, não medição de pior caso.
- **Prompt-score:** 85.

### V-60 — Segurança funcional no Zephyr (origem R-gap-34) — Classe B (6)
- **Fontes:** https://docs.zephyrproject.org/latest/safety/index.html e https://docs.zephyrproject.org/latest/safety/safety_overview.html
- **Técnicas-chave (Verificado):** o projeto tem como **objetivo** certificar IEC 61508 (SIL 3 / SC 3) para um escopo limitado, ainda a definir; caminho 3s/1s por já existir o código; branch auditável e branch LTS; metas de cobertura de 100% em pontos de entrada, instruções e ramos com justificativa para o resto; guidelines de código em fase I concluída e fase II em andamento. ISO 26262 e DO-178C não são citados.
- **Conteúdo reutilizável (redação própria):** nota do plugin: "Zephyr declara IEC 61508 como meta de processo; não há certificação obtida nesta fonte. O plugin não afirma conformidade com IEC 61508, ISO 26262 ou DO-178C."
- **Ressalvas:** correção 14. Normas pagas não foram consultadas (correto).
- **Prompt-score:** 72.

### V-61 — Skills de teste de bancada do SensorsIot (BLE, MQTT, ESP-IDF) (adicionado pelo validador) — Classe C (4)
- **Fonte:** https://github.com/SensorsIot/Embedded-AI-Harness/tree/main/.claude/skills (18 diretórios, entre eles `testbench-ble`, `testbench-mqtt`, `esp-idf-handling`, `testbench-debug`, `testbench-test-handling`; 188 estrelas, MIT)
- **Técnicas-chave (Verificado nos SKILL.md lidos):** `testbench-mqtt` (cerca de 150 linhas): descoberta da bancada com script via `sudo`, broker mosquitto aberto na rede da bancada; teste de reconexão com regra de firewall por dispositivo em vez de parar um broker compartilhado; will de "morte" observado pelo tópico de status e não pelo tópico LWT; semear valor retido sentinela antes de testar o will; valor retido durante a queda é obsoleto, exigir pelo menos duas chegadas ao vivo antes de ler contadores. `testbench-ble` (cerca de 100 linhas): uma conexão por vez, dados em hex, 409 se já conectado. `esp-idf-handling` (cerca de 450 linhas): medir o flash antes de dimensionar partições, usar `flash_args`, parar sessões de depuração antes de gravar, nunca `uhubctl` na porta raiz do uplink, nunca `gh auth login`.
- **Conteúdo reutilizável (redação própria):** checklist de teste de cliente MQTT em bancada (will, retido, reconexão, telemetria com fonte real) e de teste BLE (conexão única, hex, desconexão antes de reconectar).
- **Ressalvas de segurança (Verificado):** a API HTTP da bancada não tem autenticação (README, rodada anterior), o broker é aberto, a descoberta usa `sudo`, há IPs privados e portas fixas; `esp-idf-handling` não tem passo de confirmação humana para gravar e a seção OTA tem um bug (aspas simples impedem a expansão de `$TESTBENCH_URL`); nenhuma instrução à IA, instalador ou exfiltração. Não instalar nem copiar; só destilar (MIT permitiria copiar com atribuição, mas o conteúdo depende da bancada).
- **Prompt-score:** originais cerca de 66; destilado 78 (D1 4, D2 4, D3 4, D4 4, D5 2, D6 4, D7 4, D8 5, D9 4, D10 5, D11 4, D12 3).

### V-62 — embeddedskills `probe-rs` e `embedded-systems-architect` SKILL.md (extensão de V-21 e V-27) — Classe C (5)
- **Fontes:** https://raw.githubusercontent.com/zhinkgit/embeddedskills/main/probe-rs/SKILL.md (MIT, 734 estrelas na rodada anterior) e https://raw.githubusercontent.com/Zachariah9420/embedded-systems-architect/main/SKILL.md (MIT, 5 estrelas)
- **Técnicas-chave (Verificado):** `probe-rs` skill (cerca de 108 linhas): subcomandos list, info, flash, erase, reset, read-mem, write-mem, attach, run, gdb, rtt; risco **alto** em flash, erase, reset e write-mem, **baixo** nos demais; `.bin` exige `--address`; a skill manda parar se o chip não for informado e não adivinhá-lo; `operation_mode` 1, 2 ou 3 em `config.json` e **o documento não diz qual vale para operações de risco alto por padrão**; aviso do Windows sobre WinUSB. `embedded-systems-architect` SKILL.md (cerca de 125 a 135 linhas): materiais do projeto têm prioridade sobre a memória do modelo; dados faltantes marcados "dados insuficientes"; cinco níveis de evidência; operações irreversíveis (eFuse/OTP, chaves de secure boot, criptografia de flash, proteção permanente, anti-rollback) só listam passos, pré-requisitos e riscos, sem comando copiável; sem caminho de recuperação confirmado não há procedimento de escrita; dry-run por padrão e leitura de verificação; enviar código, pesos ou specs privados a sites externos exige consentimento e registro; sem instruções à IA fora do normal, sem instalador automático.
- **Conteúdo reutilizável (redação própria):** gate padrão do plugin: escrita (flash, erase, reset, write-mem) exige confirmação explícita, equivalente ao modo 3; chip e endereço nunca são adivinhados; mapa de evidência para os rótulos da fábrica. Reforça V-21 e V-27.
- **Ressalvas:** nenhuma evidência de uso além do auto-declarado.
- **Prompt-score:** V-27 sobe de 83 (provisório) para 85 após a leitura do SKILL.md; gate reescrito 87 (D1 4, D2 4, D3 5, D4 4, D5 3, D6 4, D7 5, D8 5, D9 4, D10 5, D11 5, D12 4).

### V-63 — trailofbits/claude-code-config: configuração segura para Claude Code (adicionado pelo validador) — Classe B (5)
- **Fonte:** https://github.com/trailofbits/claude-code-config (2,1 mil estrelas, 36 commits; licença **não exibida**; empresa de segurança)
- **Técnicas-chave (Verificado):** sandbox com `/sandbox` porque, sem ele, as regras de `deny` só bloqueiam as ferramentas nativas e o Bash as contorna; "Hooks are not a security boundary -- a prompt injection can work around them"; hooks de exemplo (bloquear `rm -rf`, bloquear push direto em main) para adaptar, não copiar; `enableAllProjectMcpServers` em `false` porque `.mcp.json` de projeto vem do git; limitar a profundidade de subagentes (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`); devcontainer para isolamento total.
- **Conteúdo reutilizável (redação própria):** reforça o princípio do plugin: nenhum hook ou MCP ativo por padrão; hook de gate de gravação é guarda e não sandbox (reforça V-05 e V-08); revisar `.mcp.json` de qualquer firmware que o usuário abra.
- **Ressalvas:** licença desconhecida, tratar como sem licença; só destilar.
- **Prompt-score:** 80.

## Rejeitados, rebaixados e fundidos neste adendo

| Item | Decisão | Motivo |
| --- | --- | --- |
| R-gap-21 (cobertura de OTA) | Rejeitado como item autônomo | Comparação MCUboot versus ESP-IDF era Inferida; fundida como tabela de decisão em V-46 |
| R-gap-26 (FreeRTOS, localização) | Substituído | Era um mapa de caminhos; as URLs `.../02-Kernel/...` existem mas não são legíveis; lacuna fechada por V-52 com fonte alternativa oficial |
| R-gap-34b (metadados GitHub) | Absorvido | Não é item de conteúdo; metadados na tabela acima |
| R-gap-06, R-gap-07 | Rebaixados e fundidos (V-34) | Só índices; sem regra |
| R-gap-14 | Rebaixado para B (5) | Última atualização da fonte em abril de 2022; sem medição |
| R-gap-15 | Rebaixado para B (6) | Top 10 em PDF com link quebrado; ISVS em RC |
| R-gap-30 | Mantido como referência (V-56) | Sem lista de capítulos nem licença |
| R-gap-34 | Rebaixado para B (6) e corrigido | O overview cita IEC 61508 como meta; o índice não citava |

## Segurança e copyright (varredura do adendo)

Nenhum arquivo lido continha instruções dirigidas à IA, links encurtados ou pedido de instalador. Riscos registrados: skills do SensorsIot dependem de `sudo` e de API de bancada sem autenticação; `esp-idf-handling` não tem confirmação humana para gravar; o serviço `idf` do pytest-embedded grava binário automaticamente; `west flash --erase` e `probe-rs` escrevem no alvo. Licenças que obrigam a destilar: FreeRTOS Kernel Book, Rust book, ISVS e FSTM (CC BY-SA 4.0, exigem atribuição e mesma licença), ETSI EN 303 645 (todos os direitos reservados), trailofbits (sem licença visível), MISRA (paga). Nenhum trecho literal foi mantido. Códigos de eFuse, queima de chave e apagamento nunca são reproduzidos.

## Mapa de cobertura atualizado (supera a tabela anterior onde houver diferença)

| Subtema | Itens validados | Cobertura agora |
| --- | --- | --- |
| Protocolos (I2C, SPI, UART, CAN, MQTT, BLE) | V-30, V-31, V-32, V-33, V-34, V-35 | I2C, CAN, MQTT: boa; SPI e UART: parcial (API do SPI do Zephyr não lida); BLE: fraca (só índices) |
| Testes de firmware | V-36, V-37, V-38, V-57 | Boa em Zephyr, ESP-IDF e Unity; HIL por pytest-embedded citado; HAL falsa com exemplo ainda sem fonte própria |
| Consumo de energia | V-39, V-40 | Parcial (ESP-IDF boa; Zephyr desatualizado; Nordic e ST sem fonte; sem fonte para "medição de corrente como critério de pronto" além da prática derivada de V-39) |
| Segurança IoT e OTA | V-41, V-42, V-43, V-44, V-45, V-46, V-63 | Boa (NIST, ETSI, ESP-IDF e MCUboot); OWASP Top 10 sem leitura |
| Drivers a partir de datasheet | V-47, V-48, V-23 | Média (SVD, svd2rust e embedded-hal; sem PAC/HAL/BSP detalhado) |
| Zephyr oficial | V-49, V-50, V-51, V-36, V-44 | Boa em threads, ISR, workqueue, Kconfig e west; devicetree pendente |
| FreeRTOS oficial | V-52, V-15 | Média (Book e fonte do kernel; páginas freertos.org ilegíveis) |
| Rust embedded | V-11, V-12, V-47, V-48, V-53, V-54, V-55, V-56 | Boa; falta ao menos um AGENTS.md ou skill de Rust no_std com licença clara |
| Arduino e PlatformIO | V-57 | Parcial (PlatformIO; Arduino sem fonte) |
| Análise estática e de pilha | V-13, V-14, V-58, V-59 | Boa (sanitizers, `-fanalyzer`, `-fstack-usage`, cppcheck); análise de pilha do Zephyr sem fonte |
| Segurança funcional | V-60 | Fraca (meta de IEC 61508 do Zephyr; sem visão pública de ISO 26262 e DO-178C) |
| Comunidade e skills de terceiros | V-61, V-62, V-63 | Parcial (skills do GitHub lidas; Reddit, X e YouTube não alcançados) |

## Lacunas restantes (pesquisáveis)

1. **Devicetree do Zephyr:** a URL testada (`/latest/build/dts/intro-input-and-output.html`) é 404; localizar pelo índice do site.
2. **OWASP IoT Top 10 2018:** o PDF listado é 404; achar o endereço atual no site do OWASP antes de citar as dez categorias.
3. **Energia:** guias da Nordic e da ST, e fonte para medir corrente como critério de pronto.
4. **BLE:** subpáginas de LE Host do Zephyr (MTU, parâmetros de conexão, segurança) e do ESP-IDF.
5. **SPI do Zephyr:** referência Doxygen (`group__spi__interface`) e o pull-up/terminação do CAN.
6. **Rust no_std:** AGENTS.md ou skill com licença clara; `DEFMT_LOG`; `embedded-hal-async`.
7. **Arduino:** guia de estilo (a página voltou vazia) e `pio test`.
8. **Segurança funcional:** visão pública de ISO 26262 e DO-178C.
9. **Comunidade:** Reddit (r/embedded, r/ClaudeCode), X e YouTube; refazer com busca quando houver orçamento de WebSearch.
10. **GitHub:** datas de push de todos os repositórios (API recusa); `atillab1`.
11. **MQTT 5.0:** seções de QoS e reenvio (segunda metade da página); **isr-ok** do Zephyr; páginas `freertos.org` (conteúdo não legível pelo WebFetch).

## Recomendações ao construtor (adendo)

| Artefato | Origem | Tipo |
| --- | --- | --- |
| `firmware-protocol-review` (barramentos e MQTT, com saída tabular e rótulos de evidência) | V-30 a V-33, V-35 | skill |
| `firmware-test-host` (ztest `unit_testing`, Unity e CMock, ESP-IDF, pytest-embedded) | V-36, V-37, V-38, V-57 | referência e skill |
| `ota-update-review` (agora com fontes de plataforma: MCUboot e ESP-IDF) | V-44, V-45, V-46, V-42, V-43 | skill, gate de confirmação humana |
| `stack-budget` | V-49, V-52, V-59 | skill |
| `rtos-isr-review` (Zephyr e FreeRTOS) | V-50, V-52, V-15 | skill |
| `power-budget-review` | V-39, V-40 | checklist; marcar como pendentes Nordic e ST |
| `iot-security-baseline` (NIST 8259, ETSI 303 645, ISVS como índice) | V-41, V-42, V-43 | checklist de produto, sem texto de norma |
| `datasheet-first` (agora com SVD e embedded-hal) | V-23, V-47, V-48 | skill |
| Gate de escrita do plugin (flash, erase, reset, write-mem, west flash, probe-rs, pytest-embedded com `idf`) | V-51, V-55, V-62, V-45 | regra de CLAUDE.md e de skill |

Não incluir: texto do ETSI, do NIST, do MISRA, do FreeRTOS Kernel Book, do ISVS e do FSTM; as dez categorias do OWASP Top 10; regra de MTU/BLE; comandos de queima de eFuse; qualquer MCP ou hook de gravação ativo; números de corrente, pull-up ou pilha sem a fonte da variante.

Veredito do adendo: **pass_with_gaps**. Protocolos (I2C, CAN, MQTT), testes, segurança IoT e OTA, Zephyr, FreeRTOS, Rust embedded e análise de pilha agora têm fontes de qualidade com regras de revisão; restam lacunas listadas acima (BLE, energia de fabricante, devicetree, OWASP Top 10, comunidade social, skill de Rust no_std).
