# REFERENCIA-AUTOMACAO: base sob demanda de automação de rotinas

Complemento do CORE-AUTOMACAO.md. Indexada na memória e consultada por seção. Versão 1.0, 2026-11-19. Fontes por ID (T-, S-, O-, G-, H-) em PESQUISA-AUTOMACAO.md. `H-01 V-04` é o item V-04 do arquivo H-01 da pesquisa validada da casa.

## 1. Vale a pena automatizar?

- O Google SRE chama de "toil" o trabalho manual, repetitivo, automatizável, tático, sem valor duradouro e que cresce junto com o serviço (S-01). É isso que se automatiza.
- Tarefa feita uma vez, que muda toda vez ou que exige julgamento a cada passo não é candidata: faça na mão.
- Fluxo fixo ou agente? Fluxo com passos previsíveis é mais barato e confiável que um agente decidindo a cada vez (H-02 V-08). Automação determinística não precisa de IA.

## 2. Quem executa: Agendador do Windows ou OpenJarvis

- **Agendador de Tarefas + PowerShell:** para tarefas determinísticas. Sem modelo carregado, sem custo de GPU, comportamento previsível.
- **Agenda do OpenJarvis:** para tarefas que precisam da IA (resumir notícias, classificar, escrever). A documentação mostra `jarvis init --preset scheduled-monitor`, que configura o agente operative com agendamento, e comandos `jarvis scheduler create`, `list` e `stop`, com expressão cron (O-01, O-02). As páginas trazem duas sintaxes diferentes para criar; confira com `jarvis scheduler --help`.
- **Resumo da manhã do OpenJarvis:** recurso próprio, configurado na seção `[digest]` com agenda cron e fuso, que junta dados dos serviços conectados e entrega em áudio (O-03).
- **Power Automate for desktop:** vem no Windows 11 para fluxos de interface gráfica; fluxos sem usuário presente exigem Windows Pro ou Enterprise e licença (T-07). Use só quando não houver comando ou API.

## 3. Criar a tarefa agendada (R2)

Script em `$W\scripts\auto-<nome>.ps1` (modelo na seção 4). Registro, mostrado no PLANO antes de rodar:

```powershell
$W = "$env:USERPROFILE\IA-Operador"
$acao = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$W\scripts\auto-<nome>.ps1`""
$gatilho = New-ScheduledTaskTrigger -Daily -At 08:00
$config = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 30) -MultipleInstances IgnoreNew -StartWhenAvailable
Register-ScheduledTask -TaskName 'IA-<nome>' -TaskPath '\IA-Operador\' -Action $acao -Trigger $gatilho -Settings $config -Description 'Ficha: IA-Operador\automacoes\<nome>.md'
```

- `ExecutionTimeLimit`: sem ele, o limite padrão é de três dias (T-01).
- `MultipleInstances IgnoreNew`: não inicia outra execução enquanto uma estiver rodando (T-02).
- `StartWhenAvailable`: roda assim que possível se o horário passou com o PC desligado (T-01; confira o comportamento na sua versão).
- Sem `-User` nem `-RunLevel Highest`, a tarefa roda na sua conta, só com você logado e sem elevação, e nenhuma senha é guardada. Rodar sem usuário logado ou como administrador é R3.
- Todas as tarefas da IA ficam na pasta `\IA-Operador\` do Agendador, com nome `IA-<nome>`, para listar e desligar em bloco: `Get-ScheduledTask -TaskPath '\IA-Operador\'`.

## 4. Modelo de script de automação

```powershell
# Automação <nome>. Ficha: IA-Operador\automacoes\<nome>.md
$ErrorActionPreference = 'Stop'
$W = "$env:USERPROFILE\IA-Operador"
$nome = '<nome>'
$estado = "$W\automacoes\estado"
New-Item -ItemType Directory -Force -Path $estado, "$W\logs" | Out-Null
$log = "$W\logs\auto-$nome-$(Get-Date -Format yyyyMMdd-HHmmss).log"
if (Test-Path "$W\automacoes\PARAR") { "Parada geral ativa; nada feito." | Out-File $log; exit 0 }
Start-Transcript -Path $log | Out-Null
$codigo = 0
try {
    $marca = "$estado\$nome-$(Get-Date -Format yyyyMMdd).ok"
    if (Test-Path $marca) { Write-Output 'Já executada hoje; nada a fazer.'; return }
    # Ações aprovadas na ficha, só R0 e R1. Qualquer outra coisa: registre como PENDENCIA e não faça.
    # ...
    New-Item -ItemType File -Force -Path $marca | Out-Null
    Remove-Item "$estado\$nome.falhas" -ErrorAction SilentlyContinue
    Write-Output 'RESULTADO: OK'
} catch {
    Write-Output "RESULTADO: ERRO $($_.Exception.Message)"
    $arquivo = "$estado\$nome.falhas"
    $falhas = [int](Get-Content $arquivo -ErrorAction SilentlyContinue) + 1
    Set-Content -Path $arquivo -Value $falhas
    if ($falhas -ge 3) {
        Disable-ScheduledTask -TaskName "IA-$nome" -TaskPath '\IA-Operador\' | Out-Null
        Write-Output 'Desativada após 3 falhas seguidas.'
    }
    $codigo = 1
} finally {
    Stop-Transcript | Out-Null
}
exit $codigo
```

