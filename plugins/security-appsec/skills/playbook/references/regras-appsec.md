# Regras de segurança com ID, severidade, detecção e correção

Molde adaptado de `github/awesome-copilot` `security-and-owasp.instructions.md` (MIT; V-27), com tom calmo e razão em cada regra. Conteúdo técnico destilado de V-20 a V-24, V-36 a V-39, V-02 e V-14 (OWASP CC BY-SA 4.0: redação própria). Referência de consulta sob demanda: não cole tudo em CLAUDE.md (para isso, use `claude-md-snippets.md`).

## Sumário

1. Como ler uma regra
2. Injeção (INJ)
3. Autenticação e sessão (AUT)
4. Autorização (AZ)
5. Segredos e criptografia (SEG)
6. Headers e configuração (CFG)
7. Front-end (FE)
8. Dependências e CI (DEP)
9. API (API)
10. IA e LLM (IA)
11. Logging e falha (LOG)
12. Regras de framework (sob demanda)

## 1. Como ler uma regra

`ID · severidade · detecção · categoria · correção`.

Severidade (sem caixa alta, com consequência prática):
- **bloqueia merge**: explorável por atacante sem condição incomum; corrigir antes de integrar.
- **corrigir neste ciclo**: exige condição adicional ou tem impacto limitado; criar tarefa com prazo.
- **sugestão**: endurecimento sem cenário imediato.

Detecção: padrão de busca (aponta candidato, não prova) ou checagem manual. Todo candidato exige rastrear origem ao uso e controles existentes (`revisao-de-diff.md`). Os padrões de grep abaixo são pontos de partida: ajuste à linguagem e ao framework e confirme APIs na versão instalada.

## 2. Injeção (INJ)

| ID | Severidade | Detecção | Cat. | Correção |
| --- | --- | --- | --- | --- |
| INJ-01 | bloqueia merge | f-string, `+`, `%`, `.format`, template literal com SQL e valor externo; SQL bruto dentro de ORM (`raw`, `execute`, `$queryRawUnsafe`) | A05 | Consulta parametrizada; identificador e direção de `ORDER BY` por lista fixa no código (V-21) |
| INJ-02 | bloqueia merge | `os.system`, `subprocess(..., shell=True)`, `child_process.exec`, `Runtime.exec` com entrada | A05 | Chamar o programa com lista de argumentos sem shell; validar por lista de permitidos |
| INJ-03 | bloqueia merge | `eval(`, `new Function`, `exec(` com dado externo | A05 | Remover; usar parser dedicado |
| INJ-04 | corrigir neste ciclo | NoSQL: filtro construído de JSON do cliente (operadores `$ne`, `$gt` aceitos) | A05 | Validar tipo (texto onde se espera texto); schema |
| INJ-05 | bloqueia merge | Template renderizado a partir de string do usuário (SSTI) | A05 | Template fixo no código; dados só como variáveis |
| INJ-06 | bloqueia merge | `open(base + nome)` com `nome` do cliente (path traversal); `../` | A01/A05 | Gerar o nome no servidor; resolver o caminho e conferir que está dentro do diretório base |
| INJ-07 | bloqueia merge | `pickle.loads`, `yaml.load` sem loader seguro, desserialização nativa de dado não confiável (Java, .NET: Inferido) | A08 | Formato de dados (JSON) com schema; loader seguro |
| INJ-08 | corrigir neste ciclo | Parser XML sem desabilitar DTD/entidades externas (XXE; Inferido) | A05 | Desabilitar DTD e entidades externas |
| INJ-09 | corrigir neste ciclo | Cabeçalho ou log com valor do cliente sem tratar CR/LF | A05/A09 | Rejeitar ou escapar quebras de linha |
| INJ-10 | sugestão | Validação ausente ou por lista de bloqueio (V-20) | A05 | Lista de permitidos: tipo, faixa, tamanho, formato; canonicalizar uma vez |

Ruim e bom (INJ-01), ver `padroes-e-antipadroes.md` P-C1.

## 3. Autenticação e sessão (AUT)

