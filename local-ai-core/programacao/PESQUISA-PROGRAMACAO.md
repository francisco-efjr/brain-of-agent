# Pesquisa: core de programação no PC

Data: 2026-11-19 · Pesquisador: Claude Opus 5.5 (Claude Code) · Consultas de busca novas: 16 · Fontes diretas: 28 (7 da casa, 21 externas) · Itens validados da casa reaproveitados: cerca de 196.

Este tema se apoia em duas camadas. A primeira é a pesquisa já validada do próprio Brain of Agent (`docs/dev-segments/research/`), feita em outubro de 2026 com pesquisador e validador separados, sobre qualidade de código, git e releases, QA, ciclo de engenharia e ferramentas de linha de comando: cerca de 196 itens aprovados, cada um com suas fontes. A segunda são buscas novas sobre o que essa pesquisa não cobria para uma IA local: desenvolvimento no Windows e riscos específicos de agentes que programam.

## 1. Achados principais

1. **Evidência antes de "pronto".** É o item mais repetido da casa: verificação executável e saída colada, nunca afirmação (H-01 V-01, H-02 V-15, H-03 V-32).
2. **Teste que falha primeiro.** Bug se corrige com teste vermelho pelo motivo certo, e três correções falhas pedem revisão da hipótese (H-01 V-04, H-02 V-17).
3. **Pequeno e separado.** Mudança pequena, refatoração separada de comportamento, fatias verticais (H-01 V-18, H-04 V-08). Mudanças pequenas são mais fáceis de recuperar (E-19).
4. **Pacotes inventados são vetor de ataque.** Cerca de 20% dos pacotes sugeridos por modelos não existiam num estudo da USENIX Security 2025, e os nomes se repetem (E-05); medições de 2026 ainda acharam de 4,6% a 6,1% (E-06). Daí dependência nova como R2 com conferência.
5. **Produção fora de alcance.** O caso de 2025 em que um agente apagou um banco de produção durante um congelamento de código, sem backup para voltar (E-10), sustenta a regra de nunca tocar produção.
6. **Segredo vazado se troca primeiro.** Limpar o histórico não desfaz a exposição; o guia do GitHub manda tratar como comprometido e trocar (E-07).
7. **O Windows tem armadilhas próprias.** Fim de linha (E-01), caminhos longos (E-02, E-03), venv e lançador `py` (E-11, E-12), versões de Node (E-13), desempenho de build (E-04).
8. **Ceticismo sobre ganho de velocidade.** Desenvolvedores experientes ficaram 19% mais lentos com IA num estudo controlado, achando que estavam mais rápidos (E-09); pipelines simples competem com agentes complexos (E-08).

## 2. Validação da esteira para programação

| Passo | Em programação | Evidência |
| --- | --- | --- |
| 0 Classificar | Ler e testar é R0; branch e commit local, R1; dependência e config global, R2; push, deploy e produção, R3 | E-10, H-02 V-38 |
| 1 Estruturar | Critério de aceite; instruções do projeto; mapa do código | H-01 V-10, V-32, H-06 |
| Observar | `git status` e linha de base de testes antes de mudar | H-02 V-01 |
| 2 a 5 Visão a conceber | Plano curto; pular plano se o diff cabe numa frase | E-20, H-02 V-01 |
| 6 Produzir | Branch nova, teste primeiro, fatia pequena | H-02 V-17, H-04 V-08 |
| 7 Testar de novo | Testes, build, lint, tipos e leitura do diff | H-01 V-01, V-17 |
| 8 Validar o escopo | Só o pedido; vizinho vira sugestão | H-01 V-10 |
| 9 Implementar | Commit local em Conventional Commits | H-02 V-18 |
| 10 Verificar e registrar | Relatório com testes antes e depois, como testar e como desfazer; bastão em trabalho longo | E-17, H-04 V-11 |

A esteira serve sem mudança. O ensaio sem efeito do tema é a própria suíte de testes rodada na branch local.

## 3. Decisões de desenho

- **Cartão no perfil padrão.** Programação entra como cartão de 7 linhas no `CORE.md` padrão; quem programa todo dia pode montar `--temas programacao,windows,memoria:cartao` ou usar o perfil `completo`.
- **Reaproveitar a casa, não repetir.** A referência aponta para os itens validados (`H-0x V-NN`) em vez de copiar o conteúdo deles.
- **Comandos em PowerShell** e equivalentes do Git Bash quando o projeto pede bash.

## 4. Limites

- As buscas novas foram conferidas por trechos de resultado, não lidas na íntegra.
- Os números de alucinação de pacotes e de produtividade são dos autores e dependem de modelo e data.
- O incidente da Replit foi reconstruído por reportagens; os números variam entre fontes.
- Nada foi executado no PC do dono; os casos de eval estão `designed_not_executed`.

