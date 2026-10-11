# Notas e incertezas

## O que não foi possível verificar
- pytest não está instalado no ambiente (e a regra era não instalar pacotes). Os arquivos compilam, mas a execução foi feita com um mini-shim de pytest + API fake em memória que eu mesmo escrevi (fora da pasta de saída). O shim ignora marcadores, `-m`, ordenação e geração de ids do pytest real. Pontos que só o pytest real confirma: `pytest.exit` dentro de fixture de sessão, `pytest.skip` em fixture com escopo de módulo/sessão, `pythonpath = tests` no `pytest.ini` (exige pytest >= 7), `--strict-markers` com os marcadores declarados.
- A API fake foi escrita por mim a partir do mesmo OpenAPI, então os testes passarem nela só mostra consistência interna. O comportamento real da homolog pode divergir.
- Nenhuma requisição de rede foi feita.

## Lacunas do spec que viraram suposições
- POST /transferencias só documenta 201, 200, 401, 404 e 422. Entrada malformada (campo ausente, valor fora do pattern, JSON quebrado, Idempotency-Key ausente ou fora do formato uuid) não tem status documentado. Os testes aceitam 400 ou 422 (`ERRO_DE_VALIDACAO`). Se o time definir um só, apertar.
- "valor mínimo 0.01": `0.00` passa no pattern; assumi que é recusado (400 ou 422), não 201.
- "limite diário de 5000.00": não está claro se é por transferência ou acumulado no dia. O teste de 5000.01 vale nas duas leituras; o acumulado (4990.00 + 20.00) é premissa e opt-in.
- "máximo = saldo disponível": usei o `saldo` do extrato como saldo disponível. Se houver bloqueios/reservas, o saldo do extrato e o disponível podem diferir e o teste de saldo insuficiente (saldo + 0.01) ainda deve passar, mas não prova o cálculo de "disponível".
- Mesma Idempotency-Key com corpo diferente: o spec não define. O teste só exige que não crie nova transferência (não aceita 201) e, se devolver 200, que seja exatamente a original. Se a API devolver 409 ou 422, passa.
- Requisições simultâneas com a mesma chave: assumi exatamente um 201 e as demais 200 ou 409. O 409 não está no spec.
- Escopo da Idempotency-Key por usuário: o teste só exige que o usuário B não receba 200 nem o id da transferência de A. Não exige 201 (a API poderia responder 409 por colisão global).
- O 200 de repetição não tem schema no spec. Assumi corpo igual ao do 201 (Transferencia) e `criadaEm` idêntico.
- `Transferencia.valor` não tem pattern no spec; exijo string decimal parseável (não número JSON).
- Sinal do `valor` do lançamento de débito: o pattern aceita `-`, mas o spec não diz se débito vem negativo. O teste compara o valor absoluto.
- Semântica de `desde`/`ate`: assumi limites inclusivos e fuso indefinido (tolerância de +-1 dia no teste de filtro, marcado `premissa`). Datas futuras e intervalos enormes não foram testados.
- `pagina` inválida e `contaId` fora do formato uuid: o spec lista 400 para "parâmetros inválidos" mas também 404; para `contaId` malformado aceito 400 ou 404 (nunca 5xx). Marcados `premissa`.
- Ordenação dos lançamentos não é especificada: nenhum teste depende dela (a busca do lançamento criado varre até 20 páginas de 100 com `desde` = ontem em UTC).
- A descrição enviada volta intacta no lançamento do extrato (premissa do teste `test_extrato_da_origem_registra_o_debito`, marcado `premissa`).
- Transferência nascendo `RECUSADA` no 201: não há como acompanhar o status depois (sem GET /transferencias/{id}); no 201 do fluxo feliz exijo `status != RECUSADA`.

## Riscos de flakiness
- Consistência eventual: débito/crédito podem demorar. `TIMEOUT_ASSINCRONO` (padrão 20 s) e `ESPERA_ESTABILIZACAO` (padrão 3 s) são palpites. Se a homolog for mais lenta, os testes de saldo (baseline "estável") podem falhar de forma intermitente.
- Se outra pessoa/processo mexer nas contas A e B durante a execução, as comparações de saldo falham. A suíte assume uso exclusivo dessas duas contas.
- Tokens expirando no meio da execução: a checagem inicial só detecta token ruim no começo.
- A execução completa leva alguns minutos por causa das esperas de estabilização.
- O teste de simultaneidade usa 5 threads com uma barreira; se houver rate limit, podem aparecer 429 e o teste falha (a premissa não prevê 429).
- `nao_vazar_detalhes_internos` procura poucas marcas ("Traceback", "SQLSTATE", etc.): heurística barata, não é varredura de segurança.

## Decisões de design que o usuário pode querer rever
- Tokens por variável de ambiente (sem login automático) e chave PIX da conta B obrigatória (`CHAVE_PIX_B`); `CHAVE_PIX_A` é opcional e só liga o teste de isolamento da Idempotency-Key.
- Valores sempre `Decimal`/string; nenhum float para dinheiro.
- Validação de contrato escrita à mão (não jsonschema) porque `nullable` do OpenAPI 3.0 e `format` não são JSON Schema puro. Se o contrato crescer, vale trocar por validação gerada do próprio YAML.
- Trava de URL: a suíte aborta se `API_BASE_URL` não contiver "homolog" (override: `PERMITIR_URL_FORA_DE_HOMOLOG=1`).
- A cobertura do tamanho padrão (20) e do limite 100 só é real se a conta de teste tiver mais de 20 / 100 lançamentos; com menos, o teste passa mas prova pouco. A paginação é pulada (skip) se a conta tiver só 1 lançamento.
- O harness de verificação (shim de pytest + API fake) ficou fora da entrega, no scratchpad da sessão (`eval6-h/`). O scratchpad é compartilhado com outras sessões e um `shim/pytest.py` de lá foi sobrescrito por outra execução durante o trabalho; recriei o meu em pasta própria.
