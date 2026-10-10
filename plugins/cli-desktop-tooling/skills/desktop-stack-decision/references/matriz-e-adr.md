# Matriz de stacks desktop e modelo de ADR

Verificado em 2026-10-10 contra V-16, V-19, V-33, V-35, V-36, V-37, V-38, V-39, V-40, V-46, V-65. Fatos voláteis (versões mínimas, formatos de instalador, política da Store) mudam: reconfira as páginas oficiais antes de decidir. Células sem fonte validada estão marcadas "não avaliado".

Sumário: [Fatos por stack](#fatos-por-stack) · [Matriz qualitativa](#matriz-qualitativa) · [Árvore de filtros](#árvore-de-filtros) · [Modelo de ADR](#modelo-de-adr) · [ADR de exemplo](#adr-de-exemplo-ilustrativo)

## Fatos por stack

| Stack | O que a fonte validada diz | Fonte |
| --- | --- | --- |
| Electron | Checklist oficial de 20 recomendações de segurança; fuses (`@electron/fuses`) para endurecer o binário; updater com Squirrel (`RELEASES`, HTTP 204); assinatura e notarização documentadas; Electron Forge recomendado para Windows | V-16, V-48, V-18, V-17 |
| Tauri v2 | Núcleo Rust com acesso total; frontend em WebView do sistema vê só o que o IPC expõe; capabilities por janela; gera apenas MSI e NSIS no Windows; Store aceita EXE ou MSI; updater com assinatura obrigatória | V-19, V-47, V-46, V-20 |
| WinUI 3 | Framework nativo recomendado para novos apps Windows; parte do Windows App SDK; C# ou C++; Windows 10 1809 (build 17763) ou posterior; acessibilidade por UI Automation | V-35, V-36 |
| WPF | Só Windows, mesmo sobre .NET moderno; XAML, binding, comandos, templates; página oficial recomenda migrar de .NET Framework para .NET | V-33 |
| .NET MAUI | Projeto único para Android, iOS, macOS e Windows; no Windows usa WinUI 3; iOS e macOS exigem um Mac para compilar | V-37 |
| Qt 6 | `windeployqt` e `macdeployqt` para implantar; licença comercial ou LGPLv3/GPLv3; 14 módulos não disponíveis sob LGPLv3 | V-38, V-39 |
| MSIX | Identidade de pacote (push, tarefas em segundo plano, Store, Intune), atualização diferencial, desinstalação limpa; todo pacote precisa estar assinado | V-40 |

## Matriz qualitativa

Legenda: F favorável, N neutro, D desfavorável, ? não avaliado (sem fonte). A coluna "Base" cita de onde veio o julgamento; julgamentos sem item V são **Inferido**.

| Critério | Electron | Tauri v2 | WinUI 3 | WPF | MAUI | Qt 6 |
| --- | --- | --- | --- | --- | --- | --- |
| Multiplataforma desktop | F | F | D (só Windows) | D (só Windows) | N (Windows e macOS, mais mobile) | F |
| MSIX / identidade de pacote | N (confirmar tooling em protótipo) | D (V-46, V-65) | F (V-36, V-40) | N (empacotável em MSIX; V-40, Inferido) | F no Windows (usa WinUI 3; Inferido) | ? |
| Segurança por padrão | N (exige configuração; V-16) | N (capabilities, mas "todos os comandos para todas as janelas" por padrão; V-19) | ? (sem fonte lida) | ? | ? | ? |
| Acessibilidade | ? | ? | F (guia oficial; V-35) | ? (página não localizada) | ? | ? |
| Auto-update documentado | F (V-18) | F (V-20) | N (App Installer; V-40) | N (idem) | N | ? |
| Curva para equipe web | F | N (Rust no núcleo) | D | D | D | D |
| Curva para equipe C# | D | D | F | F | F | D |
| Risco de licença | F | F | F | F | F | N (módulos só-GPL; V-39) |
| Pegada de instalador e memória | não avaliado (sem benchmark válido; V-65 é N=1) | idem | idem | idem | idem | idem |

Pegada e desempenho ficam "não avaliado" de propósito: meça no protótipo com os dados do próprio app.

## Árvore de filtros

1. A distribuição exige **MSIX/Store/Intune com identidade**? Sim: elimine Tauri; considere Electron (validar tooling), WinUI 3, WPF empacotado.
2. Precisa de **macOS ou mobile** com a mesma base? Sim: MAUI, Electron, Tauri (mobile do Tauri não foi avaliado aqui), Qt.
3. **Só Windows** e UI nativa moderna? WinUI 3 (novo) ou WPF (existente).
4. **Código fechado** com Qt? Cruze os módulos com os 14 só-GPL; consulte assessoria jurídica para LGPLv3.
5. **Node completo** no processo principal? Electron.
6. **Pegada pequena** com WebView do sistema aceita? Tauri; testar Linux cedo.
7. Empate? Escolha o que a equipe já domina e registre o custo de saída; protótipo de assinar, instalar, atualizar e desinstalar decide o resto.

## Modelo de ADR

```markdown
# ADR-NNN: Stack do app desktop [nome]
Data: AAAA-MM-DD · Status: proposta | aceita · Autor: [quem]

## Contexto
[Produto, usuários, SO-alvo, equipe, prazo.]

## Requisitos e restrições duras
- [restrição] (origem: pedido do usuário / V-xx)

## Alternativas consideradas
| Opção | Eliminada por | Ainda viável por |
| --- | --- | --- |

## Matriz qualitativa
[Tabela F/N/D/? com fonte por célula.]

## Decisão
[Opção escolhida e por que, em 3 a 5 linhas.]

## Consequências
[O que fica fácil, o que fica difícil, custo de saída.]

## Protótipo necessário (testes de aceite)
- [ ] Assinar, instalar, atualizar da versão anterior e desinstalar em máquina limpa
- [ ] [item específico da stack]

## Perguntas abertas
- [pergunta] (impacto: [decisão que depende dela])

## Rótulos
Verificado: [...] · Inferido: [...] · Suposição: [...] · Não verificável: [...]
```

## ADR de exemplo (ilustrativo)

Cenário fictício para mostrar o nível de detalhe esperado. Nenhum dado abaixo vem de um projeto real.

```markdown
# ADR-001: Stack do app desktop "Inventário"
Data: 2026-10-10 · Status: proposta

## Contexto
App interno de inventário para 300 máquinas Windows 11; equipe de 4 pessoas com C#; distribuição por Intune.

## Requisitos e restrições duras
- Apenas Windows 11 (origem: pedido)
- Instalar por Intune e receber notificações push → identidade de pacote → MSIX (V-40)

## Alternativas consideradas
| Opção | Eliminada por | Ainda viável por |
| --- | --- | --- |
| Tauri | Gera só MSI e NSIS (V-46) | n/a |
| MAUI | Sem alvo mobile nem macOS (V-37) | n/a |
| Electron | Equipe sem experiência web; Windows apenas | Possível, mas custa curva |
| WPF | n/a | Base existente? (não há) |
| WinUI 3 | n/a | Recomendado para novos apps (V-35) |

## Decisão
WinUI 3 empacotado em MSIX. Motivo: restrição de identidade de pacote atendida de forma nativa, equipe já domina C# e XAML, guia oficial de acessibilidade disponível.

## Consequências
Fica fácil: Intune, atualização diferencial, desinstalação limpa (V-40). Fica difícil: sem macOS; segurança de .NET desktop sem fonte lida (lacuna).

## Protótipo necessário
- [ ] Instalar, atualizar e desinstalar por Intune em máquina limpa
- [ ] Narrator nos três fluxos críticos (verificação humana; V-35)
- [ ] Bundle x64 e ARM64 se o parque tiver ARM (V-36)

## Perguntas abertas
- O parque tem Windows ARM? (decide o bundle)
- Certificado da empresa ou assinatura de outro caminho? (V-44; vai para desktop-release-checklist)

## Rótulos
Verificado: restrições V-35, V-36, V-37, V-40, V-46 · Inferido: escolha entre WinUI 3 e WPF pela data do projeto · Suposição: parque 100% Windows 11 · Não verificável: comportamento sob Intune sem teste
```
