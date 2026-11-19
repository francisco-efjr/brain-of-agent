# REFERENCIA-PROGRAMACAO: base sob demanda de programação no PC

Complemento do CORE-PROGRAMACAO.md. Indexada na memória e consultada por seção. Versão 1.0, 2026-11-19. Fontes por ID (H-, E-) em PESQUISA-PROGRAMACAO.md. Os IDs H- apontam para a pesquisa validada da casa (`docs/dev-segments/research/`), que reúne cerca de 196 itens aprovados com suas próprias fontes; `H-01 V-04` significa o item V-04 do arquivo H-01.

## 1. Entender o pedido e o projeto

- O pedido define o escopo; extras viram sugestão (H-01 V-10).
- Leia antes de afirmar: abra o arquivo antes de opinar sobre ele, investigue antes de propor (H-01 V-11).
- Instruções do projeto (README, AGENTS.md, CLAUDE.md, CONTRIBUTING) mandam sobre preferências gerais; descubra as convenções do código antes de mudar (H-01 V-32).
- Mapa do código em vez de ler tudo: arquivos, símbolos e quem chama quem, como o mapa de repositório do Aider (H-06).
- Explorar, planejar, implementar e commitar é o fluxo oficial do Claude Code; pule o plano quando o diff cabe numa frase (H-02 V-01, E-20).

## 2. Linha de base e branch

- `git status` antes de tudo. Alterações não commitadas param a edição: o usuário commita, guarda ou autoriza trabalhar num `git worktree` limpo.
- Anote a branch original. Crie `git switch -c ia/AAAA-MM-DD-<tema>`.
- Rode testes, build e lint antes de mudar e registre o que já falhava: falha antiga não é regressão sua, mas entra no relatório.
- Checkpoint do assistente não substitui git: commit é o ponto de volta (H-02 V-02).

## 3. Corrigir bug

Quatro fases e a regra dos três (H-01 V-04, H-01 V-05):
1. Reproduzir com o menor caso possível.
2. Isolar: hipótese única, testada com evidência; `git bisect` acha o commit que introduziu a regressão (H-02 V-21).
3. Corrigir com um teste que falha primeiro e passa depois (H-02 V-17).
4. Confirmar: o caso original, a suíte inteira e efeitos vizinhos.
Três correções falhas seguidas: pare e reveja a hipótese ou a arquitetura.

## 4. Funcionalidade em fatias

- Fatias verticais pequenas e completas, com o build verde entre elas (H-04 V-08).
- Critério de aceite antes do código; para o que é grande, uma especificação curta aprovada (H-04 V-04, V-05).
- Feature grande atrás de flag quando o projeto usa flags (H-04 V-26).
- Mudança pequena revisa melhor; refatoração e comportamento em mudanças separadas (H-01 V-18).

## 5. Refatorar com segurança

- Rede de segurança antes: testes de caracterização que fixam o comportamento atual (H-01 V-36).
- Parallel change (expandir, migrar, contrair) para mudar API ou dependência sem quebrar quem usa (H-01 V-37).
- Cerca de Chesterton: antes de apagar algo estranho, descubra por que está ali (H-04 V-21).
- Simplificar sem mudar comportamento é uma tarefa própria, com os testes verdes antes e depois (H-01 V-12).

## 6. Testes

- Teste o comportamento, não a implementação; pirâmide prática com mais testes de unidade e integração do que ponta a ponta (H-03 V-14, H-04 V-10).
- TDD com vermelho confirmado: o teste precisa falhar pelo motivo certo antes da correção (H-03 V-28, V-31).
- Nunca enfraqueça teste para passar; teste que custa mais do que protege é achado de relatório, não exclusão silenciosa (H-01 V-11, V-30).
- Teste intermitente: classifique e isole, não aumente retentativas para esconder (H-03 V-21, V-37).

## 7. Verificar antes de dizer pronto

- Evidência fresca, desta sessão: saída do comando de teste, do build e do lint (H-01 V-01, H-02 V-15, H-03 V-32).
- Leitura de código não é teste executado. Verde no CI não prova o fluxo se as asserções forem fracas (H-07).
- O que não pôde rodar (sem emulador, sem serviço externo) fica "Não verificado", com o motivo e o comando para o usuário.

## 8. Revisar o próprio diff

Antes de cada commit, `git diff --cached` e esta lista (adaptada do guia de revisão do Google e da casa, H-01 V-17, V-19, V-38):
- Faz o que o pedido pede e só isso?
- Tem teste para o comportamento novo ou corrigido?
- Nomes, complexidade e duplicação razoáveis?
- Segredo, token, `.env`, print de depuração, arquivo gerado ou de outra tarefa?
- Mudou fim de linha ou formatação do arquivo inteiro sem querer?
- Algum risco de segurança óbvio (entrada sem validação, SQL montado com texto, permissão aberta)?

## 9. Commits e mensagens

- Conventional Commits 1.0.0: `tipo(escopo): descrição` com `feat`, `fix`, `refactor`, `test`, `docs`, `chore`; `!` ou `BREAKING CHANGE:` para quebra (H-02 V-18).
- Um commit por mudança lógica; mensagem diz o quê e por quê (H-02 V-30).
- Nunca `--no-verify` para passar por hooks do projeto.
- Versão de release segue SemVer quando o projeto usa (H-02 V-31).

## 10. Git no dia a dia e como desfazer

