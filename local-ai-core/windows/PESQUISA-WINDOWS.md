# Pesquisa: core de controle do ecossistema Windows

Data: 2026-11-19 · Pesquisador: Claude Opus 5.5 (Claude Code) · Consultas de busca: 78 · Páginas abertas: 17 (12 lidas na íntegra ou por extração de texto, 5 por resumo) · Fontes catalogadas: 98 (89 de classe A, 8 de classe B, 1 de classe C).

Este arquivo explica de onde veio cada regra do [CORE-WINDOWS.md](CORE-WINDOWS.md) e da [REFERENCIA-WINDOWS.md](REFERENCIA-WINDOWS.md). Segue o formato e a rubrica de fontes da casa (`docs/dev-segments/foundation/source-quality-rubric.md`): classe A (8 a 10) é base, B (5 a 7) entra com cruzamento, C (até 4) é só sinal.

## Sumário

1. Método
2. Achados principais
3. Validação da esteira proposta pelo usuário
4. Achado crítico sobre o OpenJarvis
5. Decisões de desenho do core
6. Tensões a decidir por medição
7. Limites desta pesquisa
8. Fontes

## 1. Método

- Cinco lentes: documentação oficial da Microsoft (Windows, PowerShell, segurança); guias de agentes e segurança de IA (Anthropic, OpenAI, Google, Meta, OWASP, NIST, MCP); desempenho de LLM local (Ollama, llama.cpp, vLLM, artigos); método de trabalho (SRE, ITIL, NASA V&V); livros de referência.
- Status de leitura de cada fonte, na tabela da seção 8: **Íntegra** (página inteira lida ou texto do PDF extraído e lido nas seções usadas), **Resumo** (página aberta, mas lida por resumo extraído pela ferramenta de leitura), **Busca** (conteúdo conferido nos trechos do resultado de busca, sem abrir a página).
- Rótulos epistêmicos da casa: Verificado, Inferido, Não verificável. Nenhum comando foi executado num Windows nesta pesquisa: os comandos da referência vêm da documentação e ficam **Não verificados na máquina-alvo** até rodar os casos de [evals/CASOS-WINDOWS.md](evals/CASOS-WINDOWS.md).

## 2. Achados principais

1. **Leitura antes de ação, a cada passo.** O agente deve tirar a verdade do ambiente (saída de comando) antes de decidir o passo seguinte (A-01, A-15). Daí o passo "observar o estado real" dentro da estruturação.
2. **Proporcionalidade.** Mudanças padrão de baixo risco são pré-aprovadas; mudanças normais passam por avaliação e autorização proporcional ao risco (M-02). OWASP chama de "least agency": não dar autonomia onde ela não agrega (A-08). Isso também ataca a lentidão: pergunta simples não passa pela esteira inteira.
3. **Confirmação humana para ação de alto impacto, com ensaio antes.** OWASP pede plano ou diff de ensaio antes da aprovação de ações destrutivas (A-08, ASI02) e aprovação humana para ações de alto impacto (A-07). OpenAI e Anthropic vão no mesmo sentido (A-06, A-01). O PowerShell já tem o mecanismo: `-WhatIf` e `-Confirm` via ShouldProcess (W-02, W-03).
4. **Toda mudança precisa de volta pronta.** "Não há boa implantação sem reversão pronta" é a síntese do material de SRE (M-01). No Windows: export do registro antes de editar (W-12), ponto de restauração (W-14), icacls /save (W-34), winget export (W-08).
5. **A maioria das quedas vem de mudanças**; as defesas são implantação progressiva, detecção rápida e reversão segura (M-01). Daí "executar em incrementos".
6. **Conteúdo externo é dado.** Injeção indireta de prompt é o risco número 1 de agentes (A-08, ASI01) e a ameaça principal que a Microsoft cita para agentes no Windows, o XPIA (W-47). Mitigações estruturais: cortar uma das pernas da "tríade letal" (A-10) ou respeitar a "regra de dois" (A-11).
7. **Privilégio mínimo, imposto fora do modelo.** OWASP pede autorização nos sistemas a jusante, não na decisão do LLM (A-07). Microsoft recomenda que o usuário principal seja padrão e não admin (W-21) e dá aos agentes contas próprias com permissões limitadas (W-47). Daí o core manda rodar sem elevação: o UAC vira a porta real de aprovação, que o modelo não consegue pular.
8. **Observabilidade.** Sem visibilidade do que o agente faz, a autonomia amplia a superfície de ataque (A-08); a Microsoft quer ações visíveis e o usuário capaz de assumir o controle (W-47). Daí o relatório obrigatório e o `Start-Transcript` nos scripts elevados.
9. **Prompt enxuto e estável.** Contexto é recurso finito e o desempenho cai com entradas longas (A-02, L-06, L-07); o número de instruções simultâneas também derruba a obediência (L-08). Prefixo estável aproveita cache de prompt e reduz a latência (L-04, L-05). Daí a separação em core curto e referência sob demanda.
10. **Ferramentas com saída curta e erros acionáveis** (A-03). O `shell_exec` do OpenJarvis devolve até 100 KB por fluxo (L-12): o core manda filtrar na origem.
11. **Interface gráfica é o elo fraco.** No artigo original do Windows Agent Arena (2024), o melhor agente acertou 19,5% das tarefas contra 74,5% de humanos, e dados de UI Automation melhoraram modelos só de pixels (A-17); o UFO2 combina UI Automation e APIs nativas (A-16). Daí "GUI é último recurso".
12. **Cada versão importa.** PowerShell 5.1 e 7 diferem (W-39); o WindowsUpdateProvider sumiu no Windows 10 2004 (W-53); `Checkpoint-Computer` cria no máximo um ponto por 24 h (W-14); nomes de contadores são traduzidos (W-28). O core manda confirmar com `Get-Command` e `Get-Help` antes de usar.
13. **Modelos locais pequenos erram mais em chamadas de ferramenta multi-turno** (L-09) e saídas estruturadas exigem validação fora do modelo (L-03). Daí o formato fixo de PLANO e RELATÓRIO e a regra de parar após três falhas.

