# Modernização de legado, migração e upgrades

Sumário: 1 Quando usar e quando não · 2 Tipos: uplift, transform, reimagine · 3 Juiz primeiro · 4 Rulebook, mapa e inventário · 5 Piloto, lotes e fila em disco · 6 Revisão adversarial e desempate · 7 Veredito de paridade · 8 Strangler Fig · 9 Parallel Change · 10 Receitas determinísticas e atualização automática · 11 Upgrade de dependência ou framework · 12 Legado somente leitura · 13 Exemplo: JS para TypeScript · 14 Gotchas

Fontes: V-14 (relato de migração da Anthropic, 2026-07-16; caso sem números), V-15 (`code-modernization`, Apache-2.0; hooks e telemetria nunca entram), V-21 (Strangler Fig), V-37 (Parallel Change), V-40 (OpenRewrite, Dependabot), V-36 (caracterização), V-13 (`/batch`). Skill que conduz o fluxo: `migration-parity`, só por comando (`/code-quality-refactoring:migration-parity`).

## 1. Quando usar e quando não

| Situação | Caminho |
| --- | --- |
| Bump de patch/minor, sem breaking change anunciado | Direto: ler changelog, atualizar, rodar a suíte antes e depois, colar saídas |
| Major de dependência, troca de framework ou linguagem, mudança que toca muitos arquivos | `migration-parity` |
| Repositório pequeno | Um juiz e um lote bastam (V-14) |
| Troca de API pública ou esquema | Parallel Change (seção 9) |
| Sistema vivo grande | Strangler Fig (seção 8) |

## 2. Tipos (V-15)

- **Uplift**: mesma tecnologia, versão nova (ex.: major de framework). Padrão.
- **Transform**: outra tecnologia, módulo a módulo, comparando entradas iguais (ex.: JS para TypeScript, Java para Kotlin).
- **Reimagine**: nova arquitetura a partir de uma spec extraída do legado. Só com spec extraída e plano aprovado; nunca o padrão.

## 3. Juiz primeiro (V-14)

O juiz é o comando (ou conjunto) que roda contra o original e contra o novo e dá o mesmo veredito para o mesmo critério. Construa antes de migrar e **prove que ele falha em código quebrado de propósito** (injete um erro conhecido e veja o juiz reprovar). Sem suíte, construa uma a partir do original com testes de caracterização (V-36).

Exemplos de juiz por tipo de migração:
- Upgrade de framework: build + suíte existente + testes de contrato nas fronteiras.
- JS para TS: `tsc --noEmit` sem erros + a mesma suíte jest passando + comparação de saída de funções puras nos dois lados.
- Troca de biblioteca de serialização: arquivos de entrada de exemplo, saída comparada byte a byte ou campo a campo.
- Pipeline de dados: contagem de linhas e checksum por partição nos dois sistemas (o conteúdo de dados é de `data-engineering`).

## 4. Rulebook, mapa de dependências e inventário (nessa ordem)

1. **Rulebook**: equivalências (construção antiga → nova), com exemplo antes e depois e exceções. Usar `assets/templates/migration-rulebook.md`.
2. **Mapa de dependências**: define a ordem dos lotes (folhas primeiro).
3. **Inventário de comportamento implícito** do original (ordem de iteração, tratamento de nulos, fuso horário, arredondamento, efeitos colaterais). O rulebook vem antes do inventário.

## 5. Piloto, lotes e fila em disco

1. **Pré-verificação**: build do original com prova (comando e saída); leia o guia oficial de migração da versão (nenhum guia por framework foi lido nesta pesquisa: Não verificado).
2. **Plano aprovado antes de construir**: apresente e pare para aprovação. Nada é construído antes.
3. **Piloto de 3–5 arquivos**, saída descartada, regras ajustadas.
4. **Lotes retomáveis**: fila em disco; "concluído" = a saída existe **e** o juiz passa.

Formato da fila (`migration-queue.md`):

```markdown
| arquivo | lote | estado | juiz | observação |
| --- | --- | --- | --- | --- |
| src/util/date.js | 1 | concluído | passou (tsc + jest) | |
| src/api/orders.js | 2 | pendente | | depende de util/date |
| src/api/users.js | 2 | falhou | tsc: TS2339 | regra R-07 incompleta |
```

5. **Erro repetido**: corrija a regra no rulebook e regenere o lote; não remende arquivo por arquivo.
6. Modelos: menor para o volume, maior para revisão e regras (V-14; dependem do que o usuário tem).

## 6. Revisão adversarial e desempate

Dois revisores independentes (agente `code-reviewer`, contexto novo, somente leitura), cada achado citando a regra violada; um terceiro desempata. Depois: compilar, smoke test, suíte completa; agrupar falhas por causa raiz, não por arquivo.

## 7. Veredito de paridade por módulo (V-15)

| Veredito | Critério |
| --- | --- |
| PROVADO | Testes rodados do zero nos dois lados e saídas iguais para os cenários listados |
| PARCIALMENTE PROVADO | Falta evidência; é o máximo quando o sistema antigo não roda |
| NÃO PROVADO | Sem evidência ou com diferença de saída |

