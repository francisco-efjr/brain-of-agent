# Triagem de risco, escalonamento e exclusões

Atribuição: a divisão em ALTO/MÉDIO/BAIXO, a profundidade por tamanho e os gatilhos de escalonamento são inspirados na skill `differential-review` de trailofbits/skills (CC BY-SA 4.0), reescritos aqui com palavras próprias; as exclusões e os níveis de confiança vêm da destilação de anthropics/claude-code-security-review (MIT) e getsentry/skills (Apache-2.0). Itens V-03, V-28, V-30, V-01. Conferido em 2026-10-10.

## Sumário

1. Tabela de risco por arquivo
2. Profundidade por tamanho do diff
3. Escalonamento
4. Histórico de código de segurança removido
5. Exclusões padrão (ajustáveis)
6. O que não excluir em bloco
7. Severidade e ação sugerida

## 1. Tabela de risco por arquivo

| Nível | Quando o arquivo toca | Exemplos de caminho ou sinal |
| --- | --- | --- |
| ALTO | autenticação, sessão, tokens | `auth/`, `login`, `session`, `jwt`, `oauth`, `password` |
| ALTO | criptografia, geração de segredo | `crypto`, `hash`, `encrypt`, `random`, `token` |
| ALTO | chamada externa com dado vindo de fora | `fetch(`, `requests.`, `http.Client`, webhook, importação por URL |
| ALTO | transferência de valor ou estado financeiro | `payment`, `checkout`, `refund`, `balance`, `credit` |
| ALTO | validação ou checagem de acesso removida ou afrouxada | linhas `-` com `if not ...`, decorador, middleware, `validate`, `authorize` |
| ALTO | arquivos críticos de ambiente e CI (V-01) | `.github/workflows/`, `.env*`, configuração de permissões do agente, `Dockerfile`, manifests com scripts de instalação |
| MÉDIO | lógica de negócio, mudança de estado | máquina de estados, cupom, estoque, aprovação |
| MÉDIO | API pública nova ou alterada | novas rotas, esquema GraphQL, campos novos de resposta |
| MÉDIO | dependências novas ou com versão alterada | `package.json`, `requirements*.txt`, lockfiles |
| BAIXO | comentário, teste, interface visual, log sem dado sensível, documentação | `*_test.*`, `docs/`, estilos |

Regra de bolso: se a mudança altera quem pode fazer o quê, ou para onde o dado vai, o arquivo é ALTO. Um teste que passa a ser ignorado (`skip`, assertiva removida) sobe o arquivo de código associado um nível, porque ausência de teste eleva o risco.

## 2. Profundidade por tamanho do diff

| Arquivos no diff | Profundidade |
| --- | --- |
| menos de 20 | leitura profunda de todos os ALTO e MÉDIO; BAIXO só se for ponto de entrada |
| 20 a 200 | um salto: o arquivo alterado e seus chamadores ou chamados diretos |
| mais de 200 | só caminhos críticos (ALTO); declare o corte e o critério na Cobertura |

Se o corte esconder risco, ofereça uma segunda rodada por módulo em vez de fingir cobertura total.

## 3. Escalonamento

Suba a atenção (leitura profunda, refutação independente, git log) quando houver:

1. Remoção de controle de acesso, validação, sanitização ou limite sem substituto visível no mesmo diff.
2. Código removido que veio de commit cuja mensagem cita `security`, `CVE`, `vuln` ou `fix`.
3. Chamada externa nova sem checagem de destino, timeout ou tratamento de erro.
4. Função de risco alto com 50 ou mais chamadores (`Grep` pelo nome): a regressão se espalha.
5. Alteração de configuração padrão do framework: CORS, cookies, CSRF, depuração, TLS, `verify=False`.
6. Tratamento de erro que passa de "nega" para "libera" (falha aberta, A10).

## 4. Histórico de código de segurança removido

Comandos de leitura (pré-aprovados nesta skill; substitua os marcadores):

```bash
git log -S'<trecho removido>' --oneline -- <arquivo>        # quando o trecho entrou e saiu
git log -L<inicio>,<fim>:<arquivo> --oneline                # histórico de um intervalo de linhas
git log --oneline -i --grep='security\|CVE\|fix' -- <arquivo>
```

`git blame` pede permissão fora da lista pré-aprovada: use só se o usuário aprovar. Se o histórico mostra que a checagem foi adicionada para corrigir uma vulnerabilidade, a remoção é achado de severidade Alta com confiança Alta, salvo prova de substituto.

## 5. Exclusões padrão (ajustáveis)

Mostre as exclusões aplicadas no relatório. O usuário ou o guia do projeto pode desmarcar qualquer uma. Marcadas por padrão:

- [x] Negação de serviço e esgotamento de recurso genérico.
- [x] Falta de hardening genérico sem cenário de ataque concreto (cabeçalho ausente sem exploração).
- [x] Condição de corrida apenas teórica, sem estado compartilhado demonstrável.
- [x] Dependência desatualizada sem CVE explorável pelo caminho de uso.
- [x] Arquivos apenas de teste ou documentação.
- [x] Logs que não expõem dado sensível.
- [x] SSRF em que o atacante controla só o caminho, não host nem esquema.
- [x] Variáveis de ambiente e flags de CLI tratadas como confiáveis (quando só o operador as define).
- [x] Ausência de checagem de autorização apenas no cliente (o achado correto é a falta no servidor).
- [ ] Limite de taxa ausente: DESMARCADO em API pública, login, recuperação de senha, OTP, endpoints financeiros ou que chamam serviço pago. Nesses casos relate como A06 ou A07.

## 6. O que não excluir em bloco

Padrão do `cso` (gstack, MIT) para evitar zelo de exclusão: analise controle do atacante e impacto antes de descartar.

- Dependência de desenvolvimento usada em CI com segredos: pode executar código no pipeline.
- Ataque de disponibilidade com custo financeiro (rota que envia SMS, chama API paga, gera relatório pesado).
- Segredo em histórico: continua comprometido (ver skill `secrets-supply-chain-review`).
- Injeção por papel de usuário: usuário autenticado de baixo privilégio é atacante plausível.
- UUID como "autorização": só dificulta adivinhar; IDs vazam em URL, log e e-mail.
- Variável de ambiente que um workflow não confiável consegue definir.
- Padrão "mitigado pelo framework" com escape hatch explícito (`mark_safe`, `dangerouslySetInnerHTML`).

Regra complementar: "inalcançável" que você não consegue demonstrar é **desconhecido**, não inalcançável.

## 7. Severidade e ação sugerida

| Severidade | Critério (impacto realista neste aplicativo) | Ação sugerida (V-27) |
| --- | --- | --- |
| Alta | execução de código, tomada de conta, leitura/escrita em massa, acesso a dado de outro usuário/tenant, injeção com entrada de atacante, segredo real exposto, controle de segurança removido | bloqueia merge |
| Média | exploração exige pré-condição (conta autenticada específica, configuração incomum) ou impacto limitado | corrigir neste ciclo |
| Baixa | dano restrito, defesa em profundidade com cenário plausível | sugestão |

CVSS ou nome de padrão sozinhos não definem severidade. Confiança (Alta, Média) descreve o quanto a evidência sustenta o achado; evidência pode ser: hipótese, estático suportado ou reproduzido. Esta skill só chega a "estático suportado".
