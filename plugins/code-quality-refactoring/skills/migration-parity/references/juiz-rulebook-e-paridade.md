# Moldes: juiz, rulebook, fila, paridade e upgrade major

Sumário: 1 Desenhar o juiz · 2 Provar que o juiz reprova · 3 Rulebook · 4 Fila em disco · 5 Piloto e lotes · 6 Veredito por módulo · 7 Upgrade de versão major · 8 Atribuições.

Rótulos: Inferido = prática comum ou destilação das fontes; Suposição = escolha ajustável; Verificado = confirmado na fonte citada. Os exemplos são ilustrativos (nada foi executado); substitua comandos e nomes pelos do seu projeto.

## 1. Desenhar o juiz

O juiz é o conjunto de comandos que decide "igual ou diferente". Ele deve ser executável no original e no novo e produzir um veredito que não dependa do modelo.

| Camada | Exemplo (JavaScript para TypeScript) | Observação |
| --- | --- | --- |
| Compila | `npm run typecheck` (ou o `tsc` já instalado no projeto) | Use o binário do projeto; `npx` de pacote não instalado baixa código de terceiros |
| Suíte | `npm test` nos dois lados | Compare não só verde/vermelho: número de testes e lista de nomes iguais |
| Saídas | Script que roda os mesmos cenários e compara a saída (JSON normalizado) | Normalize campos voláteis (timestamps, ids) |
| Smoke | Subir o serviço e chamar 2 ou 3 rotas | Só quando o ambiente existir |
| Comportamento implícito | Teste de caracterização para o que não tem teste (V-36) | Entradas de borda e erro |

Regra: sem suíte, construa uma a partir do original antes de converter qualquer arquivo. Sem possibilidade de rodar o antigo, o teto é PARCIALMENTE PROVADO (V-15).

## 2. Provar que o juiz reprova

1. Rode o juiz no original: deve passar. Cole a saída.
2. Em uma cópia (nunca no legado), quebre de propósito: inverta uma condição, remova um campo de retorno, troque um tipo. Escolha ao menos uma quebra por camada.
3. Rode o juiz na cópia quebrada: deve falhar na camada esperada. Cole a saída.
4. Se o juiz continuou verde, ele não protege essa camada: reforce antes de seguir.

Exemplo de registro:

```text
Juiz v1
- Compila: `npm run typecheck`  -> original: exit 0 | cópia quebrada (retorno string no lugar de number): exit 2
- Suíte:   `npm test`           -> original: 112 testes, 0 falhas | cópia quebrada (condição invertida em preco.js): 3 falhas
- Camada não coberta: formatação de datas (sem teste). Ação: teste de caracterização antes do módulo `datas`.
```

## 3. Rulebook

Equivalências origem -> destino, escritas para serem aplicadas por qualquer agente, com a razão e a verificação. Ordem: rulebook primeiro, depois o inventário de comportamento implícito (V-14).

| ID | Origem | Destino | Razão | Verificação |
| --- | --- | --- | --- | --- |
| R-01 | `const x = require("m")` | `import x from "m"` | ESM do projeto | `typecheck` |
| R-02 | `module.exports = f` | `export default f` ou `export { f }` (decidir uma) | Mantém o contrato dos importadores | busca por `require(".../arquivo")` sem usos restantes |
| R-03 | Parâmetro sem tipo | Tipo explícito; `unknown` quando incerto, nunca `any` sem comentário | Evitar perder a checagem | `typecheck` estrito |
| R-04 | `// @ts-ignore` | Proibido sem justificativa na linha | Supressão esconde erro | `grep` no lote |
| R-05 | `null`/`undefined` sem guarda | Tratar explicitamente (strict null checks) | Defaults mudam entre JS e TS | testes de borda |

Inventário de comportamento implícito (exemplos): efeitos de import (registro de rotas ao importar), ordem de inicialização, defaults de parâmetros, conversões automáticas de tipo, arredondamento, ordem de iteração de objetos e mapas, tratamento de fuso horário. Cada item vira um teste ou uma regra.

