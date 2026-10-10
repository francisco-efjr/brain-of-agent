# Padrões de segredo, mascaramento e resposta a vazamento

Fontes: OWASP Secrets Management Cheat Sheet (CC BY-SA 4.0, V-19), redação própria. Formatos de chave e a lista de arquivos sensíveis são conhecimento estável do domínio e do brain-of-agent QA (MIT, conteúdo próprio): **Inferido**, formatos mudam entre provedores; confirme na documentação do provedor. Conferido em 2026-10-10.

## Sumário

1. Padrões de busca (Grep)
2. Arquivos que não deveriam estar versionados
3. Falsos positivos comuns
4. Como mostrar sem vazar
5. Ordem de resposta a um vazamento
6. Prevenção

## 1. Padrões de busca (Grep -E; candidatos, não achados)

Use `output_mode: files_with_matches` primeiro (não imprime o valor). Abra só o intervalo de linhas necessário para classificar.

| Alvo | Padrão (ERE) | Observação |
| --- | --- | --- |
| Chave de acesso AWS | `AKIA[0-9A-Z]{16}` | o ID sozinho não é o segredo, mas indica o par; procure a chave secreta ao lado |
| Chave privada | `-----BEGIN [A-Z ]*PRIVATE KEY-----` | RSA, EC, OPENSSH, PGP |
| Token GitHub | `gh[pousr]_[A-Za-z0-9]{36,}` | formatos mudam; confira a documentação do provedor |
| Token Slack | `xox[baprs]-[A-Za-z0-9-]{10,}` | |
| Chave Stripe de produção | `sk_live_[0-9a-zA-Z]{16,}` | `sk_test_` é de teste, mesmo assim não deve ficar em código |
| JWT | `eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]+` | pode conter dados pessoais no payload; token vivo é credencial |
| Atribuição suspeita | `(secret\|token\|passw(or)?d\|api[_-]?key\|private[_-]?key)["']?\s*[:=]\s*["'][^"'$<{]{8,}` | exclui valores com `$`, `<`, `{` (templates) |
| URL com credencial | `[a-z]+://[^/\s:@]+:[^/\s:@]+@` | `postgres://usuario:senha@host` |
| Conexão de banco | `(mongodb(\+srv)?\|postgres(ql)?\|mysql\|redis\|amqp)://[^\s"']+` | verifique se há senha na URL |

Sempre procure também por segredos de provedores que o projeto usa (ver `package.json`, `requirements.txt`, `docker-compose.yml`, workflows) e pelos prefixos documentados por eles.

## 2. Arquivos que não deveriam estar versionados

`.env`, `.env.*` (exceto `.env.example` sem valores), `*.pem`, `*.key`, `*.p12`, `*.pfx`, `id_rsa`, `id_ed25519`, `credentials`, `.npmrc`/`.pypirc` com token, `terraform.tfstate*`, `*.kdbx`, `kubeconfig`, dumps de banco (`*.sql`, `*.dump`), `service-account*.json`, `google-services.json` com chaves privadas (nem todo `google-services.json` é segredo: confira). Use Glob para listá-los e confira se o `.gitignore` os cobre.

## 3. Falsos positivos comuns

- Placeholders: `<SEU_TOKEN>`, `changeme`, `xxx`, `your-api-key`, `EXAMPLE`; valores documentados como exemplo pelo provedor.
- Hash de commit, UUID, checksum, ID de build, chave pública (`BEGIN PUBLIC KEY`), `integrity` de lockfile.
- Fixtures de teste com valores claramente inválidos e isolados: aceitável, desde que não tenham o prefixo de produção.
- Chave pública de provedor de pagamento/mapa (por desenho, vai ao navegador): confirme na documentação do provedor antes de descartar, e verifique restrições de domínio.
- Regra: na dúvida, classifique como "dúvida" e peça ao dono do segredo que confirme no provedor. Nunca teste o valor.

## 4. Como mostrar sem vazar

- Formato de relato: `Chave AWS (AKIA...), 20 caracteres, config/deploy.sh:14`; `Token tipo gh (ghp_...), 40 caracteres, .github/workflows/release.yml:33`.
- Ao colar trechos, substitua o valor por `<REDIGIDO>`. Em comandos, nunca coloque o segredo como argumento (vai para histórico do shell e para o transcript).
- Se o valor aparecer sem querer numa saída de ferramenta, pare, avise o usuário e não o repita (regra S03 do playbook).
- Saída de Grep com `-o` ou conteúdo (`output_mode: content`) imprime o valor: evite em candidatos reais.

## 5. Ordem de resposta a um vazamento (V-19)

1. **Revogar** na origem (provedor, painel, API do cofre). Antes de qualquer limpeza, porque o segredo pode estar copiado em clones, forks, caches de CI e logs.
2. **Rotacionar**: emitir novo, injetar por variável de ambiente ou cofre, atualizar quem o usa. Prefira credenciais dinâmicas de vida curta.
3. **Apagar** do código atual e das configurações (`git rm`, novo commit).
4. **Registrar** o incidente: o que vazou, por quanto tempo, onde (repo público? privado?), quem tinha acesso.
5. **Auditar** o uso: logs de acesso do provedor entre o commit e a revogação.
6. **Histórico**: reescrever o histórico do Git (git filter-repo, BFG) quebra links de commit e obriga colaboradores a refazer clones; só limpa o que está no repositório, não nos clones. Pese e peça decisão do usuário; a revogação já neutralizou o risco principal.

Se o segredo for de terceiro (cliente, parceiro), notifique o titular conforme o contrato; vazamento de dado pessoal é incidente e deve ir ao encarregado da organização (sem parecer jurídico aqui).

## 6. Prevenção (para propor, não para instalar)

- `.gitignore` para os arquivos da seção 2; `.env.example` só com chaves e valores falsos.
- Varredura pré-commit e em CI (gitleaks, detect-secrets, trufflehog: ver `scanners-documentados.md`).
- Segredos dinâmicos e de vida curta; mínimo privilégio; variável de ambiente só como último recurso; nada de `ENV`/`ARG` do Docker para segredo (V-19, V-38).
- Regras em `permissions.deny` do Claude Code para `.env` e `secrets/` (skill `harden-claude-code`).
- Regra de projeto no CLAUDE.md (playbook `claude-md-snippets.md`, S02 e S03).
