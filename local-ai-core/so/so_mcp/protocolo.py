"""MCP por stdio: JSON-RPC 2.0, uma mensagem por linha, só ASCII na saída.

A saída é sempre ASCII (acentos viram \\uXXXX), porque clientes no Windows podem ler o pipe com a
codificação local (cp1252). Logs vão para o stderr; o stdout só leva mensagens MCP.
"""
from __future__ import annotations

import json
import sys
from typing import Any, BinaryIO

from . import NOME, VERSAO

VERSOES = ("2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05")
INSTRUCOES = (
    "Camada de SO da IA local. Leia com so_estado, so_consultar, arquivos_listar e arquivo_ler. Mude o PC só com "
    "so_planejar e depois so_executar (o usuário aprova R2 e R3 numa janela do Windows). Memória: memoria_bastao no "
    "início, memoria_buscar e memoria_lembrar. Regras: regras_consultar."
)


def _erro(id_: Any, codigo: int, mensagem: str, dados: Any = None) -> dict:
    erro: dict[str, Any] = {"code": codigo, "message": mensagem}
    if dados is not None:
        erro["data"] = dados
    return {"jsonrpc": "2.0", "id": id_, "error": erro}


class ServidorMcp:
    def __init__(self, ferramentas):
        self.ferramentas = ferramentas

    def tratar(self, msg: Any) -> dict | None:
        if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0" or not isinstance(msg.get("method"), str):
            return _erro(msg.get("id") if isinstance(msg, dict) else None, -32600, "Requisição inválida")
        metodo, id_ = msg["method"], msg.get("id")
        notificacao = "id" not in msg
        params = msg.get("params") or {}
        if notificacao:
            return None  # notifications/initialized, cancelled etc.: nada a responder
        if metodo == "initialize":
            pedida = params.get("protocolVersion") if isinstance(params, dict) else None
            versao = pedida if pedida in VERSOES else VERSOES[0]
            return {"jsonrpc": "2.0", "id": id_, "result": {
                "protocolVersion": versao,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": NOME, "title": "IA Operador (camada de SO)", "version": VERSAO},
                "instructions": INSTRUCOES,
            }}
        if metodo == "ping":
            return {"jsonrpc": "2.0", "id": id_, "result": {}}
        if metodo == "tools/list":
            return {"jsonrpc": "2.0", "id": id_, "result": {"tools": [f.esquema() for f in self.ferramentas.lista]}}
        if metodo == "tools/call":
            if not isinstance(params, dict) or not isinstance(params.get("name"), str):
                return _erro(id_, -32602, "params.name é obrigatório")
            nome = params["name"]
            if nome not in self.ferramentas.por_nome:
                return _erro(id_, -32602, f"Ferramenta desconhecida: {nome}")
            texto, falhou = self.ferramentas.chamar(nome, params.get("arguments"))
            return {"jsonrpc": "2.0", "id": id_, "result": {"content": [{"type": "text", "text": texto}], "isError": bool(falhou)}}
        return _erro(id_, -32601, f"Método não suportado: {metodo}")

    def tratar_linha(self, linha: bytes) -> bytes | None:
        try:
            texto = linha.decode("utf-8")
        except UnicodeDecodeError:
            texto = linha.decode("cp1252", "replace")
        texto = texto.strip().lstrip("﻿")
        if not texto:
            return None
        try:
            msg = json.loads(texto)
        except ValueError:
            resposta: Any = _erro(None, -32700, "JSON inválido")
        else:
            if isinstance(msg, list):
                respostas = [r for r in (self.tratar(m) for m in msg) if r is not None]
                resposta = respostas or None
            else:
                try:
                    resposta = self.tratar(msg)
                except Exception as exc:  # noqa: BLE001
                    print(f"[so-mcp] erro interno: {exc!r}", file=sys.stderr)
                    resposta = _erro(msg.get("id") if isinstance(msg, dict) else None, -32603, "Erro interno")
        if resposta is None:
            return None
        return (json.dumps(resposta, ensure_ascii=True, separators=(",", ":")) + "\n").encode("ascii")

    def rodar(self, entrada: BinaryIO | None = None, saida: BinaryIO | None = None) -> None:
        entrada = entrada or sys.stdin.buffer
        saida = saida or sys.stdout.buffer
        for linha in entrada:
            resposta = self.tratar_linha(linha)
            if resposta is not None:
                saida.write(resposta)
                saida.flush()
