---
name: tdd-guard
description: "Guia implementação test-first em fatias verticais, com vermelho confirmado pelo motivo certo. Use ao criar funcionalidade, corrigir bug ou escrever testes para código novo: 'TDD', 'red-green-refactor', 'teste primeiro', 'escreva o teste antes', 'teste de regressão do bug', 'cobrir com testes' / Use for test-first feature work, bug fixes and regression tests. Cobre fronteira pública (seam), oráculo independente, mutation check, exceções (protótipo, configuração) e o que fazer quando um teste quebra depois de uma mudança."
argument-hint: "[funcionalidade ou bug a implementar]"
---

# tdd-guard: test-first em fatias verticais

Por quê: um teste que nunca foi visto falhando pode estar passando sem exercitar o código novo (V-28, V-31, V-33; Verificado). O ciclo abaixo transforma "escrevi um teste" em "o teste detecta a ausência do comportamento".

Esta skill edita arquivos do escopo pedido (testes e código de produção). Não faz commit nem push, e não apaga código existente sem perguntar.

## Entradas

Argumentos recebidos: $ARGUMENTS (vazio: infira do contexto ou pergunte só o que muda o resultado).

- O comportamento desejado, de preferência como regra com exemplos ("subtotal a partir de R$ 199,00 tem frete grátis; 198,99 paga").
- Linguagem e framework de teste, e o comando que roda um teste só e a suíte do escopo (confira em `CLAUDE.md`, `package.json`, `pyproject.toml`; tabela de comandos em [ciclo-e-antipadroes.md](references/ciclo-e-antipadroes.md)).
- Candidato a seam (fronteira pública): função, rota ou API pública pela qual o comportamento é observável.
- Para bug: sintoma, passos e versão. Sem reprodução, use primeiro a skill `bug-report`.

Pergunte ao usuário apenas o que mudaria o teste: ambiguidade do requisito (limite inclusivo? antes ou depois do desconto?) e escolha do seam quando houver mais de uma opção razoável. O resto vira suposição declarada.

## Pré-checagens

1. Rode a suíte do escopo agora e registre a linha de base (passados, falhos, pulados). Falha preexistente é anotada e não é sua para esconder.
2. Leia 2 ou 3 testes vizinhos: nomes, imports, fixtures, estilo de asserção. Siga o padrão do projeto.
3. Se já existe código de produção escrito antes do teste, não apague: pergunte. Apagar é ação destrutiva local (K3).
4. Verifique se o caso cabe nas exceções: protótipo descartável, configuração, código gerado. Se sim, diga ao usuário que vai pular o ciclo e registre o que fica sem cobertura.

## Passos

1. **Combine a fronteira pública.** Escolha por onde o comportamento é observado (função pública, rota, CLI). Evite método privado e colaborador interno. Saída: uma frase "testo X chamando Y e observando Z".
2. **Escreva um único teste do comportamento observável.** Nome diz a quebra que pegaria ("recusa frete grátis em 198,99"). Esperado vem de literal, exemplo calculado à mão ou especificação, nunca da própria função testada. Saída: um teste.
3. **Rode e cole a falha vermelha.** Ela deve ser pelo motivo certo: comportamento ausente ou errado (`AssertionError`, valor divergente, `NotImplementedError` de um stub), não `ImportError`, `SyntaxError`, fixture inexistente ou configuração. Se o erro é de import, crie o stub mínimo (assinatura que levanta `NotImplementedError` ou devolve valor neutro) e rode de novo. Se o teste passou de primeira, trate como suspeito: o comportamento já existe, o teste é fraco ou está medindo outra coisa. Critério de saída: falha colada e classificada.
4. **Implemente o mínimo para passar.** Só o que esse teste exige. Resista a generalizar antes da fatia seguinte pedir.
5. **Rode o teste e depois a suíte do escopo.** Cole o resultado. Número de testes executados deve ter crescido em um. Critério de saída: verde sem testes pulados novos.
6. **Próxima fatia vertical.** Repita 2 a 5 para o próximo comportamento (um por vez). Nunca escreva todos os testes antes de todo o código: o teste escrito em bloco descreve a imaginação, e o ciclo perde o feedback (V-33; anti-padrão "fatiamento horizontal").
7. **Refatore com tudo verde.** Duplicação, nomes, extração, sem mudar comportamento. Rode a suíte do escopo de novo.
8. **Mutation check manual** nos módulos de risco alto (dinheiro, permissão, regra legal): aplique uma mudança realista no código de produção (inverter `>=` por `>`, remover o efeito colateral, trocar uma constante) e confirme que pelo menos um teste fica vermelho. Faça em cópia: salve o arquivo original na pasta temporária, mute, rode, restaure da cópia e confirme com `git diff` que o diff voltou ao estado anterior. Sem restauração conferida, a tarefa não terminou. Nos demais módulos, declare "mutation check não feito: risco baixo" (V-31, V-15; custo declarado, K7).
9. **Bug: regressão antes da correção.** Reproduza; escreva o teste que falha com o sintoma do relato (vermelho colado); só então corrija com a mudança mínima; mostre o verde. Inclua o ID do ticket ou incidente no nome do teste. Após 3 tentativas de correção sem sucesso, pare, resuma as hipóteses descartadas e peça decisão.

