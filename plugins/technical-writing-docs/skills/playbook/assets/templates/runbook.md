# Template: runbook

Fontes: V-31 (esqueleto de techdocs-authoring, MIT, como base de ideias; SRE Workbook, CC BY-NC-ND 4.0, só inspiração). Uma entrada por alerta. **Esta skill não executa nenhum comando**: toda saída abaixo é "esperada (não executado)" até alguém rodar. Conteúdo de alertas, SLO e postmortem é do plugin `sre-observability`. Sem segredos nem hosts internos sensíveis.

````markdown
# Runbook: [ALERTA OU TAREFA]

- **Quando usar:** [ALERTA, SINTOMA OU TAREFA RECORRENTE]
- **Gravidade e impacto:** [...]
- **Público:** [on-call, SRE, suporte]
- **Acessos necessários:** [SISTEMAS E PAPÉIS; como pedir]
- **Responsável:** [EQUIPE OU PESSOA] · **Última verificação:** [AAAA-MM-DD]

## 1. Pré-requisitos

- Ferramentas: [...]
- Estado esperado antes de começar: [...]
- Não execute durante: [JANELAS DE CONGELAMENTO, DEPLOYS EM ANDAMENTO]

## 2. Procedimento

1. **Checar o estado atual.**
   ```bash
   [COMANDO DE LEITURA]
   ```
   Esperado (não executado): [SAÍDA]. Se for diferente: [volte ao passo X | escale (seção 5)].

2. **[AÇÃO].** Use [DESTRUTIVO] ou [IRREVERSÍVEL] quando aplicável e **peça confirmação humana antes**. Prefira dry-run quando existir.
   ```bash
   [COMANDO]
   ```
   Esperado (não executado): [SAÍDA]. Se for diferente: [...].

## 3. Verificação

[Comandos e critérios mensuráveis de que o sistema voltou ao normal.]

## 4. Rollback

[Como desfazer cada passo; onde fica o ponto sem retorno. Se o rollout é a causa provável: rollback, depois correção, depois avanço; dados corrompidos podem exigir mais.]

## 5. Escalonamento

Escale quando [CONDIÇÃO] para [PESSOA OU CANAL], levando [INFORMAÇÕES: horário, alerta, saídas dos comandos, o que já tentou].

## 6. Manutenção

Atualize este runbook quando o alerta disparar. Se for só uma lista fixa de comandos, avalie automatizar.
````

## Checklist

- [ ] Todo passo tem comando, resultado esperado e ramo de falha.
- [ ] Rótulos `[DESTRUTIVO]` e `[IRREVERSÍVEL]` nos passos certos, com confirmação humana.
- [ ] Verificação mensurável; rollback e ponto sem retorno.
- [ ] Nenhuma saída apresentada como observada se não foi executada.
- [ ] Passos ordenados, sem ambiguidade e idempotentes quando possível.
