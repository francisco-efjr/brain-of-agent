# Plano de incremento mobile: [nome da feature]

Adaptado do template `plano-incremento` do brain-of-agent (MIT, Francisco Edson). Use quando o diff não cabe em uma frase. Salve como `docs/plans/[feature].md` no projeto. Preencha só o que muda decisões.

## Objetivo e baseline

- Problema, usuário e comportamento atual:
- Critério de sucesso e fonte (spec, ticket):
- Plataformas e frameworks (iOS/SwiftUI, Android/Compose, RN/Expo, Flutter) com versões lidas e alvo mínimo:
- Arquitetura existente identificada (pastas, DI, navegação, estado): [arquivos lidos]
- Estado observado e reprodução (build, aparelho ou emulador, passos):
- Escopo, exclusões e autorização (o que pode mudar; ações externas fora do escopo):
- Ambiente do agente (SO; macOS disponível? aparelho ou emulador?):

## Fatia vertical

Ação do usuário → tela e estado → ViewModel/repositório → contrato com a API → dados locais → resultado observável. Descreva cada fronteira e sua falha e recuperação.

| Requisito | Alteração (arquivos) | Invariante | Contrato ou compatibilidade | Verificação (comando literal) e oráculo |
| --- | --- | --- | --- | --- |
| [ex.: salvar rascunho offline] | [ex.: DraftRepository.kt, DraftDao.kt] | [ex.: fonte local única] | [ex.: POST /drafts com chave de idempotência] | [ex.: `./gradlew testDebugUnitTest`; teste "rascunho sobrevive a reinício"] |

## Estados, plataforma e acessibilidade

- Estados de UI: vazio, carregando, erro, offline, permissão negada:
- Permissões e purpose strings envolvidas:
- Push, deep links ou segundo plano afetados:
- Acessibilidade: rótulos, alvos (44 pt / 48 dp), texto escalável, contraste, passagem humana com leitor de tela:
- Dados: migração local, compatibilidade com versão anterior do app:
- Timeout, duplicação, concorrência e autorização:

## Plano e riscos

| Fase | Artefato utilizável | Risco | Mitigação | Critério de saída |
| --- | --- | --- | --- | --- |
| 1 | [ex.: tela lê do banco local] | [ex.: migração] | [ex.: teste de atualização] | [ex.: testes verdes, saída colada] |

Decisões materiais (ADR necessário?): [sim/não e link]

## Validação

- Checks existentes a executar (build, lint, tipos, testes):
- Regressões novas e por quê:
- Integrações reais e isolamento:
- Roteiro manual (aparelho ou emulador) e efeitos persistidos:
- Não executável neste ambiente e risco restante (ex.: "build iOS Não verificável: sem macOS"):

## Entrega

- Como executar, configurar e observar:
- Publicação ou rollback somente dentro da autorização (ficha de ação, se houver):
- Evidências, pendências e próximo passo:
