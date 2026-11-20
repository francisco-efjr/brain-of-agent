# Matriz de contexto → regras obrigatórias

Seção "Regras por contexto" gerada a partir de `regras-*.md` (fonte única); para mudar, edite a regra e regenere. Como usar:

1. **G0 (ativação):** classifique o pedido em um ou mais contextos C1–C14. C0 vale sempre.
2. Carregue as regras de cada contexto casado (abra só os arquivos e IDs listados) e aplique-as como obrigação.
3. **Contexto dinâmico:** se no meio do trabalho surgir ação de outro contexto (apagar ou sobrescrever o que o Git da branch local não restaura = C6; mexer em permissões = C7), pare, carregue esse contexto e passe pelo portão dele antes de agir. Editar ou apagar arquivo versionado e commitado na branch local é C2.
4. Cada regra aplicável termina como Atendida, Exceção justificada ou N/A com motivo, no relatório de conformidade proporcional (`checar-conformidade`). Regras `[H]` e a parte humana das `[A+H]` nunca são marcadas como atendidas pelo agente: viram pedido ou a pendência única de aprovação da entrega ([decisões](decisoes-e-tradeoffs.md)).
5. Proporcionalidade escolhe os contextos; não dispensa regra de contexto casado. Pergunta pontual aplica C0 em silêncio e responde direto. O C0 já está no bloco do guia do playbook; para C1–C14, abra só os IDs listados, por busca do ID.

## Contextos

| Ctx | Nome | Quando casa | Portões | Skills | Agente(s) |
| --- | --- | --- | --- | --- | --- |
| C0 | Sempre | Toda invocação, inclusive pergunta pontual (com proporcionalidade). | G0 sempre; G6 quando houver implementação ou auditoria | `playbook`, `checar-conformidade` | `conformance-auditor` |
| C1 | Pedido e plano | Entender a demanda, especificar, planejar, escolher stack ou abordagem. | G1 | `especificar-pedido` | `conformance-auditor` |
| C2 | Implementação | Escrever ou alterar código, configuração ou documentação versionada; qualquer commit. | G2, G3 | `definir-oraculo`, `memoria-do-projeto` | `oracle-designer` (antes), `conformance-auditor` (depois) |
| C3 | Depuração e investigação | Bug, incidente, comportamento estranho, regressão. | G2 | `definir-oraculo` | `oracle-designer` |
| C4 | Testes e verificação | Escrever ou rodar testes, validar entrega, afirmar "pronto". | G2, G6 | `definir-oraculo`, `checar-conformidade` | `oracle-designer`, `conformance-auditor` |
| C5 | Revisão e auditoria | Revisar código, PR, contribuição externa, auditoria de segurança, relatório gerado por IA. | G6 | `revisar-codigo-de-ia` | `conformance-auditor`, `claims-verifier` |
| C6 | Ação destrutiva ou de dados | Apagar, mover, sobrescrever, limpar, migrar, sincronizar ou restaurar o que o Git da branch local não restaura (dados, banco, mídia, não versionados, trabalho não commitado). | G4 (bloqueante) | `guardar-destrutivo` | `destructive-ops-guard` |
| C7 | Ambiente do agente | Sandbox, permissões, segredos, rede, modo sem confirmação, skills, plugins ou MCP de terceiros. | G3 | `kit-seguranca-agente` | `agent-environment-auditor` |
| C8 | Produção e operação | Deploy, release, infraestrutura, monitoramento, backup de produção. | G5 | `kit-seguranca-agente`, `checar-conformidade` | `conformance-auditor` |
| C9 | Sistema que usa LLM | Código de produto que chama modelo: prompts, saídas, ferramentas, classificadores, mídia gerada. | G2 | `definir-oraculo` | `oracle-designer` |
| C10 | Modelos, benchmarks, anúncios e custo | Escolher ou avaliar modelo ou ferramenta, citar tabela ou anúncio, medir custo e cota. | G6 (afirmações datadas e verificadas) | `avaliar-modelo` | `claims-verifier` |
| C11 | Pesquisa, fatos e textos | Pesquisar, checar fatos, escrever relatório, documentação ou texto derivado de fontes. | G6 | `playbook` (regras PES-01 a PES-11) | `claims-verifier` |
| C12 | Sessão longa, memória e multiagente | Contexto grande, compactação, passagem de turno, memória do projeto, lotes paralelos, cota. | G0, G6 (passagem de turno) | `memoria-do-projeto` | `conformance-auditor` |
| C13 | Organização, processo e carreira | Adoção de IA no time, métricas, contratação, formação, mercado. | — | `adotar-ia-no-time` | `claims-verifier` |
| C14 | Uso pessoal, aprendizado, privacidade e golpes | Orientação à pessoa usuária sobre chatbot, estudo, aplicativos e golpes. | — | `playbook` (regras PES) | — |

