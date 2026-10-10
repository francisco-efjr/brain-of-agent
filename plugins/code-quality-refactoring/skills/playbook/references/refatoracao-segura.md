# Refatoração segura: rede de segurança, passos pequenos e simplificação

Sumário: 1 Quando refatorar já e quando construir rede · 2 Testes de caracterização (procedimento e exemplo) · 3 Vocabulário do catálogo de refatorações · 4 Passo pequeno com desfazer · 5 Exemplo de ponta a ponta · 6 Simplificação sem mudar comportamento · 7 Escopo e API pública · 8 Dividir a mudança · 9 `/simplify`, `/batch` e "descartar e refazer" · 10 Fechar a refatoração · 11 Gotchas

Fontes: V-36 (Feathers, Fowler: caracterização e código autotestável), V-22 (catálogo, só os nomes verificados), V-18 (Google: mudança pequena), V-12 (code-simplifier), V-13 (`/simplify`, `/batch`), V-03 (receita oficial), V-37 (Parallel Change), V-10/V-11 (escopo e qualidade). A mecânica "teste a cada passo, desfazer se quebrar" é prática (Inferido); a página do catálogo não a lista.

## 1. Refatorar já ou construir rede primeiro

| Estado do trecho | Ação |
| --- | --- |
| Testes cobrem o trecho e passam | Refatorar em passos, rodando a suíte |
| Há testes, mas não cobrem o trecho | Caracterizar o trecho, depois refatorar |
| Sem testes e testável | Caracterização completa antes |
| Não testável (efeito externo, UI sem harness) | Passo menor, preservação só por leitura, rótulo Inferido, avisar o usuário |

Fowler: código autotestável dá a confiança para mudar; sem testes os desenvolvedores evitam refatorar e a dívida cresce (V-36).

## 2. Testes de caracterização

Um teste de caracterização registra o que o código faz de fato, não o que deveria fazer (Feathers). Procedimento (V-36, redação própria):

1. Escolha o trecho e as entradas relevantes: caminho feliz, bordas, vazios, negativos, limites e casos de erro.
2. Escreva um teste por entrada com expectativa provisória, rode, e fixe a saída real como expectativa. Nomeie o teste pelo comportamento observado.
3. Marque no teste as saídas que parecem bug ("comportamento atual, possível defeito") e não as corrija nesta mudança; elas viram follow-up.
4. Refatore em passos pequenos; rode os testes a cada passo.
5. Ao terminar, mantenha os testes que protegem regra de negócio e proponha remover os que só prendem detalhe de implementação.

Limites: caracterização trava também os bugs e não substitui a especificação. Use o log `assets/templates/characterization-test-log.md`.

## 3. Vocabulário do catálogo de refatorações (nomes verificados em refactoring.com/catalog; glosas são nossas)

| Nome | Para que serve |
| --- | --- |
| Extract Function | Tirar um trecho para uma função com nome de intenção |
| Inline Function | Desfazer uma função que não diz mais que o corpo |
| Extract Variable | Nomear uma expressão complexa |
| Split Loop | Separar um laço que faz duas coisas |
| Remove Dead Code | Apagar código sem uso (confirmar por busca) |
| Move Function | Levar a função para onde seus dados vivem |
| Extract Class | Dividir uma classe com duas responsabilidades |
| Hide Delegate | Esconder a cadeia de chamadas atrás de um método |
| Encapsulate Variable | Colocar um dado compartilhado atrás de acessores |
| Replace Primitive with Object | Trocar string ou número "com regras" por tipo próprio |
| Decompose Conditional | Dar nome às condições e aos ramos |
| Replace Nested Conditional with Guard Clauses | Retornos antecipados no lugar de `if` aninhado |
| Replace Conditional with Polymorphism | Trocar `switch` de tipos por variações |
| Remove Flag Argument | Separar a função que muda de modo por um booleano |
| Change Function Declaration | Renomear ou mudar parâmetros (use Parallel Change se pública) |
| Introduce Parameter Object | Agrupar parâmetros que andam juntos |

Cite o nome em cada passo do plano; a descrição detalhada de cada um está no livro (não lido nesta pesquisa).

## 4. Passo pequeno com desfazer

1. Um passo nomeado do catálogo.
2. Rode os testes. Verde: siga. Vermelho: desfaça o passo (reverta a edição que você mesmo fez; commit ou checkpoint só com pedido do usuário) e reduza o passo.
3. Anote o resultado da suíte por passo (comando e saída final).
4. Nunca misture mudança de comportamento: se um passo "precisa" mudar comportamento, pare e relate.

## 5. Exemplo de ponta a ponta (função legada sem testes)

Pedido: "refatore `calcular_frete` para ficar legível, sem mudar o comportamento". Código:

```python
def calcular_frete(peso_kg, distancia_km, expresso=False):
    if peso_kg <= 0:
        return 0
    else:
        if distancia_km <= 100:
            if peso_kg <= 5:
                valor = 15
            else:
                valor = 15 + (peso_kg - 5) * 2
        else:
            if peso_kg <= 5:
                valor = 30
            else:
                valor = 30 + (peso_kg - 5) * 3.5
        if expresso:
            valor = valor * 1.5
        return round(valor, 1)
```

**Rede de segurança.** Expectativas provisórias calculadas à mão (Inferido; rode o teste e fixe a saída real, como manda o passo 2):

