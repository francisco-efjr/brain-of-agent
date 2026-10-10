# Checklist completo de revisão de arquitetura (itens CK-nn)

Validado em 2026-10-10 · Modelo-alvo: Claude 4.x/5.x · Rótulos: Verificado, Inferido, Suposição, Não verificável, Não aplicável.
Base: checklist de análise do brain-of-agent (MIT, Francisco Edson), oito eixos de revisão (padrões, escalabilidade, tecnologia, integração, segurança, desempenho, dívida, evolução), dez passos de design de serviço (V-42), checklist de revisão por hipótese (V-45), blueprint (V-10) e revisão de plano (V-19).

## Sumário

1. Como usar
2. Severidade, confiança e formato de achado
3. Checklist de análise, implementação e revalidação (brain-of-agent)
4. Eixos A a P (itens CK-01 a CK-76) e cobertura de plataforma
5. Revisão por hipótese em 10 passos
6. Design de serviço em 10 passos
7. Falhas de avaliação
8. Gotchas

## 1. Como usar

- Percorra só os eixos que o alvo toca. Um item respondido recebe `sim`, `não`, `parcial` ou `N.A.` (Não aplicável, com motivo de uma linha). Item `não` ou `parcial` vira achado se a coluna Sev. disser que importa para o contexto.
- A coluna "Detecção" é uma busca ou pergunta concreta; adapte os caminhos ao repositório. Resultado de `grep` prova presença de texto, não ausência de ligação em runtime (injeção de dependência, reflexão, configuração): marque como Inferido quando só houver leitura.
- Em revisão somente leitura, não rode comandos que baixam pacotes ou executam código de terceiros; sugira ao usuário.
- Sev.: C crítico, A alto, M médio, B baixo. A calibração é Suposição (ver seção 2).

## 2. Severidade, confiança e formato de achado

| Sev. | Critério |
| --- | --- |
| C | Perda ou corrupção de dados, falha de autorização por objeto, cascata de falha sem contenção, ação irreversível sem controle |
| A | Violação de invariante de negócio sob falha parcial, fronteira quebrada sem verificador, migração sem rollback, SLO inalcançável pelo desenho |
| M | Acoplamento que encarece mudança, ausência de observabilidade em fluxo crítico, abstração sem variação real |
| B | Inconsistência de nomenclatura, diagrama desatualizado sem impacto, dívida documentada |

Confiança 1 a 10: 10 = reproduzido ou provado por citação; 7 = leitura direta com `arquivo:linha`; 4 = inferência por convenção. Limiar padrão para reportar: 7 (Suposição configurável). Abaixo do limiar, mova para "Suposições e dúvidas".

Formato do achado (uma linha de tabela por achado). Para achado Alto ou Crítico, copie a linha de código (uma linha, sem dado pessoal) no cenário; evidência fora de código usa `git:<hash>:<caminho>`, `http:<url>@<data>` ou `contagem:<ferramenta e padrão>`:

```text
ARQ-nn (sequencial no relatório) | Item CK-nn de origem | Sev. | Conf. | arquivo:linha | Cenário concreto (entrada, falha, efeito) | Ação (menor mudança que fecha) | Rótulo
```

Exemplo: `ARQ-01 | CK-25 | C | 8 | billing/webhook.py:41 | Handler grava pedido e publica no broker em chamadas separadas; crash entre as duas deixa pedido sem evento | Gravar evento em tabela outbox na mesma transação (ver resiliencia-e-consistencia.md) | Verificado (leitura)`

## 3. Checklist de análise, implementação e revalidação

Adaptado do brain-of-agent (MIT, Francisco Edson), `arquitetura-e-dominio.md`:

