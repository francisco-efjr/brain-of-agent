# Pesquisa: core de memória de longo prazo

Data: 2026-11-19 · Pesquisador: Claude Opus 5.5 (Claude Code) · Consultas de busca: 22 · Documentos do ai-memory lidos: 10 (trechos) · Fontes catalogadas: 41 (34 de classe A, 7 de classe B).

Base pedida pelo dono: [akitaonrails/ai-memory](https://github.com/akitaonrails/ai-memory) (MIT, cerca de 16 mil estrelas, ativo em 2026-11-19). O repositório foi clonado só para leitura; nada dele foi executado nem copiado literalmente, só os princípios de desenho, com redação própria. Status de leitura: **Repositório** (trechos lidos no clone), **Íntegra**, **Resumo** ou **Busca**, como nos outros temas.

## 1. Princípios tirados do ai-memory

| Princípio | No ai-memory | Como entrou no core |
| --- | --- | --- |
| Markdown é a fonte da verdade | Wiki de `.md` versionado com git; banco é índice derivado (A-01, A-02) | Memória em `IA-Operador\memoria\`, reindexada com `jarvis memory index` |
| Níveis com durações diferentes | Trabalho, episódico, semântico, procedimental; só episódico envelhece (A-03) | Pastas `perfil`, `decisoes`, `procedimentos`, `episodios`, `sessoes` |
| Nada se apaga de vez | Versão nova substitui; original no git; `restore-page` (A-01, A-03) | Campo `substitui`, pasta `arquivo\`, commit por mudança, apagar de vez é R3 |
| Envelhecer sem perder o essencial | Episódio frio vira fatos duráveis; uso estende a vida da página (A-03) | Compactação proposta após uns 60 dias sem uso, com "sim" |
| Origem pesa | Classes de confiança: operador, modelo, ferramenta (A-04) | Campo `origem`; ferramenta nunca vira regra sem confirmação |
| Passagem de bastão | Onde parou, o que falhou, o que está aberto (A-01) | `<memoria-bastao>` e leitura do último bastão no início |
| Perfil abaixo das regras | Instrução atual > regras do projeto > memória > perfil; dizer qual padrão aplicou (A-05) | Ordem de autoridade no cartão e regra de citar a nota usada |
| Regra fixa é escassa | Promover memória para regra só se esquecer causar erro em muitas tarefas (A-06) | Memória fica nas pastas; o CORE só muda pela esteira |
| Começo de sessão com orçamento | Resumo inicial limitado, resumos curtos antes de textos inteiros (A-07) | No início, só perfil e último bastão |
| Local e sem telemetria | Embeddings em nuvem são o maior caminho de saída de dados (A-08) | Embeddings locais; invariante de privacidade da base |

## 2. Achados das outras fontes

1. **Memória como paginação.** O contexto é a RAM e o disco é a memória externa; o agente traz e devolve conforme precisa (P-01).
2. **Tipos de memória têm riscos diferentes.** Escrever em memória procedimental muda o comportamento futuro e pede mais cuidado (P-03). Daí procedimento só com comando e verificação.
3. **Arquivos simples competem com sistemas especializados.** Agente com ferramentas de arquivo marcou 74,0% no LoCoMo, segundo a Letta (D-01); o padrão "LLM wiki" e o OKF consolidam markdown com cabeçalho YAML (D-02, D-03).
4. **Lembrar com critério.** Recência, importância e relevância (P-02); reflexões sobre falhas (P-10); rotinas reaproveitáveis (P-11).
5. **Atualizar e se abster são os pontos fracos.** O LongMemEval mede atualização de conhecimento e abstenção, em que assistentes comerciais caem bastante (P-07). Daí as regras de contradição e de "não sei".
6. **Esquecer é útil.** Curva de Ebbinghaus replicada (P-17); o MemoryBank fortalece o que é lembrado (P-06).
7. **Envenenamento é real e passa pelas defesas de prompt.** MINJA com 98,2% de injeção (P-14); defesas no caminho de escrita, com proveniência (P-15); experiências falsas imitadas (P-16).
8. **Passagem estruturada reduz erro.** I-PASS reduziu erros médicos em 23% (P-18).

## 3. Validação da esteira para memória

| Passo | Em memória | Evidência |
| --- | --- | --- |
| 0 Classificar | Gravar a pedido é R1; limpar ou compactar é R2; apagar de vez é R3 | A-03 (nada destrutivo por padrão) |
| 1 Estruturar | O que lembrar, por quê, e procurar nota existente | P-07 (atualização), A-01 (quase-duplicatas) |
| 2 e 3 Visão e teste | Vai duplicar? Vai contradizer? É de origem ferramenta? | A-04, P-15 |
| 5 e 6 Conceber e produzir | Nota curta, uma ideia, cabeçalho com origem e datas | D-03, D-09, P-09 |
| 7 Testar de novo | Sem segredo, sem dado sensível, sem ordem embutida | A-08, P-14 |
| 9 e 10 Implementar e verificar | Gravar, reindexar e conferir que a busca acha a nota; bastão no fim | D-12, A-01 |

A esteira serve sem mudança. O estudo acrescenta ao tema duas verificações próprias: "a busca encontra o que gravei?" e "esta nota pode ser veneno?".

## 4. Decisões de desenho

- **Cartão sempre carregado, regras completas buscadas.** O tema entra no prompt padrão só como cartão de 7 linhas; as regras completas ficam na memória (`CORE-MEMORIA` indexado). Segue o próprio princípio do ai-memory de que regra fixa é escassa (A-06).
- **Sem instalar nada.** O core funciona com arquivos e o `jarvis memory index` que já existe. O ai-memory fica como opção de instalação (R2), documentada na referência.
- **Pastas em português e nomes estáveis**, para o dono navegar no Explorer e no Obsidian.

## 5. Limites

- Os documentos do ai-memory foram lidos por trechos (cabeçalhos e primeiras seções); detalhes de implementação não foram auditados.
- O ai-memory cita um estudo (arXiv 2611.09721) sobre resultado de ferramenta envenenado sobreviver à escrita em memória; não foi encontrado na busca. O core se apoia nos estudos encontrados (P-14, P-15, P-16).
- Números de Mem0, Hindsight e Letta são dos próprios autores, com métodos diferentes.
- A leitura da LGPD é Inferida e não é parecer jurídico.
- Nada foi executado no PC do dono; os casos de eval estão `designed_not_executed`.

## 6. Fontes

### 6.1 ai-memory (A)

| ID | Documento | Classe | Status | Usado em |
| --- | --- | --- | --- | --- |
| A-01 | [README](https://github.com/akitaonrails/ai-memory/blob/main/README.md) | A | Repositório | Markdown como fonte, bastão, captura, envelhecimento, contradições |
| A-02 | [docs/ARCHITECTURE.md](https://github.com/akitaonrails/ai-memory/blob/main/docs/ARCHITECTURE.md) | A | Repositório | Wiki versionado e índice derivado |
| A-03 | [docs/design-memory-aging.md](https://github.com/akitaonrails/ai-memory/blob/main/docs/design-memory-aging.md) | A | Repositório | Níveis, retenção, compactação, nada apagado |
| A-04 | [docs/design-memory-poisoning-provenance.md](https://github.com/akitaonrails/ai-memory/blob/main/docs/design-memory-poisoning-provenance.md) | A | Repositório | Classes de confiança e proveniência |
| A-05 | [docs/cross-project-profile.md](https://github.com/akitaonrails/ai-memory/blob/main/docs/cross-project-profile.md) | A | Repositório | Perfil abaixo das regras |
| A-06 | [docs/design-rules-promotion.md](https://github.com/akitaonrails/ai-memory/blob/main/docs/design-rules-promotion.md) | A | Repositório | Regra fixa é escassa |
| A-07 | [docs/design-tiered-session-brief.md](https://github.com/akitaonrails/ai-memory/blob/main/docs/design-tiered-session-brief.md) | A | Repositório | Resumo de início com orçamento |
| A-08 | [DATA_HANDLING.md](https://github.com/akitaonrails/ai-memory/blob/main/DATA_HANDLING.md) | A | Repositório | Local, sem telemetria, embeddings |
| A-09 | [docs/research-2026-landscape.md](https://github.com/akitaonrails/ai-memory/blob/main/docs/research-2026-landscape.md) | A | Repositório | Panorama: OKF, Letta, concorrentes |
| A-10 | [docs/windows.md](https://github.com/akitaonrails/ai-memory/blob/main/docs/windows.md) | A | Repositório | WSL2 suportado, Windows nativo experimental |

### 6.2 Artigos (P)

| ID | Fonte | Classe | Status | Usado em |
| --- | --- | --- | --- | --- |
| P-01 | [Packer et al. MemGPT (2023)](https://arxiv.org/abs/2310.08560) | A | Busca | Contexto como RAM, memória externa |
| P-02 | [Park et al. Generative Agents (UIST 2023)](https://arxiv.org/abs/2304.03442) | A | Busca | Recência, importância, relevância, reflexão |
| P-03 | [Sumers et al. CoALA (TMLR 2024)](https://arxiv.org/abs/2309.02427) | A | Busca | Tipos de memória |
| P-04 | [Chhikara et al. Mem0 (2025)](https://arxiv.org/abs/2504.19413) | B | Busca | Extração e fusão de fatos |
| P-05 | [Rasmussen et al. Zep (2025)](https://arxiv.org/abs/2501.13956) | B | Busca | Dois tempos e validade dos fatos |
| P-06 | [Zhong et al. MemoryBank (AAAI 2024)](https://arxiv.org/abs/2305.10250) | A | Busca | Esquecimento à Ebbinghaus |
| P-07 | [Wu et al. LongMemEval (ICLR 2025)](https://arxiv.org/abs/2410.10813) | A | Busca | Cinco habilidades, atualização e abstenção |
| P-08 | [Maharana et al. LoCoMo (ACL 2024)](https://aclanthology.org/2024.acl-long.747) | A | Busca | Conversas longas |
| P-09 | [Xu et al. A-MEM (NeurIPS 2025)](https://arxiv.org/abs/2502.12110) | A | Busca | Notas ligadas à Zettelkasten |
| P-10 | [Shinn et al. Reflexion (NeurIPS 2023)](https://arxiv.org/abs/2303.11366) | A | Busca | Memória de falhas |
| P-11 | [Wang et al. Agent Workflow Memory (ICML 2025)](https://arxiv.org/abs/2409.07429) | A | Busca | Memória de procedimentos |
| P-12 | [Hu et al. Memory in the Age of AI Agents (2025)](https://arxiv.org/abs/2512.13564) | B | Busca | Taxonomia por função |
| P-13 | [Latimer et al. Hindsight is 20/20 (2025)](https://arxiv.org/abs/2512.12818) | B | Busca | Reter, lembrar, refletir |
| P-14 | [Dong et al. MINJA (NeurIPS 2025)](https://arxiv.org/abs/2503.03704) | A | Busca | Injeção de memória |
| P-15 | [Dash et al. From Untrusted Input to Trusted Memory (ICML 2026)](https://arxiv.org/abs/2606.04329) | A | Busca | Defesa no caminho de escrita |
| P-16 | [Srivastava e He. MemoryGraft (2025)](https://arxiv.org/abs/2512.16962) | B | Busca | Experiências falsas |
| P-17 | [Murre e Dros. Replication of Ebbinghaus' forgetting curve (PLOS ONE 2015)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0120644) | A | Busca | Curva do esquecimento |
| P-18 | [Starmer et al. I-PASS (NEJM 2014)](https://psnet.ahrq.gov/issue/changes-medical-errors-after-implementation-handoff-program) | A | Busca | Passagem de bastão estruturada |

### 6.3 Documentação e produtos (D)

| ID | Fonte | Classe | Status | Usado em |
| --- | --- | --- | --- | --- |
| D-01 | [Letta: Benchmarking AI Agent Memory (2025)](https://www.letta.com/blog/benchmarking-ai-agent-memory) | B | Busca | Arquivos simples no LoCoMo |
| D-02 | [Karpathy: LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | A | Busca | Wiki mantido pelo modelo |
| D-03 | [Google Cloud: Open Knowledge Format](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) | A | Busca | Markdown com `type` |
| D-04 | [Anthropic: Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) | A | Busca | Diretório próprio e proteção de caminho |
| D-05 | [Claude Code: memory](https://code.claude.com/docs/en/memory) | A | Busca | Regras do usuário e notas do agente como contexto |
| D-06 | [OpenAI: Memory FAQ](https://help.openai.com/en/articles/8590148-memory-faq) | A | Busca | Controles de esquecer e apagar |
| D-07 | [LangChain: memory concepts](https://docs.langchain.com/oss/python/concepts/memory) | A | Busca | Semântica, episódica, procedimental; gravar na hora ou depois |
| D-08 | [basic-memory](https://raw.githubusercontent.com/basicmachines-co/basic-memory/main/README.md) | B | Busca | Markdown com entidades e relações |
| D-09 | [Obsidian: Properties](https://obsidian.md/help/properties) | A | Busca | Tipos de propriedade no cabeçalho |
| D-10 | [git restore](https://git-scm.com/docs/git-restore) | A | Busca | Voltar versão de arquivo |
| D-11 | [Lei 13.709/2018 (LGPD), texto compilado](https://www.tce.rn.gov.br/as/Ouvidoria/Legisla%C3%A7%C3%A3o/Lei_137092018_compilado_LGPD.pdf) | A | Busca | Art. 4º, I e art. 18 |
| D-12 | [OpenJarvis: memory](https://open-jarvis.github.io/OpenJarvis/user-guide/memory/) | A | Resumo | Indexar e buscar a memória |
| D-13 | [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | A | Íntegra | Context rot, notas fora do contexto |

Contagem: 10 (A) + 18 (P) + 13 (D) = 41 fontes.