Gatilhos de contexto dinâmico: remoção ou sobrescrita de dados de usuário, banco, buckets, mídia ou arquivos não versionados ou ignorados, `git clean`, `reset --hard`, `checkout --` sobre trabalho não commitado, `push --force`, `rsync --delete`, `DROP`, `TRUNCATE`, migração, sincronização ou restauração → C6 (editar ou apagar arquivo versionado e commitado na branch local é C2); `settings`, permissões, sandbox, `.env`, credenciais, instalar skill, plugin ou MCP → C7; deploy, release, servidor, produção → C8; chamada de API de modelo no código do produto → C9; citar número de modelo, benchmark, preço ou anúncio → C10; sessão longa, compactação, troca de agente ou lote paralelo → C12.

## Regras por contexto

### C0 — Sempre (34 regras)

- [regras-contexto-memoria.md](regras-contexto-memoria.md): CTX-06, CTX-08, CTX-13, CTX-15
- [regras-metodo.md](regras-metodo.md): MET-01, MET-02, MET-04, MET-05, MET-06, MET-07, MET-08, MET-11, MET-14, MET-P01, MET-P03, MET-P04, MET-S01, MET-S02
- [regras-seguranca.md](regras-seguranca.md): SEG-06, SEG-08, SEG-12, SEG-15, SEG-32
- [regras-verificacao.md](regras-verificacao.md): VER-01, VER-02, VER-03, VER-04, VER-05, VER-09, VER-10, VER-12, VER-P01, VER-P02, VER-P05

### C1 — Pedido e plano (37 regras)

- [regras-engenharia.md](regras-engenharia.md): ENG-06, ENG-16
- [regras-metodo.md](regras-metodo.md): MET-02, MET-03, MET-10, MET-12, MET-P04, MET-S03, MET-S04
- [regras-pedido.md](regras-pedido.md): PED-01, PED-02, PED-03, PED-04, PED-05, PED-06, PED-07, PED-08, PED-09, PED-10, PED-11, PED-12, PED-13, PED-14, PED-15, PED-16, PED-17, PED-18, PED-P01, PED-P02, PED-P03, PED-P04, PED-P05, PED-P06, PED-S01, PED-S02, PED-S03
- [regras-seguranca.md](regras-seguranca.md): SEG-29

### C2 — Implementação (56 regras)

- [regras-contexto-memoria.md](regras-contexto-memoria.md): CTX-01, CTX-02
- [regras-engenharia.md](regras-engenharia.md): ENG-01, ENG-02, ENG-03, ENG-04, ENG-05, ENG-06, ENG-07, ENG-08, ENG-09, ENG-10, ENG-11, ENG-13, ENG-16, ENG-17, ENG-18, ENG-19, ENG-20, ENG-21, ENG-22, ENG-23, ENG-24, ENG-25, ENG-26, ENG-27, ENG-28, ENG-30, ENG-P01, ENG-P02, ENG-P03, ENG-P04, ENG-P05, ENG-P10, ENG-P11, ENG-P12, ENG-S01, ENG-S02, ENG-S03, ENG-S04, ENG-S05
- [regras-metodo.md](regras-metodo.md): MET-03, MET-12
- [regras-pedido.md](regras-pedido.md): PED-14, PED-15
- [regras-revisao.md](regras-revisao.md): REV-01
- [regras-seguranca.md](regras-seguranca.md): SEG-09, SEG-26, SEG-27, SEG-28, SEG-29, SEG-33, SEG-34
- [regras-verificacao.md](regras-verificacao.md): VER-06, VER-27, VER-P06

### C3 — Depuração e investigação (9 regras)

- [regras-engenharia.md](regras-engenharia.md): ENG-02, ENG-10, ENG-12, ENG-14, ENG-15, ENG-P06, ENG-P07, ENG-S04
- [regras-pedido.md](regras-pedido.md): PED-10

### C4 — Testes e verificação (36 regras)

- [regras-sistemas-com-llm.md](regras-sistemas-com-llm.md): LLM-08
- [regras-verificacao.md](regras-verificacao.md): VER-01, VER-02, VER-03, VER-04, VER-05, VER-06, VER-07, VER-08, VER-09, VER-11, VER-13, VER-14, VER-15, VER-16, VER-17, VER-18, VER-19, VER-20, VER-21, VER-22, VER-23, VER-24, VER-25, VER-26, VER-27, VER-P01, VER-P02, VER-P03, VER-P04, VER-P05, VER-P06, VER-P07, VER-S01, VER-S02, VER-S03

### C5 — Revisão e auditoria (32 regras)

