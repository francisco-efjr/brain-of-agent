# TUI: comportamento por framework e snippets de teste

Verificado em 2026-10-10 contra V-30, V-31, V-32. Os trechos são ilustrativos e **não foram executados**; confirme nomes e assinaturas na versão instalada (`pip show textual`, `Cargo.lock`, `go.mod`). Itens marcados "estável" vêm de conhecimento geral dos projetos, não de uma página validada.

Sumário: [Comparação](#comparação) · [Textual](#textual-python) · [Ratatui](#ratatui-rust) · [Bubble Tea](#bubble-tea-go) · [Plano de teste](#plano-de-teste-modelo) · [Perguntas abertas](#perguntas-abertas)

## Comparação

| Aspecto | Textual | Ratatui | Bubble Tea |
| --- | --- | --- | --- |
| Modelo | Widgets, `BINDINGS`, ações | Modo imediato: reconstrói tudo a cada `draw` | `Init`, `Update`, `View` (Elm) |
| Eventos | Embutido no framework | Escolha do app (ex.: crossterm) | `tea.Msg` no `Update` |
| Resize | Não declarado nas páginas lidas | Novo `Frame::area()` no próximo draw (regra de projeto) | `WindowSizeMsg` no início e a cada resize |
| Teste headless | `app.run_test()` + `Pilot` | `TestBackend` + `insta` (só renderização) | `Update` com mensagens sintéticas; `teatest` (experimental) |
| Snapshot | `pytest-textual-snapshot` (`snap_compare`) | `assert_snapshot!(terminal.backend())` | golden files do `teatest` (`-update`) |
| Fora de TTY | Não confirmado | Não confirmado | `WithoutRenderer()` |
| Acessibilidade | Sem fonte lida | Sem fonte lida | Sem fonte lida |
| Licença do projeto | MIT | MIT | MIT |

Fonte: V-30, V-31, V-32 (licenças e estrelas verificadas pelo validador em 2026-10-10).

## Textual (Python)

Checklist de leitura:

- `BINDINGS` como tuplas `(tecla, ação, descrição)` ou instâncias `Binding`; `priority=True` só em sair e ajuda; `show=False` com critério.
- `can_focus` e widgets desabilitados: widget desabilitado não recebe foco (V-30).
- Cada `action_*` tem um teste.

Teste headless (ilustrativo):

```python
import pytest
from monitor.app import MonitorApp


@pytest.mark.asyncio  # dispensável com asyncio_mode = auto no pytest
async def test_filtrar_e_sair():
    app = MonitorApp()
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("tab", "tab")        # ordem de foco
        await pilot.press("/", "a", "enter")   # várias teclas numa chamada
        await pilot.click("#lista")            # seletor CSS do widget
        assert app.query_one("#lista").row_count >= 0
        await pilot.press("ctrl+q")            # Ctrl+Q é o binding de sair do App (V-30)
```

Snapshot em dois tamanhos (ilustrativo; `snap_compare` vem do `pytest-textual-snapshot`):

```python
import pytest

@pytest.mark.parametrize("tamanho", [(80, 24), (120, 40)])
def test_snapshot_tela_inicial(snap_compare, tamanho):
    assert snap_compare("../monitor/app.py", terminal_size=tamanho)
```

O caminho do app é relativo ao arquivo de teste. O parâmetro `press=[...]` do `snap_compare` aplica teclas antes da captura (estável; confirme na versão do plugin).

## Ratatui (Rust)

Checklist de leitura:

- A função que desenha recebe `&State` (leitura) e `&mut Frame`; qualquer mutação de estado dentro de `draw` é achado.
- O loop de eventos fica fora da renderização e não bloqueia a thread da UI (thread bloqueada trava a UI, V-31).
- Restrições `Length` + `Percentage` misturadas são testadas em tamanho pequeno.

Snapshot (ilustrativo; dependência de desenvolvimento `insta`):

```rust
use ratatui::{backend::TestBackend, Terminal};

#[test]
fn tela_inicial_80x20() {
    let mut terminal = Terminal::new(TestBackend::new(80, 20)).unwrap();
    let state = State::exemplo();
    terminal.draw(|frame| ui::draw(frame, &state)).unwrap();
    insta::assert_snapshot!(terminal.backend());
}
```

Revisão dos snapshots com `cargo insta review` (V-31). Repita com um segundo tamanho. Limites do `TestBackend`, segundo a própria página: não cobre loop de eventos, teclado nem setup do terminal; cor não é suportada nos snapshots atuais. Para esses, o plano precisa de teste de ponta a ponta com PTY (a escolha da ferramenta de PTY é do projeto; não há recomendação validada).

## Bubble Tea (Go)

Checklist de leitura:

- O modelo guarda `width` e `height` ao receber `tea.WindowSizeMsg` e a `View` usa esses valores.
- `Update` não faz I/O bloqueante; trabalho longo vai em `tea.Cmd`.
- Programa preparado para pipe e CI com `tea.WithoutRenderer()` (V-32).

Teste do `Update` com mensagens sintéticas (ilustrativo; a forma da tecla depende da versão: `tea.KeyPressMsg` na API atual do README):

```go
func TestResizeAtualizaLayout(t *testing.T) {
	m := novoModelo()
	next, _ := m.Update(tea.WindowSizeMsg{Width: 80, Height: 24})
	got := next.(modelo)
	if got.largura != 80 || got.altura != 24 {
		t.Fatalf("esperava 80x24, veio %dx%d", got.largura, got.altura)
	}
}
```

Fluxo completo com `teatest` (pacote em `x/exp`, experimental; **fixe a versão** no `go.mod`). Funções citadas em V-32: `NewTestModel`, `WaitFor` (padrão 1 s, checagem a cada 50 ms), `RequireEqualOutput` com golden files atualizáveis por `-update`. A assinatura exata e as opções variam com a versão: leia o pkg.go.dev da versão fixada antes de escrever o teste.

## Plano de teste (modelo)

| Fluxo | Teclas | Tamanho | Tipo | Cobre | Não cobre |
| --- | --- | --- | --- | --- | --- |
| Abrir e sair | iniciar, `q` | 80x24 | headless | binding de sair, restauração do terminal em código | terminal real |
| Filtrar e excluir | `/`, texto, `enter`, `d`, `y` | 80x24, 120x40 | headless + snapshot | foco, ação, layout nos dois tamanhos | cor (Ratatui), leitor de tela |
| Resize | mudar tamanho durante a execução | 80x24 para 120x40 | headless (mensagem de tamanho / `size=`) | recálculo do layout | resize real no Windows (não reverificado, V-32) |
| Pipe/CI | executar com saída redirecionada (por exemplo, para `cat`) | n/a | fora de TTY | falha limpa, sem escape codes | acessibilidade |

Acessibilidade (lacuna): marcar como risco aberto; **Suposição** a validar com usuários: contraste suficiente, estado nunca só por cor, alternativa em texto.

## Perguntas abertas

1. Qual a versão do framework e do pacote de teste fixada no projeto?
2. A TUI precisa rodar em pipe, em CI ou em SSH? Qual terminal no Windows (Windows Terminal, conhost, Git Bash)?
3. Existe processo de revisão de snapshots, para que atualizá-los não vire clique automático?