- [ ] Identificar runtime, topologia, atores e dependências observados.
- [ ] Nomear invariantes e estados de negócio; revisar casos ambíguos.
- [ ] Localizar quem autentica, autoriza e decide regras.
- [ ] Definir transações e falhas entre persistência e efeitos externos.
- [ ] Comparar opções e custos antes de mudar estrutura.
- [ ] Implementar fatia vertical com contrato, regra e teste associados.
- [ ] Validar concorrência, repetição e falha parcial no fluxo alterado.
- [ ] Atualizar ADR e sequência com a arquitetura efetivamente entregue.

## 4. Eixos A a P

### A. Descoberta e evidência (padrões, tecnologia)

| ID | Verificar | Detecção | Sev. | Correção |
| --- | --- | --- | --- | --- |
| CK-01 | Há mapa de runtime, atores e dependências com `arquivo:linha`? | Pedir ao autor o fluxo ator, comando, autorização, regra, transação, efeito, resposta | M | Produzir `research.md` (template) antes de opinar |
| CK-02 | Ligações inferidas ou só de runtime estão marcadas? | Procurar DI, reflexão, plugins, config por ambiente | M | Rotular Inferido; confirmar com ferramenta de dependências do usuário |
| CK-03 | O desenho cita código realmente usado (não morto)? | `grep -rn "<símbolo>" src tests` e histórico recente | B | Excluir dead code do mapa |
| CK-04 | Tecnologia escolhida tem motivo ligado a requisito? | ADR ou comentário de decisão | M | Registrar ADR retroativo (adr-e-governanca.md) |
| CK-05 | Versão e API de cada dependência crítica foram conferidas na versão instalada? | Arquivo de lock, `--version` | M | Conferir na doc da versão; marcar Não verificável se sem acesso |

### B. Requisitos e atributos de qualidade

| ID | Verificar | Detecção | Sev. | Correção |
| --- | --- | --- | --- | --- |
| CK-06 | Atributos de qualidade (latência, disponibilidade, consistência, custo) têm número ou estão marcados Suposição? | Procurar "rápido", "escalável", "alta disponibilidade" sem número | A | Reescrever como cenário: estímulo, resposta, medida |
| CK-07 | Há requisito que justifique cada componente caro (broker, cache, serviço separado)? | Para cada componente, pergunte "qual requisito falha sem ele?" | A | Remover componente ou registrar a justificativa |
| CK-08 | Restrições do time (tamanho, habilidades, prazo, compliance) estão declaradas? | Documento de contexto | M | Perguntar uma vez; registrar |
| CK-09 | Existe a alternativa mais simples (incluindo "não mudar nada") com motivo de rejeição? | ADR, plano | A | Acrescentar |

### C. Fronteiras e dependências (padrões, integração)

| ID | Verificar | Detecção | Sev. | Correção |
| --- | --- | --- | --- | --- |
| CK-10 | Existe tabela camada ou módulo, pode importar, não pode importar? | Procurar `boundary-rules`, docs de arquitetura | A | Criar (template `boundary-rules.md`) |
| CK-11 | A regra é verificada por máquina no CI? | Procurar teste de arquitetura, lint de import, script de grep em `ci` | A | Adicionar verificador (fronteiras-e-decomposicao.md) |
| CK-12 | O núcleo de domínio importa adaptadores, frameworks ou ORM? | `grep -rnE "^(import|from) .*(adapters|infra|orm|http)" domain/` (adapte nomes) | A | Inverter dependência com porta; adaptador implementa |
| CK-13 | Módulo acessa tabela de outro módulo? | `grep -rn "<tabela_do_outro_modulo>" <módulo_a>/` | A | Propriedade de esquema: acesso via fachada ou evento |
| CK-14 | Há ciclo entre módulos ou serviços? | Grafo de imports do usuário; dependência cíclica em coreografia de eventos | A | Quebrar com evento de domínio ou inversão; ver saga |
| CK-15 | Camadas só repassam argumentos sem decisão? | Ler 3 fluxos completos; contar camadas por fluxo | M | Colapsar camadas sem variação real (antipadrão em padroes-e-antipadroes.md) |
| CK-16 | Bounded contexts têm dono de definição e tradução na fronteira? | Termos iguais com sentido diferente entre áreas | M | `context-map.md` |
| CK-17 | Código compartilhado (lib comum) tem regra de entrada? | Pasta `shared/`, `common/`, `utils/` crescendo | M | Exigir comportamento comum e dono; similaridade aparente não basta |

