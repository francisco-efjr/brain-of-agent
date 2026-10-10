# Fronteiras e decomposição

Validado em 2026-10-10 · Modelo-alvo: Claude 4.x/5.x · Rótulos: Verificado, Inferido, Suposição, Não verificável.
Fontes: V-24 (CC0), V-25 (Cockburn), V-26 (Fowler, bounded context e agregado), V-27 (Fowler, MonolithFirst), V-28 (athola, MIT), V-29 (Fowler, Strangler), N-04 (Parallel Change), V-44, gstack plan-eng-review (MIT, só a pergunta sobre Conway). Lacunas de fonte primária: Clean Architecture (Martin), DDD de Evans e Vernon, fitness functions (Ford et al.). O que depende delas está rotulado Inferido.

## Sumário

1. Decidir: monólito modular ou serviços
2. Mapear bounded contexts e context map
3. Agregados: checklist
4. Hexagonal: quatro perguntas
5. Tabela camada para imports e regra de dependência
6. Módulos, fachadas e propriedade de esquema
7. Verificadores: testes de arquitetura (fitness functions)
8. Script de exemplo de verificação por grep
9. Strangler em 7 passos
10. Expand/contract para contratos e dados
11. Métricas de acoplamento
12. Exemplo de saída do `boundary-mapper`
13. Gotchas

## 1. Decidir: o teste do primeiro serviço (V-27)

Antes de propor dividir, responda por escrito:

1. Qual módulo seria o primeiro a extrair e por quê?
2. Que métrica ou restrição justifica (escala diferente, isolamento de falha, times bloqueados no deploy)?
3. Qual o custo de rede, observabilidade e dados após a extração?
4. Há times com ciclos de entrega diferentes?

Sem resposta para a pergunta 1: recomende monólito modular com fronteiras internas verificadas e proponha o teste de CI. Base: Fowler (2015) diz que microsserviços têm custo operacional que desacelera equipe pequena, que a maioria dos casos de sucesso começou como monólito e que mover funcionalidade entre serviços custa mais do que dentro do monólito. O teste "nomeie o primeiro serviço" vem do artigo de um fornecedor de framework (Encore, classe C) e a tese dele sobre agentes raciocinarem melhor sobre código inteiro não foi medida. Posição argumentada, não teste empírico.

Pergunta de Conway (gstack, MIT; adaptada): a fronteira técnica combina com a fronteira de equipe? Desenhe as duas juntas.

## 2. Bounded contexts e context map (V-26)

Um modelo único para o negócio todo não funciona; cada contexto tem modelo e linguagem próprios e a mudança de linguagem costuma marcar a fronteira. Perguntas para mapear:

1. Quais termos têm sentido diferente entre áreas ("cliente" em vendas e em cobrança)?
2. Quem é dono da definição de cada termo?
3. Qual é a relação entre os contextos (quem depende de quem)?
4. O que cruza a fronteira e exige tradução (campos, estados, identificadores)?

Registre no `context-map.md` (template). Os nomes clássicos de relação (Shared Kernel, Customer/Supplier, Conformist, Anticorruption Layer, Open Host Service, Published Language) são de Evans; a fonte primária não foi lida na fábrica, então use como vocabulário (Inferido) e descreva a relação em palavras. Fowler não trata a relação com microsserviços na página; ligar contexto a serviço é Inferido.

## 3. Agregados: checklist de revisão (V-26)

- [ ] Existe um agregado raiz; o mundo externo referencia só o raiz.
- [ ] Referências entre agregados são por identidade, não por objeto.
- [ ] Uma transação altera um agregado.
- [ ] Consistência entre agregados é eventual (evento, saga).
- [ ] Carrega e grava o agregado inteiro.
- [ ] Invariantes de negócio que precisam de consistência imediata estão dentro do mesmo agregado.
- [ ] Bulkhead e partições se alinham a bounded contexts (V-32).

Sinal de agregado grande demais: bloqueio frequente entre usuários não relacionados. Sinal de pequeno demais: invariante que só se mantém com duas transações (Inferido; Vernon "Effective Aggregate Design" não lido).

## 4. Hexagonal: quatro perguntas (V-25)

1. O núcleo roda em teste sem banco e sem rede?
2. Cada tecnologia externa fica atrás de uma porta com um adaptador?
3. Algum import do núcleo aponta para fora?
4. As portas são simétricas para entrada e saída (portas primárias dirigem a aplicação; secundárias são dirigidas por ela)?

Mock = adaptador em memória. Dependências apontam para dentro. A fonte é de 2005 (atemporal); Clean Architecture e onion compartilham a regra de dependência, mas não foram lidas (Inferido).

## 5. Tabela camada para imports (V-24)

Template `boundary-rules.md`. Exemplo para um serviço com quatro camadas:

| Camada | Pode importar | Não pode importar |
| --- | --- | --- |
| `api` (rotas, handlers) | `services`, `schemas` | `repositories`, `db`, SDKs externos |
| `services` (casos de uso, regras) | `repositories` (por interface), `domain` | `api`, `db`, clientes HTTP concretos |
| `repositories` | `db`, `domain` | `api`, `services` |
| `domain` | biblioteca padrão | tudo o mais do projeto |

Regra de CLAUDE.md na forma positiva, com gatilho de parada: "O domínio não importa adaptadores externos; se parecer necessário, pare e registre a dúvida." Handler com poucas linhas executáveis e arquivos com limite de tamanho são opinião do autor da regra de origem: Suposição configurável.

## 6. Módulos, fachadas e propriedade de esquema (V-28)

