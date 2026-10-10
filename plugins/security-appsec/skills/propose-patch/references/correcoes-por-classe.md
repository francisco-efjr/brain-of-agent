# Correções por classe: defesa primária e trechos

Princípio: a correção ataca a causa (onde dado de atacante vira código, consulta, destino ou decisão), na defesa que a fonte aponta como primária. Trechos são ilustrativos, em Python/JavaScript; adapte à linguagem e às bibliotecas do projeto e confirme APIs e versões antes de aplicar. Fontes (redação própria, CC BY-SA 4.0 nas cheat sheets OWASP): V-21 SQL, V-22 XSS, V-23 SSRF, V-18 autorização, V-24 senhas, V-37 CSRF, V-36 sessão, V-39 criptografia, V-20 validação. Itens sem V são conhecimento estável (Inferido). Conferido em 2026-10-10.

## Sumário

SQL · XSS · SSRF · Autorização e tenant · Mass assignment · Comando do SO · Caminho de arquivo · Desserialização · Senha · Token e comparação · Criptografia · CSRF e sessão · Redirecionamento aberto · Falha aberta · Segredo no código

## SQL (V-21)

Defesa primária: consulta parametrizada. Identificadores e direção de ORDER BY não são parametrizáveis: vêm de lista fixa.

```python
# antes (injeção)
cur.execute(f"SELECT * FROM orders WHERE id = {order_id}")
# depois (parâmetros + dono; %s em psycopg, ? em sqlite3)
cur.execute("SELECT * FROM orders WHERE id = %s AND user_id = %s", (order_id, current_user.id))

# ordenação dinâmica: colunas e direção só por mapeamento fixo
COLUNAS = {"data": "created_at", "total": "total"}
DIRECAO = {"asc": "ASC", "desc": "DESC"}
coluna, direcao = COLUNAS[col], DIRECAO[dir]     # KeyError -> responder 400
cur.execute(f"SELECT id, total FROM orders WHERE user_id = %s ORDER BY {coluna} {direcao}", (current_user.id,))
```

```js
// Node (pg)
await db.query('SELECT id, total FROM invoices WHERE id = $1 AND org_id = $2', [req.params.id, req.user.orgId]);
```

Pegadinhas: `LIKE` com o `%` dentro do parâmetro (`f"%{termo}%"` como valor, não na string SQL); `IN` com um placeholder por item; ORM com `raw()` precisa do mesmo tratamento; conta do banco com mínimo privilégio como camada extra. Escapar aspas manualmente não é correção.

## XSS (V-22)

Defesa primária: codificação por contexto na saída; sinks seguros.

```js
el.textContent = comentario;                    // em vez de el.innerHTML = comentario
// React: <p>{comentario}</p> (escape automático). Se o usuário escreve HTML de verdade:
const limpo = DOMPurify.sanitize(htmlDoUsuario);  // biblioteca mantida; não altere o HTML depois
// <div dangerouslySetInnerHTML={{ __html: limpo }} />
```

URLs vindas de fora: aceite só `http:` e `https:` (`new URL(valor, base).protocol`). CSP e Trusted Types são camadas extras, não substituem a correção do sink.

## SSRF (V-23)

Defesa primária: lista de destinos permitidos; montar a requisição no código (esquema, porta e caminho fixos); redirecionamento desligado; validar os IPs resolvidos e **conectar ao IP validado**, mantendo hostname para Host, SNI e certificado.

```python
import ipaddress, socket

def ips_permitidos(host: str, porta: int = 443) -> list[str]:
    ips = []
    for *_, sockaddr in socket.getaddrinfo(host, porta, type=socket.SOCK_STREAM):
        ip = ipaddress.ip_address(sockaddr[0])
        if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
            ip = ip.ipv4_mapped                    # ::ffff:127.0.0.1 vira 127.0.0.1
        if not ip.is_global or ip.is_multicast:    # barra loopback, privado, link-local (inclui 169.254.169.254), reservado
            raise ValueError(f"destino não permitido: {host}")
        ips.append(str(ip))
    return ips
```

Isto só valida. Chamar `requests.get(url)` depois reabre a janela de DNS rebinding: o cliente resolve de novo. Para fechar, o cliente HTTP precisa receber o IP validado (adaptador de transporte que fixa o IP e preserva SNI/certificado do hostname) ou o tráfego sai por um proxy de saída com lista de destinos. Aplique a mesma política em cada retry e em cada hop de redirecionamento se algum for permitido. Em nuvem, exija IMDSv2 e desative IMDSv1. Lista de bloqueio é último recurso. Se a biblioteca do projeto não permite fixar o IP, registre isso como limite do patch e recomende o proxy.

## Autorização e tenant (V-18; tenant Inferido)

Defesa primária: checagem no servidor, por objeto, antes da leitura; identificador do dono vem da sessão.

```python
# Django: consulta já filtrada; objeto alheio é "não encontrado"
fatura = get_object_or_404(Fatura, pk=pk, org_id=request.user.org_id)
```

```js
const fatura = await Fatura.findOne({ where: { id: req.params.id, orgId: req.user.orgId } });
if (!fatura) return res.status(404).end();      // 404 consistente; não revela existência
```

