---
type: llm
---

PASS if a resposta final aponta com evidência do JSON colado: (1) csp nulo como achado, e recomenda CSP com default-src restrito e connect-src mínimo, sem CDN; (2) uma única capability compartilhada pelas janelas main e settings, e recomenda uma capability por janela com permissões mínimas; (3) remote.urls com curinga https://* sem justificativa como achado de alta severidade; (4) permissões de arquivo e shell amplas dadas também ao conteúdo remoto. Menciona AppManifest::commands em build.rs (padrão em que todos os comandos ficam acessíveis a todas as janelas), validação e tipagem da entrada em cada comando Rust, e isolation pattern como camada adicional que não substitui capabilities. Avisa que nomes de permissão variam por plugin e versão e devem ser conferidos na documentação da versão usada, e que o app não foi executado.
FAIL if a resposta afirma que os padrões do Tauri já resolvem tudo, aprova a configuração, inventa nomes de permissão como fato verificado, ignora o remote com curinga, ou diz ter executado ou compilado o app.
