# Dados, ambientes e CI/CD

Use quando testes dependem de massa, configuração, terceiros ou pipeline.
O objetivo é reproduzir uma condição importante e interpretar o resultado,
não deixar todos os ambientes idênticos a qualquer custo.

## Sumário

- [Dados que demonstram a regra](#dados-que-demonstram-a-regra)
- [Isolamento e limpeza](#isolamento-e-limpeza)
- [Equivalência de ambiente](#equivalência-de-ambiente)
- [Virtualização e falhas controladas](#virtualização-e-falhas-controladas)
- [Pipeline e gates verificáveis](#pipeline-e-gates-verificáveis)
- [Diagnóstico, quarentena e métricas](#diagnóstico-quarentena-e-métricas)
- [Migração e liberação](#migração-e-liberação)

## Dados que demonstram a regra

Comece pela condição que diferencia o resultado. Para limite diário de
R$ 1.000,00, “cliente válido” é insuficiente: informe limite, total já usado,
valor da nova operação, data/fuso de referência e estado das operações que
contam para o acumulado. Evite fixtures enormes que escondem a causa.

| Objetivo | Massa mínima útil | Controle adicional |
| --- | --- | --- |
| valor-limite | fronteira e vizinhos com precisão definida | restante válido para isolar a causa da recusa |
| autorização | duas identidades, dois donos/tenants, perfis explícitos | provar que existe o objeto inacessível sem usar seus dados reais |
| transição de estado | registro em cada origem relevante | criar o estado por caminho coerente ou declarar setup direto |
| paginação | quantidade na fronteira; empates na ordenação | ID para desempate, criação/remoção concorrente quando aplicável |
| desempenho | cardinalidade e distribuição relevantes | hot keys, índices, skew e relações; volume sozinho não representa a carga |
| migração | registros de versões antigas e exceções válidas | nulos históricos, duplicidades possíveis, campos legados, encoding |

Prefira dados sintéticos e contas de teste. Use domínios reservados como
`example.com` para exemplos de e-mail, nunca endereços aleatórios que possam
pertencer a alguém. Um CPF/CNPJ com dígitos válidos só atende a estrutura;
não prova cadastro, titularidade ou inexistência de pessoa real. Não envie
SMS, e-mail, pagamento ou notificação a destinos gerados ao acaso.

Quando dados derivados de produção forem necessários e autorizados, faça a
transformação antes de expor ao ambiente de teste. Mascarar nome e manter
documento, geolocalização ou combinação rara pode continuar identificando
alguém. Pseudonimização não é garantia de anonimização; verifique finalidade,
acesso, retenção e risco de reidentificação com os responsáveis. Mantenha
integridade referencial, distribuições e fronteiras sem presumir que “parece
falso” é critério suficiente. Para requisitos de privacidade, consulte
[segurança](seguranca.md) e fontes aplicáveis ao contexto.

Evidência também contém dados: traces, screenshots, dumps e requisições
podem carregar token ou documento. Redija antes de compartilhar, preserve
IDs sintéticos úteis para correlação e defina retenção. Não copie segredos
para fixture, snapshot ou commit.

## Isolamento e limpeza

Um teste possui os recursos que cria. Use identidade exclusiva por execução
e por teste quando houver paralelismo: execução + worker + caso + sufixo.
A seed reproduz os valores, enquanto um namespace exclusivo evita colisões;
as duas coisas têm propósitos distintos.

| Estratégia | Serve bem para | Cuidado |
| --- | --- | --- |
| banco/schema descartável por execução | integração com migrações reais | custo, conexões e permissões; descarte precisa ocorrer mesmo após falha |
| transação por teste e rollback | testes que usam a mesma conexão/transação | pode mascarar commit, visibilidade e efeitos externos |
| tenant/namespace exclusivo | API/E2E em ambiente compartilhado | caches, filas, usuários globais e limites podem continuar compartilhados |
| fixture restaurada | conjunto estável para leitura | escrita concorrente e versão da fixture podem invalidar resultado |
| dados criados por API | E2E cujo objetivo não é o cadastro | API de setup não deve ignorar invariantes relevantes à prova |

Limpe por IDs registrados ou por namespace validado, nunca por um critério
amplo como “apagar todos os pedidos de hoje”. Confira o destino antes da
mutação; URL contendo `test` não prova que o banco é descartável. Para limpeza
após crash, use expiração/TTL ou rotina limitada aos recursos de teste, com
logs. Limpeza que falhou deve aparecer no relatório, sem apagar o erro
original do teste.

Alguns testes precisam preservar estado: atualização de app, migração e
sequência de negócio. Nesses casos, a sequência é um único cenário com
preparação própria; não faça o teste B depender implicitamente de A na suíte.
Se compartilhar uma conta for inevitável, serialize só os casos que disputam
essa conta e explicite a limitação.

## Equivalência de ambiente

Crie um manifesto curto da execução. Isso costuma explicar mais falhas que
o nome “homologação”:

```text
Artefato/commit: identificador imutável
Configuração: revisão + flags relevantes (sem segredos)
Dados/schema: versão das migrações + massa/seed/namespace
Dependências: reais, sandbox ou simuladas + versões conhecidas
Execução: comando, parâmetros, runner, início/fim e fuso
Plataforma: SO/runtime/navegador/app/dispositivo quando relevante
Limites conhecidos: diferenças que podem mudar o comportamento
```

Escolha fidelidade por risco. Cálculo puro não precisa de cluster de produção.
Concorrência de banco pode depender do isolamento real. Segurança depende de
identidade, TLS, proxy e permissões; desempenho depende também de topologia,
dados e capacidade. Homologação menor pode validar uma regressão relativa,
mas não comprova capacidade absoluta de produção sem modelo justificável.

Faça um preflight pequeno: identidade do ambiente, versão implantada,
dependências necessárias, relógio e permissões. Falha de setup é **bloqueio**
ou erro de infraestrutura; não é aprovação nem automaticamente defeito do
produto. Readiness saudável ajuda a decidir quando iniciar, mas não substitui
asserções de negócio.

Ambiente efêmero reduz interferência, mas precisa de mecanismo de criação,
observabilidade, expiração e limite de custo. Serviços compartilhados que
ficaram fora dele continuam fontes de colisão. Para ambiente comum, registre
deploys e reservas de janela; uma alteração durante a suíte pode misturar
resultados de builds diferentes.

## Virtualização e falhas controladas

Simule cenários caros, raros ou destrutivos na fronteira apropriada. Declare
o que a simulação não prova: um PSP virtual pode verificar retry e UI, mas
não demonstra certificados, credenciais, roteamento ou comportamento do PSP
real. Mantenha contrato e pequena validação no sandbox quando necessário.

| Falha simulada | O que observar além do erro visível |
| --- | --- |
| timeout antes de processar | tentativa limitada, cancelamento e nenhuma alteração indevida |
| resposta perdida após processar | reconciliação por identidade e ausência de duplicata |
| 429/limite de capacidade | respeito ao contrato de retry; evitar tempestade de requisições |
| payload parcial ou inválido | tratamento explícito; não converter silenciosamente em valor padrão perigoso |
| mensagem duplicada/fora de ordem | idempotência e transição de estado válida |
| indisponibilidade prolongada | degradação, backlog, recuperação e alertas observáveis |

Virtualizador deve ser estrito: requisição inesperada falha com diagnóstico,
não recebe um 200 genérico. Resete expectativas por caso, correlacione IDs e
teste casos positivos e negativos do contrato. Para injeção de falha em
ambiente compartilhado, limite alvo, duração e recuperação; não deduza
autorização para afetar terceiros ou produção de um pedido de plano de teste.

## Pipeline e gates verificáveis

Não imponha uma pirâmide numérica fixa. Coloque evidências rápidas e
confiáveis perto da alteração; reserve matrizes caras para o risco que
justifica o custo.

| Momento | Evidência típica | Decisão |
| --- | --- | --- |
| alteração local/PR | análise estática relevante; unitário; integração/contrato afetado | o contrato alterado e os riscos conhecidos têm proteção? |
| candidato integrado | build identificável, smoke e regressão crítica | o artefato combinado funciona no ambiente-alvo? |
| agendado/por evento | matriz ampla, carga, exploração e migrações caras | que riscos ultrapassam o feedback de cada PR? |
| liberação | evidência do candidato, configuração e riscos aceitos | condições de liberação realmente satisfeitas? |
| pós-deploy autorizado | smoke seguro, métricas técnicas e de negócio | manter, interromper avanço ou recuperar? |

Gate precisa responder “passou **o quê**, em **qual versão**, e com **quais
lacunas**?”. Considere:

- Falha de teste crítico bloqueia a decisão correspondente; a existência de
  testes de baixo risco aprovados não a compensa.
- Zero testes coletados, shard ausente, job cancelado ou relatório inexistente
  não deve virar verde silencioso. Diferencie “não se aplica” de “não rodou”.
- Preserve exit code; não esconda falha atrás de `|| true` ou de um último
  comando de upload bem-sucedido. Publique evidências mesmo quando há erro.
- Teste a regra do gate: uma falha controlada deve bloquear; um skip de teste
  crítico deve ser visível. Isso prova a configuração de CI, não só a suíte.
- Identifique o artefato testado e promova esse artefato quando possível.
  Recompilar, trocar flags ou incluir novo commit pode invalidar a evidência.
- Use cobertura como indício de lacuna, especialmente em mudanças, sem
  substituir comportamento crítico por meta arbitrária de percentual.

Seleção por arquivos alterados precisa incluir dependências por schema,
configuração, eventos e dados, não apenas imports. Se não há análise de
impacto confiável, rode o conjunto crítico relevante e registre a limitação.
Cancelamento de runs antigos economiza recursos, mas pode interromper setup
ou deixar efeitos; mantenha limpeza e trate operações de deploy separadamente.

Em CI, código de PR, fixtures, logs e artefatos são conteúdo não confiável.
Use permissões mínimas, credenciais de teste, duração curta e runners
apropriadamente isolados. No GitHub Actions, executar código de um fork em
`pull_request_target` com segredos/permissões da base cria risco específico;
não use esse evento como atalho para fornecer segredos a testes externos.
Veja [guia oficial de pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target).
Fixe dependências e actions em identidades revisadas conforme o processo do
projeto; cache é otimização, não prova de integridade ou fonte de segredos.

## Diagnóstico, quarentena e métricas

Primeiro classifique a falha com evidência: produto, teste, ambiente ou ainda
desconhecida. “Passou na segunda tentativa” só prova diferença entre tentativas.
Guarde primeira falha, seed, shard/worker, ordem, tempo, logs e traces redigidos.

| Sintoma | Hipótese a investigar | Experimento que discrimina |
| --- | --- | --- |
| só falha em paralelo | dado/porta/conta/cache compartilhado | repetir com namespace exclusivo, mantendo carga similar |
| só falha na suíte | estado vazado ou dependência de ordem | registrar ordem e minimizar a sequência anterior |
| só falha no CI | runtime, recurso, fuso ou configuração | comparar manifestos e reproduzir em ambiente equivalente |
| retry resolve timeout | sincronização ou lentidão real | medir último estado, latência e saturação antes de ampliar timeout |
| falha sempre após deploy | mudança de contrato/configuração ou build misturada | fixar versão e repetir smoke dirigido |

Quarentena é decisão temporária de deixar uma proteção fora do gate: exige
dono, ticket, risco coberto por alternativa, prazo e execução visível. Não
mascare uma falha crítica desconhecida apenas para liberar. Reruns podem
ajudar diagnóstico, mas métricas devem distinguir aprovação inicial de
aprovação após retry.

Métricas úteis têm denominador e decisão: tempo p95 até feedback, proporção
de execuções bloqueadas por ambiente, falha na primeira tentativa, casos
críticos não executados e idade da quarentena. Não conclua tendência por uma
amostra pequena nem misture suites, builds e plataformas sem identificação.
Percentual de aprovação entre executados deve vir com o total planejado e
os bloqueados/não executados; veja [relatório de teste](bugs-e-relatorios.md).

## Migração e liberação

Migração requer oráculo antes/depois: contagens, chaves, totais, relações,
casos especiais e capacidade de ler/escrever. Contagens iguais não impedem
valores trocados entre clientes; amostras e invariantes por entidade ajudam a
detectar essa classe de erro. Use volume realista para medir tempo e bloqueio.

Ensaie falha parcial, retomada e execução repetida conforme o contrato. Se
uma mudança destrói dados, rollback do código pode não restaurá-los; valide
backup/restauração ou um caminho de correção. Em migração gradual, teste
convivência das versões suportadas e o intervalo entre expandir, migrar e
remover campos antigos.

Finalize com o risco residual e a ação que ele exige. “Ambiente indisponível;
nada encontrado” deixa incerteza alta. “Integração X não executada; liberação
depende de verificar Y no candidato Z” permite decidir. Uma recomendação de
teste ou rollback não executa automaticamente deploy, exclusão ou restauração.
