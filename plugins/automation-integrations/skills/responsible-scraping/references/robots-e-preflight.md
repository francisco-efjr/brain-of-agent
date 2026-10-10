# robots.txt (RFC 9309) e pré-voo de scraping

Fonte normativa: RFC 9309, Robots Exclusion Protocol, IETF, Proposed Standard (https://www.rfc-editor.org/rfc/rfc9309), V-33 (Verificado em 2026-10-10: leitura da RFC pelo validador). Redação própria. Itens marcados Inferido são conhecimento do autor sobre o mesmo RFC que `VALIDATED.md` não detalha (por exemplo desempate entre `allow` e `disallow`, escopo por origem): confira no texto da RFC antes de citar a terceiros. O verificador abaixo foi **executado em 2026-10-10** apenas com entradas sintéticas (13 casos, 0 falhas, sem rede); a função de busca (`fetch_robots`) não foi executada contra site algum.

Sumário: 1. O que a norma diz · 2. Procedimento de pré-voo · 3. Verificador em Python · 4. Termos de uso e outras lacunas · 5. Alternativas ao scraping.

## 1. O que a norma diz (V-33)

| Tema | Regra |
| --- | --- |
| Natureza | pedido a rastreadores bem-comportados; **não é controle de acesso** nem autorização |
| Arquivo ausente (4xx) | o site pode ser tratado como irrestrito |
| Erro de servidor (5xx) ou rede indisponível | assumir **bloqueio total** (a RFC admite tolerância após período longo de indisponibilidade) |
| Redirecionamentos | seguir pelo menos 5 consecutivos |
| Cache | no máximo 24 horas (salvo indisponibilidade) |
| Escolha do grupo | pelo token do produto, sem diferenciar caixa; `*` como reserva |
| Casamento de regras | vence o padrão de caminho mais longo; empate: `allow` (Inferido) |
| Curingas | `*` e `$` (fim do caminho) nos padrões (Inferido) |
| Escopo | por origem: esquema, host e porta (Inferido) |

`Crawl-delay` e `Sitemap` não definem permissão no RFC (Inferido); trate `Crawl-delay` como cortesia e `Sitemap` como fonte legítima de URLs.

## 2. Procedimento de pré-voo (X-01..X-06)

1. **Identifique o agente:** `NomeDoProjeto-Reader/<versão> (+<CONTATO>)`, com contato fornecido pelo usuário. O token de produto (`NomeDoProjeto-Reader`) é o que casa nos grupos de `User-agent`.
2. **Busque `<origem>/robots.txt`** com esse agente (função abaixo). Guarde estado, data e URL.
3. **Decida o caminho alvo** (caminho + query, como aparece na URL) e verifique com `allowed(...)`. Registre a regra que decidiu.
4. **Se bloqueado ou inalcançável:** pare. Diga qual regra (ou qual estado) bloqueia e ofereça alternativas (seção 5).
5. **Taxa:** uma requisição por vez, intervalo mínimo entre elas (proposta: 2 segundos), teto de páginas; respeite `Crawl-delay` se existir. É uma Suposição de política: o site pode exigir mais; ajuste ao que ele publicar.
6. **Termos de uso:** pergunte se foram lidos (a norma não os cobre). Sem resposta, a conformidade de termos fica Não verificada na nota.
7. **Não reler antes de 24 horas.** Para coletas recorrentes, registre a data da última leitura.

## 3. Verificador em Python (stdlib)

```python
import re
import urllib.error
import urllib.request


def fetch_robots(origin, user_agent, timeout=10):
    """Devolve (estado, texto). Estados do RFC 9309: ok | unavailable (4xx: sem restricao) | unreachable (5xx/rede: bloqueio total)."""
    req = urllib.request.Request(origin.rstrip("/") + "/robots.txt", headers={"User-Agent": user_agent})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:      # urllib segue redirecionamentos
            return "ok", resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as err:
        return ("unavailable", "") if 400 <= err.code < 500 else ("unreachable", "")
    except (urllib.error.URLError, TimeoutError):
        return "unreachable", ""


def parse_groups(text):
    groups, agents, rules, after_agent = [], [], [], False
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        field, value = (part.strip() for part in line.split(":", 1))
        field = field.lower()
        if field == "user-agent":
            if agents and not after_agent:
                groups.append((agents, rules))
                agents, rules = [], []
            agents.append(value.lower())
            after_agent = True
        elif field in ("allow", "disallow") and agents:
            rules.append((field, value))
            after_agent = False
        else:
            after_agent = False
    if agents:
        groups.append((agents, rules))
    return groups


def rules_for(groups, product_token):
    token = product_token.lower()
    chosen = [r for agents, r in groups if token in agents] or [r for agents, r in groups if "*" in agents]
    return [rule for group in chosen for rule in group]


def pattern_to_regex(pattern):
    anchored = pattern.endswith("$")
    body = pattern[:-1] if anchored else pattern
    regex = "".join(".*" if ch == "*" else re.escape(ch) for ch in body)
    return re.compile(regex + ("$" if anchored else ""))


def allowed(state, text, product_token, path_and_query):
    if state == "unreachable":
        return False                          # RFC 9309: assumir bloqueio total
    if state == "unavailable" or path_and_query == "/robots.txt":
        return True
    best_len, verdict = -1, True              # sem regra aplicavel: permitido
    for kind, pattern in rules_for(parse_groups(text), product_token):
        if not pattern:
            continue                          # "Disallow:" vazio nao restringe
        if pattern_to_regex(pattern).match(path_and_query):
            if len(pattern) > best_len or (len(pattern) == best_len and kind == "allow"):
                best_len, verdict = len(pattern), (kind == "allow")
    return verdict
```

Uso:

```python
state, text = fetch_robots("https://exemplo.com", "NomeDoProjeto-Reader/1.0 (+contato@exemplo.com)")
ok = allowed(state, text, "nomedoprojeto-reader", "/produtos?pagina=2")
```

Testes (`test_robots.py`, rodados durante a construção do plugin):

```python
from robots_check import allowed
T = """User-agent: *
Disallow: /a/
Allow: /a/b
Disallow: /*.pdf$
Disallow: /privado

User-agent: meubot
Disallow: /so-meubot/
"""
cases = [
 ("ok", T, "outrobot", "/a/c", False), ("ok", T, "outrobot", "/a/b", True),
 ("ok", T, "outrobot", "/x.pdf", False), ("ok", T, "outrobot", "/x.pdf?v=1", True),
 ("ok", T, "outrobot", "/livre", True), ("ok", T, "outrobot", "/privado/x", False),
 ("ok", T, "meubot", "/a/c", True), ("ok", T, "meubot", "/so-meubot/x", False),
 ("ok", "User-agent: *\nDisallow:\n", "x", "/qualquer", True),
 ("ok", "User-agent: *\nAllow: /p\nDisallow: /p\n", "x", "/p", True),
 ("unavailable", "", "x", "/a/c", True), ("unreachable", "", "x", "/livre", False),
 ("ok", T, "x", "/robots.txt", True),
]
bad = 0
for st, txt, tok, path, want in cases:
    got = allowed(st, txt, tok, path); bad += got != want
    print("OK  " if got == want else "FAIL", st, tok, path, "->", got)
print("falhas:", bad)
```

Limites do verificador: não implementa todos os casos de borda da RFC (codificação percentual, linhas muito longas, regras por `User-agent` com versão no token); use para decidir com margem de segurança, e na dúvida trate como bloqueado.

Observação sobre `urllib.robotparser` (observado no código do Python 3.14.4 em 2026-10-10): aplica a **primeira** regra que casa, na ordem do arquivo, e não a mais longa (com `Disallow: /a/` antes de `Allow: /a/b`, `/a/b` sai como proibido); e em `read()` marca bloqueio total para 401/403 e liberação total para os demais 4xx, enquanto a RFC trata todo 4xx como "indisponível". Por isso ele não substitui o verificador acima.

## 4. Termos de uso e outras lacunas (declarar sempre)

- Termos de uso do site, direitos autorais da base de dados e do conteúdo, proteção de dados pessoais (LGPD/GDPR) e políticas de taxa de provedores específicos: **sem fonte validada** na pesquisa deste plugin (lacuna 7 de VALIDATED). A skill pergunta e registra; não decide.
- Acesso atrás de login: o usuário autentica; mesmo assim os termos podem proibir coleta automatizada. Peça confirmação explícita e registre.
- CAPTCHA e outros sinais anti-robô: não contorne; pare e informe.

## 5. Alternativas legítimas ao scraping

API oficial ou feed; exportação de dados oferecida pelo site; sitemap e páginas explicitamente permitidas; contato com o responsável pedindo acesso; parceria ou licença de dados. Quando `robots.txt` bloqueia, essas são as respostas, não um script que ignora a regra.
