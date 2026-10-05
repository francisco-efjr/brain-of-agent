# Segurança

Verificação defensiva de segurança que um QA executa em sistema próprio ou
com autorização: controle de acesso, autenticação, entrada, configuração,
segredos, cadeia de suprimentos, lógica de negócio e LGPD. Leia quando a
tarefa envolver OWASP, IDOR, login, sessão, permissões, dados pessoais ou
"isso está seguro para publicar?".

## Sumário

- [Escopo, ética e o que cabe ao QA](#escopo-ética-e-o-que-cabe-ao-qa)
- [OWASP Top 10:2025](#owasp-top-102025)
- [OWASP API Security Top 10:2023](#owasp-api-security-top-102023)
- [Controle de acesso na prática](#controle-de-acesso-na-prática)
- [Autenticação e sessão](#autenticação-e-sessão)
- [Injeção e validação de entrada](#injeção-e-validação-de-entrada)
- [Configuração e exposição](#configuração-e-exposição)
- [Segredos e cadeia de suprimentos](#segredos-e-cadeia-de-suprimentos)
- [Ferramentas no pipeline](#ferramentas-no-pipeline)
- [Lógica de negócio](#lógica-de-negócio)
- [LGPD para QA](#lgpd-para-qa)
- [OWASP ASVS 5.0 como checklist](#owasp-asvs-50-como-checklist)
- [Testes automatizados de exemplo](#testes-automatizados-de-exemplo)
- [Como reportar vulnerabilidade](#como-reportar-vulnerabilidade)

## Escopo, ética e o que cabe ao QA

**Autorização por escrito antes de qualquer teste ativo:** hosts no escopo,
janela, técnicas permitidas, contas de teste, contato de emergência e o que
fazer se aparecer dado real. Em sistema de terceiro, entregue casos de
verificação e ferramentas para o dono executar — nunca execute você.

- **Ambiente:** homologação com dados sintéticos. Em produção, só
  verificações passivas combinadas (cabeçalhos, arquivos expostos, TLS).
- **Nunca:** negação de serviço, engenharia social, acessar dado de outra
  pessoa além do mínimo para provar o defeito, guardar o que encontrou.
- **Sentinelas inofensivas:** prove que a entrada é tratada como dado com um
  marcador que só teria efeito se o controle falhasse.

A suíte de QA é regressão automatizada de controles conhecidos a cada PR:
barata, contínua, pega o controle que **quebrou**. O pentest é um
especialista encadeando falhas, periódico ou antes de grande mudança: acha o
controle que **nunca existiu**. Um não substitui o outro — a suíte impede
que o achado do pentest volte.

## OWASP Top 10:2025

Edição apresentada pela OWASP em novembro de 2025, substituindo a de 2021.
SSRF foi absorvido por A01; A03 amplia "componentes vulneráveis" para toda a
cadeia de suprimentos; A10 é nova.

| Categoria | O que o QA verifica |
| --- | --- |
| A01 Broken Access Control | recurso de outro usuário/tenant (IDOR); função de admin com usuário comum; URL sem link acessada direto; campo de URL buscado pelo servidor não alcança rede interna (SSRF) |
| A02 Security Misconfiguration | cabeçalhos; erro verboso; modo debug; conta padrão; listagem de diretório; arquivos expostos; CORS permissivo |
| A03 Software Supply Chain Failures | SCA sem vulnerabilidade alta/crítica sem tratativa; lockfile versionado; SBOM; Actions fixadas por SHA; script de CDN com SRI |
| A04 Cryptographic Failures | só HTTPS, com HSTS; TLS 1.2+; senha com hash forte (bcrypt, scrypt, Argon2); dado sensível fora de URL, de cache (`Cache-Control: no-store`) e de `localStorage` |
| A05 Injection | SQL, NoSQL, comando, XSS, template — ver [Injeção](#injeção-e-validação-de-entrada) |
| A06 Insecure Design | casos de abuso no refinamento; limites de valor, quantidade e frequência — ver [Lógica de negócio](#lógica-de-negócio) |
| A07 Authentication Failures | enumeração, força bruta, recuperação de senha, sessão — ver [Autenticação](#autenticação-e-sessão) |
| A08 Software or Data Integrity Failures | servidor não confia em preço, papel ou status vindos do cliente; não desserializa dado não confiável; artefatos e atualizações verificados |
| A09 Security Logging and Alerting Failures | login falho, acesso negado, troca de senha/MFA e de permissão registrados com quem/quando/onde, sem senha nem token; **o alerta dispara** (teste o alerta, não só o log); quebra de linha em campo não forja linha de log |
| A10 Mishandling of Exceptional Conditions | falha **fechada**: autorização ou antifraude fora do ar nega, não libera; JSON truncado, tipo errado ou número enorme dá 4xx, não 500 com stack; operação parcial é revertida (cobrou sem criar pedido = defeito) |

## OWASP API Security Top 10:2023

A edição de 2023 continua sendo a vigente para APIs.

| Item | Caso de teste | Esperado |
| --- | --- | --- |
| API1 BOLA | usuário B usa o ID de um objeto de A em GET, PUT, PATCH, DELETE e sub-recursos | 403/404, nada de A no corpo, objeto intacto |
| API2 Broken Authentication | rota sem token; token expirado, adulterado ou de outro ambiente; login/OTP/reset sem limite | 401; limitação após N tentativas |
| API3 BOPLA | leitura traz campo que o papel não deveria ver (hash, CPF completo, campo interno); escrita de campo protegido (`papel`, `saldo`, `tenant_id`, `status`) | campo ausente; escrita ignorada ou 400/422 |
| API4 Unrestricted Resource Consumption | `?limit=100000`, corpo enorme, upload acima do limite, consulta GraphQL profunda, exportação pesada repetida | 400, 413 ou 429 |
| API5 BFLA | usuário comum chama rota administrativa; troca de método (GET → DELETE) | 403 |
| API6 Sensitive Business Flows | compra, cadastro ou reserva automatizados em massa | limite por conta/dispositivo; antiautomação |
| API7 SSRF | campo de URL (webhook, importar por link, avatar) apontando para endereço interno, de metadados de nuvem ou esquema não HTTP | recusado por allowlist; nenhuma saída para destino interno |
| API8 Security Misconfiguration | CORS, erros verbosos, métodos desnecessários, TLS | ver [Configuração](#configuração-e-exposição) |
| API9 Improper Inventory Management | versão antiga (`/v1`) ativa sem os controles da atual; rota fora da documentação | desativada ou com os mesmos controles |
| API10 Unsafe Consumption of APIs | stub do terceiro devolve resposta enorme, malformada ou com redirecionamento | validada como entrada não confiável; timeout; sem redirecionamento cego |

- **BOLA/IDOR** é o defeito mais comum e o mais barato de automatizar. UUID
  não é controle de acesso: só dificulta adivinhar, e IDs vazam em URL, log
  e e-mail.
- **BFLA:** esconder o botão não protege a rota — teste a API, não a tela.
- **Mass assignment:** envie campos extras e **releia** o recurso; o status
  200 não prova nada, o estado relido prova.
- **Consumo de recursos** inclui custo: rota que envia SMS ou chama API paga
  sem limite vira prejuízo, não só lentidão.

## Controle de acesso na prática

Monte com o PO a matriz papel × ação × recurso; cada célula vira um caso
parametrizado.

| Ação | Anônimo | Dono | Outro usuário (mesmo tenant) | Outro tenant | Suporte | Admin do tenant |
| --- | --- | --- | --- | --- | --- | --- |
| Ver pedido | 401 | 200 | 404 | 404 | 200 (leitura) | 200 |
| Cancelar pedido pendente | 401 | 200 | 404 | 404 | 403 | 200 |
| Exportar pedidos do tenant | 401 | 403 | 403 | 403 | 403 | 200, só do próprio tenant |
| Alterar papel de usuário | 401 | 403 | 403 | 403 | 403 | 200, exceto promover a si mesmo |

- **Massa mínima:** dois usuários no tenant A, um no tenant B, um admin. SaaS
  sem teste entre tenants carrega seu maior risco sem verificação.
- **Onde trocar IDs:** caminho, query, corpo, cabeçalho, sub-recursos
  (`/pedidos/{id}/nota-fiscal`), downloads, exportações, filtros
  (`?clienteId=`), lotes, GraphQL e WebSocket.
- **403 ou 404**, desde que consistente (404 não revela que o recurso
  existe). Inaceitável é 200 — inclusive 200 com lista vazia quando a regra
  vira filtro: asserte sobre o conteúdo e, após um DELETE negado, confirme
  que o recurso ainda existe.

## Autenticação e sessão

**Login e enumeração.** Mensagem, status e tempo iguais para e-mail
inexistente e senha errada — em login, cadastro e recuperação (compare a
mediana de 20 tentativas de cada). Bloqueio ou atraso progressivo após N
falhas, por conta e por origem; durante o bloqueio **a senha correta também
é recusada** (senão é cosmético), e variar `X-Forwarded-For` não zera o
contador.

**Recuperação de senha.** Token longo, aleatório, de **uso único** e com
expiração curta; pedir outro invalida o anterior; trocar a senha encerra as
demais sessões. O link do e-mail usa o domínio configurado, não o cabeçalho
`Host` da requisição (confira na caixa de teste, ex.: Mailpit), e a página
de redefinição não repassa o token a terceiros via `Referer`.

**Sessão.** Logout invalida **no servidor**: reenviar o cookie ou token
antigo dá 401. O identificador muda no login (fixação de sessão). Expiração
por inatividade e absoluta conforme a política. Cookie de sessão com
`HttpOnly`, `Secure`, `SameSite=Lax` ou `Strict`, `Domain` restrito e
prefixo `__Host-` quando possível.

**JWT** — o servidor **recusa** (401) token com payload alterado e
assinatura original; sem assinatura ou com algoritmo diferente do
configurado (a biblioteca fixa o algoritmo esperado em vez de aceitar o do
cabeçalho); com `exp` vencido; com `iss`/`aud` de outro ambiente. O payload
é só Base64 — nada sensível dentro. Token em `localStorage` fica ao alcance
de qualquer script injetado; cookie `HttpOnly` reduz o risco. JWT sem estado
só "desloga" com expiração curta mais refresh revogável ou lista de
revogação — confirme qual é o comportamento esperado.

**OAuth 2.0 / OIDC** (boas práticas: RFC 9700). `redirect_uri` com
correspondência exata (variação de caminho, subdomínio ou parâmetro é
recusada); `state` ausente ou diferente do da sessão é recusado; PKCE com
`S256` obrigatório para clientes públicos; código de autorização de uso
único; login social não vincula conta existente por e-mail não verificado.

**MFA.** A rota pós-MFA não responde a quem só passou pela senha; código não
reaproveitável e com limite de tentativas; códigos de recuperação de uso
único; desativar MFA exige reautenticação.

## Injeção e validação de entrada

Entrada é dado, nunca código. Os testes usam **sentinelas**: valores que só
produzem efeito observável se o controle falhar.

| Tipo | Onde testar | Sentinela | Esperado |
| --- | --- | --- | --- |
| SQL | busca, filtros, ordenação, IDs | `D'Ávila` (nome legítimo) e um `'` isolado | nome salvo e buscado; `'` não gera 500 nem mensagem do banco |
| NoSQL | campos JSON | objeto onde se espera texto (`{"email": {"x": 1}}`) | 400/422 por tipo inválido |
| Comando do SO | campo que vira argumento de processo (nome de arquivo, host) | caracteres de shell (`;`, `\|`, `$()`) | rejeitados ou tratados literalmente |
| XSS refletido, armazenado e DOM | parâmetros de URL, campos salvos e relidos, fragmento `#` | HTML que definiria `window.__xss` | texto literal; `window.__xss` indefinido |
| Template (SSTI) | e-mail, PDF, mensagens renderizadas | `{{1337*7}}` | aparece literal; nunca `9359` |
| Path traversal | download por nome, parâmetro de arquivo | `../` e a forma codificada | 400/404; nunca arquivo fora do diretório |
| XXE | endpoints que aceitam XML | DTD declarando entidade interna com texto marcador | DTD rejeitada ou entidade não expandida |
| CRLF / log | cabeçalhos e campos logados | `%0d%0a` no valor | não cria cabeçalho nem linha de log |
| Redirecionamento aberto | `?next=`, `?returnUrl=` | domínio externo | só caminho relativo ou allowlist |

**Upload:** tipo verificado pelo conteúdo (assinatura do arquivo), não pela
extensão nem pelo `Content-Type`; tamanho acima do limite e arquivo
compactado que expande demais são recusados; o servidor gera o nome (nada de
`../`, nome gigante ou duplicado); SVG e HTML não são servidos inline do
mesmo domínio (`Content-Disposition: attachment` + `nosniff`); o arquivo de
teste EICAR é barrado pelo antivírus; EXIF com GPS é removido (também LGPD).

## Configuração e exposição

| Cabeçalho | Esperado |
| --- | --- |
| `Content-Security-Policy` | `script-src` sem `'unsafe-inline'`/`'unsafe-eval'` (ou com nonce/hash); `object-src 'none'`; `frame-ancestors` definido |
| `Strict-Transport-Security` | `max-age` ≥ 31536000 (um ano), `includeSubDomains` |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` ou mais restrito |
| `Permissions-Policy` | desliga câmera, microfone e geolocalização não usados |
| `X-Frame-Options` | `DENY`/`SAMEORIGIN` (legado; `frame-ancestors` prevalece) |

Cabeçalho costuma vir do host, CDN ou proxy, não do código: o teste
distingue ambiente (local pula com motivo registrado; homologação e produção
exigem). `frame-ancestors` só funciona por cabeçalho, não em `<meta>`.

**CORS:** envie `Origin: https://origem-nao-autorizada.test` e confirme que a
resposta **não** a ecoa em `Access-Control-Allow-Origin`, sobretudo com
`Access-Control-Allow-Credentials: true`; repita com `Origin: null` e com
domínio parecido (`exemplo.com.outro.test`).

**Exposição:** `/.env`, `/.git/config`, `/.DS_Store`, backups (`.zip`,
`.sql`), mapas de código (`.js.map`), endpoints de diagnóstico (ex.:
actuator), introspecção GraphQL e Swagger em produção sem decisão explícita.
Em SPA, rota inexistente devolve o HTML do app — aceite isso e recuse só o
conteúdo real. Procure padrões de segredo (chave de nuvem, `PRIVATE KEY`,
JWT) no JavaScript entregue. Forçar 404, 405 e 500 não mostra stack trace,
SQL, caminho de servidor nem versão de framework.

## Segredos e cadeia de suprimentos

```bash
gitleaks git . --redact -v                 # histórico do Git (8.19+; antes: gitleaks detect)
trufflehog git file://. --only-verified     # confirma a credencial com o provedor
npm audit --audit-level=high
pip-audit -r requirements.txt
osv-scanner scan source -r .                # v2; na v1: osv-scanner -r .
trivy fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --exit-code 1 .
syft dir:. -o cyclonedx-json > sbom.json    # SBOM em CycloneDX
```

- **Segredo vazado:** rotacione primeiro; apagar o commit não revoga nada.
- **Lockfile versionado** e instalação reprodutível (`npm ci`, hashes no
  pip). Dependência nova passa por revisão de nome (typosquatting:
  `reqeusts` por `requests`), idade, mantenedores e scripts de instalação.
- **Dependency confusion:** pacote interno cujo nome pode existir no
  registro público — fixe escopo e registro privado.
- **Actions e imagens fixadas por SHA/digest:** tags podem ser movidas
  (incidente `tj-actions/changed-files`, março de 2025).

## Ferramentas no pipeline

SAST (Semgrep, CodeQL, SonarQube) e segredos em todo PR; SCA (Dependabot,
npm audit, pip-audit, OSV-Scanner, Trivy) no PR **e** agendado, porque CVE
nova aparece em dependência antiga; DAST (OWASP ZAP) contra homologação.
Nenhuma delas acha IDOR ou falha de regra de negócio — para isso servem os
testes deste arquivo.

**ZAP baseline × full scan:** o baseline navega e analisa passivamente, sem
enviar ataques — rápido e seguro para todo PR. O full scan envia requisições
ativas: só em ambiente próprio, autorizado, fora do horário de uso.
`zap-api-scan.py` parte da definição OpenAPI. Saída do baseline: 0 ok, 1 há
FAIL, 2 só WARN, 3 erro. Gere a configuração com `-g` e ajuste cada regra
para IGNORE/WARN/FAIL em `-c`.

```yaml
# .github/workflows/seguranca.yml — em uso real, fixe actions e imagens por SHA/digest
name: seguranca
on: [pull_request]
jobs:
  sast:
    runs-on: ubuntu-latest
    container: semgrep/semgrep
    steps:
      - uses: actions/checkout@v4
      - run: semgrep scan --config p/default --error
  dast-baseline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: ZAP baseline em homologação
        env:
          ALVO: ${{ vars.URL_HOMOLOGACAO }}
        run: |
          mkdir -p zap && cp seguranca/zap-regras.tsv zap/ && chmod -R 777 zap
          docker run --rm -v "$PWD/zap:/zap/wrk:rw" ghcr.io/zaproxy/zaproxy:stable \
            zap-baseline.py -t "$ALVO" -c zap-regras.tsv -r relatorio-zap.html -J relatorio-zap.json
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: relatorio-zap, path: zap/ }
```

## Lógica de negócio

O defeito mais caro raramente é técnico: é a regra que o servidor não aplica.

- **Valores:** quantidade negativa ou zero, desconto acima de 100%, muitas
  casas decimais (o arredondamento favorece quem?), transferência para si.
- **Pular etapa:** chamar a confirmação sem pagamento aprovado; voltar a um
  passo concluído e reenviar.
- **Confiança no cliente:** preço, total, frete e desconto enviados no
  request são **recalculados** no servidor — altere-os em homologação e
  confira o valor gravado.
- **Condição de corrida:** cupom de uso único, último item do estoque, saque
  com saldo exato — requisições simultâneas (exemplo abaixo). Não reproduzir
  não prova ausência: a janela pode ser menor que a precisão do disparo.
  Confirme a proteção no código (transação, lock, restrição única).
- **Repetição:** reenviar a mesma requisição (duplo clique, retry) não
  duplica a cobrança — chave de idempotência.

## LGPD para QA

- **Dado pessoal fora do lugar:** log, URL (vai para histórico, proxy e
  `Referer`), mensagem de erro, ticket, print, vídeo e arquivo HAR (que leva
  cookies e tokens). Mascare a evidência antes de anexar.
- **Exclusão e anonimização testáveis:** após o pedido do titular, o dado
  some do banco, de índices de busca, caches, analytics e terceiros, conforme
  a política. Hash de CPF sem segredo é pseudonimização, não anonimização:
  há só ~10⁹ CPFs possíveis e o hash se reverte por força bruta.
- **Consentimento:** opt-in sem caixa pré-marcada, por finalidade, revogação
  tão fácil quanto a concessão; rastreadores não carregam antes do
  consentimento (confira as requisições de rede).
- **Minimização:** formulário pede só o necessário; API não devolve campo
  que a tela não usa. Direitos do titular (art. 18: acesso, correção,
  portabilidade, eliminação) são fluxos testáveis.
- **Vazamento de dado pessoal** é incidente: escale na hora ao encarregado
  (DPO); a comunicação à ANPD tem prazo regulamentado (Resolução CD/ANPD
  nº 15/2024).

## OWASP ASVS 5.0 como checklist

ASVS 5.0.0 (maio de 2025): cerca de 350 requisitos em 17 capítulos e três
níveis — **L1**, mínimo para qualquer aplicação; **L2**, aplicações com dados
sensíveis (a maioria dos sistemas de negócio); **L3**, críticas (saúde,
financeiro, infraestrutura). Escolha o nível pelo risco e classifique cada
requisito como teste automatizado, revisão ou "não se aplica" com motivo.

Capítulos: V1 Encoding and Sanitization · V2 Validation and Business Logic ·
V3 Web Frontend Security · V4 API and Web Service · V5 File Handling ·
V6 Authentication · V7 Session Management · V8 Authorization ·
V9 Self-contained Tokens · V10 OAuth and OIDC · V11 Cryptography ·
V12 Secure Communication · V13 Configuration · V14 Data Protection ·
V15 Secure Coding and Architecture · V16 Security Logging and Error
Handling · V17 WebRTC. Cite requisitos com a versão (`v5.0.0-6.2.1`): a
numeração muda entre edições.

## Testes automatizados de exemplo

pytest + requests contra homologação, contas sintéticas, credenciais do
ambiente. Não foram executados aqui — ajuste rotas e campos ao contrato.

```python
# conftest.py
import os
import pytest
import requests


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.environ["BASE_URL"]  # ex.: https://homolog.exemplo.com


def _sessao(base_url: str, prefixo: str) -> requests.Session:
    s = requests.Session()
    r = s.post(f"{base_url}/api/login", timeout=10, json={
        "email": os.environ[f"{prefixo}_EMAIL"], "senha": os.environ[f"{prefixo}_SENHA"]})
    r.raise_for_status()
    s.headers["Authorization"] = f"Bearer {r.json()['access_token']}"
    return s


@pytest.fixture(scope="session")
def usuario_a(base_url):  # tenant A, papel "cliente"
    return _sessao(base_url, "USUARIO_A")


@pytest.fixture(scope="session")
def usuario_b(base_url):  # tenant B, papel "cliente"
    return _sessao(base_url, "USUARIO_B")
```

```python
# test_seguranca_api.py
import os
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor

import pytest
import requests


@pytest.fixture
def pedido_de_a(base_url, usuario_a):
    r = usuario_a.post(f"{base_url}/api/pedidos", json={"descricao": f"idor-{uuid.uuid4()}"}, timeout=10)
    assert r.status_code == 201
    yield r.json()
    usuario_a.delete(f"{base_url}/api/pedidos/{r.json()['id']}", timeout=10)


@pytest.mark.parametrize("metodo, corpo", [("GET", None), ("PATCH", {"descricao": "alterado por B"}), ("DELETE", None)])
def test_outro_tenant_nao_acessa_pedido_alheio(base_url, usuario_a, usuario_b, pedido_de_a, metodo, corpo):
    url = f"{base_url}/api/pedidos/{pedido_de_a['id']}"
    r = usuario_b.request(metodo, url, json=corpo, timeout=10)
    assert r.status_code in (403, 404), f"{metodo} devolveu {r.status_code}"
    assert pedido_de_a["descricao"] not in r.text  # nada vaza no corpo do erro
    atual = usuario_a.get(url, timeout=10)          # o efeito é o que importa
    assert atual.status_code == 200 and atual.json()["descricao"] == pedido_de_a["descricao"]


def test_cliente_nao_se_promove_por_campo_extra(base_url, usuario_a):
    usuario_a.patch(f"{base_url}/api/usuarios/me", timeout=10,
                    json={"nome": "Ana Teste", "papel": "admin", "tenant_id": "outro"})
    eu = usuario_a.get(f"{base_url}/api/usuarios/me", timeout=10).json()
    assert eu["papel"] == "cliente" and eu["tenant_id"] != "outro"


def test_cabecalhos_de_seguranca(base_url):
    h = requests.get(base_url, timeout=10).headers
    csp = {p.split()[0].lower(): p.split()[1:] for p in h.get("Content-Security-Policy", "").split(";") if p.strip()}
    scripts = csp.get("script-src", csp.get("default-src", []))
    assert scripts and "'unsafe-eval'" not in scripts
    assert "'unsafe-inline'" not in scripts or any(s.startswith(("'nonce-", "'sha")) for s in scripts)
    assert "frame-ancestors" in csp
    hsts = dict(p.strip().partition("=")[::2] for p in h.get("Strict-Transport-Security", "").split(";"))
    assert int(hsts.get("max-age") or 0) >= 31536000
    assert h.get("X-Content-Type-Options", "").lower() == "nosniff"


def test_login_bloqueia_e_recusa_ate_a_senha_certa(base_url):
    email, bloqueio = os.environ["CONTA_LIMITE_EMAIL"], {429, 423}  # conta descartável; ajuste ao contrato
    status = []
    for i in range(15):
        status.append(requests.post(f"{base_url}/api/login", timeout=10,
                                    json={"email": email, "senha": f"errada-{i}"}).status_code)
        if status[-1] in bloqueio:
            break
    assert bloqueio & set(status), f"nenhum bloqueio em 15 tentativas: {status}"
    certa = requests.post(f"{base_url}/api/login", timeout=10,
                          json={"email": email, "senha": os.environ["CONTA_LIMITE_SENHA"]})
    assert certa.status_code != 200, "bloqueio cosmético: a senha correta entrou"


def test_cupom_de_uso_unico_vale_uma_vez_sob_concorrencia(base_url):
    token, cupom, n = os.environ["TOKEN_CLIENTE"], os.environ["CUPOM_USO_UNICO"], 20
    barreira = threading.Barrier(n)

    def aplicar(_):
        barreira.wait()  # todas as threads disparam juntas
        return requests.post(f"{base_url}/api/pedidos", timeout=15, headers={"Authorization": f"Bearer {token}"},
                             json={"itens": [{"produtoId": 42, "quantidade": 1}], "cupom": cupom}).status_code

    with ThreadPoolExecutor(max_workers=n) as pool:
        status = list(pool.map(aplicar, range(n)))
    assert status.count(201) == 1, f"cupom aceito {status.count(201)} vezes: {status}"
```

**XSS com sentinela** (pytest-playwright, sessão autenticada por
`storage_state`; se a aplicação remove HTML em vez de escapar, troque a
primeira asserção por "não contém a tag"):

```python
# test_xss.py
import os
import uuid

import pytest
from playwright.sync_api import Page, expect

BASE_URL = os.environ["BASE_URL"]
PAYLOADS = ['<img src=x onerror="window.__xss=1">', '"><svg onload="window.__xss=1">']


@pytest.mark.parametrize("payload", PAYLOADS)
def test_comentario_com_html_aparece_como_texto(page: Page, payload: str):
    dialogos = []
    page.on("dialog", lambda d: (dialogos.append(d.message), d.dismiss()))
    marcador = f"xss-{uuid.uuid4().hex[:8]}"
    page.goto(f"{BASE_URL}/produtos/42")
    page.get_by_label("Comentário").fill(f"{marcador} {payload}")
    page.get_by_role("button", name="Publicar").click()
    page.reload()  # armazenado: o valor volta do servidor
    expect(page.get_by_text(marcador)).to_contain_text(payload)
    assert page.evaluate("() => window.__xss === undefined")
    assert dialogos == []
```

## Como reportar vulnerabilidade

- **Canal restrito:** tracker com visibilidade limitada ou aviso privado de
  segurança do repositório. Ticket público leva título genérico ("Ajuste de
  autorização em pedidos"), sem passos, payload nem URL afetada.
- **Severidade por CVSS** (v4.0 desde novembro de 2023; v3.1 ainda comum em
  bases de CVE): 0,1–3,9 baixa; 4,0–6,9 média; 7,0–8,9 alta; 9,0–10,0
  crítica. Some o impacto de negócio — o CVSS não sabe que aquele endpoint
  expõe dados de saúde.
- **Evidência mascarada** (sem token, senha, cookie ou dado pessoal real);
  reteste após a correção, com teste de regressão no mesmo PR.
- Falha em sistema de terceiro achada por acaso: pare e reporte pelo canal
  do dono (arquivo `security.txt`, RFC 9116).

```markdown
**Título (restrito):** <componente> — <tipo de falha> — <condição>
**Severidade:** CVSS <versão> <vetor> = <nota> (<faixa>); impacto de negócio: <...>
**Ambiente, versão e contas de teste:** <...>
**Passos mínimos:** 1. ... 2. ...
**Esperado × obtido:** <...>
**Evidência (mascarada):** <requisição/resposta, ID de correlação>
**Correção sugerida e teste de regressão:** <...>
```
