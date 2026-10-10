# Matriz de aplicabilidade do modo SEGURANCA-COMPLETO

Preencha uma linha por área antes de implementar ou concluir. Estados: **Aplicável** (itens aplicados, evidência), **Não aplicável** (motivo), **Não verificável** (sem acesso ou sem fonte). Sem acesso a ambiente não vira "OK". O modo não amplia permissões. Relatório final começa com completo, parcial ou não avaliado.

Escopo: <módulo ou projeto>  ·  Data: <AAAA-MM-DD>  ·  Autor: <modelo>  ·  Revisão independente: <sim | não>

| # | Área | Estado | Itens aplicados (referência) | Evidência (`arquivo:linha`, comando e saída) | Limitação |
| --- | --- | --- | --- | --- | --- |
| 1 | Autenticação | <...> | `checklist-completo` seção 2, 5 | <...> | JWT, MFA: Inferido |
| 2 | Sessão | <...> | seção 3 | <...> | <...> |
| 3 | Autorização por objeto e tenant | <...> | `autorizacao-e-tenant` | <...> | tenant: Inferido |
| 4 | Entrada e injeção (SQL, comando, template, XSS) | <...> | seções 6, 7; `regras-appsec` INJ, FE | <...> | <...> |
| 5 | SSRF e chamadas externas | <...> | seção 8 | <...> | <...> |
| 6 | Upload e parsing | <...> | seção 9 | <...> | <...> |
| 7 | Segredos | <...> | `segredos-e-supply-chain` | <...> | <...> |
| 8 | Criptografia | <...> | seção 10 | <...> | TLS em trânsito: lacuna |
| 9 | Configuração e headers | <...> | seção 11 | <...> | depende do ambiente |
| 10 | Containers e IaC | <...> | seção 15 | <...> | só Docker coberto |
| 11 | Logging e alertas | <...> | seção 12 | <...> | <...> |
| 12 | API (Top 10 2023) | <...> | seção 13; `owasp-e-asvs` | <...> | <...> |
| 13 | Supply chain, SBOM e CI | <...> | `segredos-e-supply-chain`; `checklist-release-seguranca` | <...> | scanners não lidos |
| 14 | LLM e agentes | <...> | `conteudo-nao-confiavel`; `triagem-de-agente-mcp` | <...> | <...> |
| 15 | Configuração do Claude Code | <...> | `ferramentas-e-mcp`; `harden-claude-code` | <...> | versão a conferir |
| 16 | Privacidade / LGPD | <...> | seção 16 | <...> | lacuna: sem parecer jurídico |
| 17 | Resposta a vulnerabilidades | <...> | `security-md`; `achado-restrito` | <...> | SLA interno: lacuna |

Critério de "completo": cobertura da matriz com limitações honestas, não caixas verdes. Se houver leitura obrigatória não feita ou execução material impossível, o status é parcial.
