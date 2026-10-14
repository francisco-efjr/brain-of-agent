# Exemplo de spec comentado: F-07 Excluir tarefa

Spec do sistema-demo de tarefas (dados sintéticos), com a regra que cada trecho cumpre. O contador que não zera após excluir vem de X-14: o primeiro teste **deve falhar** enquanto o bug existir, e isso é o resultado correto. Os códigos V-NN apontam para a pesquisa do plugin.

```ts
// spec: F-07 Excluir tarefa atualiza lista e contador      matriz: FUNCIONALIDADES.md#F-07
// seed: e2e/fixtures.ts · exploração: funcional/exploracao/F-07.md · bug conhecido: BUG-01
import { test, expect } from './fixtures';

test.describe('F-07 Excluir tarefa @ui', () => {
  test('feliz: excluir remove o item, ajusta o contador e persiste', async ({ page, app, request }, testInfo) => {
    const nome = `Comprar pão ${testInfo.testId.slice(0, 6)}`;
    const pendentes = async () => Number((await page.getByText(/pendente\(s\)/).innerText()).match(/\d+/)![0]);
    await app.abrir('/tarefas');
    const antes = await pendentes();
    // Passo: adicionar
    await page.getByRole('textbox', { name: 'Nova tarefa' }).fill(nome);
    await page.getByRole('button', { name: 'Adicionar' }).click();
    const item = page.getByRole('listitem').filter({ hasText: nome });
    await expect(item).toHaveCount(1);
    await expect.poll(pendentes, { message: 'contador após adicionar' }).toBe(antes + 1);
    // Passo: excluir. O EFEITO é o contador voltar, não só o item sumir
    await item.getByRole('button', { name: 'Excluir' }).click();
    await expect(item).toHaveCount(0);
    await expect.poll(pendentes, { message: 'contador após excluir' }).toBe(antes);
    // Persistência: recarregar e conferir pela API
    await page.reload();
    await expect(item).toHaveCount(0);
    expect(JSON.stringify(await (await request.get('/api/tarefas')).json())).not.toContain(nome);
  });

  test('borda: título vazio não cria tarefa', async ({ page, app }) => {
    await app.abrir('/tarefas');
    const antes = await page.getByRole('listitem').count();
    await page.getByRole('button', { name: 'Adicionar' }).click();
    await expect(page.getByRole('alert')).toBeVisible();   // texto exato: conferir na fonte de verdade
    await expect(page.getByRole('listitem')).toHaveCount(antes);
  });
});
```

## Mapa: trecho e regra

| Trecho | Regra cumprida | Origem |
| --- | --- | --- |
| Cabeçalho `// spec:` e `// seed:` | rastro até a matriz e ao estado inicial | V-08 |
| `F-07` no `describe` e `@ui` no título | `--grep "F-07"` roda uma funcionalidade; `--grep-invert "@ui"` filtra por tipo | X-16 |
| `testInfo.testId.slice(0, 6)` no nome | dado único por teste: nenhum teste depende do que outro criou | V-33, V-34 |
| `getByRole('textbox', { name })` | locator por papel e nome acessível | V-27 |
| `filter({ hasText: nome })` | item de lista por conteúdo, não por índice | V-28 |
| `await expect(item).toHaveCount(1)` | asserção web-first com auto-retry | V-31 |
| `expect.poll(pendentes, { message })` | condição que demora, com mensagem de diagnóstico | V-31 |
| `antes` e `antes + 1` | afirma o delta: se outro spec mexer no contador, o valor absoluto engana | V-34 |
| `toBe(antes)` depois de excluir | asserção do **efeito** (contador), não só da presença | X-14 |
| `page.reload()` e `request.get` | persistência: ação na UI, verificação via API | V-51 |
| `getByRole('alert')` com comentário | o texto exato do aviso não tem fonte: não invente | PR-03 |
| ausência de `waitForTimeout`, `networkidle`, `force` | espera por estado observável | V-30, V-32 |

## Quando o spec falha por bug

Neste exemplo, o `expect.poll(pendentes ...).toBe(antes)` após excluir falha enquanto o contador não zera (X-14; `trace requests` mostrou `DELETE 200`, o backend excluiu, X-20). O spec **não muda**. O caminho é `failure-triage`, que abre `BUG-01`; o spec vermelho vai para um commit próprio (`test(e2e): F-07 reproduz BUG-01`).

Se o usuário decidir não corrigir nesta rodada, a opção explícita é marcar o teste como falha esperada e anotar o bug:

```ts
test('feliz: excluir remove o item, ajusta o contador e persiste',
  { annotation: { type: 'issue', description: 'BUG-01' } },
  async ({ page, app, request }, testInfo) => {
    test.fail();   // só com decisão registrada do usuário; o teste ainda roda e exige que falhe
    // ... mesmo corpo de antes, sem afrouxar nenhuma asserção
  });
```

`test.fail()` roda o teste e exige que ele falhe: quando o bug for corrigido, o teste passa a falhar e avisa que a marca deve sair. `test.fixme` não roda e esconde a regressão: não use sem decisão registrada.

## Tabela do gate (modelo, valores a preencher)

| Comando | Execuções | Falhas | Resultado |
| --- | --- | --- | --- |
| `--grep "F-07" --repeat-each=5 --retries=0` | 5 por teste | `<n>` | `<passou ou falhou>` |
| `--grep "F-07" --shuffle --workers=2 --retries=0` | 1 | `<n>` | `<passou ou falhou>` |

Preencha com a saída real. Para um spec que reproduz o bug, o resultado esperado do gate é falha 5/5 no teste feliz (determinística), e isso aponta para a triagem, não para mais repetição. Foi o que o smoke do orquestrador obteve no sistema-demo (X-24): o teste do efeito falhou 5/5, a borda passou 5/5 e o `results.json` trouxe `stats` = `{expected: 5, unexpected: 5, flaky: 0, skipped: 0}`.
