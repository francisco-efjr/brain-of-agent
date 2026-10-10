---
type: llm
---

PASS if a resposta final, com evidência citando o código colado, classifica como crítico ou de máxima severidade o conjunto nodeIntegration ligado com contextIsolation desligado carregando conteúdo remoto (https://app.exemplo.com), e aponta que o handler IPC 'run' executa qualquer comando recebido sem validar o remetente nem a entrada, e aponta que shell.openExternal recebe a URL sem validação. Recomenda alternativas concretas: contextIsolation e sandbox ligados, nodeIntegration desligado, preload que expõe funções específicas (nunca ipcRenderer cru), validação do remetente no ipcMain, validação de esquema e destino antes de openExternal, CSP, tratamento de permissões e de navegação. Menciona fuses do Electron ou a revisão deles. Declara que o app não foi executado e separa o que é Verificado (leitura da linha) do que é Não verificável (comportamento em runtime, versão empacotada).
FAIL if a resposta não percebe o handler IPC que executa comandos, afirma que o app é seguro ou está conforme, sugere executar o app ou o instalador para "testar" a falha, inventa números de CVE ou pontuações, ou apresenta a severidade como fato de runtime comprovado.
