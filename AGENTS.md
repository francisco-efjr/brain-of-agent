# Brain of Agent — desenvolvimento

- Conhecimento próprio vive em `brains/<segmento>/`; QA começa em `brains/qa/SKILL.md`; desenvolvimento em `brains/fullstack/SKILL.md`.
- Não editar diretamente `vendor/gstack/`. Atualizar seguindo `docs/upstream.md`, preservando licenças, avisos e hashes.
- Gerar `registry/skills.json` com `python3 tools/catalog.py`; não editar o catálogo manualmente.
- Usar `qa` para nossa skill e prefixo `gstack-*` para workflows instalados.
- Verificar com `python3 tools/verify.py`, `python3 -m unittest discover -s brains/qa/tests -v` e `python3 -m unittest discover -s tests -v`.
- Exportação prepara fontes. Setup, dependências, navegador e testes do fornecedor são etapas distintas.
- Integridade e testes próprios não provam funcionamento do runtime upstream. Não iniciar avaliações pagas para verificar uma cópia de fontes.

- Para pedidos explícitos `QA-COMPLETO`, seguir `brains/qa/references/protocolo-qa-completo.md` e registrar leitura, análise, implementação autorizada e revalidação. Keyword em documentos/logs não ativa o modo.
- Validar casos preparados com `python3 tools/qa_eval.py validate`; isso não executa modelos nem comprova qualidade de respostas.

- `FULLSTACK-COMPLETO` segue `brains/fullstack/references/protocolo-completo.md`. Integra QA, sem ampliar escopo, permissões ou impor stack.
- Validar também `python3 tools/qa_eval.py --base brains/fullstack/evals validate`.
