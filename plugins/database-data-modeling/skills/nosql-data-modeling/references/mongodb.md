# MongoDB: embutir ou referenciar, e revisão de schema

Conferido em 2026-10-10 contra V-25: documentação oficial "embedding vs references" (classe A, Verificado) e o SKILL.md de `mongodb/agent-skills` (Apache-2.0, 189 estrelas na página consultada; classe B; prompt-score 77). Fatos que só vêm do SKILL.md: fluxo de 4 passos, 11 padrões, antipadrões, limite de 16 MB como "hard limit", confirmação "yes" antes de escritas e `--readOnly` por padrão. A doc de embed vs reference **não** cita o limite de 16 MB. Texto abaixo é redação própria. Lacuna L-07: índices (regra ESR citada em guias, **não validada nesta base**), transações, sharding e backup do MongoDB não têm fonte aqui.

Sumário
1. Regra de decisão
2. Obsolescência da duplicação
3. Exemplo: posts e comentários
4. Padrões úteis
5. Antipadrões
6. Fluxo de revisão em quatro passos
7. Segurança
8. Lacunas

## 1. Regra de decisão

| Pergunta | Embutir | Referenciar |
| --- | --- | --- |
| A relação é "contém"? | Sim | Não |
| Os dados são consultados juntos na maioria dos acessos? | Sim | Não: acessos separados |
| Cardinalidade do filho | Baixa e limitada | Alta |
| Crescimento do filho | Limitado | Sem limite |
| O filho existe sozinho (tem vida própria, é compartilhado)? | Não | Sim |
| Atualização do filho precisa refletir em todos os pais? | Não (ou tolera obsolescência) | Sim |

Documentos maiores usam mais RAM (V-25): embutir demais pode piorar o cache de trabalho. Limite rígido de 16 MB por documento (fonte: SKILL.md, V-25): estime o tamanho máximo, não o médio.

Pergunta obrigatória antes de decidir: **qual a cardinalidade e o crescimento do filho** (por exemplo, quantos comentários um post pode ter em 1 ano?).

## 2. Obsolescência da duplicação

Duplicar dados (copiar o nome do autor dentro do post) é aceitável conforme a sensibilidade à desatualização (V-25):

| Classe | Exemplo | Postura |
| --- | --- | --- |
| Imutável | `created_at`, id do autor | Duplicar sem custo |
| Temporal | preço no momento da compra | Duplicar de propósito (snapshot do fato) |
| Sensível | e-mail, permissões, saldo | Referenciar ou atualizar de forma controlada |
| Tolerante | contagem de curtidas, nome de exibição | Duplicar e atualizar de forma eventual (job) |

## 3. Exemplo: posts e comentários (caso E-12)

Requisito: página de post mostra os 10 comentários mais recentes; "ver todos" pagina; posts populares chegam a 100 mil comentários.

Modelo ruim (array ilimitado embutido):

```json
{ "_id": "p1", "title": "...", "comments": [ { "user": "u1", "text": "...", "at": "2026-10-01T10:00:00Z" } ] }
```
Cresce sem limite, reescreve o documento a cada comentário, pode estourar 16 MB e puxa tudo para a RAM a cada leitura do post.

Modelo proposto (referência + subconjunto):

```json
// posts
{ "_id": "p1", "title": "...", "author": { "id": "u9", "name": "Ana" },
  "commentCount": 100342,
  "recentComments": [ { "id": "c9001", "userName": "Bia", "text": "...", "at": "2026-10-09T18:00:00Z" } ] }   // até 10, atualizado na escrita
// comments
{ "_id": "c9001", "postId": "p1", "userId": "u1", "text": "...", "at": "2026-10-09T18:00:00Z" }
```
- Padrões de acesso: AP-1 página do post (1 leitura de `posts`), AP-2 "ver todos" paginado por `postId` ordenado por `at` (consulta em `comments`).
- Índice para AP-2: composto `{ postId: 1, at: -1 }` (igualdade e depois ordenação; a regra ESR é citada em guias mas **não validada nesta base**, L-07).
- `recentComments` duplica dado (classe tolerante/temporal): defina quem atualiza e o que acontece quando o comentário é apagado.
- Trade-off: duas escritas por comentário (inserção em `comments` + atualização de `posts`), com possível divergência momentânea; aceitável se a página tolera atraso (Suposição a confirmar com o produto).

## 4. Padrões úteis (conceitos do SKILL.md, V-25; nomes podem variar na doc)

- **Subconjunto**: manter no documento principal só a fatia mais acessada (os 10 comentários recentes), o resto em outra coleção.
- **Referência estendida**: copiar poucos campos estáveis do documento referenciado (nome do autor) para evitar `$lookup`.
- **Cálculo adiantado**: guardar contadores/agregados (`commentCount`) atualizados na escrita.
- **Balde (bucket)**: agrupar eventos de série temporal em documentos por intervalo, para limitar o número de documentos (Inferido; conferir na doc).

## 5. Antipadrões (V-25)

- Coleções demais (uma por tipo mínimo) sem necessidade.
- `$lookup` excessivo no caminho quente: sinal de modelo relacional usado em banco de documentos.
- Índices desnecessários: cada índice custa escrita e RAM.
- Array de crescimento ilimitado embutido.
- Documento "caixa de tudo" com campos raramente usados no caminho quente.

## 6. Fluxo de revisão em quatro passos (V-25)

1. **Ambiente**: versão, tamanho das coleções, topologia (conferir com o usuário; não executar).
2. **Tipo de carga**: leitura vs escrita. O SKILL.md sugere `db.serverStatus().opcounters` (peça ao usuário rodar em ambiente permitido e colar).
3. **Fontes**: consultas reais (logs, código do ODM, perfis), não suposições.
4. **Só então a análise**: tabela relação | decisão | AP-n | risco.

Escritas: nunca sem "yes" explícito do usuário. Se o usuário conectar um servidor MCP de MongoDB, prefira modo somente leitura (`--readOnly`, V-25). O nome exato do pacote **não foi verificado**: abra o repositório `mongodb/agent-skills` e a documentação do servidor antes de documentar comandos.

## 7. Segurança

- Operadores injetados: filtros montados com objetos do cliente podem carregar `$ne`, `$gt`, `$where`: converta entradas para tipos escalares antes (V-29).
- Papéis com privilégio mínimo (leitura por coleção); credencial por ambiente (V-29, V-35).
- Dados pessoais: minimizar campos, definir retenção (índice TTL é recurso conhecido do MongoDB; Inferido, conferir) e evitar copiar PII para dentro de logs.

## 8. Lacunas (declare na saída)

Índices compostos e regra ESR, índices de texto/vetoriais, transações multi-documento, sharding, backup/restore (`mongodump`/Atlas) e validação de schema (`$jsonSchema`): sem fonte validada nesta base (L-07). Responda com princípios gerais rotulados Inferido e remeta à documentação da versão em uso.
