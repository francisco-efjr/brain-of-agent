# Regras de detecção por classe de vulnerabilidade

Uso: guia para gerar CANDIDATOS na revisão de diff. O padrão de busca (Grep) aponta onde olhar; só vira achado depois de rastrear origem até uso (passo 5) e conferir a proteção existente. Padrões são pontos de partida: ajuste à linguagem e ao framework do projeto.

Fontes (redação própria): OWASP Cheat Sheet Series, CC BY-SA 4.0 (V-21 SQL, V-22 XSS, V-23 SSRF, V-24 senhas, V-36 sessão, V-37 CSRF, V-39 cripto, V-20 validação, V-19 segredos); OWASP Top 10:2025 (V-13); getsentry/skills (V-30, Apache-2.0). Itens marcados (Inferido) vêm de conhecimento estável do domínio, sem item V específico. Conferido em 2026-10-10; versões de bibliotecas e valores numéricos devem ser reconferidos.

## Sumário

SQL · Comando do SO e avaliação dinâmica · XSS · SSRF · Caminho de arquivo e upload · Desserialização e XML · Autenticação e senha · Sessão e CSRF · Autorização · Criptografia e TLS · Segredos · Falha aberta e erros · LLM no produto · Logging

## SQL (A05, V-21)

| Buscar | Achado quando | Não é achado quando | Correção |
| --- | --- | --- | --- |
| `execute\(\s*f["']`, `execute\(.*(\+|%|\.format)`, `text\(f`, `\.raw\(`, `RawSQL`, `\.extra\(`, `queryRawUnsafe`, template literal com `${` dentro de `query(` | valor com origem externa chega à string SQL | o valor vem de uma lista fixa no código (ex.: direção do ORDER BY mapeada de `{"asc":"ASC","desc":"DESC"}`) | consulta parametrizada (`%s`, `?`, `$1`, `:nome`); identificadores só por mapeamento fixo; conta do banco com mínimo privilégio |

SQL bruto dentro de ORM recebe o mesmo tratamento. Escapar manualmente é fraco e desencorajado pela fonte.

## Comando do SO e avaliação dinâmica (A05)

| Buscar | Achado quando | Correção |
| --- | --- | --- |
| `os\.system`, `subprocess\..*shell\s*=\s*True`, `os\.popen`, `child_process\.(exec\|execSync)`, `Runtime\.exec`, `shell_exec`, crase com interpolação (Ruby/PHP) | argumento ou comando contém dado externo | argv em lista sem shell (`subprocess.run([...])`), lista de valores permitidos, sem montar string de comando |
| `eval\(`, `new Function`, `exec\(` (Python), `render_template_string`, `Template\(` com entrada | expressão ou template vem de fora (execução de código, SSTI) | não avaliar dado externo; template fixo e dados como contexto |

## XSS (A05, V-22)