- Desfazer algo já publicado: `git revert <commit>`, que cria um commit novo (H-02 V-24).
- Voltar um arquivo: `git restore --source <commit> <arquivo>` (E-21).
- Achou que perdeu algo: `git reflog` mostra onde a branch esteve.
- Histórico reescrito que precisa subir: `--force-with-lease` (com `--force-if-includes`), nunca `--force` puro, e só com CONFIRMO (H-02 V-19).
- Conflito de merge: entenda os dois lados antes de escolher; rode os testes depois (H-02 V-22).

## 11. Dependências e cadeia de suprimentos

- Modelos inventam nomes de pacote: num estudo publicado na USENIX Security 2025, cerca de 20% dos pacotes sugeridos não existiam, e nomes inventados se repetem, o que permite golpistas registrá-los (E-05). Medições de 2026 com modelos novos ainda acharam de 4,6% a 6,1% (E-06).
- Antes de propor: `npm view <pacote>` ou a página do PyPI, conferindo nome exato, editor, data e downloads.
- Com lockfile, `npm ci` instala exatamente o que está travado e falha se o `package.json` divergir (E-14).
- Python: um venv por projeto; nada de `pip install` global.
- Atualizar dependência é tarefa própria, com changelog lido e testes antes e depois (H-01 V-40).
- Licença da dependência compatível com o projeto.

## 12. Segredos

- Configuração que muda por ambiente vai em variáveis de ambiente, fora do código (E-15).
- `.env` no `.gitignore`; exemplo com nomes e sem valores (`.env.example`).
- Varredura de segredos antes do commit, se o projeto tiver (por exemplo, gitleaks como hook de pre-commit) (E-16).
- Segredo commitado: trate como comprometido, troque primeiro; depois limpe o histórico com `git filter-repo`, o que muda hashes, afeta PRs abertos e exige que outros clones também limpem (E-07). Limpar histórico é R3.

## 13. Windows: fim de linha

- `.gitattributes` na raiz manda sobre o `core.autocrlf` de cada pessoa; `* text=auto` é o padrão recomendado, com binários marcados (E-01).
- `text eol=crlf` para arquivos que precisam de CRLF (`.sln`, `.bat`); `text eol=lf` para scripts `.sh` (E-01).
- Diff com o arquivo inteiro alterado é sintoma de fim de linha. Não "conserte" mudando configuração global: investigue e, se for o caso, proponha `git add --renormalize .` num commit próprio.

## 14. Windows: caminhos longos

- O limite clássico é de 260 caracteres. Habilitar `LongPathsEnabled` no registro (HKLM) é R2 e o programa ainda precisa declarar suporte (E-02).
- O Git tem chave própria: `git config core.longpaths true` no repositório (R1) ou `--global` (R2) (E-03).
- Alternativa sem mexer em nada: clonar numa pasta de caminho curto (`C:\src\`).

## 15. Windows: Python e Node

- Python: instale com winget (`Python.Python.3.x`); o lançador `py` escolhe a versão (`py -3.12`, `py --list`) (E-11, E-12).
- venv: `py -m venv .venv`. Para não esbarrar na política de execução ao ativar, chame direto `.\.venv\Scripts\python.exe` e `.\.venv\Scripts\pip.exe`.
- Node: a Microsoft recomenda o nvm-windows para ter várias versões; respeite `.nvmrc` ou `engines` do projeto (E-13). Instalar o nvm-windows é R2.

## 16. Windows: shells, scripts e WSL

- Comandos do README em bash podem não funcionar no PowerShell: traduza (`export X=1` vira `$env:X = "1"`) ou rode no Git Bash ou no WSL.
- Scripts `.sh` com fim de linha CRLF quebram no bash: mantenha `eol=lf` para eles.
- Script PowerShell novo: verbos aprovados (`Get-Verb`), suporte a `-WhatIf` em quem altera algo, erros com `-ErrorAction Stop` (H-05 V-14, V-15).
- Projeto que roda ferramentas Linux fica no sistema de arquivos do WSL, não em `/mnt/c` (ver REFERENCIA-WINDOWS, seção 25).

## 17. Windows: desempenho de build

- Dev Drive é um volume ReFS otimizado para código; não dá para converter um volume existente e exige Windows 11 recente (E-04). Sugestão, não ação: criar volume é R2.
- O Defender pode deixar builds lentos. Criar exclusão de antivírus é R3 (ver CORE-WINDOWS); o Dev Drive tem um modo de desempenho do Defender próprio, que o usuário avalia (E-04).

## 18. Produção e dados reais

- Em 2025, o agente de uma plataforma de programação apagou o banco de produção de um usuário durante um congelamento de código e sem backup automático para voltar (E-10). Produção fica fora do alcance da IA local.
- Banco local de desenvolvimento, dados sintéticos e nenhuma credencial real no ambiente da IA.

## 19. Trabalho longo

- Sessões longas perdem contexto. Lista de tarefas com status fora do contexto (arquivo do projeto ou memória), progresso registrado e commits como pontos de volta (E-17, H-03 V-06, H-04 V-11).
- Ao parar, grave a passagem de bastão (CORE-MEMORIA).

## 20. Limites de agentes de código

- Num estudo controlado de 2025, desenvolvedores experientes levaram 19% mais tempo com IA, embora achassem que tinham sido 20% mais rápidos (E-09). Desconfie da sensação de velocidade; meça pelo resultado.
- Benchmarks de correção de issues têm testes mal especificados e foram depurados à mão (SWE-bench Verified, E-18). Passar no benchmark não prova competência no seu projeto.
- Pipelines simples (localizar, corrigir, validar com teste de reprodução) competem com agentes complexos (E-08). Simples primeiro.
- Mudanças pequenas são mais fáceis de recuperar quando falham (E-19).