Erro repetido em mais de um arquivo vai para o rulebook (nova regra R-nn); o lote é regenerado. Remendar arquivo por arquivo repete o erro no próximo lote.

Modelo completo: `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/migration-rulebook.md`.

## 4. Fila em disco

Arquivo `migration/migration-queue.md` (peça aprovação para criar a pasta). Estados: `pendente`, `em_curso`, `feito`, `falhou`. Um arquivo só é `feito` quando a saída existe e o juiz passa; isso torna o trabalho retomável após interrupção.

```markdown
| Arquivo origem | Módulo | Lote | Estado | Juiz | Observação |
| --- | --- | --- | --- | --- | --- |
| src/utils/money.js | utils | 1 | feito | typecheck+teste ok | R-03 aplicada |
| src/utils/dates.js | utils | 1 | falhou | typecheck: TS2345 | regra faltando para Date nullable; ver R-06 |
| src/api/orders.js | api | 2 | pendente | | depende de utils |
```

Ordem dos lotes: folhas do grafo de dependências primeiro; módulo que todos importam, por último ou isolado por Parallel Change.

## 5. Piloto e lotes

- Piloto: 3 a 5 arquivos representativos (um simples, um com dependências, um com comportamento implícito). A saída é descartada; o que fica é o rulebook ajustado.
- Lote: tamanho que o revisor humano consegue ler (Suposição: 10 a 20 arquivos ou ~400 linhas de diff). Lotes pequenos tornam a causa de uma falha localizável.
- Modelo menor para o volume e maior para revisão e regras (prática do relato V-14; Suposição para a escolha de modelos: meça custo e taxa de erro).
- Revisão adversarial: o revisor recebe o diff e o rulebook e deve citar a regra violada. Dois revisores independentes; o terceiro desempata (V-14).

## 6. Veredito por módulo

Critérios na skill. Exemplo preenchido:

| Módulo | Cenários rodados dos dois lados | Resultado | Veredito | Pendências |
| --- | --- | --- | --- | --- |
| utils/money | 14 testes + 6 cenários de arredondamento, original e novo | Saídas iguais | PROVADO | nenhuma |
| utils/dates | 9 testes; original não roda mais (dependência removida) | Novo verde; sem comparação | PARCIALMENTE PROVADO | sem referência do original |
| api/orders | sem testes; só typecheck | Compila | NÃO PROVADO | caracterizar antes de declarar migrado |

## 7. Upgrade de versão major

Sequência (V-40 e V-14, redação própria):

1. Confirme as versões atuais e de destino no manifesto e no lockfile.
2. Leia o guia oficial de migração e o changelog do destino; liste as mudanças que quebram e o que cada uma exige. Cite URL e data de consulta.
3. `Grep` no repositório pelas APIs afetadas; estime o raio.
4. Rode a suíte antes (linha de base) e cole.
5. Receita determinística oficial do mantenedor primeiro, se existir (codemod do projeto; OpenRewrite para Java, licença Não verificada aqui; Dependabot para PRs de versão, com espera padrão de 3 dias após release, não vale para segurança, V-40). Instalar só com pedido.
6. Atualize uma major por vez, em lotes pequenos, suíte após cada lote.
7. Trate avisos de depreciação como pendência com data, não como ruído.
8. API pública que mudou: Parallel Change.
9. Rode a suíte depois, o build e o smoke; cole.

## 8. Atribuições

- Anthropic, "How Anthropic runs large-scale code migrations with Claude Code" (claude.com/blog/ai-code-migration, 2026-07-16): juiz, rulebook, piloto, fila, desempate. Destilado.
- `anthropics/claude-plugins-official`, plugin `code-modernization` (Apache-2.0): tipos uplift, transform e reimagine e veredito por módulo. Destilado; hooks e telemetria não usados.
- Martin Fowler: Strangler Fig (22/08/2024) e Parallel Change (13/05/2014). Destilado.
- OpenRewrite e Dependabot: documentação oficial lida em 2026-10-10 apenas na página de entrada; detalhes por versão devem ser conferidos.
