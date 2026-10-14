# BUILD-REPORT: video-hyperframes

Data: 2026-10-14. Plugin: `plugins/video-hyperframes`. Gate final que consolida `BUILD-REPORT-structural.md` (2026-10-13) e `BUILD-REPORT-quality.md` (2026-10-14).

## 1. Resumo

- **Veredito do gate: aprovado.** `tools/verify_plugin.py` retorna `RESULT: PASS` sem nenhum ERROR ou WARNING. `claude plugin validate` retorna `Validation passed`.
- Nesta etapa do gate não houve alteração no plugin, porque não restava erro. Todas as correções feitas antes estão na seção 5.
- Contagens batem com o previsto no SYNTHESIS: 10 skills, 5 agentes, 0 comandos, 32 prompts VP, 10 referências do playbook, 10 templates, 10 evals.
- Nota de qualidade média: 85,3 antes, 87,8 depois, em 30 artefatos pontuados.
- As revisões são da mesma família de modelos (Claude) que escreveu o plugin. Os 10 evals estão **designed_not_executed**: não foram executados, porque o CLI instalado (2.1.128) não tem `claude plugin eval`.
- Pendências abertas na seção 6. Nenhuma reprova o plugin. Uma delas (item 6.14) é uma contradição entre dois relatórios sobre uma execução de teste do invólucro, que precisa ser conferida pelo dono.

## 2. Contagens

| Item | Previsto (SYNTHESIS) | Encontrado | Observação |
| --- | --- | --- | --- |
| Skills (`skills/*/SKILL.md`) | 10 | 10 | `playbook`, `prompts` e 8 de tarefa. `disable-model-invocation: true` só em `video-toolchain-setup` e `video-render-deliver`. |
| Agentes (`agents/*.md`) | 5 | 5 | `tools: Read, Grep, Glob` nos 5 (sem Write, Edit ou Bash). `model: inherit` nos 5 (ver 6.1). |
| Comandos (`commands/`) | 0 | 0 | |
| Prompts na biblioteca (VP-NN fora de blocos de código em `skills/prompts/references/*.md`) | 32 | 32 | `prompt-library.md` 8 (VP-01 a VP-08); `prompts-explicativo-de-software.md` 11 (VP-09 a VP-19); `prompts-producao-e-entrega.md` 13 (VP-20 a VP-32). |
| Casos de eval (`evals/*/prompt.md`) | 10 | 10 | `graders/` em todos. Estado: designed_not_executed. |
| Arquivos de referência (`skills/*/references/*.md`) | — | 17 | Playbook 10; prompts 3; `software-explainer-storyboard`, `video-brief-interview`, `video-frame-review` e `video-render-deliver` 1 cada. |
| Templates (`skills/playbook/assets/templates/*.md`) | 10 | 10 | TP-01 a TP-10. |
| Snippets VS01 a VS19 (tabela de `claude-md-snippets.md`) | 19 | 19 | |
| Arquivos no plugin | — | 76 | 74 `.md`, `plugin.json` e `evals/.gitignore`. |
| Links relativos | — | 115 verificados, 0 quebrados | Medido no relatório estrutural; o de qualidade também registra 0 quebrados. |
| `.ps1`, `.sh`, `.mjs`, `.py`, `.exe` | 0 | 0 arquivos | Ponto de atenção: `hf-sessao.ps1.md` é texto `.md` com `.ps1` no nome (ver 6.4). |
| `hooks/`, `.mcp.json`, `.lsp.json`, `bin/` | 0 | 0 | Ausentes. |

Descrições das skills: entre 453 e 958 caracteres (limite de 1024). Descrições dos agentes: entre 337 e 408. Playbook `SKILL.md` com 228 linhas (limite de 300).

## 3. Notas de qualidade, antes e depois

Escala da revisão de qualidade: nota = média de D1 a D12 × 20. Cada nota é julgamento do revisor, não medição. As médias abaixo foram recalculadas a partir da tabela por artefato e conferem com o relatório.

