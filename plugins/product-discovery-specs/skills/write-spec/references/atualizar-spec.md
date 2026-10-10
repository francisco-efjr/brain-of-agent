# Atualizar a spec depois da implementação (spec viva)

Fundamento: spec atualizada junto com código e testes, com a intenção (o porquê) guardada, mantém o aprendizado da implementação (V-28, Drew Breunig, 2026-05-04, ensaio de opinião sem dados). O ensaio **não** descreve um diff entre spec e código construído: o procedimento abaixo é construção deste plugin (Inferido). Níveis spec-first, spec-anchored e spec-as-source vêm de V-39; aqui se pratica spec-anchored.

## Quando atualizar

- Ao terminar uma feature, antes de fechar o trabalho.
- Quando a implementação revelou regra nova, caso de borda ou decisão de corte.
- Quando o `spec-reviewer` apontar divergência entre diff e spec.

Não atualize para "ficar bonito". Cada mudança tem motivo registrado.

## Procedimento

1. **Reúna as duas pontas.** Spec aprovada (com data) e o construído: diff salvo em arquivo, lista de arquivos tocados ou descrição do usuário. Sem o construído, o resultado é Não verificável: pare e peça.
2. **Percorra a spec item a item** (`FR`, `SC`, critérios, bordas, fora de escopo) e classifique:
   - **Conforme**: construído e verificável pelo check da spec.
   - **Adicionado**: existe no construído, não na spec.
   - **Modificado**: existe nos dois, com comportamento diferente.
   - **Removido/não construído**: está na spec, não no construído.
   - **Sem evidência**: não dá para afirmar nem por leitura; marque Não verificável.
3. **Preencha a tabela de divergências** (abaixo). Cite a evidência (arquivo, trecho do diff, teste). Leitura de código não é teste executado: rotule "lido" ou "executado".
4. **Recomende e peça decisão.** Para cada divergência, três saídas: (a) a spec muda para refletir o construído; (b) o código muda para cumprir a spec; (c) aceita-se a divergência, com justificativa e data de revisão. Dê sua recomendação com o motivo; o humano decide. Não decida em lote sem mostrar.
5. **Aplique as decisões na spec**: edite as seções, adicione linha em "Histórico" (data, o que mudou, por quê), reabra `[NEEDS CLARIFICATION]` que a implementação respondeu (com a resposta) ou criou.
6. **Registre decisões materiais** (corte de escopo, trade-off) com o agente `decision-recorder`.
7. **Reverifique**: rode a verificação do `write-spec` (marcadores, rastreabilidade FR->SC) e ofereça `spec-reviewer` em contexto novo.

## Tabela de divergências (modelo)

| ID | Item da spec | Spec dizia | Construído (evidência) | Tipo | Rótulo | Recomendação | Decisão do humano |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D1 | FR-003 | e-mail obrigatório | e-mail opcional (`signup.ts:41`, lido) | Modificado | Verificado (lido) | spec muda: regra de negócio mudou na reunião de 05/10 | pendente |
| D2 | SC-002 | exportação em até 5 s | não há teste de tempo | Sem evidência | Não verificável | rodar o teste de carga antes de decidir | pendente |
| D3 | (novo) | não previsto | limite de 10 mil linhas por exportação (`export.ts:88`, lido) | Adicionado | Verificado (lido) | spec ganha FR e critério negativo | pendente |

O exemplo é ilustrativo; datas e arquivos não correspondem a nenhum projeto real.

## Regras de bom senso

- Divergência que o usuário não consegue julgar sem dado vira pergunta com dono, não decisão.
- Se o construído contradiz o fora de escopo da spec, trate como achado de severidade alta para o humano (escopo cresceu sem decisão).
- Histórico é anexado, não reescrito: não apague o que a spec dizia antes; registre a mudança.
- Spec e código não podem discordar ao final. Se a divergência foi aceita (saída c), a spec registra a exceção com data de revisão.

## Pontos de atenção

- Atualizar só o texto, sem rodar o check correspondente, produz spec que parece verificada e não está. Informe "lido" ou "executado".
- Atualização em massa de spec grande: faça por história (P1, depois P2), com G1 curto em cada uma.
- Specs de bugfix: confirme que o bloco "inalterado" ainda vale depois da correção.
