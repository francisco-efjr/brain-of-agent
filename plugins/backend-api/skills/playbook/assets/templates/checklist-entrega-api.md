# Checklist de entrega de API

> Base: checklist de nove itens de `backend-e-contratos.md` e checklist integral do brain-of-agent (MIT), mais itens de V-11, V-14, V-34. Marque cada item com evidência (comando + saída, `arquivo:linha`) ou justifique "N/A". Item sem prova fica "Não verificado". "Concluído" só quando os itens aplicáveis têm evidência.

Projeto/objeto: [..] · Escopo: [..] · Revisão/ambiente: [commit/ambiente] · Data: [..]
Autorização: [análise | implementação local | ações externas específicas: quais]

## Contrato

- [ ] Consumidores e contratos existentes identificados.
- [ ] Spec atualizada e validada pelo validador do projeto (saída colada) ou "Não verificado: validador ausente".
- [ ] Diff de contrato classificado (compatível ou breaking) para cada mudança, incluindo enum novo em resposta, obrigatório novo, ordenação e tipo.
- [ ] `security` explícita por operação; erros em `application/problem+json` documentados; exemplos conferidos contra serializers reais.
- [ ] Deprecação sinalizada quando aplicável (`aviso-de-deprecacao.md`).

## Segurança

- [ ] Autorização por objeto, propriedade, função e tenant no servidor; teste com dois usuários (recurso alheio indistinguível de inexistente).
- [ ] Token validado de verdade (algoritmo fixo, `iss`, `aud`, `exp`/`nbf`).
- [ ] DTO de saída separado; campo sensível não vaza; campo extra na entrada não é aplicado.
- [ ] Segredos fora de código, logs, testes, Git e evidências; webhook com assinatura verificada sobre o corpo cru.
- [ ] Rate limit em login, envio e pagamento, com chave de credencial validada.

## Confiabilidade

- [ ] Operações com efeito têm chave de idempotência com escopo, fingerprint, atomicidade (restrição única) e expiração.
- [ ] Timeouts e retries limitados e classificados; webhook e fila toleram duplicação, ordem invertida e falha.
- [ ] Listas com paginação, limite padrão e máximo, ordenação determinística.
- [ ] Migração **proposta** (humano executa em staging/produção); compatibilidade entre versões coexistentes; limites de rollback declarados.

## Verificação

- [ ] Tipos, testes, lint e validação da spec executados após a última mudança relevante (saída colada).
- [ ] Teste de regressão falhava antes e passa depois (para bug).
- [ ] Testes negativos: authz, validação, duplicata, concorrência (duas requisições coordenadas).
- [ ] Oráculo independente e efeito persistido; mocks identificados.
- [ ] Reprodução original repetida; regressões por impacto.

## Entrega

- [ ] Artefatos localizáveis; como executar e configurar descrito.
- [ ] Rótulos (Verificado, Inferido, Suposição, Não verificável); nada de execução alegada sem ocorrência.
- [ ] Riscos residuais, limitações e próximo passo; revisão por agente declarada como não independente.

Leitura: [integral | parcial] · Execução: [completa no escopo | parcial | não executada]
Resultado: [concluído no escopo | parcial | impedido] · Críticos abertos: [IDs] · Recomendação: [..]
