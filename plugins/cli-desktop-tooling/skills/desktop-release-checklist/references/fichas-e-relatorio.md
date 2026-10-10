# Fichas de ação externa e modelo de relatório de release

Modelos próprios da fábrica (PAD-11 e o gate de efeito externo do playbook). O texto de exemplo é ilustrativo: valores entre `<...>` são do usuário e nenhum comando foi executado. Verificado em 2026-10-10 contra V-18, V-20, V-42, V-43, V-44, V-45, V-49.

Sumário: [Catálogo REL](#catálogo-de-itens-rel) · [Ficha de ação externa](#ficha-de-ação-externa-modelo) · [Fichas de exemplo](#fichas-de-exemplo) · [Relatório](#modelo-de-relatório)

## Catálogo de itens REL

IDs e severidades padrão do `checklist-completo.md` do playbook (`${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/checklist-completo.md`). Itens marcados "extensão" são desta skill (Inferido quanto à numeração). A severidade padrão é proposta da fábrica (Inferido): ajuste ao risco do produto.

| ID | Item | Fonte | Sev. padrão |
| --- | --- | --- | --- |
| REL-W01 | Identidade de assinatura estável entre releases | V-44 | Média |
| REL-W02 | Decisão de certificado pela árvore da Microsoft (não por "EV obrigatório") | V-44 | Média |
| REL-W03 | Assinatura com timestamp (`/tr` e `/td`) | V-44 | Média |
| REL-W04 | `signtool sign` com `/fd`; `verify /pa` nos artefatos finais | V-44 | Média |
| REL-W05 | Sem senha em `/p` e sem chave no repositório | V-44 | Crítica |
| REL-W06 | Nenhum arquivo modificado depois de assinado | V-44 | Média |
| REL-W07 | Aviso de SmartScreen na primeira release documentado | V-44 | Baixa |
| REL-W08 | MSIX testado (instalar, atualizar, desinstalar); `.appinstaller` por HTTPS | V-40 | Média |
| REL-W09 | Inno Setup: `SignTool` com `$f`, sem senha literal, desinstalador assinado | V-41 | Média |
| REL-W10 | WiX: cabs e MSI assinados, motor Burn assinado antes do bundle | V-42 | Média |
| REL-W11 | WiX v7: EULA e OSMF decididos pelo usuário | V-42 | Alta |
| REL-W12 | winget: URL direta HTTPS, SHA256 recalculado, silencioso testado | V-43 | Média |
| REL-W13 | PR no `winget-pkgs` só com autorização (ficha) | V-43 | Alta |
| REL-W14 | Tauri na Store: instalador EXE ou MSI offline assinado (não MSIX) | V-46 | Média |
| REL-W15 | Caminho de certificado escolhido e documentado (extensão) | V-44 | Alta |
| REL-W16 | Modo silencioso do instalador documentado (`/SILENT`, `/VERYSILENT`, `/S`, `/quiet`) (extensão) | V-41, V-43, V-46 | Média |
| REL-W17 | Arquiteturas: RID por build ou bundle x64/ARM64 (extensão) | V-36 | Média |
| REL-M01 a M06 | macOS e Sparkle (ver [macos-e-updaters.md](macos-e-updaters.md)); REL-M07 é extensão | V-45, V-38, V-49 | variável |
| REL-U01 a U08 | Updater (ver [macos-e-updaters.md](macos-e-updaters.md)); REL-U09 é extensão | V-18, V-20, V-49, V-21 | variável |
| REL-L01 | Linux não avaliado | V-65 | Média (Não verificável) |
| REL-C01 | Teste em máquina limpa: instalar, executar, atualizar | V-17, V-40, V-43 | Média |
| REL-C02 | Desinstalação sem resíduos | V-40, V-43 | Média |
| REL-D01 | Licenças e termos: Qt (V-39), WiX (V-42), Inno (V-41) (extensão) | V-39, V-41, V-42 | Média |

## Ficha de ação externa (modelo)

Preencha uma ficha **por ação com efeito fora do repositório**. A ficha não autoriza nada sozinha: só o usuário, no chat, confirma, e a confirmação vale para aquela ficha, naquela data.

```markdown
## Ficha: <nome da ação>
- Ação: <assinar | notarizar | publicar release | abrir PR no winget-pkgs | aceitar EULA | outra>
- Conta/identidade usada: <conta ou certificado, sem segredos>
- Artefato e versão: <arquivo, versão, hash se houver>
- Destino: <onde o efeito aparece: Store, GitHub Releases, repositório público, feed>
- Ambiente: <máquina/VM/CI e SO>
- Comando exato: <preenchido pelo usuário; conferido com `--help` da versão instalada em AAAA-MM-DD>
- Reversibilidade: <reversível | parcialmente | irreversível> e como desfazer
- Risco: <o que pode dar errado e quem vê>
- Quem executa: usuário
- Pré-requisitos verificados: <itens do relatório que precisam estar conformes>
- Confirmado pelo usuário em: <AAAA-MM-DD, trecho da confirmação no chat>
```

## Fichas de exemplo

### Assinar o instalador (ilustrativa)

```markdown
## Ficha: assinar App-Setup.exe 1.2.0
- Ação: assinar com Authenticode
- Conta/identidade usada: certificado OV da organização, guardado em HSM/serviço em nuvem do emissor
- Artefato e versão: dist\App-Setup.exe 1.2.0
- Destino: o próprio arquivo (a assinatura vira parte do binário)
- Ambiente: máquina de release do usuário, Windows 11
- Comando exato: <usuário preenche; conferido com `signtool sign /?` em AAAA-MM-DD>. Requisitos revisados: /fd SHA256, /tr e /td SHA256, sem /p
- Reversibilidade: o arquivo assinado pode ser regenerado; a identidade usada fica registrada no timestamp e na reputação do SmartScreen
- Risco: assinar binário errado ou modificado depois associa a identidade a ele (V-44)
- Quem executa: usuário
- Pré-requisitos verificados: REL-W03, REL-W04, REL-W05, REL-W15
- Confirmado pelo usuário em: <data e trecho>
```

### Abrir PR no winget-pkgs (ilustrativa)

```markdown
## Ficha: PR do manifesto Acme.App 1.2.0
- Ação: abrir PR público em microsoft/winget-pkgs
- Conta/identidade usada: conta GitHub do usuário
- Artefato e versão: manifests\a\Acme\App\1.2.0 (3 arquivos), InstallerSha256 recalculado em AAAA-MM-DD
- Destino: repositório público; visível a qualquer pessoa
- Ambiente: máquina do usuário; `winget validate` já executado por ele com saída 0
- Comando exato: <usuário escolhe: fluxo manual (fork, branch, PR) ou `wingetcreate`; não aceite a oferta de enviar sozinho sem esta confirmação>
- Reversibilidade: o PR pode ser fechado; histórico e notificações ficam públicos; a Microsoft pode recusar (V-43)
- Risco: hash divergente (Error-Hash-Mismatch), URL indireta, falha de instalação silenciosa
- Quem executa: usuário
- Pré-requisitos verificados: REL-W12, REL-W16, REL-C01
- Confirmado pelo usuário em: <data e trecho>
```

### Notarizar no macOS (ilustrativa)

```markdown
## Ficha: notarização de App.app 1.2.0
- Ação: submeter ao serviço de notarização da Apple e grampear o ticket
- Conta/identidade usada: Apple Developer Program da organização; credenciais por variáveis de ambiente do CI ou chaveiro (nunca em argumento)
- Comando exato: <usuário confere com `xcrun notarytool --help` e `xcrun stapler --help`; sintaxe NÃO verificada pela fábrica (V-45)>
- Reversibilidade: submissão não se desfaz; um build rejeitado só precisa de nova submissão
- Pré-requisitos verificados: REL-M01 a REL-M03, REL-M05
- Quem executa: usuário. Ler o log do serviço é parte do passo (recomendação da Apple)
```

## Modelo de relatório

```markdown
# Checklist de release: <app> <versão>
Data da verificação: AAAA-MM-DD · Plataformas: <...> · Stack/instalador: <...> · Canal: <...>

## Resumo
Veredito: SHIP | FIX FIRST | REWORK. Bloqueadores: <lista curta>.

## Windows
| ID | Item | Status | Evidência | Fonte | Rótulo |
## macOS
(idem) ou "Não aplicável: sem alvo macOS"
## Updater
(idem)
## Linux
Não verificável: sem fonte oficial lida.
## Máquina limpa
Roteiro e resultado esperado (para o usuário executar).
## Licenças e termos
<Qt/WiX/Inno: o que decidir; não é aconselhamento jurídico>

## Fatos voláteis (com URL e data de leitura)
| Fato | Valor lido | URL | Data |

## Ações do usuário (cada uma com ficha)
1. <ação> — ficha em anexo.

## Não verificável
<lista>

## Lacunas conhecidas
<referência à seção "Ressalvas e lacunas" da skill>
```
