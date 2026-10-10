# Offline-first e sincronização

Verificado em 2026-10-10. Base: guia oficial Android de offline-first (V-59, classe A) e WorkManager (V-60, B), SwiftData + CloudKit (V-61, A), Doze (V-63, A), mais o brain `qa/references/mobile.md` (conteúdo próprio, MIT) para filas e conflito. O checklist de terceiro V-45 só inspirou a lista de testes; seu código **não** deve ser copiado. Esboços de código são originais deste plugin (**Inferido**).

## 1. Perguntas de projeto (responder ou assumir explicitamente)

| Pergunta | Por que muda o desenho |
| --- | --- |
| Quais dados precisam funcionar offline? | Define o que entra no banco local e o que é online-only |
| Há edição concorrente (celular e tablet, ou duas pessoas)? Qual a política de conflito? | Define versionamento e UI de resolução |
| Qual latência de sincronização é aceitável? | Define pull periódico, push ou sincronização imediata |
| Quanto tempo o usuário pode ficar offline? | Define retenção da fila e migração local |
| O servidor aceita chave de idempotência? | Sem ela, a fila precisa de reconciliação por consulta |

A última pergunta é dependência do backend (fronteira `backend-api`): documente o que o cliente precisa da API.

## 2. Checklist de 7 itens (V-59)

1. **Fonte local canônica.** A UI e as camadas superiores só leem do banco local.
2. **Leitura reativa.** Tipos observáveis (Flow, LiveData, StateFlow, streams) emitem quando o banco muda.
3. **Escrever local primeiro** (para dados editáveis), depois sincronizar.
4. **Estratégia de escrita por tipo de dado**: online-only (rede primeiro, depois local), enfileirada (fila drenada com backoff exponencial ao voltar a rede) ou preguiçosa (local primeiro, rede o quanto antes).
5. **Timestamp ou versão no registro**, para ordenar e detectar conflito.
6. **Fila persistente e ordenada.** A página só a esboça: ordem firme exige Room ou DataStore (V-59).
7. **Teste de transição de rede** (seção 7).

Acrescente a pergunta "qual a política de conflito?". Modelos separados de rede, entidade e externo com mapeadores (a página usa `NetworkAuthor`, `AuthorEntity`, `Author`). Room para dados estruturados, DataStore para não estruturados. Sincronização: pull, push (réplica local) ou híbrida.

## 3. Fila de escrita (outbox): propriedades obrigatórias

| Propriedade | Como verificar |
| --- | --- |
| **Persistente** | A fila está numa tabela, não numa lista em memória |
| **Recarregada na inicialização** | Existe código que lê a fila ao subir o app/worker; teste: matar o processo com itens pendentes |
| **Processada em série** (por entidade ou global) | Um único consumidor; o listener de rede apenas agenda trabalho único, nunca processa em paralelo |
| **Idempotente** | Cada operação tem `opId` estável enviado ao servidor (por exemplo, no cabeçalho `Idempotency-Key`, se o contrato aceitar); reenvio gera um efeito |
| **Backoff exponencial com limite** | Há teto de tentativas ou prazo e destino claro para erro permanente (marcar e mostrar ao usuário) |
| **Retenção definida** | Decida o que acontece com itens muito antigos; descartar silenciosamente é defeito |
| **Estado visível** | Indicador de offline/pendente na UI |

Esboço Kotlin (Room + WorkManager; ajustar nomes ao projeto):

```kotlin
class NotesRepository(
    private val db: AppDatabase,
    private val notes: NoteDao,
    private val outbox: OutboxDao,
    private val scheduler: SyncScheduler,
    private val clock: Clock,
) {
    fun observeNotes(): Flow<List<Note>> =
        notes.observeAll().map { rows -> rows.map(NoteEntity::toModel) }

    suspend fun save(note: Note) {
        db.withTransaction {                      // grava dado e operação juntos
            notes.upsert(note.toEntity(updatedAt = clock.now(), dirty = true))
            outbox.insert(OutboxOp(opId = UUID.randomUUID().toString(), noteId = note.id, type = OpType.UPSERT))
        }
        scheduler.enqueueUnique()                 // trabalho único: não duplica
    }
}
```

Worker: `doWork()` lê a fila na ordem, envia com `opId`, apaga a operação em caso de sucesso, devolve `Result.retry()` em erro transitório (a política de retry do WorkManager aplica backoff) e marca falha em erro permanente. Nome único de trabalho evita duplicação. Declare a restrição de rede (V-60).

