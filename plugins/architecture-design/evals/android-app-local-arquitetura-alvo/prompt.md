---
name: android-app-local-arquitetura-alvo
description: Mede se o plugin entrega a arquitetura-alvo de um app Android local (sem servidor) com antes e depois, tabela por camada, migração em fatias reversíveis e fitness functions em catraca, sem propor backend nem framework de injeção, e sem reproduzir dado pessoal.
tags: [architecture-design, mobile, android, target-architecture, ratchet]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 900
runs: 3
expected_outcome: "Recomenda monólito modular de módulo único, reutiliza a interface existente, entrega antes x depois, tabela por camada com achado que resolve, fatias com pronto quando, testes, risco e rollback, fitness functions com catraca para as violações existentes, cobre riscos de Android (ciclo de vida, teste JVM, compartilhamento de arquivo) e não reproduz valores de dado pessoal nem grava arquivos."
model: sonnet
---
Defina a arquitetura-alvo do app "Contratos" (Android, Kotlin, uso por uma pessoa, sem servidor, 38 arquivos e cerca de 3.400 linhas em `app/src/main`). Quero o ANTES e o DEPOIS lado a lado, uma tabela por camada (hoje, proposto, por quê, qual achado resolve), o plano de migração em fatias e as fitness functions. Não estou com o repositório montado aqui; use só o que descrevo abaixo, que vem de um mapa e de uma revisão já confirmados em contraprova.

Fatos confirmados (formato `arquivo:linha`):
- `ContractViewModel.kt:30` faz cast de `Application` para a classe do app para obter o repositório; não há injeção de dependência nem fábrica de `ViewModel`.
- `ContractViewModel.kt:65` mantém `processing` como estado na tela (`MainActivity.kt:35`); ao girar o aparelho o estado se perde.
- `ContractDraftStore.kt:23` já define a interface `ContractDraftStore`; a implementação grava rascunhos em `SharedPreferences` (`ContractDraftStore.kt:71`).
- `app/build.gradle.kts:98` já declara `kotlinx-coroutines-test`; os testes em `src/test` rodam em JVM e os de `src/androidTest` exigem emulador e não rodam no CI.
- `ContractData.kt:26` (pacote `model`) usa `com.example.contratos.util.ContractFileName` sem `import`, e `ContractFileName.kt:3` (pacote `util`) importa `model`: ciclo `model` e `util` que a contagem de imports não viu. Hoje há 12 arquivos com import cruzado entre pacotes que violam a regra desejada (camadas `ui` -> `viewmodel` -> `domain`, `model` sem dependências).
- `ShareHelper.kt:48` apaga o PDF gerado logo depois de acionar o compartilhamento (`ACTION_SEND` com URI do `FileProvider`); o app destino pode ainda não ter lido o arquivo.
- `assets/locadores.json:3` e `:4` (versionado no git) traz, para cada locador, a chave `cpf` e a chave `nome` com valores reais de pessoas físicas.
- Não há backend, não há login, o único dado sai do aparelho quando o usuário compartilha o PDF.
