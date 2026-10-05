# QA de aplicativos mobile

Use para apps Android/iOS nativos ou híbridos. Comece pelo risco específico do
app e pela base real de dispositivos; uma lista genérica de aparelhos não é
uma estratégia. Emulação de viewport no navegador não executa o binário mobile
nem prova permissões, ciclo de vida, armazenamento ou integrações nativas.

## Sumário

- [Matriz por risco e ferramenta](#matriz-por-risco-e-ferramenta)
- [Ciclo de vida e persistência](#ciclo-de-vida-e-persistência)
- [Rede, sincronização e operações ambíguas](#rede-sincronização-e-operações-ambíguas)
- [Permissões, autenticação e links](#permissões-autenticação-e-links)
- [Instalação, atualização e compatibilidade](#instalação-atualização-e-compatibilidade)
- [Automação confiável e diagnóstico](#automação-confiável-e-diagnóstico)
- [Roteiro mínimo de uma release](#roteiro-mínimo-de-uma-release)

## Matriz por risco e ferramenta

Registre app/build, SO e versão, modelo, resolução, idioma, escala de fonte,
tipo de instalação, estado das permissões, flags e backend. Escolha primeiro
as combinações com usuários e impacto relevantes. Não deduza a versão mínima
suportada pela versão instalada no aparelho disponível.

| Dimensão | Escolha inicial | Quando ampliar |
| --- | --- | --- |
| SO | mínima suportada e versão representativa atual da base | mudança de SDK, APIs nativas, permissões ou incidente em uma versão |
| Hardware | aparelho representativo e um com recursos limitados | câmera, NFC, biometria, memória, fabricante ou problema térmico |
| Tela e entrada | tela pequena + fonte ampliada | tablet, dobrável, orientação ou teclado especial no escopo |
| Distribuição | instalação limpa + atualização desde versão em uso | migração de banco local, assinatura, login ou esquema de armazenamento |
| Rede | estável + interrupção no fluxo crítico | app offline, upload, streaming, rede corporativa ou reconexão frequente |
| Acessibilidade | TalkBack/VoiceOver e fonte ampliada no fluxo crítico | componentes novos, gestos próprios, gráficos ou controles sem rótulo |

Use emulador/simulador para retorno rápido e estados reproduzíveis; valide em
aparelhos físicos os riscos que dependem do hardware, consumo, rede real ou
comportamento de fabricante. O Android distingue testes locais e
instrumentados e admite emulador ou dispositivo nos instrumentados; isso não
torna os ambientes equivalentes. Veja [fundamentos de testes Android](https://developer.android.com/training/testing/fundamentals).

| Abordagem | Boa adequação | Limite que precisa ficar explícito |
| --- | --- | --- |
| Testes de regra/view-model | estados, cálculo, validação e sincronização controlada | não provam renderização ou integração com o SO |
| Espresso/Compose no Android | time próximo ao código Android, componentes e UI | selecionar abordagem compatível com a tecnologia de UI do projeto |
| XCTest + XCUIAutomation | fluxos e estado da UI Apple | exige infraestrutura e configuração do projeto Apple |
| Appium | automação externa por drivers, mais de uma plataforma | servidor, driver e cliente têm compatibilidades próprias |
| Maestro | jornadas declarativas com seletores visíveis/IDs | validar suporte às interações nativas necessárias antes de migrar a suíte |
| Exploração em aparelho | interrupções, ergonomia, acessibilidade e falhas difíceis de modelar | registrar estado e evidência para tornar o achado reproduzível |

Preserve o stack do projeto se ele atende ao risco. Para código de ferramenta,
confira versões instaladas e documentação do driver; Appium delega automação
a drivers instalados separadamente ([drivers do Appium](https://appium.io/docs/en/latest/intro/drivers/)).
Na plataforma Apple, UI usa XCTest com XCUIAutomation
([documentação Apple](https://developer.apple.com/documentation/xcuiautomation)).
Não gere capabilities, gestos ou comandos de sessão de memória quando a
versão é desconhecida.

## Ciclo de vida e persistência

“Fechei e abri” é ambíguo. Identifique exatamente a transição. Navegar para
Home, recriar uma tela, remover o app da lista de recentes, forçar parada,
encerrar o processo e reinstalar podem ter efeitos diferentes. No Android,
“Don't keep activities” destrói activities quando se sai delas; não é prova
de todos os cenários de morte do processo. Veja a descrição da
[opção de desenvolvedor](https://developer.android.com/studio/debug/dev-options).

| Momento de interrupção | Ação controlada | Resultado observável a definir/testar |
| --- | --- | --- |
| formulário parcialmente preenchido | alternar de app e retornar | campos preservados conforme regra; dados sensíveis tratados conforme política |
| resposta crítica pendente | enviar a segundo plano e encerrar processo de teste | ao reabrir, consultar a operação existente; não criar nova cobrança automaticamente |
| tela com conteúdo autenticado | bloquear dispositivo; expirar sessão; retomar | exigir autenticação quando previsto; não exibir dado de outra sessão |
| upload parcial | interromper processo e reabrir | retomar ou reiniciar conforme contrato, sem arquivo corrompido/duplicado |
| mudança de configuração | girar tela ou alterar tamanho quando suportado | estado coerente, sem submissão duplicada, controles utilizáveis |
| fila offline persistida | reiniciar app e dispositivo | fila preserva identidade, ordem necessária e estado de confirmação |

Escolha o esperado com produto e segurança: preservar todo dado sempre pode
ser tão errado quanto perder tudo. Teste também sair da conta A e entrar na B
no mesmo dispositivo: cache, notificações, busca recente, anexos e fila não
podem vazar entre contas.

## Rede, sincronização e operações ambíguas

Modele pelo menos: rede disponível, sem rede, latência, conexão interrompida
antes do envio e resposta perdida **depois de o servidor processar**. Timeout
no cliente não prova que a operação falhou no servidor.

Exemplo: transferência sintética de R$ 10,00 em sandbox, saldo inicial
R$ 100,00, identificador `op-qa-001`. O servidor efetiva e a resposta não chega.
Ao reconectar, a UI deve consultar/reconciliar essa identidade conforme o
contrato. Oráculo: uma transferência, saldo R$ 90,00, comprovante referente à
mesma operação; ausência de segunda cobrança. “Mensagem de erro apareceu”
não valida integridade financeira.

| Caso | Verificação importante |
| --- | --- |
| offline antes do envio | nenhum sucesso fictício; mensagem e opção de recuperação; estado local explícito |
| duas tentativas por toque/retry | identidade de operação preservada quando aplicável; um efeito |
| expiração de token durante sincronização | refresh coordenado ou login; fila não descartada silenciosamente |
| conflito com edição em outro dispositivo | regra definida de versão, merge ou recusa; nenhuma perda invisível |
| resposta antiga após consulta nova | UI não retrocede para dado obsoleto por ordem de chegada |
| troca Wi-Fi/dados móveis | operação mantém estado consistente, sem loop de requisições |
| relógio local errado | prazo e autenticação respeitam fonte de tempo definida; informar limitação quando necessário |

Uma política de conflito como “última escrita vence” precisa definir qual
relógio/versão manda; horário local de dois aparelhos não dá uma ordem
confiável por si só. Em filas com retry, verifique limite, backoff,
cancelamento, retenção e tratamento de erro permanente. Esperar indefinidamente
pela sincronização é um defeito observável, não apenas um teste lento.

## Permissões, autenticação e links

Para cada permissão realmente usada, cubra primeira solicitação, recusa,
aceite, mudança nas configurações e retorno ao app. Acrescente concessão
temporária ou parcial se existir na combinação SO/API do projeto. O esperado
deve distinguir a função bloqueada das funções que podem continuar.

- **Câmera/documentos:** recusa não fecha o app; cancelamento volta ao fluxo;
  captura inválida não passa como anexo aceito. Teste arquivo vazio, tamanho,
  orientação e formato nos níveis adequados.
- **Biometria:** sucesso, cancelamento, indisponibilidade e fallback previsto.
  Use mecanismos de simulação suportados ou identidades de teste. Simular
  sucesso biométrico testa a reação do app, não a segurança do sensor.
- **Sessão:** expiração em segundo plano, logout, revogação, troca de conta e
  aparelho compartilhado. Token não deve aparecer em log, vídeo ou relatório.
- **Deep/universal/app link:** app fechado, em segundo plano e aberto; sessão
  ausente; parâmetro inválido; recurso inexistente e recurso de outra conta.
  Abrir uma rota não concede autorização sobre o objeto.
- **Notificação:** receber e tocar são eventos distintos. Verifique conteúdo
  permitido na tela bloqueada, destino correto, ação duplicada, item removido
  e usuário que já saiu da conta. Entrega depende de SO/provedor; separe teste
  do handler de teste da entrega real.

Para segurança mais ampla, use [segurança](seguranca.md). Para TalkBack,
VoiceOver, foco, ordem e rótulos, use [acessibilidade](acessibilidade.md).
Seletores de teste não substituem nomes acessíveis úteis a pessoas.

## Instalação, atualização e compatibilidade

Não limpe dados antes do teste que pretende provar atualização. Prepare um
perfil sintético na versão anterior, mantenha-o instalado e atualize pelo
caminho compatível com a distribuição. Inclua histórico, cache, preferências,
fila pendente, sessão e banco local nos estados que a mudança pode afetar.

1. Registre build anterior, identidade sintética e estado persistido.
2. Atualize para o artefato candidato e registre sua identidade exata.
3. Confira abertura, migração, autenticação, itens e totais reconciliados.
4. Execute uma leitura e uma escrita importantes; só abrir a home é pouco.
5. Teste falha/interrupção de migração em ambiente controlado quando esse é o
   risco; confirme recuperação e ausência de alteração parcial.

Backends convivem com apps antigos em campo. Cubra cliente anterior ainda
suportado contra backend novo e a política de atualização obrigatória.
Rollback de backend não remove binários já distribuídos; rollback de app nem
sempre é instantâneo ou possível pelo mesmo canal. Planeje compatibilidade,
flags remotas e recuperação de dados antes da liberação.

Instalação limpa, atualização e reinstalação são cenários diferentes. Não
assuma que desinstalar apaga todo estado, pois sistemas de backup, credenciais
e restauração podem participar. Observe o mecanismo efetivamente habilitado.

## Automação confiável e diagnóstico

Prepare contas e registros sintéticos por API/fixture quando a criação pela
UI não for o comportamento em teste. Redefina permissões, sessão e dados
necessários, sem apagar o estado que o cenário de atualização exige.

Localize por semântica e identificador estável exposto pelo app; texto serve
quando faz parte do comportamento e o idioma está controlado. Coordenadas,
índices e XPath longo quebram com teclado, tela e conteúdo. Quando um gesto
precisa de coordenadas, derive-as de um elemento observado e valide o efeito.

Aguarde condição com limite e evidência do estado final. No Maestro,
`assertVisible` já aguarda o elemento até seu timeout; essa espera da asserção
não equivale a repetir uma ação de negócio. Veja
[assertVisible](https://docs.maestro.dev/reference/commands-available/assertvisible).
Repetir “Confirmar pagamento” para contornar lentidão pode duplicar a operação.

Na falha, capture build/commit, dispositivo e SO, estado inicial, etapas,
timestamp com fuso, screenshot/hierarquia de UI, logs redigidos e ID da
operação. Preserve o primeiro erro antes de repetir o teste. Se a UI mostra
sucesso e a API não, registre ambos; não escolha o resultado mais favorável.

Para lentidão, separe partida fria/quente, bloqueio de UI, tempo do servidor,
renderização e consumo prolongado. Defina metas e compare com baseline no
mesmo perfil; execução em debug com logs intensos não representa a release.
ANR, crash, travamento visível, memória e bateria pedem observação específica,
não somente cronômetro no teste E2E.

## Roteiro mínimo de uma release

Adapte à mudança; não trate esta lista como certificação universal:

- Uma jornada crítica com resultado persistido na matriz escolhida.
- Interrupção e retomada no ponto de maior risco dessa jornada.
- Operação com resposta perdida, quando houver efeito remoto relevante.
- Atualização preservando dados, se a release toca armazenamento, sessão ou SDK.
- Negativo de permissão/autorização relevante e troca de conta.
- Uso do fluxo com leitor de tela e fonte ampliada nas partes alteradas.
- Evidências da versão candidata, lacunas e risco residual por plataforma.

Se só houve emulador Android, escreva exatamente isso. Não estenda o resultado
a iOS, aparelho físico ou distribuição de loja sem execução correspondente.
