# Checklist completo de segurança de aplicações

Uso: checklist de revisão por área, com rótulo do grupo NIST SSDF 1.1 (PO preparar a organização, PS proteger o software, PW produzir software bem protegido, RV responder a vulnerabilidades) e a fonte. Redação própria, destilada de fontes CC BY-SA 4.0 (ver `fontes.md`). Parâmetros numéricos: "mínimos hoje" observados em 2026-10-10; reconfira na fonte antes de citar como vigentes.

## Sumário

1. Como usar e rótulos
2. Autenticação e senhas
3. Sessão
4. CSRF
5. JWT, OAuth/OIDC e MFA (Inferido)
6. Validação de entrada e injeção
7. XSS e front-end
8. SSRF e chamadas externas
9. Upload e parsing
10. Criptografia aplicada
11. Configuração, headers, CORS e exposição
12. Logging e alertas
13. API (Top 10 2023)
14. Lógica de negócio
15. Containers (Docker)
16. Privacidade por fluxo (lacuna LGPD)
17. LLM e agentes no produto
18. Checklist de entrega (9 itens)

## 1. Como usar e rótulos

- Para cada item: **OK** (evidência `arquivo:linha`), **Achado**, **Verificação pendente**, **Não aplicável** (motivo) ou **Não verificável** (sem acesso).
- Evidência é leitura de código ou saída de comando desta sessão. "Parece certo" não é evidência.
- Itens marcados *Inferido (brain)* vêm do conteúdo próprio do brain-of-agent e não foram reconferidos em fonte oficial.
- Proporcionalidade: aplique só as áreas que o escopo toca. No modo SEGURANCA-COMPLETO, aplique a matriz inteira (`assets/templates/matriz-aplicabilidade-seguranca.md`).

## 2. Autenticação e senhas

| Item | Verificação | SSDF | Fonte |
| --- | --- | --- | --- |
| Senhas com Argon2id (m=19456 KiB, t=2, p=1 como mínimo; alternativas m=12288 com t=3 e m=7168 com t=5), scrypt (N=2^17, r=8, p=1), bcrypt (fator >= 10) ou PBKDF2-HMAC-SHA256 (600.000 iterações, se FIPS for exigido) | Grep por `md5`, `sha1`, `sha256(` aplicado a senha; ler a função de hash | PW | V-24 |
| bcrypt trunca em 72 bytes: limitar ou pré-processar a senha | Ler o ponto de hash e o limite de tamanho | PW | V-24 |
| Sal único por senha, pimenta fora do banco, parâmetros guardados junto ao hash e reescrita do hash no próximo login | Ler o login e o esquema da coluna | PW | V-24 |
| Comparação de segredo em tempo constante (`hmac.compare_digest`, `crypto.timingSafeEqual`) | Grep por `==` em token, assinatura, hash | PW | V-24 |
| Mensagem, status e tempo iguais para e-mail inexistente e senha errada, em login, cadastro e recuperação | Ler os três handlers; comparar mediana de 20 tentativas se houver ambiente de teste | PW | brain QA (Inferido) |
| Bloqueio ou atraso progressivo por conta e por origem; durante o bloqueio a senha correta também é recusada | Ler o contador; variar `X-Forwarded-For` não pode zerá-lo | PW | brain QA (Inferido) |
| Recuperação de senha: token longo, aleatório, uso único, expiração curta, invalida o anterior, troca de senha encerra outras sessões; link usa domínio configurado, não o cabeçalho `Host` | Ler gerador, armazenamento e montagem do link | PW | brain QA (Inferido) |
| Unicode completo aceito na senha (sem filtro de caracteres) | Ler a validação de senha | PW | V-24 |

Lacuna: MFA, recuperação de conta e JWT não têm fonte primária validada (seção 5).

## 3. Sessão

