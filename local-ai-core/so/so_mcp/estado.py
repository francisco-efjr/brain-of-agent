"""Leitura do sistema (R0): retratos prontos por área e consultas livres só de leitura."""
from __future__ import annotations

import re

from . import politica
from .executor import cortar

_PENDENTE = r"""
$pend = (Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired') -or (Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending')
'Reinício pendente: ' + $(if ($pend) { 'sim' } else { 'não' })
"""

AREAS: dict[str, tuple[str, str]] = {
    "resumo": ("Windows, uptime, CPU, memória, disco do sistema e reinício pendente", r"""
$so = Get-CimInstance Win32_OperatingSystem
$cs = Get-CimInstance Win32_ComputerSystem
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
$disco = Get-CimInstance Win32_LogicalDisk -Filter ("DeviceID='" + $env:SystemDrive + "'")
$up = (Get-Date) - $so.LastBootUpTime
'Windows: ' + $so.Caption + ' ' + $so.Version + ' (build ' + $so.BuildNumber + ')'
'Computador: ' + $cs.Manufacturer + ' ' + $cs.Model + '; usuário: ' + $env:USERNAME
'Ligado há: ' + [int][math]::Floor($up.TotalHours) + ' h ' + $up.Minutes + ' min'
'CPU: ' + $cpu.Name.Trim() + '; uso agora: ' + $cpu.LoadPercentage + '%'
'Memória: ' + [math]::Round(($so.TotalVisibleMemorySize - $so.FreePhysicalMemory) / 1MB, 1) + ' de ' + [math]::Round($so.TotalVisibleMemorySize / 1MB, 1) + ' GB em uso'
'Disco do sistema (' + $env:SystemDrive + '): ' + [math]::Round($disco.FreeSpace / 1GB, 1) + ' GB livres de ' + [math]::Round($disco.Size / 1GB, 1) + ' GB'
""" + _PENDENTE),
    "disco": ("espaço livre por disco e saúde dos discos físicos", r"""
Get-CimInstance Win32_LogicalDisk | Where-Object { $_.DriveType -in 2, 3 } | Select-Object DeviceID, VolumeName,
    @{n = 'Tipo'; e = { if ($_.DriveType -eq 3) { 'local' } else { 'removível' } } },
    @{n = 'LivreGB'; e = { [math]::Round($_.FreeSpace / 1GB, 1) } }, @{n = 'TotalGB'; e = { [math]::Round($_.Size / 1GB, 1) } },
    @{n = 'Livre%'; e = { if ($_.Size) { [math]::Round(100 * $_.FreeSpace / $_.Size) } else { 0 } } } | Format-Table -AutoSize | Out-String -Width 160
try { Get-PhysicalDisk | Select-Object FriendlyName, MediaType, HealthStatus, @{n = 'TamanhoGB'; e = { [math]::Round($_.Size / 1GB) } } | Format-Table -AutoSize | Out-String -Width 160 }
catch { 'Saúde dos discos: indisponível' }
"""),
    "memoria": ("memória em uso e processos que mais usam memória", r"""
$so = Get-CimInstance Win32_OperatingSystem
'Memória em uso: ' + [math]::Round(($so.TotalVisibleMemorySize - $so.FreePhysicalMemory) / 1MB, 1) + ' de ' + [math]::Round($so.TotalVisibleMemorySize / 1MB, 1) + ' GB'
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First ([int](P 'LIMITE')) ProcessName, Id, @{n = 'MemMB'; e = { [math]::Round($_.WorkingSet64 / 1MB) } } | Format-Table -AutoSize | Out-String -Width 160
"""),
    "processos": ("processos por uso de CPU; filtro pelo nome ou título da janela", r"""
$f = P 'FILTRO'
Get-Process | Where-Object { -not $f -or $_.ProcessName -like ('*' + $f + '*') -or $_.MainWindowTitle -like ('*' + $f + '*') } |
    Sort-Object CPU -Descending | Select-Object -First ([int](P 'LIMITE')) ProcessName, Id, @{n = 'CPU_s'; e = { [math]::Round($_.CPU, 1) } },
    @{n = 'MemMB'; e = { [math]::Round($_.WorkingSet64 / 1MB) } }, @{n = 'Janela'; e = { $t = [string]$_.MainWindowTitle; if ($t.Length -gt 40) { $t.Substring(0, 40) } else { $t } } } |
    Format-Table -AutoSize | Out-String -Width 180
"""),
    "servicos": ("serviços; sem filtro, mostra os automáticos que estão parados", r"""
$f = P 'FILTRO'
if ($f) { $s = Get-Service | Where-Object { $_.Name -like ('*' + $f + '*') -or $_.DisplayName -like ('*' + $f + '*') } }
else { 'Sem filtro: serviços automáticos que não estão rodando.'; $s = Get-Service | Where-Object { [string]$_.StartType -eq 'Automatic' -and [string]$_.Status -ne 'Running' } }
$s | Select-Object -First ([int](P 'LIMITE')) Name, DisplayName, Status, StartType | Format-Table -AutoSize | Out-String -Width 180
"""),
    "rede": ("adaptadores ativos, IP, gateway, DNS e conectividade (sem enviar nada para fora)", r"""
Get-NetIPConfiguration | Where-Object { $_.NetAdapter.Status -eq 'Up' } | ForEach-Object {
    [pscustomobject]@{ Interface = $_.InterfaceAlias; IPv4 = ($_.IPv4Address.IPAddress -join ', '); Gateway = ($_.IPv4DefaultGateway.NextHop -join ', ');
        DNS = (($_.DNSServer | Where-Object { $_.AddressFamily -eq 2 } | ForEach-Object { $_.ServerAddresses }) -join ', ') }
} | Format-Table -AutoSize | Out-String -Width 180
Get-NetConnectionProfile | Select-Object InterfaceAlias, Name, NetworkCategory, IPv4Connectivity | Format-Table -AutoSize | Out-String -Width 160
"""),
    "programas": ("programas instalados; filtro pelo nome ou editor", r"""
$f = P 'FILTRO'
$chaves = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*', 'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*', 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*'
Get-ItemProperty $chaves -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName -and (-not $f -or $_.DisplayName -like ('*' + $f + '*') -or $_.Publisher -like ('*' + $f + '*')) } |
    Sort-Object DisplayName -Unique | Select-Object -First ([int](P 'LIMITE')) DisplayName, DisplayVersion, Publisher | Format-Table -AutoSize | Out-String -Width 180
'Para instalar, atualizar ou remover, ache o ID exato: so_consultar com "winget list <nome>" ou "winget search <nome>".'
"""),
    "inicializacao": ("programas que iniciam com o Windows", r"""
Get-CimInstance Win32_StartupCommand | Select-Object -First ([int](P 'LIMITE')) Name, Command, Location, User | Format-Table -AutoSize -Wrap | Out-String -Width 200
"""),
    "tarefas": ("tarefas agendadas fora de \\Microsoft\\ e as tarefas da IA", r"""
$f = P 'FILTRO'
if ($f) { $t = Get-ScheduledTask | Where-Object { $_.TaskName -like ('*' + $f + '*') -or $_.TaskPath -like ('*' + $f + '*') } }
else { $t = Get-ScheduledTask | Where-Object { $_.TaskPath -notlike '\Microsoft\*' } }
$t | Select-Object -First ([int](P 'LIMITE')) @{n = 'Caminho'; e = { $_.TaskPath + $_.TaskName } }, State, Author | Format-Table -AutoSize | Out-String -Width 200
'Tarefas da IA (\IA-Operador\):'
Get-ScheduledTask -TaskPath '\IA-Operador\' -ErrorAction SilentlyContinue | ForEach-Object {
    $i = $_ | Get-ScheduledTaskInfo
    [pscustomobject]@{ Tarefa = $_.TaskName; Estado = $_.State; Ultima = $i.LastRunTime; Resultado = $i.LastTaskResult; Proxima = $i.NextRunTime }
} | Format-Table -AutoSize | Out-String -Width 200
"""),
    "eventos": ("erros críticos do Sistema e de Aplicativos nas últimas 24 h; filtro pela origem ou texto", r"""
$f = P 'FILTRO'
$ev = Get-WinEvent -FilterHashtable @{ LogName = 'System', 'Application'; Level = 1, 2; StartTime = (Get-Date).AddHours(-24) } -MaxEvents 200 -ErrorAction SilentlyContinue
$ev = @($ev | Where-Object { -not $f -or $_.ProviderName -like ('*' + $f + '*') -or $_.Message -like ('*' + $f + '*') } | Select-Object -First ([int](P 'LIMITE')))
if ($ev.Count -eq 0) { 'Nenhum erro crítico nas últimas 24 h (com esse filtro).' } else {
    $ev | Select-Object TimeCreated, LogName, ProviderName, Id, @{n = 'Mensagem'; e = { $m = ([string]$_.Message -replace '\s+', ' '); if ($m.Length -gt 160) { $m.Substring(0, 160) + '...' } else { $m } } } |
        Format-Table -AutoSize -Wrap | Out-String -Width 220
}
"""),
    "atualizacoes": ("atualizações instaladas mais recentes e reinício pendente", r"""
Get-HotFix | Sort-Object InstalledOn -Descending -ErrorAction SilentlyContinue | Select-Object -First ([int](P 'LIMITE')) HotFixID, Description, InstalledOn | Format-Table -AutoSize | Out-String -Width 160
""" + _PENDENTE),
    "energia": ("plano de energia ativo, planos disponíveis e bateria", r"""
$ErrorActionPreference = 'Continue'
powercfg /getactivescheme
powercfg /list
$b = Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue
if ($b) { 'Bateria: ' + $b.EstimatedChargeRemaining + '% (status ' + $b.BatteryStatus + ')' } else { 'Sem bateria (desktop) ou não detectada.' }
"""),
    "seguranca": ("Defender, firewall, UAC, política de execução e modo de linguagem", r"""
try {
    $m = Get-MpComputerStatus
    'Defender: antivírus ' + $(if ($m.AntivirusEnabled) { 'ligado' } else { 'DESLIGADO' }) + '; tempo real ' + $(if ($m.RealTimeProtectionEnabled) { 'ligado' } else { 'DESLIGADO' }) + '; assinaturas de ' + $m.AntivirusSignatureLastUpdated + '; verificação rápida há ' + $m.QuickScanAge + ' dia(s)'
} catch { 'Defender: status indisponível (outro antivírus pode estar ativo)' }
Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction | Format-Table -AutoSize | Out-String -Width 120
$lua = (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System' -ErrorAction SilentlyContinue).EnableLUA
'UAC: ' + $(if ($lua -eq 1) { 'ligado' } else { 'DESLIGADO ou desconhecido' })
'Política de execução efetiva: ' + (Get-ExecutionPolicy)
'Modo de linguagem: ' + $ExecutionContext.SessionState.LanguageMode
"""),
    "usuario": ("usuário, se este processo está elevado e as pastas reais (OneDrive incluso)", r"""
$id = [Security.Principal.WindowsIdentity]::GetCurrent()
$adm = (New-Object Security.Principal.WindowsPrincipal($id)).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
'Usuário: ' + $id.Name
'Processo elevado: ' + $(if ($adm) { 'sim (a IA não deveria rodar elevada)' } else { 'não (bom: o UAC é a trava)' })
'Documentos: ' + [Environment]::GetFolderPath('MyDocuments')
'Área de trabalho: ' + [Environment]::GetFolderPath('Desktop')
'Downloads: ' + (Join-Path $env:USERPROFILE 'Downloads')
'Pasta da IA: ' + (Join-Path $env:USERPROFILE 'IA-Operador')
"""),
}

