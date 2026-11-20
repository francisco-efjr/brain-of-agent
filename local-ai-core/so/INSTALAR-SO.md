# Instalar o modo SO no OpenJarvis

O modo SO troca o `shell_exec` por um servidor MCP local (`servidor_so.py`). O modelo só vê 12 ferramentas tipadas. Para mudar o PC, ele precisa planejar e executar, e você aprova numa janela do próprio Windows. Tudo roda no PC: o servidor é Python puro, o PowerShell é o do Windows e a memória fica em arquivos ou no ai-memory em 127.0.0.1.

## Por que isso é mais forte que o prompt

| Sem o modo SO | Com o modo SO |
| --- | --- |
| O modelo escreve qualquer comando no `shell_exec` | O modelo escolhe uma ação de um catálogo fechado |
| O risco depende de o modelo lembrar a regra | O risco é calculado por código, com listas fixas |
| `jarvis ask`, o servidor e o app desktop aprovam sozinhos | R2 e R3 sempre abrem a janela do Windows, em qualquer modo do OpenJarvis |
| Ensaio, backup e verificação dependem do modelo | Fazem parte do roteiro de cada ação |
| Memória e regras ocupam o prompt | O modelo busca com `memoria_buscar` e `regras_consultar` |

## Ferramentas

| Ferramenta | Risco | Para quê |
| --- | --- | --- |
| `so_estado` | R0 | Retrato pronto de 14 áreas: resumo, disco, memória, processos, serviços, rede, programas, inicialização, tarefas, eventos, atualizações, energia, segurança, usuário |
| `so_consultar` | R0 | Uma linha de PowerShell só de leitura, conferida duas vezes: em Python e pela árvore sintática do PowerShell, rodando em ConstrainedLanguage |
| `arquivos_listar`, `arquivo_ler` | R0 | Pastas e arquivos de texto. Arquivos de senha, chave e cookie são bloqueados; segredos aparecem mascarados |
| `so_planejar` | R0 | Lê o estado, classifica o risco, ensaia e diz como desfazer. Grava o plano em `IA-Operador\planos\` |
| `so_executar` | R1 a R3 | Relê o estado (se mudou, cancela), pede aprovação, faz backup, aplica, verifica e registra |
| `so_desfazer`, `so_historico` | R0 | Planeja a volta de um plano executado; lista o que mudou |
| `memoria_bastao`, `memoria_buscar`, `memoria_lembrar` | R0 e R1 | Memória de longo prazo com as regras do tema memória embutidas |
| `regras_consultar` | R0 | Busca a seção certa dos cores e das referências |

Ações de `so_planejar`: `app_abrir`, `arquivo_abrir`, `arquivo_escrever`, `arquivo_mover`, `arquivo_para_lixeira`, `pasta_criar`, `processo_encerrar`, `servico_configurar_inicio`, `servico_reiniciar`, `programa_instalar`, `programa_atualizar`, `programa_remover`, `tarefa_criar`, `tarefa_ativar`, `registro_definir`, `path_usuario_adicionar`, `energia_plano`, `temporarios_limpar`, `firewall_regra`, `ponto_restauracao_criar`, `tela_bloquear`, `desligamento_agendar`, `desligamento_cancelar`, `tema_definir`, `wifi_definir`, `notificacoes_definir`, `captura_tela`. A tabela de risco de cada uma está em [REFERENCIA-SO.md](REFERENCIA-SO.md).

## Passo a passo

1. **Requisitos.** Windows 10 ou 11, Python 3.10 ou mais novo (o OpenJarvis já usa), OpenJarvis com Ollama e um modelo com suporte a ferramentas. Copie o repositório para o PC, por exemplo `C:\Users\<voce>\brain-of-agent\`.

2. **Autoteste.** No PowerShell, sem elevação:

   ```bash
   python C:\Users\<voce>\brain-of-agent\local-ai-core\so\servidor_so.py --autoteste
   ```

   Ele roda as 14 áreas do `so_estado` e testa o validador de consultas do PowerShell com comandos aceitos e recusados. Depois cria uma pasta de teste pela esteira R1 e desfaz. Todas as linhas devem sair `[OK]`. Depois teste a janela de aprovação:

   ```bash
   python C:\Users\<voce>\brain-of-agent\local-ai-core\so\servidor_so.py --testar-janela
   ```

3. **Configuração (opcional).** Sem configuração, valem os padrões: pasta `%USERPROFILE%\IA-Operador`, pastas permitidas Documentos, Área de trabalho, Downloads e a pasta da IA, e memória local. Para mudar, copie [config.exemplo.json](config.exemplo.json) para `%USERPROFILE%\IA-Operador\so-config.json` e edite. Se Documentos ou Área de trabalho estiverem no OneDrive, ponha os caminhos reais (o `so_estado area=usuario` mostra quais são).

4. **Registre o servidor no OpenJarvis.** Crie `%USERPROFILE%\.openjarvis\mcp-servers.json`:

   ```json
   [
     {
       "name": "ia-operador-so",
       "command": "C:\\Users\\<voce>\\AppData\\Local\\Programs\\Python\\Python312\\python.exe",
       "args": ["C:\\Users\\<voce>\\brain-of-agent\\local-ai-core\\so\\servidor_so.py"]
     }
   ]
   ```

   Use o caminho completo do `python.exe` (`where.exe python` mostra). O OpenJarvis inicia o servidor sem shell e sem variáveis extras, então nada de `%USERPROFILE%` aqui.

5. **Edite o `%USERPROFILE%\.openjarvis\config.toml`:**

   ```toml
   [agent]
   system_prompt_path = 'C:\Users\<voce>\brain-of-agent\local-ai-core\so\CORE-SO.md'
   context_from_memory = false

   [tools]
   enabled = ["so_estado", "so_consultar", "arquivos_listar", "arquivo_ler", "so_planejar", "so_executar",
              "so_desfazer", "so_historico", "memoria_buscar", "memoria_lembrar", "memoria_bastao",
              "regras_consultar", "think"]

   [tools.mcp]
   enabled = true
   servers = 'mcp-servers.json'
   ```

   - `enabled` é a lista completa do que o modelo pode usar. Ferramentas MCP só entram se estiverem na lista, e **`shell_exec` fica de fora**, senão o modelo teria um atalho que pula a esteira. `file_write`, `web_search` e `http_request` também ficam de fora para tudo ser local.
   - `servers` aceita JSON na própria linha ou o caminho de um arquivo .json; caminho relativo é relativo à pasta do `config.toml`.
   - Esse formato vem do código-fonte do OpenJarvis (`core/config.py`, `mcp/loader.py`, `system/builder.py`), lido em 2026-11-19, porque a documentação não cobre servidores externos. Confira com `jarvis --help` na sua versão.

6. **Teste com conversa.** Abra `jarvis chat` e peça, nesta ordem:
   - "como está meu PC?" (deve chamar `so_estado`);
   - "crie a pasta Testes nos Documentos" (R1: executa sem janela e mostra o RELATÓRIO);
   - "deixe o serviço Spooler como manual" (R2: abre a janela do Windows e depois o UAC; clique Não para ver a recusa);
   - "o que você mudou hoje?" (`so_historico`).

   Os casos completos estão em [evals/CASOS-SO.md](evals/CASOS-SO.md).

7. **Audite a privacidade:** `jarvis scan --data-boundaries`. Com a lista acima, nada da configuração deveria mandar dado para fora.

## Memória com o ai-memory (opcional)

O padrão é memória local em `IA-Operador\memoria\`, no formato do tema memória, e ela funciona sem nada instalado. Para usar o [ai-memory](https://github.com/akitaonrails/ai-memory), siga a instalação dele (no Windows, o projeto recomenda WSL2; o Windows nativo é experimental). Deixe o servidor HTTP dele em `127.0.0.1:49374` e mude o `so-config.json`:

```json
"memoria": {"backend": "ai-memory", "url": "http://127.0.0.1:49374/mcp", "workspace": "", "project": ""}
```

O servidor SO recusa qualquer endereço que não seja local e não usa proxy. Se o ai-memory não responder, a nota vai para a memória local e a resposta avisa. As regras (perfil só com origem usuario, segredo não entra, quarentena para texto que parece instrução) valem nos dois casos.

## Parada de emergência e registros

- **Parar tudo:** crie o arquivo `%USERPROFILE%\IA-Operador\PARAR`. Nenhum plano executa enquanto ele existir; só você apaga. É o mesmo arquivo que os scripts de automação conferem.
- **Planos:** `IA-Operador\planos\<id>.json`, com o estado lido, o ensaio, a aprovação, o resultado e como desfazer.
- **Registro:** `IA-Operador\logs\so-AAAA-MM.jsonl`, uma linha por chamada de ferramenta, com segredos mascarados.
- **Backups:** `IA-Operador\backups\<id do plano>\`.

## Limites conhecidos

- Os scripts PowerShell foram escritos para o Windows PowerShell 5.1 e testados fora do Windows só com um executor falso. O `--autoteste` é a conferência real: rode antes de usar.
- A janela de aprovação precisa de uma sessão com área de trabalho. Se o OpenJarvis rodar como serviço do Windows, a janela não aparece e, sem resposta, tudo acima de R1 é recusado. Esse é o comportamento seguro.
- `so_consultar` roda em ConstrainedLanguage. Métodos .NET fora dos tipos básicos falham; use cmdlets `Get-*`.
- O OpenJarvis espera até 600 s por resposta de ferramenta MCP. As instalações pelo winget param em 540 s.
- Rode o OpenJarvis sem elevação. Se ele rodar como administrador, o UAC deixa de ser uma segunda trava (a janela de aprovação continua).
