# Exemplo: N/A de app Android nativo e exploração por `adb`

Caso ilustrativo: um app Android em Kotlin com Compose, com backend HTTP, e um emulador já existente. Os comandos `adb` e as armadilhas vêm de X-21 (executados contra um AVD Pixel_10 com Android 17). Nomes de funcionalidade, textos de tela e `<serial>` são de exemplo.

## 1. Registro na matriz (N/A com executor)

| ID | Funcionalidade | Superfície | Playwright | Executor | Rótulo e motivo |
| --- | --- | --- | --- | --- | --- |
| F-15 | Adicionar item à lista de tarefas | app Android, tela Lista | Não | Compose UI test ou Espresso | N/A: UI nativa Android não é coberta pelo Playwright |
| F-16 | Sincronizar tarefas com o servidor | `/api/tarefas` | Sim | Playwright `request` | Backend do app (skill `api-and-network`) |
| F-17 | Abrir ajuda no WebView do app | WebView | Sim, **[EXPERIMENTAL]** | `_android` via ADB | Nunca único critério; requisitos: ADB autenticado, Chrome 105 ou superior, aparelho acordado |

Texto-padrão colado na linha F-15 e no relatório:

> UI nativa Android e iOS: não aplicável ao Playwright (a documentação cobre web, Electron e Chrome/WebView Android, de forma experimental; iOS só por emulação em WebKit desktop). Executor equivalente: Compose UI test ou Espresso. A matriz de funcionalidades é a mesma; só o executor muda.

A linha F-15 não é omitida e não é marcada `Passou` sem execução do executor equivalente.

## 2. Exploração por `adb` no emulador existente (sem instalar nada)

Regras: alvo existente (`-s <serial>`), dados sintéticos, nada de `adb uninstall` nem `pm clear`, sem instalar o app sem pedido do usuário. O rótulo da exploração por `adb` é Inferido até o S-13 fechar no ambiente da rodada.

Descobrir o serial:

```bash
adb devices
```

Abrir uma tela e conferir qual é a atividade em primeiro plano:

```bash
adb -s emulator-5554 shell am start -a android.settings.SETTINGS
adb -s emulator-5554 shell dumpsys activity activities
```

No resultado de `dumpsys`, procure `topResumedActivity` (no caso de X-21, `com.android.settings/.SubSettings`).

### Polling até o elemento aparecer (Git Bash)

```bash
export MSYS_NO_PATHCONV=1                      # sem isto, /sdcard/... vira caminho do Windows
SERIAL=emulator-5554
ESPERADO='<texto esperado na tela>'
achou=0
for i in $(seq 1 10); do
  adb -s "$SERIAL" shell uiautomator dump /sdcard/ui.xml >/dev/null 2>&1
  if adb -s "$SERIAL" exec-out cat /sdcard/ui.xml | grep -q "$ESPERADO"; then achou=1; break; fi
  sleep 1                                       # intervalo entre consultas; a condição é que manda
done
[ "$achou" = 1 ] && echo "elemento encontrado" || echo "Bloqueado: elemento não apareceu em 10 tentativas"
```

### Polling até o elemento aparecer (PowerShell 5.1)

```powershell
$serial = 'emulator-5554'
$esperado = '<texto esperado na tela>'
$achou = $false
foreach ($i in 1..10) {
  adb -s $serial shell uiautomator dump /sdcard/ui.xml | Out-Null
  $xml = (adb -s $serial exec-out cat /sdcard/ui.xml) -join "`n"
  if ($xml -match [regex]::Escape($esperado)) { $achou = $true; break }
  Start-Sleep -Milliseconds 800
}
if ($achou) { 'elemento encontrado' } else { 'Bloqueado: elemento não apareceu em 10 tentativas' }
```

Por que polling: logo após o boot, o `uiautomator dump` deu "null root node returned by UiTestAutomationBridge" e funcionou na repetição; e um dump 2 s depois do toque ainda mostrou a tela anterior (X-21). Espera fixa gera falso verde ou falso vermelho, pelo mesmo motivo que `waitForTimeout` no Playwright.

### Tocar e voltar

No XML do dump, cada elemento traz `bounds="[x1,y1][x2,y2]"`. O toque vai no centro: `x = (x1+x2)/2`, `y = (y1+y2)/2`.

```bash
adb -s emulator-5554 shell input tap 540 1200
adb -s emulator-5554 shell input keyevent KEYCODE_HOME
```

Depois do toque, repita o polling até a tela nova aparecer e confirme com `topResumedActivity`.

### Captura de tela

Git Bash:

```bash
adb -s emulator-5554 exec-out screencap -p > F-15-passo-1.png
```

PowerShell 5.1 (evita o redirecionamento de binário; Inferido até o S-13):

```powershell
adb -s emulator-5554 shell screencap -p /sdcard/f.png
adb -s emulator-5554 pull /sdcard/f.png .\F-15-passo-1.png
```

Registre o caminho absoluto da captura na nota. Screenshot com dado pessoal é borrado antes de anexar.

### Encerrar

Se você iniciou o emulador nesta rodada (por exemplo com `Start-Process` do `emulator.exe` do SDK, desacoplado), encerre com:

```bash
adb -s emulator-5554 emu kill
```

Emulador que já estava aberto antes da rodada fica como está.

## 3. Spec nativo equivalente

O spec de F-15 é um teste instrumentado (Compose UI test ou Espresso), escrito e rodado conforme o plugin `mobile-apps`. O resultado volta à mesma matriz `F-NN`, com status e evidência no mesmo formato, e passa pelo `evidence-report` como qualquer outra linha. Appium e Maestro só entram com a instalação confirmada pelo usuário.
