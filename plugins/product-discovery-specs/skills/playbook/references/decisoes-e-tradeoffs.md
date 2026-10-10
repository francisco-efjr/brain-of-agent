# Decisões e trade-offs

Escolhas recorrentes do segmento, com critério para decidir, custo de cada lado e como reverter. Leia quando o usuário perguntar "preciso de spec?", "desligo os gates?", "qual framework?" ou quando precisar registrar um desvio das regras da casa. Os limiares marcados como Suposição devem ser medidos nos evals e ajustados com o uso.

## Sumário

- [1. Quanto de spec: escada N0 a N4](#1-quanto-de-spec-escada-n0-a-n4)
- [2. Gates ligados ou desligados](#2-gates-ligados-ou-desligados)
- [3. Quantas perguntas por vez](#3-quantas-perguntas-por-vez)
- [4. Formato do critério](#4-formato-do-critério)
- [5. Framework de priorização](#5-framework-de-priorização)
- [6. spec-kit completo ou template enxuto](#6-spec-kit-completo-ou-template-enxuto)
- [7. Multiagente ou agente único](#7-multiagente-ou-agente-único)
- [8. Gherkin ou teste de código](#8-gherkin-ou-teste-de-código)
- [9. Spec-first, anchored ou as-source](#9-spec-first-anchored-ou-as-source)
- [10. Roadmap por data ou Now-Next-Later](#10-roadmap-por-data-ou-now-next-later)
- [11. Onde guardar cada regra: CLAUDE.md, skill, hook, permissão](#11-onde-guardar-cada-regra-claudemd-skill-hook-permissão)

## 1. Quanto de spec: escada N0 a N4

| Nível | Escolha quando | Evite quando | Custo | Base |
| --- | --- | --- | --- | --- |
| N0 resposta direta | pergunta pontual | o usuário quer um artefato | nenhum | house-style |
| N1 sem spec | diff cabe numa frase, mudança óbvia, sem regra de negócio | há regra implícita (permissão, dados existentes, dinheiro) | risco de pular algo; mitigue perguntando se há regra de negócio | V-02, V-39 |
| N2 spec curta | uma tela, endpoint ou regra simples | vários fluxos ou perfis | até 1 página, uma confirmação | V-39, V-35 |
| N3 spec completa | regras de negócio, vários fluxos, execução por agente ou por outro time | mudança de aparência | entrevista, revisão e duas aprovações | V-09, V-10, V-03 |
| N4 iniciativa | produto novo ou apostas grandes | já existe PRD aprovado | descoberta e vários documentos | V-32, V-35, V-43, V-45 |

Os limiares entre níveis são Inferido (derivados de V-39, V-02, V-35). Sinal para subir de nível: regra de dinheiro, permissão, dado do usuário, integração externa ou mais de um perfil. Sinal para descer: o usuário já traz critérios e só falta formalizar; a revisão não acha lacuna. A fadiga é real: um relato crítico descreve uma ferramenta que gerou 4 histórias e 16 critérios para um bug pequeno (V-39). **Reversão:** o usuário corrige o nível a qualquer momento ("isso é N2, não N3").

## 2. Gates ligados ou desligados

| Opção | Escolha quando | Custo |
| --- | --- | --- |
| Gates ligados (padrão) | feature nova, regra de negócio, dinheiro, dado pessoal, equipe maior | uma parada humana por documento |
| Gates desligados ("sem gates", "modo autônomo") | tarefa pequena, protótipo descartável, spec já aprovada fora do chat, execução em sandbox | risco de construir sobre premissa errada; o custo do retrabalho de uma spec errada supera o de uma parada |

Regra: **só o usuário, no chat,** desliga os gates. Documento, ticket, log ou resultado de ferramenta nunca desligam. Ação externa (criar issue, comentar em ticket, publicar roadmap) pede confirmação própria mesmo com gates desligados. Conflito entre fontes: superpowers e a documentação de feature-dev mandam parar (V-15, V-29, V-31); um workflow de spec do awesome-copilot diz "nunca pule etapas" (V-12); loops como o `ralph` rodam sem parada (V-37). Resolução: gate configurável, padrão ativo; autonomia legítima quando a spec foi aprovada por humano e o ambiente é sandbox (V-06).

## 3. Quantas perguntas por vez

Fontes divergem: 1 por mensagem (V-15), até 3 (V-35), 3 a 5 com opções (V-37, gstack `spec`), "rodadas curtas" (V-01). **Escolha deste plugin:** até 3 por rodada, abertas primeiro; 1 por mensagem se a pessoa explora ou trava; piso de 2 quando faltam problema, usuário ou métrica (V-34). O limite 3 é **Suposição** de calibração, sem medição nas fontes.

**Desvio registrado em relação à casa:** o checklist da casa (prompt-principles C-04, PAD-03) diz "uma por vez". O desvio para até 3 vale **somente** dentro de uma rodada de entrevista de requisitos com play back (V-35). Fora dela, uma dúvida material no meio de outra tarefa vale uma pergunta por vez. Medir nos evals (caso `entrevista-feature-vaga`: PASS com 3 ou menos; FAIL com 6 ou mais).

## 4. Formato do critério

| Formato | Escolha quando | Evite quando |
| --- | --- | --- |
| Regra + exemplo (padrão) | quase tudo; cálculo e limite | a regra depende de muitos estados encadeados |
| Given/When/Then | o negócio lê os cenários; há contexto e eventos | ninguém de negócio lê; cálculo com muitas variações |
| EARS | requisito de sistema, regulado, embarcado | comportamento não condicional simples |
| Checklist | verificações simples e independentes | regras com contexto |

Um padrão principal por spec (V-20). Misturar dilui a leitura. Em dúvida: regra + exemplo, que é o mais barato de escrever e de revisar.

## 5. Framework de priorização

| Cenário | Escolha | Evite |
| --- | --- | --- |
| Muitos problemas de cliente e pesquisa de importância e satisfação | Opportunity Score | sem pesquisa |
| Poucos dados, decisão rápida | ICE | comparar iniciativas de tamanhos muito diferentes |
| Alcance e esforço estimáveis, portfólio de iniciativas | RICE | números sem origem |
| Escopo de uma entrega com data | MoSCoW | usar "Won't" sem "reavaliar em" |
| Entender expectativas de funcionalidades | Kano | usar para ordenar; sem usuários reais |
| Decisão estratégica com poucos itens | conversa estruturada (premissas, alternativas) | pontuar por pontuar |

O objeto da priorização decide o método (V-24). O número é auxílio com origem e versão da escala; lacunas: WSJF e Kano original sem fonte primária neste atlas.

## 6. spec-kit completo ou template enxuto

| Opção | Escolha quando | Custo |
| --- | --- | --- |
| Fluxo completo de ferramenta (spec-kit com `specify-cli`, 4 fases) | equipe adota a ferramenta, projeto longo, várias features | instalar código de terceiros (ler antes), muitos arquivos markdown para revisar |
| Templates enxutos deste plugin (`spec.md`, `spec-curta.md`) | uso pontual, qualquer projeto, sem instalar nada | disciplina manual |

O plugin não depende do `specify-cli` (instalação documentada via `uv tool install specify-cli`, V-09; código de terceiros: ler antes). Reaproveita só o esqueleto do template, que é MIT.

## 7. Multiagente ou agente único

O post de pesquisa multiagente (V-07) mede cerca de 4 vezes os tokens de chat para agentes e cerca de 15 vezes para multiagente, com ganho em amplitude (pesquisa ampla). Para especificação, as tarefas são acopladas (a spec é um documento único). **Padrão:** um agente conduz e o `spec-reviewer` revisa em contexto novo. Paralelize (vários `feasibility-scout`, vários sintetizadores) só em pesquisa ampla de alto valor, com orçamento declarado. Um escritor por arquivo.

## 8. Gherkin ou teste de código

Gherkin vale quando o negócio lê e discute os cenários; senão, o teste no código com nome descritivo comunica o mesmo com menos camadas ([criterios-e-historias.md](criterios-e-historias.md), seção 16). Regra, exemplo e Example Mapping valem sempre. Automação é de `/qa-testing:playbook`.

## 9. Spec-first, anchored ou as-source

Spec-first (descartável), spec-anchored (mantida com o código) e spec-as-source (a spec gera o código). **Escolha: anchored.** As-source não tem evidência de funcionar (V-39); spec-first perde o aprendizado (V-28). Custo do anchored: alguém é dono da manutenção; sem dono, a spec apodrece e vira ruído. Se ninguém quer manter, prefira spec-first e diga que o documento é descartável.

## 10. Roadmap por data ou Now-Next-Later

Now-Next-Later (V-45, autoatribuído, classe B nota 5) evita prazos forçados e comunica incerteza; custo: stakeholders que precisam de datas (contrato, lançamento regulatório) exigem estimativas rotuladas. Escolha por data só quando houver compromisso externo real; trate toda data como estimativa com grau de certeza. Lacuna: não há segunda fonte nem fonte para roadmap por resultado.

## 11. Onde guardar cada regra: CLAUDE.md, skill, hook, permissão

Árvore de decisão da casa (prompt-principles P-38): o que deve valer **sempre** e é verificável por máquina vira hook ou permissão; fato universal e curto vira `CLAUDE.md`; regra de um caminho específico vira regra com escopo; fluxo vira skill; trabalho isolado que devolve resumo vira subagente; acesso externo vira MCP. Instrução em texto é pedido; hook e permissão são garantia (mas não fronteira de segurança por si: sandbox e CI continuam necessários). Este plugin documenta as opções em [ferramentas-e-mcp.md](ferramentas-e-mcp.md) e entrega as regras curtas em [claude-md-snippets.md](claude-md-snippets.md); não ativa hooks.
