# TUI: Textual, Ratatui e Bubble Tea

Sumário: 1. Regras comuns · 2. Textual (Python) · 3. Ratatui (Rust) · 4. Bubble Tea (Go) · 5. Matriz de testes · 6. Acessibilidade (lacuna) · 7. Escolha rápida · 8. Exemplo de achados

Fontes: V-30 (Textual, A), V-31 (Ratatui, B), V-32 (Bubble Tea, B). Páginas de Textual, Ratatui e Bubble Tea não trazem data ou versão: confira `pip show textual`, `Cargo.lock`, `go.mod` antes de afirmar API. A revisão é por leitura; executar testes ou instalar `pytest-textual-snapshot`, `cargo-insta` e `teatest` exige autorização do usuário.

## 1. Regras comuns (valem nas três)

| Regra | Por que | Rótulo |
| --- | --- | --- |
| Estado separado da renderização: a função de desenho não muda estado | Permite testar o estado sem terminal e evita bugs de ordem | Verificado em V-31; Inferido para as outras duas |
| Toda ação tem tecla e descrição visível (rodapé ou ajuda) | Descoberta sem manual | Verificado em V-30 |
| Ordem de foco por Tab e Shift+Tab previsível | Navegação por teclado é o único meio de uso | Verificado em V-30 |
| Um teste headless por fluxo principal | Rápido, determinístico, roda no CI | Verificado em V-30, V-31, V-32 |
| Snapshot em ao menos dois tamanhos (exemplos: 80x24 e 120x40) | Pega quebra de layout no resize | Verificado em V-30, V-31 (tamanho fixo) |
| Resize recalcula o layout | Terminal muda de tamanho a qualquer momento | Regra de projeto: Ratatui não descreve eventos de resize nas páginas lidas (V-31) |
| Falha limpa fora de TTY (pipe, CI) com mensagem e exit code | Evita tela corrompida em log | Inferido |
| Restaurar o terminal ao sair, inclusive em erro | Evita shell quebrado | Inferido (conhecimento estável) |
| Cor nunca é o único sinal; contraste suficiente | Acessibilidade (sem fonte oficial lida) | Suposição |

## 2. Textual (V-30, Classe A)

- `BINDINGS`: tuplas `(tecla, ação, descrição)` ou instâncias `Binding`. `priority=True` é checado antes dos bindings do widget focado e o widget não consegue desativá-lo (o `App` usa em Ctrl+Q): reserve para sair e ajuda. `show=False` esconde do rodapé: use com critério.
- Foco: Tab e Shift+Tab; `can_focus` é booleano; widget desabilitado não recebe foco.
- Teste headless: `async with app.run_test() as pilot:` roda sem atualizar o terminal e devolve um `Pilot`; `await pilot.press("tab", "enter")` aceita várias teclas; `await pilot.click("#botao")` aceita seletor, `offset`, `times` e modificadores; tamanho simulado padrão (80, 24), alterável com `run_test(size=(120, 40))`.
- Snapshot: `pytest-textual-snapshot` com a fixture `snap_compare(app, terminal_size=(120, 40))`.
- Cada teste `async` precisa de `@pytest.mark.asyncio`, salvo `asyncio_mode = auto` configurado uma vez.

```python
# exemplo da fábrica, não executado; confira a API na versão instalada
import pytest
from meu_app import MeuApp

@pytest.mark.asyncio
async def test_fluxo_principal():
    app = MeuApp()
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("tab", "enter")
        assert app.query_one("#resultado").renderable  # troque pelo oráculo real do fluxo

def test_snapshot_largo(snap_compare):
    assert snap_compare(MeuApp(), terminal_size=(120, 40))
```

Armadilhas: acessibilidade não aparece nas páginas lidas; a versão do Textual não consta nelas.

## 3. Ratatui (V-31, Classe B)