# Segunda cerca da consulta livre, no Windows: a árvore sintática do próprio PowerShell e, ao rodar,
# o modo de linguagem restrito (ConstrainedLanguage), que bloqueia métodos .NET fora dos tipos básicos.
VALIDADOR_PS = r"""
$cmd = P 'COMANDO'
$verbos = (P 'VERBOS').Split(',')
$externos = (P 'EXTERNOS').Split(',')
$metodos = (P 'METODOS').Split(',')
$tipos = (P 'TIPOS').Split(',')
$negados = (P 'NEGADOS').Split(',')
$extra = (P 'EXTRA').Split(',')
function Recusar([string]$m) { Write-Output ('RECUSADO: ' + $m); exit 3 }
$tokens = $null; $erros = $null
$ast = [System.Management.Automation.Language.Parser]::ParseInput($cmd, [ref]$tokens, [ref]$erros)
if ($erros.Count -gt 0) { Recusar ('erro de sintaxe: ' + $erros[0].Message) }
if (@($ast.FindAll({ param($n) $n -is [System.Management.Automation.Language.FileRedirectionAst] }, $true)).Count -gt 0) { Recusar 'redirecionamento grava arquivo' }
foreach ($c in $ast.FindAll({ param($n) $n -is [System.Management.Automation.Language.CommandAst] }, $true)) {
    if ($c.InvocationOperator -ne [System.Management.Automation.Language.TokenKind]::Unknown) { Recusar 'operador & ou . executa código' }
    $nome = $c.GetCommandName()
    if (-not $nome) { Recusar 'comando sem nome fixo' }
    $info = Get-Command -Name $nome -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $info) { Recusar ('comando desconhecido: ' + $nome) }
    $guarda = 0
    while ([string]$info.CommandType -eq 'Alias' -and $guarda -lt 5) { $info = $info.ResolvedCommand; $guarda++ }
    $tipo = [string]$info.CommandType
    if ($tipo -eq 'Cmdlet' -or $tipo -eq 'Function') {
        $n = $info.Name.ToLower()
        if ($negados -contains $n) { Recusar ($info.Name + ' lida com segredo') }
        if (-not ($extra -contains $n) -and -not ($verbos -contains ([string]$info.Verb).ToLower())) { Recusar ($info.Name + ' não é só leitura') }
    } elseif ($tipo -eq 'Application') {
        $base = [System.IO.Path]::GetFileNameWithoutExtension($info.Name).ToLower()
        if (-not ($externos -contains $base)) { Recusar ($info.Name + ' não está na lista de programas de leitura') }
    } else { Recusar ($nome + ' é do tipo ' + $tipo + ', não aceito') }
}
foreach ($m in $ast.FindAll({ param($n) $n -is [System.Management.Automation.Language.InvokeMemberExpressionAst] }, $true)) {
    if (-not ($m.Member -is [System.Management.Automation.Language.StringConstantExpressionAst])) { Recusar 'método com nome dinâmico' }
    if ($m.Static) {
        $t = $m.Expression.TypeName.FullName.ToLower()
        if (-not ($tipos -contains $t)) { Recusar ('[' + $t + ']:: não aceito') }
    } elseif (-not ($metodos -contains $m.Member.Value.ToLower())) { Recusar ('método .' + $m.Member.Value + '() não aceito') }
}
$ErrorActionPreference = 'Continue'
$ExecutionContext.SessionState.LanguageMode = 'ConstrainedLanguage'
Invoke-Expression $cmd | Out-String -Width 200
"""


