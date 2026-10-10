# Domínio, agregados e migração gradual

Sumário: 1. Bounded contexts e context map · 2. Agregados · 3. Strangler fig em 7 passos · 4. Expand/contract · 5. Exemplo de plano de extração · 6. Gotchas

Validado em 2026-10-10. Fontes: V-26 (Fowler: Bounded Context, 15/01/2014; Aggregate, 23/04/2013), V-29 (Strangler Fig, Fowler, 22/08/2024), N-04 (Parallel Change, Danilo Sato, 13/05/2014; versão de interface), V-28. Lacunas de fonte primária: DDD de Evans e Vernon, expand/contract para esquema de banco. Itens nessa situação saem como Inferido. Redação própria.

## 1. Bounded contexts e context map

Ideia (V-26): um modelo único para o negócio todo não funciona. Cada contexto tem modelo e linguagem próprios; mudança de linguagem costuma marcar a fronteira; as relações entre contextos devem ser nomeadas e documentadas em um context map.

Perguntas de mapeamento:

1. Que termos têm sentido diferente entre áreas? (Exemplo: "cliente" em vendas é quem compra; em suporte é quem abre chamado; em faturamento é o pagador.)
2. Quem é dono de cada definição? Um dono por termo por contexto.
3. Qual é a relação entre os contextos (quem depende de quem; quem dita o contrato)?
4. O que cruza a fronteira e precisa de tradução (campos, estados, identificadores)?
5. Qual time mantém cada contexto? (Lei de Conway: a fronteira que contraria a organização tende a erodir; Inferido.)

Vocabulário comum de relações entre contextos (conhecimento do DDD de Evans, sem fonte primária lida neste plugin: Inferido): parceria, núcleo compartilhado, cliente-fornecedor, conformista, camada anticorrupção, serviço aberto com linguagem publicada, caminhos separados. Use-o para nomear a relação, mas explique cada uma em linguagem simples no mapa.

Saída: tabela com contexto, dono, termos-chave, relação com os vizinhos, tradução na fronteira (modelo `context-map.md` do playbook).

## 2. Agregados

Regras (V-26), como checklist de revisão:

- [ ] Existe um **raiz**; entidades internas só são acessadas por ele.
- [ ] Referências vindas de fora apontam para o raiz, por **identidade** (id), não por objeto.
- [ ] Uma **transação por agregado**; transação que atravessa agregados é sinal de fronteira errada.
- [ ] Consistência **entre** agregados é eventual (eventos, outbox, consumidor idempotente; skill `resilience-and-consistency`).
- [ ] O agregado é carregado e gravado inteiro; se for grande demais para isso, o limite está largo.
- [ ] Invariantes do negócio são garantidas **dentro** do agregado (ex.: "total do pedido = soma dos itens").

Detecção por leitura: transações que gravam duas entidades de contextos diferentes; classes que guardam referência de objeto para o raiz de outro contexto; ORM com carregamento preguiçoso atravessando fronteiras.

## 3. Strangler fig em 7 passos (V-29, passos 4 e 7 são acréscimos)

A fonte (Fowler, 2024) trata de resultados acordados e revisados, de achar ou criar seams, de começar por componentes pequenos e de baixo risco, e de aceitar o custo de uma arquitetura transitória. Ela não trata de interceptação de chamadas nem de migração de dados (confirmado em VALIDATED).

1. **Resultado mensurável por etapa** (ex.: "faturamento responde por 100% das faturas novas com p95 < X"): acordado e revisado com as pessoas envolvidas.
2. **Seams candidatos:** pontos onde o comportamento pode ser interceptado ou substituído (fachada existente, limite de módulo, fila). Liste com risco.
3. **Primeira fatia pequena** e de baixo risco, que ensine a equipe sobre o caminho.
4. **Roteamento de tráfego com volta possível** (Inferido: fachada ou proxy que decide entre legado e novo, por feature flag, por tenant ou por percentual). Deve existir um modo de voltar ao legado sem deploy.
5. **Código de convivência marcado com data de remoção** (cola, adaptadores, escrita dupla); sem data, vira permanente.
6. **Critério de desligamento do legado:** medida (zero tráfego por N semanas), checagem de dependentes ocultos (jobs, relatórios), plano de arquivamento.
7. **Plano de dados da fatia** (Inferido; lacuna da fonte): quem é o dono do dado durante a convivência, como migrar (carga inicial, replicação, escrita dupla), como verificar equivalência (contagem origem vs destino, amostras, soma de verificação), como reverter.

Cada passo é uma fase reversível com verificação própria (V-45).

## 4. Expand/contract (Parallel Change, N-04)

Padrão (N-04, versão de interface de Danilo Sato): mudar um contrato sem quebrar clientes em três movimentos:

1. **Expandir:** adicionar o novo comportamento ao lado do antigo (novo campo, novo método, nova tabela ou coluna), aceitando ambos.
2. **Migrar:** mover cada cliente para o novo, um por vez, verificando.
3. **Contrair:** remover o antigo quando ninguém mais o usa.

Aplicação a banco de dados (Inferido; a fonte lida cobre a versão de interface): para renomear a coluna `status` em `pedido` para `situacao`:

1. Expandir: criar `situacao` (anulável) e passar a gravar nas duas colunas.
2. Migrar: carregar os dados antigos em lotes (backfill), conferir contagem e amostra, mudar leituras para `situacao`, um serviço por vez.
3. Contrair: parar de gravar `status`, aguardar um ciclo de observação, remover a coluna em migração separada.

Cada etapa é um deploy independente e reversível até a contração; a contração é a etapa irreversível: só com aprovação humana e backup verificado. Não prometa rollback de dados só porque existe migração `down` (brain-of-agent).

## 5. Exemplo de plano de extração (fictício)

Caso: extrair `faturamento` de um monólito. Premissas rotuladas Suposição.

| Fase | Mudança | Verificação | Reversão |
| --- | --- | --- | --- |
| 0 | Definir módulo `billing` dentro do monólito, fachada pública, regra de dependência e verificador no CI | Verificador falha com import proibido de exemplo; ADR proposto | Remover a regra |
| 1 | Mover leitura de tabelas de faturamento para dentro da fachada; proibir acesso direto de outros módulos | `grep` de nomes de tabela fora do módulo = 0 ocorrências | Reverter commits |
| 2 | Expandir: criar o serviço novo com API equivalente (contrato versionado) e escrita dupla de faturas novas | Contagem origem vs destino igual por dia (Suposição: janela de 2 semanas) | Desligar escrita dupla |
| 3 | Rotear 5% das leituras para o serviço novo (flag por tenant) | Comparação de respostas; p95 dentro da meta | Flag volta a 0% |
| 4 | Migrar o restante em degraus; backfill de faturas antigas | Verificação por soma de totais e amostra | Flag para o legado enquanto a escrita dupla existir |
| 5 | Contrair: parar escrita dupla, desligar o código do legado, remover tabelas após período de observação | Zero tráfego legado por 4 semanas (Suposição) | Restaurar de backup (decisão humana; irreversível sem ele) |

## 6. Gotchas

- Dividir pelo organograma ou por camadas técnicas (um serviço "de banco", outro "de UI") gera dependência circular; divida por capacidade de negócio.
- Camada anticorrupção é custo: use onde o modelo vizinho é ruim ou instável, não por padrão.
- Escrita dupla sem verificação de equivalência apodrece em silêncio; a comparação é parte da fase.
- Expand/contract exige disciplina de remover: sem data de contração, o esquema acumula versões.
- Evans e Vernon não foram lidos; terminologia de relações entre contextos é conhecimento geral (Inferido).