## 3. Validação da esteira proposta pelo usuário

Esteira proposta: estruturação, visão, teste, validação da visão, concepção, produção, teste novamente, validação do escopo, implementação.

**Veredito: a espinha está correta e foi mantida inteira.** O estudo confirma a ideia central de separar "testar" de "validar": verificação confere se foi feito do jeito certo; validação confere se é a coisa certa (M-03). Também confirma separar plano de execução (M-04, A-01) e ter ensaio antes da implantação (A-08). O estudo corrigiu quatro pontos.

| Etapa | O que o estudo diz | Decisão |
| --- | --- | --- |
| (nova) Classificar risco | Profundidade proporcional ao risco (M-02); menor autonomia necessária (A-08); prompt e passos extras custam tempo num modelo local (A-02). Sem isso, "quanto de RAM livre?" passaria por 9 etapas. | **Acrescentada** como passo 0, com caminho rápido para leitura. |
| Estruturação | Mantida. O estudo acrescenta observar o estado real antes de qualquer proposta (A-01, A-15). | Mantida, **com observação embutida**. |
| Visão | Mantida: declarar o que muda e o resultado esperado antes de agir (A-01, M-04). | Mantida. |
| Teste da visão | Mantida: checar viabilidade com leituras (o alvo existe, exige admin, dependências). | Mantida. |
| Validação da visão | Mantida como gate humano só em R3; em R0 a R2 é autoconferência contra o critério de pronto, para não pedir duas aprovações por mudança comum (M-02). | **Ajustada por risco.** |
| Concepção | Mantida. O estudo exige que a concepção inclua reversão e comando de verificação (M-01, W-12). | Mantida, **com reversão obrigatória**. |
| Produção | Mantida. Backup preparado aqui. | Mantida. |
| Teste novamente | Mantida, concretizada como ensaio sem efeito: `-WhatIf`, `robocopy /L`, `DISM /ScanHealth`, Windows Sandbox (W-02, W-33, W-19, W-15). | Mantida. |
| Validação do escopo | Mantida: OWASP pede checar desvio do escopo original e pausar diante de mudança de objetivo (A-08, ASI01). É o gate de aprovação em R2 e R3. | Mantida. |
| Implementação | Mantida, em incrementos (M-01). | Mantida, **incremental**. |
| (nova) Verificar e registrar | A esteira terminava na implementação. O estudo pede conferir o efeito real com nova leitura (A-04, A-01), registrar e deixar o caminho de volta (A-08, W-47). | **Acrescentada** como passo 10. |

Resultado: 11 passos (0 a 10), dos quais 9 são os do usuário.

## 4. Achado crítico sobre o OpenJarvis

