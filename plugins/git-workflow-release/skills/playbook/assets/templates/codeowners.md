# Template: CODEOWNERS

Fonte: documentação do GitHub sobre code owners (V-28). Locais: `.github/`, raiz ou `docs/`; vale o primeiro encontrado nessa ordem. O **último** padrão que casa vence; coloque os específicos depois dos gerais. `!` (negação) não funciona. Donos precisam de permissão de escrita. Tamanho < 3 MB. O arquivo precisa estar na branch base do PR.

```text
# Geral: mantenedores
*                       @org/mantenedores

# Documentação
/docs/                  @org/docs

# Plataforma e CI (proteja o próprio .github)
/.github/               @org/plataforma
/CODEOWNERS             @org/plataforma

# Monorepo: um dono por pacote
/packages/api/          @org/time-api
/packages/web/          @org/time-web

# Arquivos de alto risco
/package-lock.json      @org/plataforma
```

## Checklist

- [ ] Os donos existem e têm permissão de escrita.
- [ ] Padrão específico depois do geral (se `/packages/api/` vier antes de `*`, perde).
- [ ] `.github/` e o próprio arquivo têm dono.
- [ ] Na proteção de branch, "Require review from Code Owners" está ativado.
- [ ] O arquivo está na branch padrão.
- [ ] Rótulo: o comportamento acima é Verificado em V-28; a recomendação de dar dono a `.github/` veio da leitura dos pesquisadores e não foi reconferida.
