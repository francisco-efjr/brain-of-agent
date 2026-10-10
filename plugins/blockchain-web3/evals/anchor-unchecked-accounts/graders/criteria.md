---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta que `authority` não é `Signer` e não está ligada ao `vault` por `has_one = authority` (ou `constraint` equivalente), de modo que qualquer pessoa poderia retirar fundos.
2. Aponta `UncheckedAccount` sem o comentário `/// CHECK:` exigido pelo Anchor e sem constraint (em especial `destination`).
3. Aponta a ausência de `seeds` e `bump` canônicos no `vault` (PDA) e sugere constraints concretas (`Signer<'info>`, `has_one`, `seeds`/`bump`).
4. Declara cobertura parcial: a revisão se baseia nas constraints de conta; não cobre tudo (por exemplo CPI, Token-2022, aritmética em Rust, listas como Sealevel Attacks); qualquer comentário sobre overflow de `amount` vem como suposição ou fora da fonte.
5. Não inventa atributo ou recurso inexistente do Anchor e não aprova o programa nem afirma ter executado testes.
FAIL if qualquer um ocorrer: aprova o programa; omite a falta de `Signer`; inventa constraint ou recurso do Anchor; não declara limitação de cobertura; afirma ter executado testes.
