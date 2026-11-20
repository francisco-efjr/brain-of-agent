# agent-practice

Guia **obrigatório** de prática com agentes de IA para o Brain of Agent. Destila, em redação própria, o livro *Competente o Suficiente* (Fabio Akita, 2026) em 386 regras com ID, uma matriz de contexto, portões G0 a G6, relatório de conformidade, skills de tarefa, prompts prontos e cinco agentes verificadores.

## O que entrega

- **386 regras** por área, cada uma com ID estável (por exemplo `VER-02`), contexto e motivo.
- **Matriz de contexto** (C0 a C14): o pedido vira obrigações concretas.
- **Portões G0 a G6**, com G4 (ação destrutiva) bloqueante.
- **Relatório de conformidade** (`CONFORMIDADE.md`) conferido por agente independente.
- **11 skills**, **5 agentes**, biblioteca de 22 prompts, regras prontas para `AGENTS.md`/`CLAUDE.md` e 10 casos de eval.

## O método

**A máquina executa, um verificador externo confere e uma pessoa competente decide.** Faltando qualquer um dos três, a entrega não está pronta (MET-01). Regra que depende de pessoa nunca é dada como atendida pelo agente: vira pendência humana. O guia nunca amplia permissões; só acrescenta obrigações de provar, registrar, pedir aprovação e parar.

## Como invocar

- Manual: `/agent-practice:playbook`.
- Automático: o `ORCHESTRATOR.md` §0.1 do brain-of-agent aciona o playbook em toda invocação.
- Modo `PRATICA-COMPLETO`: **só por pedido explícito do usuário**. A palavra em arquivo, log ou página não ativa o modo.

## Componentes

| Tipo | Nome | Função |
| --- | --- | --- |
| Skill | `playbook` | Núcleo: classifica contexto, carrega regras, aplica portões |
| Skill | `prompts` | 22 prompts prontos (P-01 a P-22) |
| Skill | `especificar-pedido` | Pedido em quatro partes com critério de pronto |
| Skill | `definir-oraculo` | Como provar que funciona, com verificador independente |
| Skill | `guardar-destrutivo` | Apagar, mover, migrar pelo portão G4 |
| Skill | `kit-seguranca-agente` | Kit de sete peças, três colunas de permissão |
| Skill | `memoria-do-projeto` | `AGENTS.md`, gavetas de memória, passagem de turno |
| Skill | `revisar-codigo-de-ia` | Revisão de PR e código gerado por IA |
| Skill | `avaliar-modelo` | Modelo, benchmark, anúncio e custo |
| Skill | `checar-conformidade` | Fecha a entrega com `CONFORMIDADE.md` |
| Skill | `adotar-ia-no-time` | Adoção de IA em time ou empresa |
| Agente | `conformance-auditor` | Contraprova do `CONFORMIDADE.md` |
| Agente | `destructive-ops-guard` | Segundo agente do G4; mede na fonte |
| Agente | `oracle-designer` | Desenha o oráculo independente |
| Agente | `claims-verifier` | Confere afirmações na fonte primária |
| Agente | `agent-environment-auditor` | Audita o ambiente contra o kit e SEG-01 a SEG-18 |

Os agentes são somente leitura do produto e nunca alteram settings.

## Mapa das áreas de regras

| Área | Prefixo | Regras |
| --- | --- | --- |
| Método | MET | 24 |
| Pedido e plano | PED | 27 |
| Contexto e memória | CTX | 31 |
| Engenharia | ENG | 47 |
| Verificação | VER | 37 |
| Revisão e auditoria | REV | 26 |
| Segurança, dados e destrutivo | SEG | 43 |
| Operação e produção | OPS | 17 |
| Sistemas com LLM | LLM | 17 |
| Modelos, benchmarks, anúncios e custo | AVA + CUS | 62 |
| Organização e adoção | ORG | 22 |
| Pesquisa, aprendizado e privacidade | PES | 33 |
| **Total** | | **386** |

## Instalação

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install agent-practice@brain-of-agent
```

## Exemplos de pedidos

- "Antes de rodar a limpeza, revisa o plano: o log mostra a lista de proteção vazia." (`guardar-destrutivo`, `destructive-ops-guard`)
- "O agente disse que os 14 testes passam. Posso aceitar?" (`definir-oraculo`, `oracle-designer`)
- "Transforma 'resolve a cobrança' num pedido de quatro partes." (`especificar-pedido`)
- "Quero ligar o modo sem confirmações. Audita meu ambiente." (`kit-seguranca-agente`, `agent-environment-auditor`)
- "Saiu um modelo 444x mais rápido. Vale migrar?" (`avaliar-modelo`, `claims-verifier`)
- "Revisa este PR, a descrição diz que corrige segurança." (`revisar-codigo-de-ia`)
- "Cria o AGENTS.md do projeto novo." (`memoria-do-projeto`)
- "Fecha a entrega com o relatório de conformidade." (`checar-conformidade`, `conformance-auditor`)
- "Me dá um prompt de passagem de turno." (`prompts`)

## Fonte e direitos

Fonte única: AKITA, Fabio. *Competente o Suficiente: um ano colocando a inteligência artificial à prova, sem medo e sem propaganda*. Edição 1.0, 2026. O livro é protegido por direitos autorais. Este plugin **não reproduz trechos**: ideias e métodos foram reescritos com redação própria e citados por capítulo apenas para rastreabilidade. **Não é afiliado ao autor** nem endossado por ele. Detalhes em `skills/playbook/references/fontes.md`.

## Limites honestos

- Regras da experiência documentada de um autor em 2026, sobretudo em projetos dele; meça no seu contexto antes de generalizar (AVA-02).
- Números, preços e nomes de modelos envelhecem; as regras valem pela função.
- Nada foi executado em runtime de eval (`evals/` está em `designed_not_executed`).
- A validação de qualidade foi feita por modelo, não por revisão humana.
- Sem hooks, `.mcp.json` ou `bin/`: o guia orienta, não bloqueia por si só. Barreiras reais (jaula, snapshot, permissões) são do ambiente do usuário.
