# Decisões e tradeoffs de segurança de aplicações

Cada decisão traz critério, custo e quando reverter. Decisão material (muda arquitetura, permissões ou custo) merece ADR curto; decisão local e reversível não. Itens com V-nn estão em `fontes.md`.

## Sumário

1. Hook, deny, sandbox ou CI: onde colocar o controle
2. Modo auto ou manual; bypass
3. Revisor com ou sem Bash
4. Skill, agente, plugin oficial ou ferramenta externa
5. Destilar ou copiar texto de terceiros
6. Exclusões padrão: manter, ajustar ou remover
7. Custo de tokens versus cobertura
8. Escopo estático ou ativo
9. Guard de hook: ask ou deny
10. Confiança única (Alta, Média, Baixa) em vez de percentuais
11. Reescrever histórico do Git depois de vazar segredo
12. ADR de segurança: quando escrever

## 1. Hook, deny, sandbox ou CI

| Controle | Garante | Não garante | Use quando |
| --- | --- | --- | --- |
| `permissions.deny` (settings) | O Claude Code recusa a ferramenta; deny vence allow; vale para o caminho pedido ou o alvo do symlink | Regra de Bash casa o texto do comando, não a intenção; não cobre processos filhos | Impedir leitura de `.env`, `~/.ssh`, `~/.aws` por ferramentas de arquivo (V-05) |
| Sandbox | Isolamento de arquivos e rede dos comandos de shell | Ferramentas de arquivo, MCP e hooks rodam fora dele; Windows nativo sem sandbox | Rodar código não confiável em macOS, Linux ou WSL2 (V-09) |
| Hook PreToolUse | Heurística programável antes da ação; `exit 2` bloqueia | Falha aberta por padrão; decisão do hook não contorna deny/ask; regex é contornável | Guardrail adicional para comandos destrutivos, testado com marcador (V-06, V-07) |
| CI (Action, SAST, SCA) | Executa fora da máquina do dev, com permissões mínimas | Action não é endurecida contra prompt injection; achado é sugestão | Revisão em PR de fonte confiável; humano decide o bloqueio (V-04) |
| Instrução em CLAUDE.md | Orienta o comportamento | Não muda o que é permitido | Convenções e contexto; nunca como fronteira (V-05, V-31) |

Regra de decisão: o que deve valer sempre vira permissão, sandbox ou CI; o que orienta vira CLAUDE.md. Combine camadas: nenhuma sozinha basta.

## 2. Modo auto ou manual; bypass

- Verificado (V-01): o modo auto (classificador) é o modo inicial em sessões interativas do terminal e do VS Code a partir da 2.1.283; o modo manual continua disponível. O classificador não vê resultados de ferramentas, então não é defesa contra injeção em saída de ferramenta.
- Preferência: manual ou auto com deny rules e sandbox para trabalho com conteúdo de terceiros; conferir `/permissions` e `claude --version`.
- `bypassPermissions` e `--dangerously-skip-permissions` removem a confirmação: risco, aceitável só dentro de sandbox isolado e repositório confiável, e `permissions.disableBypassPermissionsMode = "disable"` (de preferência em configuração gerenciada) impede o uso acidental (V-05). Nomes de chaves: conferir na versão instalada.

## 3. Revisor com ou sem Bash

Conflito: o agente revisor somente leitura não tem Bash (V-08), mas a revisão precisa do `git diff` (V-03).
Decisão: a skill (thread principal) coleta o diff com Bash restrito a `git diff/log/show/status` e passa o diff ao agente. O agente nunca tem Bash. Custo: o diff entra no contexto duas vezes; para diffs grandes, passe lista de arquivos priorizada pela triagem. Se Bash for inevitável, restrinja por `permissions.deny` ou hook, pois `Bash(git push *)` em `disallowedTools` remove o Bash inteiro (V-08).
Reverter quando: o diff for tão grande que a cópia estoure o contexto; então divida por diretório.

## 4. Skill, agente, plugin oficial ou ferramenta externa

| Necessidade | Escolha | Porquê |
| --- | --- | --- |
| Revisar o diff atual com relatório fixo | Skill `security-review-diff` | Aceita base informada, um critério de confiança, declara cobertura |
| Perspectiva isolada e somente leitura | Agente (`security-reviewer`, `finding-verifier`) | Contexto novo; tools mínimos |
| Varredura ampla do repositório com verificadores | Plugin oficial `claude-security` (documentar, não instalar) | Verificadores que tentam refutar; alto custo de tokens (V-29) |
| Revisão por edição e por commit | Plugin oficial `security-guidance` (documentar, não instalar) | Três camadas; instala o Agent SDK por pip no primeiro uso (V-02) |
| Comando embutido `/security-review` | Já existe | Compara com o branch padrão de `origin`; exige remoto (V-03) |
| SAST, segredos, SCA | Scanners no CI (comandos documentados) | Nenhuma fonte oficial lida: Não verificável |

O plugin não duplica o que o produto oficial faz; recomenda.

## 5. Destilar ou copiar texto de terceiros

