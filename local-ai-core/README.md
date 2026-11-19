# local-ai-core: o núcleo da IA local

> **O que é.** As regras permanentes (o "core") da IA que roda localmente no PC pessoal do dono deste repositório, montada com OpenJarvis e Ollama. O core é carregado como prompt de sistema em toda execução e define como a IA pensa, decide e age.
>
> **O que não é.** Não é plugin e não é lido pelo `ORCHESTRATOR.md`. Nenhum arquivo fora desta pasta depende dela, exceto o teste `tests/test_local_ai_core.py`, que confere se o `CORE.md` está montado.

Versão 2.0, 2026-11-19. Temas: **Windows** (operar o PC) e **conhecimento** (pesquisar, citar fontes e manter a base local).

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
└── conhecimento/
    ├── CORE-CONHECIMENTO.md           # tema: pesquisa e conhecimento
    ├── REFERENCIA-CONHECIMENTO.md     # 18 seções: fontes, checagem, evidência, citação, base local, RAG
    ├── PESQUISA-CONHECIMENTO.md       # 57 fontes e validação da esteira para pesquisa
    └── evals/CASOS-CONHECIMENTO.md    # 14 casos de teste
```

## Como funciona

**Base mais temas.** A base vale para tudo: classes de risco, esteira, invariantes gerais, formatos e regras de parada. Cada tema aplica a base à sua área, com exemplos de risco, regras próprias e exemplos de conversa. Como o OpenJarvis aceita um só arquivo de prompt, o `montar_core.py` junta base e temas no `CORE.md`.

**Duas camadas por tema.** O core do tema é curto e vai no prompt. A referência do tema é longa, fica na memória e é buscada só quando a tarefa pede. Prompt curto e estável deixa o modelo local mais rápido e mais obediente.

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

   Para usar só alguns temas: `python local-ai-core/montar_core.py --temas conhecimento --saida <caminho>\CORE-pesquisa.md`. O script mostra o tamanho estimado em tokens.
3. No `%USERPROFILE%\.openjarvis\config.toml`, aponte o prompt de sistema para o `CORE.md`. Deixe `system_prompt` vazio ou comentado, porque o valor inline tem precedência sobre o arquivo:

   ```toml
   [agent]
   system_prompt_path = 'C:\Users\<voce>\brain-of-agent\local-ai-core\CORE.md'
   context_from_memory = false

   [tools]
   enabled = ["shell_exec", "file_read", "file_write", "web_search", "http_request", "retrieval", "think"]
   ```

   Aspas simples fazem do TOML uma string literal. Com `context_from_memory = false` e a ferramenta `retrieval`, a IA busca na memória só quando precisa; a busca automática soma até cerca de 2 mil tokens em toda pergunta. Os nomes das ferramentas vêm da documentação lida por resumo: confira na sua versão.
4. Indexe as referências e a base de conhecimento:

   ```bash
   jarvis memory index <caminho>\local-ai-core\windows\REFERENCIA-WINDOWS.md
   ```

   ```bash
   jarvis memory index <caminho>\local-ai-core\conhecimento\REFERENCIA-CONHECIMENTO.md
   ```

   Se a sua versão só aceitar pasta, copie as referências para uma pasta própria e indexe a pasta. As notas que a IA grava ficam em `%USERPROFILE%\IA-Operador\conhecimento\` e são reindexadas por ela.
5. Rode os casos de `windows/evals/` e `conhecimento/evals/` com `jarvis chat` antes de dar autonomia.

## O que o core não garante

O core é um pedido ao modelo, não uma trava. Segundo a documentação do OpenJarvis (lida por resumo em 2026-11-19):

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
- **Tamanho do prompt** (estimativa do script, 2026-11-19): base com os dois temas, cerca de 5.500 tokens; base com um tema, cerca de 3.700. Se o modelo ficar lento ou desobediente, monte só os temas do uso do dia.

## Como evoluir

- Mudança no core passa pela própria esteira: proposta, teste nos casos de eval, validação, versão nova, `python local-ai-core/montar_core.py`.
- Regra nova só depois de ver a mesma falha duas vezes, com motivo curto.
- Tema novo: crie `<tema>/CORE-<TEMA>.md`, `REFERENCIA-<TEMA>.md`, `PESQUISA-<TEMA>.md` e `evals/`, acrescente o tema em `TEMAS` no `montar_core.py` e remonte. O teste do CI acusa se o `CORE.md` não for remontado.
- Se o modelo pular regras, corte exemplos antes de cortar invariantes, e teste uma versão em inglês nos mesmos casos.
