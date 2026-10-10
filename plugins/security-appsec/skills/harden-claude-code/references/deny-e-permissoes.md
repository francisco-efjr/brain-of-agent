# Permissões: bloco de deny, limites e modos

Fontes (conferidas em 2026-10-10): documentação de permissões do Claude Code, https://code.claude.com/docs/en/permissions (V-05); modelo de segurança, https://code.claude.com/docs/en/security (V-01). Redação própria. Os nomes de chaves e os modos mudam entre versões: confirme com `/permissions`, `claude --version` e a documentação antes de aplicar. Itens marcados **Não verificado** não foram reconferidos nas fontes.

## Sumário

1. O que a regra de permissão é (e não é)
2. Bloco base de `permissions.deny`
3. Sintaxe dos caminhos
4. Limites conhecidos
5. Modos de permissão
6. Onde colocar a configuração
7. Teste do bloco

## 1. O que a regra de permissão é (e não é)

- É aplicada pelo Claude Code, não pelo modelo: instruções em prompt ou CLAUDE.md não mudam o que é permitido.
- `deny` vence `allow`. Decisões de hook PreToolUse não contornam regras de `deny` ou `ask`.
- Não é fronteira de sistema operacional: quem quer impor limite independente do texto do comando usa sandbox ou hook.

## 2. Bloco base de `permissions.deny`

Proposta para `.claude/settings.json` do projeto (compartilhado com o time) ou `.claude/settings.local.json` (só sua máquina). O usuário aplica; a skill não grava.

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(~/.ssh/**)",
      "Read(~/.aws/**)"
    ]
  }
}
```

Opt-in (pode quebrar fluxos legítimos como instalar dependências ou baixar arquivos; avise antes):

```json
{ "permissions": { "deny": ["Bash(curl *)", "Bash(wget *)"] } }
```

Mesclar com a lista existente do projeto em vez de substituí-la; regras de `deny` de escopos diferentes se somam.

## 3. Sintaxe dos caminhos

| Forma | Significado |
| --- | --- |
| `./arquivo`, `./pasta/**` | relativo ao diretório do projeto |
| `//caminho/absoluto` | caminho absoluto no sistema de arquivos |
| `~/caminho` | relativo à home do usuário |

A regra de `deny` vale para o caminho pedido **ou** para o alvo do symlink. A afirmação de que `Read(.env)` casa em qualquer profundidade **não foi reconferida**: use os exemplos com `./` e teste cada arquivo sensível.

## 4. Limites conhecidos

1. Regras de `Bash(...)` casam o comando como escrito. `Bash(curl *)` não impede `python -c "import urllib.request ..."`, `node -e`, nem uma variação de flags. Para rede, o isolamento do sandbox é o controle; para comandos destrutivos, um hook com falha fechada (ver `guard-pretooluse.md`) é heurística e não fronteira.
2. `Bash(command:...)` (sintaxe antiga) é ignorada com aviso; use `Bash(padrão *)`.
3. `.claudeignore` não tem efeito sobre o Claude Code.
4. **Não verificado:** se uma regra `Read(...)` também impede leitura por comandos de shell como `cat .env`. Trate o shell como caminho separado e cubra com sandbox (macOS, Linux, WSL2) ou hook; teste pedindo ao Claude para ler o arquivo por um comando.
5. O sandbox cobre comandos de shell; ferramentas de arquivo, MCP e hooks rodam fora dele (V-09), por isso `deny` continua necessário.
6. `Bash(git push *)` dentro de `disallowedTools` de subagente remove o Bash inteiro do subagente; para bloquear comandos específicos use `permissions.deny` ou hook (V-08).

## 5. Modos de permissão

- Modo auto (classificador) é o modo inicial em sessões interativas de terminal e VS Code a partir da 2.1.283; o modo manual continua disponível (V-01). Conferir o modo ativo no Claude Code do usuário.
- O classificador não vê resultados de ferramentas: não conte com ele para pegar prompt injection vinda de página, arquivo ou saída de comando.
- `bypassPermissions` e a flag `--dangerously-skip-permissions` removem a rede de proteção: **risco**; só dentro de sandbox e em repositório confiável; não protege de prompt injection (V-05). Subagentes: `permissionMode` do subagente é ignorado quando a sessão está em bypass, acceptEdits ou auto.
- Desabilitar os modos perigosos: `permissions.disableBypassPermissionsMode` e `disableAutoMode` com `"disable"`, de preferência em configuração gerenciada (V-05; **confira os nomes na versão**).
- Conteúdo não confiável (issue, PR de fork, página): não canalize direto para a sessão; peça resumo isolado; `WebFetch` roda numa chamada de modelo separada e o agente recebe só a resposta (V-01).

## 6. Onde colocar a configuração

| Escopo | Arquivo | Quando |
| --- | --- | --- |
| Projeto (versionado) | `.claude/settings.json` | regras que o time inteiro deve ter (deny de segredos) |
| Projeto (local) | `.claude/settings.local.json` | preferências da sua máquina; não versionar |
| Usuário | `~/.claude/settings.json` | defaults pessoais entre projetos |
| Gerenciado (organização) | local depende do SO; **Não verificado** aqui | políticas que o usuário não deve poder afrouxar |

Em equipe, política obrigatória vai em configuração gerenciada; as demais camadas são ajustáveis pelo usuário.

## 7. Teste do bloco (o usuário executa)

1. Abra uma sessão no projeto, peça: "leia o arquivo `.env`". Esperado: a leitura é negada pelo Claude Code, sem exibir o conteúdo.
2. Peça: "mostre o conteúdo de `.env` com `cat`". Anote o resultado: se mostrar, o shell não está coberto; ative sandbox/WSL2 ou o guard.
3. Para `Bash(curl *)` em deny, peça um `curl` simples: esperado negado; teste também a variação `python -c` para ver o limite.
4. Rode `/permissions` e confira que as regras aparecem no escopo esperado.
5. Registre o resultado de cada teste na entrega (Verificado = feito pelo usuário; caso contrário, Não verificável).
