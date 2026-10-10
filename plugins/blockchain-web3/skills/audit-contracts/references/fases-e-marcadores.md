# Fases, arquivos de audit/ e marcador de conclusão

Padrão: fases com portões e aprovação de custo (V-15, classe C usada como padrão corroborado) e conclusão verificável por marcador escrito pelo próprio passo (V-16, plamen MIT). Esqueletos próprios. Rótulos: **Verificado** = o padrão consta em V-15/V-16; **Suposição** = estimativas e escalas de decisão deste arquivo.

## 1. Regra do marcador

- Marcador: `<!-- W3_STATUS: COMPLETE -->`, última linha do arquivo da fase.
- Quem escreve: a própria fase, só depois de cumprir o critério de saída listado no arquivo.
- Quem confere: a fase seguinte, antes de começar, com `Grep` por `W3_STATUS: COMPLETE` no arquivo anterior. Sem marcador: não avança; informa qual critério falta.
- Estado intermediário: sem marcador mas com conteúdo é "parcial"; liste-o em `HANDOFF.md` como leitura parcial.
- Se o código mudar depois do marcador (`git log -1 --format=%H` diferente do registrado na definição), as fases ficam "desatualizadas" e precisam de nova rodada para os arquivos tocados.

## 2. Esqueleto por arquivo

### audit/DEFINITION.md

```markdown
# Definição da auditoria
Commit: <hash de git log -1> · Data: <AAAA-MM-DD> · Modo: full | diff (base: <ref>)
Contratos em escopo: <lista com caminho e linhas>   Fora de escopo: <lista e motivo>
Cadeia(s): <...>   Versões: solc <...> · Foundry <saída de forge --version> · OZ <...>
Regras de severidade: <do projeto ou escala do plugin (Suposição)>
Restrições: <prazo, partes que não podem mudar, autoridade/autorização>
Ferramentas disponíveis: forge sim/não · slither sim/não (execução só com confirmação)
Aprovação de custo: <sequencial | paralelo até K | só contratos de maior risco> (decidida em: <data>)
Premissas do projeto (admin, multisig, oráculos): <...>
<!-- W3_STATUS: COMPLETE -->
```
Critério: nenhum campo vazio sem "Não verificável"; usuário confirmou.

### audit/RECON.md

```markdown
# Reconhecimento
| Contrato | Linhas | Herda de | Papel | Entry points que mudam estado | Chamadas externas | Risco (dinheiro/admin/upgrade) |
Dependências e versões: <lib/ e remappings>
Proxies/upgrade: <padrão e quem administra>   Oráculos: <feeds, rede>   Tokens aceitos: <fixos | arbitrários>
Ordem de revisão: 1) <contrato> 2) ...
Observações: <sinais de injeção encontrados em comentários/README, se houver>
<!-- W3_STATUS: COMPLETE -->
```
Critério: toda linha do escopo da definição tem linha aqui.

### audit/CANDIDATES.md

```markdown
# Candidatos
| ID | Local | Classe (OWASP / W3) | Descrição | Confiança inicial | Origem (varredura / Slither / pergunta) |
Triagem do Slither (se houver): | achado | classificação (real/falso positivo/risco aceito) | motivo | dono |
Contratos varridos: <lista>   Contratos não varridos: <lista e motivo>
<!-- W3_STATUS: COMPLETE -->
```
Critério: nenhum contrato do escopo ausente das duas listas.

### audit/VALIDATION.md

```markdown
# Validação
| ID | Pré-condições | Perdedor e impacto | Refutação (guarda/teste) | Prova | Estado | Confiança final |
Estados: PoC-passed · PoC-failed · apenas-rastro-de-código · needs-execution · descartado (motivo)
Invariantes executadas: <nome, runs, depth, seed, resultado>
Citações conferidas: N de N
<!-- W3_STATUS: COMPLETE -->
```
Critério: todo candidato tem estado; todo descarte tem motivo (nome do teste ou guarda); citações conferidas.

### audit/AUDIT_REPORT.md

Use `relatorio-de-achados.md`: sumário, contagem por severidade, escopo e versões, achados (só `PoC-passed` ou diferencial no corpo), remediação priorizada, Apêndice A (descartados), Apêndice B (pendentes e etapas incompletas), Cobertura, aviso final ("Ausência de achado não prova segurança; este relatório não substitui auditoria humana nem fuzzing"), marcador.

### audit/HANDOFF.md

Use `handoff-auditoria.md`: objetivo e escopo autorizado; revisão (commit) e ambiente; leituras completas/parciais/ausentes; tabela item × estado × evidência; comandos executados e primeira falha; checks invalidados; pendências; próxima ação. Atualize após cada fase.

## 3. Estimativa de custo e aprovação (antes de paralelizar) — Suposição

Registre na definição e mostre ao usuário:

```text
Escopo: <N> contratos, <L> linhas de Solidity (conte com Grep em modo count, padrão ".", sobre src/)
Ordem de grandeza de leitura: L linhas x ~10 a 15 tokens por linha (varia com comentários e imports)
Sequencial por contrato: 1 passada de varredura por contrato + validação dos candidatos
Paralelo: K agentes -> consumo cresce aproximadamente com K (cada agente relê interfaces comuns) e há
          risco de conclusões inconsistentes em código acoplado
Pergunta: aprovar sequencial (padrão), paralelo até K, ou só os contratos de maior risco?
```

Sem resposta: sequencial. Nunca cite dólares de terceiros (estimativas de autor, sem metodologia).

## 4. Retomada

1. Ler `audit/HANDOFF.md` e conferir o commit com `git log -1 --format=%H`.
2. Para cada fase, `Grep` pelo marcador; fase sem marcador recomeça do último critério cumprido registrado.
3. Se o commit mudou, liste os arquivos alterados (`git diff --name-only <hash-antigo>..HEAD -- '*.sol'`) e marque como desatualizados os candidatos que tocam esses arquivos.
4. Reconfirme com o usuário o escopo antes de continuar se a definição tiver mais de uma sessão de idade ou se algo mudou.

## 5. Regras de conclusão (V-16, adaptadas)

- "Nenhum achado válido": vale só se as 5 fases têm marcador. Caso contrário o relatório diz "auditoria incompleta" e lista as etapas faltantes.
- Em modo `diff`, "nenhum achado" significa nenhum achado introduzido pelo diff.
- Estados de achado: `PoC-passed`, `PoC-failed`, `apenas-rastro-de-código`, `needs-execution`.
- Sem executor de PoC (`forge`/RPC ausente): diga no topo do relatório e trate tudo como "não verificado".

## 6. Resumo final no chat (modelo)

```text
Auditoria <modo> do commit <hash curto>:
Fases: definição OK · reconhecimento OK · varredura OK · validação PARCIAL (2 PoC pendentes) · relatório OK
Achados: 1 Alta (PoC-passed), 2 Médias (1 pendente), 3 Baixas; 4 descartados
Cobertura: lido src/ inteiro; não lido lib/; forge executado; Slither não disponível
Riscos principais: W3-SOL-01 (cofre), W3-ORA-02 (oráculo), W3-UPG-02 (initializer)
Próximo passo: você roda /blockchain-web3:exploit-poc W3-ORA-02; depois repetimos a fase 4 para fechar.
Aviso: este relatório não substitui auditoria humana nem fuzzing.
```