- OWASP Cheat Sheets, ASVS e Trail of Bits são CC BY-SA 4.0 (V-16, V-17, V-28); o plugin é MIT. Copiar texto pode atrair ShareAlike. Decisão: destilar com redação própria, listar atribuição em `fontes.md` e no README, e revisar por humano antes de publicar (R4 do design; a interpretação jurídica é Suposição).
- MIT e Apache-2.0 (security-review, getsentry, awesome-copilot) permitem trecho curto com atribuição, mas as fontes têm inconsistências (limiares, modelo antigo): destilar também é melhor para qualidade.
- CC0 (awesome-cursorrules) permite reuso livre; ainda assim o bloco foi reescrito em tom calmo.

## 6. Exclusões padrão: manter, ajustar ou remover

O comando oficial traz 18 exclusões e 12 precedentes (V-03); o gstack `cso` desaconselha exclusões em bloco (Inferido, brain). Decisão: lista padrão ajustável, mostrada no relatório.

| Exclusão | Mantida? | Ajuste |
| --- | --- | --- |
| Negação de serviço e esgotamento | Sim, por padrão | Não vale para endpoint caro, pago (custo) ou sem autenticação; remova "rate limiting" em API pública, login e financeiro |
| Dependência desatualizada sem CVE explorável | Sim | Vira achado com CVE alcançável (`secrets-supply-chain-review`) |
| Arquivos só de teste ou documentação | Sim | Não vale para fixture com segredo real |
| Variáveis de ambiente e flags de CLI "confiáveis" | Sim | Variável pode vir de workflow não confiável (CI) |
| Checagem de autorização ausente só no cliente | Reformular | O achado é a falta no servidor |
| Segredo histórico | Não excluir | Segredo no histórico continua comprometido |

## 7. Custo de tokens versus cobertura

- security-guidance revisa a cada turno e commit e usa por padrão um modelo caro (V-02); claude-security tem custo alto (V-29); subagentes de revisão multiplicam tokens.
- Decisão padrão: revisão do diff com `maxTurns` baixo, sem paralelismo, severidade alta com um verificador. Suba a cobertura (mais verificadores, varredura ampla) só para código de autenticação, dinheiro ou multi-tenant.
- Não existe taxa de falso positivo ou negativo confiável por modelo (lacuna 12): não prometa números.

## 8. Escopo estático ou ativo

- Padrão: estático (leitura de código), rótulo "não executado". Teste ativo só em sistema próprio, com autorização escrita (hosts, janela, técnicas, contas, contato de emergência), dados sintéticos (brain QA, Inferido).
- Sistema de terceiro: entregar casos de verificação e ferramentas ao dono; nunca executar scan. ZAP baseline (passivo) é aceitável em homologação própria; full scan só em ambiente próprio e fora do horário de uso.
- O helper `gstack-cso` (execução isolada) não é portado: depende de distribuição instalada e executaria código de terceiros.

## 9. Guard de hook: ask ou deny

| Variante | Quando | Risco |
| --- | --- | --- |
| `deny` (`exit 2`) | Formas catastróficas: `rm -r` de `/`, `~`, `$HOME`; `curl` encadeado a `sh`; force-push na branch padrão | Falso positivo trava o trabalho; o usuário precisa editar o guard |
| `ask` | Destrutivo reversível por humano: `DROP TABLE`, `TRUNCATE`, `git reset --hard`, `kubectl delete`, `docker system prune` | O usuário pode aprovar por hábito; é aviso best-effort, não política |

Padrões do projeto são somente aditivos (a configuração só adiciona regras, nunca suprime a base) e só comandos simples (sem `;`, `&&`, `|`) entram no deny; compostos caem no ask. Fontes: V-06, gstack `careful` (Inferido, brain).

## 10. Confiança única (Alta, Média, Baixa) em vez de percentuais

A fonte oficial usa corte de 80%, faixas 0,9 a 1,0 e escala 1 a 10 ao mesmo tempo (V-03). Decisão: Alta reporta, Média vira "Verificação pendente" com a pergunta a responder, Baixa descarta (V-30). Motivo: ninguém tem taxa de acerto calibrada; números sugerem precisão que não existe. Reverter quando houver dados medidos do próprio projeto.

## 11. Reescrever histórico do Git depois de vazar segredo

Ordem (V-19): revogar, rotacionar, apagar, registrar. Reescrever histórico quebra links de commits e não desfaz o vazamento. Decisão do dono do repositório: reescrever só se o segredo ainda não foi rotacionado por limitação operacional ou se houver dado sensível além de chave. O agente nunca faz `git push --force` sem autorização explícita.

## 12. ADR de segurança: quando escrever

Escreva ADR curto (contexto, decisão, alternativas, consequências, risco residual) quando: aceitar um risco (transferir ou aceitar na modelagem, V-17), adotar ou recusar um plugin/MCP com acesso a dados, mudar o modelo de autorização (RBAC para ABAC, tenant), ou desligar uma proteção (CSP, verificação de assinatura). Use `assets/templates/modelo-de-ameacas.md` (campo risco residual) e o modelo de ADR de `/architecture-design:playbook`. Mudança trivial ou correção localizada dispensa ADR.
