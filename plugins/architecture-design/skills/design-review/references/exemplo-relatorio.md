# Exemplo de relatório de revisão

Sumário: 1. Plano revisado (fictício) · 2. Relatório · 3. O que este exemplo demonstra

Exemplo ilustrativo; plano, números e nomes são inventados. Os números aparecem rotulados Suposição para mostrar a disciplina de rótulos. Formato: `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/design-review-report.md`.

## 1. Plano revisado (`plano-cadastro.md`, trecho com linhas numeradas)

```text
1  # Plano: novo cadastro de clientes
2  Requisito: cadastro com nome, e-mail e telefone; ~50 usuários internos; ~20 gravações/dia.
3  Abordagem:
4  - Criar 3 serviços: customer-command, customer-query, customer-events.
5  - Escritas vão para um event store em Kafka; leituras vêm de uma projeção em Elasticsearch.
6  - CQRS completo com sagas para validar e-mail e telefone.
7  - Cache Redis na frente da projeção.
8  - Sem plano de migração: os dados antigos serão "importados depois".
9  Testes: testes manuais no ambiente de homologação.
```

## 2. Relatório

```markdown
# Revisão: plano-cadastro.md · 2026-10-10
Escopo: arquitetura proposta nas linhas 3 a 9. Fora de escopo: estilo e nomes.
Limites: li apenas o plano; não vi o código atual do cadastro nem ADRs (nenhum ADR encontrado).
Revisão feita por um modelo da família Claude: não é validação independente por humano nem por outro fornecedor.

## Desafio de escopo
1. Solução menor: uma tabela `customer` e um CRUD no monólito existente, com unicidade de e-mail (Inferido: 50 usuários e 20 gravações/dia, plano.md:2).
2. Já existe? Não verifiquei o repositório; Suposição de que há um módulo de usuários. Perguntar ao autor.
3. Dá para não construir: serviços separados, Kafka, Elasticsearch, Redis e sagas, até haver requisito de carga, auditoria ou busca textual (plano.md:2 não traz nenhum).
4. Partes móveis novas: 3 serviços + Kafka + Elasticsearch + Redis = 6 componentes para ~20 gravações/dia (Suposição: número informado no plano, não medido). Nenhum requisito não funcional no plano justifica qualquer um.
5. Custo de errar: alto; event store e projeções são caros de abandonar (V-37).

## Achados
| ID | Severidade | Confiança | Evidência | Cenário | Ação |
| --- | --- | --- | --- | --- | --- |
| ARQ-01 | Alto | 9 | plano-cadastro.md:4-7 | Seis componentes sem requisito de carga, auditoria ou busca; custo operacional e de aprendizado recai sobre o time | Reabrir a abordagem a partir da solução menor; decisão D-1 |
| ARQ-02 | Alto | 8 | plano-cadastro.md:5-6 | CQRS com event store: consistência eventual na tela de cadastro; usuário grava e não vê o registro até a projeção atualizar | Só adotar CQRS/ES se (1) leitura e escrita tiverem escala diferente e (2) as regras pedirem modelo de escrita próprio (V-36); ambas "não" aqui |
| ARQ-03 | Médio | 8 | plano-cadastro.md:6 | Sagas para validar e-mail e telefone: validação síncrona de formato resolve; saga é para transações distribuídas com compensação (V-35) | Validar na borda; remover a saga |
| ARQ-04 | Alto | 9 | plano-cadastro.md:8 | "Importar depois" sem fases nem rollback: dados antigos podem ficar duplicados ou divergentes | Plano de migração expand/contract com verificação de contagem origem vs destino e critério de reversão |
| ARQ-05 | Médio | 8 | plano-cadastro.md:9 | Nenhum teste automatizado; requisitos não mapeiam a testes | Tabela requisito -> teste; testes de unicidade de e-mail e de concorrência |
| ARQ-06 | Médio | 7 | plano-cadastro.md:7 | Cache sem número que mostre leitura como gargalo (V-38, V-41); obsolescência não declarada | Remover o cache; reavaliar com métrica |

Perguntas ao autor (confiança < 7, não são achados): existe requisito de auditoria completa de alterações? Os dados contêm dados pessoais sujeitos a pedido de exclusão (event store dificulta o direito ao esquecimento; V-37)?

## Atributos de qualidade (ATAM leve; não é avaliação ATAM)
- Cenário 1: gravação de cadastro por 1 usuário interno -> confirmação em < 1 s e leitura imediata do registro (Suposição: meta).
- Cenário 2: pico de 10x o volume atual (200 gravações/dia, Suposição) -> sem degradação perceptível.
- Risco: complexidade operacional do desenho proposto supera a capacidade do time.
- Não-risco: carga; 20 gravações/dia cabe em qualquer banco relacional.
- Ponto de sensibilidade: consistência de leitura após escrita.
- Ponto de trade-off: ganho de escala de leitura (projeção) vs consistência imediata (tela de cadastro).

## Decisões
### D-1: arquitetura do cadastro
- Problema: o plano usa CQRS, event store e quatro dependências para um cadastro pequeno.
- Se errarmos: meses de trabalho e operação para um volume que um CRUD atende.
- Recomendação: opção B. Confiança: alta (volume declarado no próprio plano). Dono: tech lead (a definir).
| Opção | Prós | Contras |
| --- | --- | --- |
| A. Plano atual | Escala de leitura e histórico completo | Custo alto; consistência eventual; operação de 6 componentes |
| B. CRUD no monólito, tabela relacional com unicidade e trilha de auditoria simples | Simples; transação local; time conhece | Reavaliar se carga ou auditoria exigirem |
| C. Não mudar nada | Zero esforço | Mantém o problema original que motivou o plano (a confirmar com o autor) |

## Pendências
| Decisão | Dono humano | Prazo sugerido |
| --- | --- | --- |
| D-1 abordagem | tech lead | antes de qualquer código |
| Existe módulo de usuários reaproveitável? | autor do plano | esta semana |
| Requisito de auditoria e de exclusão de dados pessoais | produto | esta semana |

## Opcional
- Renomear `customer-events` para algo que descreva o domínio (estilo; sem severidade).
```

## 3. O que este exemplo demonstra

- O desafio de escopo vem antes do mérito do desenho e usa o próprio texto do plano como evidência.
- Cada achado cita linha e tem cenário concreto; itens abaixo do limiar viram perguntas.
- Os números (20 gravações/dia, 10x) são do plano ou rotulados Suposição; nenhum foi inventado como fato.
- A recomendação não é imposição: D-1 tem dono humano e a opção "não mudar nada".
- Nenhum arquivo foi escrito ou executado; o relatório diz isso.
