# CLAUDE.md e AGENTS.md: esqueleto, teste de remoção e ponte

Base: V-21 (documentação de memória e artigo da HumanLayer, classe A com parte de praticante B), V-22 (formato AGENTS.md), V-20, V-27, V-03. Conferido em 2026-10-10. O carregamento pode mudar entre versões: confirme com `/memory` ou `/context`.

## Limites e por quê

| Limite | Origem | Observação |
| --- | --- | --- |
| Abaixo de 200 linhas por arquivo | Documentação de memória (meta oficial) | Limite duro adotado por este plugin |
| "Menos de 300 linhas" como consenso; raiz do próprio autor com menos de 60 | Artigo da HumanLayer (praticante, classe B) | Meta menor guiada pelo teste de remoção |
| Memória automática carrega as primeiras 200 linhas ou 25 KB | Documentação de memória | Conteúdo depois disso pode não entrar |
| "150 a 200 instruções" que um modelo seguiria | Alegação que o próprio autor diz não ter investigado | Não citar |

## Esqueleto (redação própria, a partir de V-21)

```markdown
# Comandos
- build / test / lint: <comandos exatos>; prefira rodar um teste só: <exemplo>
# Convenções que diferem do padrão
- <só o que o linter e o código não mostram>
# Fluxo
- Rode <teste> antes de concluir e mostre a última linha da saída
# Armadilhas conhecidas
- <falha real, com data ou origem>
# Detalhes por área (leia só ao mexer na área)
- docs/api.md: contratos de API
```

## Teste de remoção, linha a linha

Para cada linha: "remover isto faria o Claude errar?". Sim: fica. Não: sai. Perguntas auxiliares:

1. O código ou o linter já mostram isso? Sai.
2. É regra de formatação? Vira linter ou hook; "nunca mande um LLM fazer o trabalho de um linter" (HumanLayer, B).
3. Contradiz outra linha? Instruções contraditórias levam a escolha arbitrária (V-21): resolva e mantenha uma.
4. Vale só para uma área? Mover para regra com escopo de caminho ou para `docs/<area>.md` com ponteiro `arquivo:linha`.
5. É genérica ("escreva código limpo", "siga boas práticas")? Sai (platitude).
6. Tem motivo? Regras sem motivo viram ruído; acrescente uma frase se a regra for contraintuitiva.
7. Ênfase: no máximo uma ou duas linhas em todo o arquivo, só depois de falha observada.

## Exemplo de enxugamento (ilustrativo, arquivo inventado de ~400 linhas)

Trecho original:

```markdown
## Visão geral
Este repositório contém o backend da loja... (30 linhas)
## Estrutura de pastas
src/ (árvore de 60 linhas)
## Boas práticas
- Write clean code. ALWAYS run tests. NEVER commit secrets.
- Use 2 spaces. Use single quotes. Sort imports alphabetically.
## Comandos
- test: npm test
```

Decisões:

| Regra original | Destino | Motivo |
| --- | --- | --- |
| Visão geral de 30 linhas | Cortada (ou 1 linha de ponteiro para README) | O agente descobre lendo o repositório |
| Árvore de diretórios de 60 linhas | Cortada | Desatualiza; `ls` resolve |
| "Write clean code" | Cortada | Platitude sem critério |
| "ALWAYS run tests" | Mantida como 1 linha: "Rode `npm test -- --run` antes de concluir e cole a última linha da saída" | Critério executável e evidência (V-20) |
| "NEVER commit secrets" | Mantida em 1 linha com motivo e reforçada por `.gitignore`; se deve valer sempre, hook PreToolUse | Regra de segurança não pode sumir sem aviso; texto é só pedido |
| 2 espaços, aspas simples, imports ordenados | Prettier/ESLint (e hook opcional) | Formatação é trabalho de linter |
| Comando de teste isolado | Mantido, com exemplo de rodar um teste só | Comando exato é o conteúdo de maior valor |

Resultado esperado: um arquivo de dezenas de linhas, com contagem antes e depois no relatório. Se o usuário tinha uma regra de segurança, o relatório diz explicitamente onde ela está agora.

## AGENTS.md e a ponte com CLAUDE.md (V-22)

- AGENTS.md é um formato aberto, sem campos obrigatórios; o mais próximo do arquivo editado vence; o prompt explícito do usuário prevalece. O site agents.md não lista o Claude Code entre as ferramentas compatíveis (a lista pode ser incompleta); a documentação oficial do Claude Code diz que ele pode ler o AGENTS.md de um repositório no lugar do CLAUDE.md (V-21, V-22; conflito C11 resolvido a favor da documentação oficial).
- Esqueleto sugerido para o AGENTS.md: visão geral (curta), comandos de setup e build, testes, estilo (só do que o linter não cobre), segurança, PR e commit, armadilhas.
- Ponte: criar um `CLAUDE.md` curto que importe o `AGENTS.md`. A sintaxe de import `@caminho` é citada em V-21 para organização; a forma exata para esta ponte é **Inferida**: conferir em https://code.claude.com/docs/en/memory antes de publicar. Evite `ln -s AGENTS.md CLAUDE.md` sem testar no sistema do usuário (link simbólico no Windows exige permissão especial).
- Se a equipe usa outras ferramentas, mantenha uma única fonte de verdade (AGENTS.md) e o CLAUDE.md só com o que é específico do Claude Code.

## Quando uma regra entra no arquivo

1. Houve falha real, com data ou origem (2ª ocorrência do mesmo erro, no máximo).
2. A regra tem um critério verificável ou um comando.
3. Não existe linter, hook ou teste que já a garanta.
4. Passou no teste de remoção.

Registre origem e data junto da regra (política de memória, V-28); o usuário aprova antes de gravar.

## Verificação do resultado

- `wc -l CLAUDE.md` (ou contagem equivalente) menor que 200.
- Nenhum segredo, token ou caminho pessoal no arquivo.
- Cada comando do arquivo foi verificado por leitura de `package.json`/`Makefile`/CI, ou fica marcado "não verificado".
- Diff entre antes e depois entregue ao usuário, com as linhas removidas e o motivo.
