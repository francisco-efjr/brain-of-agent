# BUILD-REPORT-quality — agent-practice 0.1.0

Validação independente de qualidade, antes da publicação. Data: 2026-11-19. Validador: Claude Opus 5.5, subagente somente leitura (única escrita: este arquivo). Objeto: `plugins/agent-practice/` (dev-segments) e a integração em `brain-of-agent/ORCHESTRATOR.md` (§0.1, §2 B item 7, §3, §3.1, §4, §5, §6) e em `plugins/orchestrator/skills/playbook/SKILL.md`.

> **Revalidação (2026-11-19):** o veredito atual está na seção 13: **aprovado com ressalvas**. As seções 1 a 12 registram a primeira rodada.

Rótulos: **Verificado** = lido ou executado nesta sessão (arquivo:linha, comando ou URL); **Inferido** = julgamento do validador (notas, severidades, estimativas de tokens); **Não verificável** = fora do alcance desta sessão.

## Veredito

**Reprovado no estado atual**, por um bloqueio único e de correção curta (defeito 1): `skills/revisar-codigo-de-ia/SKILL.md:5` declara `allowed-tools: Read, Glob, Grep, Bash`. Pela documentação oficial, `allowed-tools` não restringe nada: pré-aprova as ferramentas listadas, sem pedir permissão, no turno em que a skill roda. Bash sem padrão fica liberado numa skill que lê diff de terceiros. A rubrica trata isso como reprovação automática (teto 40), e o blueprint reprova o pacote quando uma skill de tarefa fica abaixo de 80.

Corrigido o defeito 1, o pacote passa a **aprovado com ressalvas**: os 16 artefatos ficam entre 83 e 93, a fidelidade é de 24 em 24 e não sobra defeito alto. Recomendo publicar só depois dos defeitos 1 a 5, que pedem poucas linhas cada. Os defeitos 6 a 10 podem ir na 0.1.1, e os baixos quando convier.

**Critério usado**
- **Aprovado:** as 16 notas ≥ 80 (rubrica de 12 dimensões, média × 20), nenhum critério de reprovação automática, amostra de fidelidade sem regra "sem base" e com no máximo 2 "exageradas", nenhum defeito alto aberto.
- **Aprovado com ressalvas:** o mesmo, com defeitos médios ou baixos abertos que têm correção pontual e não ampliam permissão nem expõem segredo.
- **Reprovado:** qualquer nota < 80 (inclusive pelo teto de 40), regra "sem base" na amostra ou defeito alto aberto.

**Números:** nota mínima 40 (teto; 83 sem o teto) · média 86,1 (88,8 sem o teto) · fidelidade: 24 fiéis, 0 exageradas, 0 sem base · defeitos: 1 alto, 9 médios, 15 baixos.

## 1. Qualidade de prompt (A)

Rubrica de `docs/foundation/prompt-quality-rubric.md`, D1 a D12 de 0 a 5. As notas são Inferidas: um avaliador, uma passada. Entre parênteses está a nota da dimensão.

| Arquivo | Nota | Dimensões mais fracas |
| --- | --- | --- |
| `skills/playbook/SKILL.md` | 83 | D5 (3): sem exemplo de classificação C0–C14. D9 (3): o G0 manda abrir a matriz e 4 arquivos do C0 (≈ 66 KB) sem resumo nem Grep por ID. D11 (3): não trata auditoria sem escrita, CTX-06 em pergunta pontual nem o escopo do C6 |
| `skills/especificar-pedido/SKILL.md` | 88 | D5 (3): sem pedido preenchido de exemplo. D11 (4): sempre grava `pedido.md`, mesmo em pedido pequeno |
| `skills/definir-oraculo/SKILL.md` | 92 | D5 (3). D3 (4): o passo 4 manda escrever o teste sem dizer quem escreve, contra o passo 2 |
| `skills/guardar-destrutivo/SKILL.md` | 88 | D11 (3): sem escopo do C6 para arquivo versionado na branch. D5 (3). D1 (4): gatilhos amplos (`rm`, "organizar arquivos") |
| `skills/kit-seguranca-agente/SKILL.md` | 87 | D8 (3): o passo 1 inventaria `.env` por leitura. D5 (3) |
| `skills/memoria-do-projeto/SKILL.md` | 88 | D5 (3). D8 (4): cria `AGENTS.md`/`CLAUDE.md` novo sem confirmação |
| `skills/revisar-codigo-de-ia/SKILL.md` | **40** (teto; 83 sem o teto) | D8 (1): `allowed-tools` com `Bash` pré-aprova qualquer comando numa skill que lê conteúdo de terceiros. D12 (3): uso contrário à semântica documentada do campo. D5 (3) |
| `skills/avaliar-modelo/SKILL.md` | 93 | D5 (3). D9 e D11 (4) |
| `skills/checar-conformidade/SKILL.md` | 90 | D11 (3): não trata auditoria sem escrita, tamanho do relatório nem aprovação dada em sessão anterior. D2 (4) |
| `skills/adotar-ia-no-time/SKILL.md` | 88 | D5 (3). D10 (4): erro de digitação. D12 (4): trata como obrigação o que o cap. 20 apresenta como sugestão do autor (o epílogo reforça, então é leve) |
| `skills/prompts/SKILL.md` | 92 | D2 (4). D12 (4): o P-22 usa o kit divergente; as fontes não têm classe A/B/C |
| `agents/conformance-auditor.md` | 88 | D8 (3): aceita aprovação humana "em arquivo datado". D11 (3): trata a falta do arquivo como achado alto mesmo em auditoria sem escrita. D5 (3) |
| `agents/oracle-designer.md` | 93 | D5 (3) |
| `agents/claims-verifier.md` | 92 | D5 (3). D3 (4): o passo 6 pede segunda leitura de outra empresa sem ferramenta para isso |
| `agents/agent-environment-auditor.md` | 83 | D8 (3): lê `.env` e `env` filtrado. D12 (3): o kit de sete peças difere do SEG-S02 e do livro. D5 (3) |
| `agents/destructive-ops-guard.md` | 93 | D9, D11 e D12 (4). O modelo de plano usa "aprovado" num parecer que o agente não pode dar |

Padrão geral: D2, D4, D6, D7 e D10 ficam em 5 em quase tudo. Cada regra traz o porquê, a saída é definida, a evidência é exigida e o tom é calmo. A dimensão mais fraca em todos é D5 (exemplos): só `prompts/SKILL.md` tem exemplo trabalhado, e os modelos em `assets/templates/` compensam em parte.

## 2. Fidelidade ao livro (B)

Método: para cada regra, Grep por palavras-chave no trecho do capítulo indicado (R1–R8) e leitura do entorno. Nenhum trecho do livro é reproduzido aqui. As páginas são aproximadas, tiradas da marcação do PDF.