## Quando um teste quebra depois da sua mudança

Falha determinística em teste que já existia: decida antes de tocar o teste.

| Pergunta | Se sim | Ação |
| --- | --- | --- |
| O requisito mudou de verdade? | a expectativa antiga está desatualizada | peça confirmação ao responsável pela regra; só então atualize o teste, citando a decisão |
| O produto regrediu? | o teste está certo | corrija o código |
| O teste dependia de detalhe interno? | acoplamento | reescreva pelo seam público, explicando o motivo |
| Não sabe? | | trate como regressão do produto até prova em contrário |

Nunca afrouxe, pule ou remova asserção para fazer passar sem decisão humana (S-02 do playbook; V-06 trata edição de testes como inaceitável).

## Verificação

- [ ] Cada fatia mostra a falha vermelha colada e o verde colado.
- [ ] O primeiro vermelho foi por comportamento ausente, não por import ou configuração.
- [ ] Esperados vêm de fonte independente.
- [ ] Mocks só em fronteira (rede, banco, fila, relógio, aleatoriedade).
- [ ] Mutation check feito e restaurado, ou motivo registrado.
- [ ] Suíte do escopo verde com contagem maior que a linha de base.
- [ ] `git diff` não mostra teste existente enfraquecido.

## Formato de saída

```markdown
## Ciclo
| Fatia | Teste | Falha observada | Mudança | Verde |
| --- | --- | --- | --- | --- |
| 1 | recusa_frete_gratis_em_19899 | AssertionError: 1500 != 0 | condição `>= 19900` | 1 passed |

## Mutation check
`>=` -> `>` em `src/frete.py:12` => 1 failed (test_frete_gratis_no_limite). Restaurado; diff limpo.

## Não coberto
Concorrência entre carrinhos; região com acento ("Sul" vs "sul") aguarda decisão do PO.
```

Exemplo completo de um ciclo (frete por região, em cents) está em [ciclo-e-antipadroes.md](references/ciclo-e-antipadroes.md).

## Evitar (com alternativa)

- Mock de colaborador interno ou método privado: teste pelo seam público e use dublê só na fronteira.
- Teste tautológico (esperado recalculado com a mesma fórmula): escreva o literal calculado à mão.
- Snapshot cego: revise o diff semântico antes de aceitar e não mascare preço, permissão ou status.
- Teste que asserta só "não lança erro": afirme valor, estado ou efeito.
- Ampliar a suíte indefinidamente depois que as verificações adequadas passaram: um teste novo precisa responder o cartão de valor (protege o quê; falha quando; por que a cobertura atual não pega) (S-22, K15).

## Gotchas

- "O teste passou de primeira" aceito sem investigar (V-28).
- Vermelho por erro de import comemorado como vermelho válido.
- Todos os testes escritos antes do código e depois todo o código de uma vez (fatiamento horizontal).
- Teste que recalcula o esperado chamando a função testada.
- Mutação deixada no código de produção por esquecimento de restaurar.
- TDD aplicado a protótipo descartável e a configuração, onde o custo supera o benefício: use a exceção declarada.
- Tom absolutista da fonte superpowers (apagar código escrito antes do teste) não é adotado: aqui pergunta-se antes (K3).

## Quando delegar

- Escrever muitos testes para código existente sem tocar produção: agente `qa-testing:test-writer`, depois `qa-testing:test-reviewer` em contexto limpo.
- Revisão dos testes novos: `qa-testing:test-reviewer` (somente leitura). Declare que revisão do mesmo modelo não é validação independente.
- Prova final de pronto: skill `verification-gate`.

## Referências

- [ciclo-e-antipadroes.md](references/ciclo-e-antipadroes.md): ciclo completo com saídas, comandos por stack, anti-padrões antes/depois, tabela de racionalizações.
- Playbook: `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/unitarios-e-integracao.md` (dublês, tempo, concorrência, propriedades, legado) e `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/padroes-e-antipadroes.md`. Os códigos K3, K7 e K15 citados acima estão em `decisoes-e-tradeoffs.md` na mesma pasta.

Validado em: 2026-10-10 · modelo-alvo: claude-sonnet-5-5. Confira flags de runner e de mutação (Stryker, mutmut) na versão instalada.