### D. Dados e propriedade (integração, evolução)

| ID | Verificar | Detecção | Sev. | Correção |
| --- | --- | --- | --- | --- |
| CK-18 | Cada dado tem um dono único que decide as regras? | Matriz dado x escritor | A | Designar dono; demais leem por contrato |
| CK-19 | Há mais de um escritor para o mesmo agregado ou tabela? | `grep -rn "INSERT INTO <t>\|<Entidade>.save" ` | A | Escritor único ou eventos |
| CK-20 | Banco compartilhado entre serviços serve de contrato oculto? | Credenciais do mesmo schema em dois serviços | A | Contrato explícito; migrar para API/evento (strangler) |
| CK-21 | Dados pessoais estão em logs, eventos imutáveis ou caches compartilhados? | `grep` por campos sensíveis em schemas de evento e chaves de cache | A | Mover para fora do evento ou criptografia por titular (V-37) |

### E. Estados, invariantes e transições (padrões)

| ID | Verificar | Detecção | Sev. | Correção |
| --- | --- | --- | --- | --- |
| CK-22 | Invariantes estão nomeadas e ligadas a camada, teste e métrica? | Ex.: "estoque nunca negativo" tem teste e constraint? | A | Escrever lista invariante, camada, teste |
| CK-23 | Transições de estado são explícitas (máquina de estados) em vez de booleanos combináveis? | `paid`, `cancelled`, `shipped` como booleanos independentes | M | Enumerar estados e transições permitidas |
| CK-24 | Estados intermediários e compensações têm nome e dono? | Procurar `pending`, `processing` sem tratamento de saída | M | Nomear; definir quem sai do estado e quando |

### F. Falhas parciais e consistência (integração)

| ID | Verificar | Detecção | Sev. | Correção |
| --- | --- | --- | --- | --- |
| CK-25 | Há dual write (banco e broker/serviço externo em chamadas separadas)? | Procurar `save()` seguido de `publish()`/`send()` no mesmo handler | C | Outbox (estado e evento na mesma transação) |
| CK-26 | Um consumidor recebe a mesma mensagem duas vezes sem efeito duplicado? | Procurar chave de deduplicação; teste com mensagem repetida | C | Consumidor idempotente com chave estável |
| CK-27 | A chave de idempotência é estável (MessageId ou chave de negócio) e não CorrelationId? | `grep -rn "CorrelationId\|correlation_id"` próximo a dedupe | A | Trocar a chave |
| CK-28 | Timeout de chamada externa distingue "rejeitado" de "aceitação desconhecida"? | Tratamento do ramo de timeout | A | Estado pendente + consulta de status, nunca assumir falha |
| CK-29 | O sistema afirma "exactly-once" fim a fim? | `grep -rni "exactly.once\|elimina duplicat"` em docs e código | A | Reescrever: at-least-once + idempotência |
| CK-30 | Transação atravessa mais de um agregado? | Handler que grava dois agregados na mesma transação | M | Uma transação por agregado; consistência eventual entre eles |
| CK-31 | Saga tem pivô, passos pós-pivô idempotentes e plano para compensação que falha? | Ler a orquestração | A | Ver resiliencia-e-consistencia.md |

### G. Resiliência (integração, desempenho)