| ID | Severidade | Detecção | Cat. | Correção |
| --- | --- | --- | --- | --- |
| AUT-01 | bloqueia merge | `md5`, `sha1`, `sha256` aplicado a senha; senha em texto | A04/A07 | Argon2id (mínimo atual m=19456 KiB, t=2, p=1; reconferir), scrypt ou bcrypt (V-24) |
| AUT-02 | corrigir neste ciclo | bcrypt sem limite de 72 bytes | A07 | Limitar ou pré-processar a senha (V-24) |
| AUT-03 | corrigir neste ciclo | `==` para comparar token, assinatura ou hash | A07 | Comparação em tempo constante |
| AUT-04 | bloqueia merge | ID de sessão do cliente aceito sem emissão do servidor; ID não regenerado no login | A07 | Regenerar no login e na mudança de privilégio (V-36) |
| AUT-05 | corrigir neste ciclo | Cookie de sessão sem `Secure`, `HttpOnly` ou `SameSite` | A07 | Configurar flags; prefixo `__Host-` quando possível (V-36) |
| AUT-06 | bloqueia merge | Token de sessão em `localStorage` ou `sessionStorage` | A07 | Cookie `HttpOnly` (V-36) |
| AUT-07 | corrigir neste ciclo | Logout só limpa o cliente | A07 | Invalidar no servidor; timeouts ocioso e absoluto no servidor |
| AUT-08 | corrigir neste ciclo | Mensagens ou tempos diferentes para e-mail inexistente e senha errada; sem limite de tentativas | A07 | Resposta uniforme; bloqueio ou atraso progressivo (brain QA, Inferido) |
| AUT-09 | bloqueia merge | Reset de senha com token curto, reutilizável, sem expiração, ou link montado do cabeçalho `Host` | A07 | Token longo, aleatório, uso único, expira; domínio configurado (brain QA, Inferido) |
| AUT-10 | bloqueia merge | JWT: algoritmo vindo do cabeçalho do token; sem checagem de `exp`, `iss`, `aud`; aceita `alg: none` | A07 | Fixar o algoritmo esperado na biblioteca; validar claims (Inferido; sem fonte primária) |
| AUT-11 | bloqueia merge | Rota que altera estado, com cookie de sessão, sem token CSRF nem verificação de origem; GET que altera estado | A01 | Token sincronizador ou double-submit assinado; `Origin`/`Sec-Fetch-Site`; `SameSite` só como camada extra (V-37) |

## 4. Autorização (AZ)

| ID | Severidade | Detecção | Cat. | Correção |
| --- | --- | --- | --- | --- |
| AZ-01 | bloqueia merge | Handler que busca objeto por ID da URL sem filtrar dono ou tenant | A01/API1 | Buscar já escopado à sessão; 404 se ausente (V-18) |
| AZ-02 | bloqueia merge | Tenant (`tenant_id`, `org_id`) lido do corpo, query ou cabeçalho como autoridade | A01 | Tenant da sessão; validar contra o objeto (Inferido) |
| AZ-03 | bloqueia merge | Rota administrativa sem checagem de papel no servidor; só o botão escondido | A01/API5 | Checagem global (middleware ou filtro) e por função |
| AZ-04 | bloqueia merge | Mass assignment: `Model(**request.json)`, `update(request.body)` sem lista de campos | A01/API3 | Lista de campos graváveis; ignorar `papel`, `tenant_id`, `status` |
| AZ-05 | corrigir neste ciclo | Resposta traz campos internos (hash, flags) | API3 | DTO explícito de saída por papel |
| AZ-06 | corrigir neste ciclo | Checagem de autorização em algumas rotas e não em exportação, download, GraphQL ou WebSocket | A01 | Aplicar a mesma política globalmente |
| AZ-07 | bloqueia merge | Autorização depende de UUID difícil de adivinhar | A01 | Checar dono e tenant; UUID não é controle |
| AZ-08 | corrigir neste ciclo | Exceção ou serviço de autorização fora do ar libera (falha aberta) | A10 | Negar e registrar sem detalhe ao cliente |

Detalhes e testes de negação em `autorizacao-e-tenant.md`.

## 5. Segredos e criptografia (SEG)