## 5. Fontes

### 5.1 Pesquisa validada da casa (H)

| ID | Arquivo | Itens | Usado em |
| --- | --- | --- | --- |
| H-01 | `docs/dev-segments/research/code-quality-refactoring/VALIDATED.md` | 40 aprovados | Verificação, depuração, escopo, revisão, refatoração, dependências |
| H-02 | `docs/dev-segments/research/git-workflow-release/VALIDATED.md` | 39 aprovados | Fluxo, commits, desfazer, force-with-lease, bisect, SemVer |
| H-03 | `docs/dev-segments/research/qa-testing/VALIDATED.md` | 40 aprovados | Pirâmide, TDD, flaky, verificação antes de concluir |
| H-04 | `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md` | 37 aprovados | Spec, fatias, contexto e handoff, Chesterton, flags |
| H-05 | `docs/dev-segments/research/cli-desktop-tooling/VALIDATED.md` | 40 aprovados | Scripts PowerShell |
| H-06 | `docs/research/agentes-desenvolvimento.md` | 9 seções | Mapa de repositório, ciclo de implementação, isolamento |
| H-07 | `docs/dev-segments/foundation/house-style.md` e `prompt-principles.md` | - | Rótulos epistêmicos, CI verde não é fluxo provado |

### 5.2 Fontes externas (E)

| ID | Fonte | Classe | Status | Usado em |
| --- | --- | --- | --- | --- |
| E-01 | [GitHub: Configuring Git to handle line endings](https://docs.github.com/en/get-started/git-basics/configuring-git-to-handle-line-endings) | A | Busca | `.gitattributes`, autocrlf, renormalize |
| E-02 | [Microsoft Learn: Maximum path length limitation](https://learn.microsoft.com/windows/win32/fileio/maximum-file-path-limitation) | A | Busca | LongPathsEnabled |
| E-03 | [Git for Windows: long paths](https://gitforwindows.org/git-cannot-create-a-file-or-directory-with-a-long-path.html) | A | Busca | `core.longpaths` |
| E-04 | [Microsoft Learn: Set up a Dev Drive](https://learn.microsoft.com/en-us/windows/dev-drive) | A | Busca | Volume ReFS para código |
| E-05 | [Spracklen et al. We Have a Package for You (USENIX Security 2025)](https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen) | A | Busca | Pacotes inventados |
| E-06 | [Reavaliação de alucinação de pacotes (2026)](https://www.alphaxiv.org/abs/2605.17062) | B | Busca | Taxas em modelos novos |
| E-07 | [GitHub: Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) | A | Busca | Trocar segredo, filter-repo |
| E-08 | [Xia et al. Agentless (FSE 2025)](https://arxiv.org/abs/2407.01489) | A | Busca | Localizar, corrigir, validar |
| E-09 | [METR: early-2025 AI and experienced developers](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) | A | Busca | 19% mais lento |
| E-10 | [Fortune: Replit wiped a database (2025)](https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/) e [AI Incident Database](https://incidentdatabase.ai/cite/1152/) | B | Busca | Produção fora de alcance |
| E-11 | [Microsoft Learn: Python on Windows](https://learn.microsoft.com/en-us/windows/python/) | A | Busca | winget, lançador `py` |
| E-12 | [Python docs: Using Python on Windows](https://docs.python.org/3/using/windows.html) | A | Busca | venv, lançador |
| E-13 | [Microsoft Learn: Install Node.js on Windows](https://learn.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-windows) | A | Busca | nvm-windows |
| E-14 | [npm docs: npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci) | A | Busca | Instalação travada pelo lockfile |
| E-15 | [The Twelve-Factor App: Config](https://12factor.net/config) | A | Busca | Configuração no ambiente |
| E-16 | [gitleaks (README)](https://github.com/gitleaks/gitleaks) | B | Busca | Varredura de segredos |
| E-17 | [Anthropic: Effective harnesses for long-running agents](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents) | A | Busca | Lista de tarefas, progresso, retomada |
| E-18 | [OpenAI: Introducing SWE-bench Verified (2024)](https://openai.com/index/introducing-swe-bench-verified/) | A | Busca | Limites de benchmarks |
| E-19 | [DORA: software delivery performance metrics](https://dora.dev/guides/dora-metrics/) | A | Busca | Mudanças pequenas |
| E-20 | [Claude Code: best practices](https://code.claude.com/docs/en/best-practices) | A | Busca | Explorar, planejar, implementar, commitar |
| E-21 | [git restore](https://git-scm.com/docs/git-restore) | A | Busca | Voltar arquivo |

Contagem: 7 (H) + 21 (E) = 28 fontes diretas; as fontes H somam cerca de 196 itens validados, com fontes próprias listadas em cada arquivo.
