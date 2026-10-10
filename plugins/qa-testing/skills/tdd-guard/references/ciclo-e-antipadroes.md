# Ciclo test-first, comandos e anti-padrões

Apoio da skill `tdd-guard`. Leia quando precisar de um ciclo completo como modelo, do comando que roda um teste só em cada stack, ou de exemplos antes/depois dos anti-padrões.

## Sumário

- [Ciclo completo: frete por região](#ciclo-completo-frete-por-região)
- [Mutation check na prática](#mutation-check-na-prática)
- [Classificar o primeiro vermelho](#classificar-o-primeiro-vermelho)
- [Comandos para rodar um teste só](#comandos-para-rodar-um-teste-só)
- [Anti-padrões: antes e depois](#anti-padrões-antes-e-depois)
- [Tabela de racionalizações](#tabela-de-racionalizações)
- [Legado e caracterização](#legado-e-caracterização)

## Ciclo completo: frete por região

Regra dada pelo usuário: `calcular_frete(subtotal_centavos, regiao)`; "sul" cobra 1500, "norte" cobra 3000; subtotal a partir de 19900 (R$ 199,00, antes de descontos) tem frete grátis; região desconhecida levanta `ValueError`. Python, `unittest` da biblioteca padrão (o mesmo ciclo vale em pytest). As saídas abaixo foram executadas ao preparar esta referência (Python 3.14, 2026-10-10); a sua variará com runner e versão.

Perguntas de oráculo antes de começar (viram suposições declaradas se ninguém responder): o limite de 19900 é inclusivo? O subtotal é antes ou depois do cupom? Região desconhecida com subtotal acima do limite deve levantar erro ou dar frete grátis? Suposição adotada aqui: o limite é inclusivo e a região é validada antes do limite.

Fatia 1 (sul abaixo do limite). Stub mínimo para o import funcionar: `def calcular_frete(subtotal_centavos, regiao): return None`.

```python
def test_sul_abaixo_do_limite_cobra_1500(self):
    self.assertEqual(calcular_frete(10000, "sul"), 1500)
```

```text
FAIL: test_sul_abaixo_do_limite_cobra_1500 ...
AssertionError: None != 1500
FAILED (failures=1)
```

Vermelho pelo motivo certo (comportamento ausente). Implementação mínima: `return 1500`. Resultado: `Ran 1 test ... OK`.

Fatia 2 (norte). O teste `calcular_frete(10000, "norte") == 3000` falha com `AssertionError: 1500 != 3000`. Isso mostra que a constante da fatia 1 era provisória. Implementação: dicionário `TARIFAS = {"sul": 1500, "norte": 3000}` e `return TARIFAS[regiao]`. Verde, `Ran 2 tests ... OK`.

Fatia 3 (limite, três valores no ponto de risco).

```python
def test_19900_tem_frete_gratis_e_19899_paga(self):
    self.assertEqual(calcular_frete(19900, "norte"), 0)
    self.assertEqual(calcular_frete(19899, "norte"), 3000)
```

```text
AssertionError: 3000 != 0
FAILED (failures=1)
```

Implementação: constante `LIMITE_FRETE_GRATIS = 19900` e `if subtotal_centavos >= LIMITE_FRETE_GRATIS: return 0` antes do retorno da tarifa. Verde, `Ran 3 tests ... OK`.

Fatia 4 (região desconhecida).

```python
def test_regiao_desconhecida_levanta_value_error(self):
    with self.assertRaises(ValueError):
        calcular_frete(10000, "leste")
```

```text
ERROR: test_regiao_desconhecida_levanta_value_error ...
KeyError: 'leste'
FAILED (errors=1)
```

O vermelho é válido: o comportamento (`ValueError`) não existe; o `KeyError` é o sintoma. Implementação final, com a validação antes do limite conforme a suposição:

```python
LIMITE_FRETE_GRATIS = 19900
TARIFAS = {"sul": 1500, "norte": 3000}


def calcular_frete(subtotal_centavos, regiao):
    if regiao not in TARIFAS:
        raise ValueError(f"região desconhecida: {regiao!r}")
    if subtotal_centavos >= LIMITE_FRETE_GRATIS:
        return 0
    return TARIFAS[regiao]
```

Verde: `Ran 4 tests ... OK`. Refatore só agora (renomear, extrair), com a suíte verde. Pendências para o relatório: tipos inválidos (`None`, float, negativo) e caixa da região ("Sul") dependem de decisão do PO; entram em "Não coberto".

Observação sobre o oráculo: os literais 1500, 3000, 0 e 19900 vêm da regra dada, não de outra chamada a `calcular_frete`.

## Mutation check na prática

Objetivo: provar que a suíte percebe uma mudança realista no código. Procedimento sem risco para o trabalho em andamento:

```bash
cp src/frete.py "$TMPDIR/frete.orig"            # copia fora do repositório
sed -i 's/>= LIMITE_FRETE_GRATIS/> LIMITE_FRETE_GRATIS/' src/frete.py   # mutação: >= vira >
python -m unittest 2>&1 | grep -E "^(FAIL|ERROR)|FAILED|Ran"
cp "$TMPDIR/frete.orig" src/frete.py            # restaura
diff "$TMPDIR/frete.orig" src/frete.py && echo restaurado
git diff --stat                                  # confere que só o esperado mudou
```

Resultado observado na preparação: `FAIL: test_19900_tem_frete_gratis_e_19899_paga` e `FAILED (failures=1)`, ou seja, a mutação foi morta. Se nenhum teste falhar, o mutante sobreviveu: o teste é fraco, falta o caso de borda ou a mudança é equivalente (V-15, Inferido para a triagem). Mutantes realistas: trocar comparador (`>=`/`>`), inverter condição, remover efeito (`save()`), trocar constante, retornar valor padrão. Em PowerShell use `Copy-Item` e `(Get-Content f) -replace ...` ou o Edit da sessão. Ferramentas automáticas (Stryker para JS/TS/.NET/Scala, mutmut para Python, PIT para Java) existem, são caras e se aplicam a módulos críticos; confira comandos na documentação da versão instalada (Não verificável aqui).

## Classificar o primeiro vermelho

| Saída | Veredito | Ação |
| --- | --- | --- |
| `AssertionError: None != 1500`, `expected 3000, got 1500` | motivo certo | seguir |
| `NotImplementedError` de stub, `KeyError`/`TypeError` que o teste espera substituir por outro erro | motivo certo (comportamento ausente) | seguir |
| `ImportError`, `ModuleNotFoundError`, `SyntaxError` | motivo errado | criar stub/arquivo e rodar de novo |
| `fixture 'x' not found`, erro de configuração, timeout de ambiente | motivo errado | consertar o ambiente do teste |
| Verde de primeira | suspeito | provar que o teste falha (mutação ou stub que devolve valor neutro) |
| Falha em teste antigo | regressão ou acoplamento | parar e decidir (seção "Quando um teste quebra" do SKILL) |

## Comandos para rodar um teste só

Confirme com `--help` na versão instalada (conhecimento estável, Inferido).

| Stack | Um teste | Repetir/ver detalhes |
| --- | --- | --- |
| pytest | `pytest tests/test_frete.py::test_sul -x` | `-x` para na primeira falha; `-vv` mostra diff |
| unittest | `python -m unittest tests.test_frete.TestFrete.test_sul -v` | `-v` lista cada teste |
| Vitest | `npx vitest run -t "sul abaixo do limite"` | `--reporter=verbose` |
| Jest | `npx jest -t "sul abaixo do limite"` | `--verbose` |
| Go | `go test ./... -run TestFreteSul -count=1 -v` | `-count=1` evita cache |
| JUnit/Maven | `mvn -Dtest=FreteTest#sul test` | |
| .NET | `dotnet test --filter "FullyQualifiedName~Frete"` | |
| Rust | `cargo test frete::tests::sul -- --nocapture` | |

## Anti-padrões: antes e depois

Fontes: V-31, V-33 (Verificado); exemplos de código são redação própria.

**Acoplado à implementação.**

```python
# antes: verifica o roteiro interno
def test_cupom_chama_repositorio():
    repo = Mock()
    aplicar_cupom(pedido, "DEZ10", repo)
    repo.buscar.assert_called_once_with("DEZ10")

# depois: verifica o efeito observável
def test_cupom_dez_reduz_total_em_10_por_cento():
    pedido = pedido_com(total_centavos=10000)
    aplicar_cupom(pedido, "DEZ10", repo_em_memoria(cupons={"DEZ10": 10}))
    assert pedido.total_centavos == 9000
```

**Tautológico.**

```ts
// antes: o esperado usa a mesma fórmula do código
expect(total(100, 10)).toBe(100 - (100 * 10) / 100);
// depois: literal calculado à mão
expect(total(100, 10)).toBe(90);
```

**Asserção fraca.**

```ts
// antes: passa com qualquer total
expect(resultado).not.toBeNull();
// depois: distingue preço correto de preço dez vezes maior
expect(resultado).toEqual({ subtotal: 25000, desconto: 2500, total: 22500 });
```

**Fatiamento horizontal.** Escrever os 12 testes da regra, depois todo o código. Sintoma: o primeiro `git diff` já traz 300 linhas de teste e nenhuma de produção. Alternativa: uma fatia por vez, cada uma com vermelho e verde colados.

**Snapshot cego.** `toMatchSnapshot()` regravado com `-u` sem leitura do diff. Alternativa: revisar o diff semântico e assertar os campos que importam (preço, status, permissão), mascarando só timestamps e IDs.

**Mock da própria unidade.** Mockar `calcular_frete` num teste de `calcular_frete`. Alternativa: dublê só em fronteira (rede, banco, fila, relógio).

**Teste sem relação com o nome.** `test_valida_cpf` que só confere que a função não lança. Alternativa: nomeie o comportamento e a quebra que pega ("recusa CPF com dígito verificador errado").

## Tabela de racionalizações

Tabela de racionalizações (redação própria): a desculpa comum, a resposta e o sinal de que é hora de recomeçar a fatia.

| Desculpa | Resposta | Sinal para recomeçar |
| --- | --- | --- |
| "É simples demais para testar primeiro" | a regra de limite é onde nascem os defeitos; a fatia leva dois minutos | você já escreveu a função inteira |
| "Escrevo o teste depois, o resultado é o mesmo" | o teste escrito depois descreve o código, não o requisito | o teste passa de primeira |
| "Já testei manualmente" | teste manual não protege contra a próxima mudança | ninguém consegue repetir o passo a passo |
| "Vou escrever todos os testes agora" | a imaginação substitui o feedback | mais de um teste novo sem código entre eles |
| "O teste falhou por import, mas conta como vermelho" | não demonstra que o comportamento é detectado | o erro cita `ImportError` |
| "Vou ajustar a asserção para passar" | pode estar escondendo regressão | você abriu o arquivo de teste existente para relaxar |

## Legado e caracterização

Em código sem especificação, antes de alterar: escreva testes de caracterização que registram o comportamento atual (declare-os como tal: já passam), marque os comportamentos suspeitos como "não aprovado como regra" e só então faça a mudança com ciclo normal. Para snapshots, mascare apenas dados voláteis. Detalhes e dublês em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/unitarios-e-integracao.md` (seção TDD, legado e manutenção). Fonte do conceito: brain-of-agent (conteúdo próprio, MIT), adaptado.