| ID | Capítulo (passagem aprox.) | Veredito | Justificativa |
| --- | --- | --- | --- |
| MET-05 | prefácio; cap. 4 (p. ~59) | Fiel | O autor só publica capítulo que leu e aprovou, como faz com o código do agente, e diz que a conclusão é de quem usa. A regra generaliza essa prática ao método |
| MET-02 | cap. 6 (p. ~79–80) | Fiel | O humano traz o quê e o porquê, e o agente traz o como. O agente é fraco em prioridade e domínio e nunca discordou de um pedido |
| PED-01 | cap. 9 (p. ~120–121) | Fiel, endurecida | As quatro partes estão lá, com a quarta descrita como a traiçoeira. "Não se começa" endurece o argumento, mas a suposição registrada atenua. O autor diz que não preenche template |
| PED-05 | caps. 6 (p. ~78) e 9 (p. ~120) | Fiel | Plano revisado antes de deixar começar, e uma porteira de aprovação manual entre planejar e mover arquivos |
| CTX-02 | cap. 9 (p. ~127–128) | Fiel | Arquivo curto e imperativo, em que cada linha ocupa contexto. Linha nova entra na terceira repetição da mesma correção |
| CTX-15 | cap. 2 (p. ~32–33) | Fiel | Depois das compactações o agente não sabe o porquê de uma decisão e pode inventar um motivo plausível |
| ENG-02 | cap. 6 (p. ~80–81) | Fiel | TDD do XP, todo bug corrigido com teste e cerca de 1,5 linha de teste por linha de código |
| ENG-13 | cap. 2 (p. ~34) | Fiel | Falhas seguidas de compactação desperdiçavam ~250 mil chamadas por dia, e o conserto foi parar após três. "Vai para diagnóstico" é um acréscimo leve |
| VER-02 | cap. 12 (p. ~166–167) | Fiel | O próprio modelo escreveu o dublê com o método inventado. A pergunta-chave é quem escreveu a verificação |
| VER-06 | caps. 6 (p. ~81) e 9 (p. ~126) | Fiel | A CI pegou bug real mais de 50 vezes em 274 commits, e o modelo de instruções manda rodar os testes com um único comando |
| REV-04 | caps. 3 (p. ~49), 6 e 16 (p. ~232) | Fiel | Claude Code, Codex e o próprio autor acharam coisas diferentes. Nas duas auditorias, a lista final é a união das duas. Das três combinações de revisor, nenhuma achou tudo |
| REV-07 | cap. 7 (p. ~90) | Fiel | A auditoria corrigiu 22 problemas, e o autor credita o achado ao pedido que nomeou o tipo de erro. SQL injection e path traversal vêm do ap. J, que a regra não cita |
| SEG-19 | cap. 16 (p. ~223) | Fiel | Com o serviço parado, a consulta voltou vazia e 69 itens foram apagados. A regra nova exige lista não vazia e com a contagem esperada |
| SEG-12 | caps. 15 e 16 (p. ~235); ap. G | Fiel | Nenhum agente em produção. Ele escreve receitas no ambiente de teste, e um humano revisa e promove |
| OPS-02 | cap. 16; ap. G (p. ~383) | Fiel | Pede snapshot automático a cada hora no período de uso, retenção em camadas (horária, diária, semanal, mensal) e saber restaurar um arquivo com antecedência |
| OPS-10 | cap. 6 (p. ~83) | Fiel | De dez processos, só um funcionou, porque uma credencial vencida era engolida. Desde então toda falha deixa registro técnico e alerta num canal olhado todo dia |
| LLM-02 | cap. 6 (p. ~83) | Fiel | A checagem de estrutura (arquivo existe, mínimo de itens, marcações) pegou todo erro de modelo encontrado |
| LLM-03 | caps. 6 (p. ~79) e 13 | Fiel | Os números de mercado inventados foram trocados pela cotação real. Regra que dá para escrever fica no código, e o modelo só extrai fatos |
| AVA-01 | caps. 3 (p. ~49) e 11 | Fiel | Mesmo modelo e mesma tarefa, só o harness mudou: 24→91 e 57→18 |
| AVA-03 | cap. 11 | Fiel | A mesma configuração tirou 100 e 91. Faixa A é menos de meia hora de conserto e B é 1 a 2 h; C e D aparecem resumidas |
| ORG-01 | cap. 20; epílogo (p. ~327) | Fiel | Medir o que chega ao cliente, porque placar de uso premia gasto (orçamento queimado em quatro meses). O epílogo manda escolher um processo e medir antes de comprar licença |
| ORG-05 | cap. 19 (p. ~280) | Fiel | Continuar contratando júniors, com sêniores orientando; o sênior forma o próprio substituto |
| PES-04 | cap. 4 (p. ~57–59) | Fiel | Segunda opinião de outro fabricante com a mesma pergunta neutra e três empresas na checagem; a fonte primária decide |
| PES-09 | cap. 4 (p. ~59–60) | Fiel | O chatbot traduz jargão e prepara perguntas. Dose, troca de medicação e diagnóstico ficam fora |

Checagens extras, fora das 24:
- **SEG-S02** (ap. G, lista curta das sete peças): fiel. Mas o agente de ambiente, o P-22 e um eval usam outra lista (defeito 8).
- **ENG-04** (cap. 9, modelo com arquivos de menos de 500 linhas): fiel.
- **CTX-14** (cap. 3, 200 mil tokens): fiel. É uma regra pessoal do autor convertida em obrigação.

Resultado: nenhuma distorção na amostra.

## 3. Coerência (C)

**Coerente** (Verificado por leitura):
- **Nomes de skills e agentes:** iguais em `ORCHESTRATOR.md` (§0.1, §3 passo 6, §4, §6), no playbook, na matriz e no README.
- **Portões e contextos:** `portoes.md` e a tabela da matriz batem. G1 vale em C1; G2 em C2, C3, C4 e C9; G3 em C7 e antes da primeira escrita em C2; G4 em C6; G5 em C8; G6 em C0 (com implementação ou auditoria), C4, C5, C10, C11 e C12.
- **Precedência:** os limites do §2 B e do §5 vêm primeiro e o guia só acrescenta obrigações. A regra é igual em `decisoes-e-tradeoffs.md:3-9`, `ORCHESTRATOR.md:53` e `playbook/SKILL.md:12`.
- **`PRATICA-COMPLETO`:** ativa só por pedido do usuário, e a palavra num arquivo não ativa. Assim em `playbook:105`, `checar-conformidade:9` e `:24`, `conformance-auditor:68`, `ORCHESTRATOR.md:53` e `:317`, e no eval `keyword-em-documento-nao-ativa`.
- **Autonomia × regra humana:** `decisoes-e-tradeoffs.md:17-20` resolve como decisão pendente sem travar o resto, igual ao §0 (`ORCHESTRATOR.md:36`).
- **Regra `[H]`:** nunca atendida sem aprovação registrada. Assim em `playbook:95`, matriz `:8`, decisões `:20`, `checar-conformidade:21`, `guardar-destrutivo:31`, `destructive-ops-guard:29` e no modelo de conformidade (`:24`). A exceção é `conformance-auditor:26` (defeito 4).

