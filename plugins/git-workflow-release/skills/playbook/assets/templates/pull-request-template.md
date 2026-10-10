# Template: `.github/pull_request_template.md` do seu repositório

Copie o bloco abaixo para `.github/pull_request_template.md` (também vale na raiz ou em `docs/`). Só passa a valer depois de entrar na branch padrão. Vários modelos: pasta `PULL_REQUEST_TEMPLATE/` escolhidos por `?template=`. Os comentários HTML não aparecem no PR renderizado.

```markdown
<!-- Título: tipo(escopo): descrição específica -->
## Resumo (o que e por quê)
<!-- Explique o porquê. Links externos podem sumir; resuma aqui. -->

## Problema

## Abordagem e alternativas descartadas

## Como testar (comandos e saída)
<!-- Cole a saída real. Sem verde, mantenha como rascunho. -->

## Riscos e reversão
<!-- Contrato público alterado? Migração? Como reverter? -->

## Issue relacionada
<!-- Closes #000 -->

## Checklist
- [ ] Um assunto; refatoração sem mudança de comportamento em PR próprio
- [ ] Testes novos ou ajustados rodaram e passaram
- [ ] Documentação ou CHANGELOG atualizados, se a superfície pública mudou
- [ ] Sem segredos no diff
- [ ] Quebra de contrato marcada com `!` ou `BREAKING CHANGE:`
```

Fonte: estrutura de V-30 (documentação do GitHub sobre templates e eng-practices do Google, CC-BY 3.0), redação própria.