```python
import pytest
from frete import calcular_frete

@pytest.mark.parametrize("peso,dist,exp,esperado", [
    (0, 10, False, 0),          # peso zero devolve 0
    (-1, 10, False, 0),         # peso negativo devolve 0
    (5, 50, False, 15),         # limite do primeiro degrau, curta distância
    (10, 50, False, 25),        # 15 + 5*2
    (5, 200, False, 30),        # longa distância, limite
    (10, 200, False, 47.5),     # 30 + 5*3.5
    (2, 50, True, 22.5),        # expresso: x1.5
    (5.04, 50, False, 15.1),    # comportamento atual, possível defeito: 15.08 vira 15.1 (centavos perdidos)
])
def test_frete_comportamento_atual(peso, dist, exp, esperado):
    assert calcular_frete(peso, dist, exp) == esperado
```

A última linha é o achado da caracterização: o arredondamento a uma casa decimal perde centavos. Ela fica no teste com a marca de possível defeito e vai para o relatório como follow-up; **não se corrige nesta mudança**.

**Passos nomeados, rodando o teste após cada um:**
1. Replace Nested Conditional with Guard Clauses: `if peso_kg <= 0: return 0` e elimina o `else`.
2. Extract Function: `_tarifa_base(peso_kg, distancia_km)` com os quatro ramos.
3. Decompose Conditional: `fixo, por_kg = (15, 2) if distancia_km <= 100 else (30, 3.5)` e `valor = fixo + max(peso_kg - 5, 0) * por_kg`, que equivale ao original porque `max(...)` vale 0 quando `peso_kg <= 5`.
4. Fechar: `return round(valor * (1.5 if expresso else 1), 1)`. Parece equivalente ao original (multiplicar por 1 não altera o valor), mas em ponto flutuante a equivalência de cada reescrita aritmética deve ser confirmada pelo teste, não pela leitura: é para isso que o teste roda a cada passo.

**Entrega:** mesma suíte, mesma saída antes e depois (comandos colados), diff final, follow-up "arredondamento perde centavos (5.04 kg, 50 km → 15.1)", status DONE_WITH_CONCERNS se a execução dos testes não ocorreu na sessão (então a preservação é Inferido).

## 6. Simplificação sem mudar comportamento (skill `simplify-safe`, V-12)

Princípio: mudar o como, nunca o quê. Escopo: o diff atual ou os arquivos indicados. Antes: rode os testes do trecho; sem teste, caracterização ou aviso de garantia só por leitura (Inferido). Passos, um por vez:
- reduzir aninhamento com retornos antecipados;
- remover duplicação;
- nomes que dizem a intenção;
- trocar ternário aninhado por if/else;
- apagar comentário que repete o código.

Não fazer: juntar responsabilidades sem relação, remover abstração com mais de um uso, mudar API pública, mexer fora do escopo, impor preferências de projeto (React, ES modules, estilo de `function`) que não estejam no CLAUDE.md. Preferir clareza a concisão. Depois: mesmos testes, saída igual; resumo de até 5 linhas.

## 7. Escopo e API pública

- Mapeie os usos (Grep) antes de mexer; liste a API pública afetada.
- Não amplie visibilidade (private para public) nem mude assinatura pública sem aprovação; para mudar, use Parallel Change (`modernizacao-e-migracao.md`).
- Bug encontrado: follow-up, não correção na mesma mudança (V-10).
- Sem abstração de uso único, sem tratamento de erro para cenário impossível (V-11).

## 8. Dividir a mudança (V-18)

- Refatoração pura em commit próprio; mudança de comportamento em outro; testes na mesma mudança do código que protegem.
- Cada commit autocontido e com a suíte verde.
- Orientação do Google: cerca de 100 linhas costuma ser razoável e cerca de 1000 é grande demais, a critério do revisor; arquivos espalhados contam. O alerta "400 linhas ou 10 arquivos" é Suposição, configurável (snippet S-09).
- Use `assets/templates/pr-split-plan.md`. Commit e push só com pedido do usuário.

## 9. `/simplify`, `/batch` e "descartar e refazer" (V-13, dependem da versão)

- `/simplify` nativo roda agentes paralelos de reuso, qualidade, eficiência e CLAUDE.md; `simplify-safe` acrescenta a garantia de comportamento com teste antes e depois.
- `/batch` entrevista e distribui o trabalho para agentes em worktrees, cada um testando e abrindo seu PR; antes dele, defina o que migra, o critério de pronto e o check por arquivo.
- Sequência recomendada: mudança, simplify, verificação de comportamento (testes e diff de saídas entre a branch e a base).
- Antes de descartar e refazer a primeira tentativa: checkpoint (commit, só se o usuário autorizar), teste de paridade e pedido mais específico.
- Prompt de endurecimento: "Liste os três pontos mais frágeis desta mudança, como você verificaria cada um, e só então proponha o PR."

## 10. Fechar a refatoração

- Compare a saída da suíte antes e depois (cole as duas).
- Confira o diff final contra o escopo.
- Mantenha os testes que protegem regra de negócio; os que só prendem implementação, proponha remover (não remova sem aprovação).
- Liste follow-ups (bugs achados pela caracterização).
- Status e rótulos; preservação sem teste executado é Inferido.

## 11. Gotchas

- Caracterização fixa bugs; "consertar" na mesma mudança torna a revisão inviável (V-18, V-36).
- Oráculo calculado pela função sob teste concorda com o erro (V-33).
- "Descartar e reimplementar" só após checkpoint e teste de paridade (V-13).
- Mudança de tipo implícita (inteiro para float, ordem de iteração, arredondamento) escapa de revisão por leitura; só o teste pega.
- Renomear símbolo exportado quebra consumidores fora do repositório: trate como API pública.