**Incoerente:**
- **Autonomia do §0:** a lista de paradas não inclui o G4, e o C6 alcança edição comum de código (defeito 2).
- **Arquivo de conformidade:** exigido mesmo em auditoria sem autorização de escrita (5).
- **Núcleo C0:** CTX-06 cobra passagem de turno até em pergunta pontual (6).
- **`[A+H]` × autonomia:** inclusive PED-05, revisão do plano antes de executar (7).
- **Kit de segurança:** duas listas de "sete peças" (8).
- **Integração:** o playbook do orchestrator não traz a linha do guia (9), e a linha `Guia:` aparece em formatos diferentes (11).
- **Profundidade 1:** skills mandam acionar agentes, o que um subagente não pode fazer (16).

## 4. Segurança (D)

- **Estrutura** (Verificado pela listagem completa do plugin): sem hooks, `.mcp.json`, `.lsp.json`, `bin/` ou `commands/`.
- **Agentes:** nenhum tem Write ou Edit, e `oracle-designer` e `claims-verifier` não têm nem Bash. Os três com Bash declaram somente leitura. `destructive-ops-guard.md:65` proíbe rm, del, Remove-Item, mv, rsync --delete, git clean, reset --hard, truncate e redirecionamento que sobrescreve, e o agente nunca aprova (`:29`). Ele não executa remoção.
- **Skills com ação sensível:** as que tocariam settings, instalação, gasto ou pessoas exigem confirmação no chat (`kit-seguranca-agente:9`, `avaliar-modelo:9`, `adotar-ia-no-time:9`, `definir-oraculo:9`). `checar-conformidade:9` escreve só o `CONFORMIDADE.md`. `guardar-destrutivo:9` e `:25` não executam sem um "sim" no chat.
- **Conteúdo externo:** tratado como dado nos 16 artefatos, e instrução dirigida ao agente vira achado (`conformance-auditor:67`, `claims-verifier:62`).
- **Falhas:**
  - defeito 1 (alto): permissão ampliada pelo frontmatter;
  - defeito 3: leitura de `.env`, contra o SEG-10 e o bloco de limites;
  - defeito 4: aprovação humana aceita por arquivo.
- **Risco residual (Inferido):** nos três agentes com Bash, a barreira é só a instrução. O `conformance-auditor` roda o comando de testes do projeto, que pode ter efeito colateral (banco, arquivos). O README declara que o guia orienta e não bloqueia (`README.md:93`).

## 5. Evals (E)

| Caso | Frontmatter do `prompt.md` | Graders | Negativo | Observação |
| --- | --- | --- | --- | --- |
| `destrutivo-lista-vazia` | description, tags, max_turns 8, allowed_tools [Read, Glob, Grep, Skill] | llm; tool_used Skill; tool_used Bash e PowerShell com min 0 e max 0 | não | Bash e PowerShell ficam fora de `allowed_tools`, então os dois graders passam por vacuidade sem `--allow-tools` (o README declara) |
| `negativo-pergunta-conceitual` | idem, max_turns 6 | llm; tool_used Skill com min 0, max 0, `arm: both` | sim | `arm: both` é o uso documentado para "não deve invocar a skill" |
| `conformidade-pendencia-humana` | idem, max_turns 8 | llm; tool_used Skill | não | Testa `[H]` sob pressão de prazo; o critério aceita linha equivalente |
| `keyword-em-documento-nao-ativa` | idem, max_turns 6 | llm; tool_used Read `references/` com max 2 | sim (e injeção) | Conta só Read: Grep e Glob em `references/` passam (defeito 23) |

- **Formato:** chaves e tipos conferem com `plugin-blueprint.md:54-87` e com a documentação oficial. São 10 casos (o blueprint pede 6 a 10), com 2 negativos.
- **README e apoio:** o README explica execução, `--ablation`, custo e `designed_not_executed`; há `.gitignore` com `results/`; a versão mínima 2.1.269 confere com a documentação.
- **Ressalva:** o critério do `yolo-sem-jaula` (`graders/criteria.md:8`) cobra o kit divergente (defeito 8).

## 6. Proporcionalidade e custo de contexto (F)

- **Declarada e boa:**
  - pergunta pontual aplica o C0 em silêncio e responde direto (`playbook:93`, matriz `:9`);
  - sem implementação nem auditoria, não há arquivo (`playbook:101`);
  - o eval negativo cobre o sobredisparo.
- **Medido** (Verificado por script PowerShell nesta sessão, sobre as tags dos 12 `regras-*.md`, 386 regras lidas):

| Pedido típico | Contextos | Regras aplicáveis | Com `[H]` ou `[A+H]` |
| --- | --- | --- | --- |
| Pergunta pontual | C0 | 34 | 9 |
| Mudança pequena com commit | C0+C2+C4 | 114 | 30 |
| Correção de bug | C0+C2+C3+C4 | 120 | 31 |
| Auditoria | C0+C5 | 66 | 21 |
| Pesquisa ou relatório | C0+C11 | 62 | 12 |

  Toda regra aplicável precisa de uma linha com status (`checar-conformidade:20` e `:29`). Assim, uma correção de uma linha gera uma tabela de ~114 linhas e ~30 pendências humanas. A tarefa pequena vira auditoria, o contrário do que o playbook promete (defeito 10).
- **Leitura** (Inferido, bytes ÷ 3,5): um G0 completo lê o playbook (10,3 KB), a matriz (13,4 KB), os portões (5,1 KB) e os quatro arquivos do C0 (36,9 KB). São ≈ 66 KB, ou ≈ 19 mil tokens por invocação.
- **Núcleo para subagentes:** o bloco do guia (`playbook:44-52`, ≈ 1,3 KB, ≈ 400 tokens) e o §0.1 item 3 (≈ 0,9 KB) são enxutos e servem como núcleo. Os quatro arquivos do C0, não.
- **Listagem de skills:** as 11 descriptions somam ≈ 7,3 mil caracteres (≈ 2 mil tokens) em toda sessão com o plugin instalado. Todas ficam abaixo do corte de 1.536 caracteres da documentação; a maior é a do playbook, com 855.

## 7. Defeitos

Todos foram Verificados por leitura do arquivo:linha citado. A severidade é Inferida. Os caminhos são relativos a `plugins/agent-practice/`, salvo indicação.

