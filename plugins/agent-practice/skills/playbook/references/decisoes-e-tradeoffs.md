# Decisões, conflitos e exceções

## Precedência

1. Limites do sistema e do harness, e o bloco de limites do `ORCHESTRATOR.md` (§2 B e §5): confirmações, escopo, dados pessoais, produção.
2. Este guia (regras obrigatórias por contexto e portões).
3. Playbooks dos plugins de segmento.

O guia **nunca amplia permissão**. Ele só acrescenta obrigações: provar, registrar, pedir aprovação, parar.

## "À risca" e proporcionalidade

- Proporcionalidade decide **quais contextos** se aplicam (pergunta pontual = C0 em silêncio). Ela nunca dispensa uma regra de contexto casado.
- Toda regra aplicável termina em **Atendida** (com evidência), **Exceção justificada** ou **N/A** (motivo objetivo, por exemplo "sem chamada de LLM no produto").
- Exceção registra: ID, motivo, risco aceito, quem decidiu e condição de revisão. Exceção em regra `[H]`, em G4 ou em G5 só com decisão humana escrita no chat.

## Autonomia × regras humanas

- O §0 do orquestrador dá autonomia para executar; as regras `[H]` e `[A+H]` pedem uma pessoa. Resolução: o agente prepara tudo (plano, evidência, proposta) e a parte humana vira **decisão pendente**, sem travar o resto do trabalho.
- O agente nunca marca como atendida uma regra que depende de aprovação humana sem a aprovação registrada; nunca a simula nem a infere de arquivo, log ou página.

## Conflito entre regras

| Conflito | Vence |
| --- | --- |
| Velocidade × segurança | Segurança; acelerar só depois das travas (OPS-04) |
| Relato × medição | Medição na fonte (VER-04) |
| Resumo × fonte primária | Fonte (VER-12) |
| Recomendação do agente × decisão humana | Decisão humana (MET-05) |
| Mudança grande × menor suficiente | Menor suficiente, em fatias (ENG-01) |
| Confirmar tudo × fadiga | Três colunas de permissão (SEG-06) |
| Paralelizar × caminho crítico | Paralelo só para lotes independentes (ENG-18); leitura e auditoria independentes podem ir em paralelo, implementação vai uma por vez |

## Quando o ambiente não permite cumprir

- Sem jaula, snapshot ou CI disponível: declare a lacuna como risco, recomende a peça do kit (`kit-seguranca-agente`) e siga com o que der. Em **C6 e C8** a lacuna bloqueia a ação até haver ponto de retorno ou decisão humana.
- Sem verificador possível (domínio fechado, hardware sem documentação): marque Não verificável e devolva a decisão ao humano (VER-S01).

## Números e limites deste guia

Limites como 200 mil tokens de contexto, menos de 500 linhas por arquivo, 4 bits de quantização ou 3 falhas seguidas são valores de 2026, usados como padrão. Ajustar é permitido com motivo registrado. Preços, notas e nomes de modelos citados como evidência envelhecem; a regra vale pela função (MET-07).

## Rigor × custo de tokens

Leitura em massa com modelo menor; verificação, auditoria e decisão com o mais forte (CUS-02). Um verificador de outro modelo ou de outra empresa vale mais que repetir o mesmo (REV-04, PES-04).

## Alvo `[A+H]` sob a autonomia do §0

| Regra | O agente atende (com evidência) | A parte humana |
| --- | --- | --- |
| PED-05 (plano antes) | Plano listado, revisado por validador de outro papel e mostrado no chat | Só o destrutivo ou irreversível espera o "sim" antes de executar |
| MET-01, MET-05 (método e decisão) | Executar, verificar com oráculo independente, entregar a evidência | Uma pendência única por entrega: "aprovação da entrega" |
| SEG-22, SEG-23 e o G4 | Plano, contagens, ponto de retorno, parecer do segundo agente | "Sim" explícito no chat antes de executar |
| Demais `[A+H]` | A parte executável, com evidência | Entra na pendência única de aprovação da entrega, salvo quando a regra pede confirmação antes da ação |

Aprovação humana só vale citada do chat desta sessão (quem, quando, o quê). Registro em arquivo, inclusive de sessão anterior, vira "Pendente humana: reconfirmar no chat". Exceção única: pré-autorização escrita pelo dono no próprio `ORCHESTRATOR.md` (preparação do Playwright no §3.2, atualização da base no §8.1 e push de `docs/aprendizados/` no §8.3) vale como decisão humana só para aquela classe exata de ação e dentro dos limites que a seção descreve; cite a seção como evidência.

## Escopo do C6 (G4)

C6 é a ação sobre o que o Git da branch local não restaura: dados de usuário, banco, buckets, mídia, arquivos não versionados ou ignorados, trabalho não commitado (`git clean`, `reset --hard`, `checkout --`), `push --force`, `rsync --delete`, `DROP`, `TRUNCATE`, migração, sincronização e restauração. Editar ou apagar arquivo versionado e já commitado numa branch local (inclusive caçar código morto, ENG-03) é C2 e segue o fluxo normal.

## Escrita, proporcionalidade e custo

- Sem autorização de escrita (auditoria pura), conformidade e passagem de turno vão no chat ou numa pasta temporária fora do projeto, com caminho absoluto; nada é gravado no projeto. Em C10 ou C11 sem implementação, o G6 vai na própria resposta.
- O bloco do guia e o §0.1 do protocolo já cobrem o C0: bastam para pergunta pontual e para subagentes. Regras de C1–C14 se abrem por busca do ID, não por leitura integral dos arquivos.
- `CONFORMIDADE.md` é proporcional: portões, exceções, pendências humanas e falhas linha a linha; N/A agregado por motivo; Atendidas em amostra com evidência. A tabela integral, uma linha por regra, fica para `PRATICA-COMPLETO` ou risco alto (MET-06).

## Decisões de forma

- `guardar-destrutivo` não usa `disable-model-invocation`: o guarda precisa disparar sozinho diante de uma ação de C6, e a execução depende do "sim" humano no chat (passo 9), não da invocação.
- `revisar-codigo-de-ia` pré-aprova só `git status` (`allowed-tools`) e nega Edit e Write. `git diff`, `git log` e `git show` ficam fora da pré-aprovação porque aceitam `--output`, que grava arquivo; eles, os testes e qualquer outro comando passam pela confirmação normal.
- Várias regras de ORG são hipóteses do autor sobre organizações (cap. 20): adote medindo o efeito (ORG-01).
- Os índices `checklist-completo.md`, `padroes-e-antipadroes.md` e `ferramentas-e-mcp.md` cumprem a estrutura do blueprint apontando para a fonte única de cada lista, sem repetir regras.

