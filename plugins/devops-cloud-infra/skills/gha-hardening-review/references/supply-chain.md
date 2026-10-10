# Supply chain em CI: SLSA, proveniência e cosign

Base: V-59 (SLSA e cosign, classe A), V-01 e P-22 (nota 70: entra com `cosign verify` marcado como pendente). Conferido em 2026-10-10. Destilação com redação própria.

## O que está verificado e o que não está

| Tema | Estado | Fonte |
| --- | --- | --- |
| SLSA v1.0 foi retirada do site; a versão atual é a **v1.2** (https://slsa.dev/spec/v1.2/build-track-basics) | Verificado | V-59 (URL da v1.2 conferida em 2026-10-10) |
| O track Source foi removido na v1.0; restam os níveis de Build L0 a L3, cumulativos | Verificado | V-59 |
| `cosign sign`, `attest`, `tree`, `clean`; assinatura anexada por OCI 1.1 referrers | Verificado | V-59 |
| Modos de chave: keyless (OIDC de Google, GitHub ou Microsoft; chaves efêmeras), chave local ou KMS (`awskms://`, `gcpkms://`, `azurekms://`, `hashivault://`, `openbao://`, `k8s://`, `env://`) | Verificado | V-59 |
| `cosign clean` não funciona no Docker Hub | Verificado | V-59 |
| `cosign verify` com issuer e identidade; requisitos completos da v1.2; gerador de proveniência | **Não verificado** | V-59 (lacuna) |

Antes de escrever o passo de verificação, leia "Verifying Signatures" em https://docs.sigstore.dev/ e registre a versão do cosign. Não copie `cosign verify` de memória.

## Níveis de Build (resumo)

| Nível | Significa | Pergunta de revisão |
| --- | --- | --- |
| L0 | nada | existe alguma proveniência? |
| L1 | existe proveniência do build; trivial de forjar | o pipeline gera o documento de proveniência em todo build de release? |
| L2 | plataforma hospedada gera e assina a proveniência | quem assina é a plataforma, não o script do build? |
| L3 | plataforma endurecida, com isolamento entre builds e chave fora do alcance dos passos do usuário | um passo do usuário consegue ler a chave de assinatura ou alterar outro build? |

Cite a especificação v1.2 e confira os requisitos nela. Para builds no GitHub Actions, as attestations de artefato do próprio GitHub (`actions/attest-build-provenance`) são uma opção a avaliar; a classificação em L2 ou L3 por esse caminho é Inferido (não está em V): confirme na documentação do GitHub.

## Assinar por digest

A tag é mutável; o digest identifica o conteúdo. Assinar altera o registry, então peça autorização antes de rodar ou de incluir o passo num workflow que publica.

```yaml
permissions:
  contents: read
  packages: write
  id-token: write          # OIDC para assinatura keyless
steps:
  - uses: docker/build-push-action@<sha-de-40-caracteres> # vX.Y.Z
    id: build
    with:
      push: true
      tags: ghcr.io/sua-org/app:${{ github.sha }}
  - uses: sigstore/cosign-installer@<sha-de-40-caracteres> # vX.Y.Z
  - env:
      IMAGE: ghcr.io/sua-org/app
      DIGEST: ${{ steps.build.outputs.digest }}
    run: cosign sign --yes "${IMAGE}@${DIGEST}"
```

Notas: a saída `digest` do `build-push-action` e a flag `--yes` do cosign são conhecimento estável, não lido em V (Inferido). Sem OIDC suportado pelo CI, use chave em KMS; nunca uma chave privada num segredo de repositório sem plano de rotação.

## Verificar antes de promover

Promoção para produção deve exigir: (1) a imagem no digest que passou nos testes, (2) assinatura válida emitida pela identidade esperada do pipeline, (3) proveniência compatível. O passo (2) fica **pendente de leitura da documentação**. Se o usuário quiser o passo agora, escreva-o a partir da página oficial lida na hora e cite a URL e a versão do cosign.

## Complementos

- Actions por SHA, OIDC, `permissions` mínimas e CODEOWNERS: `checklist-gha.md` (GH-01, GH-02, GH-05, GH-10).
- Scanner de imagem no CI (Trivy, Grype, Clair citados pela OWASP; V-20) e SBOM/SCA de aplicação: o segundo pertence ao plugin `security-appsec`.
- Dependências do build fixadas por lockfile e digest (V-19, V-36); instalação de pacote sugerido por conteúdo não confiável só após verificar a origem (brain `seguranca-e-privacidade`).