- [regras-engenharia.md](regras-engenharia.md): ENG-27
- [regras-metodo.md](regras-metodo.md): MET-09
- [regras-revisao.md](regras-revisao.md): REV-01, REV-02, REV-03, REV-04, REV-05, REV-06, REV-07, REV-08, REV-09, REV-10, REV-11, REV-12, REV-13, REV-14, REV-15, REV-P01, REV-P02, REV-P03, REV-P04, REV-P05, REV-P06, REV-P07, REV-S01, REV-S02, REV-S03, REV-S04
- [regras-seguranca.md](regras-seguranca.md): SEG-26, SEG-27
- [regras-verificacao.md](regras-verificacao.md): VER-16, VER-24

### C6 — Ação destrutiva ou de dados (17 regras)

- [regras-engenharia.md](regras-engenharia.md): ENG-22
- [regras-operacao.md](regras-operacao.md): OPS-02, OPS-03, OPS-08
- [regras-seguranca.md](regras-seguranca.md): SEG-19, SEG-20, SEG-21, SEG-22, SEG-23, SEG-24, SEG-25, SEG-33, SEG-P03, SEG-P04, SEG-P05, SEG-S01
- [regras-verificacao.md](regras-verificacao.md): VER-04

### C7 — Ambiente do agente (30 regras)

- [regras-avaliacao-modelos.md](regras-avaliacao-modelos.md): AVA-05
- [regras-revisao.md](regras-revisao.md): REV-04, REV-07, REV-15, REV-P03
- [regras-seguranca.md](regras-seguranca.md): SEG-01, SEG-02, SEG-03, SEG-04, SEG-05, SEG-06, SEG-07, SEG-08, SEG-10, SEG-11, SEG-13, SEG-14, SEG-15, SEG-16, SEG-17, SEG-18, SEG-24, SEG-31, SEG-P01, SEG-P02, SEG-P03, SEG-P04, SEG-S01, SEG-S02, SEG-S03

### C8 — Produção e operação (22 regras)

- [regras-engenharia.md](regras-engenharia.md): ENG-09
- [regras-operacao.md](regras-operacao.md): OPS-01, OPS-02, OPS-03, OPS-04, OPS-05, OPS-06, OPS-07, OPS-08, OPS-09, OPS-10, OPS-11, OPS-12, OPS-13, OPS-14, OPS-15, OPS-17
- [regras-revisao.md](regras-revisao.md): REV-02, REV-11
- [regras-seguranca.md](regras-seguranca.md): SEG-12, SEG-30
- [regras-verificacao.md](regras-verificacao.md): VER-14

### C9 — Sistema que usa LLM (31 regras)

- [regras-avaliacao-modelos.md](regras-avaliacao-modelos.md): CUS-04
- [regras-engenharia.md](regras-engenharia.md): ENG-08, ENG-13, ENG-P12
- [regras-operacao.md](regras-operacao.md): OPS-10, OPS-11, OPS-12, OPS-16
- [regras-pedido.md](regras-pedido.md): PED-11
- [regras-seguranca.md](regras-seguranca.md): SEG-15, SEG-16, SEG-35
- [regras-sistemas-com-llm.md](regras-sistemas-com-llm.md): LLM-01, LLM-02, LLM-03, LLM-04, LLM-05, LLM-06, LLM-07, LLM-08, LLM-09, LLM-10, LLM-11, LLM-12, LLM-13, LLM-14, LLM-15, LLM-S01, LLM-S02
- [regras-verificacao.md](regras-verificacao.md): VER-21, VER-25

### C10 — Modelos, benchmarks, anúncios e custo (75 regras)

- [regras-avaliacao-modelos.md](regras-avaliacao-modelos.md): AVA-01, AVA-02, AVA-03, AVA-04, AVA-05, AVA-06, AVA-07, AVA-08, AVA-09, AVA-10, AVA-11, AVA-12, AVA-13, AVA-14, AVA-15, AVA-16, AVA-B01, AVA-B02, AVA-B03, AVA-B04, AVA-B05, AVA-B06, AVA-B07, AVA-B08, AVA-B09, AVA-B10, AVA-B11, AVA-C01, AVA-C02, AVA-C03, AVA-C04, AVA-C05, AVA-C06, AVA-C07, AVA-C08, AVA-C09, AVA-C10, AVA-C11, AVA-C12, AVA-C13, AVA-C14, AVA-P01, AVA-P02, AVA-P03, AVA-P04, AVA-P05, AVA-P06, AVA-P07, CUS-01, CUS-02, CUS-03, CUS-04, CUS-05, CUS-06, CUS-07, CUS-08, CUS-09, CUS-10, CUS-P01, AVA-S01, AVA-S02, AVA-S03
- [regras-engenharia.md](regras-engenharia.md): ENG-24, ENG-P08
- [regras-metodo.md](regras-metodo.md): MET-P03
- [regras-operacao.md](regras-operacao.md): OPS-17
- [regras-revisao.md](regras-revisao.md): REV-P04
- [regras-seguranca.md](regras-seguranca.md): SEG-31
- [regras-sistemas-com-llm.md](regras-sistemas-com-llm.md): LLM-10, LLM-15
- [regras-verificacao.md](regras-verificacao.md): VER-11, VER-21, VER-22, VER-23, VER-P03

