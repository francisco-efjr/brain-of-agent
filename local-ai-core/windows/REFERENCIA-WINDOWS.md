# REFERENCIA-WINDOWS: base sob demanda do operador Windows

Complemento do CORE-WINDOWS.md. Não vai no prompt de sistema: é indexada na memória da IA e consultada por área quando a tarefa é R1, R2 ou R3. Cada seção fica de pé sozinha para caber num trecho de busca. Versão 1.0, 2026-11-19. Fontes por ID (W-, A-, L-) em PESQUISA-WINDOWS.md.

Convenções desta base: `$W = "$env:USERPROFILE\IA-Operador"` é a pasta de trabalho; `$ts = Get-Date -Format yyyyMMdd-HHmmss` dá o carimbo de data. Cada chamada de shell começa do zero: defina `$W` e `$ts` no início de cada comando que os usa. Pastas do usuário podem estar no OneDrive: use `[Environment]::GetFolderPath('Desktop')`, `('MyDocuments')` e afins em vez de montar o caminho. Risco entre colchetes: [R0] leitura, [R1] pequena e reversível, [R2] sistema ou admin, [R3] destrutiva ou reduz segurança.

## 1. Preparação e autodiagnóstico (pasta de trabalho, admin, versão, GPU, Ollama)

- [R1] Criar a pasta de trabalho: `New-Item -ItemType Directory -Force -Path "$W\backups","$W\logs","$W\scripts" | Out-Null`
- [R0] Versão do PowerShell: `$PSVersionTable.PSVersion`. 5.1 é `powershell.exe`; 7 é `pwsh.exe`. Os dois convivem. (W-39)
- [R0] Estou elevado? `([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)`
- [R0] Uso da GPU (NVIDIA): `nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv`
- [R0] Modelo carregado e divisão GPU/CPU: `ollama ps`. Coluna PROCESSOR abaixo de 100% GPU indica descarga para CPU, que deixa a IA lenta. (L-01)
- Armadilha: `Win32_VideoController.AdapterRAM` trava em cerca de 4 GB; para VRAM real use nvidia-smi.

## 2. Executar como administrador com registro (UAC, elevação, script elevado)

Padrão para um passo aprovado que exige admin. O UAC é a porta: o usuário decide no próprio Windows. (W-21, W-22)