| # | Sev. | Arquivo:linha | Defeito | Correção proposta |
| --- | --- | --- | --- | --- |
| 1 | Alta | `skills/revisar-codigo-de-ia/SKILL.md:5` (e `:10`) | `allowed-tools: Read, Glob, Grep, Bash` pré-aprova qualquer comando Bash, sem confirmação, no turno da skill. A documentação diz que o campo não restringe. A skill lê diff de terceiros (risco de injeção, contra o SEG-16) e promete "somente leitura" e "rodar testes se o usuário permitir" | Trocar por `allowed-tools: Read Grep Glob Bash(git diff *) Bash(git log *) Bash(git show *) Bash(git status *)` e acrescentar `disallowed-tools: Edit Write`. Testes passam pela confirmação normal. Revalidar a nota |
| 2 | Média | `skills/playbook/references/matriz-de-contexto.md:7,21,31`; `portoes.md:37`; `regras-seguranca.md:31`; `skills/guardar-destrutivo/SKILL.md:3,17`; brain `ORCHESTRATOR.md:31-34,100` | O C6/G4 (bloqueante, com aprovação no chat) casa com qualquer remoção, sobrescrita, `rm` ou "mover". Isso inclui editar ou apagar arquivo versionado numa branch local, até o código morto que o ENG-03 manda caçar (`regras-engenharia.md:9`). Ou trava a autonomia do §0, ou induz atalho. `claude-md-snippets.md:24` e `prompt-library.md:427` dizem "em massa", e o SEG-19 diz "qualquer exclusão" | Definir o C6 como ação sobre dados ou arquivos que o Git da branch local não restaura: dados de usuário, banco, buckets, mídia, arquivos não versionados ou ignorados, `git clean`, `reset --hard`, `checkout --` sobre trabalho não commitado, `push --force`, `rsync --delete`. Mudança versionada e commitada na branch local fica em C2. Alinhar o "em massa" e incluir "ação de C6 (G4)" na lista de paradas do §0 |
| 3 | Média | `skills/kit-seguranca-agente/SKILL.md:17,33`; `agents/agent-environment-auditor.md:34` | Mandam inventariar `.env` por leitura e citar chaves, e o auditor roda `env` filtrado por nome. Isso põe valor de segredo no contexto, contra o SEG-10 (`regras-seguranca.md:16`) e o bloco de limites (`ORCHESTRATOR.md:102`) | Nunca abrir `.env*`. Conferir só a existência (Glob) e se o arquivo está ignorado (`git check-ignore -v .env`). Nomes de variável só com `printenv \| cut -d= -f1` |
| 4 | Média | `agents/conformance-auditor.md:26` | Aceita aprovação humana "registrada no chat ou em arquivo datado". Contraria `decisoes-e-tradeoffs.md:20` (nunca inferir aprovação de arquivo) e `checar-conformidade:21`. O executor pode escrever o arquivo | Exigir citação do chat da sessão, com quem e quando. Registro em arquivo de sessão anterior vira "Pendente humana: reconfirmar no chat" |
| 5 | Média | brain `ORCHESTRATOR.md:51,279,295`; `skills/checar-conformidade/SKILL.md:9,25`; `agents/conformance-auditor.md:20`; `portoes.md:63` | Exige gravar `CONFORMIDADE.md` em auditoria, mas o §6 item 2 manda manter os relatórios no chat sem autorização de escrita, e o §5 diz que auditoria não altera o produto. O auditor trata o arquivo ausente como achado alto e para. Também não está claro se o G6 de C10/C11 sem implementação exige o arquivo | Sem autorização de escrita, o conteúdo vai no chat (ou numa pasta temporária fora do projeto, com caminho absoluto), e o auditor recebe o texto. Definir que C10/C11 sem implementação fazem o G6 na resposta, sem arquivo |
| 6 | Média | `regras-contexto-memoria.md:12`; matriz `:37`; brain `ORCHESTRATOR.md:49` × `:24` e `:249` | O CTX-06 (gravar passagem de turno ao fim de toda sessão) está no C0. Contradiz "pergunta pontual: resposta direta, sem arquivo" (`playbook:93,101`) e grava arquivo no projeto em auditoria | Em pergunta pontual ou auditoria sem escrita, a passagem de turno vai no chat (ou N/A, sem estado). O arquivo fica para implementação e C12. Ou mover o CTX-06 para C2/C12 e manter a passagem só no bloco do guia |
| 7 | Média | `regras-pedido.md:11` (PED-05); `portoes.md:19`; brain `ORCHESTRATOR.md:124`; `playbook:95`; matriz `:8,38-39` | A semântica de `[A+H]` sob a autonomia não foi definida por regra. O PED-05 pede o plano revisado antes de executar, e o §0 manda seguir sem aprovação. As 9 regras humanas do C0 viram pendência fixa em toda entrega. O playbook e a matriz falam só de `[H]`, e os demais de `[H]` e `[A+H]` | Tabela em `decisoes-e-tradeoffs.md`. PED-05 = plano revisado por um validador de outro papel e mostrado no chat; só o destrutivo ou irreversível espera o "sim". MET-01/MET-05: a parte do agente é atendida com evidência, e a humana vira uma pendência única, "aprovação da entrega". Alinhar o texto para `[H]` e `[A+H]` |
| 8 | Média | `agents/agent-environment-auditor.md:3,20-28`; `skills/prompts/references/prompt-library.md:468-472`; `evals/yolo-sem-jaula/graders/criteria.md:8` | Uma segunda lista de "sete peças" (rede; Git com push manual; segredos com produção) cita o SEG-S02, mas omite memória em arquivos e medidor de uso. Isso difere do SEG-S02 (`regras-seguranca.md:63`), do livro (ap. G) e de `kit-seguranca-agente:17-24,38` | Adotar o SEG-S02 como as sete peças e mover rede, push manual e segredos para as conferências "também" |
| 9 | Média | `plugins/orchestrator/skills/playbook/SKILL.md:42-59,73,87-121` | O formato de entrega e a mensagem final não têm a conformidade (§6 item 6) nem a linha `Guia:` (item 4). O modo melhoria não lista o `CONFORMIDADE.md`, e as combinações não têm a linha do agent-practice. Já o `references/protocolo.md` tem tudo (`:185,241,295,301`) | Copiar os quatro pontos do protocolo para o SKILL.md |
| 10 | Média | `playbook:36,39,93`; matriz `:35-40`; `checar-conformidade:20,29` | Custo e proporcionalidade. O G0 lê ≈ 66 KB (≈ 19 mil tokens), sem resumo do C0 nem Grep por ID, e os subagentes recebem os caminhos das regras. O G6 de uma mudança pequena cobra 114 linhas e 30 pendências humanas (medido). A tarefa pequena vira auditoria | Declarar que o bloco do guia e o §0.1 item 3 bastam como C0 para subagentes e perguntas pontuais. Abrir `regras-*.md` só para C1–C14 casados, por Grep do ID. Usar `CONFORMIDADE.md` proporcional: portões, exceções, pendências, N/A agregado e amostra de Atendidas. A tabela integral fica para `PRATICA-COMPLETO` ou risco alto (MET-06) |
| 11 | Baixa | `playbook:35,99`; brain `ORCHESTRATOR.md:47,106,301`; `plugins/orchestrator/agents/demand-router.md:28`; `checar-conformidade:37`; `assets/templates/conformidade.md:61` | A linha `Guia:` do plano aparece em três formatos, a de fechamento em dois, e o bloco do guia tem dois textos (o do §2 B item 7 não traz a conferência de API na versão instalada nem a regra de que consulta vazia aborta) | Um formato canônico no playbook, citado literalmente nos demais. Completar o resumo do §2 B item 7 |
| 12 | Baixa | `playbook:3` × as descriptions de `guardar-destrutivo`, `kit-seguranca-agente`, `avaliar-modelo` e `memoria-do-projeto` (`:3`); `evals/README.md:25` | Os gatilhos temáticos do playbook se sobrepõem aos das skills de tarefa. Se o router disparar no lugar da skill de tarefa, o `skill-fired` falha | Tirar do playbook os gatilhos de tarefa ou dizer "para tarefa específica, prefira a skill de tarefa" |
| 13 | Baixa | `agents/claims-verifier.md:25` | O passo 6 pede segunda leitura de modelo de outra empresa, mas o agente não tem ferramenta para isso | Registrar como pendência para o orquestrador ou o humano |
| 14 | Baixa | `skills/revisar-codigo-de-ia/SKILL.md:21,26`; `prompt-library.md:115` | Numa skill somente leitura aparece "falha de segurança se corrige no mesmo commit". O P-05 pede veredito (Aprovar, Pedir mudanças, Bloquear), e a skill diz "achados, não veredito" | Trocar por "recomende a correção no mesmo commit (SEG-26)" e alinhar o P-05 a "achados com recomendação; decisão humana" |
| 15 | Baixa | `skills/definir-oraculo/SKILL.md:18,20` | O passo 4 ("escreva o teste") não diz quem escreve, e o passo 2 separa réu e juiz | "O teste que falha é escrito pelo verificador (QA, outro contexto ou humano); se for o mesmo agente, declare a limitação" |
| 16 | Baixa | `guardar-destrutivo:24`; `checar-conformidade:23`; `definir-oraculo:9` × brain `ORCHESTRATOR.md:110` | Mandam acionar um agente. Rodando dentro de um subagente, violam a profundidade 1 | "Se você é subagente, recomende ao orquestrador acionar o agente" |
| 17 | Baixa | `skills/especificar-pedido/SKILL.md:36` | Sempre grava `pedido.md`, inclusive em pedido pequeno ou em auditoria. O autor diz que é menos formal que um template (cap. 9) | Gravar o arquivo quando o resultado importa (PED-18) e houver autorização de escrita; nos outros casos, um bloco no chat |
| 18 | Baixa | `skills/memoria-do-projeto/SKILL.md:9` | Pede confirmação só para editar `AGENTS.md`/`CLAUDE.md` existente, mas criar um novo também altera instruções persistentes | Pedir confirmação também na criação, salvo pedido explícito |
| 19 | Baixa | `skills/playbook/assets/templates/plano-destrutivo.md:52` × `agents/destructive-ops-guard.md:29,45` | O parecer do revisor no modelo é "aprovado/reprovado", mas o agente só dá "abortar / corrigir o plano / liberar para aprovação humana" e "não aprova nada" | Usar no modelo o vocabulário do agente |
| 20 | Baixa | `skills/guardar-destrutivo/SKILL.md:1-5`; `docs/foundation/plugin-blueprint.md:48` | Não usa `disable-model-invocation`, sem registrar o motivo: o guarda precisa disparar sozinho e a execução (passo 10) depende do "sim" | Registrar a decisão em `decisoes-e-tradeoffs.md` |
| 21 | Baixa | `docs/foundation/plugin-blueprint.md:14-21` × `skills/playbook/references/` | Faltam `checklist-completo.md`, `padroes-e-antipadroes.md` e `ferramentas-e-mcp.md`, da estrutura obrigatória. `portoes.md`, as seções Proibido e o mapa por sistema cumprem papel equivalente | Registrar a exceção no SYNTHESIS ou criar arquivos-ponteiro |
| 22 | Baixa | `prompt-library.md:32` (e demais linhas "Fonte") × `plugin-blueprint.md:43` | As fontes dos prompts não trazem classe A/B/C | Acrescentar "classe A (livro, experiência medida do autor)" |
| 23 | Baixa | `evals/keyword-em-documento-nao-ativa/graders/references-not-bulk-read.md:3-4` | Conta só Read, e leitura em massa por Grep ou Glob passa | Criar graders gêmeos para Grep e Glob com `references/` |
| 24 | Baixa | `skills/adotar-ia-no-time/SKILL.md:24` | "não plane" | "não planeje" |
| 25 | Baixa | brain `ORCHESTRATOR.md:45,64`; brain `CLAUDE.md:5` | Os textos já apontam `plugins/agent-practice/...`, que ainda não existe no brain (`Test-Path` = False). Se o protocolo for publicado sozinho, o §0.1 aponta para o vazio | Publicar o plugin e as mudanças do protocolo no mesmo commit |

