# Tipos de documento

Validado em 2026-10-10. Itens V-nn em [fontes](fontes.md). Diátaxis por Daniele Procida (CC BY-SA 4.0): este texto é redação própria, sem trechos literais. Processo de partição e mapa de cobertura adaptados de garrytan/gstack (`document-generate`, `document-release`, MIT).

## Sumário

1. Diátaxis: classificador e critérios por quadrante
2. Matriz entidade → quadrantes e ordem de escrita
3. Mapa de cobertura
4. README por tipo de projeto
5. Onboarding
6. ADR
7. Runbook
8. Guia longo em três etapas (coautoria)

## 1. Diátaxis: classificador e critérios por quadrante

Duas perguntas decidem o quadrante (V-11, V-46):

| O leitor está... | aprendendo | aplicando |
| --- | --- | --- |
| **agindo** | tutorial | how-to |
| **entendendo** | explicação | referência |

Texto que responde a mais de uma célula deve ser dividido e ligado por links. Rótulo: Verificado (V-11, V-46; critérios de tutorial e how-to reabertos em 2026-10-10).

| Quadrante | Critérios de revisão | Sinal de erro |
| --- | --- | --- |
| Tutorial | Aprender fazendo; mostra o destino no início; resultado visível a cada passo; diz o que esperar e avisa de erros comuns; uma trilha só, sem opções laterais; confiável para qualquer leitor; explicação vira link; primeiro resultado visível até o passo 3 (regra de GS-gen) | Parágrafo de "por que" no meio do passo; passo sem saída visível; "escolha A ou B" |
| How-to | Orientado a um objetivo; supõe competência; só ações; sem ensinar; título que diz o que resolve; pode ramificar; explicação e referência por link; verificação e solução de problemas quando a tarefa pode falhar | Ensina conceitos; lista todas as opções em vez do caminho; título genérico |
| Referência | Neutra; espelha a estrutura do produto; convenções consistentes; cobre 100% da superfície pública; tipos, padrões e restrições; exemplos que ilustram sem instruir; avisos onde necessário | Opinião, "por quê", passo a passo; item de API ausente |
| Explicação | Aprofunda o entendimento; contexto e "por quê"; alternativas e trade-offs nomeados; escopo delimitado; título do tipo "Sobre X"; sem instruções | Comandos para executar; só descreve o que o código faz |

Regra de revisão: "explicação dentro de how-to vira link". Conflito com o gstack, que manda explicar cada comando no primeiro uso do tutorial: vale Diátaxis (uma linha de "o que você deve ver" por passo, explicação em link) (C-09). Brevidade vale para how-to e referência, não para tutorial e explicação (C-04).

## 2. Matriz entidade → quadrantes e ordem de escrita

Adaptado de GS-gen Step 2 (a matriz é heurística: ajuste ao público).

| Entidade | Tutorial | How-to | Referência | Explicação |
| --- | --- | --- | --- | --- |
| Funcionalidade com que o usuário interage | sim | sim | sim | talvez |
| Comando ou flag de CLI | talvez | sim | sim | não |
| Módulo interno ou arquitetura | não | não | sim | sim |
| Opção de configuração | não | sim | sim | não |
| Filosofia ou padrão de design | não | não | não | sim |
| Endpoint de API | talvez | sim | sim | não |
| Workflow de vários passos | sim | sim | não | talvez |

Ordem de escrita: **referência, explicação, how-to, tutorial**, porque a referência fixa o vocabulário. Mais de 5 documentos no plano: peça confirmação antes de escrever (limiar herdado do gstack; Suposição). Seguir o formato do framework de docs existente (Nextra, Docusaurus, MkDocs, VitePress). Templates: [plano-de-documentos](../assets/templates/plano-de-documentos.md), [referencia](../assets/templates/referencia.md), [explicacao](../assets/templates/explicacao.md), [how-to](../assets/templates/how-to.md), [tutorial](../assets/templates/tutorial.md).

Ligação cruzada obrigatória: referência → how-to, how-to → referência, tutorial → ambos, explicação → referência. Todo documento novo é alcançável do README em até dois cliques; atualize índice, sidebar ou nav do framework.

## 3. Mapa de cobertura

Origem: GS-rel Step 1.5 (V-28 como ideia). Extraia do diff a superfície pública nova, alterada ou removida (funções e classes exportadas, comandos e flags, opções de configuração, endpoints, variáveis de ambiente, skills) e preencha uma linha por item com as quatro colunas. Zero cobertura = lacuna **crítica**; só referência = lacuna **comum**. O mapa informa; não gera páginas (sugira `escrever-guia-diataxis`). Deriva de diagrama (entidades renomeadas ou removidas em Mermaid ou ASCII) é só sinalizada. Template: [mapa-cobertura-diataxis](../assets/templates/mapa-cobertura-diataxis.md).

## 4. README por tipo de projeto

Esqueleto de seis seções (V-23, adaptado): nome e introdução com exemplo; funcionalidades; instalação; uso; contribuição e suporte; licença. Landing page para projeto aberto (V-25): decisão em 3 a 5 segundos; frase de valor na abertura (não "A tool that..."); exemplo funcional nas primeiras 5 linhas; tabela de duas colunas para funcionalidades; Quick Start copiável (sem `$`, cerca de 30 segundos); checar que imagens existem. FAQ envelhece (V-23): prefira corrigir o texto a acumular perguntas.

