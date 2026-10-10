---
description: Prepara e, após confirmação, roda claude plugin eval no plugin atual. Cada execução e cada juiz custam chamadas de modelo.
argument-hint: "[caso ou glob] [--runs N] [--ablation none|with-without]"
disable-model-invocation: true
---

# /qa-testing:eval-plugin

Rode a suíte de evals de um plugin com custo e ambiente confirmados pelo usuário. Argumentos: $ARGUMENTS. Este comando é manual (`disable-model-invocation: true`) porque gasta chamadas de modelo; desenhar os casos é da skill `eval-design`.

## Pré-checagens (antes de qualquer execução)

1. `claude --version`: exige Claude Code 2.1.269 ou superior; `git --version`: 2.31 ou superior, se o git estiver instalado. Abaixo disso, pare e diga que os casos seguem `designed_not_executed`.
2. Confirme que o diretório atual é a raiz do plugin (existe `.claude-plugin/plugin.json` e `evals/`). Liste os casos com `ls evals`.
3. Leia o frontmatter `allowed_tools` dos casos escolhidos. A execução só concede ferramentas somente leitura (`Read`, `Glob`, `Grep`, `Skill`, `Agent` e afins); `Write`, `Edit` e `Bash` exigem `--allow-tools`. Com `Bash` concedido, o run usa o sandbox do sistema: no Windows nativo não há backend e o caso falha, então use WSL2.
4. `claude plugin eval` carrega skills, hooks e agentes do plugin e roda como o usuário. Só avalie plugin cujo código você leu e confia; `--trust-plugin` é uma afirmação dessa confiança, não um atalho.

## Passos

1. Monte o comando. Padrão barato para iterar: `claude plugin eval . --case <caso> --runs 1 --ablation none --max-cost-usd <teto>`. Para medir o efeito do plugin: `--ablation with-without` com as 3 execuções padrão.
2. Mostre ao usuário: o comando completo, os casos que rodam, as ferramentas concedidas, o teto `--max-cost-usd` e o aviso de custo. Pergunte e espere um "sim" explícito. Sem resposta (execução em lote), não rode: entregue o comando como proposta.
3. Rode o comando aprovado, sem acrescentar flags que o usuário não viu.
4. Leia o resultado: código de saída (0 todos acima do `--threshold`; 1 caso abaixo, erro de carga ou opção inválida; 2 execução parcial por teto de custo, interrupção ou credencial recusada), `results/<timestamp>/aggregate-result.json` e, por amostra, as transcrições de casos que falharam.
5. Relate por caso: nota com e sem plugin, Δ, graders que falharam e se a falha parece do agente ou do grader. `tool_used: Skill` é indicador de disparo e fica fora do score em execução de dois braços.

## Formato de saída

```markdown
## Eval: <plugin> · <data> · Claude Code <versão> · modelo <modelo>
Comando: `<comando literal>` · Código de saída: <n> · Custo estimado: <do relatório>
| Caso | Com plugin | Sem plugin | Δ | Graders que falharam | Leitura da transcrição |
## Não verificado
<casos não rodados, ferramentas não concedidas, transcrições não lidas>
```

Não afirme nota, Δ ou "o plugin funciona" sem a execução desta sessão. Uma rodada com `--runs 1` orienta, não conclui; se o plugin passa mas o Δ é negativo, suspeite do juiz antes do plugin.

Fonte: V-02, https://code.claude.com/docs/en/plugin-evals (reconferida em 2026-10-10). Confira as flags com `claude plugin eval --help` na versão instalada.
