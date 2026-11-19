# local-ai-core: o núcleo da IA local

> **O que é.** As regras permanentes (o "core") da IA que roda localmente no PC pessoal do dono deste repositório, montada com OpenJarvis e Ollama. O core é carregado como prompt de sistema em toda execução e define como a IA pensa, decide e age.
>
> **O que não é.** Não é plugin, não é lido pelo `ORCHESTRATOR.md` e não participa da reestruturação do Brain of Agent. Nenhum outro arquivo do repositório depende desta pasta, e esta pasta não depende de nenhum outro.

Versão 1.0, 2026-11-19. Primeiro tema: controle do ecossistema Windows.

## Estrutura

```text
local-ai-core/
├── README.md                      # este arquivo
└── windows/
    ├── CORE-WINDOWS.md            # o prompt de sistema (vai no system_prompt_path)
    ├── REFERENCIA-WINDOWS.md      # base por área, indexada na memória e buscada sob demanda
    ├── PESQUISA-WINDOWS.md        # de onde veio cada regra: 98 fontes, validação da esteira
    └── evals/
        └── CASOS-WINDOWS.md       # 14 casos para testar se a IA obedece ao core
```

## Como funciona

**Duas camadas.** O core é curto e fixo: papel, prioridades, classes de risco, esteira, regras de execução no Windows, invariantes de segurança, formatos de plano e relatório. A referência é longa e fica fora do prompt: comandos, backups e armadilhas de 26 áreas do Windows, buscados só quando a tarefa pede. Prompt curto e estável deixa o modelo local mais rápido e mais obediente (ver PESQUISA, achado 9).

**A esteira**, proposta pelo dono e validada pela pesquisa:

```text
0 Classificar risco → 1 Estruturar (e observar o estado real) → 2 Visão → 3 Testar a visão
→ 4 Validar a visão → 5 Conceber → 6 Produzir → 7 Testar de novo → 8 Validar o escopo
→ 9 Implementar → 10 Verificar e registrar
```

Os passos 1 a 9 são os nove originais. A pesquisa acrescentou o 0 (proporcionalidade: pergunta simples não passa pela esteira inteira) e o 10 (conferir o efeito real e deixar o caminho de volta). Detalhes na seção 3 da [PESQUISA-WINDOWS.md](windows/PESQUISA-WINDOWS.md).

**Classes de risco.** R0 leitura (responde direto), R1 pequena e reversível (executa e mostra como desfazer), R2 sistema ou admin (plano, ensaio, backup, "sim"), R3 destrutiva ou que reduz segurança (tudo isso e "CONFIRMO <ação>").

## Instalar no OpenJarvis

1. Copie esta pasta para o PC, por exemplo `C:\Users\<voce>\brain-of-agent\local-ai-core\`.
2. No `%USERPROFILE%\.openjarvis\config.toml`, aponte o prompt de sistema para o core. Deixe `system_prompt` vazio ou comentado, porque o valor inline tem precedência sobre o arquivo:

   ```toml
   [agent]
   system_prompt_path = 'C:\Users\<voce>\brain-of-agent\local-ai-core\windows\CORE-WINDOWS.md'
   context_from_memory = false

   [tools]
   enabled = ["shell_exec", "file_read", "file_write", "retrieval", "think"]
   ```

   Aspas simples fazem do TOML uma string literal, então as barras invertidas valem como estão. `context_from_memory = false` com a ferramenta `retrieval` faz a IA buscar a referência só quando precisa; a busca automática (`true`) acrescenta até cerca de 2 mil tokens de trechos em toda pergunta, inclusive nas de leitura simples. Se a sua versão não tiver a ferramenta `retrieval`, use `true` e aceite o custo.
3. Indexe só a referência na memória: `jarvis memory index <caminho>\windows\REFERENCIA-WINDOWS.md`. Se a sua versão só aceitar pasta, copie o arquivo para uma pasta própria e indexe a pasta.
4. Rode os casos de [evals/CASOS-WINDOWS.md](windows/evals/CASOS-WINDOWS.md) com `jarvis chat` antes de dar autonomia.

Os nomes de chave acima vêm da documentação do OpenJarvis lida em 2026-11-19 (ver PESQUISA, L-11). Confira na versão instalada.

## O que o core não garante

O core é um pedido ao modelo, não uma trava. A documentação do OpenJarvis (lida por resumo em 2026-11-19) diz:

- `enforce_tool_confirmation` é aceito, mas não é aplicado.
- `shell_exec` só pede confirmação no `jarvis chat`. No `jarvis ask`, no servidor HTTP e no app desktop, aprova sozinho.
- `shell_exec` roda qualquer comando como o seu usuário, sem lista de permitidos e sem sandbox por padrão.

Por isso, as travas reais ficam fora do modelo:

1. **Rode o OpenJarvis sem elevação**, de preferência numa conta padrão. Tudo que exigir administrador cai no UAC, e só você aprova.
2. **Use `jarvis chat`** quando quiser aprovar cada comando.
3. **Restrinja o `file_write`** com `allowed_dirs` (confira a seção exata na página System Access da sua versão).
4. **Ligue a transcrição do PowerShell** para ter registro de tudo que rodou.

## Desempenho: por que pode estar lenta e o que ajuda

Tudo abaixo vem das páginas oficiais do Ollama (PESQUISA, L-01 e L-02). Meça antes e depois.

- **Veja se o modelo cabe na GPU:** `ollama ps`. Se a coluna PROCESSOR mostrar parte em CPU, o modelo mais o contexto não cabem na VRAM, e isso é a causa mais comum de lentidão. Saídas: modelo menor, quantização menor ou contexto menor.
- **Contexto custa memória.** O Ollama recomenda pelo menos 64 mil tokens para agentes, mas só vale se couber na VRAM.
- **Cache de atenção menor:** `OLLAMA_FLASH_ATTENTION=1` e `OLLAMA_KV_CACHE_TYPE=q8_0` usam cerca de metade da memória do cache, em geral sem perda perceptível.
- **Não recarregar o modelo:** `OLLAMA_KEEP_ALIVE=-1` o mantém carregado (o padrão descarrega após 5 minutos).
- **Paralelismo multiplica o contexto:** mantenha `OLLAMA_NUM_PARALLEL=1` se a memória estiver no limite.
- **No Windows,** defina essas variáveis em "Editar as variáveis de ambiente da sua conta", feche o Ollama pela bandeja do sistema e abra de novo.
- **Mantenha o core estável.** Prefixo idêntico entre chamadas aproveita o cache de prompt. Não coloque data, hora ou dados dinâmicos no core: o OpenJarvis já põe a hora depois do prefixo em cache.

## Como evoluir

- Mudança no core passa pela própria esteira: proposta, teste nos casos de eval, validação, versão nova.
- Regra nova só depois de ver a mesma falha duas vezes, com motivo curto. Regra para falha que nunca aconteceu só pesa no prompt.
- Se o modelo pular regras, corte exemplos antes de cortar invariantes, e teste uma versão em inglês nos mesmos casos (PESQUISA, seção 6).
- Quando entrar o segundo tema, extraia esteira, classes de risco e invariantes para um `CORE-BASE.md` comum e concatene com o core do tema.