| Sink de risco | Achado quando | Correção |
| --- | --- | --- |
| `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `srcdoc`, atributos `on*`, `setTimeout("...")` com string | dado externo chega ao sink sem codificação por contexto | `textContent`, `createTextNode`, `setAttribute` com nome fixo |
| Escape hatches: `dangerouslySetInnerHTML`, `v-html`, `{@html}`, `\|safe`, `mark_safe`, `bypassSecurityTrust` | origem do HTML inclui usuário ou terceiro | sanitizador mantido (ex.: DOMPurify), sem alterar o HTML depois de sanitizar; CSP e Trusted Types como camada extra |
| URL em `href`/`src` vinda de fora | esquema não validado (`javascript:`) | permitir só `http:` e `https:` |

Camada 1 do plugin security-guidance (V-02) usa padrões parecidos; coincidência não prova achado.

## SSRF (A01 em 2025 segundo o brain, Inferido; API7, V-23)

| Buscar | Achado quando | Correção |
| --- | --- | --- |
| `requests\.(get\|post)`, `urllib`, `httpx`, `fetch(`, `axios`, `http\.Get`, `HttpClient`, `curl_exec` com URL ou host de fora (webhook, importar por link, avatar por URL, preview) | não há lista de destinos nem checagem de IP na camada de conexão; redirecionamentos seguidos | lista de destinos; montar a URL no código (esquema, porta e caminho fixos); redirecionamento desligado; resolver o nome, validar todos os IPs (loopback, privado, link-local, metadados 169.254.169.254, multicast) e conectar ao IP validado mantendo hostname para Host, SNI e certificado; mesma política em retries; IMDSv2 |

Checagem apenas na string da URL é insuficiente (DNS rebinding, redirecionamento).

## Caminho de arquivo e upload (A01/A05, V-20)

- Buscar: `open(`, `send_file`, `sendFile`, `path.join(`, `File(`, `readFile(` com parâmetro de requisição; nomes de arquivo vindos do cliente.
- Achado: caminho montado com dado externo sem resolver e comparar com o diretório base.
- Correção: nome gerado no servidor; `Path(base).resolve()` e `candidate.resolve().is_relative_to(base)` (Python 3.9+) ou equivalente; tipo verificado pelo conteúdo, não por extensão nem `Content-Type`; limite de tamanho e de expansão de arquivos compactados; SVG/HTML do usuário não servido inline no mesmo domínio.

## Desserialização e XML (A08)

| Buscar | Achado quando | Correção |
| --- | --- | --- |
| `pickle\.load`, `yaml\.load\(` sem `SafeLoader`, `marshal`, `ObjectInputStream`, `unserialize\(`, `Marshal\.load`, `BinaryFormatter`, `node-serialize` | dado de fora é desserializado | formato de dados (JSON) com validação de schema; `yaml.safe_load` |
| Parsers XML com entidades externas ou DTD habilitados (`resolve_entities=True`, `DocumentBuilderFactory` sem desabilitar DOCTYPE) | XML de fora (Inferido) | desabilitar DTD e entidades externas; biblioteca endurecida (ex.: `defusedxml` em Python) |

## Autenticação e senha (A07, A04, V-24)

- Hash rápido para senha (`md5`, `sha1`, `sha256` simples): achado. Correção: Argon2id (mínimos observados em 2026-10-10: m=19456 KiB, t=2, p=1; reconferir a fonte antes de citar como vigente), ou scrypt/bcrypt já adotados (bcrypt: fator 10 ou mais, senha de até 72 bytes).
- Senha em texto, em log ou em URL: achado.
- Comparação de token, HMAC ou hash com `==`: usar comparação de tempo constante (`hmac.compare_digest`, `crypto.timingSafeEqual`) (Inferido).
- Mensagens ou tempos diferentes para "usuário não existe" e "senha errada" no login, cadastro e recuperação: enumeração de contas (Inferido, brain QA).
- Token de recuperação reutilizável, sem expiração curta ou derivado do `Host` da requisição (Inferido, brain QA).
- JWT: aceitar o algoritmo do cabeçalho em vez de fixar o esperado, `alg: none`, ausência de `exp`/`aud`/`iss`: achado (Inferido; sem fonte primária validada, ver lacuna de JWT).

## Sessão e CSRF (A07/A01, V-36, V-37)

- Cookie de sessão sem `Secure`, `HttpOnly` ou `SameSite` explícito; token de sessão em `localStorage`/`sessionStorage`: achado.
- ID de sessão não regenerado após login ou mudança de privilégio; logout que só apaga o cookie do cliente: achado.
- Rota que altera estado, autenticada por cookie, sem token CSRF nem verificação de Origin/Fetch Metadata; `@csrf_exempt`, `csrf: false`; GET que altera estado: achado. API só com token em cabeçalho tem risco de CSRF diferente.
- CORS que ecoa `Origin` com `Access-Control-Allow-Credentials: true`, ou aceita `null`: achado.

## Autorização (A01, V-18, API1/API3/API5)

- Rota nova sem decorador ou middleware de autenticação e autorização que as vizinhas têm.
- Busca por identificador sem filtro de dono/tenant: `findById(req.params`, `.get(pk=`, `.find(params[:id])`, `findById(` (Spring), `Model::find($id)`.
- Atribuição em massa: `**request.json`, `Model(**data)`, `update(req.body)`, `fields = '__all__'`, `permit!`: campos como `role`, `tenant_id`, `status` aceitos do cliente.
- Papel, tenant ou usuário lidos do corpo/cabeçalho da requisição em vez da sessão.
- Para profundidade, use a skill `access-control-review`.

## Criptografia e TLS (A04, V-39)

Achado para: ECB, DES/3DES/RC4, IV ou nonce fixo, chave no código, na imagem ou em variável de ambiente versionada, PRNG comum (`Math.random`, `random.random`, `rand()`) para token, senha-reset ou ID de sessão, RSA sem OAEP para cifrar, algoritmo inventado, verificação de certificado desligada (`verify=False`, `rejectUnauthorized: false`, `InsecureSkipVerify`). Correção: AES-GCM (ou outro modo autenticado) por biblioteca padrão, CSPRNG (`secrets`, `crypto.randomBytes`), chaves em KMS/HSM/gerenciador de segredos. TLS em trânsito não foi lido nas fontes (lacuna): trate achados de TLS como Inferido.

## Segredos (A02/A04, V-19)

Padrões de formato (Inferido; formatos mudam): `AKIA[0-9A-Z]{16}`, `-----BEGIN [A-Z ]*PRIVATE KEY-----`, `gh[pousr]_[A-Za-z0-9]{36,}`, `xox[baprs]-`, `sk_live_`, JWT `eyJ[A-Za-z0-9_-]{10,}\.eyJ`, atribuições `(secret|token|passw|api[_-]?key)\s*[:=]\s*["'][^"']{8,}`. Nunca reproduza o valor: mostre prefixo mascarado e local. Detalhe e ordem de resposta: skill `secrets-supply-chain-review`.

## Falha aberta e tratamento de erro (A10)

- `except:\s*pass`, `catch\s*\([^)]*\)\s*\{\s*\}`, `return True`/`next()` dentro de `except`/`catch` em código de autorização, antifraude ou validação: a falha libera em vez de negar.
- Exceção que vira resposta com stack trace, SQL ou caminho de servidor.
- Operação parcial não revertida (cobrou sem criar o pedido). Padrão correto: negar por padrão e reverter.

## LLM no produto (V-14, V-27 seção IA)

- Saída do modelo usada em SQL, shell, HTML, caminho de arquivo ou chamada de API sem validação por schema (LLM05).
- Entrada de usuário concatenada na instrução de sistema (LLM01); segredo ou regra sensível dentro do prompt de sistema (LLM07).
- Ferramenta com efeito (enviar, pagar, apagar) acionável pelo modelo sem confirmação humana (LLM06); sem teto de tokens, chamadas ou custo por usuário (LLM10).

## Logging (A09)

Registrar senha, token, `Authorization`, corpo inteiro de requisição ou dado pessoal: achado. Registrar login falho, acesso negado e mudança de permissão sem dado sensível é esperado; ausência desses eventos em código de autenticação novo é VERIFY (o alerta dispara?).
