# Causas de teste instável, correções e comandos

Apoio da skill `flaky-triage`. Leia quando precisar de comandos de repetição por runner, de código antes/depois por causa, de método para achar o teste que polui o estado ou da conta estatística de quantas execuções bastam.

Rótulos: classificação em sete causas e valores iniciais vêm de V-37 (classe C, cruzada com V-21, V-24, V-19, A); asserção web-first, `page.route`, isolamento, projeto de setup e `describe.serial` são Verificados em V-19 e V-21; `vi.setSystemTime` e `unstubAll*` em V-25. Todo o resto (flags de repetição, `page.clock`, `-race`, plugins) é conhecimento estável, Inferido: confirme com `--help` e na documentação da versão instalada.

## Sumário

- [Comandos de repetição e de preservação da falha](#comandos-de-repetição-e-de-preservação-da-falha)
- [As sete causas com código](#as-sete-causas-com-código)
- [Achar o teste que polui o estado](#achar-o-teste-que-polui-o-estado)
- [Quantas execuções bastam](#quantas-execuções-bastam)
- [Quarentena sem perder o sinal](#quarentena-sem-perder-o-sinal)

## Comandos de repetição e de preservação da falha

| Runner | Repetir | Isolar variáveis | Preservar a falha |
| --- | --- | --- | --- |
| Playwright | `npx playwright test x.spec.ts --repeat-each=30 --retries=0` | `--workers=1`; `--project=chromium` | `--trace on` ou `retain-on-failure`; `npx playwright show-trace trace.zip` |
| pytest | laço de shell (abaixo); plugin de terceiros `pytest-repeat` (`--count=30`) só se o usuário aprovar instalar | `-p no:randomly` desliga ordem aleatória; `--randomly-seed=1234` reproduz (plugin `pytest-randomly`) | `-x --tb=long -rA > log.txt 2>&1` |
| Vitest | laço de shell | `--no-file-parallelism`; `--sequence.shuffle` para testar ordem; `--retry=0` | `--reporter=verbose` e log em arquivo |
| Jest | laço de shell | `--runInBand` (`-i`); `--randomize` em versões recentes | `--verbose > log.txt 2>&1` |
| Go | `go test -count=30 -run TestX ./pkg` | `-p 1`; `-shuffle=on`; `-cpu 1,2,4` | `-race` para corrida de dados; guarde a saída `-v` |
| Cypress | laço de shell por spec | `retries: 0` na configuração durante a medição | vídeo e screenshots do `cypress run` |

Laço de shell para qualquer runner (substitua `<cmd>`):

```bash
fail=0; for i in $(seq 1 50); do <cmd> >"run-$i.log" 2>&1 || fail=$((fail+1)); done; echo "falhas: $fail/50"
```

PowerShell:

```powershell
$fail = 0; 1..50 | ForEach-Object { & <cmd> *> "run-$_.log"; if ($LASTEXITCODE -ne 0) { $fail++ } }; "falhas: $fail/50"
```

Guarde só os logs das execuções que falharam; apague os demais. Reproduzir as condições do CI: mesmo número de workers (`--workers=N`), CPU limitada (`docker run --cpus=1 ...`), sem cache, mesma imagem. Flake que só aparece com carga costuma ser timing; flake que some com `--workers=1` costuma ser dado ou estado compartilhado.

## As sete causas com código

### 1. Timing e espera

Antes (espera fixa e asserção que não espera):

```ts
await page.getByRole('button', { name: 'Finalizar' }).click();
await page.waitForTimeout(3000);
expect(await page.locator('.ok').isVisible()).toBe(true);
```

Depois (asserção web-first, que espera até o prazo):

```ts
await page.getByRole('button', { name: 'Finalizar' }).click();
await expect(page.getByRole('status')).toHaveText('Pedido criado');
```

Fora do navegador, espere por condição com prazo e diagnóstico; ao expirar, falhe mostrando o último estado, nunca devolva sucesso porque o prazo acabou:

```python
import time

def esperar(condicao, prazo=5.0, passo=0.05):
    fim = time.monotonic() + prazo
    ultimo = None
    while time.monotonic() < fim:
        ultimo = condicao()
        if ultimo:
            return ultimo
        time.sleep(passo)
    raise AssertionError(f"condição não satisfeita em {prazo}s; último valor: {ultimo!r}")
```

### 2. Dados compartilhados

Sintoma: erro de unicidade (409, `duplicate key`) em paralelo; falha dependente do que outro teste deixou. Correção: cada teste cria os próprios dados com sufixo único e limpa em `beforeEach` (V-24: limpar em `after` pode nunca rodar). Em banco compartilhado, use schema ou tenant por worker. Exemplo:

```ts
test('aplica cupom', async ({ page }, testInfo) => {
  const email = `qa+${testInfo.workerIndex}-${Date.now()}@exemplo.test`;
  // cria o usuário por API com esse e-mail e segue o teste
});
```

### 3. Dependência de ordem

Antes: `let pedidoId` global preenchido pelo teste 1 e lido pelo teste 2. Depois: o teste 2 cria o pedido por API em seu `beforeEach` ou fixture. `test.describe.serial` agrupa testes realmente dependentes e para na primeira falha, mas a documentação recomenda isolamento (V-21): use só quando o isolamento for inviável e documente por quê.

### 4. Ambiente

Diferenças de fuso, locale, versão de navegador, fontes, CPU e memória. Fixe o que o teste assume:

```ts
use: { locale: 'pt-BR', timezoneId: 'America/Sao_Paulo' }
```

Versões travadas por lockfile; navegadores instalados pela versão do Playwright do projeto; mesma imagem de CI e local quando possível.

### 5. Relógio e tempo

Falhas perto da meia-noite, no fim do mês, em horário de verão histórico. Injete o relógio. Vitest: `vi.useFakeTimers(); vi.setSystemTime(new Date('2026-03-10T10:00:00-03:00'));` e `vi.useRealTimers()` ao final, porque `setSystemTime` não se desfaz sozinho (V-25). Playwright (versões recentes): `await page.clock.install({ time: new Date('2026-03-10T10:00:00-03:00') })`. Um relógio falso local não avança o relógio do banco nem de outro processo: se a regra de expiração roda no banco, controle o tempo lá (parâmetro, função injetada) ou teste a regra por dado, não por espera.

### 6. Renderização visual

Diferença de pixels por animação, fonte ou antialiasing. Desligue animações, fixe fontes, mascare regiões dinâmicas e gere as imagens de referência na mesma imagem do CI:

```ts
await expect(page).toHaveScreenshot('painel.png', { animations: 'disabled', mask: [page.getByTestId('hora')] });
```

Imagens geradas em outro sistema operacional divergem; trate a regressão visual como suíte à parte (fonte A para o tema ausente: lacuna).

### 7. Serviço externo

Terceiros lentos ou fora do ar. Stub no teste, registrado **antes** da ação que dispara a requisição (V-19):

```ts
await page.route('**/api/frete*', route =>
  route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ valor: 1500 }) }));
await page.getByRole('button', { name: 'Calcular frete' }).click();
```

O contrato com o terceiro se verifica em outro lugar (Pact, sandbox do parceiro); o E2E não deve depender dele.

## Achar o teste que polui o estado

Quando o teste só falha dentro da suíte (causa 3 ou 2 disfarçada):

1. Liste a ordem real: `pytest --collect-only -q` ou o relatório detalhado (verbose) do runner.
2. Rode o teste "vítima" sozinho: se passa, há poluidor antes dele.
3. Busca binária: rode a metade dos testes anteriores + a vítima; se falha, o poluidor está nessa metade; repita até restar um. Em runners com ordem aleatória, fixe a seed da falha original antes (`--randomly-seed`, `--sequence.seed`; confira o nome da flag).
4. Confirme com o par poluidor + vítima isolados e corrija a limpeza (fixture sem teardown, variável global, `vi.stubGlobal` sem `unstubAll`, mock sem restaurar, arquivo temporário, linha no banco).
5. Registre o par no relatório; ele vira o teste de regressão da correção.

## Quantas execuções bastam

Cálculo (Verificado por conta): com zero falhas em n execuções, o limite superior de 95% de confiança para a taxa de falha é 1 - 0,05^(1/n), cerca de 3/n (regra dos três).

| Execuções limpas | Taxa de falha que ainda é compatível com 95% de confiança |
| --- | --- |
| 20 | até 13,9% |
| 50 | até 5,8% |
| 100 | até 3,0% |
| 300 | até 1,0% |

Inverso: chance de um teste flaky passar n execuções seguidas por sorte.

| Taxa real de falha | 50 execuções limpas | 100 execuções limpas |
| --- | --- | --- |
| 10% | 0,5% | cerca de 0% |
| 5% | 7,7% | 0,6% |
| 2% | 36,4% | 13,3% |
| 1% | 60,5% | 36,6% |

Consequência: 50 execuções é um bom valor inicial para flake de dezenas por cento e fraco para flake raro. Para falha rara, aumente as execuções ou, melhor, reproduza a condição causal (carga, ordem, relógio) em vez de esperar sorte.

## Quarentena sem perder o sinal

Confirme com o usuário antes de editar CI ou marcar skip. Em vez de `skip` puro (o teste some do radar), marque com tag e deixe um job separado rodando:

```ts
test('aplica cupom @quarantine', async ({ page }) => { /* ... */ });
// gate do PR:   npx playwright test --grep-invert @quarantine
// job separado: npx playwright test --grep @quarantine
```

Em pytest, `@pytest.mark.quarantine` e `-m "not quarantine"` no gate. Todo teste em quarentena leva comentário rastreável: ticket, dono, data de entrada e prazo (valor inicial: 14 dias). Prazo vencido sem correção força a decisão: corrigir, apagar com justificativa ou aceitar o risco por escrito. Acompanhe a fração em quarentena (valor inicial: alerta acima de cerca de 5%); todos esses números são ajustáveis (K10).
