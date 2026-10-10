# Checklist completo e matriz de aplicabilidade

Usado no modo UXUI-COMPLETO e em qualquer auditoria ampla. Cada área traz o que verificar, a evidência aceita e a lacuna conhecida. Detalhes técnicos ficam nas outras referências (links por área). Itens `V-nn` estão em `fontes.md`; "brain" é o brain-of-agent (MIT, do autor do plugin).

## Sumário

- [Como usar](#como-usar)
- [Registro de leitura](#registro-de-leitura)
- [Matriz de aplicabilidade](#matriz-de-aplicabilidade)
- [Checklist por área](#checklist-por-área)
- [Critérios de aceite da entrega](#critérios-de-aceite-da-entrega)
- [Fechamento](#fechamento)

## Como usar

1. Preencha a matriz de aplicabilidade com **aplicável**, **não aplicável (motivo)** ou **lacuna conhecida**. Áreas não aplicáveis não geram itens.
2. Para cada área aplicável, percorra os itens e registre o status: Verificado (com evidência), Inferido, Suposição, Não verificável, Não aplicável.
3. Implemente só o que o usuário autorizou. O que sair do pedido vira follow-up com ID.
4. Revalide depois dos ajustes (captura, teclado, contraste, axe quando houver) e reporte antes e depois.

## Registro de leitura

No modo completo, registre cada referência lida antes de agir:

| Arquivo | Status (lido, parcial, ausente) | Observação |
| --- | --- | --- |
| checklist-completo.md | | |
| padroes-e-antipadroes.md | | |
| wcag-aa.md | | |
| apple-e-plataformas.md | | |
| design-tokens.md | | |
| avaliacao-visual-por-llm.md | | |
| pesquisa-e-heuristicas.md | | |
| ux-writing.md | | |
| decisoes-e-tradeoffs.md | | |
| claude-md-snippets.md | | |
| ferramentas-e-mcp.md | | |
| fontes.md | | |

Arquivo não aberto não pode ser marcado como lido. Se um arquivo não puder ser lido (permissão, contexto), registre "ausente" ou "parcial" e diga qual área fica sem cobertura.

## Matriz de aplicabilidade

| # | Área | Aplicável quando | Referência | Lacuna conhecida |
| --- | --- | --- | --- | --- |
| 1 | Pesquisa com usuários | Há decisão de produto ou UX que usuários podem informar | `pesquisa-e-heuristicas.md` | Survey, personas, JTBD (`/product-discovery-specs:playbook`) |
| 2 | Arquitetura de informação | Há navegação, taxonomia ou rótulos de seção | `pesquisa-e-heuristicas.md` | Tamanhos de amostra de card sorting e tree testing |
| 3 | Fluxos | Há tarefa em mais de uma tela | `assets/templates/fluxo-de-tela.md` | Fonte A/B sobre user flows: conteúdo é Inferido |
| 4 | Visual (hierarquia, tipografia, cor, espaçamento) | Há tela a desenhar ou revisar | `padroes-e-antipadroes.md`, `avaliacao-visual-por-llm.md` | Tipografia e grid sem fonte primária |
| 5 | Estados | Há componente interativo ou dado remoto | abaixo | n/a |
| 6 | Design system e tokens | Há tokens, tema ou biblioteca de componentes | `design-tokens.md` | Figma Dev Mode e MCP oficial sem doc lida |
| 7 | Acessibilidade | Sempre que há interface | `wcag-aa.md` | Leitor de tela exige teste manual |
| 8 | UX writing | Há texto de interface | `ux-writing.md` | Voz em PT-BR sem fonte |
| 9 | Movimento | Há animação ou transição | `wcag-aa.md`, `padroes-e-antipadroes.md` | Duração e easing sem diretriz oficial lida |
| 10 | Handoff design para código | Há implementação a seguir | `assets/templates/spec-componente-handoff.md` | n/a |
| 11 | Plataforma | O alvo é iOS, iPadOS, macOS ou Android | `apple-e-plataformas.md` | Material 3 |
| 12 | Performance percebida | Há fluxo de clique ou tecla; carga | `wcag-aa.md` | Dados de campo exigem instrumentação |
| 13 | Avaliação | Entrega de cliente, redesenho, tela de alto tráfego | `avaliacao-visual-por-llm.md` | Opinião de modelo, não validação externa |

Modelo de linha: `7 · Acessibilidade · aplicável · formulário de cadastro com diálogo de termos · lacuna: leitor de tela não testado`.

## Checklist por área

### 1. Pesquisa com usuários
- [ ] A pergunta de pesquisa tem uma decisão associada (sem decisão é sinal de alerta).
- [ ] O método responde à pergunta (entrevista, teste, card sorting, tree testing).
- [ ] O perfil de participantes e o recrutamento excluem amigos e colegas; há sobra para ausências.
- [ ] Perguntas são neutras e sobre experiência concreta; nenhuma "você usaria…?".
- [ ] O plano diz o que o estudo não responde; nada de significância estatística com n pequeno.
- Evidência: plano preenchido (`plano-de-pesquisa-e-guia.md`).

### 2. Arquitetura de informação
- [ ] Método coerente: card sorting para agrupar, tree testing para validar estrutura existente ou proposta.
- [ ] Rótulos usam a linguagem do usuário; teste de tronco passa (6 de 6) nas páginas-chave.
- Evidência: tabela de tarefas de tree testing, resultado do teste de tronco.

### 3. Fluxos
- [ ] Objetivo e ponto de entrada declarados; passos tela a tela com decisão, ação e resposta do sistema.
- [ ] Ramos de erro, vazio, cancelamento e volta desenhados.
- [ ] Pontos de abandono prováveis marcados "a validar".
- Evidência: `fluxo-de-tela.md` preenchido.

### 4. Visual
- [ ] Brief de uma linha e superfície (Persuade, Operate, Read, Experience).
- [ ] Marca, tokens e `DESIGN.md` existentes respeitados; o plano diz o que foi reutilizado.
- [ ] Ponto de entrada claro, uma zona primária, níveis adjacentes com diferença de peso perceptível.
- [ ] Revisão contra o genérico feita: escolhas default trocadas ou justificadas.
- [ ] Elemento decorativo removido antes da entrega.
- Evidência: plano (`plano-de-design.md`), captura desktop e mobile, relatório `relatorio-auditoria-ui.md`.

### 5. Estados
- [ ] Para cada componente: normal, foco, hover (quando houver), pressionado, desabilitado, carregando, erro, sucesso.
- [ ] Para cada lista ou dado remoto: vazio, carregando, resultados, erro, volume e paginação.
- [ ] Conteúdo extremo: nome de 47 caracteres, zero resultados, texto que expande na tradução, 320 px.
- [ ] Falha e recuperação preservam o que o usuário digitou e evitam ação duplicada.
- Evidência: matriz de estados com captura ou descrição; dados plausíveis, sem lorem ipsum.

### 6. Design system e tokens
- [ ] Três camadas; componente sem valor cru nem primitivo; fonte única de tokens.
- [ ] Sem referência desconhecida ou circular; arquivos gerados não editados à mão.
- [ ] Renomeação com lista de nomes antigos e novos e confirmação; impacto de release (major, minor, patch).
- [ ] Contraste dos pares semânticos calculado nos dois temas.
- Evidência: relatório de drift, tabela de contraste, esqueleto DTCG com versão fixada.

### 7. Acessibilidade
- [ ] Checklist AA por tela preenchido (`checklist-a11y-por-tela.md`) com status honesto.
- [ ] Teclado, foco, diálogo (9 itens), formulário, movimento reduzido verificados ou marcados "não testado".
- [ ] Axe por rota e estado (quando existir), `incomplete` lido; leitor de tela testado ou declarado como lacuna.
- [ ] Nenhuma declaração de conformidade legal.
- Evidência: achados no formato `achado-a11y.md`, lista "não testado".

### 8. UX writing
- [ ] Botões verbo + objeto; erros em três partes; estados vazios com ação; confirmações destrutivas nomeiam a perda.
- [ ] Tom marcado Suposição quando sem guia de voz; nenhum número, prazo ou política inventado.
- Evidência: tabela elemento, recomendação, alternativas, justificativa, nota de localização.

### 9. Movimento
- [ ] Cada animação tem propósito; só `transform` e `opacity`; sem `transition: all`.
- [ ] `prefers-reduced-motion` respeitado; nada piscando mais de 3 vezes por segundo; movimento contínuo com mais de 5 s é pausável.
- Evidência: trecho de CSS, teste com preferência ligada.

### 10. Handoff
- [ ] Spec com props tipadas, estados, tokens consumidos, teclado, nota de acessibilidade, comportamento responsivo, casos de borda e critérios de aceite.
- [ ] O que reutiliza listado; o que é novo, identificado.
- Evidência: `spec-componente-handoff.md`.

### 11. Plataforma
- [ ] Plataforma e versão mínima confirmadas; convenções do ambiente-alvo respeitadas; tamanhos de alvo conforme `apple-e-plataformas.md`.
- [ ] Nenhuma migração nativa por estética; Material 3 declarado como lacuna quando relevante.

### 12. Performance percebida
- [ ] Fluxos de clique e tecla com INP ≤ 200 ms no p75 (campo) ou "não medido"; sem salto de layout visível durante a carga.
- [ ] Esqueleto de carregamento com formas iguais ao conteúdo real.

### 13. Avaliação
- [ ] `design-evaluator` acionado quando o custo se justifica; resultado rotulado como opinião de modelo da mesma família.
- [ ] Os 3 achados mais graves listados com o que testar com usuários.

## Critérios de aceite da entrega

Adaptados do checklist de aceite do brain; todos precisam de evidência ou do rótulo "Não verificado".

- [ ] Plataforma, stack e versão mínima confirmadas.
- [ ] Funções originais preservadas e mapa de alterações disponível.
- [ ] Comandos e atalhos implementados, não apenas desenhados.
- [ ] Todos os estados relevantes têm comportamento e teste ou verificação.
- [ ] Tokens, tipografia e densidade seguem o produto e a plataforma.
- [ ] Navegação por teclado e foco avaliados no fluxo.
- [ ] Preferências e tecnologias assistivas pertinentes verificadas.
- [ ] Temas e fundos reais não destroem a legibilidade (contraste medido).
- [ ] Redimensionamento, overflow e dados extremos não quebram a tarefa.
- [ ] Falha e recuperação preservam informações e evitam ação duplicada.
- [ ] Persistência, segurança e performance não foram inferidas de screenshots.
- [ ] Limitações de protótipo e medições não realizadas estão explícitas.

## Fechamento

Relatório (`relatorio-auditoria-ui.md`) mais `checkpoint-handoff.md`, com: matriz preenchida; lacunas de pesquisa do segmento (Material 3, motion, internacionalização e RTL, survey, handoff com Figma, UX writing em PT-BR); a frase "esta revisão é opinião de modelo e não substitui validação com usuários"; e o próximo passo concreto.