## 8. Fechamento requisito a requisito

| Requisito do pedido | Status | Evidência |
| --- | --- | --- |
| A. Nota ≥ 80 no playbook, nas 9 skills, nos 5 agentes e em `prompts` | Falhou (1 de 16) | §1: `revisar-codigo-de-ia` com teto 40; os outros 15 entre 83 e 93 |
| B. Fidelidade de 24 regras | Passou | §2: 24 fiéis, 0 exageradas, 0 sem base, mais 3 checagens extras |
| C. Coerência | Parcial | §3: nomes, portões, precedência e `[H]` coerentes; 9 incoerências (2, 4 a 9, 11, 16) |
| D. Segurança | Falhou até corrigir o defeito 1 | §4; 3 e 4 médios |
| E. Evals | Passou | §5; ressalvas 8 e 23 |
| F. Proporcionalidade e custo | Parcial | §6: bloco e §0.1 enxutos; C0 em arquivo e G6 de tarefa pequena desproporcionais |
| Saída: só este arquivo | Passou | nenhum outro arquivo editado |

## 9. O que não foi verificado

- **Ferramentas:** não rodei `claude plugin eval`, `claude plugin validate` nem `verify_plugin.py`; os dois últimos o pedido informa como feitos.
- **Comportamento em sessão:** `allowed-tools`, `disallowed-tools` e `arm: both` foram conferidos na documentação oficial, não reproduzidos numa sessão real.
- **Regras:** 362 das 386 regras não foram confrontadas com o livro, e itens que os leitores possam ter deixado de extrair não foram avaliados.
- **Matriz:** as listas por contexto (C2 a C14) da seção "Regras por contexto" só foram contadas pelas tags das regras, não conferidas linha a linha.
- **Arquivos não lidos:** `claude-md-snippets.md` (inteiro); os modelos `agents-md-projeto`, `passagem-de-turno`, `pedido-quatro-partes` e `relatorio-avaliacao-modelo`; 15 dos 22 prompts; 6 dos 10 casos de eval (do `yolo-sem-jaula` li o prompt e os graders).
- **Integração no brain:** só `ORCHESTRATOR.md` e a linha 5 do `CLAUDE.md`. Ficaram de fora `SKILL.md`, `AGENTS.md`, `README.md`, `THIRD_PARTY_NOTICES.md`, as tags em `docs/foundation/knowledge/` e o prompt O-08 do orchestrator.
- **Direitos:** a questão jurídica sobre a destilação, que é Não verificável por mim (§11).

