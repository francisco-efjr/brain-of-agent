# Matriz de risco, ciclo de vida e rede (QA mobile)

Fonte principal: `brains/qa/references/mobile.md` do brain-of-agent (conteúdo próprio do usuário, MIT), condensado e adaptado a este plugin. Complementos: V-08 (Android), V-59 (offline), V-65 a V-70. Verificado em 2026-10-10. Os links do arquivo original para outros brains foram trocados por referências deste plugin.

## 1. Matriz por risco

Registre: app/build, SO e versão, modelo, resolução, idioma, escala de fonte, tipo de instalação, estado das permissões, flags e backend. Escolha primeiro as combinações com mais usuários e impacto. **Não deduza a versão mínima suportada** pela versão instalada no aparelho disponível.

| Dimensão | Escolha inicial | Quando ampliar |
| --- | --- | --- |
| SO | mínima suportada + versão atual representativa | mudança de SDK, APIs nativas, permissões; incidente em uma versão |
| Hardware | aparelho representativo + um com recursos limitados | câmera, NFC, biometria, memória, fabricante, térmico |
| Tela e entrada | tela pequena + fonte ampliada | tablet, dobrável, orientação, teclado especial |
| Distribuição | instalação limpa + atualização desde a versão em uso | migração de banco local, assinatura, login, esquema de armazenamento |
| Rede | estável + interrupção no fluxo crítico | offline, upload, streaming, rede corporativa, reconexão frequente |
| Acessibilidade | TalkBack/VoiceOver + fonte ampliada no fluxo crítico | componentes novos, gestos próprios, gráficos, controles sem rótulo |

Emulador/simulador: retorno rápido e estados reproduzíveis. Aparelho físico: riscos de hardware, consumo, rede real, comportamento de fabricante. Os dois **não são equivalentes**.

## 2. Ciclo de vida e persistência

"Fechei e abri" é ambíguo: Home, recriar tela, remover dos recentes, forçar parada, encerrar processo e reinstalar têm efeitos diferentes. No Android, "Don't keep activities" destrói activities ao sair delas e não prova todos os cenários de morte de processo.

| Momento de interrupção | Ação controlada | Resultado a definir/testar |
| --- | --- | --- |
| Formulário parcial | alternar de app e voltar | campos preservados conforme regra; dados sensíveis tratados conforme política |
| Resposta crítica pendente | segundo plano + encerrar processo de teste | ao reabrir, consultar a operação existente; **não** criar nova cobrança |
| Tela autenticada | bloquear aparelho; expirar sessão; retomar | autenticar quando previsto; não exibir dado de outra sessão |
| Upload parcial | interromper e reabrir | retomar ou reiniciar conforme contrato, sem arquivo corrompido/duplicado |
| Mudança de configuração | girar tela / redimensionar | estado coerente, sem submissão duplicada |
| Fila offline persistida | reiniciar app e aparelho | identidade, ordem e estado de confirmação preservados |

Preservar todo dado sempre pode ser tão errado quanto perder tudo: defina o esperado com produto e segurança. **Troca de conta A→B** no mesmo aparelho: cache, notificações, busca recente, anexos e fila não vazam entre contas.

## 3. Rede, sincronização e operações ambíguas

Modele: rede disponível, sem rede, latência, conexão interrompida antes do envio e **resposta perdida depois de o servidor processar**. Timeout no cliente não prova falha no servidor.

Exemplo sintético: transferência de R$ 10,00 em sandbox, saldo inicial R$ 100,00, identificador `op-qa-001`. O servidor efetiva e a resposta não chega. Ao reconectar, a UI consulta/reconcilia a identidade. Oráculo: **uma** transferência, saldo R$ 90,00, comprovante da mesma operação, sem segunda cobrança. "Apareceu mensagem de erro" não valida integridade.

