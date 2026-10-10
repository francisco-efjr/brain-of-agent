# Checklist de release de segurança

Modelo para `secrets-supply-chain-review` e para o fechamento de uma release. Rótulos NIST SSDF 1.1 (V-26): PO preparar a organização, PS proteger o software, PW produzir software bem protegido, RV responder a vulnerabilidades. Rótulo é classificação, não afirmação de conformidade. Comandos de scanner são documentados e só rodam se o usuário pedir (Não verificável sem documentação oficial lida; confira flags na versão instalada).

Release: <versão e commit>  ·  Data: <AAAA-MM-DD>  ·  Responsável: <...>

| # | Item | SSDF | Evidência | Estado (OK, falha, n/a com motivo, não avaliado) |
| --- | --- | --- | --- | --- |
| 1 | Lockfile versionado; instalação reprodutível | PW | <arquivo> | <...> |
| 2 | Dependências novas revisadas (nome, origem, manutenção, scripts de instalação) | PW | <PR ou nota> | <...> |
| 3 | Varredura de dependências sem alta ou crítica pendente de tratativa (`npm audit`, `pip-audit`, `osv-scanner`, `trivy fs`) | PW, RV | <saída ou "não executado"> | <...> |
| 4 | Varredura de segredos no histórico e no diff (`gitleaks`, `trufflehog`) | PS | <saída ou "não executado"> | <...> |
| 5 | SBOM CycloneDX gerado nesta release e reconciliado com o artefato final | PS | <arquivo> | <...> |
| 6 | Atestação assinada ligando o SBOM ao digest do artefato | PS | <...> | <...> |
| 7 | SBOM comparado com a release anterior; diferenças revisadas | PS, RV | <...> | <...> |
| 8 | Lacunas do SBOM registradas (componente ausente não prova ausência) | PS | <...> | <...> |
| 9 | Actions e imagens fixadas por SHA ou digest; permissões mínimas por job | PS | <workflow> | <...> |
| 10 | Revisão de segurança do diff da release (`security-review-diff`) com status | PW | <relatório> | <...> |
| 11 | Modelo de ameaça atualizado para mudanças de fronteira | PW | <documento> | <...> |
| 12 | Teste de negação de autorização (usuários e tenants) passando | PW | <teste e saída> | <...> |
| 13 | Headers, CORS e exposição verificados no ambiente alvo | PW | <ambiente e saída> | <...> |
| 14 | `SECURITY.md` e `security.txt` atuais (contato, escopo, prazos) | RV | <arquivo> | <...> |
| 15 | Caminho de resposta a vulnerabilidade: quem recebe, quem corrige, como comunica | RV, PO | <...> | <...> |
| 16 | Segredos de produção fora do ambiente do agente e do repositório; rotação planejada | PS | <...> | <...> |
| 17 | Priorização de pendências por explorabilidade, exposição e impacto | RV | <...> | <...> |

Decisão: <liberar | liberar com ressalvas (liste) | bloquear>. Quem decide: <humano responsável>. A revisão por modelo é uma camada; este checklist não certifica conformidade.
