# Fronteiras verificáveis por máquina

Sumário: 1. Tabela camada -> imports · 2. Fachada, esquema e eventos · 3. Verificador por busca textual (testado) e 3.1 Catraca para legado (testada) · 4. Ferramentas de teste de arquitetura (não executadas) · 5. Métrica de acoplamento de mudança (testada) · 6. Regras de CLAUDE.md · 7. Gotchas

Validado em 2026-10-10. Fontes: V-24 (awesome-cursorrules, CC0: tabela de imports permitidos, handler curto, escritor único, verificação por grep; faixas de tamanho de arquivo são opinião), V-25 (hexagonal, dependências para dentro), V-28 (monólito modular, MIT: teste de dependência no CI, esquema por módulo, acoplamento de mudança), V-44 (ponteiros para arquivos canônicos, regra positiva com gatilho de parada), V-45 (ferramentas de dependência citadas sem avaliação). Os dois scripts abaixo foram executados em um repositório sintético com Git Bash em 2026-10-10 e se comportaram como descrito (Verificado para o exemplo; ajuste de extensões e padrões ao seu projeto é seu).

Instrução é pedido; teste de CI é garantia (P-26). Fronteira só vale se o build quebra quando ela é violada.

## 1. Tabela camada -> imports

Preencha por projeto (exemplo hexagonal em quatro camadas):

| Camada ou módulo | Pode importar | Não pode importar | Verificador |
| --- | --- | --- | --- |
| `domain` (regras e entidades) | `domain`, biblioteca padrão | `adapters`, `infra`, frameworks web e de banco | busca textual ou teste de arquitetura |
| `application` (casos de uso, portas) | `domain` | `adapters`, `infra` | idem |
| `adapters` (HTTP, banco, filas) | `application`, `domain` | outros `adapters` | idem |
| `modules/billing` | sua própria pasta, fachada pública de outros módulos | interior de `modules/orders` (`internal/`) | idem |

Princípio (V-25): dependências apontam para dentro; o núcleo roda sem banco nem UI; um mock é um adaptador em memória. Handler fino (a fonte V-24 usa 10 linhas executáveis como referência, Suposição) e dependências por interface ajudam a manter a regra.

## 2. Fachada, esquema e eventos

- **Fachada:** cada módulo expõe um ponto de entrada (arquivo, pacote ou interface). Importar do interior de outro módulo é violação.
- **Propriedade de esquema:** tabelas pertencem a um módulo (prefixo no nome ou esquema separado). Outro módulo lê dados apenas pela fachada, por evento ou por visão de leitura explicitamente publicada.
- **Eventos entre módulos:** contrato versionado; consumidores toleram campos novos. Em processo único, eventos internos ainda precisam de idempotência se houver reprocessamento.
- **Código compartilhado:** pasta `shared` pequena e sem regra de negócio; cada inclusão exige motivo no ADR.

## 3. Verificador por busca textual

Serve como primeira barreira quando não há ferramenta de arquitetura. Limites: busca textual não entende resolução de módulos, imports dinâmicos nem reexportações (falsos negativos); comentários que contêm o padrão geram falsos positivos (Inferido). Salve como `scripts/check-boundaries.sh` no seu projeto, revise e chame no CI. Este plugin não cria nem executa o arquivo.

```bash
#!/usr/bin/env bash
# Verifica regras de dependência por busca textual. Saída 1 se houver violação.
set -u
status=0
check() {  # $1 pasta, $2 regex (ERE), $3 motivo
  [ -d "$1" ] || { echo "AVISO: pasta inexistente: $1"; return; }
  hits=$(grep -rnE --include='*.ts' --include='*.js' --include='*.py' "$2" "$1" || true)
  if [ -n "$hits" ]; then
    echo "VIOLAÇÃO: $3"; echo "$hits"; status=1
  fi
}
check src/domain "(from|import|require).*(adapters|infra)/" "domain não importa adapters nem infra"
check src/modules/billing "orders/internal" "billing não importa o interior de orders"
exit $status
```