| ID | Severidade | Detecção | Cat. | Correção |
| --- | --- | --- | --- | --- |
| SEG-01 | bloqueia merge | Chaves de nuvem, `PRIVATE KEY`, JWT, tokens com prefixos de provedor, `.env` versionado | A02/A04 | Revogar, rotacionar, apagar, registrar; cofre ou variável injetada (V-19); nunca reproduzir o valor |
| SEG-02 | corrigir neste ciclo | `ENV`/`ARG` de Docker com segredo | A02 | Secrets do orquestrador (V-19, V-38) |
| SEG-03 | bloqueia merge | AES em modo ECB; IV fixo ou reutilizado | A04 | AES-GCM ou CCM; IV pela biblioteca (V-39) |
| SEG-04 | bloqueia merge | `random`/`Math.random` para token, senha temporária ou ID de sessão | A04 | CSPRNG (`secrets`, `crypto.randomBytes`) |
| SEG-05 | bloqueia merge | Chave de criptografia no código ou no repositório | A04 | KMS, HSM ou gerenciador; DEK protegida por KEK (V-39) |
| SEG-06 | corrigir neste ciclo | RSA sem OAEP ou com módulo menor que 2048 bits | A04 | HPKE ou RSA >= 2048 com OAEP (V-39) |
| SEG-07 | sugestão | Algoritmo "caseiro" ou composição de primitivas | A04 | Biblioteca padrão |

## 6. Headers e configuração (CFG) — brain QA, Inferido

| ID | Severidade | Detecção | Cat. | Correção |
| --- | --- | --- | --- | --- |
| CFG-01 | corrigir neste ciclo | CSP ausente ou com `'unsafe-inline'`/`'unsafe-eval'` em `script-src` | A02 | Nonce ou hash; `object-src 'none'`; `frame-ancestors` por cabeçalho |
| CFG-02 | corrigir neste ciclo | HSTS ausente ou `max-age` menor que um ano | A02 | `max-age=31536000; includeSubDomains` |
| CFG-03 | sugestão | Faltam `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy` | A02 | Definir |
| CFG-04 | bloqueia merge | CORS ecoa `Origin` arbitrária com `Allow-Credentials: true` | A02 | Lista exata de origens |
| CFG-05 | corrigir neste ciclo | Debug ligado, stack trace ao cliente, `/.env`, `/.git/config`, `.js.map` expostos | A02 | Desligar; remover do deploy |

## 7. Front-end (FE)

| ID | Severidade | Detecção | Cat. | Correção |
| --- | --- | --- | --- | --- |
| FE-01 | bloqueia merge | `innerHTML`, `outerHTML`, `document.write`, `srcdoc`, atributos de evento com dado externo | A05 | `textContent` e sinks seguros; sanitizador mantido (V-22) |
| FE-02 | bloqueia merge | `dangerouslySetInnerHTML`, `v-html`, `bypassSecurityTrustAs*`, `unsafeHTML`, `mark_safe` com dado externo | A05 | Remover o desvio ou sanitizar (DOMPurify) sem alterar depois (V-22) |
| FE-03 | corrigir neste ciclo | `setTimeout`/`setInterval` com string; `eval` | A05 | Passar função |
| FE-04 | corrigir neste ciclo | Link `href` com `javascript:` vindo de dado | A05 | Permitir só `http`/`https` |
| FE-05 | sugestão | Sem CSP ou Trusted Types | A02 | Camada extra, não defesa única |
| FE-06 | corrigir neste ciclo | `target="_blank"` sem `rel="noopener"` em navegadores antigos (Inferido) | A02 | `rel="noopener noreferrer"` |

## 8. Dependências e CI (DEP)

| ID | Severidade | Detecção | Cat. | Correção |
| --- | --- | --- | --- | --- |
| DEP-01 | corrigir neste ciclo | Sem lockfile; instalação não reprodutível | A03 | Versionar lockfile; `npm ci`; hashes no pip (brain QA, Inferido) |
| DEP-02 | bloqueia merge | Pacote novo com nome suspeito (typosquatting), sem manutenção, ou sugerido por conteúdo externo | A03 | Verificar existência, origem, mantenedores e scripts de instalação |
| DEP-03 | corrigir neste ciclo | Actions por tag móvel ou `@main`; imagens por tag | A03 | Fixar por SHA ou digest (V-04) |
| DEP-04 | bloqueia merge | Workflow que executa código de PR de fork com segredos; `pull_request_target` com checkout do PR (Inferido) | A03/A08 | Separar; sem segredos em PR de fork |
| DEP-05 | corrigir neste ciclo | Permissões do workflow amplas | A03 | Mínimo por job (V-04) |
| DEP-06 | sugestão | Sem SBOM por release | A03 | CycloneDX por release (V-25) |

