# Casos de conflito (resolver-conflitos)

Sumário: 1 Ours e theirs por operação · 2 Tipos de conflito e conduta · 3 Exemplo completo com pergunta · 4 Lockfiles e arquivos gerados · 5 Fim de linha e formatação · 6 Fontes.

Conferido em 2026-10-10. Base: manual do Git (`git-merge`, `git-rebase`, `git-diff`; V-22, V-23), redação própria. Confirme os detalhes na versão instalada com `git help merge` e `git help rebase`. Itens marcados Inferido são conhecimento estável de Git que as fontes lidas pelos pesquisadores não cobriram literalmente.

## 1. Ours e theirs por operação

| Operação | "ours" (stage 2) | "theirs" (stage 3) | Armadilha |
| --- | --- | --- | --- |
| `git merge outra` | A branch em que você está | A branch que você está trazendo | Intuitivo |
| `git rebase base` | A base sobre a qual os commits estão sendo reaplicados | O commit seu que está sendo reaplicado agora | Invertido: `--ours` mantém a versão da base e descarta a sua |
| `git cherry-pick X` | A branch atual | O commit X | Como no merge |
| `git revert X` | A branch atual | A inversa do commit X | Resolver pensando no que o revert pretende desfazer |
| `git stash pop` | Estado atual da árvore | O conteúdo do stash | Conflito deixa o stash guardado; só apague-o depois de resolver |

Os três estados de qualquer arquivo em conflito: `git show :1:<arq>` (base comum), `:2:<arq>` (ours), `:3:<arq>` (theirs). `git ls-files -u` lista os estágios presentes.

## 2. Tipos de conflito e conduta

| Sinal no `git status` | O que aconteceu | Conduta |
| --- | --- | --- |
| `both modified` (`UU`) | Os dois lados alteraram regiões que se tocam | Fluxo normal: intenção de cada lado, combinar |
| `both added` (`AA`) | Os dois criaram o mesmo caminho | Comparar os dois conteúdos; muitas vezes um é cópia do outro; pergunte qual manter ou como juntar |
| `deleted by us` / `deleted by them` (`DU`, `UD`) | Um lado removeu, o outro editou | A pergunta é "o arquivo ainda deve existir?". Veja por que foi removido (`git log --merge -- <arq>`); se deve existir, aplique a edição do outro lado no lugar novo |
| Renomeio com edição | Um lado renomeou e o outro editou | O Git costuma acompanhar o renomeio; se não, aplique a edição no arquivo renomeado e remova o antigo |
| Binário | Imagem, PDF, planilha | Peça qual versão manter; não há mescla textual |
| Lockfile ou arquivo gerado | `package-lock.json`, `*.snap`, build | Não edite: seção 4 |
| Submódulo | Dois SHAs diferentes para o ponteiro | Mostre os dois SHAs e pergunte; atualizar o ponteiro é decisão de quem mantém o submódulo |
| Sem marcadores, mas o teste quebra | Conflito semântico (um lado renomeou a função que o outro passou a chamar) | Rode os testes sempre; ache pelo erro e corrija em commit de resolução |

## 3. Exemplo completo (decisão de negócio em conflito)

Arquivo `src/cpf.ts` durante `git merge feature/cadastro`:

```ts
<<<<<<< HEAD
export function validarCpf(valor: string): boolean {
  const digitos = valor.replace(/\D/g, "");   // aceita 123.456.789-09
  return digitos.length === 11 && checarDigitos(digitos);
}
=======
export function validarCpf(_valor: string): boolean {
  return true; // validação delegada ao serviço de cadastro
}
>>>>>>> feature/cadastro
```

Passo 2, intenção de cada lado (Inferido de código e mensagens: `fix(cpf): accept masked input` em HEAD; `refactor(cadastro): move validation to registry service` na outra):
- Lado A (ours): passar a aceitar CPF com máscara, mantendo a validação local dos dígitos.
- Lado B (theirs): remover a validação local porque o serviço de cadastro valida.

Passo 3: as intenções são incompatíveis (manter ou não a validação local é decisão de arquitetura e de segurança), então pare e pergunte, em uma pergunta objetiva:

```markdown
Os dois lados mudam `validarCpf` de forma incompatível:
A) manter a validação local e aceitar máscara (a regra de HEAD);
B) remover a validação local e confiar no serviço de cadastro (a regra de feature/cadastro).
Se B, os chamadores deixam de ter erro imediato para CPF inválido e dependem da resposta do serviço.
Qual vale para esta integração? Se a resposta for "as duas", posso manter a máscara em `validarCpf`
e chamar o serviço depois, mas isso muda o contrato e merece teste novo.
```

Depois da resposta (suponha A com chamada ao serviço): escreva a função final sem marcadores, ajuste/adicione o teste que cobre máscara e CPF inválido, rode `git grep -n -e '<<<<<<<' -e '>>>>>>>'` (vazio), rode a suíte, mostre `git diff --ours -- src/cpf.ts` e `git diff --theirs -- src/cpf.ts` com cada remoção explicada, e só então proponha `git add src/cpf.ts` e `git merge --continue`.

## 4. Lockfiles e arquivos gerados

1. Resolva primeiro o arquivo-fonte do qual o gerado depende (`package.json`, `pyproject.toml`).
2. Descarte o lockfile em conflito pegando uma das versões como ponto de partida (`git checkout --theirs -- <lock>` ou `--ours`, com confirmação) e regenere com o comando do gerenciador do projeto (ex.: `npm install` para `package-lock.json`; confira a documentação do gerenciador usado). Inferido: procedimento comum; o resultado correto depende do gerenciador.
3. Confira `git diff --stat` do lockfile: mudança proporcional às dependências que alteraram; milhares de linhas inesperadas indicam versão diferente do gerenciador.
4. Rode a instalação limpa e os testes.
5. Snapshots de teste (`*.snap`): regenere com o comando do projeto e leia o diff, porque snapshot gerado cegamente esconde regressão.

## 5. Fim de linha e formatação

- Todas as linhas do arquivo em conflito: suspeite de CRLF contra LF. Compare com `git diff --ignore-space-at-eol` e `git diff -w`. A correção durável é `.gitattributes` (`* text=auto`), mas alterá-lo é mudança de política do repositório: proponha, não faça.
- Um lado só reformatou: aceite a estrutura do lado funcional e reaplique a formatação com o formatador do projeto, em vez de resolver linha a linha.
- Windows: o aviso "LF will be replaced by CRLF" não é erro.

## 6. Fontes

- Manual do Git: `git-merge` ("How conflicts are presented", "How to resolve conflicts"), `git-rebase`, `git-diff` (V-22, V-23, classe B; licença do manual não verificada, só destilado).
- Técnica de escrever a intenção de cada lado: Inferida (V-22).
