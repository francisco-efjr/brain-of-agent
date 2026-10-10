# Windows: assinatura, instaladores, winget (referência de release)

Verificado em 2026-10-10 contra V-36, V-38, V-40, V-41, V-42, V-43, V-44, V-46. Preços, regiões e versões mudam: leia as páginas oficiais citadas antes de decidir e registre a data da leitura. Comandos abaixo são **ilustrativos e não foram executados**; os valores entre `<...>` são do usuário. Nenhuma senha, thumbprint ou URL real aparece aqui.

Sumário: [Certificado](#escolha-de-certificado-v-44) · [SignTool](#signtool-v-44) · [SmartScreen](#smartscreen-v-44) · [Instaladores](#instaladores) · [winget](#winget-v-43) · [Qt](#qt-no-windows-v-38) · [Máquina limpa](#máquina-limpa-roteiro)

## Escolha de certificado (V-44)

Fontes: https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/code-signing-options (`ms.date` 2026-08-29), https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation (2026-05-04), https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool (atualizada 2026-10-05).

| Opção | O que a fonte diz | Quando considerar |
| --- | --- | --- |
| MSIX na Microsoft Store | A Microsoft reassina, sem custo e sem aviso do SmartScreen | App que cabe em MSIX e na Store |
| MSI ou EXE na Store | O publicador assina com certificado de uma CA do Programa de Raiz Confiável | Instalador clássico na Store |
| Azure Artifact Signing (antigo Trusted Signing) | Cerca de US$ 9,99 por mês; organizações nos EUA, Canadá, UE e Reino Unido; indivíduos só nos EUA e Canadá; sem token físico; integra com CI; **não dá confiança instantânea no SmartScreen** | Quando região e tipo de conta permitem |
| OV | US$ 150 a 300 por ano; desde junho de 2023 o CA/Browser Forum exige chave privada em HSM ou token | Alternativa geral |
| EV | O bypass do SmartScreen foi removido em 2024; EV e OV constroem reputação do mesmo jeito; pagar a mais por EV só para evitar aviso "não se justifica mais" | Só por outras razões da organização |
| SignPath Foundation | Assinatura gratuita para projetos de código aberto qualificados | Código aberto |
| Auto-assinado | Só desenvolvimento, ou empresa com confiança distribuída por política | Nunca para público |

Preços e países são os da página na data acima; não foram verificados em site de preços (V-44).

Regras de reputação (V-44): dois sinais, certificado do editor e hash do arquivo; arquivo sem assinatura recomeça do zero a cada versão; use a mesma identidade de assinatura; não modifique o arquivo depois de assinar; não assine programa potencialmente indesejado; não existe envio manual de reputação para o consumidor; o Smart App Control do Windows 11 pode bloquear arquivos sem assinatura e sem reputação positiva.

## SignTool (V-44)

Regras: `sign` exige `/fd` (SHA256 recomendado) e, com `/tr`, também `/td`; `timestamp` sem `/td` só avisa; `verify /pa` usa a política de autenticação padrão; `/tw` avisa quando não há timestamp; códigos de saída 0 (sucesso), 1 (falha) e 2 (avisos).

```powershell
# Certificado já instalado no store do usuário ou da máquina (selecionado pelo thumbprint).
# Sem /p: nenhuma senha em argumento.
signtool sign /fd SHA256 /tr <URL_DO_TIMESTAMP_DA_CA> /td SHA256 /sha1 <THUMBPRINT> "dist\App-Setup.exe"
if ($LASTEXITCODE -ne 0) { throw "signtool sign falhou (código $LASTEXITCODE)" }

signtool verify /pa /v /tw "dist\App-Setup.exe"
if ($LASTEXITCODE -ne 0) { throw "signtool verify falhou (código $LASTEXITCODE)" }
```

`/sha1` seleciona o certificado pelo thumbprint no store (opção padrão do SignTool; confira `signtool sign /?` na versão do Windows SDK instalada). Para assinatura em nuvem, use o fluxo do provedor (por exemplo `signCommand` do Tauri, V-46) e leia a documentação dele; não há sintaxe validada aqui.

Antipadrões a procurar: `/p <senha>` literal; `Import-PfxCertificate -Password (ConvertTo-SecureString "texto" -AsPlainText ...)` com senha no script; `.pfx` versionado; assinar antes de modificar o arquivo (por exemplo, gravar recursos depois).

## SmartScreen (V-44)

A primeira release de uma nova identidade pode exibir aviso mesmo assinada (EV e OV constroem reputação do mesmo jeito). O objetivo operacional é manter a mesma identidade de assinatura e não alterar os arquivos depois de assinados. Em dúvida sobre o que o usuário final verá, rotule **Não verificável** (depende de reputação real) e inclua o teste em máquina limpa.

## Instaladores

| Instalador | Pontos de revisão | Fonte |
| --- | --- | --- |
| MSIX / App Installer | Identidade de pacote (publisher, nome, versão); todo pacote assinado antes da instalação; conteúdo: payload, `AppxBlockMap.xml`, `AppxManifest.xml`, `AppxSignature.p7x`; `.appinstaller` servido por HTTPS; atualização diferencial por blocos de 64 KB; mesmo publisher entre versões; teste de atualização da versão anterior. App Installer vem no Windows 10 1803 ou posterior e no 11 | V-40 |
| Inno Setup | Diretiva `SignTool` que assina instalador, desinstalador (com `SignedUninstaller`) e arquivos de origem; marcador `$f` obrigatório no comando; várias entradas rodam em ordem; comando vindo de variável de ambiente ou store do sistema, sem senha literal; switches silenciosos `/SILENT` ou `/VERYSILENT`; modo por usuário ou por administrador definido; desinstalação testada. Licença própria permissiva (manter avisos de copyright); a ajuda pede licença comercial a usuários comerciais (pedido, não condição) | V-41 |
| WiX | Assinar o `.msi` ou os cabs externos (`wix msi inscribe` registra as assinaturas dos cabs no MSI; com MSBuild, `SignOutput=true` e alvos `SignCabs`, `SignMsi`); bundle em duas partes: motor Burn (`wix burn detach`, assinar, `wix burn reattach`) e depois o `.exe` inteiro (`SignBundleEngine`, `SignBundle`). **OSMF**: organizações com receita acima de US$ 10 mil devem patrocinar a organização do WiX (desde o v6). **v7 exige aceitar o EULA** (`AcceptEula`, `-acceptEula` ou `wix eula accept wix7`): decisão do usuário. A fonte não trata de `insignia`, timestamp nem `wix build` | V-42 |
| NSIS / MSI do Tauri | Formatos que o Tauri gera (MSI pelo WiX v3, NSIS `-setup.exe`); para a Store, instalador offline, assinado, silencioso (`/S` no NSIS, `/quiet` no MSI), WebView2 em modo offline | V-46 |
| Windows App SDK | Framework-dependent (padrão: pequeno, atualizável pelo sistema; depende do runtime) ou self-contained (controle e isolamento; maior); `PublishSingleFile` só para não empacotado e self-contained (1.5 ou posterior); publicar por RID (`win-x64`, `win-arm64`); bundle MSIX com ambas | V-36 |

Ordem de assinatura (WiX): cabs e MSI primeiro, bundle depois, e conferir cada artefato com `signtool verify /pa`.

## winget (V-43)

Fontes: https://learn.microsoft.com/en-us/windows/package-manager/package/manifest, https://learn.microsoft.com/en-us/windows/package-manager/package/repository, https://github.com/microsoft/winget-pkgs (MIT).

Campos mínimos do manifesto (`ManifestVersion` 1.12.0 na data da leitura): `PackageIdentifier` (Publisher.Package), `PackageVersion`, `PackageLocale`, `Publisher`, `PackageName`, `License`, `ShortDescription`, `Installers` (`Architecture`, `InstallerType`, `InstallerUrl`, `InstallerSha256`), `ManifestType`, `ManifestVersion`. Formato singleton (um instalador e uma localidade) ou múltiplo (mínimo 3 arquivos: version, defaultLocale, installer). Pasta no repositório: `manifests/<letra>/<publisher>/<app>/<versão>`; um manifesto por submissão.

Checklist de submissão (V-43):

1. URL do instalador vinda direto do publicador, em HTTPS, sem redirecionador (`Validation-Indirect-URL`).
2. SHA256 recalculado a cada release (`Error-Hash-Mismatch` se divergir).
3. Instalação silenciosa funciona (chaves típicas: MSI `/q`, Inno `/SILENT` ou `/VERYSILENT`, Nullsoft `/S`).
4. Instala e desinstala como administrador e como não administrador.
5. `winget validate` passa antes do PR.
6. Teste no Windows Sandbox com `Tools\SandboxTest.ps1` do repositório.
7. **O PR é ação externa e pública**: só com autorização explícita do usuário (ficha em [fichas-e-relatorio.md](fichas-e-relatorio.md)).

Rótulos de erro conhecidos: `Error-Hash-Mismatch`, `Validation-Indirect-URL`, `Validation-HTTP-Error`, `Validation-Domain`, `Validation-Unattended-Failed`, `Validation-Uninstall-Error`, `URL-Validation-Error`, `Binary-Validation-Error`. `Needs-Author-Feedback` fecha o PR após 10 dias sem resposta; a Microsoft pode recusar qualquer submissão. Ferramentas de criação: `wingetcreate` e `YAMLCreate.ps1` (ambas oferecem enviar o PR sozinhas; **não aceite essa oferta pelo usuário**). A enumeração de tipos de instalador do esquema pode ter valores além dos listados na página (Não verificado).

```powershell
# Ilustrativo; o caminho vem do manifesto do usuário. Só valida localmente.
winget validate --manifest "manifests\a\Acme\App\1.2.0"
```

## Qt no Windows (V-38)

`windeployqt`: `--release`, `--no-translations`, `--qmldir <dir>` (varre importações QML), `--libdir`, `--no-compiler-runtime`; copia DLLs e plugins por tipo (`qwindows.dll` fica em `platforms`). Em release, inclua o Visual C++ Redistributable oficial no instalador, não DLLs soltas do compilador. Bibliotecas de terceiros (banco de dados, por exemplo) entram à mão. Build não relocável pede `qt.conf`; build estático não implanta plugins. Licença: V-39 (14 módulos só-GPL; consulte assessoria jurídica).

## Máquina limpa (roteiro)

Para o usuário executar numa VM ou máquina sem o ambiente de desenvolvimento:

| Passo | Resultado esperado | Evidência a anexar |
| --- | --- | --- |
| Baixar o instalador pelo canal real | Aviso do SmartScreen (se houver) é o esperado para a reputação atual | Captura da tela |
| Instalar como usuário padrão e como administrador | Conclui sem erro; atalho e entrada em Aplicativos | Log do instalador |
| Primeira execução | Abre sem erros; sem pedir ferramentas de desenvolvimento | Captura |
| Atualizar da versão anterior assinada para a nova | A nova versão abre; dados do usuário preservados | Versão exibida |
| Desinstalar | Sem resíduos relevantes (pasta, serviço, tarefa) | Listagem de pastas |
| `signtool verify /pa` nos binários instalados | Código 0 | Saída |