| ID | Verificar | Detecção | Sev. | Correção |
| --- | --- | --- | --- | --- |
| CK-32 | Retry acontece em mais de uma camada (SDK, cliente, fila, job)? | `grep -rn "retry\|Retry\|backoff"` por camada; configuração do SDK | A | Uma camada só; a mais baixa falha rápido (N-01, V-31) |
| CK-33 | Retry tem limite, atraso exponencial com variação aleatória e operação idempotente? | Config de retry | A | Ajustar; sem idempotência, não repetir |
| CK-34 | Todo cliente externo tem timeout explícito e curto? | `grep -rn "timeout"` ; defaults infinitos de cliente HTTP | A | Definir timeout por dependência |
| CK-35 | Dependência instável tem circuit breaker (ou o broker/mesh já cobre)? | Ver V-30 "quando não usar" | M | Breaker por dependência ou shard; ou documentar a cobertura da plataforma |
| CK-36 | Recurso compartilhado (pool, thread, conexão) pode ser esgotado por uma dependência lenta? | Pools únicos usados por vários clientes | A | Bulkhead por dependência crítica, com tamanho medido |
| CK-37 | Há fallback definido e testado para a degradação? | Ramo de fallback sem teste | M | Teste que simula a falha |

### H. Concorrência e idempotência (padrões)

| ID | Verificar | Detecção | Sev. | Correção |
| --- | --- | --- | --- | --- |
| CK-38 | Duas requisições concorrentes produzem uma operação de negócio? | Restrição de unicidade; lock otimista com versão | A | Chave única ou concorrência otimista |
| CK-39 | Operações POST com efeito aceitam chave de idempotência definida no contrato? | Cabeçalho `Idempotency-Key`; escopo, TTL, resposta repetida | A | Definir semântica local (convenção, N-03) |
| CK-40 | Ordem de eventos importa e está tratada (por agregado, sessão ou versão)? | Consumidores que assumem ordem global | M | Ordenar por chave; versão no evento |

### I. API e contratos (integração)

| ID | Verificar | Detecção | Sev. | Correção |
| --- | --- | --- | --- | --- |
| CK-41 | Erros usam modelo padronizado (RFC 9457)? | Respostas `{error: "msg"}` ad hoc | M | `application/problem+json` (api-cache-escala.md) |
| CK-42 | Paginação de lista que cresce é por cursor? | `offset=` em tabela grande e mutável | M | Cursor opaco |
| CK-43 | Mudança de contrato é aditiva, com depreciação e janela? | Remoção ou renomeação de campo | A | Expandir, migrar, contrair (N-04) |
| CK-44 | Operação longa responde 202 com recurso de status? | Requisições que prendem conexão por minutos | M | 202 + `Location` do status |
| CK-45 | Autorização é verificada por objeto, não só por papel? | Endpoint `GET /orders/{id}` sem checar dono | C | Checagem por objeto no caso de uso |
| CK-46 | Atualizações concorrentes usam ETag ou versão? | PUT sem `If-Match` | M | ETag + 412 |

### J. Segurança de arquitetura (segurança)

| ID | Verificar | Detecção | Sev. | Correção |
| --- | --- | --- | --- | --- |
| CK-47 | Fronteiras de confiança estão desenhadas (internet, rede interna, terceiros)? | Diagrama de contêineres sem marcação | A | Marcar no C4 e fazer modelagem de ameaças leve (decisoes-e-tradeoffs.md) |
| CK-48 | Segredos estão fora do código e do cliente? | Revisão do repositório; variáveis de ambiente ou cofre | C | Mover; rotacionar o que vazou (ação do usuário) |
| CK-49 | Cada fluxo de dado sensível tem criptografia em trânsito e política de retenção declaradas? | Documento de dados | A | Declarar; decisão de segurança vai para `/security-appsec:playbook` |
| CK-50 | Há controle de acesso só descrito no prompt ou na UI, sem código? | Regra em texto sem verificação no servidor | C | Aplicar no servidor |
| CK-51 | Conteúdo externo (e-mail, ticket, página) entra em agente com ferramentas de escrita? | Fluxos LLM do produto | A | Tratar como dado; privilégio mínimo (llm-ai-agents) |

### K. Observabilidade (operação)

