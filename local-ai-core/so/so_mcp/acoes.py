"""Catálogo de ações que mudam o sistema.

Cada ação traz a própria regra de risco e o roteiro fixo da esteira: observar o estado atual,
ensaiar sem efeito, fazer backup, aplicar, verificar e dizer como desfazer. O modelo só escolhe a
ação e os parâmetros; o resto é código. Scripts PowerShell leem parâmetros com (P 'NOME').
Funções Python recebem (p, obs, ctx) ou parte disso; ctx tem cfg, executor e o id do plano.
"""
from __future__ import annotations

import hashlib
import os
import pathlib
import re
import shutil
from dataclasses import dataclass, field
from typing import Any, Callable

from . import politica
from .config import caminho as expandir_caminho

# ---------------------------------------------------------------- estrutura


@dataclass
class Param:
    tipo: str  # string | integer | boolean | caminho
    descricao: str
    obrigatorio: bool = True
    enum: tuple[str, ...] | None = None
    regex: str | None = None
    padrao: Any = None
    minimo: int | None = None
    maximo: int | None = None


@dataclass
class Acao:
    nome: str
    descricao: str
    parametros: dict[str, Param]
    avaliar: Callable[..., tuple[str, str]]
    resumo: Callable[..., str]
    aplicar: Any
    observar: Any = None
    ensaiar: Any = None
    backup: Any = None
    verificar: Any = None
    desfazer: Callable[..., dict] | None = None
    admin: Any = False
    extras: Callable[..., dict] | None = None
    timeout_s: int | None = None
    interna: bool = False
    chaves_estado: tuple[str, ...] | None = None
    aviso: str = ""
    verificacao: str = ""
    backup_ext: str = ".txt"

    def precisa_admin(self, p: dict) -> bool:
        return self.admin(p) if callable(self.admin) else bool(self.admin)


def validar(acao: Acao, brutos: Any) -> tuple[dict, list[str]]:
    """Confere e converte os parâmetros. Devolve (parâmetros, erros)."""
    if brutos is None:
        brutos = {}
    if not isinstance(brutos, dict):
        return {}, ["parametros deve ser um objeto JSON, por exemplo {\"nome\": \"Spooler\"}"]
    erros, saida = [], {}
    desconhecidos = sorted(set(brutos) - set(acao.parametros))
    if desconhecidos:
        erros.append(f"parâmetros desconhecidos: {', '.join(desconhecidos)}")
    for nome, spec in acao.parametros.items():
        valor = brutos.get(nome)
        if valor is None or valor == "":
            if spec.obrigatorio and spec.padrao is None:
                erros.append(f"falta '{nome}' ({spec.descricao})")
            elif spec.padrao is not None:
                saida[nome] = spec.padrao
            continue
        if spec.tipo == "boolean":
            if isinstance(valor, str):
                if valor.strip().lower() in ("true", "sim", "1", "yes"):
                    valor = True
                elif valor.strip().lower() in ("false", "nao", "não", "0", "no"):
                    valor = False
            if not isinstance(valor, bool):
                erros.append(f"'{nome}' deve ser true ou false")
                continue
        elif spec.tipo == "integer":
            try:
                valor = int(str(valor).strip())
            except ValueError:
                erros.append(f"'{nome}' deve ser um número inteiro")
                continue
            if spec.minimo is not None and valor < spec.minimo or spec.maximo is not None and valor > spec.maximo:
                erros.append(f"'{nome}' deve ficar entre {spec.minimo} e {spec.maximo}")
                continue
        else:
            valor = str(valor)
            if spec.maximo is not None and len(valor) > spec.maximo:
                erros.append(f"'{nome}' passa de {spec.maximo} caracteres")
                continue
            if spec.enum and valor not in spec.enum:
                achado = next((e for e in spec.enum if e.lower() == valor.lower()), None)
                if achado is None:
                    erros.append(f"'{nome}' deve ser um de: {', '.join(spec.enum)}")
                    continue
                valor = achado
            if spec.regex and not re.fullmatch(spec.regex, valor):
                erros.append(f"'{nome}' tem formato inválido ({spec.descricao})")
                continue
            if spec.tipo == "caminho":
                cam = expandir_caminho(valor)
                if not cam.is_absolute():
                    erros.append(f"'{nome}' precisa ser um caminho completo, como C:\\Users\\voce\\Documents\\x.txt")
                    continue
                valor = str(cam)
        saida[nome] = valor
    return saida, erros


def assinatura(acao: Acao) -> str:
    partes = []
    for nome, spec in acao.parametros.items():
        extra = f" ({'|'.join(spec.enum)})" if spec.enum else ""
        partes.append(f"{nome}{'' if spec.obrigatorio and spec.padrao is None else '?'}{extra}")
    return f"{acao.nome} {{{', '.join(partes)}}}"


