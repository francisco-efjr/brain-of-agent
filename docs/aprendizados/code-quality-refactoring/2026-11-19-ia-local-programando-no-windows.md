---
data: 2026-11-19
tags: [code-quality-refactoring, git-versionamento-release, seguranca-hardening]
plugins: [code-quality-refactoring, git-workflow-release, security-appsec, cli-desktop-tooling]
agentes: [code-quality-refactoring:code-reviewer, git-workflow-release:revisor-diff, security-appsec:security-reviewer]
contexto: "Regras para uma IA local que programa nos projetos do usuário num PC Windows"
tipo_de_sessao: pesquisa
modelo: claude-opus-5-5
---
# IA local programando no Windows: pacotes inventados, produção e armadilhas do Windows

Origem: tema `local-ai-core/programacao/`, que condensa cerca de 196 itens validados da casa e 21 fontes externas novas. Detalhes em `local-ai-core/programacao/PESQUISA-PROGRAMACAO.md`.

## Boas práticas confirmadas
- [Verificado na documentação] Dependência nova só depois de conferir que o pacote existe e quem publica. Motivo: cerca de 20% dos pacotes sugeridos por modelos não existiam num estudo da USENIX Security 2025, e os nomes se repetem, o que permite golpes; medições de 2026 ainda acharam 4,6% a 6,1%.
- [Verificado na documentação] Produção fora do alcance do agente. Motivo: caso de 2025 em que um agente apagou um banco de produção durante um congelamento de código, sem backup para voltar.
- [Verificado na documentação] Segredo commitado se troca primeiro; limpar histórico vem depois, muda hashes e exige que outros clones limpem. Evidência: guia do GitHub.
- [Verificado na documentação] Pipelines simples (localizar, corrigir, validar com teste de reprodução) competem com agentes complexos. Evidência: Agentless (FSE 2025).

## Armadilhas
- [Verificado na documentação] Diff com o arquivo inteiro alterado no Windows → fim de linha → respeitar `.gitattributes`, não mexer em `core.autocrlf` global, renormalizar só em commit próprio.
- [Verificado na documentação] "Filename too long" → `git config core.longpaths true` no repositório; habilitar no Windows é mudança de registro em HKLM.
- [Inferido] `Activate.ps1` do venv esbarra na política de execução → chamar `.\.venv\Scripts\python.exe` direto.
- [Verificado na documentação] Sensação de velocidade engana: desenvolvedores experientes ficaram 19% mais lentos com IA num estudo controlado, achando que estavam mais rápidos.

## Pesquisa
| Fonte (URL) | Classe | Acesso | Achado |
| --- | --- | --- | --- |
| https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen | A | 2026-11-19 | Pacotes inventados por modelos |
| https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository | A | 2026-11-19 | Segredo vazado |
| https://docs.github.com/en/get-started/git-basics/configuring-git-to-handle-line-endings | A | 2026-11-19 | Fim de linha |
| https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ | A | 2026-11-19 | 19% mais lento |
| https://arxiv.org/abs/2407.01489 | A | 2026-11-19 | Agentless |

## Lacunas
- A pesquisa da casa não tinha itens sobre desenvolvimento no Windows (fim de linha, caminhos longos, venv, Dev Drive) nem sobre pacotes inventados.

## Promoção sugerida
- `code-quality-refactoring` / `## Gotchas`: conferir existência e editor de pacote antes de propor dependência.
- `cli-desktop-tooling` / playbook: armadilhas de fim de linha e caminhos longos no Windows.
