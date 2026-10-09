# Arquitetura

`brains/` organiza conhecimento por segmento. QA foi movido com referências,
scripts, assets e regressões; seus caminhos relativos internos permanecem
válidos. Outros segmentos seguem `brains/<nome>/SKILL.md` com seus recursos.

`vendor/gstack/` mantém integralmente a estrutura do fornecedor, necessária
para seus workflows, geradores, adapters e engine. Copiar fontes não instala
o runtime. `registry/` identifica as skills por origem/caminho e fixa a
revisão e hashes do snapshot.

`tools/` integra os conjuntos sem duplicar prompts. CI próprio verifica essa
integração e os helpers QA. Os workflows originais em `vendor/gstack/.github`
ficam como fonte; não são workflows ativos do Brain of Agent.

| Recurso | Responsabilidade |
| --- | --- |
| QA (`qa`) | técnica, risco, dados, oráculos e evidência |
| gstack QA (`gstack-qa`) | workflow de execução, correção e reverificação |
| gstack QA-only | execução de auditoria sem alterar produto |
| Router próprio | selecionar recursos para a tarefa |

Mudanças próprias não alteram o fornecedor. Atualizações externas trocam o
snapshot em uma revisão dedicada. Se um fork do runtime se tornar necessário,
criar um procedimento de patches e executar seus testes antes de alterar os fontes.

O README antigo descrevia um harness Mo baile não versionado junto à skill.
Seu texto foi preservado em `docs/harness-legado.md`; esse harness não é
dependência do brain QA ou do gstack.

## Desenvolvedor fullstack

`brains/fullstack/` contém nove referências técnicas, protocolo, templates e
benchmark. A keyword `FULLSTACK-COMPLETO` integra as bases fullstack e QA com
leitura em lotes, matriz de aplicabilidade e ciclo de implementação/revalidação.
Não impõe linguagem nem herda permissão por selecionar um workflow.

O exportador descobre os brains pelo SKILL.md e copia todos com contexto
compartilhado; QA e fullstack ficam adjacentes. Testes verificam integridade,
colisões e portabilidade dos arquivos, não execução real em todo host/modelo.