| Item | Verificação | SSDF | Fonte |
| --- | --- | --- | --- |
| ID de sessão com >= 64 bits de entropia de gerador criptográfico (>= 128 bits para ID customizado) | Ler o gerador; `Math.random` ou `random.random` é achado | PW | V-36 |
| Cookie com `Secure`, `HttpOnly`, `SameSite` explícito e prefixo `__Host-` quando possível | Ler a configuração de cookie ou os cabeçalhos de resposta | PW | V-36 |
| Nenhum token de sessão em `localStorage` ou `sessionStorage` | Grep por `localStorage.setItem` com token | PW | V-36 |
| ID regenerado após login e após mudança de privilégio; ID não emitido pelo servidor é rejeitado (fixação) | Ler o fluxo de login | PW | V-36 |
| Timeouts ocioso e absoluto no servidor; logout invalida no servidor (reenviar o cookie antigo dá 401) | Ler o armazenamento de sessão | PW | V-36 |
| `Cache-Control: no-store` em respostas autenticadas sensíveis; ID de sessão fora de URL e de log (registrar hash) | Grep por log de sessão e por ID em query | PW | V-36 |

Os valores de timeout da fonte são referência por risco, não norma.

## 4. CSRF

| Item | Verificação | SSDF | Fonte |
| --- | --- | --- | --- |
| Rota que altera estado e usa cookie de sessão tem token sincronizador, double-submit assinado (HMAC ligado à sessão) ou verificação de `Origin`/`Sec-Fetch-Site` | Listar rotas POST/PUT/PATCH/DELETE e o middleware | PW | V-37 |
| GET nunca altera estado | Grep por handlers GET com escrita | PW | V-37 |
| API JSON recusa tipos simples (`application/x-www-form-urlencoded`, `multipart/form-data`, `text/plain`) | Ler o parser e o `Content-Type` aceito | PW | V-37 |
| `SameSite` Lax ou Strict é defesa em profundidade, não a única; XSS contorna CSRF | Confirmar que há outra camada | PW | V-37 |
| API com token em cabeçalho (sem cookie) tem risco de CSRF diferente: registrar como Não aplicável com motivo | Confirmar que não há cookie de autenticação | PW | V-37 |

## 5. JWT, OAuth/OIDC e MFA (Inferido, brain QA)

Sem fonte primária validada (cheat sheet de JWT retornou 404; RFC 8725 não lido). Use como lista de perguntas, rotulada Inferido:

- JWT: biblioteca fixa o algoritmo esperado em vez de aceitar o do cabeçalho; recusa token sem assinatura, com payload alterado, `exp` vencido ou `iss`/`aud` de outro ambiente; nada sensível no payload (é só Base64); revogação via expiração curta mais refresh revogável ou lista de revogação.
- OAuth/OIDC (o brain cita RFC 9700; não reconferido): `redirect_uri` com correspondência exata, `state` conferido, PKCE `S256` para clientes públicos, código de uso único, login social sem vincular conta por e-mail não verificado.
- MFA: rota pós-MFA não responde a quem só passou pela senha; código sem reuso e com limite de tentativas; códigos de recuperação de uso único; desativar MFA exige reautenticação.

## 6. Validação de entrada e injeção

| Item | Verificação | SSDF | Fonte |
| --- | --- | --- | --- |
| Validação na borda por lista de permitidos: tipo, faixa, tamanho, enum, formato; limites de tamanho e profundidade antes de parsear | Ler o schema ou validador de cada entrada | PW | V-20 |
| Canonicalizar uma vez, sem decodificar de novo; regex casa o valor inteiro, com comprimento limitado e timeout tratado como falha | Grep por `re.search` sem âncoras em validação | PW | V-20 |
| SQL por parâmetros ou ORM; identificadores e direção de `ORDER BY` vêm de lista fixa no código; SQL bruto dentro de ORM recebe o mesmo tratamento | Grep por f-string, `+`, `%` e `.format` em SQL | PW | V-21 |
| Conta do banco com mínimo privilégio, uma por aplicação | Ler a configuração de conexão | PW, PS | V-21 |
| Comando de SO, template e NoSQL: sem concatenação de entrada; NoSQL rejeita objeto onde se espera texto | Grep por `os.system`, `exec(`, `child_process.exec`, `shell=True` | PW | V-02, V-20 |
| Validação não substitui parametrização, codificação de saída nem autorização | Confirmar que as três camadas existem | PW | V-20 |
| Log da rejeição sem valor bruto e com escape (CRLF não forja linha) | Ler o logger de validação | PW | V-20 |

