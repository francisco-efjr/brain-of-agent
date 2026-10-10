---
name: tui-textual-bindings
description: Mede se a revisão de uma TUI Textual aponta bindings sem descrição, priority em tudo, falta de testes e propõe run_test, Pilot e snapshot em dois tamanhos, declarando acessibilidade como lacuna.
tags: [cli-desktop-tooling, tui-review, tui]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: Achados com evidência, correção dos bindings, plano de testes headless e de snapshot e acessibilidade registrada como risco aberto com sugestões rotuladas como suposição.
model: sonnet
---

Tenho uma TUI de tarefas em Textual e nenhum teste. Revisa o código e me diz como eu testo isso? É o app.py:

```python
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import DataTable, Footer, Header, Input


class Tarefas(App):
    BINDINGS = [
        Binding("q", "quit", "", priority=True),
        Binding("n", "nova", "", priority=True, show=False),
        Binding("d", "apagar", "", priority=True, show=False),
        Binding("ctrl+s", "salvar", "", priority=True, show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="nova tarefa")
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        self.tabela = self.query_one(DataTable)
        self.tabela.add_columns("id", "titulo", "feita")

    def action_apagar(self) -> None:
        self.tabela.remove_row(self.tabela.cursor_row)


if __name__ == "__main__":
    Tarefas().run()
```
