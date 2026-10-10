# Comandos, escalas e critérios da triagem de dívida

Sumário: 1 Frequência de mudança · 2 Proxies de dor · 3 Escalas F e D · 4 Quadrantes · 5 Modo testes · 6 Exemplo de registro · 7 Atribuições.

Rótulos: Verificado = executado em 2026-10-10 em um repositório de teste (Git, Git Bash e Windows PowerShell 5.1); Inferido = prática derivada ou conhecimento estável. Confira as opções do Git na versão instalada (`git log --help`).

## 1. Frequência de mudança

Arquivos mais alterados na janela (Git Bash). O `sed` remove as linhas em branco que o `--pretty=format:` deixa entre commits:

```bash
git log --since="6 months ago" --name-only --pretty=format: | sed '/^$/d' | sort | uniq -c | sort -rn | head -20
```

PowerShell:

```powershell
git log --since="6 months ago" --name-only --pretty=format: | Where-Object { $_ } | Group-Object | Sort-Object Count -Descending | Select-Object -First 20 Count, Name
```

Saída (repositório de teste com 6 commits): `6 billing.py` e `1 util.py` (Verificado). Use `-- <pasta>` ao final para restringir o escopo.

Sem histórico (clone raso, repositório novo): `git rev-parse --is-shallow-repository` informa clone raso; escreva "frequência não medida" e ordene só por dor.

Exclua do resultado: arquivos gerados, lockfiles, snapshots, diretórios `vendor`, `dist`.

## 2. Proxies de dor

| Proxy | Comando (Git Bash) | Leitura |
| --- | --- | --- |
| Commits de correção por arquivo | `git log --since="6 months ago" -i -E --grep="fix\|bug\|hotfix" --name-only --pretty=format: \| sed '/^$/d' \| sort \| uniq -c \| sort -rn \| head` | Proxy fraco: depende de mensagens de commit boas (Inferido) |
| Autores distintos | `git shortlog -sn --since="6 months ago" HEAD -- <arquivo>` | Muitos autores num arquivo pode indicar acoplamento ou falta de dono. Passe `HEAD`, senão o `shortlog` espera entrada padrão |
| Churn (linhas alteradas) | `git log --since="6 months ago" --numstat --pretty=format: \| awk 'NF==3 {a[$3]+=$1+$2} END {for (f in a) print a[f], f}' \| sort -rn \| head` | Churn alto com poucos commits é reescrita; com muitos commits é instabilidade |
| Marcadores | `Grep` por `TODO\|FIXME\|HACK\|XXX` com contagem por arquivo | Ruído alto; leia os mais antigos (`git blame`) |
| Tamanho | `git ls-files` e leitura dos maiores | Arquivo grande não é dívida por si só |

Verificado: o filtro por mensagem devolveu 2 commits para `billing.py` e 1 para `util.py` no repositório de teste. Em PowerShell o mesmo filtro funciona com `Where-Object { $_ }` no lugar do `sed`.

Dor também vem de fora do Git: incidentes, tickets, relato da equipe ("ninguém quer mexer aqui"). Pergunte ao usuário e registre como Inferido ou "relato do usuário".

## 3. Escalas F e D (1 a 5)

Definidas por este plugin (Suposição, ajuste ao seu repositório). F usa o percentil de commits na janela entre os arquivos do escopo.

| Nota | F (frequência) | D (dor) |
| --- | --- | --- |
| 1 | Quase não muda (abaixo do percentil 50) | Mexer é trivial |
| 2 | Percentil 50 a 70 | Exige ler um pouco de contexto |
| 3 | Percentil 70 a 85 | Exige ler vários arquivos ou rodar passos manuais |
| 4 | Percentil 85 a 95 | Gera bugs de vez em quando; poucos entendem |
| 5 | Acima do percentil 95 | Origem recorrente de bugs ou incidentes; medo de mexer |

Prioridade = F x D (1 a 25). Empate: desempate pelo menor tamanho de passo. F = 1 vai para o fim, qualquer que seja D (Fowler: área feia e estável pode ficar como está).

## 4. Quadrantes (Fowler)