## 7. XSS e front-end

| Item | Verificação | SSDF | Fonte |
| --- | --- | --- | --- |
| Saída codificada por contexto (corpo HTML, atributo entre aspas, JS apenas dentro de string entre aspas, CSS só em valor, URL só http/https) | Ler o template e o encoder | PW | V-22 |
| Sinks seguros: `textContent`, `insertAdjacentText`, `value`, `className`, `setAttribute` com nome fixo, `createTextNode` | Grep por sinks de risco | PW | V-22 |
| Sinks de risco com dado externo são achado: `innerHTML`, `outerHTML`, `document.write`, atributos de evento, `srcdoc`, `eval`, `setTimeout` com string | Grep e rastrear a origem | PW | V-22 |
| Escape hatches (`dangerouslySetInnerHTML`, `bypassSecurityTrustAs*`, `unsafeHTML`, `v-html`, `mark_safe`) só com sanitizador mantido (ex.: DOMPurify, sem alterar o HTML depois de sanitizar) e justificativa | Grep e ler a sanitização | PW | V-22, V-30 |
| CSP e Trusted Types como camadas extras, não como única defesa; WAF não é defesa recomendada | Ler o cabeçalho de CSP | PW, PS | V-22 |

## 8. SSRF e chamadas externas

| Item | Verificação | SSDF | Fonte |
| --- | --- | --- | --- |
| URL vinda de fora (webhook, importar por link, avatar) passa por lista de destinos permitidos; a requisição é montada no código com esquema, porta e caminho fixos | Grep por `fetch(`, `requests.get`, `http.Client` com URL de entrada | PW | V-23 |
| Redirecionamentos desativados ou revalidados a cada salto | Ler a configuração do cliente HTTP | PW | V-23 |
| O nome é resolvido, os IPs são validados contra faixas permitidas e a conexão vai ao IP validado, mantendo hostname para Host, SNI e certificado (contra DNS rebinding); mesma política em retries | Ler a camada de conexão, não só a string da URL | PW | V-23 |
| Deny-list só como último recurso: metadados `169.254.169.254`, localhost, RFC 1918, link-local e unique-local IPv6, multicast | Ler a lista | PW | V-23 |
| IMDSv2 ativo e IMDSv1 desativado; segmentação de rede | Perguntar ao dono da nuvem (Não verificável no código) | PS | V-23 |

## 9. Upload e parsing

- Nome, conteúdo e tipo do arquivo são não confiáveis: tipo pelo conteúdo (assinatura), não por extensão ou `Content-Type`; tamanho máximo e limite de expansão de arquivo compactado; o servidor gera o nome (nada de `../`) (V-20; brain QA, Inferido).
- SVG e HTML não são servidos inline no mesmo domínio: `Content-Disposition: attachment` e `X-Content-Type-Options: nosniff` (brain QA, Inferido).
- Desserialização de dado não confiável (`pickle`, `yaml.load` sem loader seguro, desserialização nativa de Java e .NET) é achado de severidade alta; XML sem DTD externa (XXE) (V-02 cita `pickle` na camada 1; demais Inferido).
- Dados de upload processados por worker: o worker também é fronteira de confiança (ver `threat-model`).

## 10. Criptografia aplicada

