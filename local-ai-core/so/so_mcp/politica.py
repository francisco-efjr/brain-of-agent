"""Política determinística: segredos, caminhos, registro, processos, serviços e consultas só de leitura.

Tudo aqui é regra fixa, testável e independente do modelo. As classes seguem o core:
R0 leitura, R1 pequeno e reversível no escopo do usuário, R2 sistema ou administrador,
R3 destrutivo ou reduz segurança. BLOQUEADO: o servidor não faz; o usuário faz se quiser.
"""
from __future__ import annotations

import os
import pathlib
import re

ORDEM = {"R0": 0, "R1": 1, "R2": 2, "R3": 3}


def maior(*classes: str) -> str:
    return max(classes, key=lambda c: ORDEM.get(c, 99))


# ---------------------------------------------------------------- segredos

_SEGREDOS = [
    ("chave privada", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?(?:-----END [A-Z ]*PRIVATE KEY-----|$)")),
    ("token do GitHub", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b")),
    ("chave da AWS", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("chave de API", re.compile(r"\bsk-(?:proj-|ant-)?[A-Za-z0-9_\-]{20,}\b")),
    ("token do Slack", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("chave do Google", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("senha ou token", re.compile(
        r"(?i)\b(?:senha|password|passwd|pwd|secret|segredo|token|api[_-]?key|client[_-]?secret)\b\s*[:=]\s*[\"']?[^\s\"']{4,}")),
]
_CARTAO = re.compile(r"\b(?:\d[ -]?){13,19}\b")


def _luhn(digitos: str) -> bool:
    soma, dobrar = 0, False
    for d in reversed(digitos):
        n = int(d)
        if dobrar:
            n = n * 2 - 9 if n > 4 else n * 2
        soma += n
        dobrar = not dobrar
    return soma % 10 == 0


def achar_segredos(texto: str) -> list[str]:
    achados = [nome for nome, regex in _SEGREDOS if regex.search(texto)]
    for m in _CARTAO.finditer(texto):
        digitos = re.sub(r"\D", "", m.group(0))
        if 13 <= len(digitos) <= 19 and _luhn(digitos):
            achados.append("número de cartão")
            break
    return achados


def mascarar_segredos(texto: str) -> str:
    for _, regex in _SEGREDOS:
        texto = regex.sub("[SEGREDO OMITIDO]", texto)

    def cartao(m: re.Match[str]) -> str:
        digitos = re.sub(r"\D", "", m.group(0))
        return "[CARTÃO OMITIDO]" if 13 <= len(digitos) <= 19 and _luhn(digitos) else m.group(0)

    return _CARTAO.sub(cartao, texto)


ARQUIVOS_SEGREDO = re.compile(
    r"(?i)^(?:id_(?:rsa|dsa|ecdsa|ed25519)(?:\.pub)?|.*\.(?:pem|key|pfx|p12|ppk|kdbx|kdb|keychain)|\.env(?:\..*)?"
    r"|login data|cookies|web data|local state|\.git-credentials|\.netrc|_netrc|wallet\.dat|credentials(?:\..*)?"
    r"|ntuser\.dat|sam|security|system)$"
)


def arquivo_de_segredo(caminho: pathlib.Path) -> bool:
    if caminho.name.lower().endswith(".pub"):
        return False
    return bool(ARQUIVOS_SEGREDO.match(caminho.name))


# ---------------------------------------------------------------- injeção em texto guardado

_INJECAO = re.compile(
    r"(?i)(ignore (?:as |todas as )?(?:instru[cç][oõ]es|regras)|ignore (?:all |the )?previous|"
    r"disregard (?:all|previous)|system prompt|prompt de sistema|voc[eê] (?:agora )?(?:deve|precisa) sempre|"
    r"a partir de agora,? (?:voc[eê]|sempre)|from now on|new instructions|novas instru[cç][oõ]es|"
    r"execute (?:o|este) comando|run this command|confirme? automaticamente)"
)


def parece_injecao(texto: str) -> bool:
    return bool(_INJECAO.search(texto))


# ---------------------------------------------------------------- caminhos


def _norm(p: pathlib.Path) -> str:
    try:
        resolvido = p.expanduser().resolve(strict=False)
    except (OSError, RuntimeError):
        resolvido = pathlib.Path(os.path.abspath(p))
    return os.path.normcase(str(resolvido))


def dentro(p: pathlib.Path, pasta: pathlib.Path) -> bool:
    a, b = _norm(p), _norm(pasta)
    try:
        return os.path.commonpath([a, b]) == b
    except ValueError:
        return False


def classe_caminho(p: pathlib.Path, cfg) -> str:
    """sistema (bloqueado para escrita), permitida, perfil (resto do perfil do usuário) ou fora."""
    n = _norm(p)
    if n == os.path.normcase(str(pathlib.Path(n).anchor)) or any(dentro(p, s) for s in cfg.pastas_sistema):
        return "sistema"
    if any(dentro(p, a) for a in cfg.pastas_permitidas):
        return "permitida"
    if dentro(p, cfg.perfil_usuario):
        return "perfil"
    return "fora"


def caminho_sensivel(p: pathlib.Path) -> str | None:
    """Lugares em que um arquivo novo muda o comportamento do sistema."""
    t = _norm(p).replace("\\", "/").lower()
    if "/start menu/programs/startup" in t:
        return "pasta de inicialização (o arquivo roda sozinho ao entrar)"
    if "/.ssh" in t:
        return "pasta .ssh (chaves e acessos)"
    if "/windowspowershell/" in t and t.endswith("profile.ps1"):
        return "perfil do PowerShell (roda em todo terminal)"
    return None


def risco_escrita(p: pathlib.Path, cfg, existe: bool) -> tuple[str, str]:
    classe = classe_caminho(p, cfg)
    if classe == "sistema":
        return "BLOQUEADO", "pasta do sistema ou raiz do disco: faça você mesmo, se for o caso"
    sensivel = caminho_sensivel(p)
    if sensivel:
        return "R2", sensivel
    if classe == "permitida" and not existe:
        return "R1", "arquivo ou pasta nova numa pasta permitida"
    if classe == "permitida":
        return "R2", "substitui algo que já existe (com backup)"
    return "R2", "fora das pastas permitidas"


# ---------------------------------------------------------------- registro

_HIVES = {
    "HKCU": "HKCU", "HKEY_CURRENT_USER": "HKCU",
    "HKLM": "HKLM", "HKEY_LOCAL_MACHINE": "HKLM",
}
_REG_R3 = (
    "\\policies\\microsoft\\windows defender", "\\microsoft\\windows defender", "\\currentversion\\policies\\system",
    "\\control\\lsa", "\\policies\\microsoft\\windows\\windowsupdate", "\\microsoft\\powershell\\",
    "\\currentversion\\winlogon", "\\image file execution options", "\\control\\deviceguard", "\\control\\ci",
    "\\control\\securityproviders", "\\policies\\microsoft\\windowsfirewall", "\\currentcontrolset\\services\\",
    "\\policies\\microsoft\\windows\\system", "\\control\\terminal server",
)
_REG_NOMES_R3 = {
    "enablesmartscreen", "smartscreenenabled", "enablelua", "consentpromptbehavioradmin",
    "promptonsecuredesktop", "executionpolicy", "disableantispyware", "disablerealtimemonitoring",
}


def normalizar_chave(texto: str) -> str | None:
    t = texto.strip().strip('"').replace("/", "\\")
    hive, _, resto = t.partition("\\")
    hive = _HIVES.get(hive.rstrip(":").upper())
    if not hive or not resto.strip("\\"):
        return None
    return f"{hive}:\\{resto.strip(chr(92))}"


def risco_registro(chave: str, nome: str) -> tuple[str, str]:
    baixa = chave.lower() + "\\"
    if nome.lower() in _REG_NOMES_R3 or any(p in baixa for p in _REG_R3):
        return "R3", "chave ligada a proteção, login ou serviços do Windows"
    if "\\currentversion\\run" in baixa:
        return "R2", "programa que inicia sozinho"
    if chave.startswith("HKLM"):
        return "R2", "registro da máquina (HKLM), exige administrador"
    return "R1", "preferência do próprio usuário (HKCU), com o valor anterior anotado"


# ---------------------------------------------------------------- processos e serviços

PROCESSOS_CRITICOS = {
    "system", "idle", "registry", "smss", "csrss", "wininit", "winlogon", "services", "lsass", "lsaiso",
    "svchost", "fontdrvhost", "memory compression", "secure system", "msmpeng", "nissrv", "securityhealthservice",
    "dwm", "sihost", "ctfmon", "spoolsv", "wudfhost", "conhost",
}
SERVICOS_BLOQUEADOS = {
    "rpcss", "dcomlaunch", "rpceptmapper", "lsm", "samss", "gpsvc", "brokerinfrastructure", "coremessagingregistrar",
    "power", "systemeventsbroker", "trustedinstaller", "eventlog", "winmgmt", "profsvc", "usermanager", "schedule",
}
SERVICOS_PROTEGIDOS = {
    "windefend", "wdnissvc", "sense", "securityhealthservice", "wscsvc", "mpssvc", "bfe", "wuauserv", "usosvc",
    "waasmedicsvc", "cryptsvc", "bits", "dhcp", "dnscache", "nsi", "appidsvc", "wdfilter", "wdboot", "vaultsvc",
}


# ---------------------------------------------------------------- consultas só de leitura (so_consultar)

VERBOS_LEITURA = {
    "get", "test", "measure", "select", "where", "sort", "format", "group", "foreach", "compare", "resolve",
    "convertto", "convertfrom", "join", "split",
}
CMDLETS_EXTRA = {"out-string"}
CMDLETS_NEGADOS = {
    "get-credential", "convertto-securestring", "convertfrom-securestring", "get-secret", "get-secretinfo",
    "get-clipboard",
}
ALIASES_LEITURA = {
    "gci", "ls", "dir", "gc", "cat", "type", "gps", "ps", "gsv", "gi", "gp", "gpv", "gm", "gcm", "gal", "gdr",
    "gl", "pwd", "gv", "gwmi", "select", "where", "?", "sort", "%", "foreach", "ft", "fl", "fw", "group",
    "measure", "compare", "diff", "sls", "rvpa", "echo", "write", "h", "history", "ghy",
}
PALAVRAS_OK = {
    "if", "elseif", "else", "foreach", "for", "while", "do", "until", "switch", "in", "return", "break",
    "continue", "try", "catch", "finally", "throw",
}
PALAVRAS_NEGADAS = {"function", "filter", "workflow", "class", "enum", "using", "data", "dynamicparam", "trap", "configuration"}
METODOS_OK = {
    "tostring", "toupper", "tolower", "toupperinvariant", "tolowerinvariant", "trim", "trimend", "trimstart",
    "contains", "startswith", "endswith", "split", "substring", "indexof", "lastindexof", "padleft", "padright",
    "equals", "compareto", "gettype", "toshortdatestring", "tolongdatestring", "toshorttimestring", "adddays",
    "addhours", "addminutes", "addseconds", "addmonths", "addyears", "subtract", "where", "getvaluenames",
    "getvalue", "getsubkeynames", "isnullorempty", "isnullorwhitespace", "round", "floor", "ceiling",
}
TIPOS_ESTATICOS_OK = {
    "math": None, "system.math": None, "datetime": None, "system.datetime": None, "timespan": None,
    "system.timespan": None, "string": {"isnullorempty", "isnullorwhitespace", "join", "format", "empty"},
    "environment": {"machinename", "username", "osversion", "processorcount", "is64bitoperatingsystem",
                    "getfolderpath", "getenvironmentvariable", "tickcount", "tickcount64", "version",
                    "systemdirectory", "userdomainname"},
}
TIPOS_ESTATICOS_OK["system.environment"] = TIPOS_ESTATICOS_OK["environment"]
TIPOS_ESTATICOS_OK["system.string"] = TIPOS_ESTATICOS_OK["string"]


def _regra_ipconfig(args: list[str]) -> bool:
    return all(a.lower() in ("/all", "-all", "/displaydns", "-displaydns") for a in args)


def _sem_remoto(args: list[str]) -> bool:
    return not any(a.lower() in ("/s", "-s", "/u", "-u", "/p", "-p") for a in args)


def _regra_winget(args: list[str]) -> bool:
    return bool(args) and args[0].lower() in ("search", "list", "show", "--version", "-v", "find", "ls", "view")


def _regra_powercfg(args: list[str]) -> bool:
    seguros = {"/list", "/l", "-list", "-l", "/getactivescheme", "-getactivescheme", "/query", "/q", "-query", "-q",
               "/a", "-a", "/availablesleepstates", "/requests", "-requests", "/lastwake", "-lastwake",
               "/devicequery", "-devicequery"}
    return bool(args) and args[0].lower() in seguros


EXTERNOS = {
    "ipconfig": _regra_ipconfig, "whoami": lambda a: True, "hostname": lambda a: True, "getmac": _sem_remoto,
    "systeminfo": _sem_remoto, "tasklist": _sem_remoto, "driverquery": _sem_remoto, "netstat": lambda a: True,
    "nslookup": lambda a: True, "ping": lambda a: True, "tracert": lambda a: True, "pathping": lambda a: True,
    "winget": _regra_winget, "powercfg": _regra_powercfg, "where.exe": lambda a: True, "query": lambda a: True,
}

_ASPAS_SIMPLES = str.maketrans({"‘": "'", "’": "'", "‚": "'", "‛": "'",
                                "“": '"', "”": '"', "„": '"'})
_PARAM_REMOTO = re.compile(r"(?i)(?<![\w-])-(?:computername|cn|cimsession|session|pssession|credential)\b")
_NEGADOS_TEXTO = re.compile(r"(?i)\$executioncontext|\[\s*scriptblock\s*\]|\$host\b|\bpowershell(?:\.exe)?\b|\bpwsh\b"
                            r"|\bcmd(?:\.exe)?\b|\badd-type\b|\bnew-object\b")
_ESTATICO = re.compile(r"\[\s*([A-Za-z_][\w.]*)\s*\]\s*::\s*([A-Za-z_]\w*)")
_METODO = re.compile(r"\.\s*([A-Za-z_]\w*)\s*\(")
_TOKEN = re.compile(r"[^\s|;(){}=,]+")


def _tirar_textos(cmd: str) -> tuple[str, str | None]:
    """Troca cada texto entre aspas por 0. Recusa here-string e $( ) dentro de aspas duplas."""
    saida, i, n = [], 0, len(cmd)
    while i < n:
        c = cmd[i]
        if c == "@" and i + 1 < n and cmd[i + 1] in "'\"":
            return "", "here-string (@' '@) não é aceito: use uma linha"
        if c == "'":
            j = i + 1
            while j < n:
                if cmd[j] == "'" and j + 1 < n and cmd[j + 1] == "'":
                    j += 2
                    continue
                if cmd[j] == "'":
                    break
                j += 1
            if j >= n:
                return "", "aspas simples sem fechamento"
            saida.append("0")
            i = j + 1
            continue
        if c == '"':
            j = i + 1
            while j < n:
                if cmd[j] == '"' and j + 1 < n and cmd[j + 1] == '"':
                    j += 2
                    continue
                if cmd[j] == '"':
                    break
                j += 1
            if j >= n:
                return "", "aspas duplas sem fechamento"
            if "$(" in cmd[i:j]:
                return "", "$( ) dentro de aspas duplas não é aceito: use aspas simples"
            saida.append("0")
            i = j + 1
            continue
        saida.append(c)
        i += 1
    return "".join(saida), None


def _checar_nome(nome: str, args: list[str]) -> str | None:
    baixo = nome.lower()
    if baixo.endswith(".exe") and baixo != "where.exe":
        baixo = baixo[:-4]
    if baixo in PALAVRAS_NEGADAS:
        return f"'{nome}' não é aceito numa consulta"
    if baixo in PALAVRAS_OK or baixo in ALIASES_LEITURA:
        return None
    if baixo in CMDLETS_NEGADOS:
        return f"'{nome}' lida com segredo e não é aceito"
    if re.fullmatch(r"[a-z]+-[a-z0-9]+", baixo):
        verbo = baixo.split("-", 1)[0]
        if baixo in CMDLETS_EXTRA or (verbo in VERBOS_LEITURA and baixo != "out-file"):
            return None
        return f"'{nome}' muda algo ou executa código: so_consultar só lê. Para mudar, use so_planejar"
    if baixo in EXTERNOS:
        if EXTERNOS[baixo](args):
            return None
        return f"'{nome} {' '.join(args)}' muda algo ou consulta outra máquina: não é aceito"
    if "\\" in nome or "/" in nome or nome.startswith("."):
        return f"'{nome}' é um caminho de programa ou script: so_consultar só roda comandos de leitura"
    return f"'{nome}' não está na lista de comandos de leitura"


def checar_consulta(comando: str) -> str | None:
    """Primeira cerca, em Python. Devolve o motivo da recusa ou None. No Windows, a árvore sintática
    do próprio PowerShell confere de novo antes de rodar (ver estado.VALIDADOR_PS)."""
    if not comando or not comando.strip():
        return "comando vazio"
    if len(comando) > 1500:
        return "comando longo demais (máximo 1500 caracteres)"
    cmd = comando.translate(_ASPAS_SIMPLES)
    if "`" in cmd:
        return "acento grave (`) não é aceito"
    sem_textos, erro = _tirar_textos(cmd)
    if erro:
        return erro
    for proibido, motivo in ((">", "redirecionamento (>) grava arquivo"), ("<", "o caractere < não é aceito"),
                             ("&", "o operador & executa código")):
        if proibido in sem_textos:
            return motivo
    if _PARAM_REMOTO.search(sem_textos):
        return "consultar outra máquina ou usar credencial não é aceito"
    if _NEGADOS_TEXTO.search(sem_textos):
        return "essa construção executa código arbitrário e não é aceita"
    for m in _ESTATICO.finditer(sem_textos):
        tipo, membro = m.group(1).lower(), m.group(2).lower()
        if tipo not in TIPOS_ESTATICOS_OK:
            return f"[{m.group(1)}]:: não é aceito; use cmdlets Get-*"
        permitidos = TIPOS_ESTATICOS_OK[tipo]
        if permitidos is not None and membro not in permitidos:
            return f"[{m.group(1)}]::{m.group(2)} não é aceito"
    if "::" in _ESTATICO.sub("", sem_textos):
        return ":: só é aceito em [math], [datetime], [timespan], [string] e [environment]"
    for m in _METODO.finditer(sem_textos):
        if m.group(1).lower() not in METODOS_OK:
            return f"o método .{m.group(1)}() não é aceito (pode mudar algo)"

    # Posições de comando: início, depois de | ; ( { = e de quebra de linha.
    n = len(sem_textos)
    posicoes = [0] + [k + 1 for k, c in enumerate(sem_textos) if c in "|;({=\r\n"]
    for pos in posicoes:
        i = pos
        while i < n and sem_textos[i] in " \t\r\n":
            i += 1
        if i >= n:
            continue
        m = _TOKEN.match(sem_textos, i)
        if not m:
            continue
        token = m.group(0)
        resto = sem_textos[m.end():]
        if token[0] in "$0123456789[@-!+":
            continue
        if resto.lstrip().startswith("=") and not resto.lstrip().startswith("=="):
            continue  # chave de hashtable ou atribuição
        if token == ".":
            return "dot-source (.) executa script e não é aceito"
        fim = len(resto)
        for sep in "|;)}":
            k = resto.find(sep)
            if k != -1:
                fim = min(fim, k)
        args = [a for a in resto[:fim].split() if a]
        if token.lower() in ("foreach-object", "%", "foreach"):
            inicio = resto.lstrip()[:1]
            if inicio and inicio not in "{(-" or any(a.lower().startswith(("-m", "-a")) for a in args):
                return "ForEach-Object com nome de membro pode chamar método: use ForEach-Object { $_.Propriedade }"
        erro = _checar_nome(token, args)
        if erro:
            return erro
    return None
