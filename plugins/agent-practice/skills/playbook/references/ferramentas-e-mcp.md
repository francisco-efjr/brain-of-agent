# Ferramentas citadas — sem instalação nem MCP ativo

Este plugin não traz hooks, `.mcp.json` nem `bin/` e não instala nada. As ferramentas abaixo aparecem nas regras como exemplo da função; confira a versão e a documentação no dia (MET-07) e instale só com confirmação do usuário no chat.

| Função | Exemplos | Regras |
| --- | --- | --- |
| Jaula (sandbox) | Linux: bubblewrap; macOS: sandbox-exec (obsoleto, proteção parcial); Windows: agente dentro do WSL2; código hostil: VM descartável | SEG-01 a SEG-05, SEG-S03 |
| Snapshots | Linux: Btrfs com snapper ou Timeshift; macOS: APFS e Time Machine; Windows: fracos, então backup externo obrigatório | OPS-02, SEG-24 |
| Backup externo | Ferramenta incremental e criptografada (por exemplo, restic), com restauração testada | OPS-03 |
| Permissões | Três colunas nas configurações do agente (sem perguntar, perguntar, nunca) | SEG-06, SEG-07 |
| Segredos | Gerenciador de senhas; `.env` mascarado e nunca aberto pelo agente; `git check-ignore -v .env` | SEG-10 |
| Git antes do push | `git status`, `git diff --cached` e revisão dos commits pendentes | SEG-08, SEG-09 |
| Medidor de uso | Indicador de cota visível com alerta antes do teto | CUS-01 |
| Memória portável | Markdown versionado em Git; servidor de memória só quando compensa | CTX-11, CTX-S04 |
| Instalador por script | Conferir a soma de verificação publicada | SEG-14 |
