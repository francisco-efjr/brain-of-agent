---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Não aprova o envio como está: explica que `fallbackToDestructiveMigration()` apaga todos os dados locais dos usuários quando falta migração, o que funciona nos testes do desenvolvedor (banco novo ou recriado) mas destrói os dados de quem atualiza.
2. Explica a particularidade de plataforma: a migração roda no aparelho do usuário, sem janela de manutenção, sem rollback central e podendo atualizar a partir de qualquer versão anterior (1, 2 ou 3 para 4); portanto exige migrações explícitas encadeadas.
3. Propõe uma `Migration(3, 4)` (e trata 1 para 2 e 2 para 3 existentes ou ausentes) com `ALTER TABLE tasks ADD COLUMN priority INTEGER NOT NULL DEFAULT 0` (ou valor padrão justificado), observando que no SQLite uma coluna `NOT NULL` adicionada exige valor padrão; registra a migração no builder com `addMigrations`. Pode observar, como Inferido, que a entidade deve declarar o mesmo default (`@ColumnInfo(defaultValue = "0")`) para que a validação de schema que o Room faz ao abrir o banco depois das migrações não falhe; se citar alternativas mais estreitas, `fallbackToDestructiveMigrationFrom` e `fallbackToDestructiveMigrationOnDowngrade` também apagam dados nos caminhos que cobrem.
4. Recomenda habilitar a exportação do schema (`exportSchema = true`) e testar o upgrade a partir de cada versão anterior (por exemplo com `MigrationTestHelper`), conferindo que os dados existentes sobrevivem.
5. Aponta o plugin de mobile (`/mobile-apps:playbook`) ou outra fonte específica de Android/Room para detalhes de persistência, offline-first e publicação, e não aplica conselhos específicos de servidor PostgreSQL (como `CREATE INDEX CONCURRENTLY`, `lock_timeout` ou réplicas) ao caso.
6. Rotula o que é Inferido ou Suposição (por exemplo APIs do Room que dependem da versão da biblioteca) e não afirma ter compilado ou testado o código.
FAIL if qualquer um ocorrer: aprova `fallbackToDestructiveMigration` para produção; trata o caso como migração de servidor com janela e rollback central; recomenda `CONCURRENTLY` ou outros recursos de PostgreSQL; ignora usuários em versões antigas; afirma ter testado.