| Item | Verificação | SSDF | Fonte |
| --- | --- | --- | --- |
| AES (>= 128 bits, ideal 256) com modo autenticado (GCM ou CCM); sem ECB; IV gerado pela biblioteca, nunca fixo | Grep por `ECB`, IV literal | PW | V-39 |
| Chaves, IVs e tokens por CSPRNG (`secrets`, `crypto.randomBytes`, `SecureRandom`); PRNG comum para token é achado | Grep por `random()` em token | PW | V-39 |
| Chave pública: esquema híbrido (HPKE) ou RSA >= 2048 com OAEP; plano de migração pós-quântica | Ler o esquema | PW | V-39 |
| Chave nunca no código, no repositório ou em variável de ambiente; vive em KMS, HSM ou gerenciador de segredos; DEK protegida por KEK; rotação por comprometimento ou criptoperíodo | Grep por chave literal; ler o carregamento | PW, PS | V-39 |
| Minimizar dado sensível armazenado; não inventar algoritmo | Perguntar a necessidade do dado | PW | V-39 |

Lacuna: TLS e gestão de chaves em trânsito não foram lidos; trate como Não verificável e peça a documentação da plataforma.

## 11. Configuração, headers, CORS e exposição

Brain QA (Inferido, não reconferido):

| Cabeçalho | Esperado |
| --- | --- |
| `Content-Security-Policy` | `script-src` sem `'unsafe-inline'`/`'unsafe-eval'` (ou com nonce/hash); `object-src 'none'`; `frame-ancestors` definido |
| `Strict-Transport-Security` | `max-age` >= 31536000, `includeSubDomains` |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` ou mais restrito |
| `Permissions-Policy` | desliga câmera, microfone e geolocalização não usados |

- Cabeçalho costuma vir do host, CDN ou proxy: registre o ambiente em que foi observado. `frame-ancestors` só funciona por cabeçalho, não em `<meta>`.
- CORS: a resposta não ecoa uma `Origin` arbitrária em `Access-Control-Allow-Origin`, sobretudo com `Access-Control-Allow-Credentials: true`; teste `Origin: null` e domínio parecido. CORS não substitui autorização.
- Exposição: `/.env`, `/.git/config`, backups, mapas de código (`.js.map`), endpoints de diagnóstico, introspecção GraphQL e Swagger em produção só por decisão explícita; erros 404, 405 e 500 não mostram stack, SQL, caminho ou versão. Debug desligado, conta padrão removida.

## 12. Logging e alertas

- Registrar login falho, acesso negado, troca de senha, de MFA e de permissão, com quem, quando e onde; sem senha, token, ID de sessão (registrar hash) nem dado pessoal (V-36; brain QA).
- O alerta dispara: teste o alerta, não só o log (A09, brain QA, Inferido).
- Falha fechada: exceção em autorização ou antifraude nega; JSON truncado ou tipo errado dá 4xx, não 500 com stack; operação parcial é revertida (A10, V-13).

## 13. API (Top 10 2023)

Resumo; perguntas completas em `owasp-e-asvs.md` e `autorizacao-e-tenant.md`.

- API1 BOLA e API3 BOPLA: checagem por objeto e por propriedade; leitura sem campo interno; escrita ignora campo protegido.
- API2: rota sem token, token expirado ou adulterado dá 401; login, OTP e reset com limite.
- API4: `limit`, corpo, upload, profundidade de GraphQL e exportação têm teto; rota que envia SMS ou chama API paga tem limite (custo).
- API5 BFLA: usuário comum não chama rota administrativa; troca de método não contorna.
- API6: fluxo sensível (compra, cadastro, reserva) tem limite por conta ou dispositivo.
- API7 SSRF: seção 8. API8: seção 11. API9: versão antiga (`/v1`) e endpoint de depuração inventariados. API10: resposta de terceiro validada como entrada não confiável, com timeout e sem redirecionamento cego (webhooks, MCP).

## 14. Lógica de negócio

- Quantidade negativa ou zero, desconto acima de 100%, muitas casas decimais (o arredondamento favorece quem?), transferência para si mesmo (brain QA).
- Preço, total, frete e desconto enviados pelo cliente são recalculados no servidor; etapa pulada (confirmar sem pagamento aprovado) é recusada.
- Corrida (cupom de uso único, último item, saque com saldo exato): a proteção está no código (transação, lock, restrição única); não reproduzir não prova ausência. Reenvio da mesma requisição não duplica cobrança (idempotência).

## 15. Containers (Docker)

| Item | SSDF | Fonte |
| --- | --- | --- |
| Usuário não root (`USER`, `-u`, userns, rootless) | PS | V-38 |
| `docker.sock` não exposto (montar read-only não torna a API somente leitura) | PS | V-38 |
| `--cap-drop all` com adições mínimas; nunca `--privileged`; `no-new-privileges` | PS | V-38 |
| Segredos pelo mecanismo de secrets; nada em `ENV`, `ARG`, imagem ou comando | PS | V-38, V-19 |
| `--read-only` com `--tmpfs`; limites de recursos | PS | V-38 |
| Varredura de imagem e lint de Dockerfile no CI; host e engine atualizados | PS, RV | V-38 |

Lacuna: Kubernetes, IaC e cloud não foram cobertos; trate como Não verificável.

## 16. Privacidade por fluxo (lacuna LGPD/GDPR)

Sem norma primária lida: não cite artigos da LGPD nem resoluções da ANPD; recomende o encarregado ou assessoria jurídica. O que se pode revisar tecnicamente (brain fullstack, Inferido):

- Por fluxo: finalidade, dados necessários, destinatários, retenção, descarte e evidência de acesso. Minimizar payload e telemetria; hash de identificador não garante anonimização (hash de CPF sem segredo é reversível por força bruta).
- Dado pessoal fora do lugar: log, URL (histórico, proxy, `Referer`), mensagem de erro, ticket, print e HAR (leva cookies e tokens). Mascarar evidência.
- Exclusão e anonimização testáveis em banco, índices, caches, analytics e terceiros. Consentimento sem caixa pré-marcada; rastreadores não carregam antes do consentimento.
- Pergunta ao usuário (lacuna 10): quais políticas de retenção e treinamento se aplicam ao código enviado ao modelo? Não afirme a política.

## 17. LLM e agentes no produto

Saída do LLM é entrada não confiável: validar por schema antes de SQL, shell ou HTML; não concatenar entrada do usuário à instrução de sistema; segredo ou dado de cliente fora do prompt; teto de tokens, chamadas e custo por usuário; ferramentas do agente com mínimo privilégio e confirmação para ação de saída. Perguntas completas por categoria em `owasp-e-asvs.md`; tríade em `conteudo-nao-confiavel.md` (V-11, V-14, V-27).

## 18. Checklist de entrega (9 itens)

Brain fullstack (Inferido), adaptado:

- [ ] Ativos, ameaças e fronteiras de confiança identificados (Suposição rotulada onde faltou descrição).
- [ ] Autorização no servidor por ação, objeto e tenant.
- [ ] Testes negativos verificam ausência de dados e efeitos indevidos (releem o estado, não confiam no 200).
- [ ] Entradas, uploads, URLs e saída contextual revisados.
- [ ] Sessão, revogação e comportamento após logout verificados.
- [ ] Segredos e dados pessoais não aparecem em fontes, logs nem evidências.
- [ ] Dependências e scripts de instalação avaliados proporcionalmente.
- [ ] Logs registram evento útil sem payload sensível.
- [ ] Correção revalidada pela reprodução original e por casos adjacentes.

Um achado completo contém pré-condição, caminho de exploração (em ambiente autorizado), impacto, evidência redigida e correção verificável; hipótese é classificada separadamente de vulnerabilidade reproduzida. ASVS é critério de aceite, não selo: não afirme conformidade só por usar a lista.
