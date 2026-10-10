# Gatekeeper e entrevista de ADR

Sumário: 1. Gatekeeper em detalhe · 2. Sinais de decisão implícita · 3. Roteiro de entrevista por tópico · 4. Como tratar respostas fracas · 5. Sem decisor disponível · 6. Gotchas

Validado em 2026-10-10 (modelos Claude 4.x/5.x). Fontes: V-12 (Azure Well-Architected, critério de inclusão), V-14 e V-15 (entrevista, gatekeeper, `[NEEDS CLARIFICATION]`), V-16 (gatilhos, consentimento), V-13 (Nygard e Fowler). Redação própria.

## 1. Gatekeeper em detalhe

Pergunta única de inclusão (V-12): "Isto afeta a estrutura, um atributo de qualidade ou custa caro reverter?". Se sim, siga para o estágio 2.

| Estágio | Pergunta | Se a resposta for não |
| --- | --- | --- |
| 1 | A decisão trata de como o sistema é construído (estrutura, tecnologia de base, fronteiras, contratos, dados)? | Rejeitar e rotear: requisito vai para a spec; processo de equipe vai para o guia de contribuição |
| 2 | É estruturalmente significativa, cara de reverter ou transversal (muitos módulos ou times dependem dela)? | Rejeitar: convenção vai para o `CLAUDE.md`; pequena e reversível não precisa de registro |

Teste de reversibilidade rápido: "se estiver errada, quanto custa voltar atrás: um commit, uma semana, uma migração de dados, uma renegociação contratual?". Só o primeiro é reversível barato.

Teste de transversalidade: "se esta decisão mudar, quantos módulos, times ou contratos externos precisam mudar junto?". Dois ou mais sugerem ADR.

Exemplos de aceitação: escolha de banco de dados principal; módulo que vira serviço; protocolo entre serviços; estratégia de multitenancy; política de consistência (eventual vs forte) em um fluxo; formato público de erro de API; provedor de identidade.

Exemplos de rejeição, com destino:

| Pedido | Veredito | Destino |
| --- | --- | --- |
| "Renomear `tmp` para `orderDraft`" | rejeitado, estágio 1 | nenhum registro |
| "Todas as datas em UTC no JSON" | rejeitado, estágio 2 (convenção) | `CLAUDE.md` |
| "O cliente só pode cancelar até 24 h antes" | rejeitado, estágio 1 (regra de negócio) | spec do produto |
| "Usar Redis para cache de sessão" | depende: se for decisão única, reversível e local, nenhum registro; se virar dependência obrigatória de disponibilidade de login, ADR | perguntar ao usuário a consequência de queda do Redis |

## 2. Sinais de decisão implícita

A skill pode sugerir ADR (sem gravar) quando a conversa contém uma escolha com razões: framework, banco, protocolo, esquema de autenticação, "vamos migrar para...", "decidimos que...", "em vez de X vamos Y porque...". Gatilhos explícitos: "registre essa decisão", "escreva um ADR", "documente por que escolhemos". Sugira uma vez; se o usuário recusar, não insista (V-16: consentimento).

## 3. Roteiro de entrevista por tópico (uma pergunta por vez)

Pule o tópico quando o repositório ou a conversa já responderam. Ordem sugerida:

1. **Problema:** "Que problema ou pressão força esta decisão agora? O que acontece se não decidirmos?" (alimenta Contexto e a alternativa "não mudar nada").
2. **Forças e restrições:** "Quais restrições são fixas (prazo, time, orçamento, compliance, stack existente)? Quais metas de qualidade importam mais (latência, disponibilidade, custo, simplicidade operacional)?"
3. **Opções:** "Quais alternativas sérias foram consideradas, além de não mudar nada? Por que cada uma foi descartada ou ficou em segundo lugar?"
4. **Decisão:** "O que foi decidido, em uma frase começando por 'Vamos...'?"
5. **Consequências negativas:** "Qual o pior custo que aceitamos com esta escolha (operacional, dados, aprendizado, lock-in)?"
6. **Decisor e reavaliação:** "Quem decidiu (ou decidirá)? Que fato mensurável nos faria reabrir a decisão?"

Quando o usuário trouxe tudo no pedido, faça zero perguntas e vá ao rascunho. Quando faltar só o decisor, pergunte só isso.

## 4. Como tratar respostas fracas

| Resposta do usuário | O que fazer |
| --- | --- |
| "Não sei, faça o que achar melhor" | Dar uma recomendação com rótulo Inferido e pedir confirmação explícita; manter "Decidido por: pendente" até alguém assumir |
| "Só tem uma opção" | Perguntar o que acontece com "não mudar nada"; se realmente não há alternativa, registrar a restrição que elimina as demais |
| Consequência negativa "nenhuma" | Perguntar custo operacional, curva de aprendizado e saída (lock-in); se nada surgir, registrar "não identificada até AAAA-MM-DD" como Suposição |
| Número sem fonte ("200 req/s") | Manter, com rótulo Suposição e quem estimou |
| Decisão já implementada | ADR retroativo: Contexto "inferido do código", decisor pendente, data real da decisão se conhecida |

## 5. Sem decisor disponível (execução em lote)

O roteiro da seção 3 vira uma tabela de pendências em vez de perguntas; o rascunho sai completo naquilo que o repositório e o pedido respondem.

| Tópico do roteiro | O que fazer sem interação |
| --- | --- |
| Problema, forças, opções | Preencher do pedido e do repositório; o que faltar vira `[NEEDS CLARIFICATION: pergunta]` no Contexto |
| Decisão | "Decisão proposta (aguarda <decisor ou papel>): vamos ..." com a recomendação rotulada Inferido ou Suposição |
| Consequências negativas | Registrar as identificadas; se nenhuma, "não identificada até AAAA-MM-DD" como Suposição |
| Decisor e reavaliação | "Decidido por: pendente"; gatilho proposto como Suposição |

Ao final, uma seção "Pendências" com pergunta, recomendação, dono (pessoa ou papel, "a definir" se desconhecido) e o que a resposta destrava. Uma decisão adiada (D-3 de um plano, por exemplo) não vira ADR: o gatekeeper a rejeita com destino "pendência do plano".

## 6. Gotchas

- O adlc (V-15) é um projeto de uma estrela, "early alpha": o método é usado porque coincide com a fonte A (V-12), não pela popularidade.
- O agente de ADR do awesome-copilot (V-14) grava sem pedir confirmação; este plugin exige aprovação (conflito C3).
- Códigos POS-001/NEG-001 do V-14 são cosmética para parsing por máquina; omita salvo pedido.
- Entrevista longa cansa: mais de 6 perguntas é sinal de que a decisão ainda não está madura; devolva "decisão prematura, faltam X e Y" em vez de insistir.