- Modo imediato: a UI é reconstruída a cada quadro dentro de `terminal.draw(|f| ...)` a partir do estado. O crate só desenha em um backend (por exemplo `CrosstermBackend`); a biblioteca de eventos é escolha do app. Thread bloqueada trava a UI: tarefas longas fora do loop de desenho.
- Layout divide `Frame::area()` com `Length` (fixo), `Percentage` e `Ratio` (proporcional; cuidado ao misturar com fixos), `Min`, `Max` e `Fill`. Quando as restrições não cabem, o solver pode devolver resultado próximo e não determinístico: teste os tamanhos pequenos.
- Teste: `TestBackend::new(80, 20)`, `terminal.draw(...)`, `assert_snapshot!(terminal.backend())` com `insta`; revisão por `cargo insta review`; a página recomenda tamanho fixo para reprodutibilidade.
- Limites do `TestBackend` (da própria página): não cobre loop de eventos, teclado nem setup do terminal. Para isso, teste de ponta a ponta com PTY. Cor não é suportada nos snapshots atuais.

## 4. Bubble Tea (V-32, Classe B)

- Modelo com `Init`, `Update`, `View`. `tea.KeyPressMsg` chega ao `Update` (README). `WindowSizeMsg` (largura e altura) é enviado ao `Update` uma vez no início e a cada resize; guarde as dimensões no modelo e recalcule o layout na `View`. "Update é função pura" é Inferido da assinatura.
- Fora de TTY (pipe, CI): opção `WithoutRenderer()`. Outras opções: `WithInput`, `WithOutput`, `WithoutSignalHandler`.
- Teste do `Update`: mensagens sintéticas, sem terminal. Fluxo completo: `teatest` (caminho `x/exp`, experimental: fixe a versão) com `NewTestModel`, `WaitFor` (padrão 1 s, checagem a cada 50 ms) e `RequireEqualOutput` com arquivos golden atualizáveis por `-update`.
- Não afirme que o Windows não reporta resize: veio de resumo do pkg.go.dev e não foi reverificado na v2 (C-8 em `fontes.md`). Teste no Windows.
- O README não menciona `WindowSizeMsg` nem teste; essas informações vêm do pkg.go.dev.

## 5. Matriz de testes por camada

| Camada | Textual | Ratatui | Bubble Tea |
| --- | --- | --- | --- |
| Lógica de estado | pytest direto | teste unitário de Rust | `Update` com mensagens sintéticas |
| Fluxo headless | `run_test` e `Pilot` | não coberto pelo `TestBackend`: PTY | `teatest` (experimental) |
| Snapshot visual | `snap_compare` | `TestBackend` e `insta` | golden files do `teatest` |
| Fora de TTY | verificar manualmente | verificar manualmente | `WithoutRenderer()` |
| Terminal real | manual ou PTY | PTY | manual ou PTY |

## 6. Acessibilidade (lacuna declarada)

Nenhuma das três tem fonte oficial de acessibilidade lida. Registre como risco aberto, não como conformidade. Sugestões, todas **Suposição**: contraste suficiente, não depender só de cor, alternativa em texto para estados, modo sem animação, e oferecer a mesma função como CLI não interativa (`--json`, `--no-input`) para quem usa leitor de tela e terminal de linha.

## 7. Escolha rápida (Inferido; ver `decisoes-e-tradeoffs.md`)

| Contexto | Inclinação | Motivo |
| --- | --- | --- |
| Time Python, protótipo rápido, teste headless pronto | Textual | `run_test`, `Pilot`, snapshot documentados |
| Binário único e desempenho, time Rust | Ratatui | Modo imediato; teste de eventos precisa de PTY |
| Time Go, modelo Elm | Bubble Tea | `Update` testável; `teatest` experimental |
| Ferramenta que também roda em pipe | Qualquer uma com modo não interativo | CLI-04 de `checklist-completo.md` |

## 8. Exemplo de achados

| ID | Severidade (Inferido) | Evidência | Correção |
| --- | --- | --- | --- |
| TUI-02 | Média | `BINDINGS = [("q", "quit")]` sem descrição | `("q", "quit", "Sair")` visível no rodapé |
| TUI-03 | Média | `priority=True` em todos os bindings | Restringir a sair e ajuda |
| TUI-05 | Alta | Nenhum teste para o fluxo de salvar | `run_test` com `press` e asserção do estado |
| TUI-08 | Média | Acessibilidade sem registro | Seção "Risco aberto" no relatório |