Diferença de saída = pendência, não "aceitável". Use `assets/templates/parity-verdict-table.md`. Nada é declarado migrado sem o juiz rodado do zero sobre o resultado final.

## 8. Strangler Fig (V-21)

Substituir por partes em vez de reescrever tudo. Quatro atividades, sem ordem fixa (a página as atribui a Cartwright, Horn e Lewis, citados por Fowler): entender os resultados desejados, decidir como quebrar o problema, entregar as partes com sucesso, mudar a organização. Use quando a reescrita total é arriscada e o remendo é caro. Todo código de transição tem data de remoção.

## 9. Parallel Change: expandir, migrar, contrair (V-37)

Aplica-se a assinatura de função, esquema de banco (conceito; migração de dados é de `database-data-modeling`), API remota e flags.

1. **Expandir**: crie a versão nova ao lado da antiga (a antiga pode delegar para a nova).
2. **Migrar**: mova os clientes aos poucos, em commits pequenos.
3. **Contrair**: remova a antiga só quando a busca não achar usos e a suíte passar. Registre a data prevista da contração.

Exemplo: trocar `enviar_email(para, assunto, corpo)` por `enviar_email(mensagem)`:

```python
# 1. Expandir
def enviar_email_v2(mensagem: Mensagem) -> None: ...
def enviar_email(para, assunto, corpo):          # antiga delega
    enviar_email_v2(Mensagem(para, assunto, corpo))
# 2. Migrar: um commit por módulo chamador, suíte verde em cada um.
# 3. Contrair: grep "enviar_email(" sem resultados fora do módulo; remover antiga e renomear v2. Data prevista: [DATA].
```

Risco: nunca contrair e piorar o código. Registre a contração no registro de dívida (snippet S-13).

## 10. Receitas determinísticas e atualização automática (V-40)

- Prefira receita determinística ou codemod quando existir; use o agente para o que sobra; rode a suíte antes e depois; em lotes pequenos.
- OpenRewrite: receitas para migração de framework, correções de segurança e estilo, via plugins Gradle e Maven, começando por Java. Licença e comandos: Não verificado. Instalar plugin altera o build: só com pedido do usuário.
- Dependabot: abre PRs de atualização com `dependabot.yml`; espera 3 dias após uma release por padrão (não vale para correção de segurança). Ver `ferramentas-e-mcp.md`.

## 11. Upgrade de dependência ou framework (checklist)

1. Ler o guia oficial de migração e o changelog da versão-alvo (cite a URL e a versão; Não verificado quando não aberto).
2. Linha de base: suíte, build e lint verdes antes; cole as saídas.
3. Lockfile: atualizar uma dependência por vez quando possível.
4. Receita ou codemod oficial primeiro; revisar o diff gerado.
5. APIs removidas ou renomeadas: Parallel Change quando o projeto expõe a API a terceiros.
6. Suíte depois; comparar avisos novos de depreciação.
7. Lotes pequenos e commits separados: upgrade mecânico, ajustes de comportamento, remoção de código de transição.
8. Relatório: o que mudou, o que o juiz provou, o que ficou parcial.

## 12. Legado somente leitura

Durante análise e migração, o código legado não é editado: as saídas vão para pasta própria (por exemplo `analysis/[NOME]/` e `modernized/`). Isso preserva o oráculo de comparação. Se o legado precisa ser alterado (ex.: para instrumentar), peça aprovação e registre como exceção.

## 13. Exemplo: migrar 180 arquivos JS para TypeScript

Pedido: "Use /code-quality-refactoring:migration-parity: migrar 180 arquivos JS para TypeScript, 2 devs, tem testes jest."

1. Tipo: transform, módulo a módulo.
2. Pré-verificação: `npm test` no original, saída colada; ler o guia de migração do TypeScript e do jest na versão do projeto (Não verificado até abrir).
3. Juiz: `npx tsc --noEmit` (deve zerar erros no novo) + `npm test` (deve manter o número de testes passando); prova: injetar um erro de tipo conhecido e ver o `tsc` reprovar.
4. Rulebook: `require` para `import`, tipos de retorno explícitos nas fronteiras, `any` só com comentário justificando; mapa de dependências (utilitários primeiro).
5. Piloto: 3–5 arquivos folha, saída descartada, ajuste de regras.
6. Plano apresentado; parar para aprovação.
7. Lotes de 20 arquivos com fila em disco; erro repetido (ex.: tipagem de eventos) corrige a regra e regenera o lote.
8. Revisão adversarial por regra violada; suíte completa; paridade por módulo.
9. Entrega: `migration-rulebook.md`, `parity-verdict-table.md`, fila, status.

## 14. Gotchas

- O relato de migração da Anthropic é um caso sem números (V-14): não cite taxas de sucesso.
- Nunca embuta hooks ou telemetria do `code-modernization` (aviso 4 de VALIDATED).
- Não instale OpenRewrite nem ative Dependabot sem pedido.
- "Compilou" não prova paridade de comportamento; o juiz deve rodar cenários nos dois lados.
- Migrar e corrigir bugs ao mesmo tempo mistura causas; bugs achados viram follow-up.