Lido nas páginas Configuration, Security e System Access da documentação (L-11, L-12), por resumo da ferramenta de leitura, em 2026-11-19. Confira na sua versão instalada antes de confiar.

- `enforce_tool_confirmation = true` em `[security]` é aceito pelo carregador, mas a documentação diz que **não é aplicado**.
- `shell_exec` pede confirmação só no `jarvis chat`. Em `jarvis ask`, no servidor HTTP e no app desktop, a aprovação é automática.
- `shell_exec` roda qualquer comando como o seu usuário, sem lista de permitidos, sem lista de bloqueados e sem sandbox por padrão; tempo limite padrão de 30 s; saída limitada a 100 KB por fluxo.
- `file_write` respeita `allowed_dirs`, que vazio libera todos os caminhos; `shell_exec` e `code_interpreter` ignoram `allowed_dirs`.

Consequência: **o core é um pedido ao modelo, não uma garantia.** Instrução é pedido; permissão é garantia (regra P-26 da casa, de A-01 e A-07). As garantias reais disponíveis hoje no seu PC são externas ao modelo:

1. Rodar o OpenJarvis **sem elevação**, numa conta padrão se possível. Qualquer coisa de administrador cai no UAC, que só você aprova (W-21, W-47).
2. Usar o `jarvis chat` quando quiser confirmação a cada comando.
3. Preencher `allowed_dirs` para o `file_write`.
4. Ligar a transcrição do PowerShell para auditoria (W-40).

## 5. Decisões de desenho do core

- **Duas camadas.** Core curto e estável no prompt de sistema (regras, esteira, invariantes, formatos) e referência por área na memória, buscada quando necessário (A-02, just-in-time). O OpenJarvis põe a hora atual depois do prefixo em cache (L-11); o core não leva nada dinâmico para não quebrar o cache.
- **Português do Brasil**, por convenção da casa e para o dono ler e auditar. Português gasta mais tokens que inglês na maioria dos tokenizadores; com o prefixo em cache, o custo cai para a primeira chamada (L-04). Ver tensões.
- **Quatro classes de risco** inspiradas em mudança padrão, normal e de alto risco (M-02), com a classe mais alta em caso de dúvida.
- **Duas palavras de aprovação**: "sim" para R2, "CONFIRMO <ação>" para R3. A frase exata reduz aprovação no automático, viés que a OWASP aponta em ASI09 (A-08).
- **Tom calmo, uma ênfase só nas invariantes**, conforme os princípios de prompt da casa (M-05): regras com motivo e com alternativa.
- **Três exemplos curtos** (leitura, mudança R2, injeção) em vez de lista longa de casos (A-02).
- **Pasta de trabalho fixa** (`%USERPROFILE%\IA-Operador`) para backups, scripts e logs, porque reversão e auditoria precisam de lugar conhecido.

## 6. Tensões a decidir por medição

- **Português contra inglês no core.** Se o modelo local obedecer mal, teste uma versão em inglês com a mesma estrutura nos mesmos casos de eval.
- **Tamanho do core** (cerca de 2.500 a 3.500 tokens) contra obediência: se o modelo pular regras, corte exemplos antes de cortar invariantes (L-08).
- **Confirmações contra velocidade**: medir quantas aprovações por dia o uso real pede. Se R2 incomodar, a saída é pré-aprovar tarefas padrão nomeadas (M-02), nunca abolir o gate.
- **Contexto do Ollama**: as páginas oficiais divergem sobre o padrão (4.096 no FAQ, por VRAM na página de contexto) (L-01, L-02). Agentes pedem contexto maior, que custa memória; meça com `ollama ps`.

## 7. Limites desta pesquisa

- Livros não foram lidos de capa a capa (sem acesso ao texto integral): entram como referência de aprofundamento, com o conteúdo confirmado por fontes oficiais.
- A maioria das páginas da Microsoft foi conferida por trechos de busca, não lida inteira. Os comandos centrais (ShouldProcess, CIM, eventos, serviços, registro, winget, DISM) batem em mais de uma fonte.
- A documentação do OpenJarvis foi lida por resumo; nomes de chaves e comportamento devem ser conferidos na versão instalada.
- Nada foi executado no seu PC. Os casos de eval estão `designed_not_executed`.
- O que muda rápido (Windows 11 agentic, MCP no Windows, OpenJarvis) foi lido em 2026-11-19 e envelhece.

## 8. Fontes

Status: Íntegra, Resumo ou Busca (ver seção 1).