| ID | Verificar | Detecção | Sev. | Correção |
| --- | --- | --- | --- | --- |
| CK-52 | O operador consegue localizar uma intenção de negócio e seus efeitos? | ID de correlação propagado e logado | M | Propagar trace context e chave de negócio |
| CK-53 | Há métrica de duplicatas, fila parada, tamanho de DLQ e idade do evento mais antigo no outbox? | Dashboards, alertas | M | Definir; implementação em `/sre-observability:playbook` |
| CK-54 | Transições do circuit breaker geram evento e alerta? | Config | B | Acrescentar |

### L. Desempenho e escala (escalabilidade, desempenho)

| ID | Verificar | Detecção | Sev. | Correção |
| --- | --- | --- | --- | --- |
| CK-55 | Existe estimativa de ordem de grandeza (QPS pico, armazenamento, banda) com premissas rotuladas? | Documento de design | M | Fazer a conta no texto (api-cache-escala.md) |
| CK-56 | Cache foi introduzido depois de um número mostrar leitura como gargalo? | ADR ou comentário | M | Remover ou medir primeiro |
| CK-57 | Cache tem orçamento de obsolescência, TTL com variação e proteção contra stampede? | Config de cache | M | Ver api-cache-escala.md |
| CK-58 | Há consulta N+1 ou fan-out sem limite entre serviços? | Loop com chamada remota | A | Batch, limite, paginação |
| CK-59 | Existe limite de fila/backpressure ou descarte controlado? | Fila sem tamanho máximo | A | Limite e política de descarte (fonte primária de load shedding não lida: Inferido) |

### M. Migração, rollback e evolução (evolução)

| ID | Verificar | Detecção | Sev. | Correção |
| --- | --- | --- | --- | --- |
| CK-60 | A migração é em fases reversíveis, cada uma com verificação própria? | Plano | A | Fatiar; critério de conclusão por fase |
| CK-61 | Há plano de rollback que não promete recuperar dados perdidos só porque existe migração `down`? | Scripts de migração | A | Declarar limites de reversibilidade |
| CK-62 | Código de convivência (strangler) tem data de remoção e critério de desligamento? | Comentários, tickets | M | Marcar com data |
| CK-63 | Mudança de esquema segue expandir, migrar, contrair? | Migração que remove coluna usada | A | Expand/contract (N-04 para interface; para banco é Inferido) |
| CK-64 | Há feature flag ou rollout incremental para mudanças de risco? | Deploy atômico de tudo | M | Rollout gradual (detalhe em `/devops-cloud-infra:playbook`) |

### N. Testes por camada (qualidade)

| ID | Verificar | Detecção | Sev. | Correção |
| --- | --- | --- | --- | --- |
| CK-65 | Cada requisito do plano mapeia para um teste? | Tabela requisito x teste | A | Completar |
| CK-66 | Há teste de arquitetura/fronteira no CI? | Ver CK-11 | A | Adicionar |
| CK-67 | Falha parcial tem teste: duplicata, crash após commit, timeout com aceitação desconhecida? | Suíte de integração | A | Escrever os três |
| CK-68 | Testes de integração usam banco real quando a propriedade depende dele? | Mock de banco para testar constraint | M | Banco real em contêiner de teste (decisão do usuário) |
| CK-69 | Cobertura de linha está sendo usada como prova de proteção do domínio? | Relatório de cobertura sem asserção de invariante | B | Testar invariantes, não linhas |

### O. Simplicidade e decisão (padrões, dívida)

| ID | Verificar | Detecção | Sev. | Correção |
| --- | --- | --- | --- | --- |
| CK-70 | A decisão estrutural tem ADR com alternativas e consequência negativa? | `docs/adr/` | A | `adr` skill |
| CK-71 | ADR aceito foi editado em vez de substituído? | `git log -p docs/adr/` | M | Reverter edição; criar substituto |
| CK-72 | Abstração tem pelo menos uma variação real que acomoda? | Interface com uma única implementação e sem teste duplo | M | Remover indireção |
| CK-73 | Microsserviço, CQRS ou event sourcing têm gatilho nomeado? | Pergunta "qual módulo seria o primeiro e por quê" | A | Voltar a monólito modular ou documentar gatilho |

