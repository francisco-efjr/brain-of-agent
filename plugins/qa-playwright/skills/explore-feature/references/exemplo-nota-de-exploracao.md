# Exemplo de nota de exploração: F-07 no sistema-demo

Nota ilustrativa de uma exploração do sistema-demo de tarefas (dados sintéticos). O achado do contador vem de X-14 e o `DELETE 200` de X-20; o código gerado segue o formato de X-06 e X-11. Caminhos e nomes de arquivo são de exemplo.

````markdown
# F-07 Excluir tarefa atualiza lista e contador · exploração · 2026-10-13 · Playwright 1.64.0 · Chrome
Alvo: http://127.0.0.1:4173/tarefas · Papel: usuário (estado carregado com state-load, arquivo não lido) · Estado inicial: lista vazia

## Passos e observado
1. `open` na rota `/tarefas`; `state-load` do estado da porta 4173; `goto`. Página abriu com o campo "Nova tarefa" e o botão "Adicionar".
2. `fill` do campo com "Comprar pão" e `click` em "Adicionar". Item "Comprar pão" apareceu; parágrafo mostra `1 pendente(s)`.
3. `click` em "Excluir" do item. A lista ficou vazia. O parágrafo continua `1 pendente(s)`.
4. `find "pendente"` confirmou o texto do parágrafo depois da exclusão: `1 pendente(s)`. (Passo ilustrativo: recarregar a página e repetir o `find` mostraria se o valor persiste; X-14 não registra esse resultado.)

## Efeito verificado (como)
O efeito esperado é o contador voltar a `0 pendente(s)`. Conferi pelo texto do parágrafo com `find "pendente"` depois da exclusão. **Falhou:** o contador não zera (X-14).

## Esperado e fonte
Esperado: `0 pendente(s)` com a lista vazia. Fonte: coerência da própria UI (o rótulo do contador precisa bater com a lista). Sem requisito escrito: se o dono do produto discordar, a falha vira decisão pendente.

## Console e rede (triagem)
- `console`: 404 de `favicon.ico`. Ruído conhecido, não é achado (X-10).
- Rede: `requests` lista as chamadas no formato `[GET] …/api/tarefas => [200] OK` (estáticas ocultas sem `--static`) e `request <n>` mostra o detalhe (X-26). Registre método e status da exclusão. No trace do spec que falha, `trace requests` mostrou `DELETE 200` (X-20): o backend excluiu e o defeito está no contador da UI.

## Evidência (caminhos absolutos)
- Snapshot depois de excluir: `C:\...\sistema-demo\e2e-playwright\.playwright-cli\F-07-depois.yml`
- Screenshot: `C:\...\sistema-demo\e2e-playwright\.playwright-cli\F-07-depois.png`
- Trace: `C:\...\sistema-demo\e2e-playwright\.playwright-cli\traces\<arquivo>.trace`

## Código gerado
```ts
await page.getByRole('textbox', { name: 'Nova tarefa' }).fill('Comprar pão');
await page.getByRole('button', { name: 'Adicionar' }).click();
await page.getByRole('listitem').filter({ hasText: 'Comprar pão' }).getByRole('button', { name: 'Excluir' }).click();
```
(As ações vêm da CLI. A asserção do contador não vem: o spec a escreve.)

## Conteúdo da página (dado)
Nenhum texto da página pediu ação fora do cenário.

## Veredito provisório
Falhou (efeito errado, esperado com fonte). Candidato a BUG-NN; classificação final no `failure-triage`.

## Cenários sugeridos ao spec
- Feliz: adicionar e excluir devolve o contador ao valor de antes (afirmar o delta, não o valor absoluto, se a lista é compartilhada).
- Persistência: recarregar e consultar `/api/tarefas`.
- Borda: título vazio não cria tarefa.

## Não verificado
- Comportamento com mais de um item na lista.
- Papel sem permissão (a funcionalidade não tem papéis no demo).
````

## O que a nota mostra

- O efeito foi verificado com um comando de leitura (`find`) sobre o contador, e não só pelo item sumir da lista.
- O ruído do console está separado do achado.
- A evidência tem caminho absoluto, e o código gerado vem junto, sem asserção.
- O veredito é provisório. Quem muda o status da matriz é `evidence-report`.
