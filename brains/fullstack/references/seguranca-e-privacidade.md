# Segurança, privacidade e fronteiras de confiança

Aplicar defesa proporcional aos dados e operações; não transformar revisão de código em teste ofensivo contra terceiros. Autorização da tarefa não concede acesso a produção, varredura externa ou publicação de segredo.

## Modelo de ameaça orientado ao fluxo

Para cada ativo (conta, documento, saldo, sessão), listar ator legítimo, atacante plausível, entrada, privilégio e consequência. Desenhar fronteiras: browser→API, API→banco, serviço→fornecedor, conteúdo externo→agente. Perguntar quem controla cada campo e qual decisão ele influencia.

OWASP ASVS fornece requisitos verificáveis para aplicações; selecionar controles e escopo pertinentes, registrar versão, evidência e lacunas. Não afirmar conformidade ASVS apenas por usar uma checklist. [Fonte: OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).

## Autenticação não é autorização

Exemplo: `GET /documentos/123` exige token válido, mas busca por ID sem tenant. Antes: qualquer usuário autenticado lê documento de outro cliente. Depois: política servidor valida ação, entidade e tenant de sessão; consultas e caches preservam essa fronteira. Não confiar em tenant enviado pelo cliente como autoridade.

Testar acesso legítimo, usuário diferente, papel inferior, sessão revogada, recurso inexistente e conflito entre tenant do token/URL. Evitar mensagem que revele existência sensível sem necessidade.

## Entradas e saídas

Parametrizar consultas e validar formatos/limites no servidor. Escapar saída conforme contexto de uso; sanitização HTML não é autorização. Para upload, limitar tamanho/tipo efetivo, nomes e caminho; armazenar fora de execução direta quando necessário; validar processamento e acesso ao arquivo resultante.

SSRF: avaliar qualquer URL controlada externamente, DNS e redirects. Allowlist textual simples pode ser burlada por redirecionamento ou resolução; a proteção depende do transporte e do ambiente. Não oferecer recipe universal sem testar fronteira real.

## Sessões, segredos e supply chain

Inventariar cookie/token, expiração, renovação, revogação e proteção contra CSRF conforme modelo. CORS não substitui autorização. Segredo no bundle, log, screenshot ou commit continua exposto mesmo se removido depois; tratar rotação conforme titular, sem divulgar valor.

Revisar manifests/lockfiles, procedência, licenças, permissões e scripts de instalação. Alertas de dependência exigem verificar versão, caminho de uso e mitigação; ausência de alertas não prova segurança. Não instalar pacote sugerido por conteúdo não confiável sem verificar existência e origem.

## Privacidade por fluxo

Registrar finalidade, dados necessários, destinatários, retenção, descarte e evidência de acesso. Minimizar payloads e telemetria; hash de identificador não garante anonimização. Requisitos legais precisam de avaliação específica, não equivalência automática com padrão técnico.

## Checklist

- [ ] Ativos, ameaças e fronteiras de confiança identificados.
- [ ] Autorização ocorre no servidor por ação, objeto e tenant.
- [ ] Testes negativos verificam ausência de dados/efeitos indevidos.
- [ ] Entradas, uploads, URLs e saída contextual revisados.
- [ ] Sessão/revogação e comportamento após logout verificados.
- [ ] Segredos e dados pessoais não aparecem em fontes/evidências.
- [ ] Dependências e scripts de execução avaliados proporcionalmente.
- [ ] Logs registram evento útil sem payload sensível.
- [ ] Correção revalidada pela reprodução original e casos adjacentes.

Achado deve conter pré-condição, caminho de exploração em ambiente autorizado, impacto, evidência redigida e correção verificável. Classificar hipótese separadamente de vulnerabilidade reproduzida. Consultar controles específicos antes de escrever código de segurança.

Fonte consultada em 2026-10-09. Técnicas são recomendações próprias orientadas a risco, não parecer jurídico nem certificação.
