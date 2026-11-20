"""A esteira do core aplicada pelo servidor: planejar, aprovar, executar, verificar, registrar e desfazer.

so_planejar faz os passos 0 a 7 (classificar, observar, ensaiar, preparar backup e desfazer).
so_executar faz o 8 (aprovação humana na janela do Windows), o 9 (aplicar) e o 10 (verificar e
registrar). O modelo nunca aprova sozinho e nunca roda nada fora do roteiro da ação.
"""
from __future__ import annotations

import json
import pathlib
import secrets
import time
from dataclasses import dataclass, field
from typing import Any, Callable

from . import acoes as cat
from . import politica
from .executor import UAC_CANCELADO, cortar
from .registro import Registro, agora

_ALFABETO = "abcdefghjkmnpqrstuvwxyz23456789"
MAX_FALHAS = 3

# SEG-24 do guia: antes de um R3, um ponto de restauração do Windows, sem travar se o Windows recusar.
_PONTO_RETORNO = r"""
try { Checkpoint-Computer -Description (P 'DESCRICAO') -RestorePointType MODIFY_SETTINGS -WarningAction Stop -ErrorAction Stop; 'ponto de restauração criado' }
catch { if ($_.Exception.Message -match '1440') { 'já existe um ponto de restauração das últimas 24 h' } else { 'ponto de restauração não criado: ' + $_.Exception.Message } }
"""


def _falavel(resumo: str, p: dict | None = None) -> str:
    """Caminho inteiro não se fala: troca os caminhos dos parâmetros pelo nome do arquivo ou da pasta."""
    for valor in sorted(((p or {}).values()), key=lambda v: -len(str(v))):
        if isinstance(valor, str) and (":\\" in valor or valor.startswith("\\\\")):
            resumo = resumo.replace(valor, pathlib.PureWindowsPath(valor).name or valor)
    return resumo


def _voz(status: str, resumo: str, desf: dict, p: dict | None = None) -> str:
    """Uma frase para o canal de voz: o que aconteceu, sem dizer que fez o que a verificação não confirmou."""
    resumo = _falavel(resumo, p)
    inicio = {"Verificado": "Feito e conferido", "Parcial": "Feito, mas não consegui conferir tudo",
              "Falhou": "Não confirmei o resultado"}.get(status, status)
    resumo = (resumo[:1].lower() + resumo[1:]) if resumo else ""
    volta = " Dá para desfazer se você pedir." if isinstance(desf, dict) and desf.get("acao") else ""
    return f"{inicio}: {resumo}.{volta}"


class Recusado(Exception):
    pass


@dataclass
class Ctx:
    cfg: Any
    executor: Any
    plano_id: str = ""
    extras: dict = field(default_factory=dict)


def _estado_curto(obs: dict, limite: int = 900) -> str:
    partes = []
    for chave, valor in obs.items():
        if isinstance(valor, (dict, list)):
            valor = json.dumps(valor, ensure_ascii=False)
        texto = str(valor).replace("\r", " ").replace("\n", " | ")
        partes.append(f"{chave}: {texto[:200]}")
    return cortar("; ".join(partes), limite) if partes else "(nada a ler)"


def _texto_desfazer(d: dict, plano_id: str, previsto: bool = False) -> str:
    if d.get("acao"):
        texto = f"so_desfazer com plano_id=\"{plano_id}\" (vai planejar {d['acao'].lstrip('_')})"
        if not previsto:
            texto += f" com {json.dumps(d.get('parametros', {}), ensure_ascii=False)[:200]}"
    else:
        texto = "manual: " + d.get("nota", "sem desfazer automático")
        return texto
    return texto + (f". Obs.: {d['nota']}" if d.get("nota") else "")