### P. Dívida e evolução

| ID | Verificar | Detecção | Sev. | Correção |
| --- | --- | --- | --- | --- |
| CK-74 | A dívida arquitetural está registrada com gatilho de pagamento? | Backlog | B | Registrar |
| CK-75 | Acoplamento de mudança entre módulos é acompanhado? | Arquivos que mudam juntos em `git log --name-only` | M | Métrica com limiar configurável (50% é Suposição de V-28) |
| CK-76 | Diagramas e CLAUDE.md foram atualizados junto com a fronteira? | Data do diagrama vs último commit estrutural | B | Atualizar no mesmo PR |

### Cobertura de plataforma (sem ID `CK`)

O eixo A a P foi escrito com sistemas de servidor em mente (outbox, idempotência, retry, concorrência entre requisições, deploy gradual). Em outra plataforma, muitos itens ficam "Não aplicável" e esse resultado esconde riscos próprios do ambiente. Antes de marcar N.A. em bloco, percorra a linha da plataforma abaixo. Conteúdo desta seção é conhecimento geral do modelo, sem fonte primária lida pelo plugin (Inferido); confirme na documentação da plataforma e na versão usada. Detalhe de implementação: `/mobile-apps:playbook` (app), `/cli-desktop-tooling:playbook` (desktop), `/backend-api:playbook` e `/devops-cloud-infra:playbook` (servidor).

| Plataforma | O que muda na revisão de arquitetura | Detecção (leitura) |
| --- | --- | --- |
| **Mobile Android** | **Composition root:** onde as dependências são montadas (`Application`, `Activity`, fábrica de `ViewModel`); `AndroidViewModel` acopla ao contexto, `ViewModel` puro é mais testável; cast para `Application` na fábrica é um sinal. **Ciclo de vida:** morte de processo, rotação e cancelamento de corrotina em `viewModelScope`; estado de tela que precisa sobreviver mora no `ViewModel` ou em armazenamento, não na `Activity`. **Testes:** teste JVM roda no CI comum; teste instrumentado exige emulador ou aparelho e em geral não é gate; tipos como `android.net.Uri` não funcionam em JVM sem `isReturnDefaultValues`, então portas com tipos simples (`String`) são mais testáveis. **Retenção local:** `SharedPreferences`, banco local e `cacheDir`: o que fica, por quanto tempo, se entra no backup (`allowBackup`). **Compartilhamento de arquivo:** `FileProvider` com permissão temporária de URI; apagar o arquivo logo após acionar o compartilhamento pode cortar o envio. **Fronteira de confiança:** `Intent` de outros apps (`ACTION_SEND`), URIs `content://` e `file://`, componentes exportados. **Manifesto:** `INTERNET`, `usesCleartextTraffic`, `allowBackup`, `exported`, `file_paths.xml`. **Room:** `exportSchema` e teste de migração. **Build:** módulo único contra multimódulo é decisão de proporção; KSP e R8 (minificação) mudam o que o teste vê. | `AndroidManifest.xml`, `**/*Factory*.kt`, `**/*ViewModel*.kt`, `app/build.gradle*`, `src/test` contra `src/androidTest`, `res/xml/file_paths.xml` |
| **Mobile iOS** | **Composition root:** `App`/`SceneDelegate` e injeção por inicializador contra singleton global. **Ciclo de vida:** transições de cena, app em segundo plano, término sem aviso; trabalho em segundo plano com tempo limitado. **Testes:** `XCTest` de unidade contra de interface (mais lento, em geral fora do gate rápido). **Retenção local:** `Keychain` para segredo, `UserDefaults` para preferência, arquivos em Application Support contra `Caches` (o sistema pode apagar o último), backup. **Fronteira de confiança:** URL schemes, universal links, share extension, App Transport Security. **Dados:** migração de Core Data ou SwiftData testada. | `Info.plist`, entitlements, `*.xcodeproj` (alvos de teste), uso de `UserDefaults` e `Keychain` |
| **Desktop** | Instalação, atualização e assinatura do binário; dados por usuário contra por máquina; processos e IPC entre UI e núcleo; várias instâncias abertas ao mesmo tempo; sandbox e permissões do sistema; migração de arquivos de configuração entre versões; teste de interface fora do CI sem tela. | Manifesto de empacotamento, caminhos de configuração, canal de atualização |
| **Servidor** | Os eixos A a P valem como estão: falha parcial e outbox, idempotência, concorrência entre requisições, autorização por objeto, deploy gradual e compatibilidade com a versão anterior. | Eixos F, G, H, J, M |