| Grupo | Antes | Depois |
| --- | --- | --- |
| Skills (10) | 85,8 | 89,2 |
| Agentes (5) | 89,0 | 89,6 |
| Prompts VP amostrados (14 de 32) | 83,5 | 86,2 |
| Evals (10 casos e README) | 86 | 88 |
| **Geral (30 artefatos)** | **85,3** | **87,8** |

- Mínimo: 76 (VP-16) antes; 83 (VP-01) depois. Abaixo de 80: 1 antes, nenhum depois.
- Maiores ganhos: VP-16 (76 para 86), `video-render-deliver` (84 para 90), `playbook` (86 para 91), `video-env-preflight` (85 para 90), `execution-security-auditor` (87 para 90), VP-25 (81 para 87), VP-32 (82 para 87).
- Nenhum critério de reprovação automática encontrado: nada inventa execução, nada autoriza ação externa sem confirmação, conteúdo externo é tratado como dado, não há cópia literal sem licença e não há segredo.

## 4. Saídas das validações

Validação estrutural, antes e depois das correções (saídas idênticas):

```
python tools/verify_plugin.py plugins/video-hyperframes
Plugin: video-hyperframes  {'skills': 10, 'agents': 5, 'commands': 0, 'evals': 10, 'files': 74}
RESULT: PASS
```

```
claude plugin validate plugins/video-hyperframes
✔ Validation passed
```

Gate final (esta etapa, sem alteração no plugin): as mesmas duas saídas. CLI do Claude Code: 2.1.128.

Observação: o campo `files` do verificador conta só os `.md` (74).

## 5. Correções aplicadas

Revisão estrutural (2 correções, em defeitos que os validadores oficiais não detectam):

1. `README.md`, linha 62: removida a flag `--strict` de `claude plugin validate`. A flag não existe no CLI 2.1.128.
2. `skills/playbook/assets/templates/hf-sessao.ps1.md`, exemplo "5. Como usar": `--preset <nome>` virou `--preset "<nome>"`. Sem aspas, o PowerShell rejeita `<`. Após a correção, os 12 blocos PowerShell em `.md` parseiam com 0 erros (só sintaxe; nada foi executado).

Revisão de qualidade (correções factuais conferidas no clone de `heygen-com/hyperframes`, commit `bf4cf860fbd26a7d51938c5f11987c335d4e848a`):

