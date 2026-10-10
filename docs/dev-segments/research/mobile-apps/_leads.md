# mobile-apps — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Pista é ponto de partida: reabrir a URL antes de citar. Segmento com cobertura fraca no atlas: tratar como lacuna aberta. Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| SwiftUI guidelines .mdc (CT-12) | https://github.com/PatrickJS/awesome-cursorrules | B (6) | Swift 6 concurrency, `@MainActor`, `.task(id:)`, `body` ≤ 50 linhas, IDs estáveis, mocks por protocolo, warnings como erros. CC0; trechos literais Verificados ("Always use stable `id`", "Treat warnings as errors."). |
| Padrão "Flexibility Notice" (CT-12) | https://github.com/PatrickJS/awesome-cursorrules | B | Adaptar à arquitetura existente em vez de impor estrutura. CC0. |
| Android Jetpack Compose e Flutter .mdc (CT-12) | https://github.com/PatrickJS/awesome-cursorrules | C (4) | Formato gerado, sem verificação; só como sinal. |
| vercel-labs/agent-skills (EC-07) | https://github.com/vercel-labs/agent-skills | A- | Atlas marca o repo para mobile; a pista exata (ex.: React Native) não foi detalhada: abrir e verificar. Licença da API null. |
| wshobson/agents (EC-10) | https://github.com/wshobson/agents | B | Atlas marca mobile; plugins específicos não listados: abrir. |
| garrytan/gstack (EC-11, BR-23) | https://github.com/garrytan/gstack | B | `ios-qa` e `ios-design-review` (ver brain); notas por dimensão. Não executar `bin/` e `setup`. |
| claude-plugins-official (AO-30) | https://github.com/anthropics/claude-plugins-official | A | Atlas lista mobile entre as tags; os 12 LSPs de `plugins/` podem incluir Swift/Kotlin (Não verificado): abrir `plugins/`. Apache-2.0. |
| awesome-cursorrules catálogo (EC-19, CT-06) | https://github.com/PatrickJS/awesome-cursorrules | B | Regras por stack; qualidade desigual. |
| Ask HN: agentic coding (CP-21) | https://news.ycombinator.com/item?id=46691243 | B | Fronteiras de módulo fortes, logar para o agente "ver"; citado com tag mobile. |
| Tests for mobile (CT-12, CT-17) | https://github.com/github/awesome-copilot/tree/main/instructions | B | Mocks por protocolo; pirâmide 60-70/20-30/5-10. MIT. |
| Prompting best practices (AO-01) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | A | Escopo mínimo, verificação, confirmação de ações visíveis (publicação em loja). |
| Security review (AO-24, BR-14) | https://github.com/anthropics/claude-code-security-review | A | Revisão de PR; OWASP Top 10:2025 verificado (BR-14); MASVS não consta no atlas. |

## 2. Repositórios e arquivos a abrir
- `PatrickJS/awesome-cursorrules/rules/swiftui-guidelines-…mdc` (Verificado no raw); `android-jetpack-compose-…`, `flutter-app-expert-…` (nomes truncados no atlas: localizar na pasta `rules/`).
- `vercel-labs/agent-skills` (pastas de React Native, se existirem).
- `anthropics/claude-plugins-official/plugins/` (LSPs).
- HIG, Material, documentação de Swift/Kotlin/Expo/Flutter, App Store Review Guidelines e Play policies não estão no atlas: lente authoritative.

## 3. Materiais oficiais Anthropic pertinentes
AO-30 (plugins oficiais, marcados com mobile), AO-01, AO-06, AO-24. Nenhum material Anthropic específico de mobile foi aprovado.

## 4. Padrões da comunidade
- Separar terminal e Xcode e declarar "limites do agente" no CLAUDE.md: apenas princípio Inferido (CP-28 foi rejeitado).
- Adaptar à arquitetura existente em vez de reestruturar (CT-12).
- Warnings como erros; IDs estáveis; concorrência explícita (CT-12).
- Evidência de que o agente funciona depende de escopo e stack (CP-21).

## 5. O que o brain-of-agent já oferece
- `brains/qa/references/mobile.md`, `brains/fullstack/references/apple-design.md`, `vendor/gstack/ios-qa/SKILL.md`, `vendor/gstack/ios-design-review/SKILL.md`.
- BR-23: notas 0 a 10 por dimensão com "o que seria um 10"; `apple-design.md` = preferência de acabamento, não imposição de plataforma.
- BR-14: referências de acessibilidade (WebAIM) e segurança; NBR 17060 e EAA não verificados.
- BR-18: tiers por risco. BR-03: modo `MOBILE-COMPLETO`.

## 6. Lacunas e cuidados
- Acessibilidade mobile, publicação em lojas, offline-first, push, deep links, permissões, performance e bateria: sem fonte aprovada no atlas.
- React Native/Expo e Flutter só têm sinal fraco; Android/Compose em formato gerado.
- Rejeitado: thepromptshelf, devlog Godot e post Reddit (CP-28); não usar.
- Nada de executar simuladores, builds ou publicação sem autorização explícita do usuário.