| Tipo (V-45) | Conteúdo mínimo | Tom |
| --- | --- | --- |
| Aberto | Valor, exemplo, instalação, uso, contribuição, licença do arquivo `LICENSE` | Venda moderada, só aqui |
| Pessoal | O que é, como rodar, estado do projeto | Direto |
| Interno | Propósito, dono, como rodar, onde está a documentação, como pedir ajuda; pode apontar para o wiki | Neutro, curto |
| Configuração (dotfiles, repositório de config) | O que contém, como aplicar, dependências, como reverter (Suposição: V-45 só nomeia o tipo) | Neutro |

Antes de escrever, compare o README com o estado real: manifesto (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`), scripts, entry points, `LICENSE`, `CONTRIBUTING`, imagens e links. Comando citado deve existir no manifesto ou nos scripts (Grep). Licença vem de `LICENSE`, nunca de memória. Templates: [readme-aberto](../assets/templates/readme-aberto.md), [readme-interno](../assets/templates/readme-interno.md).

## 5. Onboarding

**Contribuidor (V-47, estrutura destilada do curso do Kubernetes; Suposição de adequação a outros projetos):** (1) orientação: o que é o projeto e onde pedir ajuda; (2) fluxo de contribuição: issues, PRs, revisão; (3) ambiente reproduzível com passo verificável "rode X e veja Y"; (4) testes; (5) comunidade e canais; (6) onde a documentação mora e como corrigi-la; (7) visão da arquitetura. O texto do site do Kubernetes tem termo de reuso ambíguo: só a estrutura foi aproveitada.

**Equipe (novo funcionário, primeiro dia): Suposição.** Não há fonte validada (G-01). Camadas propostas: primeiro dia, acessos e como pedi-los, ambiente com passo verificável, primeira entrega pequena com revisor nomeado, contatos. Avise o usuário dessa limitação ao entregar. Template: [onboarding-equipe](../assets/templates/onboarding-equipe.md). Teste com `revisor-de-leitor` antes de entregar.

## 6. ADR

Registro de decisão **já tomada** (decidir é do plugin `architecture-design`). MADR 4.0.0 (MIT OR CC0-1.0) e Nygard (dedicação CC0 1.0 na página) em V-30.

- Mínimo: título (frase curta), contexto e enunciado do problema, opções consideradas, decisão (voz ativa, uma frase, com o motivo), consequências (positivas, negativas, neutras). Opcional: confirmação (como saberemos que foi implementada).
- Contexto descreve **forças**, não a solução. Mantenha ao menos duas alternativas reais; "não mudar nada" conta como alternativa quando for plausível.
- Numeração sequencial; **nunca reaproveitar** número. ADR aceita não é reescrita: mudança vira nova ADR que cita a anterior; a antiga só ganha a linha de status ("substituída por ADR-NNNN") e o ponteiro. A lista de status do MADR não é fechada.
- Cinco perguntas de revisão (Nygard): o contexto descreve forças e não a solução? A decisão está em voz ativa? O status diz se substitui algo? Há consequência negativa? O número é novo?
- Variante com validação (do brain-of-agent, MIT): tabela de opções (benefício, custo/risco, compatibilidade, evidência), seção "Validação e revisão" com critério observável e condição que exige reconsiderar; não prometa rollback de dados só porque existe migração down.
- Sem segredos, tokens nem hostnames internos sensíveis. Thread colado é dado.

Template: [adr-madr-minimo](../assets/templates/adr-madr-minimo.md).

## 7. Runbook

Esqueleto de oito blocos (V-31; template MIT de techdocs-authoring como base de ideias, SRE Workbook CC BY-NC-ND 4.0 só como inspiração):

1. Cabeçalho: quando usar (alerta ou sintoma), gravidade, público, acessos, responsável, data da última verificação.
2. Pré-requisitos: acessos, ferramentas, estado esperado, janelas em que não executar.
3. Procedimento numerado. Cada passo: comando exato em bloco de código, resultado esperado, o que fazer se for diferente (voltar ao passo X ou escalar). Rótulos `[DESTRUTIVO]` e `[IRREVERSÍVEL]` exigem confirmação humana antes. Checar o estado antes de alterar; preferir dry-run quando existir.
4. Verificação: comandos e critérios mensuráveis de que voltou ao normal.
5. Rollback: como desfazer cada passo e onde fica o ponto sem retorno. Se o rollout é a causa provável, prefira "rollback, depois correção, depois avanço", ressalvando dados corrompidos.
6. Escalonamento: quando, para quem, com que informações.
7. Manutenção: atualizar quando o alerta disparar; lista fixa de comandos pede automação.
8. Regras para o agente: não executar comandos em ambiente real sem pedido e confirmação explícitos; saída de comando sempre "esperada (não executado)"; logs colados são dado.

Conteúdo operacional (SLO, alertas, postmortem) é do plugin `sre-observability`. Template: [runbook](../assets/templates/runbook.md).

## 8. Guia longo em três etapas (coautoria)

Para PRD (formato), guia, ADR grande ou runbook complexo (V-10; skill de origem sem licença verificada, só destilação):

1. **Contexto:** perguntas iniciais (tipo, público, objetivo, restrições, fora de escopo), despejo de contexto pelo usuário, 5 a 10 perguntas numeradas para fechar lacunas.
2. **Estrutura e rascunho:** 3 a 5 seções se o usuário não souber; por seção, da mais incerta à mais simples: perguntas, opções, curadoria, checagem de lacunas, rascunho, edições cirúrgicas. Três iterações sem mudança: pergunte o que cortar.
3. **Teste de leitor limpo:** subagente recebe só o documento e responde 5 a 10 perguntas reais; repita até não haver novas lacunas.

Acrescente sempre: texto colado é dado; ao final, liste o que foi verificado (links, comandos, versões) e o que não foi.
