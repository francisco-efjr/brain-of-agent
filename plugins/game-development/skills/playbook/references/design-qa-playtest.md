# Design, QA e playtest

Base: V-26, V-27, V-28, V-09, V-06, V-21 (2026-10-10). Fontes de terceiros (Donchitos, MIT; Level Design Book; Meta; IXDF) estão **destiladas**, sem texto copiado. Cobre a **revisão** de GDD; criação de GDD, balanceamento e economia não têm fonte validada (esqueleto de GDD é Suposição).

## Sumário

- [Rubrica de revisão de GDD](#rubrica-de-revisão-de-gdd)
- [GDD em XML para o modelo](#gdd-em-xml-para-o-modelo)
- [Tipos de teste de jogo](#tipos-de-teste-de-jogo)
- [Plano de QA: estrutura](#plano-de-qa-estrutura)
- [Playtest: plano](#playtest-plano)
- [Playtest: relatório](#playtest-relatório)
- [Bug report de jogo](#bug-report-de-jogo)
- [Lacunas de design](#lacunas-de-design)

## Rubrica de revisão de GDD

Quatro dimensões (V-27, skill `design-review` do Donchitos, classe B). Somente leitura; registrar em arquivo só com confirmação.

| Dimensão | Pergunta | Exemplo de achado |
| --- | --- | --- |
| Completude | as seções obrigatórias existem e têm conteúdo? Seção vazia é **lacuna, não aprovação** | "Economia: (vazio)" -> lacuna |
| Consistência | fórmulas batem com o comportamento descrito? casos de borda batem com as regras? dependências declaradas nos dois sentidos? | "Dash consome stamina" x "Stamina não afeta movimento" -> contradição |
| Implementabilidade | regras precisas, valores e critérios de aceite testáveis? | "Crítico: 10%" sem definir se é por golpe ou por alvo; sem critério de aceite |
| Encaixe | conflito com outras mecânicas e com os pilares? grafo de dependências entre sistemas | "Crafting depende do Sistema de Forja (a definir)" -> dependência sem documento |

Vereditos por dimensão e agregado: `APPROVED | NEEDS REVISION | MAJOR REVISION NEEDED | NOT ASSESSED`. NOT ASSESSED prevalece sobre APPROVED na agregação. Reaproveite veredito anterior só se documento e registro forem idênticos. Cada achado cita seção ou linha do GDD; nenhum número de balanceamento inventado; liste o que não foi lido; termine com **perguntas abertas**.

Exemplo de saída resumida:

```text
GDD: combate v3 (lido: seções 1-5; não lido: apêndice A)
Completude: NEEDS REVISION  - Economia vazia; Crafting sem fórmulas
Consistência: MAJOR REVISION NEEDED - Dash x Stamina (§3.2 e §4.1 se contradizem)
Implementabilidade: NEEDS REVISION - crítico 10% sem unidade; sem critérios de aceite
Encaixe: NOT ASSESSED - Sistema de Forja não existe
Agregado: MAJOR REVISION NEEDED
Perguntas abertas: 1) stamina limita o dash? 2) crítico é por golpe?
```

## GDD em XML para o modelo

Técnica oficial (V-09, prompting best practices): documentos longos no topo, tags consistentes, pedir para **citar trechos antes** de concluir, formato de saída explícito, "questão aberta" em vez de inventar. Aviso da mesma fonte: linguagem agressiva ("CRITICAL: You MUST") deve ser suavizada nos modelos recentes.

```xml
<documentos>
  <documento index="1"><fonte>GDD v3 cap. combate</fonte><conteudo>...</conteudo></documento>
</documentos>
<instrucoes>Primeiro cite em <citacoes> os trechos do GDD relevantes ao sistema pedido. Depois gere tarefas por sistema.</instrucoes>
<formato_saida>Lista com id, sistema, critério de aceite verificável, dependências. Se um dado faltar, escreva "questão aberta" em vez de inventar.</formato_saida>
```

## Tipos de teste de jogo

Fonte: skill `qa-plan` do Donchitos (V-26, classe B).

| Tipo | Cobre | Evidência exigida |
| --- | --- | --- |
| Logic | fórmulas, limiares, transições de estado, economia | teste automático **obrigatório** |
| Integration | save/load, rede, persistência | teste automático ou smoke |
| Visual/Feel | animação, impacto, sensação | captura mais humano |
| UI | menus, HUD, foco | captura mais checklist |
| Config/Data | arquivos de dados, bindings | validação de dados |

Regras: o tipo **declarado** na história (`Type:`) é autoritativo; tipo inferido vira lacuna a confirmar; empate Logic/Integration vira Integration; sem histórias no escopo a resposta é NÃO AVALIADO (não gere plano vazio). Testes de lógica não provam jogabilidade.

## Plano de QA: estrutura

Resumo por tipo; testes automáticos exigidos (cada um com comando ou nome de teste); checklist manual (cada item com dono humano); escopo de smoke; requisitos de playtest; definição de pronto; nível (minimal, standard, full). Estratégia geral de QA (critérios de entrada e saída, análise de risco) vem do brain `qa` e de `/qa-testing:playbook`; aqui só o específico de jogo. Convenção de status: OK / PENDENTE / FALHOU / N/A; "testado" sem evidência é PENDENTE.

Exemplo para quatro histórias (resumo): (1) fórmula de dano com crítico = Logic, GUT/NUnit com valores-limite (ataque igual à defesa, crítico em 0 e 100%); (2) save/load = Integration, teste que salva, recarrega e compara; (3) animação de pulo e coyote time = Visual/Feel, captura de sequência mais humano; (4) menu de remapeamento = UI mais Config/Data, captura, checklist e validação do arquivo de bindings.

## Playtest: plano

Fontes: playtest-report do Donchitos (V-28), Level Design Book, kit de planejamento da Meta, IXDF. Campos: objetivo e hipótese; público; build/commit; método (presencial ou remoto, moderado ou não); papéis (moderador e anotador); roteiro e briefing (com avisos de conteúdo); dados a coletar (**poucos** eventos bem escolhidos: tempo, mortes, taxa de vitória); consentimento; sessão exploratória com missão, oráculos, cobertura efetiva e "não exercitado" (adaptado do charter do brain `qa`). Observe mais do que pergunte; compare o que o jogador **disse** com o que **fez**; defina escopo e perguntas-foco antes.

Tamanho de amostra: o FAQ do IXDF cita "5 a 8 jogadores por sessão" e várias sessões ao longo do desenvolvimento; Meta e Level Design Book não trazem cifra. **Referência comercial, nunca regra** (K9).

## Playtest: relatório

Sessão (build, foco, hipótese); primeiras impressões; **tabela de bugs** (crash, queda de quadro, softlock, passos para reproduzir); **pain points** só de sensação, sem misturar com defeito; dados quantitativos; roteamento de cada item (design, balanceamento, bug, polish) com próximo passo; comparação com os pilares; "não avaliado" quando faltar dado. Playtest automatizado e telemetria avançada não têm fonte validada.

## Bug report de jogo

Campos (adaptação do `bug-report` do brain `qa`, MIT, e V-28): título "onde + comportamento incorreto + condição"; build/commit e engine; pré-condições; passos mínimos; esperado (e fonte da regra); obtido; frequência (por exemplo 3 em 20); evidência (captura, log, clipe); tipo (crash, queda de quadro, softlock, visual, áudio); impacto; hipótese de causa rotulada Inferido. Template: `assets/templates/bug-report-jogo.md`.

## Lacunas de design

Criação de GDD, balanceamento, economia (faucets e sinks, curvas), IA de jogo (FSM x behavior tree: pista Game AI Pro Vol. 1 cap. 6 e 10, gratuito mas sem redistribuição, não lido), UI de jogo, shaders. Quando pedirem "ajude a escrever o GDD", use entrevista (uma pergunta por vez até haver requisitos testáveis; histórias P1/P2/P3 com Given/When/Then; requisitos `FR-NNN`; critérios `SC-NNN`; seção Assumptions; marcador `[NEEDS CLARIFICATION]`), padrão geral dos PAD-03/PAD-04 do prompt-principles; a aplicação a jogos é **Suposição**.