### 8.1 Microsoft: Windows, PowerShell e segurança (W)

| ID | Fonte | Classe | Status | Usado em |
| --- | --- | --- | --- | --- |
| W-01 | [about_Execution_Policies](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_execution_policies) | A | Busca | Política de execução, não é fronteira de segurança |
| W-02 | [Everything you wanted to know about ShouldProcess](https://learn.microsoft.com/powershell/scripting/learn/deep-dives/everything-about-shouldprocess) | A | Busca | `-WhatIf`, `-Confirm`, ConfirmImpact |
| W-03 | [Requesting confirmation from cmdlets](https://learn.microsoft.com/powershell/scripting/developer/cmdlet/requesting-confirmation-from-cmdlets) | A | Busca | Confirmação nativa |
| W-04 | [Getting WMI objects with Get-CimInstance](https://learn.microsoft.com/powershell/scripting/samples/getting-wmi-objects--get-ciminstance-) | A | Busca | Inventário via CIM |
| W-05 | [Collecting information about computers](https://learn.microsoft.com/en-us/powershell/scripting/samples/collecting-information-about-computers) | A | Busca | Inventário |
| W-06 | [Get-ComputerInfo](https://learn.microsoft.com/powershell/module/microsoft.powershell.management/get-computerinfo) | A | Busca | Inventário |
| W-07 | [Use the WinGet tool](https://learn.microsoft.com/windows/package-manager/winget) | A | Busca | Programas |
| W-08 | [winget export](https://learn.microsoft.com/windows/package-manager/winget/export) | A | Busca | Backup de programas |
| W-09 | [winget import](https://learn.microsoft.com/windows/package-manager/winget/import) | A | Busca | Restauração de programas |
| W-10 | [Creating Get-WinEvent queries with FilterHashtable](https://learn.microsoft.com/powershell/scripting/samples/creating-get-winevent-queries-with-filterhashtable) | A | Busca | Eventos |
| W-11 | [ScheduledTasks module](https://learn.microsoft.com/powershell/module/scheduledtasks) | A | Busca | Tarefas agendadas |
| W-12 | [How to back up and restore the registry](https://support.microsoft.com/en-us/help/322756) | A | Busca | Export antes de editar |
| W-13 | [about_Registry_Provider](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_registry_provider) | A | Busca | Registro no PowerShell |
| W-14 | [Checkpoint-Computer](https://learn.microsoft.com/powershell/module/microsoft.powershell.management/checkpoint-computer) | A | Busca | Ponto de restauração, limite de 24 h |
| W-15 | [Windows Sandbox](https://learn.microsoft.com/windows/security/application-security/application-isolation/windows-sandbox) | A | Busca | Ensaio isolado |
| W-16 | [Windows Sandbox configuration (.wsb)](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file) | A | Busca | Sandbox sem rede |
| W-17 | [Get-MpComputerStatus (Defender)](https://learn.microsoft.com/powershell/module/defender/get-mpcomputerstatus) | A | Busca | Defender |
| W-18 | [NetSecurity module](https://learn.microsoft.com/powershell/module/netsecurity/) | A | Busca | Firewall |
| W-19 | [Repair a Windows image (DISM)](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/repair-a-windows-image) | A | Busca | Reparos |
| W-20 | [Use the System File Checker tool](https://support.microsoft.com/article/79aa86cb-ca52-166a-92a3-966e85d4094e) | A | Busca | SFC |
| W-21 | [How User Account Control works](https://learn.microsoft.com/windows/security/identity-protection/user-account-control/how-user-account-control-works) | A | Busca | UAC como porta de aprovação |
| W-22 | [Administrator protection](https://learn.microsoft.com/windows/security/application-security/application-control/administrator-protection/) | A | Busca | Privilégio mínimo no Windows 11 |
| W-23 | [Test-NetConnection (NetTCPIP)](https://learn.microsoft.com/powershell/module/nettcpip/test-netconnection) | A | Busca | Rede |
| W-24 | [Get-PhysicalDisk (Storage)](https://learn.microsoft.com/powershell/module/storage/get-physicaldisk) | A | Busca | Saúde do disco |
| W-25 | [Managing services](https://learn.microsoft.com/en-us/powershell/scripting/samples/managing-services) | A | Busca | Serviços e dependentes |
| W-26 | [Set-Service](https://learn.microsoft.com/powershell/module/microsoft.powershell.management/set-service) | A | Busca | Tipo de inicialização, exige admin |
| W-27 | [Stop-Process](https://learn.microsoft.com/powershell/module/microsoft.powershell.management/stop-process) | A | Busca | `-Force` suprime confirmação |
| W-28 | [Get-Counter](https://learn.microsoft.com/powershell/module/microsoft.powershell.diagnostics/get-counter) | A | Busca | Contadores traduzidos |
| W-29 | [Powercfg command-line options](https://learn.microsoft.com/windows-hardware/design/device-experiences/powercfg-command-line-options) | A | Busca | Energia |
| W-30 | [BitLocker operations guide](https://learn.microsoft.com/windows/security/operating-system-security/data-protection/bitlocker/operations-guide) | A | Busca | BitLocker |
| W-31 | [PSScriptAnalyzer rules](https://learn.microsoft.com/powershell/utility-modules/psscriptanalyzer/rules-recommendations) | A | Busca | Qualidade de scripts |
| W-32 | [about_Error_Handling](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_error_handling) | A | Busca | `-ErrorAction Stop` e try/catch |
| W-33 | [robocopy](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy) | A | Busca | `/L` como ensaio |
| W-34 | [icacls](https://learn.microsoft.com/windows-server/administration/windows-commands/icacls) | A | Busca | Backup de ACL |
| W-35 | [Smart App Control](https://learn.microsoft.com/windows/apps/develop/smart-app-control/overview) | A | Busca | Ação sem volta |
| W-36 | [about_Language_Modes](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_language_modes) | A | Busca | Modo restrito |
| W-37 | [PnPUtil command syntax](https://learn.microsoft.com/windows-hardware/drivers/devtest/pnputil-command-syntax) | A | Busca | Drivers |
| W-38 | [WSL: working across file systems](https://learn.microsoft.com/windows/wsl/filesystems) | A | Busca | WSL |
| W-39 | [Differences between Windows PowerShell 5.1 and PowerShell 7](https://learn.microsoft.com/powershell/scripting/whats-new/differences-from-windows-powershell) | A | Busca | Versões |
| W-40 | [about_Logging_Windows](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_logging_windows) | A | Busca | Auditoria |
| W-41 | [Just Enough Administration](https://learn.microsoft.com/powershell/scripting/learn/remoting/jea/overview) | A | Busca | Negar por padrão, sem curingas |
| W-42 | [about_Environment_Variables](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_environment_variables) | A | Busca | PATH e escopos |
| W-43 | [Security Compliance Toolkit](https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/windows-security-configuration-framework/security-compliance-toolkit-10) | A | Busca | Linhas de base de segurança |
| W-44 | [Manage drive space with Storage Sense](https://support.microsoft.com/en-us/help/5000679) | A | Busca | Espaço em disco |
| W-45 | [Sysinternals utilities](https://learn.microsoft.com/en-us/sysinternals/downloads/) | A | Busca | Diagnóstico avançado |
| W-46 | [UI Automation control patterns](https://learn.microsoft.com/en-us/windows/win32/WinAuto/uiauto-controlpatternsoverview) | A | Busca | GUI |
| W-47 | [Securing AI agents on Windows (blog, 2025-10-16)](https://blogs.windows.com/windowsexperience/2025/10/16/securing-ai-agents-on-windows/) | A | Íntegra | Contas de agente, privilégio limitado, XPIA |
| W-48 | [Agentic security (Windows security book)](https://learn.microsoft.com/en-us/windows/security/book/operating-system-agentic-security) e páginas de agent governance e agent identity | A | Íntegra | Contenção, governança, identidade |
| W-49 | [Experimental agentic features](https://support.microsoft.com/en-us/windows/ai/ai-features/experimental-agentic-features) | A | Busca | Desligado por padrão, opt-in |
| W-50 | [MCP on Windows](https://learn.microsoft.com/windows/ai/mcp/) | A | Busca | Registro de conectores, contenção |
| W-51 | [Securing the Model Context Protocol on Windows](https://blogs.windows.com/windowsexperience/2025/05/19/securing-the-model-context-protocol-building-a-safer-agentic-future-on-windows/) | A | Busca | Assinatura e proxy de MCP |
| W-52 | [Define least privilege administration](https://learn.microsoft.com/training/modules/perform-windows-server-secure-administration/2-define-least-privilege-administration) | A | Busca | Privilégio mínimo |
| W-53 | [Q&A: Start-WUScan not available](https://learn.microsoft.com/en-us/answers/questions/212035/start-wuscan-cmdlet-is-not-avialble-to-run-on-few) | B | Busca | Módulo de update removido |

### 8.2 Agentes e segurança de IA (A)

| ID | Fonte | Classe | Status | Usado em |
| --- | --- | --- | --- | --- |
| A-01 | [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | A | Íntegra | Simplicidade, verdade do ambiente, paradas, sandbox |
| A-02 | [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | A | Íntegra | Core enxuto, just-in-time, exemplos canônicos |
| A-03 | [Anthropic: Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | A | Íntegra | Saída curta, erros acionáveis |
| A-04 | [Claude Code best practices](https://code.claude.com/docs/en/best-practices) | A | Busca | Explorar, planejar, executar, verificar com evidência |
| A-05 | [Anthropic: Computer use](https://docs.anthropic.com/en/docs/agents-and-tools/computer-use) | A | Busca | Isolar de dados sensíveis, risco de injeção |
| A-06 | [OpenAI: A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) | A | Busca | Guardrails em camadas, limites de falha, humano em ações de alto risco |
| A-07 | [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) | A | Busca | Menos funções, menos permissão, aprovação humana, autorização fora do LLM |
| A-08 | [OWASP Top 10 for Agentic Applications 2026 (dez. 2025)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | A | Íntegra (PDF extraído) | Least agency, ASI01 a ASI10, ensaio antes de aprovar |
| A-09 | [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices) | A | Busca | Consentimento, confused deputy |
| A-10 | [Simon Willison: The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) | B | Busca | Dados privados, conteúdo não confiável, comunicação externa |
| A-11 | [Meta: Agents Rule of Two](https://ai.meta.com/blog/practical-ai-agent-security/) | A | Busca | No máximo duas das três propriedades por sessão |
| A-12 | [Google's approach for secure AI agents](https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/) | A | Busca | Controlador humano, poderes limitados, ações observáveis |
| A-13 | [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | A | Busca | Configuração humano-IA, viés de automação |
| A-14 | [Spotlighting (Microsoft Research)](https://arxiv.org/abs/2403.14720) | A | Busca | Separar instrução de conteúdo |
| A-15 | [ReAct (Yao et al., ICLR 2023)](https://arxiv.org/abs/2210.03629) | A | Busca | Raciocinar e agir intercalados |
| A-16 | [UFO2: The Desktop AgentOS](https://arxiv.org/abs/2504.14603) | A | Busca | UIA mais APIs nativas no Windows |
| A-17 | [Windows Agent Arena](https://arxiv.org/abs/2409.08264) | A | Busca | 19,5% contra 74,5% humano |
| A-18 | [Claude Help: using Cowork safely](https://support.claude.com/en/articles/13364135) | B | Busca | Duas condições para injeção ter sucesso |
| A-19 | [HiddenLayer: injeção em computer use](https://hiddenlayer.com/research/the-lethal-trifecta-and-how-to-defend-against-it) | C | Busca | Demonstração de comando destrutivo via arquivo |

### 8.3 Método de trabalho (M)

| ID | Fonte | Classe | Status | Usado em |
| --- | --- | --- | --- | --- |
| M-01 | [Google SRE: lessons learned](https://sre.google/resources/practices-and-processes/twenty-years-of-sre-lessons-learned/) e [Building reliable releases and rollbacks](https://cloud.google.com/blog/products/gcp/reliable-releases-and-rollbacks-cre-life-lessons/) | A | Busca | Mudanças causam quedas, implantação progressiva, reversão pronta |
| M-02 | [ITIL 4 change enablement (AWS)](https://docs.aws.amazon.com/wellarchitected/latest/change-enablement-in-the-cloud/change-enablement-in-itil4.html) | B | Busca | Mudança padrão, normal, emergencial; aprovação por risco |
| M-03 | [NASA SWEHB e SE Handbook: verificação e validação](https://www.nasa.gov/seh/5-realization) | A | Busca | Testar contra validar |
| M-04 | [Microsoft Learn: separate planning, reasoning, and execution](https://learn.microsoft.com/en-gb/training/modules/design-agent-architecture-integration/4-plan-reason-execution) | A | Busca | Separar plano de execução |
| M-05 | Princípios de prompt da casa (`docs/dev-segments/foundation/prompt-principles.md`) | A | Íntegra | Tom, motivo por regra, formatos |

### 8.4 LLM local e OpenJarvis (L)

| ID | Fonte | Classe | Status | Usado em |
| --- | --- | --- | --- | --- |
| L-01 | [Ollama: context length](https://docs.ollama.com/context-length) | A | Íntegra | Contexto, VRAM, `ollama ps` |
| L-02 | [Ollama FAQ](https://docs.ollama.com/faq) | A | Íntegra | keep_alive, KV cache q8_0, flash attention, Windows |
| L-03 | [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs) | A | Busca | Validar saída fora do modelo |
| L-04 | [llama.cpp: KV cache reuse](https://github.com/ggml-org/llama.cpp/discussions/13606) | B | Busca | Reaproveitar prefixo do system prompt |
| L-05 | [vLLM: automatic prefix caching](https://docs.vllm.ai/en/v0.30.0/features/automatic_prefix_caching/) | A | Busca | Prefixo idêntico reduz latência |
| L-06 | [Lost in the Middle (TACL 2024)](https://arxiv.org/abs/2307.03172) | A | Busca | Posição da informação no contexto |
| L-07 | [Chroma: Context Rot](https://research.trychroma.com/context-rot) | B | Busca | Desempenho cai com entrada longa |
| L-08 | [IFScale: How many instructions can LLMs follow at once?](https://arxiv.org/abs/2507.11538) | A | Busca | Densidade de instruções |
| L-09 | [Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard) | A | Busca | Modelos pequenos em multi-turno |
| L-10 | [Qwen: function calling](https://qwen.readthedocs.io/en/latest/framework/function_call.html) | A | Busca | Formato de ferramenta em modelos locais |
| L-11 | [OpenJarvis: configuration](https://open-jarvis.github.io/OpenJarvis/getting-started/configuration) | A | Resumo | `system_prompt_path`, `[agent]`, memória |
| L-12 | [OpenJarvis: system access](https://open-jarvis.github.io/OpenJarvis/user-guide/system-access/) e [security](https://open-jarvis.github.io/OpenJarvis/user-guide/security/) | A | Resumo | Confirmação não aplicada, shell_exec sem allowlist |
| L-13 | [Ollama blog: OpenJarvis](https://ollama.com/blog/openjarvis) | A | Íntegra | Instalação no Windows, presets |
| L-14 | [OpenJarvis: Personal AI, On Personal Devices](https://huggingface.co/papers/2605.17172) | B | Busca | Contexto do projeto |

### 8.5 Livros (B)

| ID | Livro | Classe | Status | Usado em |
| --- | --- | --- | --- | --- |
| B-01 | Yosifovich, Ionescu, Russinovich, Solomon. *Windows Internals, 7th ed., Part 1*. Microsoft Press, 2017. [página oficial](https://learn.microsoft.com/en-us/sysinternals/resources/windows-internals) | A | Busca | Processos, memória, segurança |
| B-02 | Allievi, Russinovich, Ionescu, Solomon. *Windows Internals, 7th ed., Part 2*. Microsoft Press. | A | Busca | Serviços, registro, boot |
| B-03 | Russinovich, Margosis. *Troubleshooting with the Windows Sysinternals Tools*. [página oficial](https://learn.microsoft.com/en-us/sysinternals/resources/troubleshooting-book) | A | Busca | Diagnóstico |
| B-04 | Plunk, Petty, Leonhardt. *Learn PowerShell in a Month of Lunches, 4th ed.* Manning, 2022. [Manning](https://www.manning.com/books/learn-powershell-in-a-month-of-lunches) | A | Busca | Fundamentos de PowerShell |
| B-05 | Huyen. *AI Engineering*. O'Reilly, 2025. [O'Reilly](https://www.oreilly.com/library/view/ai-engineering/9781098166298/) e [capítulo de agentes](https://huyenchip.com/2025/01/07/agents) | A | Busca | Planejamento e modos de falha de agentes |
| B-06 | Gulli. *Agentic Design Patterns*. Springer. [Springer](https://link.springer.com/doi/10.1007/978-3-032-01402-3) | B | Busca | Reflexão, planejamento, humano no circuito, guardrails |
| B-07 | Beyer et al. *Site Reliability Engineering*. O'Reilly, 2016. [sre.google](https://sre.google/sre-book/service-best-practices/) | A | Busca | Gestão de mudanças |

Contagem: 53 (W) + 19 (A) + 5 (M) + 14 (L) + 7 (B) = 98 fontes.
