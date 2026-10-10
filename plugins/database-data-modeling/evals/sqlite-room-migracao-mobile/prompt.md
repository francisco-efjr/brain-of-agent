---
name: sqlite-room-migracao-mobile
description: "Mede a cobertura de plataforma: migração de SQLite local em app Android com Room. O plugin deve explicar que a migração roda no aparelho do usuário sem rollback central, rejeitar fallbackToDestructiveMigration que apaga dados, exigir Migration explícita e teste de upgrade a partir de cada versão e apontar o plugin de mobile."
tags: [database-data-modeling, safe-migrations, mobile, sqlite, platform]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Rejeita fallbackToDestructiveMigration por apagar os dados do usuário, propõe Migration(3, 4) com ALTER TABLE ADD COLUMN NOT NULL DEFAULT, exige teste de upgrade a partir de cada versão anterior e aponta o plugin mobile-apps, sem aplicar conselhos específicos de PostgreSQL."
model: sonnet
---
Tenho um app Android (Kotlin, Room) com banco SQLite local, versão do schema 3. Adicionei uma coluna `priority` (inteiro, obrigatória) na tabela `tasks`, subi a versão para 4 e, para o app não crashar quando atualiza, coloquei `.fallbackToDestructiveMigration()` no builder. Funcionou nos meus testes. Pode ir para a Play Store assim?

```kotlin
@Entity(tableName = "tasks")
data class Task(
    @PrimaryKey val id: Long,
    val title: String,
    val priority: Int,
)

@Database(entities = [Task::class], version = 4, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun taskDao(): TaskDao
}

val db = Room.databaseBuilder(context, AppDatabase::class.java, "app.db")
    .fallbackToDestructiveMigration()
    .build()
```

Tem usuário na versão 1.0 do app (schema 1), na 1.1 (schema 2) e na atual (schema 3).
