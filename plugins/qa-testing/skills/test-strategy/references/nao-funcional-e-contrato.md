# Não funcional e contrato: API, acessibilidade, performance

Apoio da skill `test-strategy` (e consultado por `test-design` para casos de API). Cobre as linhas não funcionais que todo plano precisa decidir: testes de API, contrato entre serviços, acessibilidade e performance.

Rótulos: onde a fonte foi lida por um validador aparece o item V-nn (Verificado). O restante é conhecimento estável do domínio ou conteúdo próprio do brain-of-agent (MIT), Inferido: confira na documentação da ferramenta instalada. Não rode nada daqui contra produção ou sistema de terceiros.

## Sumário

- [Checklist de API por endpoint](#checklist-de-api-por-endpoint)
- [Casos negativos de autorização](#casos-negativos-de-autorização)
- [Contrato entre serviços (Pact)](#contrato-entre-serviços-pact)
- [Schemathesis a partir de OpenAPI](#schemathesis-a-partir-de-openapi)
- [Acessibilidade em três camadas](#acessibilidade-em-três-camadas)
- [Performance: tipos de teste e lacuna de limiares](#performance-tipos-de-teste-e-lacuna-de-limiares)
- [Como decidir o que entra no plano](#como-decidir-o-que-entra-no-plano)

## Checklist de API por endpoint

Use como lista de lembrete por endpoint; marque N/A com justificativa. A ordem prioriza o que costuma custar dinheiro, dado ou segurança. Base: conhecimento estável e brain-of-agent (Inferido).

| # | Área | Casos mínimos | Oráculo |
| --- | --- | --- | --- |
| 1 | Sucesso | status correto (200/201/204), corpo contra o schema (campos, tipos, formato de data e moeda), `Content-Type`, `Location` em 201 | contrato OpenAPI ou exemplo da especificação |
| 2 | Autenticação | sem credencial, credencial malformada, expirada, de outro ambiente | 401 com formato de erro do contrato |
| 3 | Autorização | perfil sem permissão; recurso de outro usuário ou tenant (IDOR) | 403 ou 404 conforme contrato; nunca o dado |
| 4 | Validação de entrada | campo ausente, `null`, `""`, tipo errado, acima do limite, valor fora da lista, campo extra desconhecido | 400/422 com erro por campo; nada gravado |
| 5 | Corpo e cabeçalhos | JSON malformado, `Content-Type` errado, corpo vazio, corpo gigante | 400, 415, 413 |
| 6 | Idempotência | `PUT`/`DELETE` repetidos; `POST` com a mesma chave de idempotência; mesma chave com payload diferente | um efeito só; conflito definido (409/422) |
| 7 | Paginação, filtros, ordenação | 0, 1, limite, limite+1, página além do fim, parâmetro inválido, ordenação estável | totais e cursores coerentes |
| 8 | Concorrência | duas atualizações simultâneas, último item de estoque, versão otimista (`ETag`/`If-Match`) | um vencedor, o outro recebe 409/412 |
| 9 | Erros | formato consistente (por exemplo Problem Details, RFC 9457), sem stack trace, SQL ou segredo | mensagem útil e segura |
| 10 | Limites operacionais | rate limit (429 com `Retry-After`), timeout, payload no limite e +1 | contrato e configuração do gateway |
| 11 | Efeitos colaterais | registro no banco, evento publicado, e-mail; confirmar com leitura posterior (`GET`, consulta, fila) | estado observado, não só o status 2xx |
| 12 | Dados sensíveis | resposta e logs sem senha, token, CPF completo | lista de campos proibidos |

Exemplo executável contra ambiente de teste (substitua variáveis; token de teste, nunca real):

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X POST "$BASE_URL/api/pedidos" \
  -H "Authorization: Bearer $TOKEN_QA" -H "Content-Type: application/json" \
  -d '{"itens":[{"sku":"FONE-XZ","qtd":-1}]}'
# esperado pelo contrato: 422; qualquer 2xx ou 500 é achado
```

Em PowerShell use `curl.exe` (o alias `curl` chama `Invoke-WebRequest`). Registre o `request id` da resposta para ligar o achado ao log.

Armadilhas: validar só pela tela e esquecer que a API aceita o que a tela bloqueia; asserir só `200` sem conferir corpo e efeito; reusar o mesmo usuário em todos os casos (esconde falha de autorização); status HTTP de sucesso não prova que o consumidor de um evento aplicou o efeito.

## Casos negativos de autorização

Matriz mínima para qualquer recurso com dono (Inferido; fronteira com o segmento de segurança: aqui se escreve o caso de verificação, não a exploração):

| Ator | Recurso | Ação | Esperado |
| --- | --- | --- | --- |
| dono | próprio | ler, alterar | permitido |
| mesmo perfil, outro dono | de outro | ler, alterar, apagar | 403/404, nenhum dado vazado |
| perfil menor | qualquer | ação privilegiada | 403 |
| sem sessão | qualquer | qualquer | 401 |
| tenant A | recurso do tenant B (ID trocado na URL e no corpo) | qualquer | 403/404 |
| token revogado | próprio | qualquer | 401 |

Teste direto na API, pulando a tela: a interface esconde o botão, o back-end esquece a regra.

## Contrato entre serviços (Pact)

Base: V-16 (Verificado). O contrato é gerado nos testes do consumidor, só com o que o consumidor realmente usa (consumer-driven); o provider reenvia as requisições gravadas em seu pipeline e compara com a resposta mínima esperada; um broker liga as duas pontas ao CI. A página lida não confirma `can-i-deploy`.

Checklist:

1. Liste as interações por consumidor (endpoint, campos usados, estados do provider).
2. Gere o contrato nos testes do consumidor e publique no broker (ou compartilhe o arquivo).
3. Verifique no provider no CI; quebra de contrato é breaking change e bloqueia o merge.
4. Para APIs públicas descritas por OpenAPI, "provider contract testing" contra o documento é uma abordagem distinta (V-16).
5. Contrato não substitui E2E de jornada nem prova efeito de negócio.

## Schemathesis a partir de OpenAPI

Base: V-26 (Verificado nas páginas; licença e versão não constam nelas). Gera casos a partir de OpenAPI (2.0 a 3.2) e GraphQL; checagens incluem erro 5xx, status não documentado, resposta fora do schema, requisição inválida aceita, autenticação ausente ou inválida e método não suportado. A saída traz um `curl` de reprodução e um seed; `replay <ID>` reenvia um caso.

```bash
uvx schemathesis run "$STAGING_URL/openapi.json"
```

Riscos: executa pacote de terceiros e envia muitas requisições de borda. Só contra ambiente local ou de staging, com credenciais de teste, fora do pico, depois de confirmar licença e versão do pacote. Não entra como hook nem comando automático do plugin. Achados viram bug report com o `curl` de reprodução (skill `bug-report`).

## Acessibilidade em três camadas

Base: V-18 (Verificado). WCAG 2.2 é Recomendação W3C de 12/12/2024; o critério 4.1.1 Parsing foi removido; há nove critérios novos (2.4.11, 2.4.12, 2.4.13, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8, 3.3.9; os nomes e níveis A/AA/AAA vêm de conhecimento estável: confirme no W3C). Os princípios são Perceptível, Operável, Compreensível e Robusto. A W3C WAI afirma que nenhuma ferramenta sozinha determina conformidade; avaliação humana qualificada e pessoas com deficiência fazem parte do processo.

| Camada | O que faz | Limite |
| --- | --- | --- |
| 1. Automatizada | axe-core, Lighthouse, pa11y ou similar varrem a página (integração do axe com Playwright: Inferido, confirmar na doc da ferramenta) | acha só uma parte dos problemas; "zero violações" não é conformidade |
| 2. Revisão manual | roteiro de teclado e leitor de tela (abaixo) | depende de quem executa |
| 3. Teste com usuários | pessoas com deficiência usam fluxos reais | custo e recrutamento |

Roteiro manual de 15 minutos por fluxo (Inferido, conhecimento estável):

1. **Teclado.** Percorra com `Tab` e `Shift+Tab`; a ordem é lógica? O foco é sempre visível e nunca fica escondido por cabeçalho fixo ou banner (2.4.11 é novo na 2.2)? Dá para ativar tudo com `Enter`/`Espaço`; menus e modais fecham com `Esc`; não há armadilha de teclado.
2. **Zoom e reflow.** 200% de zoom e largura de 320 px CSS sem rolagem horizontal nem perda de função.
3. **Contraste.** Texto 4.5:1 (3:1 para texto grande); componentes de interface e ícones informativos 3:1.
4. **Leitor de tela.** NVDA com Firefox ou Chrome no Windows; VoiceOver com Safari no macOS; TalkBack no Android. Verifique: cada campo tem rótulo; botões e links têm nome acessível; títulos e regiões (landmarks) permitem navegar; erros de formulário são anunciados (por exemplo `role="alert"` ou `aria-live`) e ligados ao campo; atualizações dinâmicas (toast, carrinho) são anunciadas.
5. **Alvos e arrasto.** Alvos de toque com tamanho mínimo e alternativa a arrastar (2.5.8, 2.5.7).
6. **Autenticação e repetição.** Login sem teste cognitivo obrigatório e sem pedir de novo o que o usuário já informou no mesmo fluxo (3.3.8, 3.3.7).

Formato do achado: critério WCAG, nível, passos, esperado, obtido, impacto para quem usa a tecnologia assistiva, evidência (captura, trecho do DOM) e severidade (tabela na skill `bug-report`). Exemplo de gravidade: botão "Pagar" inacessível por teclado e leitor de tela é Crítica (sem contorno para um grupo de usuários, possível violação legal).

## Performance: tipos de teste e lacuna de limiares

Base: V-23 (Verificado). Tipos do k6: **smoke** (a carga mínima valida que o script e o sistema funcionam), **average-load**, **stress**, **soak** (horas, acha vazamento e degradação lenta), **spike**, **breakpoint**. Ordem sugerida: começar pelo smoke e subir carga e duração. Durações aproximadas da fonte: smoke de segundos a minutos; load e stress de 5 a 60 minutos; soak de horas. A página não traz limiares nem SLO; essa é uma lacuna deste plugin. Definição de SLO, alertas e canário pertence ao segmento de SRE.

Como usar em um plano:

1. Declare o objetivo (capacidade, regressão de latência, estabilidade longa) e a métrica de negócio ligada (p95 do checkout, taxa de erro).
2. Pegue a linha de base da produção ou da versão anterior; sem ela, o resultado é número solto.
3. Comece por smoke; só suba com autorização do dono do ambiente.
4. Registre o ambiente (tamanho, dados, dependências simuladas) e rode mais de uma vez: uma execução não prova nada.

Esqueleto de smoke em k6 (API estável, Inferido; os limiares são placeholders, Suposição, a calibrar com a linha de base):

```js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 1,
  duration: '30s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<800'],
  },
};

export default function () {
  const res = http.get(`${__ENV.BASE_URL}/health`);
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```

Rodar: `k6 run -e BASE_URL=https://staging.exemplo.test smoke.js`. Armadilhas: gerador de carga na mesma máquina do sistema; massa de dados pequena demais (cache quente); dependências de terceiro reais recebendo carga; média no lugar de percentis.

## Como decidir o que entra no plano

| Sinal no contexto | Linha não funcional a incluir |
| --- | --- |
| Muitos usuários, pico sazonal, SLA contratado | performance: smoke + load do fluxo crítico |
| API pública ou consumida por vários times | contrato + checklist de API + Schemathesis em staging |
| Fluxo de pagamento, cadastro ou saúde | autorização negativa + acessibilidade do fluxo |
| Público com deficiência, exigência legal ou setor público | acessibilidade nas 3 camadas |
| App em loja ou instalação on-premises (correção cara) | mais profundidade antes do release; compatibilidade |
| Serviços pequenos com risco nas fronteiras | integração com serviço real + contrato |

Se a linha não se aplica, escreva por quê ("sem alteração de código de interface; acessibilidade fora do plano, risco residual: nenhum novo").
