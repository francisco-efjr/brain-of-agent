#!/usr/bin/env python3
"""Gera dados/usuarios.json com contas sintéticas para o teste de carga.

Uso: python3 gerar_massa.py --n 10000
Os e-mails usam example.com (domínio reservado, nunca entrega). As contas precisam
ser criadas no STAGING pela equipe (seed/API), com a mesma senha informada em
SENHA_USUARIOS, com notificações (e-mail/SMS) desligadas ou apontando para um sumidouro.
A senha não é gerada nem gravada aqui.
"""
import argparse
import json
import pathlib

p = argparse.ArgumentParser()
p.add_argument("--n", type=int, default=10000, help="quantidade de contas")
p.add_argument("--saida", default="dados/usuarios.json")
a = p.parse_args()

contas = [{"email": f"carga.{i:06d}@example.com"} for i in range(1, a.n + 1)]
destino = pathlib.Path(a.saida)
destino.parent.mkdir(parents=True, exist_ok=True)
destino.write_text(json.dumps(contas, ensure_ascii=False, indent=0), encoding="utf-8")
print(f"{len(contas)} contas em {destino}")