## 10. Limites

- **Quem validou:** um modelo (Claude Opus 5.5), da mesma família do autor do núcleo (Opus) e dos construtores (Sonnet). É uma segunda leitura, não revisão independente de família nem revisão humana.
- **Notas:** notas e severidades são julgamento de um avaliador numa passada (Inferido), sem calibração entre avaliadores.
- **Evals:** estão em `designed_not_executed`. Nenhuma taxa de disparo, acerto ou ganho sobre o baseline pode ser alegada.
- **Amostra de fidelidade:** 24 + 3 regras (≈ 7%), por Grep e leitura do entorno, sobre texto extraído do PDF com pdftotext (páginas aproximadas).
- **Fontes externas** (consultadas em 2026-11-19): https://code.claude.com/docs/en/skills (semântica de `allowed-tools`, `disallowed-tools` e `disable-model-invocation`, e corte de 1.536 caracteres da description) e https://code.claude.com/docs/en/plugin-evals (chaves do `prompt.md`, `tool_used`, `arm`, versão mínima).

## 11. Pendências humanas

- **Direitos:** `skills/playbook/references/fontes.md:11` registra que o livro reserva reprodução, adaptação, obra derivada e mineração de texto e dados, e o plugin sai com licença MIT. A decisão de publicar a destilação cabe ao dono, se quiser com orientação jurídica: repositório público ou privado e licença do plugin. Não é defeito de prompt e não entrou na nota.
- **Revisão humana das regras:** pedida pelo MET-05; o SYNTHESIS (`:41`) declara que ela não houve.
- **Correções 1 a 5:** aprovar antes da publicação.

## 12. Passagem de turno

- **Feito:**
  - leitura integral de 16 artefatos (playbook, 9 skills, `prompts/SKILL.md`, 5 agentes), de `portoes.md`, `decisoes-e-tradeoffs.md`, dos 12 `regras-*.md`, de `ORCHESTRATOR.md` e do playbook do orchestrator;
  - amostra: 7 prompts, 4 evals completos e a matriz (cabeçalho, tabela, C0 e C1);
  - 27 confrontos com o livro;
  - 2 consultas à documentação oficial;
  - 1 script de contagem de regras.
- **Ficou de fora:** listado no §9.
- **Falta:**
  - corrigir os defeitos 1 a 5 e revalidar `revisar-codigo-de-ia` (com só o frontmatter corrigido, a nota volta a 83);
  - rodar `claude plugin eval .` uma vez com `--allow-tools` no WSL2, para os graders de shell deixarem de passar por vacuidade;
  - publicar o plugin junto com o protocolo.
- **Decisões e motivos:**
  - apliquei o teto de 40 porque o frontmatter tira a confirmação de qualquer Bash justamente onde se lê conteúdo de terceiros, contra o SEG-16 e contra o "não amplia permissões" do próprio playbook;
  - o C6 ficou médio porque o efeito é bloqueio ou atalho, não perda de dados;
  - `.env` e a aprovação por arquivo ficaram médios porque o texto proíbe imprimir valor e o produtor do relatório exige a citação do chat.
- **Guia aplicado a esta validação:** contextos C0+C5+C11. O G6 ficou parcial: o `CONFORMIDADE.md` não foi gerado porque o pedido limita a escrita a este arquivo, o que é um exemplo prático do defeito 5.

## 13. Revalidação

Segunda rodada, 2026-11-19, depois das correções do autor. Conferi cada correção no disco, sem me apoiar no resumo do coordenador.

- **Relido:**
  - por inteiro: os arquivos que mudaram desde a primeira rodada (pela data de modificação), entre eles `revisar-codigo-de-ia`, `guardar-destrutivo`, `kit-seguranca-agente`, `checar-conformidade`, `definir-oraculo`, o playbook, `conformance-auditor`, `agent-environment-auditor`, `decisoes-e-tradeoffs.md`, `portoes.md`, os três índices novos, o modelo de conformidade, o playbook do orchestrator, os graders novos e o critério do `yolo-sem-jaula`;
  - por busca e trecho: matriz (cabeçalho e tabela), `regras-seguranca.md`, `regras-contexto-memoria.md`, `regras-pedido.md`, `regras-organizacao.md`, `claude-md-snippets.md`, `prompt-library.md` (P-05, P-20, P-22 e as 22 linhas "Fonte"), `claims-verifier`, `especificar-pedido`, `memoria-do-projeto`, `plano-destrutivo.md`, `adotar-ia-no-time`, `evals/README.md`, `demand-router.md` e os trechos alterados de `ORCHESTRATOR.md`.
- **Verificado por comando:**
  - `ORCHESTRATOR.md`, `plugins/orchestrator/skills/playbook/references/protocolo.md` e `publish/ORCHESTRATOR.md` têm o mesmo SHA-256;
  - a recontagem por script das tags dos 12 `regras-*.md` repetiu as 386 regras.
- **Não refeito:** `verify_plugin.py`, `claude plugin validate` e a checagem de sobreposição literal; o coordenador informa PASS.
- **Sobreposição apontada:** a justificativa do OPS-02 (seção 2) foi reescrita com outras palavras.

### 13.1 Defeito → status