Regra de uso: item de servidor marcado N.A. em app local precisa do motivo ("não há requisições concorrentes ao mesmo recurso: um processo, um usuário"), e a linha da plataforma precisa ser percorrida. Mudança de plataforma muda a pergunta, não o rigor de evidência: `arquivo:linha` e rótulos continuam.

## 5. Revisão por hipótese em 10 passos (V-45, classe C, usada como sinal cruzado)

1. Leitura apenas (modo somente leitura). 2. Escopo por fluxo, não por repositório. 3. Mapa do estado atual com citação por afirmação. 4. Checagem por ferramenta estática de dependências, a cargo do usuário. 5. Comparação de opções por impacto no código (grafo de chamadas, restrições do time). 6. Identificar o fato que mudaria a recomendação e verificá-lo. 7. ADR somente após a decisão humana, com regra de dependência imposta por CI e ponteiro no CLAUDE.md. 8. Auditoria das citações em sessão nova, com aprovação do responsável técnico. 9. Migração em fases reversíveis com plano de rollback por fase. 10. Atualizar a documentação quando o grafo mudar.

## 6. Design de serviço em 10 passos (V-42, usado como checklist, sem listas de produtos)

1. Requisitos e restrições. 2. Fronteiras por domínio (bounded contexts). 3. Contratos. 4. Comunicação síncrona ou assíncrona (e por quê). 5. Resiliência. 6. Observabilidade. 7. Segurança. 8. Desempenho. 9. Testes. 10. Documentação com ADR. Regra de delegação: banco, nuvem, auditoria de segurança e desempenho detalhado pertencem a outros segmentos (ver Fronteiras no playbook). Acrescente o que a fonte não tem: autoverificação e marcação de suposições.

## 7. Falhas de avaliação (brain-of-agent, adaptado)

- Pastas não são isolamento: organização em diretórios sem verificador de import não impede acoplamento.
- Cobertura de linha não é proteção do domínio.
- Compilação não é integração; mock de fornecedor não é evidência do fornecedor.
- Revisão do mesmo modelo que escreveu o plano não é validação independente.
- Onde faltar acesso (produção, secrets, runtime), registre a fronteira não observada e a validação restante.

## 8. Gotchas

- O checklist tem 76 itens: aplique só os eixos do alvo. Rodar todos em mudança local é excesso e esconde os achados relevantes.
- `grep` não enxerga injeção de dependência, reflexão nem configuração por ambiente (V-45): marque Inferido.
- Limiar de confiança 7 e faixas de severidade são Suposições; ajuste ao projeto e diga quando mudar.
- Itens CK-53 a CK-54 e CK-64 apenas pedem a decisão; a instrumentação e o rollout pertencem a `/sre-observability:playbook` e `/devops-cloud-infra:playbook`.
- Fontes de load shedding e de segurança de design não foram lidas na fábrica (lacunas em fontes.md); itens CK-59 e CK-47 a CK-51 são conhecimento geral, rotulados Inferido.