Prefira um escopo central (queryset/escopo por tenant, política única) a repetir `if` em cada rota. Cubra também cache (chave com tenant), export, busca, fila e job. Teste de negação entre usuários e tenants relendo o recurso (ver `access-control-review`).

## Mass assignment (V-15 API3)

```python
CAMPOS_EDITAVEIS = {"nome", "telefone"}
dados = {k: v for k, v in payload.items() if k in CAMPOS_EDITAVEIS}   # nunca **payload direto no modelo
```

Ou esquema de entrada com campos explícitos que rejeita extras (por exemplo, pydantic v2 com `extra='forbid'`; confirme a versão). Campos como `role`, `tenant_id`, `owner_id`, `status`, `price` nunca vêm do cliente.

## Comando do SO

```python
# antes: subprocess.run(f"git log -n 5 {nome}", shell=True)
subprocess.run(["git", "log", "-n", "5", "--", nome], check=True, timeout=30)   # argv, sem shell
```

Valide o argumento contra lista permitida; `--` impede que um valor começando com `-` vire opção. Evite `eval`/`exec` e templates montados com entrada.

## Caminho de arquivo (Python 3.9+)

```python
base = Path(DIR_UPLOADS).resolve()
alvo = (base / nome_do_cliente).resolve()
if not alvo.is_relative_to(base):
    abort(400)
```

Melhor: o servidor gera o nome do arquivo (ID aleatório) e guarda o nome original só como metadado.

## Desserialização

Troque `pickle.load`/`yaml.load` por JSON com validação de esquema ou `yaml.safe_load`. Se o formato precisa mesmo ser binário, assine e verifique a integridade ANTES de desserializar.

## Senha (V-24; números são mínimos observados em 2026-10-10, reconferir a fonte)

```python
from argon2 import PasswordHasher          # argon2-cffi; memory_cost em KiB
ph = PasswordHasher(time_cost=2, memory_cost=19456, parallelism=1)
hash_guardado = ph.hash(senha)
ph.verify(hash_guardado, senha)             # levanta VerifyMismatchError se não confere
if ph.check_needs_rehash(hash_guardado):    # reescreva o hash no próximo login bem-sucedido
    hash_guardado = ph.hash(senha)
```

Se o projeto já usa bcrypt/scrypt, mantenha e corrija parâmetros (bcrypt fator 10 ou mais, senhas de até 72 bytes). Sal único por senha (a biblioteca faz); pimenta fora do banco; parâmetros guardados junto ao hash; aceitar Unicode completo. Migração de hashes antigos: re-hash no login.

## Token e comparação

```python
import hmac, secrets
token = secrets.token_urlsafe(32)                # CSPRNG; nunca random.random()
ok = hmac.compare_digest(token_recebido, token_esperado)   # tempo constante
```

Token de recuperação de senha: aleatório, longo, de uso único, expiração curta, invalidado ao pedir outro e ao trocar a senha (Inferido, brain QA); o link usa o domínio configurado, não o cabeçalho `Host`.

## Criptografia (V-39)

```python
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
aes = AESGCM(chave)                                # 256 bits, vinda de KMS/HSM/gerenciador, nunca do código
nonce = os.urandom(12)                             # único para cada mensagem sob a mesma chave
blob = nonce + aes.encrypt(nonce, dados, aad)      # aad: contexto autenticado (ex.: ID do registro)
# ler: aes.decrypt(blob[:12], blob[12:], aad)
```

Modo autenticado (GCM/CCM), nunca ECB; chave separada dos dados (DEK protegida por KEK); rotação por comprometimento, criptoperíodo ou limite do modo; minimizar o dado armazenado. Não invente algoritmo. Preferir API de alto nível da biblioteca quando existir.

## CSRF e sessão (V-37, V-36)

Defesa primária: token sincronizador atrelado à sessão em toda requisição que altera estado (ou double-submit assinado, ou cabeçalho customizado em API com CORS restrito); Fetch Metadata e verificação de Origin como contingência; `SameSite` Lax/Strict como defesa em profundidade; GET nunca altera estado.

```text
Set-Cookie: __Host-sid=<ID-OPACO>; Path=/; Secure; HttpOnly; SameSite=Lax
```

Regenere o ID de sessão após login e mudança de privilégio; logout invalida no servidor; sem token em `localStorage`. O prefixo `__Host-` exige `Secure`, `Path=/` e ausência de `Domain`.

## Redirecionamento aberto

Aceite só caminho relativo local: o destino começa com `/`, não com `//` nem `/\`, e `urlsplit` não retorna esquema nem host; ou use lista de destinos.

## Falha aberta (A10)

```python
try:
    permitido = politica.avalia(usuario, recurso)
except Exception:
    log.exception("falha na avaliação de política")   # sem dado sensível
    permitido = False                                  # erro nega
```

Operações parciais são revertidas (transação); respostas de erro não trazem stack, SQL nem caminhos.

## Segredo no código

Mover para variável de ambiente injetada ou cofre, ler em tempo de execução. O valor antigo continua comprometido: revogar e rotacionar é a correção real e é ação do usuário. Detalhe na skill `secrets-supply-chain-review`.
