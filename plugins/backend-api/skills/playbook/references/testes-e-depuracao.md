# Testes de API e depuração de backend

Resumo para `api-test-suite` e `backend-debugging` (os exemplos de código por framework vivem em `${CLAUDE_PLUGIN_ROOT}/skills/api-test-suite/references/`). Técnicas gerais de teste (estratégia, pirâmide, flaky, E2E, evals) pertencem a `/qa-testing:playbook`; aqui fica o que é específico de API. Fontes: brain-of-agent (`automacao-api.md`, `testes-e-debugging.md`, MIT), V-25 e demais `V-nn` de `fontes.md`.

## Sumário

- [1. Princípios de teste de API](#1-princípios-de-teste-de-api)
- [2. Estrutura da suíte](#2-estrutura-da-suíte)
- [3. Contrato: Pact, schema e fuzz](#3-contrato-pact-schema-e-fuzz)
- [4. Eventos, webhooks e GraphQL/gRPC](#4-eventos-webhooks-e-graphqlgrpc)
- [5. Antipadrões de teste](#5-antipadrões-de-teste)
- [6. Depuração em quatro fases](#6-depuração-em-quatro-fases)
- [7. Sintomas comuns e hipóteses a testar](#7-sintomas-comuns-e-hipóteses-a-testar)
- [8. Lentidão: medir antes de mudar](#8-lentidão-medir-antes-de-mudar)
- [9. Relatório de causa raiz](#9-relatório-de-causa-raiz)

## 1. Princípios de teste de API

1. **Priorize pelo risco:** dinheiro, dado de terceiros, operação irreversível.
2. **Status 200 não prova nada:** confira valor de negócio contra oráculo independente (total calculado à parte, dado semeado) e o efeito persistido (o `GET` seguinte, a linha no banco, o evento emitido **uma** vez).
3. **Menor camada que prova a regra:** unidade para cálculo e transição; integração para serialização, persistência e adapters; contrato para consumidor/provedor; E2E para a jornada. Não duplique cenários em todas as camadas.
4. **Vermelho confirmado:** para bug, o teste de regressão falha pelo motivo certo antes da correção.
5. **Mock** serve para falha externa; não substitui persistência real quando a atomicidade é a questão. Declare o que é mock e o que é integração real.
6. **Ambiente:** local ou descartável; homologação só com autorização; produção nunca. Segredos por variável de ambiente.

A tabela de 14 aspectos por endpoint e a de status HTTP estão em `checklist-completo.md`.

## 2. Estrutura da suíte

- **Cliente fino:** um método por operação que devolve a resposta crua, sem asserção nem exceção em 4xx (senão os testes negativos ficam impossíveis).
- **Fábrica de dados:** cada teste cria o que usa, com identificador único, para rodar em paralelo e em qualquer ordem; limpa o que criou ou usa ambiente descartável.
- **Schema para forma, asserção separada para valor:** JSON Schema, Pydantic ou Zod provam a forma; os valores de negócio são conferidos à parte. Na resposta aceite campo novo.
- **Autenticação por fixture:** token obtido uma vez por sessão com credenciais do ambiente; **dois usuários** de teste para provar isolamento (BOLA).
- **Erro comparado por `type`/código**, nunca pelo texto.
- **Esperas por condição** com prazo (`esperar_ate`), nunca `sleep` fixo.
- Teste de concorrência **coordena** as duas requisições (barreira/threads), nunca as dispara em sequência.

Exemplo mínimo de oráculo (Python/pytest, adaptado do brain, MIT): "CAFE-500G" custa 24,95 na massa semeada; dois itens somam `"49.90"`.

```python
def test_total_do_pedido_vem_do_catalogo_semeado(api):
    r = api.post("/pedidos", json=novo_pedido(), headers={"Idempotency-Key": str(uuid.uuid4())})
    assert r.status_code == 201, r.text
    assert r.json()["total"] == "49.90"                 # 2 x 24,95: oráculo independente
    lido = api.get(r.headers["location"])
    assert lido.status_code == 200 and lido.json()["id"] == r.json()["id"]   # efeito persistido
```

## 3. Contrato: Pact, schema e fuzz

Escolha pela tabela de `decisoes-e-tradeoffs.md`, seção 6. Pontos operacionais (brain; *Inferido* onde a fonte oficial não foi lida):

- **Pact:** o consumidor gera o contrato executando o **código real do cliente** contra um mock; o provedor reproduz cada interação contra a API verdadeira. Use matchers de tipo e formato; regra de negócio não entra no contrato. `provider states` parametrizados preparam os dados; `enablePending` impede que expectativa nova de um consumidor quebre o build do provedor antes de implementada; `can-i-deploy` como gate de deploy; token do broker por variável de ambiente.
- **OpenAPI como fonte:** Schemathesis gera requisições a partir da spec e confere respostas (500, resposta fora do schema, `negative_data_rejection`, `ignored_auth`, `use_after_free`); Prism mocka e valida tráfego; diff de spec (oasdiff) no CI. Fases `examples`, `coverage`, `fuzzing`, `stateful`.
- **Fuzz** cria lixo e pode derrubar o serviço: só em ambiente **descartável** e autorizado, com token de teste. Cada falha vira teste de regressão com o caso mínimo.
- Comandos e riscos em `ferramentas-e-mcp.md`.

## 4. Eventos, webhooks e GraphQL/gRPC

- **Mensageria:** consuma desde o início (`auto.offset.reset=earliest`, grupo exclusivo) e filtre pelo ID criado; com `latest`, a mensagem publicada antes da atribuição de partições se perde e o teste fica intermitente. Teste duplicata (um efeito), mensagem envenenada (DLQ com motivo, seguintes continuam) e ordem invertida.
- **Webhooks:** assinatura válida (2xx); um byte alterado (401, nada processado); timestamp fora da tolerância; mesmo evento duas vezes (um efeito); rotação de segredo.
- **GraphQL:** a asserção começa por `errors` ausente; profundidade, aliases em massa, N+1 por contagem de consultas (constante com 1 e com 50 itens), introspecção em produção, autorização por campo em cada caminho.
- **gRPC:** o HTTP é 200 e o resultado vem no trailer `grpc-status`; teste deadline curto contra dependência lenta (`DEADLINE_EXCEEDED` rápido), streaming (cancelar libera recursos), `buf breaking` para `.proto`. `grpcurl` com reflection só em desenvolvimento.

## 5. Antipadrões de teste

Testar só status; dependência de ordem (ID em variável global); dados compartilhados entre testes; asserção sobre texto de mensagem; IDs fixos; token fixo no código; oráculo circular; sleep fixo; Postman como substituto de suíte em código para regressão (JSON grande, sem tipo, diff ilegível; Bruno grava um arquivo por requisição e versiona melhor). Ver `padroes-e-antipadroes.md` (AB-01 a AB-04).

## 6. Depuração em quatro fases

Base: V-25 (obra/superpowers e wshobson, MIT), reescrita em tom calmo. A regra de **três correções falhas** é convenção, não lei; a doc oficial de boas práticas sugere `/clear` e prompt melhor após duas correções falhas (V-04).

1. **Investigar sem corrigir:** leia o erro inteiro; reproduza (ou declare que não reproduziu); liste o que mudou há pouco; colete evidência em cada fronteira (entrada → camada → dados → dependência externa).
2. **Comparar:** com código semelhante que funciona; liste as diferenças.
3. **Hipótese única:** formule uma hipótese refutável e teste com a menor mudança possível; registre as descartadas. Uma mudança por vez.
4. **Corrigir com prova:** escreva o teste que falha; aplique **uma** correção na causa; rode a suíte e cole a saída.

Após três correções seguidas sem sucesso, pare e revise a arquitetura com o usuário; não empilhe patches. Segredos mascarados em logs; sem `.env`; nada de teste contra produção ou staging sem autorização. Bugs vizinhos viram follow-up.

## 7. Sintomas comuns e hipóteses a testar

*Inferido* (conhecimento estável de engenharia). Cada linha é uma hipótese a **testar**, não um diagnóstico.

| Sintoma | Hipóteses prováveis | Como testar |
| --- | --- | --- |
| 500 intermitente só sob carga; erro de "conexões esgotadas" | Engine/pool criado por requisição; conexão não devolvida; pool menor que a concorrência | Contar conexões abertas durante o teste; engine único por processo; sessão fechada via dependência |
| Timeout após deploy | Dependência lenta, orçamento de timeout mal distribuído, DNS, migração com lock | Medir tempo por salto; checar locks; comparar com a versão anterior |
| Funciona local, falha em produção | Variável de ambiente, versão de dependência, fuso, tamanho de dados, proxy que muda cabeçalho | Diff de configuração e de lockfile; reproduzir com dados representativos em ambiente permitido |
| Duplicação de efeito | Retry sem idempotência, corrida sem unicidade, reprocessamento de fila | Rastrear o ID da operação entre camadas; teste com duas requisições concorrentes |
| 401 intermitente | Relógio/`exp`/`nbf` com tolerância, chaves em rotação (`kid`), cache de JWKS | Comparar `iat`/`exp` com o relógio; logar o `kid` (não o token) |
| 403 inesperado | Escopo não mapeado, `aud` errado, guard em ordem errada | Reproduzir com perfil mínimo; ler a ordem de guards/filtros |
| Resposta com dado de outro usuário | Cache sem escopo, consulta sem filtro de dono | Teste com dois usuários; conferir chave de cache |
| JSON válido, regra errada | Oráculo ausente; tipo de dinheiro float; fuso | Valor esperado calculado à parte |

## 8. Lentidão: medir antes de mudar

Não otimize por intuição. Meça: tempo por requisição (percentis), **contagem de consultas por requisição**, tamanho da resposta, uso do pool de conexões e tempo gasto em dependências. **N+1** se prova por contagem de consultas num teste (constante ao crescer a lista: sem N+1; linear: N+1) e se corrige com carregamento antecipado/DataLoader/lote. Índice, plano de execução e modelagem pertencem a `/database-data-modeling:playbook` (delegue; *Inferido*). Paginação e limites protegem a latência (API4). Testes de carga/performance: `/qa-testing:playbook`, e limiares de SLO em `/sre-observability:playbook`; nunca carga contra ambiente compartilhado sem autorização.

## 9. Relatório de causa raiz

```text
Sintoma: [erro, endpoint, frequência]            Reproduzido: sim | não | parcial (como)
Causa raiz: [uma frase, com o arquivo:linha]     Rótulo: Verificado | Inferido | Suposição
Evidência: [comando + saída essencial; log mascarado]
Hipóteses descartadas: [lista curta com o teste que refutou]
Correção: [diff mínimo]                          Teste de regressão: [nome; falhava antes: sim]
Verificação: [suíte completa, comando e saída]   Prevenção: [teste, validação, linha de CLAUDE.md proposta]
Não executado / limitações: [...]
```

Validado em 2026-10-10.
