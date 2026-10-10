# Ambiente, sandbox e camadas automáticas

Fontes (conferidas em 2026-10-10): modelo de segurança (V-01, https://code.claude.com/docs/en/security); sandbox (V-09, https://code.claude.com/docs/en/sandboxing e https://www.anthropic.com/engineering/claude-code-sandboxing); security-guidance (V-02, https://code.claude.com/docs/en/security-guidance); Claude Security (V-29, https://code.claude.com/docs/en/claude-security); Action de CI (V-04). Redação própria. Nomes de comandos e chaves de sandbox não foram listados nas fontes lidas: **Não verificado**; siga a documentação da versão instalada.

## Sumário

1. Onde o trabalho com código não confiável deve rodar
2. Sandbox: o que cobre e o que não cobre
3. Windows
4. Plugin security-guidance
5. Plugin claude-security
6. Action de CI
7. Escolha de camadas

## 1. Onde o trabalho com código não confiável deve rodar

| Cenário | Recomendação |
| --- | --- |
| Código ou repositório próprio e confiável | modo manual ou auto com `deny` de segredos; sandbox quando disponível |
| Scripts ou chamadas a serviços de origem duvidosa | VM, dev container ou WSL2 (V-01) |
| PR de fork, issue ou página como entrada | não canalizar direto para a sessão; pedir resumo isolado; revisar comandos propostos antes de aprovar |
| Agente autônomo ou CI | sandbox, permissões mínimas, sem credenciais de produção, PR de fonte confiável |

`bypassPermissions` (flag `--dangerously-skip-permissions`) é **risco**, não padrão: só em sandbox e repositório confiável, e não protege de prompt injection (V-05).

## 2. Sandbox: o que cobre e o que não cobre (V-09)

- Isolamento de arquivos: escrita limitada ao diretório atual. Isolamento de rede: acesso por proxy externo com lista de domínios e confirmação para domínio novo.
- Mecanismos citados: bubblewrap (Linux) e seatbelt (macOS); um isolamento cobre a lacuna do outro.
- A Anthropic relata que o sandbox reduziu 84% dos pedidos de permissão em uso interno (sem metodologia; não independente).
- Cobre comandos de shell. **Ferramentas de arquivo, MCP e hooks rodam fora do sandbox**: mantenha `permissions.deny` para leitura de segredos.
- Credenciais de produção ficam fora do ambiente do agente. No modo web, credenciais de git ficam fora do sandbox e um proxy confere a operação (por exemplo, push só para a branch configurada).

## 3. Windows

A documentação de sandboxing diz que ele roda em macOS, Linux e WSL2. No **Windows nativo os comandos rodam sem sandbox**. O artigo de engenharia de 2025-10-20 cita só Linux e macOS; vale a documentação atual.

Recomendação para quem está no Windows:
1. Trabalhar com código não confiável em WSL2 ou dev container, mantendo o projeto no sistema de arquivos do Linux (melhor desempenho e isolamento).
2. Não habilitar WebDAV e não acessar caminhos `\\*` por meio do agente (aviso da doc de segurança, V-01).
3. Manter `permissions.deny` para `.env`, `~/.ssh` e `~/.aws` também no Windows (formatos `./`, `//absoluto`, `~/`).
4. Guard PreToolUse: executar o interpretador disponível (`python`, `py -3`) e testar com o marcador no próprio ambiente.

## 4. Plugin security-guidance (V-02)

Três camadas, e nenhuma bloqueia:
1. **Por edição**: padrões sem modelo (`eval(`, `new Function`, `os.system`, `child_process.exec`, `pickle`, `dangerouslySetInnerHTML`, `.innerHTML =`, `document.write`, edições em `.github/workflows/`). Um aviso por padrão, por arquivo, por sessão.
2. **Fim do turno**: revisor com contexto novo sobre o diff do que mudou (inclui Bash e subagentes), em segundo plano; até 30 arquivos; no máximo 3 disparos seguidos.
3. **Commit/push** feito pelo Bash do Claude: revisão agêntica que lê chamadores e sanitizadores; limite de 20 por hora.

Arquivos do projeto: `.claude/claude-security-guidance.md` (também em `~/.claude/` e versão `.local.md`; teto combinado de 8 KB) e `security-patterns.{yaml,yml,json}` (até 50 regras, campo `reminder` até 1 KB; JSON funciona sempre, YAML exige PyYAML). Regras são aditivas: não suprimem classes de vulnerabilidade. Desligar com `ENABLE_PATTERN_RULES`, `ENABLE_STOP_REVIEW`, `ENABLE_COMMIT_REVIEW`, `ENABLE_CODE_SECURITY_REVIEW`, `SECURITY_GUIDANCE_DISABLE`.

O que o usuário precisa saber antes de habilitar:
- Custo de uso do modelo a cada revisão de turno e de commit (modelo padrão observado: Opus 4.7, configurável por `SECURITY_REVIEW_MODEL` e `SG_AGENTIC_MODEL`).
- Exige repositório git; Python 3.7+ (3.10+ para a revisão agêntica).
- No primeiro uso cria um venv em `~/.claude/security/` e instala o Agent SDK por pip: rede e código de terceiros na máquina.
- Pode perder problemas: é camada de defesa em profundidade, não garantia. Limiares e taxas de falso positivo de blogs/leads não foram confirmados e não devem ser citados.

Modelo de guia do projeto: `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/guia-seguranca-projeto.md`; exemplo de regras por edição: `security-patterns.exemplo.json` no mesmo diretório.

## 5. Plugin claude-security (V-29)

Instalação documentada: `/plugin install claude-security@claude-plugins-official` (documentar; não executar sem decisão do usuário). Mapeia arquitetura e modelo de ameaça; cada candidato vai a verificadores independentes que tentam derrubá-lo; severidade e confiança ficam limitadas ao que a verificação sustenta; correções são feitas numa cópia de trabalho, revisadas por agente independente com testes do projeto, e gravadas só se a revisão atestar; patches nunca são aplicados automaticamente. Saídas `.md`, `.jsonl` e `.sarif`. Requisitos: Python 3.9+ e git. Custo alto de tokens, execução não determinística, telemetria de uso desligável por variáveis, licença conforme o LICENSE do plugin (o README não informa). Este plugin recomenda, não duplica.

## 6. Action de CI (V-04)

Documentada, não instalada: entradas `claude-api-key`, `comment-pr`, `upload-results`, `exclude-directories`, `claude-model`, `claudecode-timeout`, `run-every-commit`, `false-positive-filtering-instructions`, `custom-security-scan-instructions`; saídas `findings-count` e `results-file`; exemplo com `pull-requests: write` e `contents: read`. Cuidados: o README usa `@main` (fixe por SHA), o modelo padrão do README é antigo (defina o modelo), a Action não é endurecida contra prompt injection (PR de fonte confiável ou aprovação de mantenedor), chave só como segredo do repositório. Achado de modelo é sugestão: humano decide bloquear merge.

## 7. Escolha de camadas

| Preciso de | Camada | Observação |
| --- | --- | --- |
| Negar leitura de arquivos sensíveis | `permissions.deny` | aplicado pelo Claude Code; cobre ferramentas de arquivo |
| Impedir rede/escrita fora do projeto em comandos | sandbox (macOS, Linux, WSL2) | Windows nativo: não há |
| Aviso/bloqueio de comando destrutivo | hook PreToolUse com falha fechada | heurístico; testar com marcador |
| Revisão do que o Claude escreve | security-guidance / claude-security | custo e instalação; não bloqueiam |
| Revisão em PR | Action de CI + revisão humana | pin por SHA, modelo explícito, PR de fonte confiável |
| Política obrigatória do time | configuração gerenciada | o usuário não pode afrouxar |

Tradeoffs completos: `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/decisoes-e-tradeoffs.md`.