```powershell
$script = "$W\scripts\passo-$ts.ps1"
$log    = "$W\logs\passo-$ts.log"
Set-Content -Path $script -Encoding UTF8 -Value @"
Start-Transcript -Path '$log'
try {
    # comandos aprovados aqui, com -ErrorAction Stop
} catch { Write-Output "ERRO: `$(`$_.Exception.Message)" }
Stop-Transcript
"@
try {
    Start-Process powershell.exe -Verb RunAs -Wait -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$script`""
} catch { "UAC recusado ou falha ao elevar: $($_.Exception.Message)" }
Get-Content $log -Tail 40
```

- `-ExecutionPolicy Bypass` vale só para esse processo e só para script que você escreveu e mostrou. A política de execução não é fronteira de segurança, e mudá-la em LocalMachine ou CurrentUser é R3. (W-01)
- Saída de processo elevado não volta para você: leia sempre o log.
- Acentos: se você roda no PowerShell 7, grave o script com `-Encoding utf8BOM`. O `powershell.exe` 5.1 lê UTF-8 sem BOM como ANSI e estraga caminhos como "Área de Trabalho".

## 3. Inventário da máquina (sistema, hardware, disco, memória, uptime)

- [R0] Sistema: `Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, OSArchitecture, LastBootUpTime, FreePhysicalMemory, TotalVisibleMemorySize` (memória em KB). (W-04, W-05)
- [R0] Hardware: `Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer, Model, TotalPhysicalMemory` e `Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors`
- [R0] Discos com espaço: `Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | Select-Object DeviceID, @{n='LivreGB';e={[math]::Round($_.FreeSpace/1GB,1)}}, @{n='TotalGB';e={[math]::Round($_.Size/1GB,1)}}`
- [R0] Visão geral: `Get-ComputerInfo -Property OsName, OsVersion, OsBuildNumber, CsTotalPhysicalMemory` (lento, vários segundos; peça só as propriedades necessárias). (W-06)
- Armadilha: `Get-WmiObject` não existe no PowerShell 7. Use `Get-CimInstance`.

## 4. Processos e desempenho (CPU, memória, travamento, contadores)

- [R0] Top CPU: `Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name, Id, CPU, @{n='MemMB';e={[math]::Round($_.WorkingSet64/1MB)}}`
- [R0] Top memória: troque `CPU` por `WorkingSet64` no Sort-Object.
- [R0] Contador de CPU: `Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 3`. (W-28)
- [R1] Fechar app do usuário: `Stop-Process -Name <nome> -WhatIf` e depois sem -WhatIf. Avise que trabalho não salvo se perde.
- [R3] Encerrar processo do sistema ou usar `-Force`: só com CONFIRMO. `-Force` suprime a confirmação nativa; alguns processos não podem ser encerrados. (W-27)
- Armadilha: nomes de contadores são traduzidos. Num Windows em português o caminho pode ser `\Processador(_Total)\% Tempo de Processador`. Liste com `Get-Counter -ListSet *processador*` ou `*processor*`.

## 5. Serviços (Get-Service, Set-Service, tipo de inicialização, dependências)

- [R0] Estado: `Get-CimInstance Win32_Service -Filter "Name='<nome>'" | Select-Object Name, DisplayName, State, StartMode, PathName`
- [R0] Quem depende dele: `Get-Service -Name <nome> -DependentServices`
- [R2] Backup: anote State e StartMode no log antes de mudar.
- [R2] Mudar inicialização: `Set-Service -Name <nome> -StartupType Disabled -WhatIf` (valores: Automatic, Manual, Disabled; AutomaticDelayedStart só no PowerShell 7). Exige admin. (W-25, W-26)
- [R2] Parar: `Stop-Service -Name <nome> -WhatIf`. Com dependentes, exige `-Force` e para os dependentes também: liste-os no PLANO.
- Desfazer: `Set-Service -Name <nome> -StartupType <original>` e `Start-Service -Name <nome>`.
- Armadilha: StartMode do Win32_Service vem como Auto, Manual ou Disabled; o Set-Service usa Automatic.

## 6. Inicialização com o Windows (programas que abrem sozinhos, Run, startup)

- [R0] Lista: `Get-CimInstance Win32_StartupCommand | Select-Object Name, Command, Location, User`
- [R0] Chaves Run: `Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'` e o mesmo caminho em `HKLM:`.
- [R1] Caminho preferido para desligar um item: abrir `Start-Process ms-settings:startupapps` e deixar o usuário alternar, porque é reversível pela mesma tela.
- [R2] Remover de uma chave Run: `reg export` da chave antes, depois `Remove-ItemProperty -Path <chave> -Name <valor> -WhatIf`.
- Tarefas agendadas no logon também iniciam programas: veja a seção 7. Para auditoria completa, Autoruns (seção 22).

## 7. Tarefas agendadas (Task Scheduler, ScheduledTasks)