| Caso | Verificação |
| --- | --- |
| Offline antes do envio | nenhum sucesso fictício; mensagem e recuperação; estado local explícito |
| Duas tentativas por toque/retry | identidade de operação preservada; um efeito |
| Expiração de token na sincronização | refresh coordenado ou login; fila não descartada em silêncio |
| Conflito com edição em outro aparelho | regra de versão, merge ou recusa; nenhuma perda invisível |
| Resposta antiga após consulta nova | UI não retrocede por ordem de chegada |
| Troca Wi-Fi/dados móveis | estado consistente, sem loop de requisições |
| Relógio local errado | prazo e autenticação respeitam a fonte de tempo definida |

"Última escrita vence" exige definir qual relógio ou versão manda; hora local de dois aparelhos não dá ordem confiável. Em filas com retry, verifique limite, backoff, cancelamento, retenção e tratamento de erro permanente. Esperar para sempre pela sincronização é defeito observável.

## 4. Permissões, autenticação e links (casos)

- Permissão: primeira solicitação, recusa, aceite, mudança nas configurações e retorno ao app; função bloqueada distinta das que continuam.
- Biometria: sucesso, cancelamento, indisponibilidade, fallback. Simulação testa a reação do app, não a segurança do sensor.
- Sessão: expiração em segundo plano, logout, revogação, troca de conta, aparelho compartilhado; token não aparece em log, vídeo ou relatório.
- Deep link: app fechado/segundo plano/aberto; sessão ausente; parâmetro inválido; recurso inexistente; recurso de outra conta. Abrir rota não concede autorização.
- Notificação: receber ≠ tocar; conteúdo na tela bloqueada; destino; ação duplicada; item removido; usuário que saiu.

## 5. Instalação, atualização e compatibilidade

Não limpe dados antes do teste que pretende provar atualização.

1. Registre build anterior, identidade sintética e estado persistido.
2. Atualize para o artefato candidato (identidade exata registrada).
3. Confira abertura, migração, autenticação, itens e totais reconciliados.
4. Execute uma leitura e uma escrita importantes (abrir a home é pouco).
5. Teste falha/interrupção de migração em ambiente controlado quando esse é o risco.

Backends convivem com apps antigos: cubra o cliente anterior suportado contra o backend novo e a política de atualização obrigatória. Rollback de backend não remove binários distribuídos; rollback de app não é instantâneo.

## 6. Automação confiável

Contas e registros sintéticos por API/fixture; redefina permissões, sessão e dados sem apagar o estado que a atualização exige. Localize por semântica ou identificador estável (coordenadas, índices e XPath longo quebram). Aguarde condição com limite. No Maestro, `assertVisible` já aguarda o elemento até o timeout — isso não equivale a repetir uma ação de negócio: **repetir "Confirmar pagamento" para contornar lentidão pode duplicar a operação.**

Na falha, capture: build/commit, aparelho e SO, estado inicial, passos, timestamp com fuso, screenshot/hierarquia de UI, logs redigidos, ID da operação. Preserve o **primeiro** erro antes de repetir. Se a UI mostra sucesso e a API não, registre os dois.

Lentidão: separe partida fria/quente, bloqueio de UI, servidor, renderização e consumo prolongado; defina metas e compare com baseline no mesmo perfil. ANR, crash, memória e bateria pedem observação específica, não só cronômetro de E2E.

## 7. Roteiro mínimo de uma release

Adapte à mudança; não é certificação universal:

- Uma jornada crítica com resultado persistido na matriz escolhida.
- Interrupção e retomada no ponto de maior risco dessa jornada.
- Operação com resposta perdida, quando houver efeito remoto relevante.
- Atualização preservando dados, se a release toca armazenamento, sessão ou SDK.
- Negativo de permissão/autorização relevante e troca de conta.
- Fluxo com leitor de tela e fonte ampliada nas partes alteradas.
- Evidências da versão candidata, lacunas e risco residual por plataforma.

Se só houve emulador Android, escreva exatamente isso. Não estenda o resultado a iOS, aparelho físico ou distribuição de loja sem execução correspondente.
