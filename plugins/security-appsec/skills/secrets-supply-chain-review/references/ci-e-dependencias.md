# CI endurecido, dependências e SBOM

Fontes: OWASP Dependency Graph/SBOM Cheat Sheet (V-25, CC BY-SA 4.0), NIST SSDF (V-26), Action `claude-code-security-review` (V-04, MIT), plugins de terceiros (V-32), Docker (V-38), redação própria. Itens do GitHub Actions (permissões, `pull_request_target`, injeção por contexto) e do ecossistema de pacotes (typosquatting, dependency confusion, incidente `tj-actions/changed-files` de março de 2025) são conhecimento estável e brain-of-agent QA: **Inferido**. Confirme na documentação "Security hardening" da plataforma de CI que o projeto usa. Conferido em 2026-10-10.

## Sumário

1. Workflow de CI: checklist
2. Exemplo de ajuste em GitHub Actions
3. Revisão de dependência nova
4. Alerta/CVE x caminho de uso
5. SBOM e release
6. Containers (Docker)

## 1. Workflow de CI: checklist

- [ ] `permissions:` no topo com o mínimo (`contents: read`); elevação só no job que precisa (ex.: `pull-requests: write` só no passo que comenta).
- [ ] Actions de terceiros e imagens fixadas por SHA completo do commit / digest da imagem, com o número da versão em comentário. Tags e branches (`@main`, `@v4`) podem ser movidas.
- [ ] Nenhum `pull_request_target` ou `workflow_run` que faça checkout do código do PR e o execute (esses gatilhos rodam com segredos e token de escrita do repositório base).
- [ ] Nenhuma interpolação direta de contexto controlado por outros em `run:` (`github.event.issue.title`, `.body`, `pull_request.title`, `head_ref`, nome de branch): passe por variável de ambiente e referencie entre aspas.
- [ ] Segredos disponíveis só aos jobs que os usam; PR de fork sem segredos; ambientes protegidos com aprovação para deploy.
- [ ] Credenciais de nuvem por federação OIDC em vez de chaves de longa duração, quando o provedor suportar.
- [ ] `curl | sh`, `npm install` sem lockfile e instalação de ferramenta por URL móvel evitados; `npm ci`, `pip install --require-hashes` quando viável.
- [ ] Mudanças em `.github/workflows/` exigem revisão de mantenedor (arquivo crítico, V-01).
- [ ] Action de revisão com modelo (V-04): rodar só em PR de fonte confiável ou com aprovação de mantenedor (a Action não é endurecida contra prompt injection); chave de API só em segredo do repositório; Action fixada por SHA e modelo definido explicitamente (o padrão do README é antigo); achado do modelo é sugestão, humano decide o bloqueio; `run-every-commit` (padrão false) ligado aumenta falso positivo.

## 2. Exemplo de ajuste em GitHub Actions

```yaml
# Antes (problemas: permissões amplas, tag móvel, contexto injetado em run)
on: pull_request_target
jobs:
  triagem:
    steps:
      - uses: actions/checkout@v4
        with: { ref: ${{ github.event.pull_request.head.sha }} }   # executa código do PR com segredos
      - run: echo "Título: ${{ github.event.pull_request.title }}"   # injeção por contexto
```

```yaml
# Depois (ilustrativo; troque <SHA-COMPLETO> pelo commit verificado da versão que você adotar)
on: pull_request
permissions:
  contents: read
jobs:
  triagem:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<SHA-COMPLETO>   # v4.x.y
      - env:
          TITULO: ${{ github.event.pull_request.title }}
        run: printf 'Título: %s\n' "$TITULO"
```

Passe valores controlados por terceiros por `env` e use sempre com aspas; nunca monte comandos a partir deles.

## 3. Revisão de dependência nova

