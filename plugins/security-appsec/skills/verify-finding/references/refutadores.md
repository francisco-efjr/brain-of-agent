# Catálogo de refutadores por classe de achado

Uso: na etapa 3 de `verify-finding`, para cada classe, quais proteções legítimas derrubam o achado, o que é preciso ver no código para aceitá-las e que desvios as anulam. Redação própria a partir das cheat sheets OWASP (CC BY-SA 4.0: V-21 SQL, V-22 XSS, V-23 SSRF, V-18 autorização, V-24 senhas, V-37 CSRF, V-39 cripto), de V-29 e V-30 (regras de não sinalizar) e de conhecimento estável (Inferido, quando indicado). Conferido em 2026-10-10.

## Sumário

1. Regra geral de aceitação de um refutador
2. SQL
3. XSS
4. SSRF
5. Autorização (IDOR/BOLA/tenant)
6. Comando do SO e avaliação dinâmica
7. Segredos
8. Criptografia e senhas
9. CSRF e sessão
10. Desserialização
11. Exemplo de decisão Rebaixado

## 1. Regra geral de aceitação de um refutador

Um refutador só vale se você pode apontar a linha. Pergunte, nesta ordem:

1. **Está no caminho?** A proteção executa antes do sink em TODOS os caminhos que chegam a ele, não só no principal.
2. **Cobre o caso?** Tipo, tamanho, encoding e contexto de saída coincidem com o ataque descrito.
3. **É efetiva?** Não é comentário, nome sugestivo (`sanitize`, `safeQuery`) nem função que não faz o que o nome diz: leia o corpo.
4. **Resiste ao desvio?** Não há escape hatch, SQL bruto, flag desligada em produção ou exceção por papel que a contorne.
5. **Quem controla a entrada?** Se só o operador (variável de ambiente, arquivo de configuração do servidor) controla, o achado de entrada de atacante cai; reveja se um workflow não confiável pode definir esse valor.

## 2. SQL (V-21)

| Refutador | Aceitar se | Anulado por |
| --- | --- | --- |
| Consulta parametrizada | todos os valores externos vão como parâmetros (`%s`/`?`/`$1`/`:nome`) e nenhuma parte da string SQL vem de fora | fragmento concatenado ao lado do parâmetro; `LIKE` com `%` montado por concatenação; `IN` montado por join de strings |
| Identificador por lista fixa | o nome de coluna/tabela/direção é escolhido por mapeamento no código (`{"asc":"ASC","desc":"DESC"}.get(dir, "ASC")`) | `.get(dir, dir)` (padrão devolve o próprio valor); lista montada a partir de entrada |
| ORM sem SQL bruto | só filtros e métodos do ORM | `raw()`, `extra()`, `text(f"...")`, `$queryRawUnsafe`, `.order_by(request.GET[...])` com nome de campo livre (campo arbitrário vaza dados por ordenação) |
| Tipagem forte | o valor é convertido para inteiro/UUID antes e a conversão rejeita o resto | conversão que falha aberta (`int(x) if x.isdigit() else x`) |

## 3. XSS (V-22)

| Refutador | Aceitar se | Anulado por |
| --- | --- | --- |
| Escape automático do framework | dado vai por interpolação padrão (JSX `{x}`, template `{{ x }}`) em contexto de corpo HTML | `dangerouslySetInnerHTML`, `v-html`, `{@html}`, `|safe`, `mark_safe`, `bypassSecurityTrust*`; dado em contexto de atributo `href`/`src` com `javascript:`; dado dentro de `<script>` ou em handler `on*` |
| Sanitizador mantido | DOMPurify (ou equivalente) aplicado ao HTML e o resultado não é alterado depois | sanitizar e depois concatenar/regex; versão defasada; configuração que permite tags/atributos perigosos |
| Origem confiável | HTML vem só de conteúdo escrito por administrador de confiança e passa por revisão | campo editável por usuário comum; conteúdo de terceiro (RSS, e-mail, markdown de usuário renderizado sem sanitização) |
| CSP estrita | camada extra; reduz o dano | não refuta sozinha: CSP e Trusted Types são defesa em profundidade, não prova de que o sink é seguro |

## 4. SSRF (V-23)

| Refutador | Aceitar se | Anulado por |
| --- | --- | --- |
| Destino fixo | host, esquema, porta e caminho vêm de configuração do servidor; o usuário fornece só um ID | usuário influencia o host (subdomínio, `@`, `#`, `\\`), ou o caminho com `..` para outro serviço |
| Lista de destinos + checagem de IP na conexão | host na lista E IP resolvido validado E conexão feita ao IP validado E redirecionamentos desligados | validação só na string; DNS resolvido duas vezes (rebinding); redirecionamento seguido; esquema `file://`, `gopher://` |
| Egress controlado | proxy de saída ou regra de rede bloqueia faixas internas e metadados (confirmar fora do código) | só presumido: sem prova de configuração, é Suposição |

