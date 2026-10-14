// spec: F-07 Excluir tarefa atualiza lista e contador      matriz: FUNCIONALIDADES.md#F-07
// seed: e2e/fixtures.ts · exploração: funcional/exploracao/F-07.md · bug conhecido: BUG-01 (no sistema-demo, X-14)
//
// Template do plugin qa-playwright. Exemplo com o sistema-demo de tarefas (dados sintéticos). Troque rota, rótulos e
// efeito pelos da sua funcionalidade. Renomeie para e2e/F-NN-<slug>.spec.ts. Um arquivo por funcionalidade.
// Regras: ID F-NN no início do título do describe; @ui ou @api no título (X-16); locator por papel ou rótulo (V-27);
// asserção do EFEITO e não só da presença (X-14); sem waitForTimeout, networkidle nem force: true (V-30, V-32).
import { test, expect } from './fixtures';

test.describe('F-07 Excluir tarefa @ui', () => {
  test('feliz: excluir remove o item, ajusta o contador e persiste', async ({ page, app, request }, testInfo) => {
    const nome = `Comprar pão ${testInfo.testId.slice(0, 6)}`;           // dado único por teste (V-33)
    const pendentes = async () => Number((await page.getByText(/pendente\(s\)/).innerText()).match(/\d+/)![0]);

    await app.abrir('/tarefas');
    // Contador global: afirme o delta, não o valor absoluto. Se outro spec o altera em paralelo (inclusive as cópias
    // deste teste no gate: --repeat-each=5 e --workers=2 rodam em paralelo), proteja o recurso com `lock` (V-34)
    // ou use uma conta própria por teste.
    const antes = await pendentes();

    // Passo: adicionar
    await page.getByRole('textbox', { name: 'Nova tarefa' }).fill(nome);
    await page.getByRole('button', { name: 'Adicionar' }).click();
    const item = page.getByRole('listitem').filter({ hasText: nome });   // por conteúdo, nunca por índice (V-28)
    await expect(item).toHaveCount(1);
    await expect.poll(pendentes, { message: 'contador após adicionar' }).toBe(antes + 1);

    // Passo: excluir. O EFEITO é o contador voltar ao valor anterior, não só o item sumir (X-14)
    await item.getByRole('button', { name: 'Excluir' }).click();
    await expect(item).toHaveCount(0);
    await expect.poll(pendentes, { message: 'contador após excluir' }).toBe(antes);

    // Persistência: recarregar e conferir pela API (ação na UI, verificação via API: V-51)
    await page.reload();
    await expect(item).toHaveCount(0);
    expect(JSON.stringify(await (await request.get('/api/tarefas')).json())).not.toContain(nome);
  });

  test('borda: título vazio não cria tarefa', async ({ page, app }) => {
    await app.abrir('/tarefas');
    const antes = await page.getByRole('listitem').count();              // lista global no sistema-demo: mesma ressalva do `lock`
    await page.getByRole('button', { name: 'Adicionar' }).click();
    await expect(page.getByRole('alert')).toBeVisible();                 // texto exato: confira na fonte de verdade do esperado
    await expect(page.getByRole('listitem')).toHaveCount(antes);
  });
});

// Funcionalidade de API: use @api no título e a fixture `request`, sem `page`.
// test.describe('F-08 Listar tarefas @api', () => { test('feliz: GET devolve 200 e a lista', async ({ request }) => { ... }); });
//
// Rodar uma funcionalidade:  npx playwright test --grep "F-07"      ou o filtro de arquivo (Git Bash):  npx playwright test F-07-
// Gate (verificado, X-24):   --repeat-each=5 --retries=0   e   --shuffle --workers=2 --retries=0
// Rodar por tipo:            npx playwright test --grep "@ui|@api"  (sem barra invertida; `--grep-invert "@ui"` exclui)
// Nunca use `--%` com npx (X-16). Com mais de 99 funcionalidades, use IDs de três dígitos desde o início:
// o filtro é por substring e "F-07" casaria "F-070".
// O primeiro teste falha enquanto o bug do contador existir, e isso é o resultado correto (X-14): o spec fica vermelho,
// em commit próprio, ligado ao BUG-NN. Não troque o esperado pelo observado.
