#!/usr/bin/env python3
"""Varredura automática com regras WCAG 2.2 A/AA do axe-core em rotas.

Uso:
    python auditoria_axe.py https://exemplo.com /login /cadastro
    python auditoria_axe.py http://localhost:8081 --todas-as-rotas rotas.txt

Imprime violações e resultados `incomplete` que precisam de revisão manual.
Zero violações não comprova conformidade WCAG. Examina apenas o estado
carregado: diálogos, erros, teclado e tecnologia assistiva exigem outros testes.
Códigos de saída: 0 = sem violações automáticas (pode haver revisão pendente),
1 = violações, 2 = erro de entrada, navegação ou execução da auditoria.

Requisitos: `pip install playwright && playwright install chromium`.
O axe-core fixado em 4.10.2 é baixado do CDN na primeira execução e guardado
em axe.min.js ao lado do script. Cache existente permite execução sem download.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

AXE_URL = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js"
AXE_LOCAL = Path(__file__).with_name("axe.min.js")
TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]


def obter_axe() -> str:
    if not AXE_LOCAL.exists():
        print(f"baixando axe-core de {AXE_URL}…", file=sys.stderr)
        with urllib.request.urlopen(AXE_URL, timeout=30) as resposta:
            fonte = resposta.read().decode("utf-8")
        # Interrupção durante download/gravação não deve deixar cache parcial.
        temporario = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=AXE_LOCAL.parent,
                                             delete=False) as arquivo:
                temporario = Path(arquivo.name)
                arquivo.write(fonte)
            temporario.replace(AXE_LOCAL)
        finally:
            if temporario is not None:
                temporario.unlink(missing_ok=True)
    return AXE_LOCAL.read_text(encoding="utf-8")


def analisar_completo(pagina, fonte_axe: str) -> dict:
    """Retorna violações e revisão manual; fonte deve ser axe-core confiável."""
    # A avaliação direta funciona também em páginas com CSP restritiva.
    # Injeta a fonte escolhida mesmo se a aplicação já tiver outra versão do axe.
    try:
        pagina.evaluate(fonte_axe)
    except Exception:
        pagina.add_script_tag(content=fonte_axe)
    return pagina.evaluate(
        """async (tags) => {
             const r = await window.axe.run(document, {
               runOnly: { type: 'tag', values: tags },
               resultTypes: ['violations', 'incomplete'],
             });
             return { violations: r.violations, incomplete: r.incomplete };
           }""",
        TAGS,
    )


def analisar(pagina, fonte_axe: str) -> list[dict]:
    """API compatível: só violações; use analisar_completo para revisão manual."""
    return analisar_completo(pagina, fonte_axe)["violations"]


def montar_url(base: str, rota: str) -> str:
    origem = urlsplit(base)
    caminho = urlsplit(rota)
    if origem.scheme not in {"http", "https"} or not origem.hostname or origem.query or origem.fragment:
        raise ValueError("base precisa ser uma URL HTTP(S) sem query nem fragmento")
    if caminho.scheme or caminho.netloc:
        raise ValueError(f"rota precisa ser relativa à base: {rota!r}")
    return base.rstrip("/") + "/" + rota.lstrip("/")


def imprimir_resultados(resultados: list[dict], revisao: bool = False) -> None:
    for resultado in resultados:
        rotulo = "revisão manual" if revisao else resultado.get("impact", "?")
        print(f"  [{rotulo}] {resultado['id']}: {resultado['help']}")
        for no in resultado.get("nodes", [])[:5]:
            # Seletores de iframe/shadow DOM podem ser arrays aninhados.
            print(f"      {json.dumps(no.get('target', []), ensure_ascii=False)}")
        print(f"      {resultado['helpUrl']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", help="base da aplicação, ex.: https://exemplo.com")
    parser.add_argument("rotas", nargs="*", help="rotas a auditar")
    parser.add_argument("--todas-as-rotas", type=Path, help="arquivo UTF-8: uma rota por linha, # para comentário")
    parser.add_argument("--largura", type=int, default=1440)
    parser.add_argument("--altura", type=int, default=900)
    parser.add_argument("--esperar", type=int, default=800, help="ms após a carga; não garante prontidão")
    parser.add_argument("--esperar-seletor", help="seletor visível que identifica a tela pronta")
    parser.add_argument("--timeout-ms", type=int, default=30000, help="timeout por operação no navegador")
    args = parser.parse_args(argv)
    if args.largura <= 0 or args.altura <= 0 or args.esperar < 0 or args.timeout_ms <= 0:
        parser.error("dimensões e timeout precisam ser positivos; espera não pode ser negativa")

    try:
        rotas = list(args.rotas)
        if args.todas_as_rotas:
            rotas += [r.strip() for r in args.todas_as_rotas.read_text(encoding="utf-8").splitlines()
                      if r.strip() and not r.lstrip().startswith("#")]
            if not rotas:
                raise ValueError("arquivo de rotas vazio; nenhuma tela seria auditada")
        urls = [montar_url(args.base, rota) for rota in (rotas or ["/"])]
        from playwright.sync_api import sync_playwright

        fonte = obter_axe()
        total = pendentes = 0
        with sync_playwright() as p:
            navegador = p.chromium.launch(headless=True)
            try:
                pagina = navegador.new_context(
                    viewport={"width": args.largura, "height": args.altura}, locale="pt-BR"
                ).new_page()
                pagina.set_default_timeout(args.timeout_ms)
                for url in dict.fromkeys(urls):
                    resposta = pagina.goto(url, wait_until="domcontentloaded")
                    if resposta is None or resposta.status >= 400:
                        status = resposta.status if resposta else "sem resposta HTTP"
                        raise RuntimeError(f"{url}: navegação falhou ({status})")
                    if urlsplit(pagina.url).netloc != urlsplit(url).netloc:
                        raise RuntimeError(f"{url}: redirecionou para outra origem ({pagina.url})")
                    if args.esperar_seletor:
                        pagina.locator(args.esperar_seletor).wait_for(state="visible")
                    pagina.wait_for_timeout(args.esperar)
                    resultado = analisar_completo(pagina, fonte)
                    violacoes, revisao = resultado["violations"], resultado["incomplete"]
                    total += len(violacoes)
                    pendentes += len(revisao)
                    print(f"\n===== {url} =====")
                    if not violacoes:
                        print("  nenhuma violação automática detectada neste estado")
                    imprimir_resultados(violacoes)
                    imprimir_resultados(revisao, revisao=True)
            finally:
                navegador.close()
        print(f"\ntotal de violações: {total}; regras com revisão manual pendente: {pendentes}")
        print("Varredura automática não comprova conformidade WCAG; complete a avaliação manual.")
        return 1 if total else 0
    except Exception as erro:
        print(f"erro: auditoria não concluída: {erro}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
