# Referência do modo SO

Detalhe do servidor `servidor_so.py`, buscado sob demanda com `regras_consultar` (tema `so`). Instalação em [INSTALAR-SO.md](INSTALAR-SO.md); fontes em [PESQUISA-SO.md](PESQUISA-SO.md). Versão 1.0, 2026-11-19.

## 1. A esteira dentro das ferramentas

| Passo da esteira | Onde acontece |
| --- | --- |
| 0 Classificar | `so_planejar`: a regra de risco da ação, em código |
| 1 Estruturar e observar | `so_planejar` lê o estado atual antes de tudo; `so_estado` e `so_consultar` para o resto |
| 2 a 4 Visão, testar, validar | O modelo escolhe a ação; ação inexistente, parâmetro inválido ou estado impossível voltam como NÃO PLANEJADO |
| 5 Conceber | O roteiro fixo da ação: aplicar, verificar, desfazer |
| 6 Produzir | Backup preparado (registro exportado, tarefa exportada, cópia do arquivo, PATH anotado) |
| 7 Testar de novo | Ensaio: `-WhatIf` quando o cmdlet aceita, ou descrição exata do que muda |
| 8 Validar o escopo | `so_executar` relê o estado; se mudou, cancela. R2 e R3 pedem aprovação na janela do Windows |
| 9 Implementar | Aplica uma ação por plano; administrador só pelo UAC |
| 10 Verificar e registrar | Relê o efeito, devolve o RELATÓRIO, grava o plano e uma linha no JSONL |

## 2. Ações e risco