def _filtro(texto: str | None) -> str:
    return re.sub(r"[*?\[\]`'\"]", "", texto or "").strip()[:60]


class Leitor:
    def __init__(self, cfg, executor):
        self.cfg = cfg
        self.executor = executor

    def areas(self) -> str:
        return "; ".join(f"{nome} ({desc})" for nome, (desc, _) in AREAS.items())

    def estado(self, area: str, filtro: str | None = None, limite: int | None = None) -> tuple[str, bool]:
        if area not in AREAS:
            return f"Área desconhecida: {area!r}. Use uma de: {', '.join(AREAS)}", True
        limite = max(1, min(int(limite or 15), 50))
        r = self.executor.rodar(AREAS[area][1], {"FILTRO": _filtro(filtro), "LIMITE": limite}, rotulo=f"estado:{area}")
        texto = politica.mascarar_segredos(r.texto()) or "(sem saída)"
        return cortar(texto, self.cfg.saida_max_caracteres), not r.ok

    def consultar(self, comando: str) -> tuple[str, bool]:
        motivo = politica.checar_consulta(comando)
        if motivo:
            return (f"RECUSADO: {motivo}. so_consultar só lê. Para áreas comuns use so_estado; para mudar algo use so_planejar.", True)
        args = {
            "COMANDO": comando,
            "VERBOS": ",".join(sorted(politica.VERBOS_LEITURA)),
            "EXTERNOS": ",".join(sorted(e.removesuffix(".exe") for e in politica.EXTERNOS)),
            "METODOS": ",".join(sorted(politica.METODOS_OK)),
            "TIPOS": ",".join(sorted(politica.TIPOS_ESTATICOS_OK)),
            "NEGADOS": ",".join(sorted(politica.CMDLETS_NEGADOS)),
            "EXTRA": ",".join(sorted(politica.CMDLETS_EXTRA)),
        }
        r = self.executor.rodar(VALIDADOR_PS, args, rotulo="consultar")
        texto = r.texto()
        if r.saida.strip().startswith("RECUSADO:"):
            return r.saida.strip() + ". so_consultar só lê; para mudar algo use so_planejar.", True
        texto = politica.mascarar_segredos(texto) or "(sem saída)"
        return cortar(texto, self.cfg.saida_max_caracteres), not r.ok and not r.saida.strip()
