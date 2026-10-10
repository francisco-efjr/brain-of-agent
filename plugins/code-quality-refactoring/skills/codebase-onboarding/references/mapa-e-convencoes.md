# Mapa, convenções e buscas para onboarding de código

Sumário: 1 Manifestos por ecossistema · 2 Pontos de entrada · 3 Convenções: o que procurar e como contar · 4 Mapa de dependências · 5 Modelo de saída · 6 research.md · 7 Exemplo · 8 Sugestões para o CLAUDE.md · 9 Atribuições.

Rótulos: Verificado = visto em arquivo lido nesta sessão; Inferido = deduzido ou conhecimento estável; Suposição = escolha ajustável. As tabelas de manifestos e de padrões de busca são conhecimento estável do domínio (Inferido); confira na versão do seu projeto.

## 1. Manifestos por ecossistema

| Ecossistema | Manifestos e configs (Glob) | O que ler |
| --- | --- | --- |
| JavaScript/TypeScript | `package.json`, `tsconfig*.json`, `pnpm-workspace.yaml`, `turbo.json`, `nx.json` | `scripts`, `engines`, `workspaces`, `main`/`exports`, `bin` |
| Python | `pyproject.toml`, `setup.cfg`, `requirements*.txt`, `tox.ini`, `noxfile.py` | `[project]`, `[tool.*]`, scripts, versões do Python |
| Go | `go.mod`, `go.work`, `Makefile` | módulo, versão do Go, diretórios `cmd/` |
| Rust | `Cargo.toml`, `Cargo.lock`, `rust-toolchain*` | `[workspace]`, `[[bin]]`, features |
| Java/Kotlin | `pom.xml`, `build.gradle(.kts)`, `settings.gradle(.kts)` | módulos, plugins, versão do JDK |
| .NET | `*.sln`, `*.csproj`, `global.json` | projetos, framework alvo |
| Ruby | `Gemfile`, `*.gemspec`, `Rakefile` | gems, tarefas |
| PHP | `composer.json` | autoload, scripts |
| Genérico | `Makefile`, `Dockerfile`, `docker-compose*.yml`, `.github/workflows/*`, `.gitlab-ci.yml` | comandos oficiais de build/teste, serviços de apoio |

Leia a configuração de CI antes dos scripts locais: ela mostra o comando que a equipe considera "verde". Comandos lidos aqui são descritos, não executados.

## 2. Pontos de entrada

| Tipo | Onde procurar |
| --- | --- |
| Servidor HTTP | `main`, `app`, `server`, `routes`, decoradores de rota; `Grep` por `listen(`, `@app.route`, `@GetMapping`, `http.ListenAndServe` |
| CLI | campo `bin`, `console_scripts`, `cmd/`, `argparse`, `commander`, `cobra` |
| Worker/job | `queue`, `worker`, `cron`, `schedule`, consumidores de mensagem |
| Biblioteca | `main`/`exports`/`__init__.py`/`lib.rs`: o que é exportado é a API pública |
| Frontend | `index.html`, `main.tsx`/`main.jsx`, `app/` e `pages/`, roteador |
| Testes | pastas `test`, `tests`, `__tests__`, `spec`, arquivos `*_test.*`, `*.spec.*` |

## 3. Convenções: o que procurar e como contar

Regra de contagem: ocorrências são **arquivos distintos** onde o padrão aparece, não linhas. Use `Grep` com `output_mode` de contagem ou de arquivos. 3 ou mais arquivos: Verificado; 1 ou 2: Inferido. Registre o padrão de busca usado.

| Categoria | O que comparar | Busca de exemplo (adapte) |
| --- | --- | --- |
| Nomes | `camelCase` x `snake_case`, sufixos (`Service`, `Repository`, `Handler`), nomes de arquivos | Listar arquivos (`Glob`) e agrupar por formato |
| Estrutura | por camada (`controllers/`, `services/`) x por feature (`orders/`, `billing/`) | Árvore de 2 níveis |
| Erros | exceções x `Result`/`Either` x códigos de retorno; erros engolidos | `throw new` x `Result<`; `except Exception`, `catch (e) {}` |
| Testes | runner, nome (`test_*`, `*.spec.*`), fixtures, mocks x dublês reais, localização (ao lado x pasta `tests/`) | `Glob` de testes; `Grep` por `describe(`, `def test_`, `mock` |
| Logging | biblioteca, formato, nível, identificador de correlação | `Grep` por `logger.`, `console.log`, `log.` |
| Configuração | variáveis de ambiente, arquivo, validação na inicialização | `Grep` por `process.env`, `os.environ`, `viper` |
| Acesso a dados | ORM, SQL cru, repositórios, transações | `Grep` por `SELECT `, `session.`, `prisma.` |
| Importações | alias de caminho, imports relativos x absolutos, barris (`index.ts`) | `Grep` nos imports de 3 arquivos recentes |

