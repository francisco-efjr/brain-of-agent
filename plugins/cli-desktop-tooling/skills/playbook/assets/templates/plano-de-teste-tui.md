# Plano de teste de TUI

Framework: [Textual | Ratatui | Bubble Tea] · Versão: [pip show textual | Cargo.lock | go.mod] · Tamanhos-alvo: [80x24, 120x40] · Roda também em pipe ou CI: [sim/não]

Instalar `pytest-textual-snapshot`, `cargo-insta` ou `teatest` e rodar os testes exigem autorização do usuário. Este plano é um desenho; marque "não executado" até haver saída.

## Fluxos e teclas

| Fluxo | Teclas | Resultado esperado (oráculo) | Teste headless | Snapshot |
| --- | --- | --- | --- | --- |
| Abrir item e salvar | Tab, Enter, Ctrl+S | [estado final e mensagem] | [Pilot, Update com mensagens ou TestBackend] | [80x24, 120x40] |

## Cobertura por camada

| Camada | Textual | Ratatui | Bubble Tea | Escolha para este projeto |
| --- | --- | --- | --- | --- |
| Lógica de estado | pytest | teste Rust | `Update` com mensagens sintéticas | |
| Fluxo headless | `run_test`, `Pilot` | PTY (o `TestBackend` não cobre eventos) | `teatest` (experimental, fixar versão) | |
| Snapshot | `snap_compare` | `TestBackend` e `insta` | golden files | |
| Fora de TTY | verificar | verificar | `WithoutRenderer()` | |

## O que o framework não cobre

- Textual: acessibilidade não documentada nas páginas lidas.
- Ratatui: loop de eventos, teclado e setup do terminal ficam fora do `TestBackend`; cor não aparece nos snapshots atuais.
- Bubble Tea: resize no Windows não reverificado (testar).

## Acessibilidade (risco aberto)

Sem fonte oficial lida nas três. Suposições a validar: contraste suficiente, estado nunca só por cor, alternativa em texto, versão não interativa (`--json`, `--no-input`).

## Critérios de saída

- [ ] Um teste headless por fluxo principal, com oráculo explícito.
- [ ] Snapshot nos dois tamanhos revisado por humano.
- [ ] Falha limpa fora de TTY.
- [ ] Terminal restaurado ao sair e em erro.
- [ ] Riscos abertos listados no relatório.

## Execução

Comandos propostos: [ ] · Resultado: "não executado" ou saída colada.
