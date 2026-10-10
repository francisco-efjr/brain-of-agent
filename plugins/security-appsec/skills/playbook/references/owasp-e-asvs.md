# OWASP Top 10:2025, API Top 10 2023, LLM Top 10 2025 e ASVS

Mapa de taxonomias para o campo `categoria` do relatório e para derivar critérios de aceite. Nomes das categorias: Verificado em 2026-10-10 (V-13, V-14, V-15). A coluna "o que procurar em código" é redação própria a partir de V-18 a V-24, V-36 a V-39 e do brain QA (Inferido onde indicado); as páginas OWASP consultadas listam só os nomes das categorias nesta validação. Não cite números de requisito ASVS.

## Sumário

1. OWASP Top 10:2025
2. OWASP API Security Top 10 2023
3. OWASP Top 10 for LLM Applications 2025
4. ASVS 5.0.0 por nome de capítulo
5. Como usar no relatório

## 1. OWASP Top 10:2025 (https://top10.owasp.org/2025)

Direitos 2021 a 2025; a data exata de publicação não aparece na página (o brain cita novembro de 2025: Inferido). O brain afirma que SSRF foi absorvido por A01 (Inferido, não reconferido): trate SSRF como A01 ou como API7/A10 conforme o contexto, citando a versão.

| ID | Categoria | O que procurar em código (grep e leitura) |
| --- | --- | --- |
| A01 | Broken Access Control | Rota sem checagem por objeto; ID da URL usado direto na consulta; tenant vindo do cliente; função administrativa acessível por troca de método; mass assignment de `papel`, `tenant_id`, `status`; URL buscada pelo servidor sem lista (SSRF, se agrupado aqui) |
| A02 | Security Misconfiguration | Debug ligado, erro verboso, conta padrão, CORS permissivo com credenciais, headers ausentes, listagem de diretório, arquivos expostos, permissões de nuvem amplas |
| A03 | Software Supply Chain Failures | Lockfile ausente, dependência com nome suspeito (typosquatting), scripts de instalação, Actions por tag em vez de SHA, imagem sem digest, CDN sem SRI, SBOM ausente |
| A04 | Cryptographic Failures | Hash rápido para senha, ECB, IV fixo, chave embutida, PRNG comum para token, HTTP sem TLS, dado sensível em URL, cache ou `localStorage` |
| A05 | Injection | SQL por concatenação (inclusive em ORM), comando de SO com entrada, template com entrada, XSS em sinks de risco, NoSQL com objeto controlável, LDAP/XPath |
| A06 | Insecure Design | Fluxo sem limite (valor, quantidade, frequência), regra de negócio no cliente, sem caso de abuso, sem modelo de ameaça para fluxo sensível, corrida em recurso escasso |
| A07 | Authentication Failures | Enumeração de contas, sem limite de tentativas, reset fraco, sessão que não muda no login, logout só no cliente, senha com hash fraco, MFA contornável |
| A08 | Software or Data Integrity Failures | Cliente decide preço, papel ou status; desserialização de dado não confiável; atualização ou artefato sem verificação de assinatura ou digest; pipeline que executa código de PR |
| A09 | Security Logging and Alerting Failures | Login falho, acesso negado e mudança de permissão sem log; log com segredo ou dado pessoal; sem alerta (testar se o alerta dispara); quebra de linha forjando entrada de log |
| A10 | Mishandling of Exceptional Conditions | Exceção que libera (falha aberta), 500 com stack, operação parcial sem reversão (cobrou sem criar pedido), `except: pass` em checagem de segurança, JSON truncado ou número enorme sem 4xx |

## 2. OWASP API Security Top 10 2023 (https://api-security.owasp.org/editions/2023/en/0x11-t10)

A página lista só as edições 2019 e 2023: pode haver edição mais nova; confira.

| ID | Categoria | Caso de teste | Esperado |
| --- | --- | --- | --- |
| API1 | Broken Object Level Authorization | Usuário B usa o ID de um objeto de A em GET, PUT, PATCH, DELETE e sub-recursos | 403 ou 404, nada de A no corpo, objeto intacto |
| API2 | Broken Authentication | Rota sem token; token expirado, adulterado ou de outro ambiente; login, OTP e reset sem limite | 401; limitação após N tentativas |
| API3 | Broken Object Property Level Authorization | Leitura traz campo que o papel não deveria ver; escrita de campo protegido | Campo ausente; escrita ignorada ou 400/422 |
| API4 | Unrestricted Resource Consumption | `?limit=100000`, corpo enorme, upload acima do limite, GraphQL profundo, exportação pesada repetida | 400, 413 ou 429; custo limitado |
| API5 | Broken Function Level Authorization | Usuário comum chama rota administrativa; troca de método | 403 |
| API6 | Unrestricted Access to Sensitive Business Flows | Compra, cadastro ou reserva automatizados em massa | Limite por conta ou dispositivo |
| API7 | Server Side Request Forgery | Campo de URL (webhook, importar, avatar) apontando para endereço interno, metadados de nuvem ou esquema não HTTP | Recusado por lista de destinos |
| API8 | Security Misconfiguration | CORS, erros verbosos, métodos desnecessários, TLS | Ver `checklist-completo.md` seção 11 |
| API9 | Improper Inventory Management | Versão antiga (`/v1`) ativa sem os controles da atual; rota fora da documentação; endpoint de depuração | Desativada ou com os mesmos controles |
| API10 | Unsafe Consumption of APIs | Terceiro devolve resposta enorme, malformada ou com redirecionamento | Validada como entrada não confiável; timeout; sem redirecionamento cego |

