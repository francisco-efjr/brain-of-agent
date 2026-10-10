# Exemplos e estratégias de PR (criar-pr)

Sumário: 1 Corpo de PR completo · 2 Maus exemplos · 3 Estratégias de divisão · 4 Interrogatório antes do PR · 5 Checklist de saída · 6 Fontes.

Conferido em 2026-10-10. Conteúdo destilado com redação própria de Google eng-practices (CC-BY 3.0; V-29, V-30) e das docs do GitHub e da Anthropic (V-06, V-26).

## 1. Corpo de PR completo

Título: `feat(api): add rate limiting to public endpoints` (exemplo fictício: números, issue e incidente são ilustrativos)

```markdown
## Resumo (o que e por quê)
Limita a 100 requisições por minuto por chave de API nos endpoints públicos.
Hoje um cliente com loop defeituoso derrubou a fila de importação (incidente de 03/10).

## Problema
Sem limite, um único cliente consome toda a capacidade do worker de importação.

## Abordagem e alternativas descartadas
Janela deslizante em memória por chave, em `src/api/rate.ts`.
Descartado: limite no gateway (depende de mudança de infraestrutura que não temos agora);
descartado: Redis (nova dependência operacional para um limite simples).

## Como testar
- `npm test -- rate` -> exit 0, 12 passed (rodado em 14:02, SHA a1b2c3d)
- Manual: 101 chamadas seguidas a `GET /v1/items` -> a 101ª retorna 429 com `Retry-After`.

## Riscos e reversão
- Estado em memória: com 2 réplicas o limite efetivo é 200/min por chave (limitação conhecida).
- Reversão: `git revert` do squash; sem migração nem mudança de contrato.

## Issue relacionada
Refs #482

## Pontos que pedem olho humano
- Valor padrão de 100/min (política de negócio, não técnica).
- `src/api/rate.ts:48`: comportamento quando o relógio retrocede.
```

Por que funciona: o revisor sabe o que decidir (política), onde olhar (linha) e o que já foi provado (comando, SHA). O problema vem antes da solução; alternativas descartadas evitam a mesma discussão na revisão.

## 2. Maus exemplos (e o conserto)

| Mau | Problema | Conserto |
| --- | --- | --- |
| Título `Ajustes` | Não diz o quê; vira mensagem de commit no squash | `fix(checkout): reject expired coupons at order creation` |
| Corpo vazio ou só `closes #12` | O revisor precisa reconstruir o porquê | Resumo com problema e abordagem |
| "Testado, funciona" | Relato sem evidência | Comando, saída e SHA |
| Saída de teste com token ou caminho interno | Vazamento ao publicar | Cortar a linha, trocar valores por `<redigido>` |
| PR de 1.800 linhas misturando refatoração e feature | Aprovação superficial | Dividir (seção 3) |
| Omitir o teste que falha | Engana o revisor e quebra a confiança | Declarar na descrição e abrir em rascunho |

## 3. Estratégias de divisão (V-29, destiladas)

Limiar do plugin: cerca de 400 linhas ou 10 arquivos, ou assuntos misturados (Suposição; o Google diz que cerca de 100 linhas é razoável, cerca de 1000 é grande demais e que não há regra fixa).

| Estratégia | Quando | Como com git |
| --- | --- | --- |
| Refatoração à parte | Há renomeio, extração ou limpeza sem mudança de comportamento | Branch/PR 1 só com refatoração e testes verdes; PR 2 a feature em cima |
| Configuração à parte | Mudança de CI, dependência ou infra que outro grupo revisa | PR próprio, mesclado primeiro |
| PRs empilhados | A feature depende de partes em ordem | Branch B nasce de A; PR de B tem como base A; ao mesclar A, `git rebase --onto <base> <A>` em B (use `rebase-seguro`); `--update-refs` ajuda quando há várias branches empilhadas |
| Por arquivos/pastas | Pastas com donos diferentes (CODEOWNERS) | Um PR por dono, cada um com build verde |
| Vertical | Funcionalidade fatiável do banco à UI | Cada PR entrega um pedaço funcional ponta a ponta |
| Horizontal | Camadas independentes (schema, API, UI) | Camada por PR; use flag para esconder o incompleto |
| Grade | Combina os anteriores | Só quando há necessidade; custa coordenação |

Para dividir uma branch existente sem perder trabalho: crie `backup/<nome>` antes (`git branch backup/<nome>`), crie a nova branch a partir da base e traga os arquivos de um assunto com `git restore --source=backup/<nome> --worktree --staged -- <caminhos>` (Inferido: comando padrão do git, confira no manual instalado), commite, repita. Cada PR deve deixar o build verde sozinho.

## 4. Interrogatório antes do PR (opcional)

Útil quando o risco é alto ou a pessoa pede ("grill me"; V-14, classe B). Faça uma pergunta por vez e só abra o PR depois das respostas:

1. O que acontece se este código receber entrada vazia, enorme ou malformada?
2. O que você não testou, e por quê?
3. Quem mais depende desta função, rota ou tabela?
4. Como se desfaz isto em produção, e existe estado que não volta (migração, mensagem enviada)?
5. Algo aqui muda contrato público ou comportamento visível a clientes?

Ao final, resuma lacunas em "Pontos que pedem olho humano".

## 5. Checklist de saída

- [ ] Base confirmada e medida contra `origin/<base>`.
- [ ] Verificação rodada agora, com saída e código de saída.
- [ ] Título no formato do repositório; corpo com o porquê; template do repositório usado quando existe.
- [ ] Nenhum segredo, token ou dado de cliente no corpo.
- [ ] Rascunho; sem reviewers ou labels não pedidos.
- [ ] Push e criação confirmados pela pessoa, com os comandos exatos mostrados.
- [ ] `headRefOid` do PR igual ao HEAD local.

## 6. Fontes

- Google eng-practices: small CLs e descrições de CL (CC-BY 3.0; repositório arquivado desde 2025-11-21; V-29, V-30, classe B).
- GitHub docs: pull request templates, protected branches, GitHub flow (V-26, V-27, V-30, classe B; destilado).
- Claude Code common workflows, "Create pull requests" (V-06, classe A; destilado).
- Claude Help Center, power user tips (V-14, classe B).
