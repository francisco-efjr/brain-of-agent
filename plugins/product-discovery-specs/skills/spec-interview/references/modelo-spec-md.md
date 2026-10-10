# Modelo do SPEC.md (saída de `spec-interview`)

Spec enxuta para feature de nível N3 que será executada em sessão nova. Para spec completa com histórias P1/P2/P3 e `FR-`/`SC-`, use `write-spec`. Para N2, reduza a: Objetivo, Comportamento, Fora de escopo, Critérios com check, Perguntas abertas.

Estrutura inspirada no relato oficial de V-01 (spec que nomeia arquivos e interfaces, declara fora de escopo e termina com verificação ponta a ponta). Redação própria.

## Modelo

```markdown
# SPEC: <nome da feature>

Status: Rascunho | Aprovado em AAAA-MM-DD por <nome>
Origem: <conversa de AAAA-MM-DD, ticket, PRD>

## Objetivo
<2 a 4 linhas: quem, qual problema, qual resultado observável.>

## Resultado esperado (como saberemos)
- <métrica ou fato observável, com origem do número: dado / estimativa / Suposição>

## Fora de escopo
- <item que alguém poderia esperar e que NÃO entra nesta entrega>

## Comportamento
1. <passo do fluxo principal, em linguagem de produto>
2. Falhas e bordas: <situação> -> <o que a pessoa vê / o que o sistema faz>

## Arquivos e interfaces envolvidos (existentes, achados no repositório)
- `<caminho>`: <papel>. Origem: Read/Grep em AAAA-MM-DD.
(Contexto para o executor. Não é decisão de arquitetura.)

## Critérios de aceite
| # | Critério (um comportamento, dado concreto) | Check que prova | Oráculo |
| --- | --- | --- | --- |
| C1 | <...> | <comando, teste ou verificação manual descrita> | <resultado esperado exato> |
| C2 (negativo) | <...> | <...> | <...> |

## Verificação ponta a ponta
<como rodar do começo ao fim e o que deve aparecer; marque o que só pode ser verificado manualmente>

## Perguntas abertas
- [NEEDS CLARIFICATION: <pergunta> | dono: <nome>]

## Premissas
- <Suposição declarada, com o que mudaria se estiver errada>
```

## Trecho resolvido: login com Google (agenda de consultas)

Fatos dados pelo usuário: app de agenda de consultas, Next.js + Postgres, hoje só e-mail e senha. Todo o resto abaixo é palpite ou lacuna, rotulado.

```markdown
# SPEC: Login com Google

Status: Rascunho
Origem: conversa de 2026-10-10

## Objetivo
Permitir que pacientes entrem no app com a conta Google, além de e-mail e senha, para reduzir
abandono no cadastro. [Palpite: o usuário não confirmou o público nem o motivo.]

## Resultado esperado
- [NEEDS CLARIFICATION: qual métrica e qual meta? | dono: produto]

## Fora de escopo
- Outros provedores (Apple, Microsoft). [Palpite, a confirmar]
- Remover o login por senha.

## Comportamento
1. Na tela de entrada, a pessoa escolhe "Entrar com Google" e autoriza no Google.
2. Se já existe conta com o mesmo e-mail e senha: [NEEDS CLARIFICATION: vincular automaticamente,
   pedir a senha antes de vincular ou recusar? | dono: produto/segurança]
3. Se o Google não devolver e-mail verificado: [NEEDS CLARIFICATION: bloquear ou pedir verificação?]
4. Falha: se a pessoa nega a autorização no Google, volta à tela de entrada com a mensagem
   "Não conseguimos entrar com o Google. Tente de novo ou use e-mail e senha."
5. Perda de acesso à conta Google: [NEEDS CLARIFICATION: existe caminho de recuperação por e-mail e senha?]

## Arquivos e interfaces envolvidos
- Não consegui ver o repositório nesta conversa; nenhum arquivo foi citado. [Suposição: Next.js + Postgres,
  informado pelo usuário.]

## Critérios de aceite
| # | Critério | Check | Oráculo |
| --- | --- | --- | --- |
| C1 | Pessoa sem conta entra com Google e passa a ter conta | teste ponta a ponta com conta Google de teste | conta criada e sessão iniciada |
| C2 (negativo) | Autorização negada no Google não cria conta | idem, negando no consentimento | nenhuma conta criada; mensagem do item 4 |
| C3 (negativo) | Conta existente com o mesmo e-mail segue a regra do item 2 | depende da resposta | pendente |

## Perguntas abertas
(ver marcadores acima: 4 abertas com dono)
```

O que este trecho demonstra: números e comportamentos que o usuário não deu aparecem como lacuna ou palpite, nunca como fato; o critério C3 fica pendente em vez de inventado; a spec admite que não viu o código.