- Preview: o servidor escuta em `127.0.0.1` por padrão, `HYPERFRAMES_PREVIEW_HOST` troca o endereço, e a porta começa em 3002 e tenta até 100 portas (`portUtils.ts`).
- Invólucro TP-06: `Set-HfSession` passou a remover `HYPERFRAMES_PREVIEW_HOST` (alteração no template; ver 6.14).
- Telemetria do media-use: só o valor `1` desliga; `DO_NOT_TRACK=1` sozinho não basta.
- `code-scroll` é um dos quatro blocos de explicação, não troca legibilidade.
- Scripts de áudio: o laço examina 5 pastas, contando a de partida, e para no primeiro `.env` (inclusive vazio).
- `.media` fica em `<MEDIA_HOME>\.media\`, não em `<pasta-do-video>\.media-home`.
- `--strict` removido também de `ferramentas-e-mcp` §8.
- Posturas alinhadas: `catalog --on-device` é C; `telemetry disable` é P.
- Comandos com placeholders sem aspas corrigidos (`--preset`, `--quality` e `--output`, `--voice`, `snapshot --at`).
- Referência `init.ts:842` corrigida (era 843-846).
- Rastreabilidade: `fontes.md` ganhou §10 (índice dos 76 itens V-nn) e §11 (siglas internas). Referências opacas removidas.
- Sumário adicionado a `hf-sessao.ps1.md` (pendência estrutural resolvida).

Gate final (esta etapa): nenhuma alteração no plugin.

## 6. Pendências

| # | Pendência | Ação |
| --- | --- | --- |
| 6.1 | Os 5 agentes têm `model: inherit`. O SYNTHESIS (4.5) previa `sonnet` para `frame-reviewer`, `composition-reviewer` e `fact-privacy-checker`, e `haiku` para `execution-security-auditor`. | Decisão de custo do dono. Não alterado. |
| 6.2 | `tools/verify_plugin.py` (ferramenta compartilhada) não mede descrições em bloco `>-` (lê o literal `>-`), nem `tools` de agentes, `disable-model-invocation` ou `min`/`max` dos graders. As medições foram feitas à mão e estão dentro do limite. | Coordenador. |
| 6.3 | Não existe `dev-segments/.claude-plugin/marketplace.json`. A entrada de `video-hyperframes`, `CATALOGO.md` e a tag `video-edicao` do orquestrador estão pendentes (SYNTHESIS 4.10). | Coordenador. |
| 6.4 | O nome `hf-sessao.ps1.md` contém `.ps1`, mas é texto `.md`, sem execução (TP-06, nome previsto pelo SYNTHESIS). Aparece em 13 pontos do plugin. | Mantido. Renomear exige editar as 13 referências. Decisão do dono. |
| 6.5 | Evals não executáveis: o CLI 2.1.128 não tem `claude plugin eval`, que exige Claude Code 2.1.269 ou superior. Não há caso positivo de `VIDEO-COMPLETO` nem de delegação aos agentes. | Atualizar o CLI e executar. Até lá, designed_not_executed. |
| 6.6 | Hooks e regras `deny` não foram testados dentro do Claude Code (lacuna L15). | Testar no primeiro uso real. |
| 6.7 | Nada do caminho real foi executado: render, voz PT-BR, Parakeet, efeito de `.env` vazio, `MEDIA_HOME` e endereço do preview em execução. Continuam Inferidos ou Não verificáveis. | Começar pelo render de prova e conferir a escuta com `Get-NetTCPConnection`. |
| 6.8 | IDs `V-nn`: o índice em `fontes.md` §10 resolve os IDs para quem instala. O `VALIDATED.md` de origem não viaja com o plugin. | Resolvido em parte. Incluir o arquivo ou manter o índice, a critério do dono. |
| 6.9 | Colisão de nomes: `C1` a `C14` (checklist do `composition-reviewer`) e `C1` a `C18` (conflitos). Documentada em `fontes.md` §11. | Renomear exigiria mexer em agente, skill e referências. Não feito. |
| 6.10 | Densidade: a lista de variáveis de sessão se repete nas 8 skills de tarefa. | Mantida de propósito, para que cada skill funcione carregada sozinha. |
| 6.11 | Amostra de prompts: 14 dos 32 foram pontuados um a um. Os outros 18 foram lidos, sem achado bloqueante, sem nota individual. | Opcional. |
| 6.12 | Cor `#0b0f14` em `contrato-de-composicao.md`, linha 71: exemplo genérico de CSS. Não é um dos valores do dono. | Confirmar com o dono. |
| 6.13 | Exemplo de `STORYBOARD.md` em `formatos-storyboard-e-script.md` usa `arc: concept-explainer com processo` (mistura de idiomas). | Cosmético. |
| 6.14 | Contradição de auditoria: o relatório de qualidade (seção 3, item 3) registra que o invólucro foi executado com `hfs -DryRun lint` numa cópia de teste no scratchpad. O relatório estrutural (seção 5, item 9) diz que esse `-DryRun` não foi executado, por política, porque roda o CLI do HyperFrames. A instrução desta sessão é não rodar nada do HyperFrames. Nesta etapa nada foi executado, e não reexecutei nada disso. | Conferir o que de fato rodou. O plugin não é afetado pelo texto, mas o registro se contradiz. |

## 7. Declarações

- As revisões estrutural e de qualidade foram feitas por modelos Claude da mesma família que escreveu o plugin (o relatório de qualidade registra claude-opus-5-5 como revisor e Sonnet como construtor). A independência é parcial, e as notas são leitura adversarial, não medição. Este gate final foi feito por Claude Haiku 5.5, também da mesma família.
- Os 10 evals estão **designed_not_executed**. Foram escritos e checados estruturalmente, não executados. Nenhum resultado de eval é afirmado aqui.
- Nada do HyperFrames foi executado neste gate: sem render, sem CLI do HyperFrames, sem `npx`. Nas revisões anteriores houve só análise sintática de PowerShell, com a ressalva do item 6.14.
- Nenhum arquivo de skill, agente ou referência foi reescrito neste gate. O único arquivo criado é este `BUILD-REPORT.md`.
