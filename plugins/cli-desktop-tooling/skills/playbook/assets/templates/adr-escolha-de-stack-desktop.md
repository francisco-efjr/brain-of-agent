# ADR [ID]: escolha de stack desktop

Estado: [proposta | aceita | substituída] · Data: [AAAA-MM-DD] · Autor: [ ]

Moldado no ADR do brain-of-agent (MIT) e adaptado a este segmento. Sem números de benchmark: o relato V-65 é N=1.

## Contexto

Produto, usuários, SO-alvo, canal de distribuição, equipe e habilidades. Requisitos funcionais relevantes à stack (Node completo? APIs nativas? offline? auto-update?).

## Restrições duras (cada uma cita a fonte)

| Restrição | Efeito nas alternativas | Fonte |
| --- | --- | --- |
| [Store com MSIX / identidade de pacote] | Tauri gera só MSI e NSIS; a Store aceita EXE ou MSI | V-46, V-40, V-65 |
| [Alvo mobile ou macOS] | MAUI | V-37 |
| [Só Windows moderno] | WinUI 3 | V-35 |
| [Licença de código fechado com Qt] | Cruzar módulos com os 14 só-GPL | V-39 |
| [Linux sério] | Testar WebKitGTK (Tauri) cedo; sem fonte oficial | V-65 |

## Alternativas

| Opção | Benefício | Custo/risco | Compatibilidade com as restrições | Evidência |
| --- | --- | --- | --- | --- |

## Matriz qualitativa (sem números)

| Critério | A | B | C | Rótulo |
| --- | --- | --- | --- | --- |
| Segurança padrão | | | | |
| Distribuição e Store | | | | |
| Auto-update | | | | |
| Acessibilidade | | | | |
| Curva da equipe | | | | |
| Manutenção | | | | |

## Decisão

Opção escolhida e por quê. Hipóteses ainda não confirmadas, com rótulo Inferido ou Suposição.

## Consequências

Segurança (checklists aplicáveis), distribuição, operação, testes. Limites de reversibilidade.

## Protótipo necessário antes de aceitar

- [ ] Assinar, instalar, atualizar (N-1 para N) e desinstalar em máquina limpa.
- [ ] Comportamento do WebView em Linux (se aplicável).
- [ ] Ordem de assinatura do updater do Tauri (se aplicável; hipótese de V-21).

## Perguntas abertas e condição para reconsiderar

[ ]

## Rótulos

Verificado: [ ] · Inferido: [ ] · Suposição: [ ] · Não verificável: [ ]