- Módulos por capacidade de negócio ou bounded context.
- Internos encapsulados; fachada, API ou evento como contrato; contrato formal por interação.
- Nenhum acesso direto a tabela de outro módulo (propriedade de esquema): consulta via fachada, ou projeção alimentada por evento.
- Código compartilhado entra com regra: comportamento comum e dono; similaridade aparente não basta.
- Critérios de saída: ADR de fronteiras (mapa de módulos, regras de código compartilhado, condições de extração), CI que falha em import proibido, ao menos um caso de violação documentado.

## 7. Verificadores: testes de arquitetura (conceito de fitness function, Inferido)

Fitness function (Ford, Parsons, Kua) é uma verificação automática de uma propriedade arquitetural; a fonte primária não foi lida (lacuna 7), então o termo vale como conceito. Opções para fazer a regra falhar o build:

| Opção | Quando | Observação |
| --- | --- | --- |
| Script de grep no CI | Qualquer linguagem; poucas regras | Seção 8; falsos negativos com DI/reflexão |
| Ferramenta de dependências da linguagem (dependency-cruiser, madge em JS; ArchUnit em JVM) | Regras numerosas | Citadas em V-45 sem execução nem avaliação; ArchUnit é lacuna; instalar pacote é decisão do usuário |
| Lint de imports do próprio linter | Já usa o linter | Confirme suporte na versão |

O plugin não instala nem executa nenhuma delas.

## 8. Script de exemplo (grep) para fronteiras

Exemplo ilustrativo, escrito para este plugin, **não testado** nesta fábrica (Suposição). Adapte nomes de pastas e de pacotes. Rode no CI do projeto, por decisão do usuário.

```bash
#!/usr/bin/env bash
# Falha se o domínio importa camadas externas. Ajuste padrões e caminhos.
set -u
fail=0
check() { # $1=descrição $2=pasta $3=regex proibida
  hits=$(grep -rnE "$3" "$2" --include='*.py' 2>/dev/null)
  if [ -n "$hits" ]; then
    echo "VIOLAÇÃO: $1"; echo "$hits"; fail=1
  fi
}
check "domain não importa adapters/infra/api" src/domain '^(from|import) +(src\.)?(adapters|infra|api)'
check "api não importa repositories diretamente" src/api '^(from|import) +(src\.)?repositories'
exit $fail
```

Limites: encontra imports textuais; não vê import dinâmico, reflexão, nem injeção por configuração (marque ligações assim como Inferido). Um caso de violação documentado (arquivo, linha, correção) prova que o verificador funciona.

## 9. Strangler em 7 passos (V-29)

Fowler (2024): resultados acordados e revisados; achar ou criar seams; começar por componentes pequenos e de baixo risco; arquitetura transitória vale o custo. A página não trata de interceptação de chamadas nem de migração de dados.

1. Resultado mensurável por etapa (ex.: "tráfego de /faturas servido pelo novo módulo: 100% em 8 semanas").
2. Seams candidatos com risco (pontos onde se pode inserir uma fachada).
3. Primeira fatia pequena e de baixo risco.
4. Roteamento de tráfego com volta possível (fachada, proxy ou feature flag: Inferido).
5. Código de convivência marcado com data de remoção.
6. Critério de desligamento do legado (métrica e período sem tráfego).
7. Plano de dados da fatia (propriedade, sincronização, corte): lacuna da fonte; trate como decisão a registrar em ADR.

Cada fase reversível, com verificação própria e plano de rollback (V-45).

## 10. Expand/contract (N-04, Parallel Change; Danilo Sato, 2014)

Expandir (adicionar a interface nova ao lado da antiga), migrar consumidores, contrair (remover a antiga). Aplica-se a contratos de API; aplicação a esquema de banco (adicionar coluna, copiar dados, trocar leitura, depois remover) é Inferido, pois a fonte trata de interface. Detalhes de migração SQL pertencem a `/database-data-modeling:playbook`.

## 11. Métricas de acoplamento (Suposição)

Acoplamento de mudança: percentual de commits em que arquivos do módulo A mudam junto com arquivos do módulo B (`git log --name-only`). O limiar de 50% do material de origem (V-28) é escolha do autor: Suposição. Defina um limiar com o time e registre no ADR de fronteiras. Use como sinal de revisão da fronteira, não como regra de bloqueio.

## 12. Exemplo de saída do `boundary-mapper`

```text
Mapa (resumo): 6 módulos; 11 dependências observadas; 2 violações.
Violações:
 | arquivo:linha            | importa                | regra violada                         |
 | billing/service.py:14    | orders.models.Order    | acesso a tabela/modelo de outro módulo |
 | catalog/api.py:88        | db.session             | api importando camada de dados         |
Regra proposta: ver boundary-rules (tabela camada x imports).
Verificador sugerido: script de grep da seção 8 no CI; revisar com ferramenta de dependências do usuário (Inferido: ligações por DI não aparecem).
Candidato à extração: billing (teste do primeiro serviço: motivo = deploy bloqueado; métrica = Suposição).
```

## 13. Gotchas

- Fowler MonolithFirst é posição argumentada, não experimento. Use com o teste do primeiro serviço e com dados do projeto.
- Encore é fornecedor (classe C): apoio fraco; não cite como evidência de limiar.
- A regra de origem V-24 é exemplo em Python/FastAPI e não nomeia o padrão (hexagonal, clean); a ponte é feita por V-25.
- Listas longas de "não use X" em CLAUDE.md funcionam pior do que regras positivas com gatilho de parada e ponteiro para arquivo de exemplo (V-44, relato de um autor via espelho).
- Ligação em runtime (DI, plugins, mensageria) não aparece em grep: marque Inferido.
- Para microsserviços, o custo de observabilidade e dados é o que mais surpreende; pergunte antes de aprovar a extração.
