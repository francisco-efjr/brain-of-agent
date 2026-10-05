# Atualizar o snapshot

1. Clone https://github.com/garrytan/gstack em um diretório temporário fora do checkout.
2. Escolha uma revisão e confira changelog, licença, avisos e requisitos.
3. Execute `python3 tools/import_gstack.py --source /caminho/do/clone --revision SHA_COMPLETO`.
   O importador exige origin oficial e checkout limpo, verifica blobs,
   monta a cópia antes de substituir o snapshot e atualiza o manifest.
4. Execute `python3 tools/catalog.py` e revise mudanças de skills/comandos.
5. Rode a integridade e as duas suítes próprias. Testes/build upstream,
   quando necessários, são executados e reportados separadamente.
6. Atualize versões/contagens no README e avisos. Faça commit dedicado com
   revisão anterior/nova e evidências.

Não edite hashes para ocultar mudanças locais. Adaptações deliberadas exigem
patches documentados e testes; não se apresentam como cópia fiel. O exportador
nunca sobrescreve uma instalação existente ou atualiza instalações por conta própria.