class Planejador:
    def __init__(self, cfg, executor, confirmador, registro: Registro, relogio: Callable[[], float] = time.time):
        self.cfg = cfg
        self.executor = executor
        self.confirmador = confirmador
        self.registro = registro
        self.relogio = relogio
        self.falhas: dict[str, int] = {}

    # ------------------------------------------------------------ apoio

    def _ctx(self, plano_id: str = "") -> Ctx:
        return Ctx(self.cfg, self.executor, plano_id)

    def _arquivo(self, plano_id: str) -> pathlib.Path:
        return self.cfg.planos / f"{plano_id}.json"

    def _salvar(self, plano: dict) -> None:
        self.cfg.planos.mkdir(parents=True, exist_ok=True)
        self._arquivo(plano["id"]).write_text(json.dumps(plano, ensure_ascii=False, indent=1), encoding="utf-8")

    def _carregar(self, plano_id: str) -> dict | None:
        plano_id = plano_id.strip().strip('"').lower()
        if not plano_id or any(c not in _ALFABETO for c in plano_id):
            return None
        arq = self._arquivo(plano_id)
        return json.loads(arq.read_text(encoding="utf-8")) if arq.is_file() else None

    def _novo_id(self) -> str:
        while True:
            pid = "p" + "".join(secrets.choice(_ALFABETO) for _ in range(5))
            if not self._arquivo(pid).exists():
                return pid

    def _vencido(self, plano: dict) -> bool:
        return self.relogio() - plano["criado"] > self.cfg.plano_validade_min * 60

    def _ultimo_planejado(self) -> dict | None:
        if not self.cfg.planos.is_dir():
            return None
        planos = []
        for arq in self.cfg.planos.glob("p*.json"):
            try:
                planos.append(json.loads(arq.read_text(encoding="utf-8")))
            except (OSError, ValueError):
                continue
        planos = [p for p in planos if p.get("estado") == "planejado" and not self._vencido(p)]
        return max(planos, key=lambda p: p["criado"], default=None)

    def _args(self, acao: cat.Acao, p: dict, obs: dict, plano_id: str, extra: dict | None = None) -> dict:
        args = dict(p)
        if acao.extras:
            args.update(acao.extras(p, obs))
        args["PLANO"] = plano_id
        args.update(extra or {})
        return {k.upper(): v for k, v in args.items()}

    def _ps(self, acao: cat.Acao, etapa: str, script: str, p: dict, obs: dict, plano_id: str,
            extra: dict | None = None, elevado: bool = False):
        return self.executor.rodar(script, self._args(acao, p, obs, plano_id, extra), timeout=acao.timeout_s,
                                   elevado=elevado, rotulo=f"{acao.nome}:{etapa}")

    def _observar(self, acao: cat.Acao, p: dict, plano_id: str) -> dict:
        if acao.observar is None:
            return {}
        if callable(acao.observar):
            return acao.observar(p, self._ctx(plano_id))
        r = self._ps(acao, "observar", acao.observar, p, {}, plano_id)
        if not r.ok:
            raise RuntimeError(r.texto() or f"código {r.codigo}")
        dados = r.json()
        if not isinstance(dados, dict):
            raise RuntimeError("o estado veio em formato inesperado")
        return dados

    def _ensaiar(self, acao: cat.Acao, p: dict, obs: dict, plano_id: str) -> tuple[str, bool]:
        if acao.ensaiar is None:
            return "sem ensaio próprio: o estado atual foi lido acima", True
        if callable(acao.ensaiar):
            return cortar(acao.ensaiar(p, obs, self._ctx(plano_id)), 1500), True
        r = self._ps(acao, "ensaiar", acao.ensaiar, p, obs, plano_id)
        texto = cortar(r.texto(), 1500)
        return (texto or "(o ensaio não mostrou saída)", True) if r.ok else ("o ensaio falhou: " + texto, False)

    def _backup(self, acao: cat.Acao, p: dict, obs: dict, plano_id: str) -> dict:
        pasta = self.cfg.backups / plano_id
        if callable(acao.backup):
            return acao.backup(p, obs, self._ctx(plano_id), pasta)
        pasta.mkdir(parents=True, exist_ok=True)
        arq = pasta / f"{acao.nome.lstrip('_')}{acao.backup_ext}"
        r = self._ps(acao, "backup", acao.backup, p, obs, plano_id, {"BACKUP": str(arq)})
        if not r.ok:
            raise RuntimeError(r.texto() or f"código {r.codigo}")
        return {"texto": cortar(r.saida.strip(), 300), "backup": str(arq) if arq.exists() else ""}

    def _aplicar(self, acao: cat.Acao, p: dict, obs: dict, plano_id: str, admin: bool) -> dict:
        if callable(acao.aplicar):
            return dict(acao.aplicar(p, obs, self._ctx(plano_id)))
        r = self._ps(acao, "aplicar", acao.aplicar, p, obs, plano_id, elevado=admin)
        if r.codigo == UAC_CANCELADO:
            raise Recusado(r.erro or "o usuário não autorizou no UAC")
        if not r.ok:
            raise RuntimeError(r.texto() or f"código {r.codigo}")
        return {"texto": cortar(r.saida.strip(), 800)}

    def _verificar(self, acao: cat.Acao, p: dict, obs: dict, info: dict, plano_id: str) -> tuple[bool | None, str]:
        if acao.verificar is None:
            return None, "o Windows aceitou o pedido; confira na tela"
        if callable(acao.verificar):
            ok, detalhe = acao.verificar(p, obs, info, self._ctx(plano_id))
            return (None if ok is None else bool(ok)), detalhe
        r = self._ps(acao, "verificar", acao.verificar, p, obs, plano_id)
        if not r.ok:
            return False, "não consegui verificar: " + r.texto()[:300]
        try:
            dados = r.json()
        except ValueError as exc:
            return False, f"verificação ilegível: {exc}"
        ok = dados.get("ok")
        return (None if ok is None else bool(ok)), str(dados.get("detalhe", ""))

    # ------------------------------------------------------------ ferramentas

    def listar_acoes(self) -> str:
        return "\n".join(f"- {cat.assinatura(a)}: {a.descricao}" for a in cat.PUBLICAS)

    def planejar(self, nome: str, parametros: Any, motivo: str = "", interno: bool = False) -> tuple[str, bool]:
        """Devolve (texto para o modelo, erro?)."""
        acao = cat.ACOES.get(str(nome).strip())
        if acao is None or (acao.interna and not interno):
            return (f"Ação desconhecida: {nome!r}. Ações disponíveis:\n{self.listar_acoes()}", True)
        p, erros = cat.validar(acao, parametros)
        if erros:
            return (f"PARÂMETROS INVÁLIDOS para {acao.nome}: " + "; ".join(erros) + f".\nUse: {cat.assinatura(acao)}", True)

        pid = self._novo_id()
        try:
            obs = self._observar(acao, p, pid)
        except Exception as exc:  # noqa: BLE001 - qualquer falha de leitura vira resposta clara
            self.registro.anotar(tipo="plano", acao=acao.nome, parametros=p, resultado="falha ao observar", erro=str(exc))
            return (f"NÃO PLANEJADO: não consegui ler o estado atual: {cortar(str(exc), 600)}", True)

        risco, motivo_risco = acao.avaliar(p, obs, self._ctx(pid))
        if risco == "BLOQUEADO":
            self.registro.anotar(tipo="plano", acao=acao.nome, parametros=p, resultado="bloqueado", motivo=motivo_risco)
            return (f"BLOQUEADO: {motivo_risco}. Não tente outro caminho para fazer o mesmo. Explique ao usuário e, "
                    "se ele quiser, diga como ele mesmo pode fazer.", True)
        if risco == "INVIAVEL":
            self.registro.anotar(tipo="plano", acao=acao.nome, parametros=p, resultado="inviável", motivo=motivo_risco)
            return (f"NÃO PLANEJADO: {motivo_risco}.", True)

        admin = acao.precisa_admin(p)
        ensaio, ensaio_ok = self._ensaiar(acao, p, obs, pid)
        if not ensaio_ok and not admin:
            self.registro.anotar(tipo="plano", acao=acao.nome, parametros=p, resultado="ensaio falhou", ensaio=ensaio)
            return (f"NÃO PLANEJADO: {ensaio}", True)
        if not ensaio_ok:
            ensaio = "sem administrador, o ensaio não rodou por completo (" + ensaio + "); a janela do UAC vai aparecer na execução"

        previsto = acao.desfazer(p, obs, {"previsao": True, "criado": not obs.get("existe", True)}) if acao.desfazer else {}
        resumo = acao.resumo(p, obs)
        plano = {
            "id": pid, "criado": self.relogio(), "criado_em": agora().isoformat(timespec="seconds"),
            "acao": acao.nome, "parametros": p, "motivo": str(motivo or "")[:500], "risco": risco,
            "motivo_risco": motivo_risco, "admin": admin, "resumo": resumo, "observado": obs, "ensaio": ensaio,
            "desfazer_previsto": previsto, "estado": "planejado",
        }
        self._salvar(plano)
        self.registro.anotar(tipo="plano", plano=pid, acao=acao.nome, parametros=p, risco=risco, resumo=resumo)
        return self._texto_plano(plano, acao), False

    def _texto_plano(self, plano: dict, acao: cat.Acao) -> str:
        pid, risco = plano["id"], plano["risco"]
        linhas = [
            f"PLANO {pid} [{risco}] {plano['resumo']}",
            f"Por que {risco}: {plano['motivo_risco']}",
            f"Estado atual (lido agora): {_estado_curto(plano['observado'])}",
            f"Ensaio: {plano['ensaio']}",
            "Backup: " + ("automático, antes de aplicar" if acao.backup else "não precisa; o valor anterior está anotado no plano"),
            "Como desfazer: " + _texto_desfazer(plano["desfazer_previsto"] or {"nota": "sem desfazer automático"}, pid, previsto=True),
            "Como vou verificar: " + (acao.verificacao or ("conferir o resultado" if acao.verificar else "o Windows confirma o pedido")),
        ]
        if acao.aviso:
            linhas.append("Aviso: " + acao.aviso)
        uac = " O Windows também vai pedir permissão de administrador (UAC)." if plano["admin"] else ""
        if risco == "R1":
            linhas.append("Aprovação: não precisa (R1).")
            linhas.append(f"Próximo passo: chame so_executar com plano_id=\"{pid}\".")
        elif risco == "R2":
            linhas.append("Aprovação: quando você chamar so_executar, o Windows abre uma janela e o usuário clica Sim ou Não. "
                          "Não peça \"sim\" no chat." + uac)
            linhas.append(f"Próximo passo: diga ao usuário, em uma frase, o que vai acontecer e chame so_executar com plano_id=\"{pid}\".")
        else:
            linhas.append("Aprovação: alto risco. O Windows vai pedir que o usuário digite CONFIRMO." + uac)
            linhas.append(f"Próximo passo: explique o risco ao usuário em até 3 linhas e pergunte se ele quer seguir. Só se ele disser "
                          f"que sim, chame so_executar com plano_id=\"{pid}\".")
        return "\n".join(linhas)

    def _texto_janela(self, plano: dict, acao: cat.Acao, risco: str, motivo_risco: str) -> str:
        previsto = _texto_desfazer(plano.get("desfazer_previsto") or {"nota": "sem desfazer automático"}, plano["id"], previsto=True)
        partes = [
            plano["resumo"],
            "",
            f"Risco: {risco} ({motivo_risco})",
            f"Como desfazer: {previsto}",
        ]
        if acao.aviso:
            partes.append(acao.aviso)
        if plano.get("motivo"):
            partes.append(f"Motivo dado pela IA: {plano['motivo'][:300]}")
        partes += ["", f"Plano {plano['id']} (detalhes em {self._arquivo(plano['id'])})",
                   "Aprove só se foi você quem pediu isso."]
        return "\n".join(partes)

    def executar(self, plano_id: str | None = None) -> tuple[str, bool]:
        plano = self._carregar(plano_id) if plano_id else self._ultimo_planejado()
        if plano is None:
            return ("Plano não encontrado. Chame so_planejar primeiro e use o plano_id que ele devolver.", True)
        pid = plano["id"]
        if plano["estado"] != "planejado":
            return (f"O plano {pid} está como {plano['estado']}; nada foi feito. Planeje de novo se precisar.", True)
        if self._vencido(plano):
            plano["estado"] = "vencido"
            self._salvar(plano)
            return (f"O plano {pid} venceu (mais de {self.cfg.plano_validade_min} min). Chame so_planejar de novo para ler o estado atual.", True)
        if self.cfg.arquivo_parar.exists():
            return (f"PARADA GERAL ATIVA ({self.cfg.arquivo_parar} existe). Nada foi executado. Só o usuário apaga esse arquivo.", True)

        acao = cat.ACOES[plano["acao"]]
        p, antes = plano["parametros"], plano["observado"]
        chave = acao.nome + json.dumps(p, sort_keys=True, ensure_ascii=False)
        if self.falhas.get(chave, 0) >= MAX_FALHAS:
            return (f"Esta ação já falhou {MAX_FALHAS} vezes seguidas. Pare, mostre os erros ao usuário e pergunte como seguir.", True)

        try:
            obs = self._observar(acao, p, pid)
        except Exception as exc:  # noqa: BLE001
            return (f"NÃO EXECUTADO: não consegui reler o estado: {cortar(str(exc), 400)}", True)
        chaves = acao.chaves_estado if acao.chaves_estado is not None else tuple(antes)
        mudou = [f"{k}: {antes.get(k)!r} → {obs.get(k)!r}" for k in chaves if obs.get(k) != antes.get(k)]
        if mudou:
            plano["estado"] = "cancelado"
            self._salvar(plano)
            self.registro.anotar(tipo="execucao", plano=pid, acao=acao.nome, risco=plano["risco"], status="Cancelado",
                                 resumo=plano["resumo"], motivo="a realidade mudou: " + "; ".join(mudou))
            return ("A REALIDADE MUDOU desde o plano (" + "; ".join(mudou)[:400] + "). Nada foi executado. Planeje de novo.", True)

        risco, motivo_risco = acao.avaliar(p, obs, self._ctx(pid))
        if risco in ("BLOQUEADO", "INVIAVEL") or politica.ORDEM.get(risco, 9) > politica.ORDEM[plano["risco"]]:
            plano["estado"] = "cancelado"
            self._salvar(plano)
            return (f"NÃO EXECUTADO: a avaliação mudou para {risco} ({motivo_risco}). Planeje de novo.", True)

        if risco in ("R2", "R3"):
            titulo = f"IA local pede aprovação [{risco}]"
            aprovado, aprovacao = self.confirmador.pedir(risco, titulo, self._texto_janela(plano, acao, risco, motivo_risco))
        else:
            aprovado, aprovacao = True, "R1: não precisa de aprovação"
        if not aprovado:
            plano.update(estado="recusado", aprovacao=aprovacao)
            self._salvar(plano)
            self.registro.anotar(tipo="execucao", plano=pid, acao=acao.nome, risco=risco, status="Recusado",
                                 resumo=plano["resumo"], aprovacao=aprovacao)
            return (f"NÃO EXECUTADO: {aprovacao}. Não tente de novo nem por outro caminho; pergunte ao usuário o que ele prefere.", True)

        admin = plano["admin"]
        ponto = ""
        if risco == "R3" and acao.nome != "ponto_restauracao_criar" and getattr(self.cfg, "ponto_antes_r3", True):
            try:
                r = self.executor.rodar(_PONTO_RETORNO, {"DESCRICAO": f"IA-Operador {pid}"}, timeout=300,
                                        elevado=True, rotulo="ponto_retorno")
                ponto = cortar(r.texto().strip(), 200) or f"ponto de restauração: código {r.codigo}"
            except Exception as exc:  # noqa: BLE001
                ponto = "ponto de restauração não criado: " + cortar(str(exc), 200)
        backup: dict = {}
        if acao.backup:
            try:
                backup = self._backup(acao, p, obs, pid)
            except Exception as exc:  # noqa: BLE001
                plano.update(estado="falhou", aprovacao=aprovacao, erro="backup: " + str(exc))
                self._salvar(plano)
                self.registro.anotar(tipo="execucao", plano=pid, acao=acao.nome, risco=risco, status="Falhou",
                                     resumo=plano["resumo"], erro="backup falhou: " + str(exc))
                return (f"NÃO EXECUTADO: o backup falhou, então nada foi aplicado: {cortar(str(exc), 400)}", True)

        try:
            info = self._aplicar(acao, p, obs, pid, admin)
        except Recusado as exc:
            plano.update(estado="recusado", aprovacao=str(exc))
            self._salvar(plano)
            self.registro.anotar(tipo="execucao", plano=pid, acao=acao.nome, risco=risco, status="Recusado",
                                 resumo=plano["resumo"], aprovacao=str(exc))
            return (f"NÃO EXECUTADO: {exc}. Não tente de novo; pergunte ao usuário.", True)
        except Exception as exc:  # noqa: BLE001
            self.falhas[chave] = self.falhas.get(chave, 0) + 1
            desf = acao.desfazer(p, obs, {"backup": backup.get("backup", "")}) if acao.desfazer else {}
            plano.update(estado="falhou", aprovacao=aprovacao, erro=str(exc), backup=backup, desfazer=desf)
            self._salvar(plano)
            self.registro.anotar(tipo="execucao", plano=pid, acao=acao.nome, risco=risco, status="Falhou",
                                 resumo=plano["resumo"], erro=str(exc))
            return ("\n".join([
                f"FEITO: nada confirmado; a aplicação falhou ({plano['resumo']}).",
                f"EVIDÊNCIA: {cortar(str(exc), 600)}",
                "STATUS: Falhou",
                f"APROVAÇÃO: {aprovacao}",
                "BACKUP: " + (backup.get("texto") or "não houve") + (f" · {ponto}" if ponto else ""),
                "DESFAZER: confira o estado com so_estado; se algo mudou pela metade, mostre ao usuário antes de tentar de novo.",
                f"PENDÊNCIAS: tentativa {self.falhas[chave]} de {MAX_FALHAS}. Leia o erro, corrija a causa e planeje de novo.",
                f"CONFORMIDADE (guia): plano relido sem mudança · aprovação: {aprovacao} · verificação: Falhou · "
                f"falhas seguidas: {self.falhas[chave]}/{MAX_FALHAS}",
                f"VOZ: Não deu certo: {_falavel(plano['resumo'][:1].lower() + plano['resumo'][1:], p)}. Nada foi confirmado; o erro está na tela.",
            ]), True)

        if backup.get("backup"):
            info.setdefault("backup", backup["backup"])
        ok, detalhe = self._verificar(acao, p, obs, info, pid)
        status = "Verificado" if ok else ("Parcial" if ok is None else "Falhou")
        desf = acao.desfazer(p, obs, info) if acao.desfazer else {"nota": "sem desfazer automático"}
        if ok is False:
            self.falhas[chave] = self.falhas.get(chave, 0) + 1
        else:
            self.falhas.pop(chave, None)
        plano.update(estado="executado", executado_em=agora().isoformat(timespec="seconds"), aprovacao=aprovacao,
                     info=info, backup=backup, verificacao={"ok": ok, "detalhe": detalhe}, desfazer=desf, status=status)
        self._salvar(plano)
        self.registro.anotar(tipo="execucao", plano=pid, acao=acao.nome, risco=risco, status=status,
                             resumo=plano["resumo"], aprovacao=aprovacao, evidencia=detalhe)
        pendencias = "nenhuma"
        if status == "Parcial":
            pendencias = "confira na tela e conte ao usuário o que viu"
        elif status == "Falhou":
            pendencias = "a verificação não confirmou o efeito: mostre a evidência ao usuário antes de qualquer nova tentativa"
        return ("\n".join([
            f"FEITO: {plano['resumo']}. {info.get('texto', '')}".strip(),
            f"EVIDÊNCIA: {detalhe}",
            f"STATUS: {status}",
            f"APROVAÇÃO: {aprovacao}",
            "BACKUP: " + (backup.get("texto") or "não precisou") + (f" · {ponto}" if ponto else ""),
            "DESFAZER: " + _texto_desfazer(desf, pid),
            f"PENDÊNCIAS: {pendencias}",
            f"CONFORMIDADE (guia): plano relido sem mudança · aprovação: {aprovacao} · ponto de retorno: "
            f"{backup.get('texto') or ('backup ' + backup['backup'] if backup.get('backup') else 'não precisou')}"
            f"{(' + ' + ponto) if ponto else ''} · verificação na fonte: {status} · falhas seguidas: "
            f"{self.falhas.get(chave, 0)}/{MAX_FALHAS}",
            "VOZ: " + _voz(status, plano["resumo"], desf, p),
        ]), status == "Falhou")

    def desfazer(self, plano_id: str) -> tuple[str, bool]:
        plano = self._carregar(plano_id or "")
        if plano is None:
            return ("Plano não encontrado. Veja os planos executados com so_historico.", True)
        if plano["estado"] not in ("executado", "falhou"):
            return (f"Só dá para desfazer um plano executado; o {plano['id']} está como {plano['estado']}.", True)
        d = plano.get("desfazer") or {}
        if not d.get("acao"):
            return (f"Desfazer o plano {plano['id']} não é automático: {d.get('nota', 'sem instrução registrada')}", False)
        texto, erro = self.planejar(d["acao"], d.get("parametros", {}), f"desfazer o plano {plano['id']}", interno=True)
        cabecalho = f"Para desfazer o plano {plano['id']}, planejei a volta" + (f" (obs.: {d['nota']})" if d.get("nota") else "") + ":\n"
        return cabecalho + texto, erro

    def historico(self, limite: int = 10) -> str:
        eventos = self.registro.ultimos(max(1, min(int(limite), 50)), tipo="execucao")
        if not eventos:
            return "Nenhuma execução registrada ainda."
        linhas = ["quando | plano | ação | risco | status | resumo"]
        for e in eventos:
            linhas.append(" | ".join(str(e.get(k, "")) for k in ("quando", "plano", "acao", "risco", "status", "resumo")))
        return "\n".join(linhas)
