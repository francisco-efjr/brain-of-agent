# ADR e governança de decisões

Validado em 2026-10-10 · Modelo-alvo: Claude 4.x/5.x · Rótulos: Verificado, Inferido, Suposição, Não verificável.
Fontes: V-12 (Azure Well-Architected, ADR), V-13 (Nygard, Fowler), V-14 (awesome-copilot, MIT), V-15 (adlc, MIT), V-16 (ECC, MIT), N-05 (MADR 4.0.0), brain-of-agent `adr.md` (MIT, Francisco Edson). Redação própria; template literal só do brain-of-agent.

## Sumário

1. Princípio: o ADR registra o que humanos decidiram
2. Critério de inclusão e gatekeeper de dois estágios
3. Tabela de roteamento de rejeições
4. Gatilhos: quando oferecer um ADR
5. Entrevista por tópico
6. Template consolidado (e variante MADR)
7. Checklist de qualidade do ADR
8. Status, numeração e supersessão
9. Política de consentimento e gravação
10. Índice
11. ADR retroativo em legado
12. Revisão de ADR por diff
13. Consulta: "por que escolhemos X?"
14. Governança no repositório
15. Exemplo curto
16. Gotchas

## 1. Princípio

O ADR registra uma decisão que um humano nomeado tomou. O agente estrutura, pergunta, compara e cobra consequências negativas; não inventa decisores nem decisão. Ponto não resolvido vira `[NEEDS CLARIFICATION]` no texto e entra na lista de pendências (V-15). Isso evita registro plausível e falso.

## 2. Critério de inclusão e gatekeeper de dois estágios (V-12, V-15)

Pergunta única de inclusão (V-12): a decisão afeta estrutura, um atributo de qualidade, ou é cara de reverter?

- Estágio 1: a decisão trata de como o sistema é construído (estrutura, tecnologia, integração, dados, implantação)? Se não, rejeite e roteie.
- Estágio 2: é estruturalmente significativa, cara de reverter ou transversal (afeta vários módulos ou times)? Se não, rejeite e roteie.

## 3. Roteamento de rejeições

| Rejeitado porque | Encaminhar para |
| --- | --- |
| É requisito ou comportamento esperado do produto | Spec do produto (`/product-discovery-specs:playbook`) |
| É convenção de código ou de equipe | CLAUDE.md ou guia de estilo (ver `claude-md-snippets.md`) |
| É pequena e reversível (renomear variável, trocar formatter) | Lugar nenhum: decida e siga |
| É tarefa ou bug | Backlog |
| É política de segurança ou compliance | Documento de política; ADR só se mudar a estrutura |

Exemplo: "Usar PostgreSQL em vez de DynamoDB para pedidos" passa nos dois estágios; "renomear `tmp` para `orderDraft`" é rejeitado e não vai a lugar nenhum.

## 4. Gatilhos (V-16)

Explícitos: "registre esta decisão", "isso merece ADR?", "write an ADR", "why did we choose X".
Implícitos, para oferecer (não para gravar sem pedir): escolha de framework, banco, broker, estilo de API ou modelo de autenticação com razões discutidas; decisão de dividir ou unir serviços; adoção de padrão com custo (CQRS, event sourcing, saga); mudança de fronteira de módulo. Ofereça uma vez por decisão; se o usuário recusar, não insista.

## 5. Entrevista por tópico (V-14, V-15)

Antes de perguntar, leia o repositório e os ADRs existentes (reunir contexto reduz perguntas). Entradas mínimas: título, contexto, decisão, alternativas, decisores. Se faltar algo, pergunte um tópico por vez, nesta ordem: forças e restrições; opções (mínimo duas, mais "não mudar nada"); critério de decisão; decisor humano; gatilhos de reavaliação. Quando o usuário não souber um ponto, grave `[NEEDS CLARIFICATION: ...]` e siga.

## 6. Template consolidado

Arquivo `adr-NNNN-slug.md` (4 dígitos, sem reuso de número; é o padrão do plugin: a convenção do projeto ou do pedido, como `ADR-001-slug.md`, vence). Versão completa em `assets/templates/adr.md`.

```markdown
# ADR-NNNN: [título nominal]

Status: [proposto | aceito | substituído por NNNN | descontinuado]
Data: [AAAA-MM-DD] · Decidido por: [nome(s)] · Confiança: [alta | média | baixa]

## Contexto
[forças em tensão, restrições, requisitos, evidências; neutro]

## Decisão
Vamos [verbo no futuro: ação].

## Alternativas
| Opção | Prós | Contras | Motivo da rejeição |
| --- | --- | --- | --- |
| Não mudar nada | | | |

## Consequências
Positivas: ... · Negativas: ... · Neutras: ...
Reversibilidade: [limites; não prometer rollback de dados]

## Gatilhos de reavaliação
[evidência concreta que reabre a decisão]

## Links
[requisitos, issues, ADRs relacionados]
```

**Variante MADR 4.0.0** (N-05, MIT ou CC0 à escolha; versão de 2024-09-17): seções Context and Problem Statement, Decision Drivers, Considered Options, Decision Outcome (com Consequences e Confirmation), Pros and Cons of the Options, More Information. Use quando o time já adotou MADR; mapeamento para o template consolidado: Decision Drivers = forças do Contexto; Confirmation = Gatilhos e Validação. Template em `assets/templates/adr-madr.md` (redação própria).

## 7. Checklist de qualidade do ADR (rode antes de mostrar)

