# Forward-test: edição de cliente com isolamento de tenant

Avaliação por IA em fixture sintética descartável. Não é teste de produto real, comparação controlada de modelos, nem demonstração de superioridade da skill.

## Contexto consumido

Leitura seletiva: brains/fullstack/SKILL.md, backend-e-contratos.md, dados-e-migracoes.md, seguranca-e-privacidade.md e testes-e-debugging.md. Não houve ativação da keyword, leitura integral alegada, consulta de rubricas nesta tentativa ou alteração no repositório.

## Contrato e decisões

API preservada: edit_customer(db, authenticated_tenant, customer_id, name). Fixture define sucesso com retorno None, entrada inválida como ValueError, e ausência/inacessibilidade como CustomerNotFound('Customer not found'), tipo e mensagem idênticos. Nome valida antes de qualquer escrita, usa str.strip e len do texto normalizado; 100 caracteres Python Unicode são aceitos, 101 rejeitados. Isso não define limite por bytes nem por grafemas. authenticated_tenant é identidade confiável recebida do chamador; sua autenticação não faz parte desta função.

Baseline intencionalmente vulnerável atualiza somente por id. Correção mínima adiciona tenant_id ao predicado do mesmo UPDATE parametrizado; verifica linha afetada e não consulta recurso estrangeiro para emitir mensagem diferente. Ausência/inacessibilidade são equivalentes no contrato de exceção, sem alegar resistência a todo side channel de timing.

Esta fixture assume conexão sem transação externa pendente e função responsável pelo commit. O context manager SQLite pode confirmar/abortar transação já existente; em produto que compõe unidades transacionais, definir titularidade antes de reutilizar esta implementação. Não foram executadas cargas, testes distribuídos, HTTP ou análise da camada de autenticação.

## Checklist e evidências

- [x] Reprodução anterior: python3 -m unittest -v test_customer.CustomerTests.test_cross_tenant_no_mutation; before.exit=1, saída integral before.txt.
- [x] Baseline preservado em customer_baseline.py.
- [x] SQL parametrizado e filtro por objeto mais tenant em customer.py.
- [x] Tenant incorreto não altera DB; ausência e recurso estrangeiro têm erro externo igual.
- [x] Texto inválido (tipos/trim/101) mantém DB; limites 1/99/100 após trim são aceitos.
- [x] Persistência e normalização verificadas, incluindo fechamento/reabertura de banco em disco sintético.
- [x] Entrada semelhante a SQL permanece nome literal; tenant None não concede acesso.
- [x] Repetição da edição válida mantém resultado.
- [x] Revalidação: python3 -m unittest -v; after.exit=0, saída integral after.txt, 9 testes passam.
- [x] Ambiente registrado em environment.txt e hashes em hashes.json.
- [ ] Produto real, UI/API, autenticação e transação composta: fora deste escopo, não executados.

Dados usados são Alice/Bob e tenants a/b sintéticos. Nenhuma publicação ou chamada externa ocorreu. Próximo passo em produto: adaptar contrato de erros/retorno e titularidade transacional ao existente, mantendo predicado de autorização e testes negativos.
