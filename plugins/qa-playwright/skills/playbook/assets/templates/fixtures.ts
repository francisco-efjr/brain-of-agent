// Template do plugin qa-playwright: estado inicial único dos specs (substitui o seed.spec.ts do init-agents; V-09, V-35).
// Copie para e2e/fixtures.ts. Sem asserção aqui: a fixture só prepara o ambiente.
// Acrescente fixtures de papel, de dados criados por API e de limpeza quando a matriz pedir.
import { test as base, expect } from '@playwright/test';

type App = {
  abrir: (rota: string) => Promise<void>;
};

export const test = base.extend<{ app: App }>({
  app: async ({ page }, use) => {
    // Antes de use() é o setup; depois de use() é o teardown (V-35).
    await use({
      abrir: async (rota) => {
        await page.goto(rota);
      },
    });
  },
});

export { expect };

// Exemplo de extensão (descomente e adapte): dado criado pelo próprio teste e limpo por id capturado (V-33, V-51).
// export const testComTarefa = test.extend<{ tarefa: { id: string; nome: string } }>({
//   tarefa: async ({ request }, use, testInfo) => {
//     const nome = `Tarefa ${testInfo.testId.slice(-8)}`;
//     const criada = await request.post('/api/tarefas', { data: { nome } });
//     const { id } = await criada.json();
//     await use({ id, nome });
//     await request.delete(`/api/tarefas/${id}`);
//   },
// });
