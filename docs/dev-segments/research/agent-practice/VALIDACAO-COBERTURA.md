# Validação de cobertura — agent-practice

Data: 2026-11-19. Fonte: *Competente o Suficiente* (Fabio Akita, 2026), revisão v1.1.0. Método e direitos em `plugins/agent-practice/skills/playbook/references/fontes.md`.

## Método

1. Texto completo extraído do PDF da cópia do usuário (pdftotext) e dividido em 8 trechos: prefácio a parte I; caps. 5–8; caps. 9–11 e interlúdio 1; caps. 12–15 e interlúdio 2; caps. 16–18; caps. 19–21; cap. 22, epílogo, posfácio e apêndices A–F; apêndices G–J. Fontes, créditos, glossário e referências ficaram de fora (sem práticas).
2. Oito leitores independentes (Sonnet 5.5) extraíram, com redação própria, todo "fazer", "não fazer" e sinal de alerta, com ID e página aproximada: **839 itens**.
3. Consolidação (Opus 5.5) em **386 regras** com ID estável, alvo e contexto. Cada regra guardou, durante a construção, os IDs dos itens de origem.
4. Script determinístico conferiu a cobertura: **839 de 839 itens mapeados** a pelo menos uma regra, nenhuma regra duplicada, nenhuma referência a item inexistente. Depois os IDs internos foram trocados pela referência de capítulo que aparece em cada regra.
5. As notas dos leitores (paráfrases por capítulo) **não são publicadas**: ficaram no diretório temporário da sessão, para não reproduzir a estrutura do livro capítulo a capítulo.

Limite: o mapeamento prova que nenhum item extraído ficou sem regra; não prova que os leitores extraíram tudo o que o livro diz. A validação independente (`BUILD-REPORT-quality.md`) amostra regras contra o texto.

## Regras por área

| Arquivo | Regras |
| --- | --- |
| `regras-avaliacao-modelos.md` | 62 |
| `regras-contexto-memoria.md` | 31 |
| `regras-engenharia.md` | 47 |
| `regras-metodo.md` | 24 |
| `regras-operacao.md` | 17 |
| `regras-organizacao.md` | 22 |
| `regras-pedido.md` | 27 |
| `regras-pessoa.md` | 33 |
| `regras-revisao.md` | 26 |
| `regras-seguranca.md` | 43 |
| `regras-sistemas-com-llm.md` | 17 |
| `regras-verificacao.md` | 37 |
| **Total** | **386** |

## Seção do livro → regras derivadas

