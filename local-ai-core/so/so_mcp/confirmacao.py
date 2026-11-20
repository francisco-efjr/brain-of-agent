"""Confirmação humana fora do modelo: janela do próprio Windows.

O modelo não consegue aprovar por conta própria: a resposta vem do clique ou da digitação do
usuário. R2 abre uma janela Sim/Não (o botão padrão é Não). R3 abre uma janela em que é preciso
digitar CONFIRMO. Sem resposta dentro do prazo, a resposta é não.
"""
from __future__ import annotations

from typing import Protocol

_JANELA_SIM_NAO = r"""
$w = New-Object -ComObject WScript.Shell
# 4 = Sim/Não, 48 = alerta, 256 = botão padrão Não, 4096 = sempre na frente
$r = $w.Popup((P 'TEXTO'), [int](P 'TEMPO'), (P 'TITULO'), 4 + 48 + 256 + 4096)
Write-Output ('RESPOSTA:' + $r)
"""

_JANELA_CONFIRMO = r"""
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$f = New-Object System.Windows.Forms.Form
$f.Text = (P 'TITULO'); $f.TopMost = $true; $f.Width = 600; $f.Height = 400
$f.StartPosition = 'CenterScreen'; $f.FormBorderStyle = 'FixedDialog'; $f.MaximizeBox = $false; $f.MinimizeBox = $false
$caixa = New-Object System.Windows.Forms.TextBox
$caixa.Multiline = $true; $caixa.ReadOnly = $true; $caixa.ScrollBars = 'Vertical'; $caixa.Text = (P 'TEXTO')
$caixa.SetBounds(12, 12, 560, 230)
$rotulo = New-Object System.Windows.Forms.Label
$rotulo.Text = 'Ação de alto risco. Para executar, digite CONFIRMO e clique em Executar.'
$rotulo.SetBounds(12, 252, 560, 20)
$entrada = New-Object System.Windows.Forms.TextBox
$entrada.SetBounds(12, 276, 220, 24)
$ok = New-Object System.Windows.Forms.Button
$ok.Text = 'Executar'; $ok.SetBounds(372, 316, 96, 30); $ok.DialogResult = [System.Windows.Forms.DialogResult]::OK
$nao = New-Object System.Windows.Forms.Button
$nao.Text = 'Cancelar'; $nao.SetBounds(476, 316, 96, 30); $nao.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
$f.Controls.AddRange(@($caixa, $rotulo, $entrada, $ok, $nao))
$f.CancelButton = $nao
$relogio = New-Object System.Windows.Forms.Timer
$relogio.Interval = [int](P 'TEMPO') * 1000
$relogio.Add_Tick({ $f.DialogResult = [System.Windows.Forms.DialogResult]::Cancel; $f.Close() })
$relogio.Start()
$f.Add_Shown({ $f.Activate(); $entrada.Focus() })
$r = $f.ShowDialog()
$relogio.Stop()
if ($r -eq [System.Windows.Forms.DialogResult]::OK) { Write-Output ('DIGITADO:' + $entrada.Text) } else { Write-Output 'CANCELADO' }
"""


class Confirmador(Protocol):
    def pedir(self, risco: str, titulo: str, texto: str) -> tuple[bool, str]: ...


class ConfirmadorJanela:
    def __init__(self, executor, timeout_s: int = 120):
        self.executor = executor
        self.timeout_s = timeout_s

    def pedir(self, risco: str, titulo: str, texto: str) -> tuple[bool, str]:
        texto = texto.replace("\r\n", "\n").replace("\n", "\r\n")
        args = {"TITULO": titulo, "TEXTO": texto, "TEMPO": self.timeout_s}
        if risco == "R3":
            r = self.executor.rodar(_JANELA_CONFIRMO, args, timeout=self.timeout_s + 30, rotulo="janela:confirmo")
            linha = r.saida.strip().splitlines()[-1] if r.saida.strip() else ""
            if linha.startswith("DIGITADO:"):
                digitado = linha[len("DIGITADO:"):].strip()
                if digitado.upper() == "CONFIRMO":
                    return True, "janela R3: o usuário digitou CONFIRMO"
                return False, f"janela R3: o usuário digitou '{digitado[:20]}', não CONFIRMO"
            if linha == "CANCELADO":
                return False, "janela R3: o usuário cancelou ou o prazo acabou"
            return False, "janela R3 não abriu: " + r.texto()[:200]
        r = self.executor.rodar(_JANELA_SIM_NAO, args, timeout=self.timeout_s + 30, rotulo="janela:sim_nao")
        linha = r.saida.strip().splitlines()[-1] if r.saida.strip() else ""
        if linha == "RESPOSTA:6":
            return True, "janela R2: o usuário clicou Sim"
        if linha == "RESPOSTA:7":
            return False, "janela R2: o usuário clicou Não"
        if linha == "RESPOSTA:-1":
            return False, f"janela R2: sem resposta em {self.timeout_s} s"
        return False, "janela R2 não abriu: " + r.texto()[:200]


class ConfirmadorNegar:
    """Para execução sem ninguém na frente da tela: nada acima de R1 é aprovado."""

    def pedir(self, risco: str, titulo: str, texto: str) -> tuple[bool, str]:
        return False, "sem janela de confirmação disponível: nada acima de R1 roda sem o usuário"