## 4. Política de conflito (decisão de produto por tipo de dado)

| Política | Quando serve | Cuidado |
| --- | --- | --- |
| **Last write wins** | Dados simples, baixo risco de perda | Comum em mobile (V-59: o dispositivo anexa timestamp, a rede descarta o mais antigo). Defina **qual relógio ou versão manda**; hora local de dois aparelhos não dá ordem confiável (**Inferido**, brain). De preferência, timestamp ou contador do servidor |
| **Versão/ETag + recusa (409)** | Edição rara em paralelo | O cliente precisa buscar, mostrar e deixar o usuário escolher |
| **Merge por campo** | Campos independentes (título vs corpo) | Exige modelo com granularidade de campo; a página V-59 não o discute |
| **Perguntar ao usuário** | Conteúdo de alto valor | Fila precisa parar naquele item sem bloquear os demais |

V-59 diz que "há muitas estratégias" e que LWW é "descrita como comum". Não apresente LWW como única opção nem como norma.

## 5. SwiftData com CloudKit (V-61, oficial)

- Duas capabilities: iCloud com CloudKit (e contêiner) e Background Modes com Remote notifications. Exige conta de desenvolvedor ativa com permissão de administrador (ação do usuário; Xcode requer macOS).
- Limitações: sem atributos `unique`; relacionamentos opcionais; regra de exclusão `deny` não suportada; inverso explícito quando não inferível.
- Esquema de desenvolvimento é inicializado manualmente (build DEBUG) e **promovido a produção antes do lançamento**; o esquema de produção só aceita adições (sem apagar tipos nem alterar atributos). Teste o modelo antes de promover.
- `ModelConfiguration(cloudKitDatabase: .private(...))` escolhe o contêiner; `.none` desliga a sincronização.
- **Resolução de conflito: a página não descreve.** "Último gravador vence" é **Suposição**; não escreva como fato (lacuna 7).

## 6. Segundo plano e bateria

WorkManager serve para trabalho **adiável** que precisa sobreviver ao fechamento do app. Horário exato é outro mecanismo (alarmes; **Inferido**, V-60). Em Doze, a página oficial diz que tarefas do WorkManager não rodam durante o Doze (V-63): o trabalho espera a janela de manutenção. Mensagem crítica usa FCM de alta prioridade, apenas se gerar notificação (V-63). Veja `mobile-performance-diagnosis` para wake locks (V-62).

Checklist por worker (V-60, reescrito): idempotente; nome único; restrição de rede declarada; `retry` com política; não segura wake lock manualmente.

## 7. Plano de teste (reescrito do brain e de V-45)

| Cenário | Resultado esperado |
| --- | --- |
| Offline antes do envio | Nenhum sucesso fictício; item pendente visível; recuperação ofertada |
| Reiniciar app/aparelho com fila cheia | Fila preserva identidade, ordem e estado; nada some |
| Rede cai no meio do envio | Reenvio com o mesmo `opId`; um efeito no servidor |
| **Resposta perdida depois de o servidor processar** | Cliente reconcilia pela identidade da operação; sem segunda cobrança/criação |
| Token expira durante a sincronização | Refresh coordenado ou login; fila não descartada |
| Edição em dois aparelhos | Política de conflito aplicada; nenhuma perda invisível |
| Resposta antiga chega depois da nova | UI não retrocede para dado obsoleto |
| Troca Wi-Fi ↔ dados móveis | Sem loop de requisições |
| Relógio local errado | Política respeita a fonte de tempo definida |
| Troca de conta A→B | Cache, fila e notificações de A não aparecem em B |

Exemplo sintético do brain: transferência de R$ 10,00 em sandbox, saldo inicial R$ 100,00, `op-qa-001`. O servidor efetiva e a resposta não chega. Oráculo: uma transferência, saldo R$ 90,00, comprovante da mesma operação, nenhuma segunda cobrança. "Apareceu mensagem de erro" não valida integridade financeira.

## 8. Lacunas

Offline em React Native e Flutter: sem fonte lida (lacuna 12 e de desenho). Aplique os mesmos princípios com o banco local da stack e rotule Inferido. Sincronização de dados do servidor (contrato, paginação, delta) é do `backend-api`.