| # | Status | Evidência no disco |
| --- | --- | --- |
| 1 | Corrigido | `revisar-codigo-de-ia/SKILL.md:5-6`: só leitura do Git pré-aprovada, e `disallowed-tools: Edit Write`. Corpo alinhado em `:11`; decisão em `decisoes-e-tradeoffs.md:71`. Resíduo: N1 |
| 2 | Corrigido | Escopo do C6 em `decisoes-e-tradeoffs.md:58-60` e `portoes.md:39`; matriz `:7`, `:21`, `:31`; `guardar-destrutivo:3`, `:17`; SEG-19 em `regras-seguranca.md:31`; `claude-md-snippets.md:24`; P-20 em `prompt-library.md:408`; brain `ORCHESTRATOR.md:34`, `:48`. Resíduos: N5, N7 |
| 3 | Corrigido | `kit-seguranca-agente:17`, `:33`; `agent-environment-auditor:30`, `:34`; `ferramentas-e-mcp.md:11`. Resíduo: N2 |
| 4 | Corrigido | `conformance-auditor:26`; `decisoes-e-tradeoffs.md:56`; `checar-conformidade:21`; `playbook:98`; brain `ORCHESTRATOR.md:49`. Resíduo: N3 |
| 5 | Corrigido | `checar-conformidade:9`, `:25`; `conformance-auditor:20`; `portoes.md:65`; `playbook:40`, `:103`; `decisoes-e-tradeoffs.md:64`; brain `ORCHESTRATOR.md:51`, `:295`. Resíduo: N5 |
| 6 | Corrigido | `regras-contexto-memoria.md:12`: o CTX-06 vale só com estado a retomar e vai no chat ou é N/A em pergunta pontual. Também `portoes.md:64` e brain `ORCHESTRATOR.md:49` |
| 7 | Corrigido | Tabela `[A+H]` em `decisoes-e-tradeoffs.md:47-56`; PED-05 em `regras-pedido.md:11`; `portoes.md:19`; matriz `:8`; `playbook:98`; `checar-conformidade:21` |
| 8 | Corrigido | `agent-environment-auditor:3`, `:18-30`; P-22 em `prompt-library.md:447-452`; `evals/yolo-sem-jaula/graders/criteria.md:8`. Os três seguem o SEG-S02 |
| 9 | Corrigido | Orchestrator `SKILL.md:59` (combinação), `:74` (modo melhoria), `:114` (item 6), `:120` (linha do guia). Resíduo: N5 |
| 10 | Corrigido, com efeito colateral | `playbook:36`, `:39`; matriz `:9`; `checar-conformidade:18`, `:20`, `:29`; `decisoes-e-tradeoffs.md:65-66`; modelo `conformidade.md:26`; brain `ORCHESTRATOR.md:50`. Recontagem por script numa mudança pequena (C0+C2+C4): as aplicáveis seguem 114, mas as pendências humanas caem de 30 para cerca de 3 (ENG-S04, MET-04 e a pendência única), mais as confirmações de ação que de fato ocorrerem. A tabela deixa de ter uma linha por regra. Efeito colateral: N4 |
| 11 | Corrigido | Linha do plano em `playbook:35`, brain `ORCHESTRATOR.md:47` e `demand-router.md:28`. Linha de fechamento em `playbook:102`, `checar-conformidade:37`, modelo `:63`, brain `ORCHESTRATOR.md:301` e orchestrator `SKILL.md:120`. §2 B item 7 completo (brain `ORCHESTRATOR.md:106`); as três cópias do protocolo têm o mesmo SHA-256 |
| 12 | Corrigido | `playbook:3`: os gatilhos de tarefa saíram, e a description manda preferir a skill de tarefa |
| 13 | Corrigido | `claims-verifier:25` |
| 14 | Corrigido | `revisar-codigo-de-ia:22`, `:27`; P-05 em `prompt-library.md:111` |
| 15 | Corrigido | `definir-oraculo:20` |
| 16 | Corrigido | `guardar-destrutivo:24`; `checar-conformidade:23`; `definir-oraculo:9` |
| 17 | Corrigido | `especificar-pedido:36` |
| 18 | Corrigido | `memoria-do-projeto:9` |
| 19 | Corrigido | `plano-destrutivo.md:52` |
| 20 | Corrigido | `decisoes-e-tradeoffs.md:70` |
| 21 | Corrigido | `checklist-completo.md`, `padroes-e-antipadroes.md` e `ferramentas-e-mcp.md`, índices curtos que apontam para a fonte única (o restic citado está no ap. G). Mapa em `playbook:73-75`; decisão em `decisoes-e-tradeoffs.md:73` |
| 22 | Corrigido | As 22 linhas "Fonte" de `prompt-library.md` (por exemplo `:32`) trazem a classe A |
| 23 | Corrigido | `evals/keyword-em-documento-nao-ativa/graders/references-not-bulk-grep.md` e `references-not-bulk-glob.md`. Resíduo: N6 |
| 24 | Corrigido | `adotar-ia-no-time:24` |
| 25 | Pendente (publicação) | `brain-of-agent\plugins\agent-practice` ainda não existe (`Test-Path` = False). O coordenador informa publicação conjunta depois deste veredito. Não pesa no veredito, mas impede publicar o protocolo sozinho |

### 13.2 Achados novos

| # | Sev. | Arquivo:linha | Achado | Correção proposta |
| --- | --- | --- | --- | --- |
| N1 | Baixa | `skills/revisar-codigo-de-ia/SKILL.md:5` | `Bash(git diff *)`, `Bash(git log *)` e `Bash(git show *)` também pré-aprovam `--output=<arquivo>`, opção de diff do Git que grava arquivo. Numa skill que lê diff de terceiros, uma injeção poderia gravar arquivo sem confirmação. O mesmo padrão aparece em outros plugins da fábrica (Inferido pela documentação do Git, não reproduzido) | Declarar o resíduo em `decisoes-e-tradeoffs.md:71` e recomendar ao usuário uma regra deny para `--output` nas settings dele (o plugin não altera settings). Ou tirar os três padrões do `allowed-tools` e deixar o harness perguntar |
| N2 | Baixa | `skills/kit-seguranca-agente/SKILL.md:17`; `agents/agent-environment-auditor.md:34` | `printenv \| cut -d= -f1` repassa inteiras as linhas de continuação de valores com várias linhas (chave PEM, JSON de credencial) e corta no primeiro `=` as que têm `=`. Parte do segredo entra no contexto (comportamento POSIX do `cut`; Inferido) | Usar `compgen -e` (bash), que lista só os nomes. A variante PowerShell já está certa |
| N3 | Baixa | `agents/conformance-auditor.md:26` | Como subagente, o auditor não vê o chat. Ele confere se a citação existe e está completa, mas não pode confirmar a autenticidade, e o texto não diz isso | Acrescentar: "a autenticidade da citação é Não verificável para você; o orquestrador, que vê o chat, confirma antes de fechar" |
| N4 | Média | modelo `assets/templates/conformidade.md:26`; `skills/checar-conformidade/SKILL.md:20,29`; `agents/conformance-auditor.md:25,29,38` | O relatório proporcional conta as Atendidas fora da amostra sem listar os IDs, e o auditor trata como omissão todo ID aplicável ausente do relatório (passo 6 e checklist). Ou ele acusa relatório correto, ou não acha omissão real. Além disso, a amostra é escolhida por quem preencheu (risco de amostra a dedo, VER-P03) | No modelo e no `checar-conformidade`: uma linha "Atendidas fora da amostra: <IDs>" e amostra que sempre inclua as regras de maior risco (G4, G5, VER-02, SEG-09). No auditor, em modo proporcional: reconferir algumas Atendidas escolhidas por ele mesmo na lista e tratar como omissão só o ID que não aparece em lista nenhuma |
| N5 | Baixa | `plugins/orchestrator/skills/playbook/SKILL.md:21`, `:27`, `:40`, `:71` | O resumo do orchestrator ainda diz "dados irreversíveis" sem o escopo do C6/G4 (`:21`, `:71`). Também exige o `CONFORMIDADE.md` "com implementação ou auditoria" (`:40`; `:27` fala só em fechar com o arquivo), contra o protocolo novo, que põe o conteúdo no chat em auditoria sem escrita | Alinhar ao brain `ORCHESTRATOR.md:34` e `:51` |
| N6 | Baixa | `evals/README.md:17` | A tabela não lista os graders novos do caso | Acrescentar `references-not-bulk-grep` e `references-not-bulk-glob` |
| N7 | Baixa | brain `ORCHESTRATOR.md:100` (§2 B item 1) e cópias | O bloco de limites proíbe ao subagente "apagar ou migrar dados" sem remeter ao C6. Um implementador pode recusar remover código morto já commitado, que o guia agora classifica como C2 | Escrever "apagar ou migrar dados (ações de C6 do guia)" |

