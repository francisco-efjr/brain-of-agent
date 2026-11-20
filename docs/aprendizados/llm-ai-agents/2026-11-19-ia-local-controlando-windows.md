---
data: 2026-11-19
tags: [llm-ai-agents, seguranca-hardening, contexto-agente]
plugins: [llm-ai-agents, security-appsec, cli-desktop-tooling]
agentes: [llm-ai-agents:agent-architect, llm-ai-agents:agent-security-reviewer, llm-ai-agents:prompt-reviewer]
contexto: "Prompt de sistema para IA local (OpenJarvis + Ollama) que opera um PC Windows por PowerShell"
tipo_de_sessao: pesquisa
modelo: claude-opus-5-5
---
# IA local controlando o Windows: core de regras, segurança e desempenho

Origem: pesquisa de 98 fontes que gerou `local-ai-core/windows/` (PR 1 do repositório). Detalhes e todas as fontes em `local-ai-core/windows/PESQUISA-WINDOWS.md`.

## Boas práticas confirmadas
- [Verificado na documentação] Classificar o risco antes de agir (leitura, mudança pequena, mudança de sistema, destrutiva) e escalar a profundidade do processo e da aprovação pela classe. Motivo: pergunta simples não paga o custo de uma esteira completa, o que importa muito num modelo local lento. Evidência: aprovação proporcional ao risco no ITIL 4 e "least agency" na OWASP Agentic Top 10 2026.
- [Verificado na documentação] Separar teste de validação na esteira: teste confere se foi feito certo; validação confere se é a coisa certa. Evidência: definições de verificação e validação da NASA.
- [Verificado na documentação] Mostrar ensaio sem efeito antes de pedir aprovação de ação de alto impacto. No Windows o ensaio já existe: `-WhatIf` (ShouldProcess), `robocopy /L`, `DISM /ScanHealth`, Windows Sandbox. Evidência: OWASP ASI02 pede plano ou diff de ensaio antes da aprovação; Microsoft Learn documenta o ShouldProcess.
- [Verificado na documentação] Ter a reversão pronta antes de mudar: `reg export`, `Checkpoint-Computer`, `icacls /save`, `winget export`, `Export-ScheduledTask`. Evidência: material de SRE do Google sobre mudanças e reversão; guia de backup do registro da Microsoft.
- [Verificado na documentação] Rodar o agente sem elevação para que tudo que exige administrador passe pelo UAC. Motivo: a aprovação humana fica imposta pelo sistema operacional, fora do modelo. Evidência: Microsoft recomenda usuário padrão no UAC e contas de agente com privilégio limitado no Windows 11.
- [Verificado na documentação] Prompt de sistema curto e estável, com a base detalhada fora dele e buscada sob demanda. Motivo: o desempenho cai com contexto longo e com densidade de instruções, e prefixo idêntico aproveita cache de prompt. Evidência: Anthropic (context engineering), Lost in the Middle, IFScale, cache de prefixo do vLLM e do llama.cpp.

## Armadilhas
- [Verificado na documentação] OpenJarvis: `enforce_tool_confirmation = true` é aceito mas não é aplicado; o `shell_exec` só pede confirmação no `jarvis chat` e aprova sozinho no `jarvis ask`, no servidor HTTP e no app desktop; não há allowlist nem sandbox por padrão → o prompt é a única barreira se nada mais for configurado → rodar sem elevação, usar `jarvis chat` e restringir `allowed_dirs`. Não verificado numa instalação real.
- [Verificado na documentação] `Checkpoint-Computer` cria no máximo um ponto de restauração por 24 horas e é do Windows PowerShell 5.1 → planejar o ponto uma vez por janela de mudança e chamar via `powershell.exe` a partir do PowerShell 7.
- [Verificado na documentação] Nomes de contadores de desempenho são traduzidos (Windows em português usa `\Processador(...)`) → listar com `Get-Counter -ListSet` antes de consultar.
- [Verificado na documentação] O módulo nativo WindowsUpdateProvider sumiu a partir do Windows 10 2004 → não depender dele; PSWindowsUpdate é da comunidade e exige aprovação para instalar.
- [Inferido] Script elevado gravado pelo PowerShell 7 com UTF-8 sem BOM e executado pelo `powershell.exe` 5.1 estraga acentos em caminhos → gravar com `-Encoding utf8BOM`.
- [Verificado na documentação] As páginas oficiais do Ollama divergem sobre o contexto padrão (4.096 no FAQ, por VRAM na página de contexto) → medir com `ollama ps` em vez de presumir.

## Pesquisa
| Fonte (URL) | Classe | Acesso | Achado |
| --- | --- | --- | --- |
| https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ | A | 2026-11-19 | Least agency; ASI01 a ASI10; ensaio antes de aprovar; tratar todo texto lido como não confiável |
| https://www.anthropic.com/engineering/building-effective-agents | A | 2026-11-19 | Verdade do ambiente a cada passo, limites de iteração, sandbox, ferramentas à prova de erro |
| https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | A | 2026-11-19 | Menor conjunto de tokens de alto sinal; busca just-in-time; exemplos canônicos |
| https://blogs.windows.com/windowsexperience/2025/10/16/securing-ai-agents-on-windows/ | A | 2026-11-19 | Contas de agente distintas, privilégio limitado, XPIA como ameaça principal |
| https://ai.meta.com/blog/practical-ai-agent-security/ | A | 2026-11-19 | Regra de dois: no máximo duas entre entrada não confiável, dado sensível e mudança de estado |
| https://open-jarvis.github.io/OpenJarvis/user-guide/system-access/ | A | 2026-11-19 | Confirmação de ferramenta não aplicada; shell_exec sem allowlist (lido por resumo) |
| https://docs.ollama.com/faq | A | 2026-11-19 | KV cache `q8_0` com flash attention usa cerca de metade da memória; keep_alive |
| https://arxiv.org/abs/2409.08264 | A | 2026-11-19 | Agente só por pixels acertou 19,5% das tarefas no Windows contra 74,5% de humanos (2024) |

## Lacunas
- Não há tag para operar um sistema operacional ou automatizar o desktop (Windows, PowerShell como operador). `cli-desktop-tooling` cobre escrever scripts e apps, não operar a máquina. Sugestão: tag curada `operacao-windows` com líder `cli-desktop-tooling` e fundamentos `llm-ai-agents` e `security-appsec`.

## Promoção sugerida
- `llm-ai-agents` / seção `## Gotchas` do playbook: a armadilha do OpenJarvis (confirmação documentada como não aplicada) e a regra "instrução é pedido, permissão é garantia" aplicada a agentes locais.
- `security-appsec` / skill `agent-risk-triage`: classes de risco R0 a R3 com ensaio e reversão obrigatórios para agentes que executam comandos.
