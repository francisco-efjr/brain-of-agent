# Plano de teste — <!-- nome da funcionalidade ou da release -->

<!--
COMO USAR ESTE TEMPLATE
- Plano enxuto inspirado na ISO/IEC/IEEE 29119-3 (documentação de teste). O
  objetivo é apoiar decisões, não produzir documento: mire em 2 a 4 páginas.
- Cada seção traz uma instrução (comentário como este) e um mini-exemplo
  marcado "Exemplo". Ao preencher, apague os dois.
- Seção que não muda nenhuma decisão pode ficar como "N/A — motivo".
- Os exemplos usam o mesmo caso: PIX no checkout de um e-commerce.
- Como pensar risco, níveis, critérios e go/no-go: references/estrategia.md.
-->

| Campo | Valor |
| --- | --- |
| Versão do plano | <!-- 0.1, 1.0… --> |
| Autor(a) | |
| Data | |
| Status | <!-- Rascunho / Em revisão / Aprovado --> |
| Revisores e aprovadores | <!-- quem precisa concordar: PO, líder técnico, QA --> |
| Referências | <!-- épico, histórias, protótipo, especificação, contrato de API --> |

## 1. Contexto

<!--
O que muda e por quê; quem usa; o pior efeito realista de uma falha; prazo e o
que é imóvel; como se publica e se desfaz. Declare as suposições ("Supondo
que…"). 5 a 10 linhas.
-->

> Exemplo: o checkout web passa a aceitar PIX via provedor (PSP), com QR Code
> dinâmico válido por 30 min e confirmação por webhook. Público: clientes
> pessoa física, 70% no celular. Pior falha: cliente paga e o pedido não é
> liberado, ou cobrança com valor errado. Lançamento até 14/10, antes da
> campanha de 20/10 (data imóvel). Deploy contínuo com feature flag. Supondo
> que o sandbox do PSP simula pagamento, expiração e devolução.

## 2. Escopo

### Em escopo

<!-- Funcionalidades, plataformas e integrações cobertas. Ligue a IDs do backlog. -->

> Exemplo: geração de cobrança PIX (LOJA-201); tela de QR Code e "copia e
> cola" (LOJA-202); processamento de webhook e liberação do pedido (LOJA-203);
> expiração e liberação de estoque (LOJA-204); reconciliação diária (LOJA-205).
> Navegadores: Chrome e Safari (desktop e celular), Firefox desktop.

### Fora de escopo

<!--
Tudo que alguém poderia supor coberto e não está. Para cada item: motivo e
risco residual. Este é o trecho que mais evita mal-entendido depois.
-->

| Item | Motivo | Risco residual |
| --- | --- | --- |
| _Exemplo:_ PIX no app nativo | fase 2 | nenhum nesta release; app continua sem PIX |
| _Exemplo:_ carga acima de 3× o pico anterior | sem ambiente equivalente | comportamento desconhecido em pico extremo; mitigado por liberação gradual |

## 3. Riscos do produto priorizados

<!--
Escreva cada risco como "falha → efeito". P (probabilidade) e I (impacto) de 1
a 3; nível pela matriz: 6–9 Alto, 3–4 Médio, 1–2 Baixo, e impacto 3 nunca
abaixo de Médio. Mitigação concreta (técnica, nível, monitoramento). Ordene do
maior para o menor e revise quando o escopo mudar.
-->

| ID | Risco (falha → efeito) | Característica | P | I | Nível | Mitigação | Dono |
| --- | --- | --- | --- | --- | --- | --- | --- |
| _Ex._ R1 | webhook perdido ou com erro → cliente pagou e pedido não é liberado | Confiabilidade | 2 | 3 | 6 Alto | teste do handler com falha e reprocesso; consulta periódica ao PSP; alerta "pago e não liberado há 5 min" | time Pagamentos |
| _Ex._ R2 | webhook duplicado → baixa dupla de estoque | Adequação funcional | 3 | 3 | 9 Alto | idempotência pelo ID da transação; mesmo evento 2× no teste de integração | time Pagamentos |
| _Ex._ R3 | QR sem rótulo acessível no "copia e cola" | Capacidade de interação | 2 | 2 | 4 Médio | axe + roteiro com leitor de tela | QA |

## 4. Abordagem

<!--
Por nível e tipo: o que cada nível cobre, com que técnica, se é automatizado
e quem faz. Cada linha aponta os riscos que mitiga. Regra: cada risco no nível
mais barato que o prova; ponta a ponta só para o que depende da integração.
-->

| Nível / tipo | O que cobre | Técnicas | Automação | Riscos | Responsável |
| --- | --- | --- | --- | --- | --- |
| _Ex._ Unitário | cálculo do valor em centavos; estados do pedido | valor-limite; transição de estados (inclui proibidas) | sim, em todo PR | R2 | dev |
| _Ex._ Integração | handler de webhook com banco real | idempotência; eventos fora de ordem; falha no meio | sim, em todo PR | R1, R2 | dev + QA |
| _Ex._ Contrato | API do PSP | contrato + virtualização de 5xx e timeout | sim | R1 | SDET |
| _Ex._ Sistema (E2E) | pagar no prazo; expirar; pagar após cancelar | cenários | 3 fluxos, noturno e pré-release | R1 | QA |

**Exploratório** <!-- cartas previstas: missão, área, duração -->

> Exemplo: "Explorar a tela do QR com recarregar, voltar e duas abas para
> descobrir cobranças duplicadas" — 60 min, celular Android e iPhone.

**Não funcional** <!-- meta mensurável e como medir; sem meta não há resultado -->

> Exemplo: geração de cobrança com p95 ≤ 2 s em 50 requisições/s, PSP
> virtualizado com latência de 800 ms; tela do QR sem violação grave de WCAG 2.2 AA.

**Liberação e produção** <!-- flag, etapas, métricas e limiares de aborto definidos antes -->

> Exemplo: flag para 5% → 25% → 100% em 3 dias; aborta se "pago e não
> liberado" > 0 por mais de 10 min ou erro na geração de cobrança > 1%.

## 5. Ambientes e dados de teste

<!--
Onde roda cada nível; o que é real, sandbox ou simulado; massa de dados
(origem, anonimização conforme a LGPD, como reiniciar); acessos e contas.
-->

| Ambiente | Uso | Dependências | Observações |
| --- | --- | --- | --- |
| _Ex._ CI (contêineres) | unitário, integração, contrato | PSP virtualizado | banco descartável por execução |
| _Ex._ Homologação | E2E, exploratório | sandbox do PSP | sandbox costuma cair; reservar janela |

> Exemplo de dados: clientes e pedidos criados por API em cada teste; CPFs
> gerados por `scripts/documentos_br.py`; nenhum dado copiado de produção.

## 6. Critérios de entrada, saída, suspensão e retomada

<!--
Critérios verificáveis, não "quando estiver estável". Suspensão: quando parar
porque continuar desperdiça esforço; retomada: o que precisa acontecer.
-->

- **Entrada:** _Exemplo:_ build em homologação com smoke verde; sandbox do PSP
  acessível; critérios de aceite com exemplos aprovados pelo PO.
- **Saída:** _Exemplo:_ riscos altos com mitigação executada e evidência;
  nenhum defeito crítico aberto; altos com contorno e aceite; regressão
  crítica verde; metas não funcionais medidas.
- **Suspensão:** _Exemplo:_ smoke falha ou sandbox indisponível por mais de 4 h.
- **Retomada:** _Exemplo:_ nova build com smoke verde; sandbox estável por 1 h.

## 7. Cronograma e marcos

<!-- Marcos de teste ligados aos do projeto. Inclua ciclos de reteste. -->

| Marco | Data | Depende de |
| --- | --- | --- |
| _Ex._ Análise de risco com dev e PO | 30/09 | histórias refinadas |
| _Ex._ Automação de integração e contrato verde | 07/10 | handler implementado |
| _Ex._ Execução E2E e exploratório (2 ciclos) | 08–11/10 | sandbox estável |
| _Ex._ Go/no-go | 13/10 | checklist de release preenchido |

## 8. Papéis e responsabilidades

| Papel | Pessoa | Responsabilidade |
| --- | --- | --- |
| _Ex._ QA | | estratégia, exploratório, E2E, parecer |
| _Ex._ Devs | | unitário, integração, correções |
| _Ex._ PO | | critérios de aceite, aceite de risco residual |
| _Ex._ Líder técnico | | decisão de go/no-go com o PO |

## 9. Entregáveis

<!-- Só o que alguém vai usar. Diga onde fica cada um. -->

> Exemplo: testes automatizados no repositório (tag `@LOJA-20x`); notas das
> sessões exploratórias; relatório de teste; checklist de release com parecer.

## 10. Riscos do projeto e contingência

<!--
Riscos para a atividade de teste (não para o produto): ambiente, pessoas,
prazo, dependências. Cada um com contingência e dono.
-->

| Risco | P | I | Contingência | Dono |
| --- | --- | --- | --- | --- |
| _Ex._ sandbox do PSP indisponível | 3 | 2 | virtualização cobre os cenários de erro; E2E em janela reservada | líder técnico |
| _Ex._ correções chegando no último dia | 2 | 3 | congelamento em 11/10; o que chegar depois vai atrás de flag | PO |

## 11. Aprovação e histórico

| Versão | Data | Mudança | Autor(a) | Aprovado por |
| --- | --- | --- | --- | --- |
| | | | | |
