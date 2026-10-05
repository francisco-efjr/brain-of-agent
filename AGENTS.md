# Brain of Agent — desenvolvimento

- Conhecimento próprio vive em `brains/<segmento>/`; QA começa em `brains/qa/SKILL.md`.
- Não editar diretamente `vendor/gstack/`. Atualizar seguindo `docs/upstream.md`, preservando licenças, avisos e hashes.
- Gerar `registry/skills.json` com `python3 tools/catalog.py`; não editar o catálogo manualmente.
- Usar `qa` para nossa skill e prefixo `gstack-*` para workflows instalados.
- Verificar com `python3 tools/verify.py`, `python3 -m unittest discover -s brains/qa/tests -v` e `python3 -m unittest discover -s tests -v`.
- Exportação prepara fontes. Setup, dependências, navegador e testes do fornecedor são etapas distintas.
- Integridade e testes próprios não provam funcionamento do runtime upstream. Não iniciar avaliações pagas para verificar uma cópia de fontes.