Confira no primeiro uso que a tarefa consegue desativar a si mesma na sua conta; se não conseguir, o aviso de falha basta e o usuário desativa.

## 5. Idempotência

- Rodar de novo não pode duplicar efeito. A AWS faz isso com um identificador por pedido, de modo que repetir o mesmo pedido não cria registro novo (S-05).
- Na prática local: arquivo-marca por execução (`<nome>-<data>.ok`), conferir antes de copiar se o arquivo já está no destino, operações que convergem para um estado ("garantir que a pasta existe") em vez de passos cegos.
- Receptores de evento recebem duplicatas e fora de ordem: deduplique por identificador (H-02 V-18).

## 6. Tentativas, espera e disjuntor

- Repita só erro transitório (rede, arquivo em uso, serviço ocupado). Erro de configuração ou permissão não melhora com repetição (S-04).
- Espera exponencial com teto e um componente aleatório ("jitter"), para não bater sempre no mesmo instante; o próprio blog de arquitetura da AWS mostra que espera exponencial sem aleatoriedade é a pior variante (S-04, S-09).
- Teto de tentativas e prazo total (S-04).
- Disjuntor: depois de falhas seguidas, pare de tentar e falhe rápido até alguém olhar; evita desperdício e efeito em cascata (S-06). Falhas em cascata e repetições que viram tempestade são riscos de agente listados pela OWASP (G-01, ASI08) e pela casa (H-01 V-22).

```powershell
for ($tentativa = 1; $tentativa -le 3; $tentativa++) {
    try { <operação>; break }
    catch {
        if ($tentativa -eq 3) { throw }
        Start-Sleep -Seconds ([math]::Pow(2, $tentativa) + (Get-Random -Minimum 0 -Maximum 3))
    }
}
```

## 7. Execução sem ninguém para aprovar

- A OpenAI orienta a passar para um humano quando o agente excede limites de falha ou vai executar ação de alto risco, sensível ou irreversível (G-03). Sem humano presente, a ação espera.
- Automação que lê conteúdo não confiável (e-mail, web, arquivo baixado) é o cenário clássico de injeção. Pela regra de dois da Meta, ela não deve ter ao mesmo tempo acesso a dados sensíveis e poder de mudar o sistema ou se comunicar para fora (G-02; checklist por fluxo na casa, H-02 V-20).
- Pendência: o que precisaria de aprovação vira linha `PENDENCIA:` no log e item no resumo. Nunca "resolva" sozinho.
- Parada de emergência: arquivo `PARAR` (todas as automações) e `Disable-ScheduledTask` (uma). Sinais de agente fora do escopo pedem desligar primeiro e investigar depois (G-01, ASI10).

## 8. Observar e avisar

- Monitoramento responde "o que quebrou" (sintoma) e "por quê" (causa); avise pelo sintoma e deixe a causa no log (S-02, H-01 V-04).
- Aviso bom é urgente, importante, acionável e real; quem recebe aviso demais passa a ignorar todos (S-03, H-01 V-05).
- Silêncio também é falha: a técnica do "dead man's switch" avisa quando o sinal de sucesso não chega no horário esperado (S-07). Localmente, uma automação diária pode conferir `Get-ScheduledTaskInfo -TaskName 'IA-<nome>' -TaskPath '\IA-Operador\'` das outras e incluir no resumo as que não rodaram.
- Códigos do Agendador: `0x0` sucesso; `0x41301` a tarefa ainda está rodando; `0x8004131F` já havia outra instância em execução (T-03).
- Logs sem segredos: mascare tokens e dados pessoais antes de gravar (H-01 V-26).
- Notificação na tela: o módulo comunitário BurntToast cria notificações do Windows pelo PowerShell (`New-BurntToastNotification -Text '...'`); instalar é R2 (T-08). Sem módulo, o resumo vai para um arquivo na área de trabalho ou para a próxima conversa.

## 9. Energia e horário

- Tarefa com IA local ocupa GPU e memória: agende para quando o PC está ligado e ocioso.
- "Acordar o computador para executar esta tarefa" fica na aba Condições; `powercfg /waketimers` mostra o que vai acordar o PC, e no Modern Standby os timers se comportam diferente (T-05). Acordar o PC é decisão do usuário.
- Notebook na bateria: prefira condições que só rodem na tomada para tarefas pesadas.

## 10. Disparo por evento (pasta, arquivo)

- O `FileSystemWatcher` do .NET pode perder eventos quando o buffer estoura; a Microsoft recomenda filtrar (NotifyFilter, Filter, IncludeSubdirectories) em vez de só aumentar o buffer (T-06).
- Por isso, combine evento com uma conferência periódica que reconcilia o estado (por exemplo, a cada hora, processar o que ficou para trás).

## 11. Backups automáticos

- Regra 3-2-1, recomendada pela CISA: três cópias, em duas mídias diferentes, uma fora do lugar (S-08).
- Backup que nunca foi restaurado não é backup confiável: inclua um teste de restauração periódico na ficha.
- Automação de backup só copia; apagar cópias antigas é regra explícita na ficha, e mudar essa regra é R2.

## 12. Revisar e aposentar

- Toda ficha tem `revisar_em`. Na data, mostre: quantas vezes rodou, falhas, avisos gerados, e proponha manter, ajustar ou desligar.
- Automação que ninguém lê o resultado é ruído: proponha desligar.
- Mudança em automação segue a esteira e o PLANO, como mudança de sistema (H-01 V-17).
