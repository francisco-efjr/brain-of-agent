# Notas da execução (eval-6, with_skill)

## Arquivos da skill que li
- `skills/qa/SKILL.md` (inteiro)
- `skills/qa/references/automacao-api.md` (inteiro: checklist por endpoint, tabela de status HTTP, estrutura de suíte, exemplo pytest, idempotência, paginação, anti-padrões)
- `skills/qa/references/dominios.md` (inteiro; usei pagamentos e PIX: idempotência, limite diário, concorrência de saldo, arredondamento, EndToEndId)
- `skills/qa/references/dados-ambientes-ci.md` (inteiro; usei isolamento, preflight, manifesto de execução, falha de setup como bloqueio)
- `skills/qa/references/seguranca.md` (inteiro; usei BOLA/IDOR, mass assignment, exemplo pytest de isolamento e corrida)
- `skills/qa/references/design-de-testes.md` (só as primeiras ~150 linhas: escolha de técnica, partição, valor-limite com 3 valores, limites ocultos)
- `skills/qa/scripts/documentos_br.py` (executado só para confirmar que `52998224726` é CPF com DV errado e `529.982.247-25` é válido)
- Não abri templates (a skill não indica template para automação de API) nem os outros scripts.
- Também li `evals/qa/files/openapi-contas.yaml` (arquivo citado no pedido).

## Como verifiquei
- `python3 -m py_compile` em todos os arquivos.
- pytest e httpx NÃO estão instalados na máquina e não pude instalar. Usei `requests` e `pydantic` (instalados) em vez de httpx.
- Escrevi, fora da pasta de saída (no scratchpad), um mini-substituto de pytest (`shim/pytest.py`), um simulador da API em memória (`fake_api.py`, adaptador do `requests`, sem rede) e um runner (`selfcheck.py`). Resultados: padrão 93 passaram + 4 puladas; com destrutivos e saldos adequados 97/97; 12 defeitos injetados no simulador, todos detectados. O simulador reflete as MINHAS suposições; isso valida a lógica dos testes, não a API real.
- Cenários de preflight (variável ausente, host sem "homolog", token inválido, contas iguais, saldo baixo, xdist) abortam com mensagem clara.
- Não executei nada contra o pytest real: coleta, `ids` de parametrização (conferi à mão que o número de ids bate com o de valores), `pytest.exit` em fixture de sessão, `register_assert_rewrite` e o relatório ficam para a primeira execução do usuário.

## Incertezas
- Contrato omisso (marcados com `@pytest.mark.inferido` ou aceitando 400/422): status de entrada inválida no POST; `Idempotency-Key` ausente/inválida; mesma chave com corpo diferente (só asserto o invariante: sem segundo débito, sem troca de valor); simultâneas com a mesma chave (aceito 409); `contaId` não-UUID (assumi 400 pelo "Parâmetros inválidos"); cursor adulterado (400); `Cache-Control: no-store` no extrato; cursor de outro titular; JSON malformado (400).
- Suposições de comportamento que NÃO estão marcadas como `inferido` mas sustentam vários testes: (1) `descricao` do POST aparece no lançamento do extrato (uso como marcador); (2) sinal do valor de DEBITO é livre (comparo `abs`); (3) saldo e extrato refletem a transferência em até 20 s (`API_ESPERA_MAX`); (4) saldo de B sobe exatamente o valor (a chave PIX de B aponta para a conta B); (5) `Transferencia.valor` é decimal comparável (`Decimal`), sem exigir 2 casas porque o contrato não fixa.
- Filtros `desde`/`ate`: supus fuso America/Sao_Paulo e extremos inclusivos; pode falhar à noite se a API usar UTC.
- Limite diário acumulado (testes destrutivos): supus que o consumido = soma dos débitos do dia no extrato; pode divergir da regra real (ex.: tarifas, transferências recusadas).
- Prazo de espera (20 s) e tolerância de 10 min para `criadaEm`/`data` são palpites razoáveis, não requisitos.
- A trava "host precisa conter homolog" é heurística (a skill avisa que URL com "test" não prova ambiente descartável); existe override por variável.
- Duas contas fixas e compartilhadas obrigam execução em série; isolamento é por marcador na descrição, não por dados exclusivos. A skill recomenda dados por teste; aqui não é possível (sem endpoint de criação de conta).
- Python >= 3.10 (sintaxe `X | None` em modelos Pydantic); `tzdata` listado nos requisitos para fusos em Windows/containers.
- Nenhum teste de segurança ativo além de isolamento entre titulares e sentinelas inofensivas (`' OR 1=1 --`) em ambiente de homologação do próprio usuário.
