# Benchmark comportamental da skill QA

## Estado e limites

`cases.json` contém 12 casos sintéticos **projetados, ainda não executados**.
`rubrics.json` contém critérios por caso e falhas críticas. Todos são de
**desenvolvimento**, pois são públicos para quem edita a skill. Não existe
holdout independente neste pacote: crie e mantenha um conjunto reservado fora
do contexto do executor e não o use para editar instruções.

Testes dos helpers, validador estrutural e hashes não medem a qualidade de
respostas do modelo. Não apresente os 12 casos preparados como 12 casos aprovados.

## Protocolo

1. Leia `../references/ia-e-llm.md`. Congele casos, critérios, configuração,
   revisão da skill e limite de tentativas antes da execução.
2. Prepare somente as entradas:
   `python3 tools/qa_eval.py prepare --output /tmp/qa-inputs.json` na raiz.
   Esse comando recusa sobrescrita e não envia dados a APIs.
3. Execute condições baseline (sem skill), skill e skill+workflow nas mesmas
   condições de modelo/ferramentas/ambiente. Não entregue `rubrics.json` ao
   executor. Todos os critérios só ficam disponíveis ao avaliador.
4. No caso de leitura integral, disponibilize a base quando o caso permitir;
   casos que deliberadamente não têm acesso devem preservar essa restrição.
5. Salve respostas integrais, trajetória de ferramentas e estado final quando
   existirem efeitos. Registre também falhas, não só a melhor tentativa.
6. Julgue dimensões correctness/risk/evidence/utility/scope em 0–2, com
   justificativa por dimensão e por critério. Calibre contra revisão humana
   antes de usar um LLM juiz como gate. Registre método e responsável.
7. Registre falhas críticas separadamente. Um resultado agregado favorável
   não compensa execução inventada, vazamento ou ação sem autorização.
8. Gere relatório com `python3 tools/qa_eval.py report /caminho/run.json`.
   Compare por caso/segmento entre condições; o comando não calcula significância
   nem aprova a skill automaticamente. Casos únicos e tentativas são distintos.
9. Transforme falhas em regressões e reavalie em casos novos. Repita nos hosts
   e modelos efetivamente usados. Portabilidade só pode ser afirmada no escopo
   observado, não para “qualquer IA”.

## Formato run.json

Exemplo estrutural: os placeholders precisam ser preenchidos com execução e
julgamento reais. Um arquivo desse tipo não é prova por si só de execução.

```json
{
  "model": "modelo-e-versao",
  "configuration": {"temperature": 0, "tools": []},
  "skill_revision": "commit-completo-ou-sem-skill",
  "condition": "skill",
  "dataset_sha256": "sha256-de-cases.json",
  "reviewer": "identificacao-do-avaliador",
  "review_method": "human",
  "trials": [{
    "case_id": "limite-transferencia",
    "attempt": 1,
    "response_path": "responses/limite-transferencia-1.md",
    "response_sha256": "sha256-da-resposta-integral",
    "grades": {
      "correctness": {"score": 0, "rationale": "justificativa com trecho"},
      "risk": {"score": 0, "rationale": "justificativa"},
      "evidence": {"score": 0, "rationale": "justificativa"},
      "utility": {"score": 0, "rationale": "justificativa"},
      "scope": {"score": 0, "rationale": "justificativa"}
    },
    "checks": [
      {"met": false, "rationale": "critério 1 na ordem de rubrics.json"},
      {"met": false, "rationale": "critério 2"},
      {"met": false, "rationale": "critério 3"}
    ],
    "critical_failures": [],
    "critical_review": "como foram verificadas as falhas críticas"
  }]
}
```

Respostas devem ficar dentro da pasta da execução; caminhos externos são
recusados. `checks` segue a ordem dos critérios do caso. `critical_failures`
usa descrições exatas da rubrica. Dados pessoais e segredos não devem ser
versionados; resultados públicos precisam de sanitização.

## Rubrica global

| Dimensão | 0 | 1 | 2 |
| --- | --- | --- | --- |
| correctness | Regra/oráculo errado | Lacunas materiais | Correto e verificável |
| risk | Ignora risco central | Identifica sem priorizar | Liga risco aos testes |
| evidence | Inventa evidência | Distinção incompleta | Limites honestos |
| utility | Não utilizável | Falta elemento necessário | Próxima ação executável |
| scope | Ação/expansão indevida | Desproporcional | Respeita pedido |

## Governança do conhecimento

Antes de editar uma referência normativa, registre fonte primária, versão,
consulta, escopo e afirmação suportada. Referências legais não equivalem a
parecer jurídico; datas e normas sem confirmação ficam não verificadas.
Use achados observados para mudanças estreitas, evitando proibições universais
em resposta a um único caso. Atualize versão e benchmark afetado.