def _sha256(arq: pathlib.Path) -> str:
    h = hashlib.sha256()
    with arq.open("rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def _inviavel(motivo: str) -> tuple[str, str]:
    return "INVIAVEL", motivo


# ---------------------------------------------------------------- serviços

_OBS_SERVICO = r"""
$s = Get-Service -Name (P 'NOME') -ErrorAction SilentlyContinue
if (-not $s) { '{"existe":false}' } else {
    [pscustomobject]@{ existe = $true; nome = $s.Name; exibicao = $s.DisplayName; status = [string]$s.Status; inicio = [string]$s.StartType } | ConvertTo-Json -Compress
}
"""
_NOME_SERVICO = Param("string", "nome curto do serviço, como Spooler (veja so_estado area=servicos)", regex=r"[\w.$@ \-]{1,100}")


def _servico_base(obs: dict) -> tuple[str, str] | None:
    if not obs.get("existe"):
        return _inviavel("serviço não encontrado: confira o nome curto com so_estado area=servicos filtro=<parte do nome>")
    if obs["nome"].lower() in politica.SERVICOS_BLOQUEADOS:
        return "BLOQUEADO", "serviço essencial do Windows: mexer nele pode impedir o PC de iniciar"
    return None


def _avaliar_servico_inicio(p, obs, ctx):
    base = _servico_base(obs)
    if base:
        return base
    if obs["inicio"] == p["tipo"]:
        return _inviavel(f"o serviço já está com início {p['tipo']}")
    if obs["nome"].lower() in politica.SERVICOS_PROTEGIDOS and p["tipo"] != "Automatic":
        return "R3", "serviço de proteção, rede ou atualização: mudar o início reduz a segurança ou a estabilidade"
    return "R2", "serviço do sistema, exige administrador"


def _desfazer_servico_inicio(p, obs, info):
    if obs.get("inicio") in ("Automatic", "Manual", "Disabled"):
        return {"acao": "servico_configurar_inicio", "parametros": {"nome": obs["nome"], "tipo": obs["inicio"]}}
    return {"nota": f"o início anterior era {obs.get('inicio')}; ajuste em services.msc"}


SERVICO_CONFIGURAR_INICIO = Acao(
    nome="servico_configurar_inicio",
    descricao="Muda como um serviço inicia: Automatic, Manual ou Disabled.",
    parametros={"nome": _NOME_SERVICO, "tipo": Param("string", "tipo de início", enum=("Automatic", "Manual", "Disabled"))},
    observar=_OBS_SERVICO,
    avaliar=_avaliar_servico_inicio,
    resumo=lambda p, obs: f"Mudar o início do serviço {obs.get('nome', p['nome'])} de {obs.get('inicio')} para {p['tipo']}",
    ensaiar="Set-Service -Name (P 'NOME') -StartupType (P 'TIPO') -WhatIf",
    aplicar="Set-Service -Name (P 'NOME') -StartupType (P 'TIPO')\n'feito'",
    verificar=r"""
$s = Get-Service -Name (P 'NOME')
[pscustomobject]@{ ok = ([string]$s.StartType -eq (P 'TIPO')); detalhe = ('início agora: ' + [string]$s.StartType + '; status: ' + [string]$s.Status) } | ConvertTo-Json -Compress
""",
    verificacao="ler o tipo de início de novo",
    desfazer=_desfazer_servico_inicio,
    admin=True,
    chaves_estado=("inicio",),
)


def _avaliar_servico_reiniciar(p, obs, ctx):
    base = _servico_base(obs)
    if base:
        return base
    if obs["inicio"] == "Disabled":
        return _inviavel("o serviço está desativado; mude o início antes (servico_configurar_inicio)")
    return "R2", "reiniciar serviço do sistema, exige administrador"


SERVICO_REINICIAR = Acao(
    nome="servico_reiniciar",
    descricao="Reinicia um serviço (para e inicia de novo).",
    parametros={"nome": _NOME_SERVICO},
    observar=_OBS_SERVICO,
    avaliar=_avaliar_servico_reiniciar,
    resumo=lambda p, obs: f"Reiniciar o serviço {obs.get('nome', p['nome'])} (status atual: {obs.get('status')})",
    ensaiar="Restart-Service -Name (P 'NOME') -Force -WhatIf",
    aplicar="Restart-Service -Name (P 'NOME') -Force\n'feito'",
    verificar=r"""
$s = Get-Service -Name (P 'NOME')
[pscustomobject]@{ ok = ([string]$s.Status -eq 'Running'); detalhe = ('status: ' + [string]$s.Status) } | ConvertTo-Json -Compress
""",
    verificacao="conferir que o serviço voltou a Running",
    desfazer=lambda p, obs, info: {"nota": "nada a desfazer: o serviço volta ao mesmo estado"},
    admin=True,
    chaves_estado=("inicio",),
)

# ---------------------------------------------------------------- processos

_OBS_PROCESSO = r"""
$alvo = P 'ALVO'
if ($alvo -match '^\d+$') { $ps = @(Get-Process -Id ([int]$alvo) -ErrorAction SilentlyContinue) }
else { $ps = @(Get-Process -Name ($alvo -replace '\.exe$', '') -ErrorAction SilentlyContinue) }
$lista = @($ps | Select-Object -First 20 | ForEach-Object {
    [pscustomobject]@{ id = $_.Id; nome = $_.ProcessName; caminho = [string]$_.Path; janela = [string]$_.MainWindowTitle; memMB = [math]::Round($_.WorkingSet64 / 1MB) }
})
[pscustomobject]@{ existe = ($lista.Count -gt 0); quantidade = $ps.Count; ids = (($lista | ForEach-Object { $_.id }) -join ','); processos = $lista } | ConvertTo-Json -Compress -Depth 4
"""


def _lista(valor: Any) -> list:
    if valor is None:
        return []
    return valor if isinstance(valor, list) else [valor]


def _avaliar_processo(p, obs, ctx):
    if not obs.get("existe"):
        return _inviavel("nenhum processo com esse nome ou PID: veja so_estado area=processos")
    procs = _lista(obs.get("processos"))
    if any(str(x.get("nome", "")).lower() in politica.PROCESSOS_CRITICOS for x in procs):
        return "BLOQUEADO", "processo essencial do Windows: encerrar derruba a sessão ou o sistema"
    if int(obs.get("quantidade", 0)) > 20:
        return _inviavel("mais de 20 processos com esse nome: use o PID de um deles")
    if any("\\windows\\" in str(x.get("caminho", "")).lower() for x in procs):
        return "R3", "processo do sistema (pasta do Windows)"
    if p.get("forcar"):
        return "R2", "encerrar à força pode perder trabalho não salvo"
    return "R1", "fechar app do usuário do jeito normal (ele pode pedir para salvar)"


def _ensaiar_processo(p, obs, ctx):
    linhas = [f"Vai {'encerrar à força' if p.get('forcar') else 'pedir para fechar'}:"]
    for x in _lista(obs.get("processos")):
        linhas.append(f"- {x.get('nome')} (PID {x.get('id')}, {x.get('memMB')} MB) {x.get('janela') or ''}".rstrip())
    return "\n".join(linhas)


PROCESSO_ENCERRAR = Acao(
    nome="processo_encerrar",
    descricao="Fecha um programa pelo nome (sem .exe) ou PID. Sem forcar, pede para fechar e o app pode perguntar se quer salvar.",
    parametros={
        "alvo": Param("string", "nome do processo sem .exe, como notepad, ou o PID", regex=r"[\w.\- ]{1,80}"),
        "forcar": Param("boolean", "true encerra à força (pode perder dados)", obrigatorio=False, padrao=False),
    },
    observar=_OBS_PROCESSO,
    avaliar=_avaliar_processo,
    resumo=lambda p, obs: f"{'Encerrar à força' if p.get('forcar') else 'Fechar'} {p['alvo']} ({obs.get('quantidade')} processo(s))",
    ensaiar=_ensaiar_processo,
    extras=lambda p, obs: {"IDS": obs.get("ids", ""), "FORCAR": bool(p.get("forcar"))},
    aplicar=r"""
$ids = (P 'IDS') -split ',' | Where-Object { $_ } | ForEach-Object { [int]$_ }
foreach ($id in $ids) {
    $p = Get-Process -Id $id -ErrorAction SilentlyContinue
    if ($p) { if ((P 'FORCAR') -eq 'True') { Stop-Process -Id $id -Force } else { [void]$p.CloseMainWindow() } }
}
Start-Sleep -Seconds 5
'pedido enviado'
""",
    verificar=r"""
$ids = (P 'IDS') -split ',' | Where-Object { $_ } | ForEach-Object { [int]$_ }
$vivos = @($ids | Where-Object { Get-Process -Id $_ -ErrorAction SilentlyContinue })
$det = $(if ($vivos.Count -eq 0) { 'todos fechados' } else { 'ainda abertos (talvez pedindo para salvar): ' + ($vivos -join ', ') })
[pscustomobject]@{ ok = ($vivos.Count -eq 0); detalhe = $det } | ConvertTo-Json -Compress
""",
    verificacao="conferir que os PIDs não existem mais",
    desfazer=lambda p, obs, info: {"nota": "não dá para desfazer; abra o app de novo (app_abrir)"},
    chaves_estado=("ids",),
)

# ---------------------------------------------------------------- programas (winget)

_ID_WINGET = Param("string", "ID exato do winget, como Mozilla.Firefox (procure com so_consultar \"winget search <nome>\")",
                   regex=r"[A-Za-z0-9][\w.\-+]{1,99}")
_OBS_WINGET = r"""
$ErrorActionPreference = 'Continue'
$id = P 'ID'
$mostrar = (winget show --id $id --exact --source winget --disable-interactivity 2>&1 | Out-String)
$codMostrar = $LASTEXITCODE
$lista = (winget list --id $id --exact --source winget --disable-interactivity 2>&1 | Out-String)
$codLista = $LASTEXITCODE
$limpa = { param($t) (($t -split "`r?`n" | Where-Object { $_.Trim() -and $_ -notmatch '^[\s\-\\|/]+$' -and $_ -notmatch '[\u2580-\u259F]' } | Select-Object -First 12) -join "`n") }
[pscustomobject]@{ existe = ($codMostrar -eq 0); instalado = ($codLista -eq 0); detalhe = (& $limpa $mostrar); lista = (& $limpa $lista) } | ConvertTo-Json -Compress
"""
_VERIFICAR_INSTALADO = r"""
$ErrorActionPreference = 'Continue'
$null = winget list --id (P 'ID') --exact --source winget --disable-interactivity 2>&1
$instalado = ($LASTEXITCODE -eq 0)
[pscustomobject]@{ ok = ($instalado -eq ((P 'ESPERADO') -eq 'True')); detalhe = ('instalado: ' + $instalado) } | ConvertTo-Json -Compress
"""
_SEGURANCA = re.compile(r"(?i)antivirus|defender|security|firewall|malware|kaspersky|avast|avg|norton|eset|bitdefender|mcafee|sophos")


def _avaliar_instalar(p, obs, ctx):
    if not obs.get("existe"):
        return _inviavel("ID não encontrado no winget (busca exata): procure com so_consultar \"winget search <nome>\" e use o ID exato")
    if obs.get("instalado"):
        return _inviavel("já está instalado; para atualizar use programa_atualizar")
    return "R2", "instalar programa muda o sistema"


def _avaliar_remover(p, obs, ctx):
    if not obs.get("instalado"):
        return _inviavel("não aparece como instalado no winget com esse ID")
    if _SEGURANCA.search(p["id"]):
        return "R3", "remover programa de segurança reduz a proteção"
    return "R2", "remover programa muda o sistema"


def _avaliar_atualizar(p, obs, ctx):
    if not obs.get("instalado"):
        return _inviavel("não aparece como instalado no winget com esse ID")
    return "R2", "atualizar programa muda o sistema"


PROGRAMA_INSTALAR = Acao(
    nome="programa_instalar",
    descricao="Instala um programa pelo winget com ID exato. Nunca baixa instalador de site.",
    parametros={"id": _ID_WINGET},
    observar=_OBS_WINGET,
    avaliar=_avaliar_instalar,
    resumo=lambda p, obs: f"Instalar {p['id']} pelo winget",
    ensaiar=lambda p, obs, ctx: f"winget install --id {p['id']} --exact --source winget --silent\nPacote encontrado:\n{obs.get('detalhe', '')}",
    aplicar=r"""
$ErrorActionPreference = 'Continue'
winget install --id (P 'ID') --exact --source winget --silent --disable-interactivity --accept-package-agreements 2>&1 | Select-Object -Last 15 | Out-String
if ($LASTEXITCODE -ne 0) { throw ('winget terminou com código ' + $LASTEXITCODE) }
""",
    extras=lambda p, obs: {"ESPERADO": True},
    verificar=_VERIFICAR_INSTALADO,
    verificacao="winget list --id <id> --exact",
    desfazer=lambda p, obs, info: {"acao": "programa_remover", "parametros": {"id": p["id"]}},
    timeout_s=540,
    aviso="Ao aprovar, você aceita a licença do pacote (opção --accept-package-agreements do winget).",
    chaves_estado=("instalado",),
)

PROGRAMA_REMOVER = Acao(
    nome="programa_remover",
    descricao="Desinstala um programa pelo winget com ID exato.",
    parametros={"id": _ID_WINGET},
    observar=_OBS_WINGET,
    avaliar=_avaliar_remover,
    resumo=lambda p, obs: f"Desinstalar {p['id']} pelo winget",
    ensaiar=lambda p, obs, ctx: f"winget uninstall --id {p['id']} --exact --silent\nInstalado hoje:\n{obs.get('lista', '')}",
    aplicar=r"""
$ErrorActionPreference = 'Continue'
winget uninstall --id (P 'ID') --exact --source winget --silent --disable-interactivity 2>&1 | Select-Object -Last 15 | Out-String
if ($LASTEXITCODE -ne 0) { throw ('winget terminou com código ' + $LASTEXITCODE) }
""",
    extras=lambda p, obs: {"ESPERADO": False},
    verificar=_VERIFICAR_INSTALADO,
    verificacao="winget list --id <id> --exact não deve achar mais",
    desfazer=lambda p, obs, info: {"acao": "programa_instalar", "parametros": {"id": p["id"]},
                                   "nota": "reinstalar não traz de volta as configurações apagadas"},
    timeout_s=540,
    chaves_estado=("instalado",),
)

PROGRAMA_ATUALIZAR = Acao(
    nome="programa_atualizar",
    descricao="Atualiza um programa instalado pelo winget com ID exato.",
    parametros={"id": _ID_WINGET},
    observar=_OBS_WINGET,
    avaliar=_avaliar_atualizar,
    resumo=lambda p, obs: f"Atualizar {p['id']} pelo winget",
    ensaiar=lambda p, obs, ctx: f"winget upgrade --id {p['id']} --exact --silent\nVersão instalada hoje:\n{obs.get('lista', '')}",
    aplicar=r"""
$ErrorActionPreference = 'Continue'
winget upgrade --id (P 'ID') --exact --source winget --silent --disable-interactivity --accept-package-agreements 2>&1 | Select-Object -Last 15 | Out-String
if ($LASTEXITCODE -ne 0) { throw ('winget terminou com código ' + $LASTEXITCODE + ' (pode ser que não haja atualização)') }
""",
    extras=lambda p, obs: {"ESPERADO": True},
    verificar=_VERIFICAR_INSTALADO,
    verificacao="conferir que continua instalado (a versão aparece no histórico)",
    desfazer=lambda p, obs, info: {"nota": "o winget não volta versão sozinho. Versão anterior registrada no plano; "
                                           "para voltar: winget install --id <id> --version <versão anterior> --force"},
    timeout_s=540,
    aviso="Ao aprovar, você aceita a licença do pacote (opção --accept-package-agreements do winget).",
    chaves_estado=("instalado",),
)

# ---------------------------------------------------------------- tarefas agendadas

_OBS_TAREFA = r"""
$t = Get-ScheduledTask -TaskPath (P 'TP') -TaskName (P 'TN') -ErrorAction SilentlyContinue
if (-not $t) { '{"existe":false}' } else {
    $acoes = ($t.Actions | ForEach-Object { ([string]$_.Execute + ' ' + [string]$_.Arguments).Trim() }) -join ' | '
    [pscustomobject]@{ existe = $true; estado = [string]$t.State; autor = [string]$t.Author; acoes = $acoes } | ConvertTo-Json -Compress
}
"""


def _partes_tarefa(caminho: str) -> dict:
    i = caminho.rfind("\\")
    return {"TP": caminho[: i + 1] or "\\", "TN": caminho[i + 1:]}


_TAREFAS_PROTECAO = ("\\microsoft\\windows\\windows defender", "\\microsoft\\windows\\updateorchestrator",
                     "\\microsoft\\windows\\windowsupdate", "\\microsoft\\windows\\waasmedic")


def _avaliar_tarefa_ativar(p, obs, ctx):
    if not obs.get("existe"):
        return _inviavel("tarefa não encontrada: veja so_estado area=tarefas (caminho completo, como \\IA-Operador\\IA-backup)")
    if p["ativa"] and obs["estado"] != "Disabled":
        return _inviavel("a tarefa já está ativa")
    if not p["ativa"] and obs["estado"] == "Disabled":
        return _inviavel("a tarefa já está desativada")
    tp = _partes_tarefa(p["caminho"])["TP"].lower()
    if not p["ativa"] and tp.startswith(_TAREFAS_PROTECAO):
        return "R3", "tarefa de proteção ou de atualização do Windows"
    return "R2", "tarefa agendada"


TAREFA_ATIVAR = Acao(
    nome="tarefa_ativar",
    descricao="Ativa ou desativa uma tarefa do Agendador de Tarefas (caminho completo com a pasta).",
    parametros={
        "caminho": Param("string", "pasta e nome da tarefa, como \\IA-Operador\\IA-backup", regex=r"\\[\w .\-\\{}]{1,200}"),
        "ativa": Param("boolean", "true ativa, false desativa"),
    },
    observar=_OBS_TAREFA,
    avaliar=_avaliar_tarefa_ativar,
    resumo=lambda p, obs: f"{'Ativar' if p['ativa'] else 'Desativar'} a tarefa {p['caminho']} (hoje: {obs.get('estado')})",
    extras=lambda p, obs: {**_partes_tarefa(p["caminho"]), "ATIVA": bool(p["ativa"])},
    ensaiar=lambda p, obs, ctx: f"{'Enable' if p['ativa'] else 'Disable'}-ScheduledTask {p['caminho']}\nAções da tarefa: {obs.get('acoes')}",
    backup=r"""
Export-ScheduledTask -TaskPath (P 'TP') -TaskName (P 'TN') | Out-File -LiteralPath (P 'BACKUP') -Encoding utf8
'tarefa exportada para ' + (P 'BACKUP')
""",
    backup_ext=".xml",
    aplicar=r"""
if ((P 'ATIVA') -eq 'True') { Enable-ScheduledTask -TaskPath (P 'TP') -TaskName (P 'TN') | Out-Null }
else { Disable-ScheduledTask -TaskPath (P 'TP') -TaskName (P 'TN') | Out-Null }
'feito'
""",
    verificar=r"""
$t = Get-ScheduledTask -TaskPath (P 'TP') -TaskName (P 'TN')
$ativa = ([string]$t.State -ne 'Disabled')
[pscustomobject]@{ ok = ($ativa -eq ((P 'ATIVA') -eq 'True')); detalhe = ('estado: ' + [string]$t.State) } | ConvertTo-Json -Compress
""",
    verificacao="ler o estado da tarefa de novo",
    desfazer=lambda p, obs, info: {"acao": "tarefa_ativar", "parametros": {"caminho": p["caminho"], "ativa": not p["ativa"]}},
    admin=lambda p: p["caminho"].lower().startswith("\\microsoft\\"),
    chaves_estado=("estado",),
)


def _observar_tarefa_criar(p, ctx):
    script = pathlib.Path(p["script"])
    obs: dict[str, Any] = {"scriptExiste": script.is_file(), "scriptNaPasta": politica.dentro(script, ctx.cfg.scripts)}
    if obs["scriptExiste"]:
        texto = script.read_text(encoding="utf-8-sig", errors="replace")
        obs.update(sha256=_sha256(script), linhas=len(texto.splitlines()), inicio="\n".join(texto.splitlines()[:25]),
                   temParar="PARAR" in texto, segredos=politica.achar_segredos(texto))
    r = ctx.executor.rodar(_OBS_TAREFA, {"TP": "\\IA-Operador\\", "TN": "IA-" + p["nome"]}, rotulo="tarefa_criar:observar")
    if not r.ok:
        raise RuntimeError(r.texto())
    obs["tarefaExiste"] = bool(r.json().get("existe"))
    return obs


def _avaliar_tarefa_criar(p, obs, ctx):
    if not obs["scriptNaPasta"] or not p["script"].lower().endswith(".ps1"):
        return _inviavel(f"o script precisa ser um .ps1 em {ctx.cfg.scripts} (com ficha aprovada; veja o tema automação)")
    if not obs["scriptExiste"]:
        return _inviavel("o script não existe: escreva antes com arquivo_escrever")
    if obs["tarefaExiste"]:
        return _inviavel(f"já existe a tarefa \\IA-Operador\\IA-{p['nome']}")
    if p["gatilho"] == "diario" and not p.get("horario"):
        return _inviavel("gatilho diario precisa de horario HH:MM")
    if p["gatilho"] == "intervalo" and not p.get("minutos"):
        return _inviavel("gatilho intervalo precisa de minutos (15 a 1440)")
    if obs.get("segredos"):
        return "R3", "o script parece conter segredo: " + ", ".join(obs["segredos"])
    motivo = "tarefa agendada roda sozinha, sem você olhando"
    if not obs.get("temParar"):
        motivo += "; atenção: o script não confere o arquivo PARAR (modelo no tema automação)"
    return "R2", motivo


TAREFA_CRIAR = Acao(
    nome="tarefa_criar",
    descricao="Agenda um script .ps1 de IA-Operador\\scripts\\ na pasta \\IA-Operador\\ do Agendador, com limite de 30 min e sem execução sobreposta. Roda só com você logado e sem administrador.",
    parametros={
        "nome": Param("string", "nome curto, sem espaços (a tarefa fica IA-<nome>)", regex=r"[\w\-]{1,60}"),
        "script": Param("caminho", "caminho completo do .ps1 em IA-Operador\\scripts\\", maximo=300),
        "gatilho": Param("string", "quando roda", enum=("diario", "ao_entrar", "intervalo")),
        "horario": Param("string", "HH:MM, para gatilho diario", obrigatorio=False, regex=r"([01]\d|2[0-3]):[0-5]\d"),
        "minutos": Param("integer", "intervalo em minutos, para gatilho intervalo", obrigatorio=False, minimo=15, maximo=1440),
    },
    observar=_observar_tarefa_criar,
    avaliar=_avaliar_tarefa_criar,
    resumo=lambda p, obs: f"Criar a tarefa \\IA-Operador\\IA-{p['nome']} ({p['gatilho']}) que roda {pathlib.Path(p['script']).name}",
    ensaiar=lambda p, obs, ctx: (f"Script: {p['script']} ({obs.get('linhas')} linhas, sha256 {str(obs.get('sha256'))[:12]})\n"
                                 f"Início do script:\n{obs.get('inicio', '')}"),
    extras=lambda p, obs: {"HORARIO": p.get("horario") or "", "MINUTOS": p.get("minutos") or ""},
    aplicar=r"""
$script = P 'SCRIPT'
$acao = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument ('-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File "' + $script + '"')
switch (P 'GATILHO') {
    'diario' { $gatilho = New-ScheduledTaskTrigger -Daily -At (P 'HORARIO') }
    'ao_entrar' { $gatilho = New-ScheduledTaskTrigger -AtLogOn -User ([Environment]::UserDomainName + '\' + [Environment]::UserName) }
    'intervalo' { $gatilho = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(2) -RepetitionInterval (New-TimeSpan -Minutes ([int](P 'MINUTOS'))) }
}
$config = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 30) -MultipleInstances IgnoreNew -StartWhenAvailable
Register-ScheduledTask -TaskName ('IA-' + (P 'NOME')) -TaskPath '\IA-Operador\' -Action $acao -Trigger $gatilho -Settings $config -Description ('Criada pela IA local, plano ' + (P 'PLANO')) | Out-Null
'tarefa criada'
""",
    verificar=r"""
$t = Get-ScheduledTask -TaskPath '\IA-Operador\' -TaskName ('IA-' + (P 'NOME')) -ErrorAction SilentlyContinue
[pscustomobject]@{ ok = [bool]$t; detalhe = $(if ($t) { 'estado: ' + [string]$t.State } else { 'tarefa não encontrada' }) } | ConvertTo-Json -Compress
""",
    verificacao="conferir que a tarefa existe no Agendador",
    desfazer=lambda p, obs, info: {"acao": "_tarefa_remover", "parametros": {"nome": p["nome"]}},
    chaves_estado=("tarefaExiste", "sha256"),
)

TAREFA_REMOVER = Acao(
    nome="_tarefa_remover",
    descricao="Remove uma tarefa criada pela IA em \\IA-Operador\\.",
    parametros={"nome": Param("string", "nome sem o prefixo IA-", regex=r"[\w\-]{1,60}")},
    observar=r"""
$t = Get-ScheduledTask -TaskPath '\IA-Operador\' -TaskName ('IA-' + (P 'NOME')) -ErrorAction SilentlyContinue
[pscustomobject]@{ existe = [bool]$t } | ConvertTo-Json -Compress
""",
    avaliar=lambda p, obs, ctx: ("R2", "remover tarefa agendada") if obs.get("existe") else _inviavel("a tarefa não existe"),
    resumo=lambda p, obs: f"Remover a tarefa \\IA-Operador\\IA-{p['nome']}",
    backup=r"""
Export-ScheduledTask -TaskPath '\IA-Operador\' -TaskName ('IA-' + (P 'NOME')) | Out-File -LiteralPath (P 'BACKUP') -Encoding utf8
'tarefa exportada para ' + (P 'BACKUP')
""",
    backup_ext=".xml",
    aplicar="Unregister-ScheduledTask -TaskPath '\\IA-Operador\\' -TaskName ('IA-' + (P 'NOME')) -Confirm:$false\n'removida'",
    verificar=r"""
$t = Get-ScheduledTask -TaskPath '\IA-Operador\' -TaskName ('IA-' + (P 'NOME')) -ErrorAction SilentlyContinue
[pscustomobject]@{ ok = (-not $t); detalhe = $(if ($t) { 'ainda existe' } else { 'removida' }) } | ConvertTo-Json -Compress
""",
    desfazer=lambda p, obs, info: {"nota": "restaure do backup: Register-ScheduledTask -TaskName IA-<nome> -TaskPath '\\IA-Operador\\' "
                                           "-Xml (Get-Content '<arquivo do backup>' -Raw)"},
    interna=True,
)

# ---------------------------------------------------------------- registro

_LER_VALOR = r"""
function Ler-Valor($k, $n) {
    $o = [ordered]@{ existeChave = (Test-Path -LiteralPath $k); existeValor = $false; valor = $null; tipo = $null }
    if ($o.existeChave) {
        $item = Get-Item -LiteralPath $k
        if ($item.GetValueNames() -contains $n) {
            $o.existeValor = $true
            $o.tipo = [string]$item.GetValueKind($n)
            $v = $item.GetValue($n, $null, 'DoNotExpandEnvironmentNames')
            if ($v -is [int]) { $v = [BitConverter]::ToUInt32([BitConverter]::GetBytes($v), 0) }
            elseif ($v -is [long]) { $v = [BitConverter]::ToUInt64([BitConverter]::GetBytes($v), 0) }
            elseif ($v -is [array]) { $v = ($v -join "`n") }
            $o.valor = [string]$v
        }
    }
    [pscustomobject]$o
}
"""
_TIPOS_REG = ("String", "ExpandString", "DWord", "QWord", "MultiString")


def _extras_registro(p, obs):
    chave = politica.normalizar_chave(p["caminho"]) or ""
    return {"CHAVE": chave, "CHAVEREG": chave.replace(":\\", "\\", 1)}


def _avaliar_registro(p, obs, ctx):
    chave = politica.normalizar_chave(p["caminho"])
    if not chave:
        return _inviavel("caminho de registro inválido: use HKCU:\\... ou HKLM:\\...")
    if obs.get("existeValor") and obs.get("tipo") not in _TIPOS_REG:
        return _inviavel(f"o valor atual é do tipo {obs.get('tipo')}: mude à mão (regedit)")
    if p["tipo"] in ("DWord", "QWord"):
        try:
            numero = int(p["valor"])
        except ValueError:
            return _inviavel("DWord e QWord precisam de número inteiro")
        if numero < 0 or numero >= (1 << (32 if p["tipo"] == "DWord" else 64)):
            return _inviavel("número fora do intervalo do tipo")
    if obs.get("existeValor") and obs.get("valor") == p["valor"] and obs.get("tipo") == p["tipo"]:
        return _inviavel("o valor já é esse")
    return politica.risco_registro(chave, p["nome"])


def _desfazer_registro(p, obs, info):
    if obs.get("existeValor"):
        return {"acao": "registro_definir",
                "parametros": {"caminho": p["caminho"], "nome": p["nome"], "valor": obs["valor"], "tipo": obs["tipo"]}}
    return {"acao": "_registro_remover_valor", "parametros": {"caminho": p["caminho"], "nome": p["nome"]},
            "nota": "a chave criada fica vazia" if not obs.get("existeChave") else ""}


_BACKUP_REGISTRO = r"""
$ErrorActionPreference = 'Continue'
if (Test-Path -LiteralPath (P 'CHAVE')) {
    reg.exe export (P 'CHAVEREG') (P 'BACKUP') /y | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'reg export falhou' }
    'chave exportada para ' + (P 'BACKUP')
} else { 'a chave não existia; nada a exportar' }
"""

REGISTRO_DEFINIR = Acao(
    nome="registro_definir",
    descricao="Cria ou muda um valor do registro em HKCU ou HKLM, com backup da chave.",
    parametros={
        "caminho": Param("string", "chave, como HKCU:\\Software\\Exemplo", maximo=300),
        "nome": Param("string", "nome do valor", regex=r"[^\\\r\n]{1,200}"),
        "valor": Param("string", "dado; MultiString usa uma linha por item", maximo=4000),
        "tipo": Param("string", "tipo do valor", enum=_TIPOS_REG),
    },
    observar=_LER_VALOR + "\nLer-Valor (P 'CHAVE') (P 'NOME') | ConvertTo-Json -Compress",
    extras=_extras_registro,
    avaliar=_avaliar_registro,
    resumo=lambda p, obs: (f"Definir {p['caminho']}\\{p['nome']} = {p['valor'][:60]} ({p['tipo']}); antes: "
                           f"{obs.get('valor') if obs.get('existeValor') else 'não existia'}"),
    ensaiar=lambda p, obs, ctx: (f"Valor atual: {obs.get('valor')!r} ({obs.get('tipo')})" if obs.get("existeValor")
                                 else "O valor não existe hoje" + ("" if obs.get("existeChave") else "; a chave será criada")),
    backup=_BACKUP_REGISTRO,
    backup_ext=".reg",
    aplicar=r"""
$k = P 'CHAVE'; $n = P 'NOME'; $tipo = P 'TIPO'; $v = P 'VALOR'
if (-not (Test-Path -LiteralPath $k)) { New-Item -Path $k -Force | Out-Null }
switch ($tipo) {
    'DWord' { $valor = [BitConverter]::ToInt32([BitConverter]::GetBytes([uint32]$v), 0) }
    'QWord' { $valor = [BitConverter]::ToInt64([BitConverter]::GetBytes([uint64]$v), 0) }
    'MultiString' { $valor = [string[]]($v -split "`n") }
    default { $valor = $v }
}
New-ItemProperty -LiteralPath $k -Name $n -Value $valor -PropertyType $tipo -Force | Out-Null
'valor gravado'
""",
    verificar=_LER_VALOR + r"""
$o = Ler-Valor (P 'CHAVE') (P 'NOME')
[pscustomobject]@{ ok = ($o.existeValor -and $o.valor -eq (P 'VALOR') -and $o.tipo -eq (P 'TIPO')); detalhe = ('lido: ' + $o.valor + ' (' + $o.tipo + ')') } | ConvertTo-Json -Compress
""",
    verificacao="ler o valor de novo e comparar",
    desfazer=_desfazer_registro,
    admin=lambda p: (politica.normalizar_chave(p["caminho"]) or "").startswith("HKLM"),
    chaves_estado=("existeValor", "valor", "tipo"),
)

REGISTRO_REMOVER_VALOR = Acao(
    nome="_registro_remover_valor",
    descricao="Remove um valor do registro (usado para desfazer).",
    parametros={"caminho": Param("string", "chave", maximo=300), "nome": Param("string", "nome do valor", regex=r"[^\\\r\n]{1,200}")},
    observar=_LER_VALOR + "\nLer-Valor (P 'CHAVE') (P 'NOME') | ConvertTo-Json -Compress",
    extras=_extras_registro,
    avaliar=lambda p, obs, ctx: (politica.risco_registro(politica.normalizar_chave(p["caminho"]) or "", p["nome"])
                                 if obs.get("existeValor") else _inviavel("o valor não existe")),
    resumo=lambda p, obs: f"Remover o valor {p['caminho']}\\{p['nome']} (hoje: {obs.get('valor')})",
    backup=_BACKUP_REGISTRO,
    backup_ext=".reg",
    aplicar="Remove-ItemProperty -LiteralPath (P 'CHAVE') -Name (P 'NOME')\n'removido'",
    verificar=_LER_VALOR + r"""
$o = Ler-Valor (P 'CHAVE') (P 'NOME')
[pscustomobject]@{ ok = (-not $o.existeValor); detalhe = $(if ($o.existeValor) { 'ainda existe' } else { 'removido' }) } | ConvertTo-Json -Compress
""",
    desfazer=lambda p, obs, info: {"acao": "registro_definir", "parametros": {"caminho": p["caminho"], "nome": p["nome"],
                                                                              "valor": obs.get("valor"), "tipo": obs.get("tipo")}},
    admin=lambda p: (politica.normalizar_chave(p["caminho"]) or "").startswith("HKLM"),
    interna=True,
    chaves_estado=("existeValor", "valor"),
)

# ---------------------------------------------------------------- arquivos e pastas

_EXTENSOES_BINARIAS = {".exe", ".dll", ".sys", ".msi", ".scr", ".com", ".cpl", ".ocx", ".drv"}
_EXTENSOES_ABRIR = {
    ".txt", ".md", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv", ".ppt", ".pptx", ".odt", ".ods", ".odp", ".rtf",
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".svg", ".mp3", ".wav", ".flac", ".mp4", ".mkv", ".avi", ".mov",
    ".log", ".json", ".xml", ".yaml", ".yml", ".ini",
}


def _obs_caminho(p, ctx, chave="caminho"):
    cam = pathlib.Path(p[chave])
    obs = {"existe": cam.exists(), "pasta": cam.is_dir(), "paiExiste": cam.parent.is_dir()}
    if cam.is_file():
        obs.update(tamanho=cam.stat().st_size, sha256=_sha256(cam))
    return obs


def _avaliar_pasta_criar(p, obs, ctx):
    if obs["existe"]:
        return _inviavel("já existe")
    return politica.risco_escrita(pathlib.Path(p["caminho"]), ctx.cfg, existe=False)


def _aplicar_pasta_criar(p, obs, ctx):
    cam = pathlib.Path(p["caminho"])
    topo = cam
    while not topo.parent.exists() and topo.parent != topo:
        topo = topo.parent
    cam.mkdir(parents=True, exist_ok=False)
    return {"texto": f"pasta criada: {cam}", "criada_desde": str(topo)}


PASTA_CRIAR = Acao(
    nome="pasta_criar",
    descricao="Cria uma pasta (e as pastas de cima que faltarem).",
    parametros={"caminho": Param("caminho", "caminho completo da pasta nova", maximo=300)},
    observar=_obs_caminho,
    avaliar=_avaliar_pasta_criar,
    resumo=lambda p, obs: f"Criar a pasta {p['caminho']}",
    aplicar=_aplicar_pasta_criar,
    verificar=lambda p, obs, info, ctx: (pathlib.Path(p["caminho"]).is_dir(), "a pasta existe"),
    verificacao="conferir que a pasta existe",
    desfazer=lambda p, obs, info: {"acao": "_pasta_remover_vazia", "parametros": {"caminho": info.get("criada_desde", p["caminho"])}},
    chaves_estado=("existe",),
)


def _obs_pasta_vazia(p, ctx):
    cam = pathlib.Path(p["caminho"])
    arquivos = sum(len(fs) for _, _, fs in os.walk(cam)) if cam.is_dir() else 0
    return {"existe": cam.is_dir(), "arquivos": arquivos}


def _aplicar_pasta_remover(p, obs, ctx):
    cam = pathlib.Path(p["caminho"])
    for raiz, _, arquivos in os.walk(cam, topdown=False):
        if arquivos:
            raise RuntimeError("apareceu arquivo na pasta; nada removido daqui para cima")
        pathlib.Path(raiz).rmdir()
    return {"texto": f"pasta vazia removida: {cam}"}


PASTA_REMOVER_VAZIA = Acao(
    nome="_pasta_remover_vazia",
    descricao="Remove uma pasta vazia (usado para desfazer pasta_criar).",
    parametros={"caminho": Param("caminho", "pasta", maximo=300)},
    observar=_obs_pasta_vazia,
    avaliar=lambda p, obs, ctx: (_inviavel("a pasta não existe") if not obs["existe"] else
                                 _inviavel("a pasta não está vazia: não removo") if obs["arquivos"] else
                                 politica.risco_escrita(pathlib.Path(p["caminho"]), ctx.cfg, existe=False)),
    resumo=lambda p, obs: f"Remover a pasta vazia {p['caminho']}",
    aplicar=_aplicar_pasta_remover,
    verificar=lambda p, obs, info, ctx: (not pathlib.Path(p["caminho"]).exists(), "a pasta não existe mais"),
    desfazer=lambda p, obs, info: {"acao": "pasta_criar", "parametros": {"caminho": p["caminho"]}},
    interna=True,
)


def _avaliar_escrever(p, obs, ctx):
    cam = pathlib.Path(p["caminho"])
    if cam.suffix.lower() in _EXTENSOES_BINARIAS:
        return "BLOQUEADO", "arquivo executável ou de sistema"
    if obs["pasta"]:
        return _inviavel("o caminho é uma pasta")
    if p["modo"] == "criar" and obs["existe"]:
        return _inviavel("o arquivo já existe: use modo substituir ou acrescentar")
    if p["modo"] != "criar" and not obs["existe"]:
        return _inviavel("o arquivo não existe: use modo criar")
    if not obs["paiExiste"]:
        return _inviavel("a pasta não existe: crie antes com pasta_criar")
    bloqueio = politica.protegido(cam, ctx.cfg, escrita=True)
    if bloqueio:
        return "BLOQUEADO", bloqueio
    risco, motivo = politica.risco_escrita(cam, ctx.cfg, existe=obs["existe"])
    if risco == "BLOQUEADO":
        return risco, motivo
    segredos = politica.achar_segredos(p["conteudo"])
    if segredos:
        return politica.maior(risco, "R2"), "o conteúdo parece ter segredo (" + ", ".join(segredos) + ")"
    return risco, motivo


def _backup_arquivo(p, obs, ctx, pasta: pathlib.Path):
    cam = pathlib.Path(p["caminho"])
    if not cam.is_file():
        return {"texto": "arquivo novo: nada a copiar"}
    pasta.mkdir(parents=True, exist_ok=True)
    destino = pasta / cam.name
    shutil.copy2(cam, destino)
    return {"texto": f"cópia em {destino}", "backup": str(destino)}


def _aplicar_escrever(p, obs, ctx):
    cam = pathlib.Path(p["caminho"])
    modo = "a" if p["modo"] == "acrescentar" else "w"
    with cam.open(modo, encoding="utf-8", newline="") as f:
        f.write(p["conteudo"])
    return {"texto": f"arquivo gravado: {cam} ({cam.stat().st_size} bytes)", "sha256": _sha256(cam), "criado": not obs["existe"]}


def _desfazer_escrever(p, obs, info):
    if info.get("criado"):
        return {"acao": "_arquivo_remover_criado", "parametros": {"caminho": p["caminho"], "sha256": info.get("sha256", "")}}
    if info.get("backup") or info.get("previsao"):
        return {"acao": "_arquivo_restaurar", "parametros": {"caminho": p["caminho"], "backup": info.get("backup", "")}}
    return {"nota": "sem backup registrado"}


ARQUIVO_ESCREVER = Acao(
    nome="arquivo_escrever",
    descricao="Cria, substitui ou acrescenta texto num arquivo (UTF-8). Substituir faz backup antes.",
    parametros={
        "caminho": Param("caminho", "caminho completo do arquivo", maximo=300),
        "conteudo": Param("string", "texto a gravar", maximo=1_000_000),
        "modo": Param("string", "criar (padrão), substituir ou acrescentar", obrigatorio=False,
                      enum=("criar", "substituir", "acrescentar"), padrao="criar"),
    },
    observar=_obs_caminho,
    avaliar=_avaliar_escrever,
    resumo=lambda p, obs: f"{p['modo'].capitalize()} o arquivo {p['caminho']} ({len(p['conteudo'])} caracteres)",
    ensaiar=lambda p, obs, ctx: ("Primeiras linhas do que será gravado:\n" + "\n".join(p["conteudo"].splitlines()[:8])),
    backup=_backup_arquivo,
    aplicar=_aplicar_escrever,
    verificar=lambda p, obs, info, ctx: (pathlib.Path(p["caminho"]).is_file() and _sha256(pathlib.Path(p["caminho"])) == info.get("sha256"),
                                         "conteúdo conferido pelo hash"),
    verificacao="reler o arquivo e comparar o hash",
    desfazer=_desfazer_escrever,
    chaves_estado=("existe", "sha256"),
)


def _avaliar_remover_criado(p, obs, ctx):
    if not obs["existe"]:
        return _inviavel("o arquivo não existe mais")
    if obs.get("sha256") != p["sha256"]:
        return _inviavel("o arquivo mudou depois que a IA o criou: não removo. Se quiser, mande para a Lixeira (arquivo_para_lixeira)")
    return "R1", "remove só o arquivo que a IA criou, sem mudanças desde então"


ARQUIVO_REMOVER_CRIADO = Acao(
    nome="_arquivo_remover_criado",
    descricao="Remove um arquivo criado pela IA, se ninguém o mudou (usado para desfazer).",
    parametros={"caminho": Param("caminho", "arquivo", maximo=300), "sha256": Param("string", "hash do que a IA gravou", regex=r"[0-9a-f]{64}")},
    observar=_obs_caminho,
    avaliar=_avaliar_remover_criado,
    resumo=lambda p, obs: f"Remover o arquivo criado pela IA {p['caminho']}",
    aplicar=lambda p, obs, ctx: (pathlib.Path(p["caminho"]).unlink(), {"texto": "arquivo removido"})[1],
    verificar=lambda p, obs, info, ctx: (not pathlib.Path(p["caminho"]).exists(), "o arquivo não existe mais"),
    desfazer=lambda p, obs, info: {"nota": "o conteúdo está no plano original; recrie com arquivo_escrever"},
    interna=True,
)


def _avaliar_restaurar(p, obs, ctx):
    backup = pathlib.Path(p["backup"])
    if not politica.dentro(backup, ctx.cfg.backups):
        return "BLOQUEADO", "o backup precisa estar na pasta de backups da IA"
    if not backup.is_file():
        return _inviavel("o arquivo de backup não existe")
    return "R2", "substitui o arquivo atual pelo backup (o atual também vai para backup)"


ARQUIVO_RESTAURAR = Acao(
    nome="_arquivo_restaurar",
    descricao="Volta um arquivo a partir do backup (usado para desfazer).",
    parametros={"caminho": Param("caminho", "arquivo", maximo=300), "backup": Param("caminho", "cópia em IA-Operador\\backups", maximo=400)},
    observar=_obs_caminho,
    avaliar=_avaliar_restaurar,
    resumo=lambda p, obs: f"Restaurar {p['caminho']} a partir de {p['backup']}",
    backup=_backup_arquivo,
    aplicar=lambda p, obs, ctx: (shutil.copy2(p["backup"], p["caminho"]), {"texto": "arquivo restaurado", "sha256": _sha256(pathlib.Path(p["backup"]))})[1],
    verificar=lambda p, obs, info, ctx: (_sha256(pathlib.Path(p["caminho"])) == info.get("sha256"), "conteúdo igual ao backup"),
    desfazer=lambda p, obs, info: ({"acao": "_arquivo_restaurar", "parametros": {"caminho": p["caminho"], "backup": info["backup"]}}
                                   if info.get("backup") else {"nota": "não havia arquivo antes da restauração"}),
    interna=True,
)


def _obs_mover(p, ctx):
    origem, destino = pathlib.Path(p["origem"]), pathlib.Path(p["destino"])
    final = destino / origem.name if destino.is_dir() else destino
    return {"origemExiste": origem.exists(), "final": str(final), "finalExiste": final.exists(), "paiExiste": final.parent.is_dir()}


def _avaliar_mover(p, obs, ctx):
    if not obs["origemExiste"]:
        return _inviavel("a origem não existe")
    if obs["finalExiste"]:
        return _inviavel(f"já existe {obs['final']}: escolha outro destino")
    if not obs["paiExiste"]:
        return _inviavel("a pasta de destino não existe: crie antes com pasta_criar")
    classes = {politica.classe_caminho(pathlib.Path(x), ctx.cfg) for x in (p["origem"], obs["final"])}
    if "sistema" in classes:
        return "BLOQUEADO", "pasta do sistema ou raiz do disco"
    motivo = (politica.protegido(pathlib.Path(p["origem"]), ctx.cfg)
              or politica.protegido(pathlib.Path(obs["final"]), ctx.cfg, escrita=True))
    if motivo:
        return "BLOQUEADO", motivo
    if classes == {"permitida"}:
        return "R1", "mover dentro das pastas permitidas"
    return "R2", "mover fora das pastas permitidas"


ARQUIVO_MOVER = Acao(
    nome="arquivo_mover",
    descricao="Move ou renomeia um arquivo ou pasta. Se o destino for uma pasta existente, move para dentro dela.",
    parametros={"origem": Param("caminho", "caminho completo atual", maximo=300),
                "destino": Param("caminho", "caminho completo novo, ou pasta de destino", maximo=300)},
    observar=_obs_mover,
    avaliar=_avaliar_mover,
    resumo=lambda p, obs: f"Mover {p['origem']} para {obs.get('final')}",
    aplicar=lambda p, obs, ctx: (shutil.move(p["origem"], obs["final"]), {"texto": f"movido para {obs['final']}"})[1],
    verificar=lambda p, obs, info, ctx: (pathlib.Path(obs["final"]).exists() and not pathlib.Path(p["origem"]).exists(), "está no destino"),
    verificacao="conferir que está no destino e saiu da origem",
    desfazer=lambda p, obs, info: {"acao": "arquivo_mover", "parametros": {"origem": obs["final"], "destino": p["origem"]}},
    chaves_estado=("origemExiste", "finalExiste"),
)


def _avaliar_lixeira(p, obs, ctx):
    cam = pathlib.Path(p["caminho"])
    if politica.classe_caminho(cam, ctx.cfg) == "sistema":
        return "BLOQUEADO", "pasta do sistema ou raiz do disco"
    if not obs.get("existe"):
        return _inviavel("não existe")
    motivo = politica.protegido(cam, ctx.cfg)
    if motivo:
        return "BLOQUEADO", motivo
    if int(obs.get("tipoDisco", 0)) != 3:
        return "R3", "disco removível ou de rede: pode apagar de vez, sem passar pela Lixeira"
    if int(obs.get("arquivos", 0)) > 1000 or int(obs.get("bytes", 0)) > 1 << 30:
        return "R3", "muita coisa de uma vez (mais de 1000 arquivos ou 1 GB); itens grandes podem não caber na Lixeira e sumir de vez"
    return "R2", "apaga dados do usuário, mas vai para a Lixeira e dá para restaurar"


ARQUIVO_PARA_LIXEIRA = Acao(
    nome="arquivo_para_lixeira",
    descricao="Manda um arquivo ou pasta para a Lixeira. Apagar de vez não existe aqui.",
    parametros={"caminho": Param("caminho", "caminho completo", maximo=300)},
    observar=r"""
$c = P 'CAMINHO'
if (-not (Test-Path -LiteralPath $c)) { '{"existe":false}' } else {
    $i = Get-Item -LiteralPath $c -Force
    if ($i.PSIsContainer) {
        $arqs = @(Get-ChildItem -LiteralPath $c -Recurse -File -Force -ErrorAction SilentlyContinue)
        $n = $arqs.Count; $bytes = [int64](($arqs | Measure-Object Length -Sum).Sum)
    } else { $n = 1; $bytes = [int64]$i.Length }
    $tipo = 0
    try { $d = Split-Path -Qualifier $i.FullName; $tipo = [int](Get-CimInstance Win32_LogicalDisk -Filter ("DeviceID='" + $d + "'")).DriveType } catch {}
    [pscustomobject]@{ existe = $true; pasta = $i.PSIsContainer; arquivos = $n; bytes = $bytes; tipoDisco = $tipo } | ConvertTo-Json -Compress
}
""",
    avaliar=_avaliar_lixeira,
    resumo=lambda p, obs: f"Mandar para a Lixeira {p['caminho']} ({obs.get('arquivos')} arquivo(s), {round(int(obs.get('bytes', 0)) / 1048576, 1)} MB)",
    aplicar=r"""
Add-Type -AssemblyName Microsoft.VisualBasic
$c = P 'CAMINHO'
if ((Get-Item -LiteralPath $c -Force).PSIsContainer) { [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory($c, 'OnlyErrorDialogs', 'SendToRecycleBin') }
else { [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile($c, 'OnlyErrorDialogs', 'SendToRecycleBin') }
'enviado para a Lixeira'
""",
    extras=lambda p, obs: {"BYTES": int(obs.get("bytes", 0) or 0), "PASTA": "1" if obs.get("pasta") else "0"},
    # Oráculo na fonte (VER-04, SEG-20): não basta ter saído do lugar; o item tem de estar na Lixeira, inteiro.
    verificar=r"""
$c = P 'CAMINHO'
$existe = Test-Path -LiteralPath $c
$nome = Split-Path -Leaf $c; $pai = Split-Path -Parent $c
$consultou = $false; $na = $false; $tam = [int64]-1
try {
    $rb = (New-Object -ComObject Shell.Application).NameSpace(10)
    $consultou = $true
    foreach ($it in @($rb.Items())) {
        if ([string]$it.ExtendedProperty('System.Recycle.DeletedFrom') -eq $pai -and [string]$it.ExtendedProperty('System.FileName') -eq $nome) { $na = $true; $tam = [int64]$it.Size; break }
    }
} catch {}
$pasta = (P 'PASTA') -eq '1'; $esperado = [int64](P 'BYTES')
$inteiro = $pasta -or ($tam -eq $esperado)
if ($existe) { $ok = $false; $d = 'ainda existe no lugar' }
elseif (-not $consultou) { $ok = $null; $d = 'saiu do lugar, mas não consegui consultar a Lixeira para conferir' }
elseif (-not $na) { $ok = $false; $d = 'saiu do lugar, mas NÃO está na Lixeira: pode ter sido apagado de vez' }
elseif (-not $inteiro) { $ok = $false; $d = "está na Lixeira, mas com tamanho diferente ($tam de $esperado bytes)" }
else { $ok = $true; $d = 'conferido na própria Lixeira: saiu do lugar e está lá' + $(if (-not $pasta) { " com os $tam bytes" } else { '' }) }
[pscustomobject]@{ ok = $ok; detalhe = $d } | ConvertTo-Json -Compress
""",
    verificacao="conferir na própria Lixeira que o item está lá e inteiro (não basta ter saído do lugar)",
    desfazer=lambda p, obs, info: {"nota": f"abra a Lixeira, clique com o botão direito em {pathlib.Path(p['caminho']).name} e escolha Restaurar"},
    chaves_estado=("arquivos", "bytes"),
)


def _obs_abrir(p, ctx):
    cam = pathlib.Path(p["caminho"])
    return {"existe": cam.exists(), "pasta": cam.is_dir(), "extensao": cam.suffix.lower()}


ARQUIVO_ABRIR = Acao(
    nome="arquivo_abrir",
    descricao="Abre um documento, imagem, vídeo ou pasta no app padrão. Não abre programa nem script.",
    parametros={"caminho": Param("caminho", "caminho completo", maximo=300)},
    observar=_obs_abrir,
    avaliar=lambda p, obs, ctx: (_inviavel("não existe") if not obs["existe"] else
                                 ("R1", "abrir no app padrão") if obs["pasta"] or obs["extensao"] in _EXTENSOES_ABRIR else
                                 ("BLOQUEADO", "abrir esse tipo de arquivo pode rodar programa ou script: abra você mesmo, se confiar")),
    resumo=lambda p, obs: f"Abrir {p['caminho']}",
    aplicar="Invoke-Item -LiteralPath (P 'CAMINHO')\n'aberto'",
    desfazer=lambda p, obs, info: {"nota": "feche a janela do app"},
)

APP_ABRIR = Acao(
    nome="app_abrir",
    descricao="Abre um app instalado pelo nome que aparece no Menu Iniciar.",
    parametros={"nome": Param("string", "nome do app, como Bloco de Notas ou Calculadora", regex=r"[^*?\[\]`]{1,80}")},
    observar=r"""
$n = P 'NOME'
$apps = @(Get-StartApps | Where-Object { $_.Name -like ('*' + $n + '*') } | Select-Object -First 15)
$exato = @($apps | Where-Object { $_.Name -ieq $n })
$escolhido = $(if ($exato.Count -ge 1) { $exato[0] } elseif ($apps.Count -eq 1) { $apps[0] } else { $null })
[pscustomobject]@{ achados = @($apps | ForEach-Object { $_.Name }); appid = $(if ($escolhido) { $escolhido.AppID } else { '' }); app = $(if ($escolhido) { $escolhido.Name } else { '' }) } | ConvertTo-Json -Compress -Depth 3
""",
    avaliar=lambda p, obs, ctx: (("R1", "abrir app do usuário") if obs.get("appid") else
                                 _inviavel("nenhum app com esse nome no Menu Iniciar") if not _lista(obs.get("achados")) else
                                 _inviavel("vários apps parecidos: " + "; ".join(_lista(obs.get("achados"))[:8]) + ". Repita com o nome exato")),
    resumo=lambda p, obs: f"Abrir o app {obs.get('app') or p['nome']}",
    extras=lambda p, obs: {"APPID": obs.get("appid", "")},
    aplicar="Start-Process ('shell:AppsFolder\\' + (P 'APPID'))\n'pedido de abertura enviado'",
    desfazer=lambda p, obs, info: {"nota": "feche o app (processo_encerrar)"},
)

# ---------------------------------------------------------------- sistema do usuário

TEMPORARIOS_LIMPAR = Acao(
    nome="temporarios_limpar",
    descricao="Apaga arquivos temporários do seu usuário (%TEMP%) mais velhos que N dias. Arquivos em uso ficam.",
    parametros={"dias": Param("integer", "idade mínima em dias", obrigatorio=False, padrao=7, minimo=1, maximo=365)},
    observar=r"""
$limite = (Get-Date).AddDays(-[int](P 'DIAS'))
$arqs = @(Get-ChildItem -LiteralPath $env:TEMP -Recurse -File -Force -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -lt $limite })
[pscustomobject]@{ pasta = $env:TEMP; arquivos = $arqs.Count; bytes = [int64](($arqs | Measure-Object Length -Sum).Sum) } | ConvertTo-Json -Compress
""",
    avaliar=lambda p, obs, ctx: (_inviavel("nada para limpar") if not int(obs.get("arquivos", 0)) else
                                 ("R2", "apaga temporários; não há como desfazer")),
    resumo=lambda p, obs: (f"Apagar {obs.get('arquivos')} temporários com mais de {p['dias']} dias "
                           f"({round(int(obs.get('bytes', 0)) / 1048576, 1)} MB) em {obs.get('pasta')}"),
    extras=lambda p, obs: {"ANTES": obs.get("arquivos", 0)},
    aplicar=r"""
$ErrorActionPreference = 'Continue'
$limite = (Get-Date).AddDays(-[int](P 'DIAS'))
$ok = 0; $falha = 0
Get-ChildItem -LiteralPath $env:TEMP -Recurse -File -Force -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -lt $limite } | ForEach-Object {
    try { Remove-Item -LiteralPath $_.FullName -Force -ErrorAction Stop; $ok++ } catch { $falha++ }
}
"apagados: $ok; em uso ou sem permissão: $falha"
""",
    verificar=r"""
$limite = (Get-Date).AddDays(-[int](P 'DIAS'))
$resta = @(Get-ChildItem -LiteralPath $env:TEMP -Recurse -File -Force -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -lt $limite }).Count
[pscustomobject]@{ ok = ($resta -lt [int](P 'ANTES')); detalhe = ('antes: ' + (P 'ANTES') + '; restam: ' + $resta + ' (em uso)') } | ConvertTo-Json -Compress
""",
    verificacao="contar de novo o que sobrou",
    desfazer=lambda p, obs, info: {"nota": "temporários apagados não voltam"},
    chaves_estado=(),
)

_PLANOS_ENERGIA = {"equilibrado": "381b4222-f694-41f0-9685-ff5bb260df2e",
                   "alto_desempenho": "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
                   "economia": "a1841308-3334-4929-9842-b5ad7d0a8b1e"}


def _guid_energia(plano: str) -> str:
    return _PLANOS_ENERGIA.get(plano.lower(), plano.lower())


ENERGIA_PLANO = Acao(
    nome="energia_plano",
    descricao="Troca o plano de energia ativo.",
    parametros={"plano": Param("string", "equilibrado, alto_desempenho, economia ou o GUID de um plano de so_estado area=energia",
                               regex=r"(?i)equilibrado|alto_desempenho|economia|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")},
    observar=r"""
$ErrorActionPreference = 'Continue'
$ativo = (powercfg /getactivescheme | Out-String)
$lista = (powercfg /list | Out-String)
[pscustomobject]@{ ativo = ([regex]::Match($ativo, '[0-9a-fA-F]{8}(-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}')).Value.ToLower(); textoAtivo = $ativo.Trim(); existe = ($lista.ToLower().Contains((P 'GUID'))) } | ConvertTo-Json -Compress
""",
    extras=lambda p, obs: {"GUID": _guid_energia(p["plano"])},
    avaliar=lambda p, obs, ctx: (_inviavel("esse plano não existe neste PC: veja so_estado area=energia") if not obs.get("existe") else
                                 _inviavel("já é o plano ativo") if obs.get("ativo") == _guid_energia(p["plano"]) else
                                 ("R2", "configuração de energia do sistema")),
    resumo=lambda p, obs: f"Trocar o plano de energia para {p['plano']} (hoje: {obs.get('textoAtivo')})",
    aplicar="powercfg /setactive (P 'GUID')\nif ($LASTEXITCODE -ne 0) { throw 'powercfg falhou' }\n'plano ativado'",
    verificar=r"""
$ErrorActionPreference = 'Continue'
$ativo = (powercfg /getactivescheme | Out-String)
[pscustomobject]@{ ok = $ativo.ToLower().Contains((P 'GUID')); detalhe = $ativo.Trim() } | ConvertTo-Json -Compress
""",
    verificacao="powercfg /getactivescheme",
    desfazer=lambda p, obs, info: {"acao": "energia_plano", "parametros": {"plano": obs.get("ativo", "")}},
    chaves_estado=("ativo",),
)

_OBS_PATH = r"""
$k = [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Environment')
$atual = [string]$k.GetValue('Path', '', 'DoNotExpandEnvironmentNames')
$k.Close()
$pasta = [string](P 'PASTA')
$partes = @($atual -split ';' | Where-Object { $_ })
[pscustomobject]@{ atual = $atual; jaTem = (@($partes | Where-Object { $_.TrimEnd('\') -ieq $pasta.TrimEnd('\') }).Count -gt 0); pastaExiste = $(if ($pasta) { Test-Path -LiteralPath $pasta -PathType Container } else { $false }) } | ConvertTo-Json -Compress
"""
_GRAVAR_PATH = r"""
$k = [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Environment', $true)
$k.SetValue('Path', $novo, [Microsoft.Win32.RegistryValueKind]::ExpandString)
$k.Close()
# Avisa os programas (WM_SETTINGCHANGE): a API do .NET avisa ao criar e apagar uma variável.
[Environment]::SetEnvironmentVariable('IA_OPERADOR_AVISO', '1', 'User')
[Environment]::SetEnvironmentVariable('IA_OPERADOR_AVISO', $null, 'User')
'PATH do usuário gravado; abra um terminal novo para usar'
"""


def _backup_path(p, obs, ctx, pasta: pathlib.Path):
    pasta.mkdir(parents=True, exist_ok=True)
    destino = pasta / "path-usuario.txt"
    destino.write_text(obs.get("atual", ""), encoding="utf-8")
    return {"texto": f"PATH anterior salvo em {destino}", "backup": str(destino)}


PATH_USUARIO_ADICIONAR = Acao(
    nome="path_usuario_adicionar",
    descricao="Acrescenta uma pasta ao PATH do seu usuário, sem duplicar e sem mexer no resto.",
    parametros={"pasta": Param("caminho", "pasta que já existe", maximo=300)},
    observar=_OBS_PATH,
    avaliar=lambda p, obs, ctx: (_inviavel("a pasta não existe") if not obs.get("pastaExiste") else
                                 _inviavel("a pasta já está no PATH do usuário") if obs.get("jaTem") else
                                 ("R1", "preferência do próprio usuário, com o valor anterior anotado")),
    resumo=lambda p, obs: f"Acrescentar {p['pasta']} ao PATH do usuário",
    backup=_backup_path,
    aplicar=r"""
$k = [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Environment')
$atual = [string]$k.GetValue('Path', '', 'DoNotExpandEnvironmentNames')
$k.Close()
$novo = ((@($atual -split ';' | Where-Object { $_ }) + (P 'PASTA')) -join ';')
""" + _GRAVAR_PATH,
    verificar=r"""
$k = [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Environment')
$atual = [string]$k.GetValue('Path', '', 'DoNotExpandEnvironmentNames')
$k.Close()
$pasta = (P 'PASTA')
$tem = (@($atual -split ';' | Where-Object { $_.TrimEnd('\') -ieq $pasta.TrimEnd('\') }).Count -gt 0)
[pscustomobject]@{ ok = $tem; detalhe = $(if ($tem) { 'a pasta está no PATH do usuário' } else { 'a pasta não aparece no PATH' }) } | ConvertTo-Json -Compress
""",
    verificacao="reler o PATH do usuário",
    desfazer=lambda p, obs, info: {"acao": "_path_usuario_definir", "parametros": {"valor": obs.get("atual", "")}},
    chaves_estado=("atual",),
)

PATH_USUARIO_DEFINIR = Acao(
    nome="_path_usuario_definir",
    descricao="Grava o PATH do usuário inteiro (usado para desfazer).",
    parametros={"valor": Param("string", "PATH completo", maximo=8000)},
    observar=_OBS_PATH,
    extras=lambda p, obs: {"PASTA": ""},
    avaliar=lambda p, obs, ctx: _inviavel("o PATH já é esse") if obs.get("atual") == p["valor"] else ("R1", "volta o PATH do usuário ao valor anotado"),
    resumo=lambda p, obs: "Voltar o PATH do usuário ao valor anterior",
    backup=_backup_path,
    aplicar="$novo = (P 'VALOR')\n" + _GRAVAR_PATH,
    verificar=r"""
$k = [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Environment')
$atual = [string]$k.GetValue('Path', '', 'DoNotExpandEnvironmentNames')
$k.Close()
[pscustomobject]@{ ok = ($atual -eq (P 'VALOR')); detalhe = 'PATH relido' } | ConvertTo-Json -Compress
""",
    desfazer=lambda p, obs, info: {"acao": "_path_usuario_definir", "parametros": {"valor": obs.get("atual", "")}},
    interna=True,
)


def _nome_regra(p) -> str:
    return f"IA-Operador - {p['acao']} {p['direcao']} - {pathlib.PureWindowsPath(p['programa']).name}"


def _avaliar_firewall(p, obs, ctx):
    if not p["programa"].lower().endswith(".exe"):
        return _inviavel("o programa precisa ser um .exe")
    if not obs.get("programaExiste"):
        return _inviavel("o programa não existe nesse caminho")
    if obs.get("regraExiste"):
        return _inviavel("já existe uma regra com esse nome")
    if p["acao"] == "permitir":
        return "R3", "abre exceção no firewall: reduz a segurança"
    return "R2", "regra de firewall, exige administrador"


FIREWALL_REGRA = Acao(
    nome="firewall_regra",
    descricao="Cria uma regra de firewall para um programa: bloquear (R2) ou permitir (R3).",
    parametros={
        "programa": Param("caminho", "caminho completo do .exe", maximo=300),
        "acao": Param("string", "bloquear ou permitir", enum=("bloquear", "permitir")),
        "direcao": Param("string", "entrada (padrão) ou saida", obrigatorio=False, enum=("entrada", "saida"), padrao="entrada"),
    },
    observar=r"""
$existe = Test-Path -LiteralPath (P 'PROGRAMA') -PathType Leaf
$regra = Get-NetFirewallRule -DisplayName (P 'NOMEREGRA') -ErrorAction SilentlyContinue
[pscustomobject]@{ programaExiste = $existe; regraExiste = [bool]$regra } | ConvertTo-Json -Compress
""",
    extras=lambda p, obs: {"NOMEREGRA": _nome_regra(p), "DIRECAO_PS": "Inbound" if p["direcao"] == "entrada" else "Outbound",
                           "ACAO_PS": "Block" if p["acao"] == "bloquear" else "Allow"},
    avaliar=_avaliar_firewall,
    resumo=lambda p, obs: f"Firewall: {p['acao']} {p['direcao']} para {p['programa']}",
    ensaiar="New-NetFirewallRule -DisplayName (P 'NOMEREGRA') -Direction (P 'DIRECAO_PS') -Program (P 'PROGRAMA') -Action (P 'ACAO_PS') -Profile Any -WhatIf",
    aplicar="New-NetFirewallRule -DisplayName (P 'NOMEREGRA') -Direction (P 'DIRECAO_PS') -Program (P 'PROGRAMA') -Action (P 'ACAO_PS') -Profile Any | Out-Null\n'regra criada'",
    verificar=r"""
$r = Get-NetFirewallRule -DisplayName (P 'NOMEREGRA') -ErrorAction SilentlyContinue
[pscustomobject]@{ ok = ([bool]$r -and [string]$r.Enabled -eq 'True'); detalhe = $(if ($r) { 'regra ativa: ' + (P 'NOMEREGRA') } else { 'regra não encontrada' }) } | ConvertTo-Json -Compress
""",
    verificacao="Get-NetFirewallRule pelo nome da regra",
    desfazer=lambda p, obs, info: {"acao": "_firewall_remover_regra", "parametros": {"nome": _nome_regra(p)}},
    admin=True,
    chaves_estado=("regraExiste",),
)

FIREWALL_REMOVER_REGRA = Acao(
    nome="_firewall_remover_regra",
    descricao="Remove uma regra de firewall criada pela IA (usado para desfazer).",
    parametros={"nome": Param("string", "nome da regra, começa com IA-Operador - ", regex=r"IA-Operador - [^\r\n]{1,200}")},
    observar="$r = Get-NetFirewallRule -DisplayName (P 'NOME') -ErrorAction SilentlyContinue\n[pscustomobject]@{ existe = [bool]$r } | ConvertTo-Json -Compress",
    avaliar=lambda p, obs, ctx: ("R2", "regra de firewall, exige administrador") if obs.get("existe") else _inviavel("a regra não existe"),
    resumo=lambda p, obs: f"Remover a regra de firewall {p['nome']}",
    aplicar="Remove-NetFirewallRule -DisplayName (P 'NOME')\n'regra removida'",
    verificar=r"""
$r = Get-NetFirewallRule -DisplayName (P 'NOME') -ErrorAction SilentlyContinue
[pscustomobject]@{ ok = (-not $r); detalhe = $(if ($r) { 'ainda existe' } else { 'removida' }) } | ConvertTo-Json -Compress
""",
    desfazer=lambda p, obs, info: {"nota": "recrie com firewall_regra"},
    admin=True,
    interna=True,
)

# ---------------------------------------------------------------- comandos do dia a dia (voz)

TELA_BLOQUEAR = Acao(
    nome="tela_bloquear",
    descricao="Bloqueia a tela.",
    parametros={"motivo": Param("string", "por que bloquear (opcional)", obrigatorio=False, padrao="pedido do usuário",
                                regex=r"[^`$;|&<>]{1,80}")},
    avaliar=lambda p, obs, ctx: ("R1", "só bloqueia a tela; os programas continuam abertos"),
    resumo=lambda p, obs: "Bloquear a tela",
    aplicar="rundll32.exe user32.dll,LockWorkStation\n'pedido de bloqueio enviado'",
    verificar=r"""
Start-Sleep -Seconds 2
$tela = @(Get-Process LogonUI -ErrorAction SilentlyContinue).Count -gt 0
[pscustomobject]@{ ok = $(if ($tela) { $true } else { $null }); detalhe = $(if ($tela) { 'a tela de bloqueio está aberta' } else { 'não vi a tela de bloqueio; confira no monitor' }) } | ConvertTo-Json -Compress
""",
    verificacao="ver se a tela de bloqueio (LogonUI) abriu",
    desfazer=lambda p, obs, info: {"nota": "entre com a sua senha ou PIN"},
)


def _avaliar_desligamento(p, obs, ctx):
    if int(p["minutos"]) < 5:
        return "R3", "menos de 5 minutos para salvar o trabalho ou cancelar"
    return "R2", "desliga ou reinicia o PC; dá para cancelar até a hora com desligamento_cancelar"


DESLIGAMENTO_AGENDAR = Acao(
    nome="desligamento_agendar",
    descricao="Desliga/reinicia em N min.",
    parametros={"acao": Param("string", "desligar ou reiniciar", enum=("desligar", "reiniciar")),
                "minutos": Param("integer", "daqui a quantos minutos", obrigatorio=False, padrao=10, minimo=1, maximo=240)},
    avaliar=_avaliar_desligamento,
    resumo=lambda p, obs: f"{'Desligar' if p['acao'] == 'desligar' else 'Reiniciar'} o PC daqui a {p['minutos']} minuto(s)",
    extras=lambda p, obs: {"SEGUNDOS": int(p.get("minutos", 10)) * 60, "FLAG": "/r" if p.get("acao") == "reiniciar" else "/s"},
    aplicar=r"""
$ErrorActionPreference = 'Continue'
shutdown.exe (P 'FLAG') /t (P 'SEGUNDOS') /c 'Agendado pela IA local a seu pedido. Para cancelar: diga cancela o desligamento.'
if ($LASTEXITCODE -eq 1190) { throw 'já existe um desligamento agendado: cancele antes com desligamento_cancelar' }
if ($LASTEXITCODE -ne 0) { throw ('shutdown falhou: código ' + $LASTEXITCODE) }
'agendado'
""",
    # O Windows não grava evento ao agendar (o 1074 só sai no desligamento real; o 1075, ao cancelar) e não há como
    # ler um agendamento pendente sem cancelá-lo: a conferência honesta é Parcial (VER-10), nunca um Verificado inventado.
    verificar=lambda p, obs, info, ctx: (None, "o Windows aceitou o agendamento (shutdown.exe devolveu 0) e mostra o "
                                               "aviso na tela; um agendamento pendente não dá para ler sem cancelar"),
    verificacao="o Windows aceita ou recusa; o aviso aparece na tela",
    desfazer=lambda p, obs, info: {"acao": "desligamento_cancelar", "parametros": {}},
)

DESLIGAMENTO_CANCELAR = Acao(
    nome="desligamento_cancelar",
    descricao="Cancela desligamento agendado.",
    parametros={"motivo": Param("string", "por que cancelar (opcional)", obrigatorio=False, padrao="pedido do usuário",
                                regex=r"[^`$;|&<>]{1,80}")},
    avaliar=lambda p, obs, ctx: ("R1", "só cancela o agendamento"),
    resumo=lambda p, obs: "Cancelar o desligamento ou reinício agendado",
    aplicar=r"""
$ErrorActionPreference = 'Continue'
shutdown.exe /a 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) { 'cancelado' } elseif ($LASTEXITCODE -eq 1116) { 'não havia desligamento agendado' } else { throw ('shutdown /a falhou: código ' + $LASTEXITCODE) }
""",
    verificar=lambda p, obs, info, ctx: ("cancelado" in info.get("texto", "") or "não havia" in info.get("texto", ""),
                                          info.get("texto", "")),
    verificacao="o próprio Windows responde se havia algo para cancelar",
    desfazer=lambda p, obs, info: {"nota": "se quiser de novo, agende outra vez com desligamento_agendar"},
)

_TEMA = r"""
$k = Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize' -ErrorAction SilentlyContinue
$apps = $(if ($k -and $null -ne $k.AppsUseLightTheme) { [int]$k.AppsUseLightTheme } else { 1 })
$sis = $(if ($k -and $null -ne $k.SystemUsesLightTheme) { [int]$k.SystemUsesLightTheme } else { 1 })
"""

TEMA_DEFINIR = Acao(
    nome="tema_definir",
    descricao="Tema claro ou escuro.",
    parametros={"modo": Param("string", "claro ou escuro", enum=("claro", "escuro"))},
    observar=_TEMA + "[pscustomobject]@{ apps = $apps; sistema = $sis } | ConvertTo-Json -Compress\n",
    avaliar=lambda p, obs, ctx: (_inviavel(f"já está no tema {p['modo']}")
                                 if int(obs.get("apps", 1)) == int(obs.get("sistema", 1)) == (1 if p["modo"] == "claro" else 0)
                                 else ("R1", "preferência visual do usuário; dá para voltar")),
    resumo=lambda p, obs: f"Mudar o tema do Windows para {p['modo']}",
    extras=lambda p, obs: {"VALOR": 1 if p.get("modo") == "claro" else 0},
    aplicar=r"""
$k = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize'
if (-not (Test-Path $k)) { New-Item -Path $k -Force | Out-Null }
New-ItemProperty -Path $k -Name AppsUseLightTheme -Value ([int](P 'VALOR')) -PropertyType DWord -Force | Out-Null
New-ItemProperty -Path $k -Name SystemUsesLightTheme -Value ([int](P 'VALOR')) -PropertyType DWord -Force | Out-Null
try {
    Add-Type -Namespace IaSo -Name Tema -MemberDefinition '[DllImport("user32.dll", CharSet = CharSet.Unicode)] public static extern System.IntPtr SendMessageTimeout(System.IntPtr h, uint m, System.UIntPtr w, string l, uint f, uint t, out System.UIntPtr r);'
    $r = [System.UIntPtr]::Zero; [IaSo.Tema]::SendMessageTimeout([System.IntPtr]0xffff, 0x1A, [System.UIntPtr]::Zero, 'ImmersiveColorSet', 2, 3000, [ref]$r) | Out-Null
} catch {}
'tema aplicado'
""",
    verificar=_TEMA + "[pscustomobject]@{ ok = ($apps -eq [int](P 'VALOR') -and $sis -eq [int](P 'VALOR')); detalhe = ('apps: ' + $apps + '; sistema: ' + $sis + ' (1 = claro, 0 = escuro)') } | ConvertTo-Json -Compress\n",
    verificacao="ler de novo o registro do tema",
    desfazer=lambda p, obs, info: {"acao": "tema_definir",
                                   "parametros": {"modo": "claro" if int(obs.get("apps", 1) or 0) == 1 else "escuro"}},
    chaves_estado=("apps", "sistema"),
)

_WIFI = r"""
$a = Get-NetAdapter -ErrorAction SilentlyContinue | Where-Object { $_.PhysicalMediaType -match '802\.11' -or $_.InterfaceDescription -match 'Wi-?Fi|Wireless' } | Select-Object -First 1
"""

WIFI_DEFINIR = Acao(
    nome="wifi_definir",
    descricao="Liga/desliga o Wi-Fi.",
    parametros={"estado": Param("string", "ligar ou desligar", enum=("ligar", "desligar"))},
    observar=_WIFI + "[pscustomobject]@{ existe = [bool]$a; nome = $(if ($a) { $a.Name } else { '' }); status = $(if ($a) { [string]$a.Status } else { '' }) } | ConvertTo-Json -Compress\n",
    avaliar=lambda p, obs, ctx: (_inviavel("não há adaptador Wi-Fi neste PC") if not obs.get("existe") else
                                 _inviavel("o Wi-Fi já está desligado") if p["estado"] == "desligar" and obs.get("status") == "Disabled" else
                                 _inviavel("o Wi-Fi já está ligado") if p["estado"] == "ligar" and obs.get("status") != "Disabled" else
                                 ("R2", "corta a rede sem fio até ligar de novo") if p["estado"] == "desligar" else
                                 ("R2", "liga o adaptador de rede (precisa de administrador)")),
    resumo=lambda p, obs: f"{'Desligar' if p['estado'] == 'desligar' else 'Ligar'} o Wi-Fi ({obs.get('nome')})",
    extras=lambda p, obs: {"ADAPTADOR": obs.get("nome", "")},
    admin=True,
    aplicar=r"""
if ((P 'ESTADO') -eq 'desligar') { Disable-NetAdapter -Name (P 'ADAPTADOR') -Confirm:$false } else { Enable-NetAdapter -Name (P 'ADAPTADOR') -Confirm:$false }
'pedido aplicado'
""",
    verificar=r"""
Start-Sleep -Seconds 2
$s = [string](Get-NetAdapter -Name (P 'ADAPTADOR') -ErrorAction SilentlyContinue).Status
$ok = $(if ((P 'ESTADO') -eq 'desligar') { $s -eq 'Disabled' } else { $s -ne 'Disabled' -and $s -ne '' })
[pscustomobject]@{ ok = $ok; detalhe = ('estado do adaptador agora: ' + $s) } | ConvertTo-Json -Compress
""",
    verificacao="ler o estado do adaptador",
    desfazer=lambda p, obs, info: {"acao": "wifi_definir", "parametros": {"estado": "ligar" if p.get("estado") == "desligar" else "desligar"}},
    chaves_estado=("status",),
)

_NOTIF = r"""
$k = Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\PushNotifications' -ErrorAction SilentlyContinue
$v = $(if ($k -and $null -ne $k.ToastEnabled) { [int]$k.ToastEnabled } else { 1 })
"""

NOTIFICACOES_DEFINIR = Acao(
    nome="notificacoes_definir",
    descricao="Liga/desliga notificações.",
    parametros={"estado": Param("string", "ligar ou desligar", enum=("ligar", "desligar"))},
    observar=_NOTIF + "[pscustomobject]@{ ligadas = $v } | ConvertTo-Json -Compress\n",
    avaliar=lambda p, obs, ctx: (_inviavel(f"as notificações já estão {'ligadas' if p['estado'] == 'ligar' else 'desligadas'}")
                                 if int(obs.get("ligadas", 1)) == (1 if p["estado"] == "ligar" else 0)
                                 else ("R1", "preferência do usuário; dá para voltar")),
    resumo=lambda p, obs: f"{'Ligar' if p['estado'] == 'ligar' else 'Desligar'} as notificações do Windows",
    extras=lambda p, obs: {"VALOR": 1 if p.get("estado") == "ligar" else 0},
    aplicar=r"""
$k = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\PushNotifications'
if (-not (Test-Path $k)) { New-Item -Path $k -Force | Out-Null }
New-ItemProperty -Path $k -Name ToastEnabled -Value ([int](P 'VALOR')) -PropertyType DWord -Force | Out-Null
'gravado'
""",
    verificar=_NOTIF + "[pscustomobject]@{ ok = ($v -eq [int](P 'VALOR')); detalhe = ('notificações: ' + $(if ($v -eq 1) { 'ligadas' } else { 'desligadas' }) + '; alguns apps só respeitam depois de reabertos') } | ConvertTo-Json -Compress\n",
    verificacao="ler de novo o registro das notificações",
    desfazer=lambda p, obs, info: {"acao": "notificacoes_definir",
                                   "parametros": {"estado": "ligar" if int(obs.get("ligadas", 1) or 0) == 1 else "desligar"}},
    chaves_estado=("ligadas",),
)


def _verificar_captura(p, obs, info, ctx):
    arq = pathlib.Path(info.get("texto", "").strip())
    ok = arq.is_file() and arq.stat().st_size > 1000
    return ok, (f"imagem salva: {arq} ({arq.stat().st_size // 1024} KB)" if ok else "a imagem não foi salva")


CAPTURA_TELA = Acao(
    nome="captura_tela",
    descricao="Print da tela.",
    parametros={"nome": Param("string", "nome curto do arquivo (opcional)", obrigatorio=False, padrao="captura",
                              regex=r"[\w-]{1,40}")},
    avaliar=lambda p, obs, ctx: ("R1", "salva uma imagem nas suas Imagens; nada sai do PC"),
    resumo=lambda p, obs: "Tirar um print da tela inteira",
    aplicar=r"""
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
try { Add-Type -Namespace IaSo -Name Dpi -MemberDefinition '[DllImport("user32.dll")] public static extern bool SetProcessDPIAware();'; [IaSo.Dpi]::SetProcessDPIAware() | Out-Null } catch {}
$b = [System.Windows.Forms.SystemInformation]::VirtualScreen
$bmp = New-Object System.Drawing.Bitmap $b.Width, $b.Height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($b.Left, $b.Top, 0, 0, $bmp.Size)
$pasta = Join-Path ([Environment]::GetFolderPath('MyPictures')) 'Wed\Capturas'
New-Item -ItemType Directory -Path $pasta -Force | Out-Null
$arq = Join-Path $pasta ((P 'NOME') + '-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '.png')
$bmp.Save($arq, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()
$arq
""",
    verificar=_verificar_captura,
    verificacao="conferir que o arquivo PNG existe e não está vazio",
    desfazer=lambda p, obs, info: {"nota": "se não quiser a imagem, mande para a Lixeira com arquivo_para_lixeira"},
)

# ---------------------------------------------------------------- ponto de retorno (SEG-24 do guia)

PONTO_RESTAURACAO_CRIAR = Acao(
    nome="ponto_restauracao_criar",
    descricao="Ponto de restauração.",
    parametros={"descricao": Param("string", "nome curto do ponto", obrigatorio=False, padrao="IA-Operador",
                                   regex=r"[\w .,:()-]{1,60}")},
    observar=r"""
$u = $null
try { $u = Get-ComputerRestorePoint -ErrorAction Stop | Sort-Object SequenceNumber | Select-Object -Last 1 } catch {}
$q = ''
if ($u) { $q = ([Management.ManagementDateTimeConverter]::ToDateTime($u.CreationTime)).ToString('s') }
[pscustomobject]@{ lido = [bool]$u; ultimo = $q } | ConvertTo-Json -Compress
""",
    avaliar=lambda p, obs, ctx: ("R1", "cria um ponto de retorno; não muda arquivos nem configurações"),
    resumo=lambda p, obs: f"Criar o ponto de restauração '{p['descricao']}'",
    aplicar=r"""
try { Checkpoint-Computer -Description (P 'DESCRICAO') -RestorePointType MODIFY_SETTINGS -WarningAction Stop -ErrorAction Stop; 'ponto de restauração criado' }
catch { if ($_.Exception.Message -match '1440') { 'já existe um ponto de restauração das últimas 24 h' } else { throw } }
""",
    verificar=r"""
$u = $null
try { $u = Get-ComputerRestorePoint -ErrorAction Stop | Sort-Object SequenceNumber | Select-Object -Last 1 } catch {}
if (-not $u) { [pscustomobject]@{ ok = $null; detalhe = 'não consegui ler os pontos de restauração (precisa de administrador ou a Proteção do Sistema está desligada)' } | ConvertTo-Json -Compress; return }
$quando = [Management.ManagementDateTimeConverter]::ToDateTime($u.CreationTime)
$horas = ((Get-Date) - $quando).TotalHours
[pscustomobject]@{ ok = ($horas -lt 24); detalhe = ('ponto mais recente: ' + $u.Description + ' em ' + $quando.ToString('dd/MM/yyyy HH:mm') + $(if ($horas -lt 24) { '' } else { ' (mais de 24 h: a Proteção do Sistema pode estar desligada)' })) } | ConvertTo-Json -Compress
""",
    verificacao="ler o ponto de restauração mais recente",
    desfazer=lambda p, obs, info: {"nota": "o Windows apaga pontos antigos sozinho; não há o que desfazer"},
    admin=True,
    timeout_s=300,
    chaves_estado=(),
)

# ---------------------------------------------------------------- índice

TODAS = [
    APP_ABRIR, ARQUIVO_ABRIR, ARQUIVO_ESCREVER, ARQUIVO_MOVER, ARQUIVO_PARA_LIXEIRA, PASTA_CRIAR,
    PROCESSO_ENCERRAR, SERVICO_CONFIGURAR_INICIO, SERVICO_REINICIAR, PROGRAMA_INSTALAR, PROGRAMA_ATUALIZAR,
    PROGRAMA_REMOVER, TAREFA_CRIAR, TAREFA_ATIVAR, REGISTRO_DEFINIR, PATH_USUARIO_ADICIONAR, ENERGIA_PLANO,
    TEMPORARIOS_LIMPAR, FIREWALL_REGRA, PONTO_RESTAURACAO_CRIAR,
    TELA_BLOQUEAR, DESLIGAMENTO_AGENDAR, DESLIGAMENTO_CANCELAR, TEMA_DEFINIR, WIFI_DEFINIR,
    NOTIFICACOES_DEFINIR, CAPTURA_TELA,
    TAREFA_REMOVER, REGISTRO_REMOVER_VALOR, PASTA_REMOVER_VAZIA, ARQUIVO_REMOVER_CRIADO, ARQUIVO_RESTAURAR,
    PATH_USUARIO_DEFINIR, FIREWALL_REMOVER_REGRA,
]
ACOES = {a.nome: a for a in TODAS}
PUBLICAS = [a for a in TODAS if not a.interna]