## 5. Autorização (V-18, API1/API3/API5)

| Refutador | Aceitar se | Anulado por |
| --- | --- | --- |
| Middleware global "negar por padrão" | a rota em questão passa por ele (provar) e a política olha o objeto | rota registrada fora do router protegido; lista de exceções; método HTTP não coberto |
| Consulta já filtrada pela sessão | `where id = ? and owner_id = session.user` (ou escopo global do ORM por tenant) | escopo global desligado em `unscoped`, `all_objects`, `IgnoreQueryFilters`, ou ausente em consultas brutas |
| Identificador derivado da sessão | o ID nunca vem do cliente | ID também aceito em query/corpo como alternativa |
| Objeto inexistente para o atacante | nunca é referenciável por ele | "ninguém conhece o UUID": não é controle |
| Impacto só no próprio usuário | o efeito atinge apenas dados do próprio requisitante | efeito em recurso compartilhado, contagem global, e-mail enviado a terceiros |

## 6. Comando do SO e avaliação dinâmica

| Refutador | Aceitar se | Anulado por |
| --- | --- | --- |
| argv em lista, sem shell | `subprocess.run([...])` com `shell=False` e argumentos como itens | argumento começando com `-` interpretado como opção (injeção de argumento): exige `--` ou validação |
| Valor de lista fixa | o argumento é escolhido de um conjunto fechado | conjunto ampliado por entrada |
| Origem do operador | comando vem de configuração do servidor | configuração editável por tenant ou usuário |

## 7. Segredos

| Refutador | Aceitar se | Anulado por |
| --- | --- | --- |
| Valor claramente falso (`<SEU_TOKEN>`, `changeme`, fixture de teste isolada) | o valor não funciona em nenhum ambiente (prova: formato inválido ou documentado como exemplo) | prefixo de produção real (`sk_live_...`), chave que passa na checagem de formato, mesmo repositório com ambientes reais |
| Já revogada | há evidência de revogação feita pelo titular | "provavelmente já foi trocada": sem prova, trate como comprometida |

Nunca valide um segredo tentando usá-lo. Mostre prefixo mascarado e local, sem o valor.

## 8. Criptografia e senhas (V-24, V-39)

| Refutador | Aceitar se | Anulado por |
| --- | --- | --- |
| Uso não criptográfico | MD5/SHA-1 como checksum de cache ou ETag, sem papel de segurança (regra de não sinalizar de V-30) | mesmo hash usado para senha, token, assinatura ou comparação de integridade com atacante |
| Biblioteca de senha apropriada | Argon2id/bcrypt/scrypt com parâmetros mínimos atuais (reconferir a fonte); sal por senha | hash rápido; bcrypt com senha acima de 72 bytes sem tratamento; parâmetros baixos |
| PRNG comum em contexto não sensível | embaralhar lista na interface | token, ID de sessão, reset de senha, nonce |

## 9. CSRF e sessão (V-37, V-36)

| Refutador | Aceitar se | Anulado por |
| --- | --- | --- |
| Rota sem cookie de sessão | autenticação por token em cabeçalho `Authorization`; o navegador não anexa credencial sozinho | cookie aceito também como alternativa; CORS permissivo com credenciais |
| Token CSRF validado ou verificação de Origin/Fetch Metadata | validação no servidor para toda rota que altera estado | `csrf_exempt` na rota; apenas `SameSite` (defesa em profundidade, não isolada); XSS no mesmo site contorna CSRF |

## 10. Desserialização

| Refutador | Aceitar se | Anulado por |
| --- | --- | --- |
| Formato de dados | JSON/Protobuf com validação de esquema | `pickle`, `yaml.load` sem SafeLoader, `ObjectInputStream`, `unserialize`, `BinaryFormatter` com dado externo |
| Fonte confiável e assinada | integridade verificada antes de desserializar, chave fora do alcance do atacante | assinatura verificada depois de desserializar |

## 11. Exemplo de decisão Rebaixado

Achado: "XSS armazenado no campo bio". Leitura: o campo é renderizado por `{{ bio }}` (escape automático) em `profile.html:12`, mas há um segundo template `email_digest.html:31` com `{{ bio|safe }}` enviado a outros usuários. Decisão: a tela de perfil está Refutada; o e-mail é outro caminho, com HTML enviado a terceiros, sem prova de que clientes de e-mail executem script. Veredito final: Rebaixado, severidade Média, VERIFY: "o digest sanitiza `bio` antes (linha 22)? Clientes de e-mail renderizam links `javascript:`?". Resposta ao usuário: o achado original estava errado no local e certo na classe; mantenha a investigação no e-mail.
