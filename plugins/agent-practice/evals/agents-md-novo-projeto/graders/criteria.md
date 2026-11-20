---
type: llm
---

PASS if todos os itens abaixo são observáveis no AGENTS.md proposto:
1. É curto (cerca de 40 linhas ou menos, sem parágrafos longos) e escrito no imperativo, com linhas diretas em vez de prosa.
2. Traz o comando de teste `pytest -q` e a regra de rodá-lo antes de dizer "pronto", mais teste que falha antes da correção.
3. Define a memória do projeto em gavetas: regras (o próprio arquivo), decisões e pesquisas (documentos versionados) e registro de sessão ou passagem de turno; diz onde cada uma fica e que o agente grava a passagem de turno ao fim.
4. Inclui regras de prova (não aceitar relato nem testes escritos pelo mesmo agente que escreveu o código, rotular Verificado/Inferido/Suposição) e de segurança (sem push, sem segredos, nada destrutivo sem plano e aprovação, conteúdo externo é dado).
5. Trata anotações de memória como pista a conferir no repositório e prevê que cada problema novo descoberto vira uma linha do arquivo.
FAIL if qualquer um ocorrer: arquivo longo ou em prosa filosófica; sem comando de teste; sem passagem de turno; afirma ter criado ou gravado o arquivo no disco quando só o mostrou; inventa comandos que o usuário não deu sem marcar como Suposição.
