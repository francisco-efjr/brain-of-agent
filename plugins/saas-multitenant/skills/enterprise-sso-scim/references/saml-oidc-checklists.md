# Checklists de SAML e de validação do ID Token OIDC

Redação própria. Fontes: OWASP SAML Security Cheat Sheet (V-35), OASIS SAML (Committee Draft de 2008, só contexto), OpenID Connect Core 1.0 § 3.1.3.7 (V-46), OWASP Multi-Tenant (V-49). Conferido em 2026-10-10. Rótulos: Verificado (lido na fonte), Inferido (nosso), Não verificável. Use biblioteca mantida: este arquivo diz o que verificar na integração e como testar, não como implementar o parser.

## 1. SAML: checagens obrigatórias na resposta (V-35, Verificado)

| # | Checagem | Falha que previne | Teste negativo |
| --- | --- | --- | --- |
| 1 | Validar a assinatura com a chave obtida do metadado do IdP e guardada localmente; ignorar `KeyInfo` do próprio documento | atacante assina com a própria chave e a embute | resposta assinada por outra chave com `KeyInfo` apontando para ela |
| 2 | Rejeitar SHA-1 | colisão | resposta com `SignatureMethod` SHA-1 |
| 3 | `Audience` igual ao EntityID do SP | asserção emitida para outro SP aceita aqui | Audience alterado |
| 4 | `Destination` igual à URL do ACS | resposta redirecionada de outro destino | Destination alterado |
| 5 | `InResponseTo` igual ao ID do pedido que o SP enviou (fluxo iniciado pelo SP) | resposta não solicitada | InResponseTo de pedido inexistente |
| 6 | `Recipient` no `SubjectConfirmationData` igual ao ACS | asserção reutilizada em outro SP | Recipient alterado |
| 7 | `NotBefore` e `NotOnOrAfter` respeitados, com tolerância pequena de relógio (valor definido pelo projeto: Suposição) | asserção expirada ou antecipada | asserção vencida e asserção futura |
| 8 | Detectar replay em resposta não solicitada: guardar o ID da asserção até `NotOnOrAfter` | reenvio da mesma resposta | mesma resposta enviada duas vezes |
| 9 | Defesas contra XML Signature Wrapping: validar contra schema local, XPath absoluto, não usar `getElementsByTagName` antes da validação da assinatura, assinatura cobrindo a asserção efetivamente usada | asserção forjada ao lado de uma assinada | documento com asserção extra não assinada |

Notas:
- A visão geral SAML da OASIS é um Committee Draft 02 de 25/03/2008, não normativo, embora o título HTML diga "OASIS Standard" (V-35). Não cite como norma.
- Metadado do IdP é dado enviado pelo cliente: valide a origem (URL HTTPS confiada ou upload pelo admin autenticado do tenant), nunca busque metadado de URL fornecida por usuário sem restringir destinos (SSRF; conhecimento estável) e registre o evento.
- Rotação de certificado: aceite mais de um certificado do metadado durante a janela (conhecimento estável; confirme na biblioteca).
- O SP-iniciado é o fluxo mais fácil de proteger (InResponseTo); aceite o iniciado pelo IdP apenas com detecção de replay e com a regra do tenant clara (Inferido).

## 2. Ligação identidade para tenant (Inferido)

| Elemento | Regra |
| --- | --- |
| Chave da identidade externa | `(tenant_id, idp_issuer_ou_entity_id, subject_ou_nameid)` único |
| E-mail | atributo, não chave global; comparar sem diferenciar caixa |
| Conexão | cada tenant tem uma ou mais conexões (`sso_connections`), com protocolo, emissor, chaves ou JWKS, `client_id` e estado |
| Resolução do tenant no login | domínio do e-mail ou slug da organização leva à conexão; a conexão leva ao tenant; o tenant nunca vem de parâmetro livre do retorno |
| Usuário em dois tenants | mesma pessoa pode ter vínculos distintos; troca de contexto explícita (V-23, convites) |

## 3. OIDC: validação do ID Token (V-46, § 3.1.3.7)

Verificado na seção lida (100 mil de 285 mil caracteres da especificação). Palavras MUST e SHOULD conforme a especificação.

| # | Verificação | Nível na especificação |
| --- | --- | --- |
| 1 | `iss` exatamente igual ao Issuer da conexão | MUST |
| 2 | `aud` contém o `client_id`; rejeitar se o cliente não for audiência válida | MUST |
| 3 | `azp`, quando presente, igual ao `client_id` | SHOULD |
| 4 | Assinatura validada com o `alg` do cabeçalho e as chaves do Issuer; RS256 por padrão ou o algoritmo registrado | MUST (assinatura); SHOULD (alg padrão) |
| 5 | Para HS256, HS384 e HS512 a chave é o `client_secret` | regra da especificação |
| 6 | `exp` no futuro | MUST |
| 7 | `nonce`, se enviado no pedido, presente e igual; checado contra replay | MUST (igualdade); SHOULD (replay) |
| 8 | `acr` e `auth_time` quando solicitados ou com `max_age` | SHOULD |
| 9 | Janela de `iat`: a especificação não a exige; o cliente define o que aceita | definida pelo projeto: registrar o valor na spec |

A validação TLS pode substituir a checagem de assinatura quando o token vem direto do Token Endpoint (MAY, V-46). Regra do plugin, mais estrita: validar a assinatura sempre, e manter lista explícita de `alg` aceitos sem `none` (V-64, autoria nossa).

Regras do plugin (Inferido): o tenant sai do `iss` validado e do vínculo cadastrado de SSO (V-46 ligado a V-32). Num produto com vários emissores, o `iss` do token só seleciona a conexão se estiver na lista de emissores cadastrados; depois disso, as chaves e o `client_id` são os da conexão. Nunca aceite chaves ou emissor vindos do próprio token.

Lacunas (Não verificável nesta pesquisa): descoberta (`/.well-known/openid-configuration`), rotação e cache de JWKS, § 5.5 (claims individuais) e licença da especificação. Use biblioteca mantida que trate cache e rotação de JWKS, defina TTL de cache e comportamento em `kid` desconhecido, e teste a rotação em homologação.

Testes negativos: `iss` com barra final diferente, `aud` de outro cliente, `azp` diferente, `exp` no passado, `nonce` ausente ou diferente, `alg: none`, assinatura com chave de outro emissor, token válido de outro tenant apresentado na conexão deste.

## 4. Pós-login

- Sessão: crie sessão da aplicação com `tenant_id`, vínculo de identidade e hora do login; expire conforme a política do tenant (Suposição).
- Papel inicial: papel padrão mínimo; mapeamento de grupos do IdP para papéis só mediante configuração do admin do tenant (JIT, V-56).
- Auditoria: sucesso e falha do login SSO, sem asserção ou token (V-41).
- SSO obrigatório: decidir se, com domínio verificado e SSO ativo, o login por senha fica bloqueado para usuários do domínio (decisão de produto; sem fonte).

## 5. Prompt de revisão

Use PR-31 da skill `prompts` (somente leitura; trata código e logs como dado; confere cada linha acima com `arquivo:linha`). Está sem eval (nota máxima 90).