| Seção | Nº | Regras |
| --- | --- | --- |
| prefácio | 11 | AVA-02, AVA-C01, AVA-C03, AVA-P02, MET-01, MET-05, MET-07, MET-08, MET-S01, ORG-06, PES-03 |
| cap. 1 | 11 | AVA-C03, AVA-P01, AVA-S01, LLM-S02, MET-02, MET-10, MET-P01, MET-P02, MET-S02, ORG-S04, VER-P03 |
| cap. 2 | 17 | CTX-05, CTX-06, CTX-07, CTX-08, CTX-09, CTX-11, CTX-13, CTX-14, CTX-15, CTX-19, CTX-P02, CTX-S01, CTX-S05, CUS-P01, ENG-13, SEG-30, VER-P05 |
| cap. 3 | 16 | AVA-01, AVA-05, AVA-P03, AVA-S01, CTX-14, CTX-P04, CUS-04, ENG-17, ENG-18, ENG-P08, LLM-13, REV-04, VER-01, VER-03, VER-05, VER-11 |
| cap. 4 | 19 | MET-05, MET-P01, PED-11, PED-13, PES-01, PES-02, PES-03, PES-04, PES-05, PES-06, PES-07, PES-08, PES-09, PES-P01, PES-S01, PES-S02, REV-P05, SEG-32, VER-10 |
| cap. 5 | 23 | CTX-01, CUS-03, ENG-01, ENG-03, ENG-06, ENG-10, ENG-14, ENG-P01, ENG-P09, ENG-P10, ENG-S02, ENG-S05, MET-02, MET-06, MET-11, MET-P02, MET-P05, MET-S04, PED-10, PED-15, PES-12, REV-01, REV-02 |
| cap. 6 | 30 | CTX-03, ENG-02, ENG-03, ENG-P05, ENG-S05, LLM-02, LLM-03, MET-02, MET-03, MET-P05, MET-S02, MET-S05, OPS-10, ORG-11, PED-03, PED-05, PED-06, PED-08, PED-13, PED-16, PED-P01, PED-P02, PED-P03, REV-04, REV-P01, SEG-26, SEG-34, VER-06, VER-07, VER-P01 |
| cap. 7 | 30 | AVA-02, AVA-P01, CUS-10, ENG-08, ENG-11, ENG-27, ENG-S03, LLM-01, LLM-04, LLM-05, LLM-06, LLM-07, LLM-S01, MET-11, MET-13, OPS-11, OPS-12, OPS-13, OPS-14, PED-04, PED-08, PED-09, PED-11, PED-P06, PED-S03, REV-07, SEG-28, SEG-33, VER-03, VER-P01 |
| cap. 8 | 19 | ENG-06, ENG-10, ENG-11, ENG-12, ENG-14, ENG-23, ENG-P02, ENG-P03, ENG-P07, ENG-P12, ENG-S04, MET-S03, PED-P04, PES-12, VER-01, VER-13, VER-P03, VER-P06, VER-P07 |
| cap. 9 | 35 | CTX-01, CTX-02, CTX-04, CTX-07, CTX-17, CTX-P03, ENG-04, ENG-09, ENG-19, ENG-21, MET-03, MET-05, MET-06, PED-01, PED-02, PED-05, PED-06, PED-07, PED-12, PED-15, PED-17, PED-18, PED-P01, PED-P02, PED-P04, PED-P05, PED-S01, PED-S02, PES-05, PES-10, REV-03, SEG-17, SEG-22, VER-06, VER-10 |
| cap. 10 | 19 | AVA-15, AVA-P01, CUS-03, ENG-11, ENG-16, ENG-20, ENG-21, ENG-P09, ENG-S05, MET-06, MET-07, MET-11, MET-P05, MET-S05, OPS-14, ORG-08, ORG-11, REV-01, REV-02 |
| cap. 11 | 28 | AVA-01, AVA-02, AVA-03, AVA-04, AVA-05, AVA-06, AVA-07, AVA-08, AVA-10, AVA-B07, AVA-B11, AVA-C14, AVA-P01, ENG-18, ENG-P08, MET-07, OPS-17, SEG-31, VER-03, VER-05, VER-08, VER-09, VER-11, VER-12, VER-16, VER-P01, VER-P03, VER-S02 |
| cap. 12 | 15 | AVA-05, AVA-12, AVA-13, AVA-C02, AVA-P04, AVA-P05, ENG-07, LLM-15, REV-08, SEG-31, VER-02, VER-03, VER-04, VER-23, VER-P01 |
| cap. 13 | 9 | AVA-15, AVA-P06, CUS-06, CUS-07, LLM-03, LLM-10, MET-07, VER-15, VER-21 |
| cap. 14 | 14 | AVA-12, AVA-16, AVA-C12, AVA-S01, CUS-09, ENG-24, PES-13, VER-15, VER-21, VER-22, VER-23, VER-P04, VER-S02, VER-S03 |
| cap. 15 | 22 | AVA-09, AVA-10, AVA-C03, AVA-C04, AVA-C05, AVA-C06, AVA-C07, AVA-C08, AVA-C10, AVA-C11, AVA-C12, AVA-C13, AVA-P02, AVA-P05, CUS-08, LLM-14, PES-03, PES-P06, SEG-02, SEG-11, SEG-12, VER-25 |
| cap. 16 | 28 | CTX-03, OPS-01, OPS-02, OPS-03, OPS-09, OPS-15, PES-21, REV-04, REV-P01, SEG-01, SEG-02, SEG-03, SEG-04, SEG-08, SEG-11, SEG-12, SEG-19, SEG-20, SEG-21, SEG-22, SEG-23, SEG-24, SEG-25, SEG-P01, SEG-P03, SEG-P05, SEG-S01, VER-04 |
| cap. 17 | 27 | ENG-05, ENG-22, ENG-P04, MET-09, ORG-04, PED-14, REV-02, REV-03, REV-05, REV-06, REV-09, REV-10, REV-15, REV-P03, REV-P04, REV-P05, REV-P06, REV-S01, REV-S02, SEG-15, SEG-16, SEG-17, SEG-18, SEG-27, SEG-28, SEG-29, VER-14 |
| cap. 18 | 15 | AVA-12, LLM-09, PES-17, PES-18, PES-19, PES-20, PES-P04, PES-P05, PES-S04, PES-S05, PES-S06, REV-06, REV-S03, SEG-27, SEG-35 |
| cap. 19 | 24 | AVA-02, AVA-07, AVA-S01, ENG-16, ENG-P11, MET-03, MET-04, MET-12, MET-P03, MET-S04, MET-S05, ORG-05, ORG-P05, PED-02, PED-04, PED-S01, PES-12, PES-13, PES-16, PES-P02, REV-11, REV-12, VER-01, VER-16 |
| cap. 20 | 26 | AVA-C13, ENG-11, ENG-S02, MET-06, OPS-04, OPS-05, OPS-06, OPS-07, OPS-08, ORG-01, ORG-02, ORG-03, ORG-07, ORG-08, ORG-P01, ORG-P02, ORG-P03, ORG-P04, ORG-S01, ORG-S02, ORG-S03, PED-03, PED-P03, REV-03, REV-P02, VER-14 |
| cap. 21 | 19 | MET-05, MET-08, MET-09, MET-12, MET-S05, ORG-09, ORG-10, ORG-11, ORG-P06, ORG-S05, PED-07, PED-P01, PES-14, PES-15, PES-P02, PES-P03, PES-S03, REV-14, VER-27 |
| cap. 22 | 21 | AVA-07, AVA-08, AVA-C03, AVA-C14, AVA-S01, CTX-11, CUS-02, CUS-05, ENG-07, ENG-10, LLM-10, MET-01, MET-10, MET-P01, MET-P02, MET-P04, MET-P05, ORG-06, ORG-P04, VER-01, VER-S01 |
| interlúdio 1 | 4 | CUS-01, ENG-18, OPS-16, VER-26 |
| interlúdio 2 | 5 | AVA-S02, LLM-11, LLM-15, SEG-P04, VER-24 |
| epílogo | 21 | AVA-02, AVA-C14, AVA-P02, ENG-02, MET-04, MET-05, MET-14, MET-P04, ORG-01, ORG-02, ORG-P05, PED-01, PES-12, PES-13, PES-14, PES-19, PES-P02, PES-P06, PES-S04, SEG-32, VER-12 |
| posfácio | 13 | CTX-16, ENG-26, ENG-28, ENG-29, ENG-30, MET-05, MET-11, REV-13, REV-14, REV-P07, VER-12, VER-17, VER-18 |
| ap. A | 7 | ENG-28, MET-09, MET-S03, PED-P01, REV-14, VER-12, VER-18 |
| ap. B | 10 | AVA-P07, AVA-S01, AVA-S03, CTX-S06, LLM-S02, MET-P01, MET-P03, PES-S02, VER-25, VER-S01 |
| ap. C | 1 | PES-11 |
| ap. D | 5 | PES-12, PES-13, PES-14, PES-P02, PES-S03 |
| ap. E | 2 | ORG-S04, PES-16 |
| ap. F | 1 | VER-05 |
| ap. G | 30 | CTX-04, CTX-06, CTX-09, CTX-10, CTX-P01, CTX-S04, CUS-01, ENG-01, MET-07, OPS-02, OPS-03, PES-10, SEG-01, SEG-02, SEG-03, SEG-04, SEG-05, SEG-06, SEG-07, SEG-08, SEG-09, SEG-10, SEG-12, SEG-13, SEG-24, SEG-P01, SEG-P02, SEG-S02, SEG-S03, VER-P02 |
| ap. H | 11 | CTX-10, CTX-11, CTX-12, CTX-18, CTX-20, CTX-P01, CTX-P05, CTX-S02, CTX-S04, CTX-S06, SEG-14 |
| ap. I | 28 | AVA-02, AVA-06, AVA-10, AVA-12, AVA-B01, AVA-B02, AVA-B03, AVA-B04, AVA-B05, AVA-B06, AVA-B07, AVA-B08, AVA-B09, AVA-B10, AVA-B11, AVA-C02, AVA-C03, AVA-C04, AVA-C05, AVA-C06, AVA-C07, AVA-C08, AVA-C09, AVA-C10, AVA-C11, AVA-C12, AVA-C13, PES-01 |
| ap. J | 43 | AVA-02, AVA-07, AVA-10, AVA-11, AVA-12, AVA-14, CTX-05, CTX-07, CTX-17, CTX-18, CTX-S03, CTX-S05, CUS-06, ENG-01, ENG-05, ENG-14, ENG-15, ENG-16, ENG-22, ENG-25, ENG-P06, ENG-P07, ENG-P11, ENG-S01, LLM-03, LLM-08, LLM-10, LLM-12, MET-P03, PES-04, REV-10, REV-P05, REV-S04, VER-02, VER-07, VER-08, VER-11, VER-15, VER-19, VER-20, VER-21, VER-P02, VER-S03 |