- [R0] Ativas: `Get-ScheduledTask | Where-Object State -ne 'Disabled' | Select-Object TaskPath, TaskName, State`
- [R0] Última execução: `Get-ScheduledTaskInfo -TaskName <nome> -TaskPath '<pasta>'`
- [R2] Backup: `Export-ScheduledTask -TaskName <nome> -TaskPath '<pasta>' | Out-File "$W\backups\tarefa-<nome>-$ts.xml" -Encoding utf8`
- [R2] Desativar: `Disable-ScheduledTask -TaskName <nome> -TaskPath '<pasta>' -WhatIf`. Desfazer: `Enable-ScheduledTask`.
- [R2] Criar: monte com `New-ScheduledTaskAction`, `New-ScheduledTaskTrigger` e `New-ScheduledTask`, registre com `Register-ScheduledTask`. Restaurar de backup: `Register-ScheduledTask -TaskName <nome> -TaskPath '<pasta>' -Xml (Get-Content '<arquivo>' -Raw)`. (W-11)
- Armadilha: tarefas em `\Microsoft\Windows\` são do sistema; mexer nelas é R3.

## 8. Registro do Windows (HKCU, HKLM, reg export, reg import)

- [R0] Ler: `Get-ItemProperty -Path 'HKCU:\Software\<caminho>'` (W-13)
- [R1 em HKCU, R2 em HKLM] Backup obrigatório: `reg export "HKCU\Software\<caminho>" "$W\backups\reg-$ts.reg" /y` (W-12)
- Mudar: `Set-ItemProperty -Path 'HKCU:\Software\<caminho>' -Name <valor> -Value <dado> -WhatIf`, depois sem -WhatIf.
- Desfazer: `reg import "<arquivo>.reg"`. Se você criou um valor novo, desfazer é `Remove-ItemProperty`, porque o import não apaga o que foi criado depois do export.
- Armadilha: no provider do PowerShell o caminho leva dois-pontos (`HKLM:\...`); no reg.exe não (`HKLM\...`).
- Mudanças amplas em HKLM: ponto de restauração antes (seção 17).

## 9. Arquivos e pastas (tamanho, limpeza, mover, copiar, Lixeira, robocopy)

- [R0] Maiores pastas de um nível: `Get-ChildItem '<pasta>' -Directory | ForEach-Object { [pscustomobject]@{Pasta=$_.Name; GB=[math]::Round((Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum/1GB,2)} } | Sort-Object GB -Descending | Select-Object -First 10`. Em árvores grandes passa de 30 s: rode em segundo plano.
- [R2] Temporários do usuário com mais de 7 dias: `$alvo = Get-ChildItem $env:TEMP -Recurse -File -ErrorAction SilentlyContinue | Where-Object LastWriteTime -lt (Get-Date).AddDays(-7)`; mostre contagem e tamanho; ensaio com `$alvo | Remove-Item -WhatIf`.
- [R3] Apagar dados do usuário: prefira a Lixeira: `Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile('<arquivo>','OnlyErrorDialogs','SendToRecycleBin')` (para pasta, `DeleteDirectory`). Confira no primeiro uso que o item foi para a Lixeira.
- [R3] Esvaziar a Lixeira: `Clear-RecycleBin -WhatIf`. Não tem volta.
- Copiar ou espelhar: `robocopy "<origem>" "<destino>" /E /L` (ensaio) antes do real. `/MIR` apaga no destino o que não existe na origem: R3, sempre com `/L` antes, nunca apontando para a raiz de um disco. Sucesso é `$LASTEXITCODE` de 0 a 7. (W-33)

## 10. Permissões NTFS (ACL, icacls, Get-Acl, dono)

- [R0] Ler: `Get-Acl '<caminho>' | Format-List` ou `icacls '<caminho>'`
- [R2] Backup: `icacls "<pasta>" /save "$W\backups\acl-$ts.txt" /t /c` (salva só DACLs; dono e SACL não). (W-34)
- Desfazer: `icacls "<pasta-pai>" /restore "<arquivo>"`. O restore usa o pai da pasta salva; não edite nem reconverta a codificação do arquivo.
- [R3] Tomar posse (`takeown`) ou mudar permissões de pastas do sistema.

## 11. Rede (adaptadores, IP, DNS, conectividade, portas)

- [R0] Adaptadores: `Get-NetAdapter | Select-Object Name, Status, LinkSpeed, MacAddress`
- [R0] Configuração IP: `Get-NetIPConfiguration`
- [R0] Conectividade: `Test-NetConnection 1.1.1.1` e porta: `Test-NetConnection <host> -Port 443`. (W-23)
- [R0] DNS: `Resolve-DnsName <host>`. IP responde e nome não: problema de DNS.
- [R1] Limpar cache DNS: `Clear-DnsClientCache`
- [R2] Mudar DNS ou IP: backup com `Get-DnsClientServerAddress` e `Get-NetIPAddress` no log; desfazer reaplicando os valores.
- [R3] `netsh winsock reset` ou `netsh int ip reset`: exigem reiniciar e mexem em toda a pilha.

## 12. Firewall do Windows (NetSecurity, regras, perfis)

- [R0] Perfis: `Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction` (W-18)
- [R0] Regras de entrada ativas: `Get-NetFirewallRule -Direction Inbound -Enabled True | Select-Object -First 30 DisplayName, Action, Profile`
- [R0] Regras de um programa: `Get-NetFirewallApplicationFilter -Program '<exe>' | Get-NetFirewallRule`
- [R2] Backup: `netsh advfirewall export "$W\backups\firewall-$ts.wfw"`
- [R2] Regra específica (preferida a desligar o firewall): `New-NetFirewallRule -DisplayName 'IA: <motivo>' -Direction Inbound -Program '<exe>' -Action Allow -Profile Private -WhatIf`. Abrir porta de entrada exige aprovação (invariante 6).
- Desfazer: `Remove-NetFirewallRule -DisplayName 'IA: <motivo>'`; restauração total: `netsh advfirewall import "<arquivo>.wfw"`.
- [R3] Desligar um perfil: só com CONFIRMO e motivo claro.

## 13. Armazenamento (volumes, saúde do disco, otimização, Storage Sense)

- [R0] Volumes: `Get-Volume | Select-Object DriveLetter, FileSystemLabel, HealthStatus, SizeRemaining, Size` (W-24)
- [R0] Discos físicos: `Get-PhysicalDisk | Select-Object FriendlyName, MediaType, HealthStatus, OperationalStatus`. HealthStatus Warning ou Unhealthy: recomende backup imediato.
- [R2] Otimizar: `Optimize-Volume -DriveLetter C -Analyze -Verbose` primeiro. O cmdlet escolhe TRIM para SSD e desfragmentação para HDD.
- [R1] Storage Sense: abrir `Start-Process ms-settings:storagesense`. Atua só no disco do sistema e está desligado por padrão. (W-44)
- Para liberar espaço, comece pelo diagnóstico da seção 9 e proponha opções; não apague nada antes do PLANO.

## 14. Programas e pacotes (winget, instalar, atualizar, remover)

- [R0] Instalados: `winget list`. Atualizações disponíveis: `winget upgrade`. (W-07)
- [R0] Encontrar: `winget search "<nome>"` e conferir com `winget show --id <ID> --exact` (editor, versão, origem).
- [R2] Backup da lista: `winget export -o "$W\backups\apps-$ts.json"`. Reinstalar a lista: `winget import -i <arquivo>`. (W-08, W-09)
- [R2] Instalar: `winget install --id <ID> --exact --source winget`. Aceitar licenças (`--accept-package-agreements`) só depois que o usuário aprovou o PLANO.
- [R2] Atualizar um: `winget upgrade --id <ID> --exact`. Em lote (`--all`) é longo: segundo plano com log.
- [R2] Remover: `winget uninstall --id <ID> --exact`.
- [R0] Apps da Store: `Get-AppxPackage | Select-Object -First 20 Name, Version`. Remover app do sistema é R3.
- Armadilha: winget pode faltar num perfil novo antes do primeiro login completo.

## 15. Windows Update (atualizações, reinício pendente)

- [R0] Últimas atualizações: `Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10 HotFixID, Description, InstalledOn` (mostra só parte das atualizações).
- [R0] Reinício pendente (chave usada na prática, não é API documentada): `Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired'`
- [R1] Abrir a tela: `Start-Process ms-settings:windowsupdate` e deixar o usuário iniciar.
- O módulo nativo WindowsUpdateProvider sumiu a partir do Windows 10 2004 (W-53). O PSWindowsUpdate é da comunidade: instalá-lo é R2, com aprovação.
- [R3] Pausar ou desativar o Windows Update.

## 16. Segurança: Defender, assinatura, UAC, Smart App Control, BitLocker

- [R0] Defender: `Get-MpComputerStatus | Select-Object AMRunningMode, AntivirusEnabled, RealTimeProtectionEnabled, AntivirusSignatureLastUpdated, QuickScanEndTime` (W-17)
- [R0] Ameaças detectadas: `Get-MpThreatDetection | Select-Object -First 10`
- [R1] Atualizar assinaturas: `Update-MpSignature` (pode exigir admin).
- [R1] Varredura rápida: `Start-MpScan -ScanType QuickScan -AsJob` (minutos). Arquivo suspeito: `Start-MpScan -ScanType CustomScan -ScanPath '<arquivo>'`.
- [R0] Assinatura de executável: `Get-AuthenticodeSignature '<arquivo>' | Select-Object Status, @{n='Assinante';e={$_.SignerCertificate.Subject}}`
- [R3] Exclusões (`Add-MpPreference -ExclusionPath`) ou desligar proteção em tempo real: alternativa mais estreita primeiro.
- [R0] BitLocker: `Get-BitLockerVolume | Select-Object MountPoint, VolumeStatus, ProtectionStatus, EncryptionPercentage` (admin). Não exiba a senha de recuperação sem pedido exato. (W-30)
- Smart App Control: desligado, só volta com reinstalação ou reset do Windows (W-35). UAC: o usuário principal deveria ser padrão, não admin (W-21).

## 17. Pontos de restauração e backup (System Restore, File History)

- [R0] Listar: `Get-ComputerRestorePoint` (admin, PowerShell 5.1).
- [R2] Criar: `Checkpoint-Computer -Description 'IA antes de <ação>' -RestorePointType MODIFY_SETTINGS`. Exige admin e Proteção do Sistema ligada; o Windows cria no máximo um a cada 24 h e o segundo pedido dá erro. (W-14)
- [R2] Ligar a proteção: `Enable-ComputerRestore -Drive 'C:\'`
- Armadilha: esses cmdlets são do Windows PowerShell 5.1; no 7, rode via `powershell.exe` (confira com `Get-Command Checkpoint-Computer`).
- Backup de arquivos do usuário: Histórico de Arquivos ou app Backup do Windows, configurados pelo próprio usuário.

## 18. Logs e eventos (Event Viewer, Get-WinEvent, falhas, desligamentos)

- [R0] Erros e críticos das últimas 24 h: `Get-WinEvent -FilterHashtable @{LogName='System'; Level=1,2; StartTime=(Get-Date).AddDays(-1)} -MaxEvents 30 -ErrorAction SilentlyContinue | Select-Object TimeCreated, Id, ProviderName, LevelDisplayName` (W-10)
- [R0] Desligamento inesperado: `@{LogName='System'; Id=41}`. Falha de aplicativo: `@{LogName='Application'; Id=1000}`.
- [R0] Mensagem de um evento: `(Get-WinEvent -FilterHashtable @{LogName='System'; Id=<id>} -MaxEvents 1).Message`
- [R1] Monitor de Confiabilidade: `perfmon /rel`
- Armadilha: sem eventos, o cmdlet lança erro "No events were found"; use `-ErrorAction SilentlyContinue`. Filtre no hashtable, não com Where-Object, pela velocidade.
- [R3] Limpar logs.

## 19. Reparos do sistema (DISM, SFC, chkdsk)

Ordem recomendada, tudo com admin e em segundo plano com log (W-19, W-20):
1. `DISM /Online /Cleanup-Image /ScanHealth` (diagnóstico, R1)
2. `DISM /Online /Cleanup-Image /RestoreHealth` (reparo da imagem, R2, pode levar dezenas de minutos)
3. `sfc /scannow` (repara arquivos protegidos usando a imagem, R2)
- [R1] Disco online: `chkdsk C: /scan`
- Logs: `C:\Windows\Logs\DISM\dism.log` e `C:\Windows\Logs\CBS\CBS.log`. A saída do sfc capturada pelo PowerShell pode vir com caracteres estranhos: leia o CBS.log.

## 20. Energia (powercfg, plano, bateria, o que acorda o PC)

- [R0] Planos: `powercfg /list` e `powercfg /getactivescheme` (W-29)
- [R1] Trocar de plano: `powercfg /setactive <GUID>` (anote o GUID anterior para desfazer).
- [R0] Relatório de bateria: `powercfg /batteryreport /output "$W\logs\bateria-$ts.html"`
- [R0] O que impede o sono: `powercfg /requests` (admin). O que acordou: `powercfg /lastwake`.
- [R1] Diagnóstico de energia: `powercfg /energy` (admin, 60 s, PC ocioso).

## 21. Dispositivos e drivers (PnP, pnputil, Gerenciador de Dispositivos)

- [R0] Com problema: `Get-PnpDevice -PresentOnly | Where-Object Status -ne 'OK' | Select-Object Class, FriendlyName, Status, InstanceId`
- [R0] Também: `pnputil /enum-devices /problem` e `pnputil /enum-drivers` (W-37)
- [R2] Desativar ou reativar: `Disable-PnpDevice -InstanceId '<id>' -WhatIf` / `Enable-PnpDevice`.
- [R3] Remover driver: `pnputil /delete-driver oem<N>.inf`. Ponto de restauração antes.

## 22. Diagnóstico avançado (Sysinternals, Process Explorer, Process Monitor, Autoruns)

- Ferramentas oficiais da Microsoft: Process Explorer (o que cada processo abriu), Process Monitor (atividade de arquivo, registro e processo em tempo real) e Autoruns (tudo que inicia sozinho). (W-45, B-03)
- [R2] Instalar: `winget search Sysinternals`, confira o editor Microsoft com `winget show`, e só então instale.
- Process Monitor gera muito volume: filtre por processo e grave em arquivo; nunca leia a captura inteira.

## 23. Variáveis de ambiente e PATH

- [R0] Ler: `[Environment]::GetEnvironmentVariable('Path','User')` e `'Machine'` (W-42)
- [R1 em User, R2 em Machine] Backup do valor antigo: `[Environment]::GetEnvironmentVariable('Path','User') | Out-File "$W\backups\path-user-$ts.txt"`
- Acrescentar sem duplicar:

```powershell
$a = [Environment]::GetEnvironmentVariable('Path','User')
$partes = @($a -split ';' | Where-Object { $_ })
if ($partes -notcontains '<pasta>') {
    [Environment]::SetEnvironmentVariable('Path', (($partes + '<pasta>') -join ';'), 'User')
}
```

- Nunca substitua o PATH inteiro. A mudança vale para processos novos: reabra o terminal.

## 24. PowerShell: política de execução, modos de linguagem, registro de atividade

- [R0] `Get-ExecutionPolicy -List`. Não altere LocalMachine nem CurrentUser (R3). (W-01)
- [R0] `$ExecutionContext.SessionState.LanguageMode`. ConstrainedLanguage indica controle de aplicativos ativo: respeite, não contorne. (W-36)
- Auditoria: todo script elevado usa `Start-Transcript` (seção 2). O registro de blocos de script (evento 4104) e a transcrição automática são configurados pelo usuário via política. (W-40)
- Qualidade de scripts maiores: verbos aprovados (`Get-Verb`) e PSScriptAnalyzer, se instalado. (W-31)

## 25. WSL e Windows Sandbox (Linux no Windows, ambiente descartável para testes)

- [R0] `wsl --status` e `wsl --list --verbose`. [R1] `wsl --shutdown` encerra todas as distros: confirme se há trabalho aberto.
- Arquivos usados por ferramentas Linux ficam no sistema de arquivos do Linux; acessar `/mnt/c` a partir do Linux é mais lento. (W-38)
- Windows Sandbox: desktop isolado e descartável para testar script ou instalador R3. Não existe no Windows Home. [R0] `Get-WindowsOptionalFeature -Online -FeatureName Containers-DisposableClientVM` (admin). [R2] Habilitar exige reinício. (W-15)
- Arquivo `.wsb` para teste sem rede e com pasta só leitura (W-16):

```xml
<Configuration>
  <Networking>Disable</Networking>
  <MappedFolders>
    <MappedFolder>
      <HostFolder>C:\Users\<usuario>\IA-Operador\scripts</HostFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
  </MappedFolders>
</Configuration>
```

Abrir: `Start-Process '<arquivo>.wsb'`. Tudo some ao fechar.

## 26. Interface gráfica (último recurso)

- Prefira cmdlet ou linha de comando. Agentes que operam só por cliques acertam pouco em benchmarks de Windows; usar a árvore de acessibilidade (UI Automation) ajuda, mas API vem antes. (A-16, A-17, W-46)
- Telas de configuração: `Start-Process ms-settings:<pagina>` (exemplos: display, sound, network-status, windowsupdate, startupapps, storagesense).
- Abrir app: `Start-Process '<exe ou app>'`.