Amostragem: leia ao menos um arquivo antigo e um recente por área; código recente costuma refletir o padrão atual e o antigo, o legado. Em dois padrões concorrentes, reporte os dois com contagem.

Exclua das buscas: `node_modules`, `vendor`, `dist`, `build`, código gerado, lockfiles.

## 4. Mapa de dependências

1. Liste as pastas de primeiro nível com a responsabilidade em uma linha (leia o `README` da pasta ou os primeiros arquivos).
2. Quem importa quem: `Grep` pelos imports que cruzam pastas (`from billing`, `import ... from "../orders"`); anote direção e contagem.
3. Camadas e violações: dependência de baixo nível para alto nível, ciclos entre pastas.
4. Áreas de risco (sinais, todos Inferidos até medidos): sem testes ao lado; arquivos com milhares de linhas; muitos autores; mudança frequente (`git log --since="6 months ago" --name-only --pretty=format:` com contagem); `TODO`/`HACK` antigos (`git blame` mostra a idade).

## 5. Modelo de saída

```markdown
## Resumo
<3 a 5 linhas>

## Comandos (lidos, não executados)
| Ação | Comando | Origem | Rótulo |

## Mapa
| Área | Caminho | Responsabilidade | Evidência |

## Convenções
| Categoria | Exemplo | Arquivos (contagem) | Rótulo |

## Riscos e hotspots
<lista com evidência>

## Perguntas abertas
<o que o código não responde>

## Status
DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
```

Para o `codebase-mapper`, o limite é ~60 linhas; um mapa maior vira `research.md` por pedido do usuário.

## 6. research.md

Gravar só a pedido, sem planejar:

```markdown
# Pesquisa: <tema>
Data: <AAAA-MM-DD> | Escopo: <pastas> | Modo: somente leitura
## O que existe
- <fato> (<caminho:linha>, Verificado)
## Como funciona o fluxo
1. <passo> (<caminho:linha>)
## O que não encontrei
- <termo buscado> em <onde> (Não encontrado; não significa que não exista)
## Riscos para a mudança prevista
- <risco> (<evidência>)
```

`plan.md` é uma etapa seguinte, só se pedida: abordagem, arquivos afetados, trade-offs, tarefas por fase, e uma parada para o usuário anotar antes de implementar (fluxo de V-25, relato pessoal de autor, classe C; use só para mudança maior que uma frase).

## 7. Exemplo: convenção de erro com amostra pequena

Entrada: árvore de pastas e 4 arquivos curtos colados (2 usam `Result<T, E>`, 1 usa `throw`, 1 não trata erros).

```text
Tratamento de erro (amostra: 4 arquivos lidos)
- Result<T, E>: src/orders/create.ts, src/orders/cancel.ts -> 2 arquivos, Inferido
- throw/try-catch: src/payments/charge.ts -> 1 arquivo, Inferido
- sem tratamento (funções puras): src/orders/total.ts -> 1 arquivo, não conta
Divergência: dois estilos na amostra. Não há evidência de qual é o padrão do projeto; 3 ou mais arquivos por estilo exigiriam ler mais código.
Pergunta aberta: o time padronizou Result? charge.ts é um desvio ou um módulo legado?
```

O que o exemplo evita: afirmar "o projeto usa Result" com 2 arquivos; escolher um estilo em silêncio; editar `charge.ts`.

## 8. Sugestões para o CLAUDE.md

Teste de poda para cada linha: "remover esta linha faria Claude errar?". Entram apenas fatos que não saem do código:

- comando exato de teste de um arquivo (`pytest tests/unit/test_x.py -q`), se o padrão do runner não bastar;
- convenção divergente do padrão da linguagem ("erros do domínio usam `Result`, nunca `throw`");
- fronteira que não se cruza ("não importar `billing` de `orders`");
- passo de verificação obrigatório antes de dar por pronto.

Fora: árvore de pastas, descrição genérica do repositório, "boas práticas" gerais. Menos de 200 linhas no total. Modelos em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/claude-md-snippets.md`.

## 9. Atribuições

- Descoberta de convenções com um arquivo de exemplo e contagem: ideia do agent-os (Builder Methods, MIT) em redação própria (V-32); nada instalado.
- Pesquisa antes de plano: Boris Tane, "How I Use Claude Code" (2026-02-10), relato pessoal, classe C (V-25); redação própria.
- Subagente de pesquisa que devolve resumo curto: documentação oficial de receitas do Claude Code (V-03), redação própria.