### C11 — Pesquisa, fatos e textos (30 regras)

- [regras-avaliacao-modelos.md](regras-avaliacao-modelos.md): AVA-C14, AVA-P07
- [regras-engenharia.md](regras-engenharia.md): ENG-28, ENG-29, ENG-30, ENG-P07
- [regras-metodo.md](regras-metodo.md): MET-09
- [regras-pedido.md](regras-pedido.md): PED-13
- [regras-pessoa.md](regras-pessoa.md): PES-01, PES-02, PES-03, PES-04, PES-05, PES-06, PES-07, PES-08, PES-09, PES-11, PES-P01, PES-P05, PES-S01, PES-S02
- [regras-revisao.md](regras-revisao.md): REV-06, REV-13, REV-14, REV-P07
- [regras-seguranca.md](regras-seguranca.md): SEG-32
- [regras-verificacao.md](regras-verificacao.md): VER-12, VER-17, VER-18

### C12 — Sessão longa, memória e multiagente (42 regras)

- [regras-avaliacao-modelos.md](regras-avaliacao-modelos.md): CUS-01, CUS-02, CUS-10
- [regras-contexto-memoria.md](regras-contexto-memoria.md): CTX-01, CTX-02, CTX-03, CTX-04, CTX-05, CTX-06, CTX-07, CTX-08, CTX-09, CTX-10, CTX-11, CTX-12, CTX-13, CTX-14, CTX-15, CTX-16, CTX-17, CTX-18, CTX-19, CTX-20, CTX-P01, CTX-P02, CTX-P03, CTX-P04, CTX-P05, CTX-S01, CTX-S02, CTX-S03, CTX-S04, CTX-S05, CTX-S06
- [regras-engenharia.md](regras-engenharia.md): ENG-15, ENG-17, ENG-18, ENG-29, ENG-P08
- [regras-metodo.md](regras-metodo.md): MET-P02
- [regras-sistemas-com-llm.md](regras-sistemas-com-llm.md): LLM-14
- [regras-verificacao.md](regras-verificacao.md): VER-19

### C13 — Organização, processo e carreira (41 regras)

- [regras-avaliacao-modelos.md](regras-avaliacao-modelos.md): AVA-C01, AVA-C13, AVA-P02, AVA-P05, CUS-08
- [regras-engenharia.md](regras-engenharia.md): ENG-P09
- [regras-metodo.md](regras-metodo.md): MET-10, MET-13, MET-P05, MET-S03, MET-S04, MET-S05
- [regras-operacao.md](regras-operacao.md): OPS-04
- [regras-organizacao.md](regras-organizacao.md): ORG-01, ORG-02, ORG-03, ORG-04, ORG-05, ORG-06, ORG-07, ORG-08, ORG-09, ORG-10, ORG-11, ORG-P01, ORG-P02, ORG-P03, ORG-P04, ORG-P05, ORG-P06, ORG-S01, ORG-S02, ORG-S03, ORG-S04, ORG-S05
- [regras-pedido.md](regras-pedido.md): PED-P05
- [regras-pessoa.md](regras-pessoa.md): PES-16
- [regras-revisao.md](regras-revisao.md): REV-02, REV-10, REV-P05
- [regras-seguranca.md](regras-seguranca.md): SEG-35

### C14 — Uso pessoal, aprendizado, privacidade e golpes (40 regras)

- [regras-avaliacao-modelos.md](regras-avaliacao-modelos.md): AVA-C01, AVA-C02, AVA-C03, AVA-C04, AVA-C05, AVA-C06, AVA-C07, AVA-C08, AVA-C09, AVA-C10, AVA-C11, AVA-C12, AVA-C13
- [regras-pessoa.md](regras-pessoa.md): PES-01, PES-02, PES-03, PES-07, PES-08, PES-09, PES-10, PES-12, PES-13, PES-14, PES-15, PES-16, PES-17, PES-18, PES-19, PES-20, PES-21, PES-P01, PES-P02, PES-P03, PES-P04, PES-P05, PES-P06, PES-S03, PES-S04, PES-S05, PES-S06