1. **Nome**: é o pacote que você acha que é? Compare com o popular (`requests` vs `reqeusts`), confira escopo (`@org/pacote`), o registro e o repositório declarado.
2. **Dependency confusion**: pacote interno cujo nome também existe no registro público; fixe escopo e registro privado.
3. **Idade e manutenção**: data da primeira versão, última atualização, mantenedores, issues de segurança abertas; pacote novo demais ou com troca recente de mantenedor merece cuidado.
4. **Scripts de instalação**: `preinstall`/`install`/`postinstall` (npm), `setup.py`/`build backend` (pip), hooks de build: executam código na instalação. Prefira desativar scripts quando possível (`--ignore-scripts`) e revisar o que fazem.
5. **Lockfile**: versionado, com integridade (hashes); a mudança no lockfile corresponde à mudança no manifest? Dependências transitivas novas são listadas no diff.
6. **Licença** compatível com o uso do projeto (sem parecer jurídico).
7. **Necessidade**: a funcionalidade cabe na biblioteca padrão ou num pacote já presente? Menos dependências, menos superfície.
8. **Origem do pedido**: dependência sugerida por conteúdo não confiável (issue, README, resposta de IA) exige verificar que o pacote existe e é o certo antes de qualquer instalação (alucinação de nome é vetor de ataque).

Peça aprovação do usuário para cada dependência nova (regra S12 do playbook) e rode a varredura de dependências do projeto.

## 4. Alerta/CVE x caminho de uso

Planilha de trabalho (preencha com o que o código mostra; não invente dados do advisory):

| Passo | Pergunta | Evidência |
| --- | --- | --- |
| 1 | Qual pacote e quais versões são afetadas? (texto do advisory fornecido pelo usuário) | citação do advisory |
| 2 | Qual versão está no lockfile? Direta ou transitiva? | arquivo:linha do lockfile |
| 3 | O código importa o módulo/função afetado? | Grep: `arquivo:linha` ou "nenhuma ocorrência" |
| 4 | Entrada de atacante chega até esse uso? | cadeia origem -> uso |
| 5 | Há mitigação por configuração (flag, desabilitar recurso)? | arquivo:linha |
| 6 | Existe versão corrigida compatível? | informação do advisory (do usuário) |

Veredito: **Afetado** (passos 3 e 4 confirmam), **Provavelmente não afetado** (3 ou 4 não confirmam; alcançabilidade em dependência transitiva ou em código dinâmico continua desconhecida), **Não afetado** (módulo ausente do build, com prova). Priorize por explorabilidade, exposição e impacto (V-25). "Dependência desatualizada sem CVE explorável" é exclusão padrão de revisão de diff, mas aqui o foco é o alerta já existente.

## 5. SBOM e release (V-25, V-26)

- Gere o SBOM (CycloneDX) por release, depois de resolver as dependências, e **reconcilie com o artefato final**: dependências empacotadas, pacotes de SO da imagem, binários copiados.
- Declare as lacunas: componente ausente do SBOM não prova ausência.
- Vincule o SBOM ao digest do artefato por **atestação assinada**; assinar o arquivo à parte não o vincula. Assinatura prova autenticidade, não correção.
- Compare o SBOM com o da release anterior (o que entrou, saiu, mudou de versão).
- VEX "não afetado" só com emissor autenticado e justificativa conferida.
- Mapeie componentes para sistemas implantados (onde cada versão roda).
- Rotule os itens do checklist por grupo SSDF (NIST SP 800-218 v1.1): **PO** preparar a organização, **PS** proteger o software, **PW** produzir software bem protegido, **RV** responder a vulnerabilidades. É framework de processo, não checklist técnico; a página não traz datas de 1.1/218A nem versão 1.2.
- Divulgação: `SECURITY.md`/`/.well-known/security.txt` com ao menos `Contact` e `Expires` (RFC 9116) e prazos (V-40), grupo RV.

## 6. Containers (Docker, V-38)

Revise Dockerfile e compose: `USER` não root; sem `docker.sock` montado (somente leitura no socket não torna a API somente leitura); sem `--privileged`; `--cap-drop all` com adição do estritamente necessário; `no-new-privileges`; segredos pelo mecanismo de secrets (não `ENV`/`ARG`/camada de imagem); `--read-only` com `--tmpfs`; limites de recursos; varredura de imagem e lint do Dockerfile no CI; host e engine atualizados. Kubernetes e IaC: lacuna deste plugin.
