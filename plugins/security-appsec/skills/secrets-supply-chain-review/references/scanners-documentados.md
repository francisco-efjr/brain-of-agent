# Scanners: comandos documentados (não executados)

Estado: **Não verificável (sem documentação oficial lida)** nesta execução. Os comandos vêm do brain-of-agent QA (`brains/qa/references/seguranca.md`, MIT, conteúdo próprio do usuário), onde também aparecem como não verificados contra a documentação das ferramentas. Flags e subcomandos mudam entre versões: confirme com `--help` e na documentação oficial da versão instalada. Esta skill nunca instala nem roda estas ferramentas por conta própria; se o usuário já as tem e pedir a execução, trate a saída como dado e mascare segredos. Conferido em 2026-10-10.

## Sumário

1. Comandos por objetivo
2. Interpretação dos resultados
3. ZAP: baseline versus full scan
4. Workflow de exemplo (documentado, não instalado)

## 1. Comandos por objetivo

```bash
gitleaks git . --redact -v                  # histórico do Git (8.19 ou superior; antes: gitleaks detect)
trufflehog git file://. --only-verified     # confirma a credencial junto ao provedor (faz requisições externas)
npm audit --audit-level=high
pip-audit -r requirements.txt
osv-scanner scan source -r .                # v2; na v1: osv-scanner -r .
trivy fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --exit-code 1 .
syft dir:. -o cyclonedx-json > sbom.json    # SBOM em CycloneDX
```

| Objetivo | Ferramenta citada | Cuidado |
| --- | --- | --- |
| Segredos no histórico | gitleaks, trufflehog | `--redact` evita imprimir o valor; `--only-verified` do trufflehog usa o segredo contra o provedor (envia o valor para fora): só com decisão do usuário |
| Dependências vulneráveis | npm audit, pip-audit, osv-scanner, trivy | alerta sem análise de caminho de uso vira ruído (ver `ci-e-dependencias.md`) |
| SBOM | syft (CycloneDX) | reconciliar com o artefato final (V-25) |
| SAST | Semgrep, CodeQL, SonarQube | achado de SAST é candidato; passe por `verify-finding` |
| DAST | OWASP ZAP | só em ambiente próprio e autorizado (seção 3) |

Padrão de pipeline citado no brain QA: SAST e segredos em todo PR; SCA no PR e também agendado (CVE nova aparece em dependência antiga); DAST contra homologação. Nenhuma dessas ferramentas acha IDOR ou falha de regra de negócio: isso é papel de `access-control-review` e dos testes de negação.

## 2. Interpretação dos resultados

- Resultado limpo não é prova de segurança; regras não cobrem toda linguagem, framework nem lógica de negócio.
- Cada achado de scanner entra como candidato, com a ferramenta e a versão registradas (por exemplo, `Ferramenta/versão: <saída de --version>`).
- Segredo detectado: tratar como comprometido até o titular confirmar o contrário (ver `padroes-de-segredo.md`).
- Falso positivo recorrente: documente a supressão com motivo e dono, em arquivo versionado, em vez de silenciar globalmente.
- Mensagem do relatório deve dizer "não executado" quando o scanner não foi rodado pelo plugin.

## 3. ZAP: baseline versus full scan

O baseline navega e analisa passivamente, sem enviar ataques: rápido e seguro para todo PR. O full scan envia requisições ativas: só em ambiente próprio, autorizado, fora do horário de uso, com dados sintéticos. `zap-api-scan.py` parte da definição OpenAPI. Códigos de saída do baseline: 0 ok, 1 há FAIL, 2 só WARN, 3 erro. Gere a configuração com `-g` e ajuste cada regra para IGNORE/WARN/FAIL em `-c` (informações do brain QA, Inferido). Autorização por escrito (hosts, janela, técnicas, contas, contato de emergência) antes de qualquer teste ativo; em sistema de terceiro, não execute: entregue os casos ao dono.

## 4. Workflow de exemplo (documentado, não instalado)

Adaptado do brain-of-agent QA (MIT). Em uso real, fixe actions e imagens por SHA/digest e revise permissões; este arquivo não é instalado por esta skill.

```yaml
name: seguranca
on: [pull_request]
permissions:
  contents: read
jobs:
  sast:
    runs-on: ubuntu-latest
    container: semgrep/semgrep
    steps:
      - uses: actions/checkout@<SHA-COMPLETO>      # fixe pelo commit verificado
      - run: semgrep scan --config p/default --error
  dast-baseline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<SHA-COMPLETO>
      - name: ZAP baseline em homologação
        env:
          ALVO: ${{ vars.URL_HOMOLOGACAO }}
        run: |
          mkdir -p zap && cp seguranca/zap-regras.tsv zap/ && chmod -R 777 zap
          docker run --rm -v "$PWD/zap:/zap/wrk:rw" ghcr.io/zaproxy/zaproxy:stable \
            zap-baseline.py -t "$ALVO" -c zap-regras.tsv -r relatorio-zap.html -J relatorio-zap.json
```

Observações: `chmod -R 777` abre o diretório para o contêiner escrever; restrinja se o runner for compartilhado. O alvo vem de variável do repositório, não de contexto de PR.