Saída observada no teste: com `import x from '../adapters/db'` em `src/domain/order.ts`, o script imprimiu `VIOLAÇÃO: domain não importa adapters nem infra` seguido de `src/domain/order.ts:1:...` e saiu com código 1.

### 3.1 Catraca para legado

Em código que já viola a regra, o script da seção 3 falha de imediato e ninguém o adota. A catraca aceita as violações que existem hoje, registradas em uma lista, e impede que a lista cresça: violação nova falha o build; violação corrigida também falha até sair da lista, o que baixa o teto. A lista só encolhe. Salve como `scripts/boundary-ratchet.sh` no seu projeto (este plugin não cria nem executa o arquivo). O padrão busca **também o nome qualificado**, não só `import`: contar só linhas de import deixa passar uso qualificado e ciclos entre pacotes (numa avaliação real, um ciclo `model` e `util` só apareceu ao ler o arquivo).

```bash
#!/usr/bin/env bash
# Catraca de fronteiras para legado: violações conhecidas ficam em scripts/boundary-baseline.txt
# e só podem diminuir. Violação nova falha; violação corrigida também falha até sair da lista.
set -u
baseline=scripts/boundary-baseline.txt
current=$(mktemp)
rule() {  # $1 id da regra, $2 pasta, $3 regex ERE (pega import e nome qualificado), $4 extensão
  [ -d "$2" ] || { echo "AVISO: pasta inexistente: $2"; return; }
  grep -rlE --include="*.$4" "$3" "$2" | awk -v r="$1" '{print r "\t" $0}' >> "$current" || true
}
rule R1-model-nao-usa-util app/src/main/java/com/app/model 'com\.app\.util\.' kt
sort -o "$current" "$current"
[ -f "$baseline" ] || : > "$baseline"
sort -o "$baseline" "$baseline"
novas=$(comm -13 "$baseline" "$current")
corrigidas=$(comm -23 "$baseline" "$current")
status=0
if [ -n "$novas" ];      then echo "VIOLAÇÃO NOVA (fora da lista conhecida):"; echo "$novas"; status=1; fi
if [ -n "$corrigidas" ]; then echo "CORRIGIDA: remova de $baseline para baixar o teto:"; echo "$corrigidas"; status=1; fi
echo "violações conhecidas: $(wc -l < "$baseline"), atuais: $(wc -l < "$current")"
rm -f "$current"
exit $status
```

Primeira execução: com a lista vazia, o script imprime as violações atuais como novas; copie-as para `scripts/boundary-baseline.txt` (formato `regra<TAB>arquivo`) e comite. Teste em repositório sintético com Git Bash em 2026-10-10: com dois arquivos violadores listados saiu 0; um terceiro arquivo violador saiu 1 (violação nova); corrigir um dos listados saiu 1 pedindo a remoção da linha (Verificado para o exemplo). Limites: a granularidade é o arquivo (um arquivo que ganha uma segunda violação passa) e a busca textual não resolve reexportações nem imports dinâmicos. O mesmo padrão serve para o teto de qualquer contagem (por exemplo, número de usos de uma API proibida). Em Kotlin ou Java, um teste JVM que lê os `.kt` e `.java` e aplica a mesma regex dispensa o script de shell e roda no CI comum (ideia; não testada aqui).

Outras verificações de leitura úteis como fitness function: varredura de arquivos que sugerem dado pessoal versionado, `git ls-files | grep -Ei '(cpf|cadastro|contrato|\.csv$|\.xlsx$|\.pdf$)'` (lista candidatos para revisão humana; não prova ausência), e checagem de manifesto (por exemplo `grep -n 'allowBackup\|usesCleartextTraffic' app/src/main/AndroidManifest.xml`).