- [ ] Número sequencial, nome na convenção do projeto ou do pedido (padrão `adr-NNNN-slug.md`, 4 dígitos), data ISO.
- [ ] Título nominal (substantivo), uma decisão por ADR, cerca de uma página.
- [ ] Contexto neutro, sem defender a decisão.
- [ ] Decisão em voz ativa ("Vamos...").
- [ ] Pelo menos 2 alternativas com motivo de rejeição, incluindo "não mudar nada" quando aplicável.
- [ ] Pelo menos 1 consequência positiva e 1 negativa.
- [ ] Nível de confiança e, se baixa, data de revisão.
- [ ] Gatilho de reavaliação concreto (ex.: "se o p95 passar de 400 ms por 7 dias").
- [ ] Decisor humano nomeado; nenhum decisor inventado.
- [ ] Afirmações sobre código com `arquivo:linha`.

## 8. Status, numeração e supersessão (V-12, V-13)

Status: `proposto`, `aceito`, `substituído por NNNN`, `descontinuado`. O ADR aceito não se edita (log append-only). Para mudar, crie um novo ADR que o substitui, com link, e no antigo atualize apenas a linha de Status, mostrando o diff antes. Numeração não reaproveita números. Decisão em fases (curto, médio, longo prazo) pode ter um ADR por fase, com links.

## 9. Política de consentimento e gravação (conflito C3)

1. Rascunhe no chat. 2. Peça aprovação explícita. 3. Só então grave, com status `proposto` (ou `aceito` somente se o usuário disser). 4. Se o usuário recusar, descarte. 5. Pergunte antes de criar o diretório (`docs/adr/` por padrão). 6. Escrita só dentro do diretório de ADR. A skill `adr` rascunha e consulta (somente leitura); a skill manual `adr-write` grava.

## 10. Índice (`docs/adr/README.md`, template `adr-index.md`)

Tabela: número, título, status, data, confiança, substitui, substituído por. Atualize a cada ADR novo e a cada supersessão. Uma linha por ADR, ordenada por número.

## 11. ADR retroativo em legado (V-12)

O log pode ser gerado depois, em projeto existente. Passos: (1) liste as decisões estruturais visíveis no código (banco, broker, fronteiras, autenticação, deploy); (2) para cada uma, leia código e histórico (`git log` do arquivo de configuração) para reconstruir o contexto; (3) marque o que é inferência: "Contexto reconstruído a partir do código; motivo original: Não verificável"; (4) peça ao responsável confirmar ou corrigir; (5) status `aceito (retroativo)` só após confirmação humana; (6) data do ADR = data da decisão se conhecida, senão data do registro com a nota. Nunca invente o motivo histórico.

## 12. Revisão de ADR por diff (V-15)

Proposta de mudança em ADR existente: mostre o diff, liste o impacto a jusante (ADRs, módulos, regras do CLAUDE.md que dependem dele) e pergunte. Mudança de substância = ADR novo com supersessão; correção de digitação ou link = diff aprovado.

## 13. Consulta "por que escolhemos X?" (V-16)

Leia `docs/adr/`; cite número, status e a seção de Contexto e Alternativas. Se o ADR estiver `substituído`, siga o link e responda com o vigente, citando o histórico. Sem ADRs: diga "nenhum ADR encontrado; quer começar?" e ofereça ADR retroativo. Não invente razões a partir do código; marque como Inferido.

## 14. Governança no repositório (V-12)

- ADRs no repositório do código, em pasta aberta junto da documentação.
- Numeração sequencial e status visível.
- Decisão de baixa confiança: data de revisão.
- Índice atualizado a cada supersessão.
- ADRs aceitos viram restrições vigentes (snippet S-03 em `claude-md-snippets.md`).
- Registros curtos, afirmativos e factuais; material de apoio por link.

## 15. Exemplo curto

```markdown
# ADR-0003: PostgreSQL como banco do serviço de pedidos

Status: proposto
Data: 2026-10-10 · Decidido por: [responsável técnico, a confirmar] · Confiança: média

## Contexto
Time de 4 pessoas; consultas relacionais com junções por pedido, cliente e item; pico estimado de 200 req/s (Suposição, a confirmar com tráfego real).

## Decisão
Vamos usar PostgreSQL gerenciado como banco único do serviço de pedidos.

## Alternativas
| Opção | Prós | Contras | Motivo da rejeição |
| --- | --- | --- | --- |
| Não mudar nada (planilha + API legada) | Sem custo de migração | Sem transação; consulta manual | Não atende integridade dos pedidos |
| DynamoDB | Escala horizontal simples | Consultas relacionais exigem modelagem por acesso; time sem experiência | Custo de modelagem maior que o benefício na carga estimada |

## Consequências
Positivas: transações e junções nativas. Negativas: escala de escrita vertical limitada; backup e upgrade são nossa responsabilidade. Neutras: ORM a definir.
Reversibilidade: migrar para outro banco exige reescrita da camada de dados.

## Gatilhos de reavaliação
Escrita sustentada acima de [limiar a combinar] ou latência p95 acima de 400 ms por 7 dias.
```

## 16. Gotchas

- Hook, regra de permissão ou texto não impedem sozinhos que o agente edite um ADR aceito; o plugin exige diff mostrado e aprovação. `tools` de agente não restringe diretório (V-04).
- O gerador ADR original (V-14) grava sem pedir confirmação e usa códigos POS/NEG/ALT opcionais; aqui a confirmação é obrigatória e os códigos podem ser omitidos.
- O adlc (V-15) é alpha com 1 estrela: o conteúdo é aprovado pelo critério cruzado com V-12, não pela popularidade.
- Limiares numéricos de confiança (V-18) são Suposição; ADR usa alta, média, baixa.
- Um ADR por decisão: "ADR de tudo" não é consultável.