## 9. API (API)

| ID | Severidade | Detecção | Cat. | Correção |
| --- | --- | --- | --- | --- |
| API-01 | bloqueia merge | URL de entrada buscada pelo servidor sem lista de destinos e checagem de IP na conexão | A01/API7 | Lista, resolução, IP validado, sem redirect (V-23) |
| API-02 | corrigir neste ciclo | Paginação sem teto; corpo sem limite; rota que envia SMS ou chama API paga sem limite | API4 | Tetos e rate limiting (achado em API pública, login e financeiro) |
| API-03 | corrigir neste ciclo | Versão antiga ou endpoint de depuração ativo | API9 | Desativar ou aplicar os mesmos controles |
| API-04 | corrigir neste ciclo | Resposta de terceiro usada sem validação, timeout ou limite; redirecionamento seguido às cegas | API10 | Tratar como entrada não confiável |
| API-05 | corrigir neste ciclo | Webhook sem verificação de assinatura | API2/API10 | Verificar assinatura em tempo constante antes de processar (Inferido) |
| API-06 | corrigir neste ciclo | Fluxo sensível (compra, cupom, reserva) sem limite por conta ou idempotência | API6 | Limites e chave de idempotência |

## 10. IA e LLM (IA)

| ID | Severidade | Detecção | Cat. | Correção |
| --- | --- | --- | --- | --- |
| IA-01 | bloqueia merge | Entrada do usuário concatenada à instrução de sistema | LLM01 | Separar papéis; conteúdo do usuário como dado (V-27) |
| IA-02 | bloqueia merge | Saída do LLM usada em SQL, shell, HTML ou template sem validação | LLM05 | Tratar como entrada não confiável; validar por schema; rejeitar o que não conferir (V-27) |
| IA-03 | corrigir neste ciclo | Validação da saída ausente: sem schema | LLM05 | JSON Schema ou equivalente |
| IA-04 | bloqueia merge | Agente com dados privados, leitura de conteúdo de terceiros e envio externo sem confirmação | LLM06 | Remover uma perna, separar sessões ou confirmar a saída (V-11) |
| IA-05 | corrigir neste ciclo | Segredo ou dado de cliente no prompt de sistema | LLM07/LLM02 | Retirar; buscar por ferramenta com permissão (V-33) |
| IA-06 | corrigir neste ciclo | Sem teto de tokens, chamadas ou custo por usuário | LLM10 | Limites e orçamento |

## 11. Logging e falha (LOG)

| ID | Severidade | Detecção | Cat. | Correção |
| --- | --- | --- | --- | --- |
| LOG-01 | corrigir neste ciclo | Log com senha, token, ID de sessão, dado pessoal | A09 | Remover; registrar hash do ID de sessão (V-36) |
| LOG-02 | corrigir neste ciclo | Login falho, acesso negado ou mudança de permissão sem registro; alerta que nunca foi testado | A09 | Registrar quem, quando e onde; testar o alerta (brain QA) |
| LOG-03 | corrigir neste ciclo | `except: pass` ou `catch {}` em checagem de segurança; 500 com stack | A10 | Negar e registrar; resposta genérica |
| LOG-04 | corrigir neste ciclo | Operação parcial sem reversão (cobrou sem criar pedido) | A10 | Transação ou compensação |

## 12. Regras de framework (sob demanda)

Regras de framework datam rápido: confirme na documentação da versão instalada e carregue só a do framework em uso. Pontos de partida a confirmar (todos Inferido, sem fonte validada):

- Django: `mark_safe`, `|safe`, `extra()`/`raw()`, `CSRF_COOKIE_*`, `SESSION_COOKIE_*`, `DEBUG`, `ALLOWED_HOSTS`.
- Flask/Jinja: `render_template_string` com entrada, `|safe`, `SECRET_KEY` fixa.
- Express/Node: `helmet`, `cors` com origem aberta, `child_process.exec`, `req.body` direto no ORM.
- Spring: `@PreAuthorize` ausente, desserialização, actuator exposto.
- React/Next: `dangerouslySetInnerHTML`, variáveis públicas com segredo (`NEXT_PUBLIC_`), Server Actions sem checagem de autorização.
- Go: `html/template` versus `text/template`, `database/sql` com `fmt.Sprintf`.
- Angular: `bypassSecurityTrustAs*`. Vue: `v-html`.
