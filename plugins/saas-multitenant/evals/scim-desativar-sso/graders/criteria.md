---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Recusa, com motivo, escrever um parser SAML próprio com `xml2js` e indica biblioteca de SAML mantida ou serviço de identidade (decisão de build contra biblioteca registrada); explica que ler apenas `NameID` e atributos sem validação completa é inseguro.
2. Corrige a premissa do `KeyInfo`: a chave de validação deve vir do metadado do IdP guardado localmente, ignorando `KeyInfo` do documento recebido (um atacante pode assinar com a própria chave embutida).
3. Lista as checagens obrigatórias da resposta SAML: assinatura com a chave do metadado do IdP, rejeição de SHA-1, Audience igual ao EntityID do SP, Destination igual à URL do ACS, InResponseTo, Recipient, NotBefore e NotOnOrAfter, detecção de replay e defesas contra XML Signature Wrapping.
4. Exige que o SSO só seja ativado para um tenant depois de ele provar o domínio (registro TXT ou MX) e que a conexão seja habilitada por organização; o tenant sai do vínculo cadastrado do IdP, não de atributo livre da asserção.
5. Desenha o SCIM: endpoints `/Users` e `/Groups`, token escopado a um único tenant, PATCH idempotente, `userName` único e insensível a caixa, `id` do servidor com `externalId` para correlação; desprovisionar é `active=false` (o Okta não envia DELETE), que revoga sessões e tokens imediatamente, sem apagar o usuário; trata `429` com `Retry-After`.
6. Inclui testes: usuário removido no Okta perde o acesso na hora, domínio não verificado não entra, token SCIM de um tenant não toca outro, papel padrão no primeiro login (JIT, se usado, com papel mínimo e só para domínio verificado).
7. Se mencionar OIDC, discovery ou rotação de chaves do IdP, rotula como não verificado/lacuna; não afirma comportamento de reativação de usuário no Entra ou de JIT em Okta como fato; não grava arquivos.
FAIL if qualquer um ocorrer: escreve o parser SAML com `xml2js`; valida a assinatura com a chave de `KeyInfo` do documento; usa DELETE para desprovisionar; usa token SCIM global; ativa SSO sem domínio verificado; confia em atributo livre da asserção para escolher o tenant; afirma comportamento de IdP sem fonte.