| Ação | Risco | Regra |
| --- | --- | --- |
| `app_abrir` | R1 | Só apps do Menu Iniciar (`Get-StartApps`), pelo nome |
| `arquivo_abrir` | R1 ou BLOQUEADO | Documentos, mídia e pastas abrem; executável e script ficam bloqueados |
| `arquivo_escrever` | R1, R2 ou BLOQUEADO | Arquivo novo em pasta permitida: R1. Substituir, fora das pastas permitidas, pasta de inicialização, `.ssh` ou conteúdo com segredo: R2. Pasta do sistema ou binário: BLOQUEADO |
| `arquivo_mover` | R1, R2 ou BLOQUEADO | Dentro das pastas permitidas: R1; fora: R2; sistema: BLOQUEADO |
| `arquivo_para_lixeira` | R2 ou R3 | Lixeira em disco local: R2. Disco removível ou de rede, mais de 1000 arquivos ou mais de 1 GB: R3. Apagar de vez não existe |
| `pasta_criar` | R1 ou R2 | Como `arquivo_escrever` |
| `processo_encerrar` | R1, R2, R3 ou BLOQUEADO | Fechar normalmente: R1. Forçar: R2. Processo da pasta do Windows: R3. Processo essencial (lsass, csrss, svchost...): BLOQUEADO |
| `servico_configurar_inicio` | R2, R3 ou BLOQUEADO | R2. Proteção, rede ou atualização (WinDefend, mpssvc, wuauserv...) fora de Automatic: R3. Essencial (RpcSs, EventLog...): BLOQUEADO |
| `servico_reiniciar` | R2 ou BLOQUEADO | Essencial: BLOQUEADO |
| `programa_instalar`, `programa_atualizar` | R2 | Só winget, fonte `winget`, ID exato conferido com `winget show`. A janela avisa que aprovar aceita a licença do pacote |
| `programa_remover` | R2 ou R3 | Programa de segurança: R3 |
| `tarefa_criar` | R2 ou R3 | Só script `.ps1` em `IA-Operador\scripts\`, na pasta `\IA-Operador\` do Agendador, 30 min no máximo, sem instância sobreposta, só com o usuário logado e sem elevação. Script com segredo: R3 |
| `tarefa_ativar` | R2 ou R3 | Desativar tarefa de proteção ou atualização: R3 |
| `registro_definir` | R1, R2 ou R3 | HKCU: R1. Chave Run ou HKLM: R2. Defender, UAC, LSA, Winlogon, serviços, política de execução, SmartScreen: R3 |
| `path_usuario_adicionar` | R1 | Acrescenta sem duplicar e mantém o tipo REG_EXPAND_SZ |
| `energia_plano` | R2 | Planos padrão ou GUID listado em `so_estado area=energia` |
| `temporarios_limpar` | R2 | Só `%TEMP%` do usuário; sem desfazer |
| `firewall_regra` | R2 ou R3 | Bloquear: R2. Permitir: R3 |

Ações internas, usadas só por `so_desfazer`: `_tarefa_remover`, `_registro_remover_valor`, `_pasta_remover_vazia`, `_arquivo_remover_criado`, `_arquivo_restaurar`, `_path_usuario_definir`, `_firewall_remover_regra`.

## 3. Respostas das ferramentas e o que o modelo faz

| Começo da resposta | Significado | O que fazer |
| --- | --- | --- |
| `PLANO <id> [R1]` | Pronto para executar | Chamar `so_executar` |
| `PLANO <id> [R2]` | Vai abrir a janela Sim/Não | Dizer em uma frase o que vai acontecer e chamar `so_executar` |
| `PLANO <id> [R3]` | Vai pedir CONFIRMO | Explicar o risco, perguntar no chat e só então chamar `so_executar` |
| `BLOQUEADO` | O servidor não faz | Explicar; não procurar outro caminho |
| `NÃO PLANEJADO` | Parâmetro, estado ou ensaio impede | Corrigir a causa (ex.: achar o ID certo) ou perguntar |
| `NÃO EXECUTADO` | Recusa na janela, no UAC, ou backup falhou | Não repetir; perguntar o que o usuário prefere |
| `A REALIDADE MUDOU` | O estado mudou desde o plano | Planejar de novo |
| `PARADA GERAL ATIVA` | Existe o arquivo PARAR | Avisar; só o usuário apaga |
| `FEITO / EVIDÊNCIA / STATUS` | Relatório | Mostrar sem acrescentar nada |

## 4. Consulta livre (so_consultar)

Passa: cmdlets e funções com verbo de leitura (Get, Test, Measure, Select, Where, Sort, Format, Group, ForEach, Compare, Resolve, ConvertTo, ConvertFrom, Join, Split) e `Out-String`; aliases de leitura (`gps`, `gci`, `?`, `%`...); `ipconfig /all`, `whoami`, `systeminfo`, `tasklist`, `netstat`, `nslookup`, `ping`, `tracert`, `winget search|list|show`, `powercfg /list|/getactivescheme|/query`; `[math]`, `[datetime]`, `[timespan]` e partes de `[string]` e `[environment]`; métodos de texto e data (`ToUpper`, `Contains`, `AddDays`...).

Não passa: qualquer outro verbo (Set, Remove, Stop, Start, Invoke, New...), redirecionamento, `&`, `.` (dot-source), acento grave, here-string, `$( )` dentro de aspas duplas, métodos que mudam algo (`.Kill()`, `.Delete()`...), `ForEach-Object <método>`, outra máquina (`-ComputerName`, `-CimSession`, `-Credential`), `Get-Credential`, `Get-Clipboard`, caminho de programa ou script.

Três cercas: a checagem em Python; a árvore sintática do próprio PowerShell (`Parser.ParseInput`), que resolve aliases e confere verbo, programa e método; e a execução em ConstrainedLanguage. A documentação da Microsoft diz que mudar o modo de linguagem pelo `$ExecutionContext` é útil para experimentar. Aqui ele é camada extra, não a fronteira principal: a fronteira é a lista de permitidos e a conta sem elevação.

## 5. Memória

- Tipos: `perfil` (só origem usuario), `decisao`, `procedimento` (origem usuario ou ia) e `episodio` (qualquer origem).
- Texto de ferramenta não vira regra. Texto de origem ia ou ferramenta que parece instrução para a IA vai para `memoria\quarentena\`.
- Segredo não entra; o texto é recusado.
- Mesmo título no mesmo tipo: a nota antiga vai para `memoria\arquivo\` e a nova ganha `substitui:`. Nada se apaga.
- Se `memoria\` for um repositório git, cada gravação vira um commit.
- Backend ai-memory: `memory_write_page` (caminho `ia-operador/<pasta>/<slug>.md`, tier semantic, procedural ou episodic), `memory_query`, `memory_handoff_begin`, `memory_briefing` e `memory_handoff_list`. Só endereço local e sem proxy; se falhar, usa a memória local e avisa.

## 6. Decisões de projeto

- **Lixeira é R2**, não R3. O CORE-WINDOWS põe "apagar dados do usuário" em R3. Mandar para a Lixeira em disco local dá para desfazer, por isso fica em R2; disco sem Lixeira, volume grande ou item que pode não caber nela sobe para R3. Apagar de vez não existe no catálogo.
- **PATH do usuário pelo registro.** `[Environment]::SetEnvironmentVariable` no .NET Framework grava com `SetValue(nome, valor)`, e string vira REG_SZ. A leitura pela mesma API devolve o valor já expandido. Juntas, trocam `%USERPROFILE%\...` por caminhos fixos e mudam o tipo de REG_EXPAND_SZ para REG_SZ. O servidor lê com `DoNotExpandEnvironmentNames`, grava como `ExpandString` e usa a API do .NET só para avisar os programas (WM_SETTINGCHANGE).
- **winget sem aceitar termos da fonte.** O servidor usa `--source winget` e não passa `--accept-source-agreements`. A licença do pacote (`--accept-package-agreements`) só é aceita quando você aprova na janela, que avisa disso.
- **Parâmetro nunca vira código.** Os valores vão por variável de ambiente (`SO_P_<NOME>`) e o script lê com `(P 'NOME')`. O script vai por `-EncodedCommand`, sem arquivo `.ps1`.
- **Saída só ASCII.** O OpenJarvis abre o pipe em modo texto com a codificação local; acentos viajam como `\uXXXX`.
- **Anotações MCP são só dica.** O OpenJarvis descarta `readOnlyHint` e afins ao montar as ferramentas, então a política inteira fica no servidor.

## 7. Como acrescentar uma ação

1. Em `so_mcp/acoes.py`, crie um `Acao` com: parâmetros tipados (com regex quando for nome), `observar` que devolve JSON, `avaliar` com a regra de risco, `resumo`, `ensaiar`, `backup` se muda algo que não volta sozinho, `aplicar`, `verificar` que devolve `{ok, detalhe}`, e `desfazer`.
2. Acrescente em `TODAS`.
3. Rode `python -m unittest discover -s tests`: o teste confere que os scripts só leem parâmetros declarados e que o desfazer aponta para uma ação existente.
4. Rode `--autoteste` no Windows e um caso de conversa em `evals/CASOS-SO.md`.

## 8. Guia agent-practice no servidor (desde 2026-11-20)

O servidor aplica em código regras do guia obrigatório do brain-of-agent (`plugins/agent-practice`, destilado do livro *Competente o Suficiente*):

| Regra | Onde | O que faz |
| --- | --- | --- |
| G4, lista de proteção (SEG-19, SEG-P03) | `politica.protegido` em `arquivo_para_lixeira`, `arquivo_mover` e `arquivo_escrever` | BLOQUEADO para apagar ou mover `backups`, `logs`, `planos`, `memoria` e `PARAR` da IA-Operador, o brain-of-agent, a pasta do usuário ou uma pasta pessoal inteira, e as `pastas_protegidas` da configuração; escrever dentro da trilha de auditoria também |
| Oráculo na fonte (VER-04, SEG-20) | verificação de `arquivo_para_lixeira` | Confere na própria Lixeira que o item está lá e com o mesmo tamanho; fora da Lixeira = Falhou; Lixeira ilegível = Parcial |
| Ponto de retorno (SEG-24) | `so_executar` em todo R3 e a ação `ponto_restauracao_criar` (R1, administrador) | Tenta um ponto de restauração antes do R3, sem travar se o Windows recusar (um a cada 24 h); `ponto_antes_r3: false` desliga |
| Conformidade e voz (G6, VER-09) | RELATÓRIO de `so_executar` | Linhas `CONFORMIDADE (guia)` (plano relido, aprovação, ponto de retorno, verificação, falhas seguidas) e `VOZ` (uma frase que nunca diz feito sem Verificado) |

Testes: `tests/test_so_mcp.py`, classe `TestGuia`.

### Comandos do dia a dia (voz), desde 2026-11-20

| Ação | Risco | Como confere | Desfazer |
| --- | --- | --- | --- |
| `tela_bloquear` | R1 | tela de bloqueio (LogonUI) aberta; se não vir, Parcial | entrar com a senha |
| `desligamento_agendar` | R2 (R3 com menos de 5 min) | Parcial por desenho: o Windows não deixa ler um agendamento pendente sem cancelar | `desligamento_cancelar` |
| `desligamento_cancelar` | R1 | resposta do próprio Windows (`shutdown /a`); ele grava o evento 1075 | agendar de novo |
| `tema_definir` | R1 | relê o registro do tema | volta ao tema anterior |
| `wifi_definir` | R2, administrador | estado do adaptador | o estado oposto |
| `notificacoes_definir` | R1 | relê `ToastEnabled` | volta ao anterior |
| `captura_tela` | R1 | o PNG existe e não está vazio | mandar para a Lixeira |

Provado no PC em 20/11/2026: tema, notificações, agendar e cancelar, print e o print conferido na Lixeira. Wi-Fi e bloquear tela só por teste (desligar o Wi-Fi cortaria a sessão que testava; bloquear trancaria a tela do dono).
