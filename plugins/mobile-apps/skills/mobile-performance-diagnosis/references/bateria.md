# Bateria e segundo plano

Verificado em 2026-10-10. Fontes: Android vitals, wake locks parciais excessivos (V-62, https://developer.android.com/blog/posts/raising-the-bar-on-battery-performance-excessive-partial-wake-locks-metric-is-now-out-of-beta, post de 2025-11-10); Doze e App Standby (V-63, https://developer.android.com/training/monitoring-device-state/doze-standby); energia no iOS (V-64, classe B, rebaixada). Redação própria. Limiares e datas mudam: reconfira as páginas antes de afirmar números ao usuário.

## Android vitals: wake locks parciais excessivos (V-62)

| Fato (Verificado na página) | Detalhe |
| --- | --- |
| Sessão excessiva | Mais de **2 horas acumuladas** de wake locks parciais não isentos em 24 h |
| Limiar cruzado | Quando **5%** das sessões dos últimos 28 dias são excessivas |
| Onde investigar | Wake locks com duração **P90 ou P99 acima de 60 minutos** |
| Isenção | Wake lock de sistema com benefício claro que não otimiza mais (reprodução de áudio, transferência iniciada pelo usuário) |
| Consequência | A partir de 2026-03-01 o título **pode** ser excluído de superfícies de descoberta e, em alguns casos, receber aviso na ficha da loja. São possibilidades; a aplicação atual não foi confirmada |

Checklist:

1. Abra Android vitals no Play Console (ação do usuário) e identifique as tags de wake lock com P90/P99 acima de 60 minutos.
2. Localize no código: `PowerManager.WakeLock`, `acquire(`, bibliotecas que adquirem wake lock em segundo plano (`Grep: "newWakeLock\|acquire\("`).
3. Troque por **WorkManager** para trabalho adiável (V-60) ou use APIs que o sistema isenta. Sempre `release()` em `finally` e prefira `acquire(timeout)`.
4. Remeça após a mudança, na mesma janela de comparação.

## Doze e App Standby (V-63)

O que a página oficial diz:

- Doze: aparelho parado, desconectado e com tela desligada; App Standby: apps sem uso recente. Ambos desde o Android 6.0.
- Em Doze: rede suspensa, wake locks ignorados, alarmes comuns adiados para a janela de manutenção, sem varredura Wi-Fi, sem sync adapters, sem JobScheduler. A página diz que o **WorkManager, que usa JobScheduler, também não roda**. `setAlarmClock()` ainda dispara.
- Recomendações: **FCM** para mensagens; **alta prioridade só para mensagens que geram notificação**; payload com dados suficientes para não precisar de rede; `setAndAllowWhileIdle()`/`setExactAndAllowWhileIdle()` (no máximo um alarme a cada nove minutos por app); pedir exclusão de otimização de bateria **só** se a função central do app for afetada (a política da Play proíbe o contrário).

Decisão rápida:

| Necessidade | Mecanismo |
| --- | --- |
| Trabalho adiável que sobrevive ao fechamento do app | WorkManager (espera a janela de manutenção em Doze; C5) |
| Mensagem que o usuário precisa ver já | FCM de alta prioridade que gere notificação |
| Horário exato visível ao usuário (despertador, agenda) | Alarmes (`setAlarmClock`; exatidão com `...AllowWhileIdle`); detalhes na doc de alarmes, **Inferido** |
| Função em tempo real longa (navegação, chamada) | Serviço em primeiro plano com notificação (política da Play, **Inferido**) |

### Testar Doze e Standby (somente em emulador, como referência)

Estes comandos alteram o estado do aparelho de teste; não rode em aparelho de uso pessoal (V-63).

```bash
adb shell dumpsys deviceidle force-idle      # entra em Doze
adb shell dumpsys deviceidle unforce         # sai
adb shell am set-inactive <pacote> true      # App Standby
adb shell am set-inactive <pacote> false
```

Pelo bash/PowerShell do usuário, via prompt de permissão normal; este plugin não executa `adb` sozinho.

## iOS (V-64, classe B)

O índice atual "Reducing your app's battery use" dá o processo: **fazer menos trabalho, trabalhar com mais eficiência, não abusar das APIs**. Atualizar estado com menos frequência; executar operações caras (como localização) só quando o usuário pedir; preferir frameworks de alto nível. Artigos de detalhe (CPU, rede e Bluetooth, localização, escrita em disco, análise de uso de bateria, Power Profiler, notificações de energia) **não foram lidos**.

Low Power Mode (página arquivada, 2016): reduz CPU/GPU e pausa atividade discricionária e de rede. O app deve reduzir animações, taxa de quadros, localização, sincronizações e backups. Observe a mudança de estado e consulte:

```swift
if ProcessInfo.processInfo.isLowPowerModeEnabled { /* reduzir trabalho */ }
// notificação: NSNotification.Name.NSProcessInfoPowerStateDidChange
```

A sintaxe Swift da página arquivada está obsoleta; use a forma acima (confirme no SDK). Medição com as ferramentas da Apple exige macOS.

Checklist "economia no iOS": reagir ao Low Power Mode; reduzir sincronização, animação e localização; retomar ao sair; medir antes de otimizar.

## Relatório

Use o formato de `relatorio-performance.md`: sintoma, causa suspeita, evidência, correção, validação. Para bateria, a evidência é a métrica do vitals (ou "Não verificável: sem acesso ao Play Console nesta sessão") e o procedimento de remedição.