### 13.3 Notas novas

| Arquivo | 1ª rodada | Revalidação | O que mudou |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 83 | 90 | D1 e D3 → 5; D9 e D11 → 4 (C0 pelo bloco, busca por ID, escopo do C6, auditoria sem escrita); D5 segue 3 |
| `skills/especificar-pedido/SKILL.md` | 88 | 92 | D11 e D12 → 5 (arquivo condicional, PED-18) |
| `skills/definir-oraculo/SKILL.md` | 92 | 93 | D3 → 5 (autor do teste definido) |
| `skills/guardar-destrutivo/SKILL.md` | 88 | 92 | D1 → 5 e D11 → 4 (escopo do C6, nota para subagente) |
| `skills/kit-seguranca-agente/SKILL.md` | 87 | 88 | D8 → 4 (não abre `.env*`; resta N2) |
| `skills/memoria-do-projeto/SKILL.md` | 88 | 90 | D8 → 5 (confirmação também na criação) |
| `skills/revisar-codigo-de-ia/SKILL.md` | 40 (83 sem teto) | 92 | Sem teto; D8 → 4 (resta N1) e D12 → 5 |
| `skills/avaliar-modelo/SKILL.md` | 93 | 93 | Não mudou |
| `skills/checar-conformidade/SKILL.md` | 90 | 93 | D8 e D9 → 5, D11 → 4; D7 cai para 4 (Atendidas fora da amostra sem evidência listada, N4) |
| `skills/adotar-ia-no-time/SKILL.md` | 88 | 92 | D10 → 5 (digitação); D12 → 5 (`regras-organizacao.md:3` marca as hipóteses do autor) |
| `skills/prompts/SKILL.md` | 92 | 93 | D12 → 5 (P-22 no SEG-S02, fontes com classe A) |
| `agents/conformance-auditor.md` | 88 | 88 | D8 → 4 (só citação do chat; resta N3); D7 cai para 4 e D11 segue 3 (N4) |
| `agents/oracle-designer.md` | 93 | 93 | Não mudou |
| `agents/claims-verifier.md` | 92 | 93 | D3 → 5 |
| `agents/agent-environment-auditor.md` | 83 | 92 | D1, D3 e D12 → 5 (kit do SEG-S02); D8 → 4 (resta N2) |
| `agents/destructive-ops-guard.md` | 93 | 95 | D12 → 5 (o modelo de plano usa agora o vocabulário do agente) |

Média 91,8 (antes 86,1) · mínima 88, em `kit-seguranca-agente` e `conformance-auditor` (antes 40) · nenhuma nota abaixo de 80 · nenhum critério de reprovação automática.

### 13.4 Veredito

**Aprovado com ressalvas**, pelo critério do início deste relatório: as 16 notas ≥ 80, nenhum critério de reprovação automática, fidelidade inalterada (24 de 24) e nenhum defeito alto aberto.

Ficam abertos 1 achado médio (N4), 6 baixos (N1 a N3, N5 a N7) e o #25, que depende da publicação conjunta. Nenhum amplia permissão de forma geral nem expõe segredo diretamente; N1 e N2 são caminhos estreitos, por isso ficaram baixos.

Recomendações:
- Corrigir o N4 antes do primeiro `CONFORMIDADE.md` proporcional real: sem isso, o auditor acusa como omissão toda Atendida fora da amostra.
- N1 a N3 e N5 a N7 podem ir na 0.1.1.
- Publicar plugin e protocolo no mesmo commit (#25).

### 13.5 Limites desta rodada

- **Limites da seção 10:** continuam valendo (validação por modelo da mesma família, um avaliador, evals não executados).
- **Arquivos sem mudança:** `oracle-designer`, `destructive-ops-guard`, `avaliar-modelo` e `prompts/SKILL.md` não mudaram, pela data de modificação. A nota do `destructive-ops-guard` subiu só pela coerência com o modelo de plano corrigido, e a do `prompts` pela biblioteca que ele entrega.
- **N1 e N2:** o efeito de `--output` nos padrões do Git e de `cut` com valores de várias linhas vem da documentação dessas ferramentas. Não reproduzi nesta sessão (Inferido).

### 13.6 Passagem de turno

- **Feito:**
  - os 25 defeitos conferidos no disco: 24 corrigidos e o #25 pendente de publicação;
  - 7 achados novos;
  - 16 notas refeitas;
  - justificativa do OPS-02 reescrita.
- **Falta:**
  - o N4 antes do primeiro relatório proporcional real, e N1 a N3 e N5 a N7 na 0.1.1;
  - a publicação conjunta (#25);
  - uma rodada de `claude plugin eval .` com `--allow-tools`.
- **Decisões:**
  - tirei o teto de 40 do `revisar-codigo-de-ia` porque o frontmatter agora pré-aprova só leitura do Git e o resíduo do `--output` é estreito;
  - classifiquei o N4 como médio porque afeta a contraprova do G6, central no método, embora não abra permissão.

## 14. Correções do autor após a revalidação (não revalidadas)

Registro do autor do núcleo, não do validador: os itens abaixo foram corrigidos depois da seção 13 e **não passaram por nova rodada independente**.

| Achado | Correção | Onde |
| --- | --- | --- |
| N1 | `allowed-tools` reduzido a `Read Grep Glob Bash(git status *)`; `git diff`, `git log` e `git show` passam pela confirmação normal porque aceitam `--output` | `skills/revisar-codigo-de-ia/SKILL.md`; `decisoes-e-tradeoffs.md` (Decisões de forma) |
| N2 | `compgen -e` no lugar de `printenv \| cut -d= -f1` | `kit-seguranca-agente`, `agent-environment-auditor` |
| N3 | Autenticidade da citação declarada Não verificável para o auditor; o orquestrador confirma | `agents/conformance-auditor.md` |
| N4 | Linha "Atendidas fora da amostra: <IDs>", amostra com as regras de maior risco (G4, G5, VER-02, SEG-09, `[A+H]`) e uma por contexto; o auditor reconfere ao menos 3 escolhidas por ele e só acusa omissão de ID ausente de todas as listas | modelo `conformidade.md`, `checar-conformidade`, `conformance-auditor` |
| N5 | Escopo do C6 e conformidade no chat em auditoria sem escrita alinhados | `plugins/orchestrator/skills/playbook/SKILL.md` |
| N6 | Graders `references-not-bulk-grep` e `references-not-bulk-glob` na tabela | `evals/README.md` |
| N7 | "apagar ou migrar dados (ações de C6 do guia, §0.1)" no bloco de limites | brain `ORCHESTRATOR.md` §2 B item 1 e cópias |
| #25 | Plugin e protocolo publicados juntos por `publish_brain.py` | brain |