Casos de teste: brain QA (Inferido); nomes: V-15 (Verificado). API10 é relevante para webhooks e MCP.

## 3. OWASP Top 10 for LLM Applications 2025 (https://genai.owasp.org/llm-top-10/)

Nomes Verificados (V-14). A página liga a edição 2023-24 e não aponta edição 2026 nem um "Agentic Top 10" ranqueado. As perguntas são redação própria; as de LLM04, LLM08 e LLM09 são Inferido (V-14 só reabriu os títulos).

| ID | Categoria | Pergunta de revisão |
| --- | --- | --- |
| LLM01 | Prompt Injection | Que conteúdo externo chega ao prompt (páginas, e-mails, documentos, saída de ferramenta)? |
| LLM02 | Sensitive Information Disclosure | Que dado sensível o modelo vê e quem lê a saída? |
| LLM03 | Supply Chain | De onde vêm modelos, plugins, MCP e dados? Versão fixada? |
| LLM04 | Data and Model Poisoning (Inferido) | Quem pode escrever nos dados de treino, ajuste fino ou base de conhecimento? |
| LLM05 | Improper Output Handling | A saída do modelo vai para SQL, shell ou HTML sem validação por schema? |
| LLM06 | Excessive Agency | Quais ferramentas o agente aciona sem aprovação, com que permissão? Aplica-se a tríade (`conteudo-nao-confiavel.md`) |
| LLM07 | System Prompt Leakage | O prompt de sistema contém segredo ou regra que não deveria estar lá? |
| LLM08 | Vector and Embedding Weaknesses (Inferido) | A busca vetorial respeita autorização e tenant do usuário que consulta? |
| LLM09 | Misinformation (Inferido) | O produto apresenta saída do modelo como fato verificado em decisão de risco? |
| LLM10 | Unbounded Consumption | Qual o teto de tokens, de chamadas e de custo por usuário? |

Três regras de IA do molde awesome-copilot (V-27, redação própria): separar instrução de sistema do conteúdo do usuário; tratar a saída do LLM como entrada não confiável; validar a saída contra schema e rejeitar o que não conferir.

## 4. ASVS 5.0.0 por nome de capítulo

Verificado (V-16): ASVS 5.0.0 estável de maio de 2025 (tag v5.0.0), CC BY-SA 4.0, https://owasp.org/www-project-application-security-verification-standard/ e https://github.com/OWASP/ASVS ; a página do projeto ainda rotula 5.0.0 como "Bleeding Edge" (inconsistência da própria página). Só o capítulo 1 (Encoding and Sanitization, seção 1.2 Injection Prevention) foi conferido.

Inferido (brain QA, não reconferido): cerca de 350 requisitos em 17 capítulos e três níveis (L1 mínimo para qualquer aplicação; L2 aplicações com dado sensível; L3 críticas). Capítulos: Encoding and Sanitization; Validation and Business Logic; Web Frontend Security; API and Web Service; File Handling; Authentication; Session Management; Authorization; Self-contained Tokens; OAuth and OIDC; Cryptography; Secure Communication; Configuration; Data Protection; Secure Coding and Architecture; Security Logging and Error Handling; WebRTC.

Mapa de uso (por nome de capítulo, sem número de requisito):

| Área do plugin | Capítulo ASVS equivalente |
| --- | --- |
| Injeção, XSS | Encoding and Sanitization; Web Frontend Security |
| Validação, lógica de negócio | Validation and Business Logic |
| API | API and Web Service |
| Upload | File Handling |
| Senhas, MFA, reset | Authentication |
| Sessão, CSRF | Session Management |
| IDOR, tenant | Authorization |
| JWT | Self-contained Tokens |
| OAuth/OIDC | OAuth and OIDC |
| Cripto | Cryptography |
| TLS | Secure Communication |
| Headers, debug, segredos | Configuration; Data Protection |
| Falha fechada, logs | Secure Coding and Architecture; Security Logging and Error Handling |

Regras de uso: escolha o nível pelo risco e classifique cada requisito como teste automatizado, revisão ou "não se aplica" com motivo. ASVS é critério de aceite, não selo: não afirme "conforme ASVS" só por usar a lista. Sempre cite a versão (por exemplo "ASVS 5.0.0, capítulo Authorization"). Para citar um requisito específico, abra o arquivo oficial no repositório OWASP/ASVS (lacuna 3).

## 5. Como usar no relatório

- Campo `categoria`: use o formato `A05 Injection` (Top 10:2025); em API acrescente `API1`; em LLM, `LLM05`. Uma categoria principal por achado.
- Um achado de IDOR em API REST é A01 (Top 10:2025) e API1 (API Top 10 2023); escreva ambos.
- A taxonomia classifica, não mede risco: severidade e confiança vêm da análise (`revisao-de-diff.md`).
- Se o usuário usa outro padrão (CWE, PCI, ISO 27001), registre a equivalência como Suposição; não há fonte validada aqui para mapear.