Dois eixos: deliberada ou inadvertida; prudente ou imprudente (martinfowler.com/bliki/TechnicalDebtQuadrant.html; descrição em redação própria).

| Quadrante | Significado | Ação típica |
| --- | --- | --- |
| Deliberada e prudente | Escolheu-se o atalho sabendo o custo, com plano de pagar | Exigir dono e prazo; cobrar o prazo |
| Deliberada e imprudente | Ignorou-se o desenho por pressa, sem plano | Registrar, definir dono e prazo, evitar repetir |
| Inadvertida e prudente | Aprendeu-se depois o que era melhor | Normal; refatorar quando tocar a área |
| Inadvertida e imprudente | Faltava conhecimento básico na época | Treinamento e revisão; corrigir onde dói |

Metáfora com limite: o juro vem do uso do código, não do tempo (Fowler, `TechnicalDebt`, reescrito em 2019). Por isso a frequência pesa mais que a idade.

## 5. Modo testes (V-30)

Os cinco critérios com exemplo e uma busca inicial. As buscas geram candidatos (Inferido); só vale o item que você leu.

| # | Critério | Exemplo | Busca inicial |
| --- | --- | --- | --- |
| 1 | Testa o código-fonte em vez do comportamento | Teste lê `src/auth.js` como texto e confere que contém `bcrypt` | `Grep` por leitura de arquivo de código no teste (`readFileSync(` / `open(` apontando para `src/`) |
| 2 | Duplica outro teste | Dois testes com a mesma entrada e a mesma asserção | Mesmos nomes ou corpos idênticos; compare blocos |
| 3 | Executa sem asserção | Chama a função e termina | Arquivos de teste sem `assert\|expect\|should` (`grep -L` no Git Bash) |
| 4 | Depende de export criado só para o teste | `export const __internal` ou `// exported for testing` | `Grep` por esses marcadores e verifique se algum código de produção usa |
| 5 | O mock confirma a chamada, não o efeito | `expect(pay).toHaveBeenCalled()` sem conferir cobrança persistida | Asserções só de `toHaveBeenCalled`/`assert_called` no teste |

Cartão de evidência por item:

```text
TS-03 | tests/billing.test.js:41 | critério 5 (mock confirma a chamada)
Trecho: expect(gateway.charge).toHaveBeenCalledWith(order.id)
Por que custa mais do que protege: a asserção passa mesmo se a cobrança for duplicada (o teste de mock não observa o efeito)
Custo: quebra a cada mudança de assinatura de charge (3 vezes nos últimos 6 meses, pelo git log)
Proposta: trocar por teste que confere uma cobrança persistida com a mesma chave; só depois remover este
Rótulo: Verificado (li o teste); custo: Inferido
Ação: nenhuma sem aprovação
```

Nunca remova testes na triagem: a remoção é um passo seguinte, com aprovação e com suíte rodando antes e depois (`refactor-seguro`).

## 6. Exemplo de registro (ilustrativo)

| ID | Local | Quadrante | F | D | Prioridade | Ação proposta | Dono/prazo | Evidência | Rótulo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TD-01 | `src/billing/invoice.py` | inadvertida-imprudente | 5 | 4 | 20 | Extrair cálculo de impostos, caracterizar antes (refactor-seguro, ~2 dias) | pendente | 41 commits na janela, 9 com "fix" | Verificado (comandos acima) |
| TD-02 | `src/legacy/export.py` | deliberada-prudente | 1 | 5 | 5 | Nenhuma agora; estável há 14 meses | Maria, revisar até 2027-01 | 0 commits na janela | Verificado |
| TD-03 | `tests/test_checkout.py` | n/a (teste) | 4 | 3 | 12 | Trocar mocks por teste de efeito (modo testes) | pendente | cartão TS-03 | Inferido |

Linhas de baixo: TD-02 (estável e feio) fica no fim da fila de propósito.

## 7. Atribuições

- Fowler, "Technical Debt" (21/05/2019) e "Technical Debt Quadrant" (2009, republicado em 2014): destilados; sem texto literal (copyright do site).
- Auditoria de testes: ideia do `/test-audit` do gstack (Garry Tan, MIT), redação própria; nada instalado.
- Escalas F e D e percentis: autoria deste plugin (MIT).
