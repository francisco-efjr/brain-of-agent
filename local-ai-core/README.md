# local-ai-core: o núcleo da IA local

> **O que é.** As regras permanentes (o "core") da IA que roda localmente no PC pessoal do dono deste repositório, montada com OpenJarvis e Ollama. O core é carregado como prompt de sistema em toda execução e define como a IA pensa, decide e age.
>
> **O que não é.** Não é plugin e não é lido pelo `ORCHESTRATOR.md`. Nenhum arquivo fora desta pasta depende dela, exceto os testes `tests/test_local_ai_core.py` (confere se o `CORE.md` está montado) e `tests/test_so_mcp.py` (servidor do modo SO).

Versão 3.2, 2026-11-19. Cinco temas e um modo de operação por ferramentas:

| Tema | Para quê | Fontes |
| --- | --- | --- |
| **Windows** | Operar o PC com PowerShell, com ensaio, backup e aprovação por risco | 98 |
| **Conhecimento** | Pesquisar, citar fontes, checar afirmações e manter a base local | 57 |
| **Memória** | Lembrar preferências, decisões, procedimentos e onde parou, com base no desenho do [ai-memory](https://github.com/akitaonrails/ai-memory) | 41 |
| **Programação** | Trabalhar nos projetos de código com branch, testes e evidência | 28, mais cerca de 196 itens validados da casa |
| **Automação** | Tarefas que rodam sozinhas, com ficha aprovada, limites e parada de emergência | 25, mais 63 itens validados da casa |
| **Modo SO** | A IA age só por um servidor MCP local que aplica as regras em código e pede aprovação numa janela do Windows | 27, mais a base dos temas |

## Dois modos

| | Modo prompt | Modo SO (recomendado para modelo fraco) |
| --- | --- | --- |
| Prompt | `CORE.md` (base e temas, de 3.300 a 9.600 tokens) | `so/CORE-SO.md` (curto) e 12 ferramentas, cerca de 4.500 tokens no total |
| Como age | `shell_exec` com qualquer comando | Catálogo fechado de 27 ações e leitura conferida |
| Quem aplica as regras | O modelo, se lembrar | O servidor, em código |
| Aprovação | "sim" no chat; fora do `jarvis chat` o OpenJarvis aprova sozinho | Janela do Windows em R2 e R3, em qualquer modo do OpenJarvis |
| Instalação | Passos abaixo | [so/INSTALAR-SO.md](so/INSTALAR-SO.md) |

Os dois usam as mesmas classes de risco e a mesma esteira. No modo SO, as regras dos temas viram código e ficam consultáveis por `regras_consultar`.

## Estrutura

```text
local-ai-core/
├── README.md                          # este arquivo
├── CORE.md                            # o prompt montado: é ele que vai no system_prompt_path (gerado)
├── CORE-BASE.md                       # base comum: risco, esteira, invariantes, formatos, parada
├── montar_core.py                     # junta a base e os temas no CORE.md
├── windows/
│   ├── CORE-WINDOWS.md                # tema: operar o Windows
│   ├── REFERENCIA-WINDOWS.md          # 26 áreas do Windows, buscadas sob demanda
│   ├── PESQUISA-WINDOWS.md            # 98 fontes e validação da esteira
│   └── evals/CASOS-WINDOWS.md         # 14 casos de teste
├── conhecimento/
│   ├── CORE-CONHECIMENTO.md           # tema: pesquisa e conhecimento
│   ├── REFERENCIA-CONHECIMENTO.md     # 18 seções: fontes, checagem, evidência, citação, base local, RAG
│   ├── PESQUISA-CONHECIMENTO.md       # 57 fontes e validação da esteira para pesquisa
│   └── evals/CASOS-CONHECIMENTO.md    # 14 casos de teste
├── memoria/
│   ├── CORE-MEMORIA.md                # tema: memória de longo prazo
│   ├── REFERENCIA-MEMORIA.md          # 17 seções: tipos, formato, envelhecimento, bastão, envenenamento
│   ├── PESQUISA-MEMORIA.md            # 41 fontes, princípios do ai-memory e validação da esteira
│   └── evals/CASOS-MEMORIA.md         # 12 casos de teste
├── programacao/
│   ├── CORE-PROGRAMACAO.md            # tema: programação no PC
│   ├── REFERENCIA-PROGRAMACAO.md      # 20 seções: bug, fatias, refatoração, testes, git, dependências, Windows
│   ├── PESQUISA-PROGRAMACAO.md        # 28 fontes diretas e a pesquisa validada da casa
│   └── evals/CASOS-PROGRAMACAO.md     # 12 casos de teste
├── automacao/
│   ├── CORE-AUTOMACAO.md              # tema: automação de rotinas
│   ├── REFERENCIA-AUTOMACAO.md        # 12 seções: Agendador, script modelo, idempotência, disjuntor, avisos
│   ├── PESQUISA-AUTOMACAO.md          # 25 fontes diretas e a pesquisa validada da casa
│   └── evals/CASOS-AUTOMACAO.md       # 12 casos de teste
└── so/
    ├── CORE-SO.md                     # prompt do modo SO: agir só por ferramentas
    ├── INSTALAR-SO.md                 # instalação no OpenJarvis, memória com ai-memory, parada de emergência
    ├── REFERENCIA-SO.md               # esteira nas ferramentas, risco por ação, respostas, decisões de projeto
    ├── PESQUISA-SO.md                 # 27 fontes: MCP, código do OpenJarvis e do ai-memory, Microsoft
    ├── evals/CASOS-SO.md              # 14 casos de teste
    ├── config.exemplo.json            # configuração opcional
    ├── servidor_so.py                 # o servidor MCP (stdio); --autoteste confere tudo no PC
    └── so_mcp/                        # política, catálogo de ações, planos, janelas, memória, regras, protocolo
```

## Como funciona

**Base mais temas.** A base vale para tudo: classes de risco, esteira, invariantes gerais, formatos e regras de parada. Cada tema aplica a base à sua área, com exemplos de risco, regras próprias e exemplos de conversa. Como o OpenJarvis aceita um só arquivo de prompt, o `montar_core.py` junta base e temas no `CORE.md`.

**Três camadas por tema.** O **cartão** (6 a 7 linhas) diz o que vale sempre e manda buscar o resto. O **core do tema** traz as regras completas. A **referência** é longa e só é buscada quando a tarefa pede. Prompt curto e estável deixa o modelo local mais rápido e mais obediente.

**Perfis.** Cada tema entra no `CORE.md` completo ou só como cartão:

| Perfil | Temas completos | Temas como cartão | Tamanho estimado |
| --- | --- | --- | --- |
| `padrao` (o `CORE.md`) | Windows, conhecimento | memória, programação, automação | cerca de 6.500 tokens |
| `dev` | Windows, programação | memória, conhecimento, automação | cerca de 6.000 tokens |
| `completo` | todos | nenhum | cerca de 9.600 tokens |
| `leve` | nenhum | todos | cerca de 3.300 tokens |

Para quem usa cartão, o core completo do tema precisa estar indexado na memória (passo 4 da instalação). Combinação própria: `--temas windows,memoria:cartao`.

**A esteira**, proposta pelo dono e validada pela pesquisa:

```text
0 Classificar risco → 1 Estruturar (e observar a realidade) → 2 Visão → 3 Testar a visão
→ 4 Validar a visão → 5 Conceber → 6 Produzir → 7 Testar de novo → 8 Validar o escopo
→ 9 Implementar → 10 Verificar e registrar
```

Os passos 1 a 9 são os nove originais; a pesquisa acrescentou o 0 (proporcionalidade) e o 10 (conferir o efeito real e registrar). No tema conhecimento, o mesmo fluxo vira: pergunta e base local, hipótese, busca exploratória, plano de busca, leitura com SIFT, checagem de cada afirmação, resposta com fontes e nota na base local.

**Classes de risco.** R0 leitura local; R1 efeito pequeno e reversível ou busca sem dado pessoal; R2 sistema, administrador, dado pessoal saindo, custo ou decisão importante; R3 destrutivo, reduz segurança, ou decisão de saúde, jurídica, financeira ou de segurança. Aprovação vale para ação com efeito ("sim" em R2, "CONFIRMO <ação>" em R3); pesquisa pura sobe o rigor da verificação, não pede aprovação.

## Instalar no OpenJarvis

1. Copie esta pasta para o PC, por exemplo `C:\Users\<voce>\brain-of-agent\local-ai-core\`.
2. Monte o prompt (precisa de Python 3.10 ou mais novo, que o OpenJarvis já usa):

   ```bash
   python local-ai-core/montar_core.py
   ```

   Outro perfil: `python local-ai-core/montar_core.py --perfil leve --saida <caminho>\CORE-leve.md`. Combinação própria: `--temas conhecimento,memoria:cartao`. O script mostra o tamanho estimado em tokens.
3. No `%USERPROFILE%\.openjarvis\config.toml`, aponte o prompt de sistema para o `CORE.md`. Deixe `system_prompt` vazio ou comentado, porque o valor inline tem precedência sobre o arquivo:

   ```toml
   [agent]
   system_prompt_path = 'C:\Users\<voce>\brain-of-agent\local-ai-core\CORE.md'
   context_from_memory = false

   [tools]
   enabled = ["shell_exec", "file_read", "file_write", "web_search", "http_request", "retrieval", "think"]
   ```

   Aspas simples fazem do TOML uma string literal. Com `context_from_memory = false` e a ferramenta `retrieval`, a IA busca na memória só quando precisa; a busca automática soma até cerca de 2 mil tokens em toda pergunta. Os nomes das ferramentas vêm da documentação lida por resumo: confira na sua versão.
4. Indexe na memória os cores e as referências de todos os temas (a IA busca neles quando um tema está como cartão ou quando precisa de detalhe). O jeito mais simples é copiar os arquivos `CORE-*.md` e `REFERENCIA-*.md` dos temas para uma pasta só e indexar a pasta:

   ```bash
   jarvis memory index <caminho>\local-ai-core-indice
   ```

   A IA grava em `%USERPROFILE%\IA-Operador\`: notas de pesquisa em `conhecimento\`, memória em `memoria\`, fichas de automação em `automacoes\`, além de `backups\`, `logs\` e `scripts\`. Ela mesma reindexa o que grava.
5. Rode os casos de `evals/` de cada tema com `jarvis chat` antes de dar autonomia.

## O que o core não garante

No modo prompt, o core é um pedido ao modelo, não uma trava. O modo SO resolve isso com ferramentas que aplicam as regras e pedem aprovação fora do modelo; veja [so/INSTALAR-SO.md](so/INSTALAR-SO.md). Segundo a documentação do OpenJarvis (lida por resumo em 2026-11-19):

- `enforce_tool_confirmation` é aceito, mas não é aplicado; `shell_exec` só pede confirmação no `jarvis chat` e aprova sozinho no `jarvis ask`, no servidor HTTP e no app desktop.
- `shell_exec` roda qualquer comando como o seu usuário, sem lista de permitidos e sem sandbox por padrão.
- `web_search` manda a consulta para provedores externos (You.com sem chave, DuckDuckGo como reserva, ou Tavily, Serply e Firecrawl com chave).

Travas reais, fora do modelo:

1. **Rode o OpenJarvis sem elevação**, de preferência numa conta padrão: tudo que exigir administrador cai no UAC.
2. **Use `jarvis chat`** quando quiser aprovar cada comando.
3. **Restrinja o `file_write`** com `allowed_dirs` (confira a seção na página System Access).
4. **Ligue a transcrição do PowerShell** para ter registro do que rodou.
5. **Audite a privacidade** com `jarvis scan --data-boundaries`, que lista o que a configuração deixa sair da máquina.

## Desempenho

Vem das páginas oficiais do Ollama; meça antes e depois.

- `ollama ps`: se a coluna PROCESSOR mostrar parte em CPU, modelo mais contexto não cabem na VRAM, a causa mais comum de lentidão.
- Contexto custa memória. Agentes pedem contexto grande, mas só vale se couber na VRAM.
- `OLLAMA_FLASH_ATTENTION=1` e `OLLAMA_KV_CACHE_TYPE=q8_0` usam cerca de metade da memória do cache, em geral sem perda perceptível.
- `OLLAMA_KEEP_ALIVE=-1` mantém o modelo carregado; `OLLAMA_NUM_PARALLEL=1` se a memória estiver no limite.
- No Windows, defina as variáveis em "Editar as variáveis de ambiente da sua conta" e reinicie o Ollama pela bandeja.
- **Prompt estável:** prefixo idêntico aproveita o cache. Não ponha nada dinâmico nos arquivos de core.
- **Tamanho do prompt:** veja a tabela de perfis acima. Se o modelo ficar lento ou desobediente, use o perfil `leve` ou uma combinação própria.

## Como evoluir

- Mudança no core passa pela própria esteira: proposta, teste nos casos de eval, validação, versão nova, `python local-ai-core/montar_core.py`.
- Regra nova só depois de ver a mesma falha duas vezes, com motivo curto.
- Tema novo: crie `<tema>/CORE-<TEMA>.md` (com o bloco de cartão entre `<!-- cartao:inicio -->` e `<!-- cartao:fim -->`), `REFERENCIA-<TEMA>.md`, `PESQUISA-<TEMA>.md` e `evals/`, acrescente o tema em `TEMAS` e nos `PERFIS` do `montar_core.py` e remonte. O teste do CI acusa cartão faltando e `CORE.md` desatualizado.
- Se o modelo pular regras, corte exemplos antes de cortar invariantes, e teste uma versão em inglês nos mesmos casos.