Regra de CLAUDE.md correspondente (S-02, forma positiva com gatilho de parada): "O domínio não importa adaptadores. Verificação: `bash scripts/check-boundaries.sh`. Se parecer necessário importar, pare e registre a dúvida."

## 4. Ferramentas de teste de arquitetura (citadas, não executadas)

Estas ferramentas são citadas em V-45 como vocabulário e **não foram executadas nem avaliadas** nesta pesquisa. Instalar pacote de terceiros é decisão do usuário; este plugin não instala nem roda nada.

| Ecossistema | Ferramenta | Ideia | Estado de verificação |
| --- | --- | --- | --- |
| JavaScript/TypeScript | dependency-cruiser, madge | Regras `forbidden` de dependência entre pastas; detecta ciclos | Citadas em V-45; sintaxe de configuração Não verificada aqui: consulte a documentação oficial da versão instalada |
| Java/Kotlin | ArchUnit | Regras em teste de unidade (`noClasses().that().resideInAPackage(...)...`) | Lacuna de fonte (Não verificado); conferir a documentação |
| Python | busca textual ou ferramenta de lint de imports do projeto | Mesma ideia | Não avaliado |

Ao recomendar uma ferramenta, diga: "ainda não verificada por este plugin; confira a documentação e a licença antes de adotar".

## 5. Métrica de acoplamento de mudança

Fração dos commits recentes que tocam mais de um módulo. Subindo ao longo do tempo, indica fronteiras no lugar errado (V-28). O limiar de 50% da fonte é escolha do autor (Suposição); acompanhe a tendência.

```bash
# Ajuste "src/modules" e a posição do nome do módulo (p[3] = src/modules/<modulo>/...)
git log --since="90 days ago" --name-only --pretty=format:'#%h' -- src/modules |
awk '
/^#/ { if (n>0) { total++; if (n>1) multi++ } delete mods; n=0; next }
NF==0 { next }
{ split($0, p, "/"); m=p[3]; if (!(m in mods)) { mods[m]=1; n++ } }
END { if (n>0) { total++; if (n>1) multi++ }
      printf "commits: %d, multi-módulo: %d (%.0f%%)\n", total, multi, total ? 100*multi/total : 0 }'
```

Teste: em repositório sintético com 3 commits (um só no módulo `billing`, dois tocando `billing` e `orders`), a saída foi `commits: 3, multi-modulo: 2 (67%)` (nesse teste o texto sem acento). É comando de leitura; rodá-lo pelo fluxo normal de permissão é decisão do usuário. Commits de merge e de renomeação em massa distorcem o número: filtre se necessário (Inferido).

## 6. Regras de CLAUDE.md para fronteiras

- "Módulo A não importa módulo B. Verificação: `<comando>`. Se parecer necessário importar, pare e registre a dúvida." (S-02)
- "Antes de criar tipo ou função, procure o nome no repositório e reutilize. Padrão canônico de `<tema>`: `<arquivo>`." (S-07)
- "ADRs aceitos em `docs/adr/` são restrições vigentes; mudar uma exige novo ADR que a substitua." (S-03)

Listas longas de "não use X" falham; um ponteiro para um arquivo de exemplo funciona melhor (V-44, relato de praticante, Inferido).

## 7. Gotchas

- Faixas de tamanho de arquivo (verde até 399 linhas, amarelo até 599, vermelho 600 ou mais, em V-24) são opinião da fonte: Suposição configurável.
- A regra em prosa sem verificador degrada em semanas: registre sempre o comando.
- Busca só por `import` perde uso qualificado (`com.app.util.Names.f()` sem import) e ciclos entre pacotes: inclua o nome qualificado no padrão.
- Falso senso de segurança: o grep passa, mas um import dinâmico ou reexportação escapa; complemente com revisão (`architecture-design:boundary-mapper`) e, quando justificar, ferramenta de arquitetura.
- Fronteiras mudam: revise a tabela quando um ADR de módulo for aceito.
