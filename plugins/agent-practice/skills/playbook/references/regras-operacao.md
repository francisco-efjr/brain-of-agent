# OPS — Operação, entrega e produção

Legenda em [regras-metodo.md](regras-metodo.md).

## Obrigatório

- **OPS-01** [A+H · C8] Nada vira "produção" sem backups testados com restauração ensaiada e sem monitoramento. — _por quê:_ sem ver o estado do sistema, só resta torcer. _(cap. 16)_
- **OPS-02** [A+H · C6 C8] Snapshots automáticos (no mínimo de hora em hora) com retenção por hora, dia, semana e mês, e restauração conhecida antes de precisar. — _por quê:_ desfaz em segundos o erro de minutos atrás. _(cap. 16; ap. G)_
- **OPS-03** [A+H · C6 C8] Backup externo automático, versionado com retenção em camadas, criptografado, fora do alcance do agente e testado abrindo arquivos restaurados (no mínimo alguns por mês); dado crítico tem cópia em outro local físico. — _por quê:_ snapshot morre com o disco; redundância de disco não cobre perda do aparelho; o aviso "concluído" não prova nada. _(cap. 16; ap. G)_
- **OPS-04** [A+H · C8 C13] Antes de acelerar entregas: testes de lógica e de integração (concorrência, falha no meio), CI em toda mudança, revisão automática desconfiada, feature flag, staging, rollback em minutos e monitoramento. — _por quê:_ entregar rápido só é seguro com as travas prontas. _(cap. 20)_
- **OPS-05** [A+H · C8] Entregue com frequência, em lotes pequenos, atrás de chave e reversíveis, ao cliente real. — _por quê:_ o uso real acha o que o teste não acha, e corrigir ficou barato. _(cap. 20)_
- **OPS-06** [A+H · C8] Calibre a velocidade pelo custo do erro; rollback não desfaz efeito externo (pagamento, ação física, e-mail enviado), migração de banco, biblioteca publicada nem revisão de loja. — _por quê:_ esses casos pedem trava antes, não reversão depois. _(cap. 20)_
- **OPS-07** [A+H · C8] Em sistema regulado (saúde, finanças), testes de cenário pesados e mais de uma trava por modo de falha, para código humano ou de IA. _(cap. 20)_
- **OPS-08** [A · C6 C8] Mudança de esquema em três tempos: acrescente o formato novo sem remover o velho, migre, e só então remova o velho. _(cap. 20)_
- **OPS-09** [A+H · C8] Nada roda em produção sem forma de recuperação; o botão de produção tem um responsável nominal. _(cap. 16)_
- **OPS-10** [A · C8 C9] Toda falha é registrada com detalhe técnico e gera alerta visível num canal olhado todo dia; erro nunca é engolido (busca externa que falha não devolve lista vazia como se fosse sucesso). — _por quê:_ credencial vencida engolida deixou nove de dez processos mortos sem sinal. _(cap. 6)_
- **OPS-11** [A+H · C8 C9] Com serviço sobrecarregado, use disjuntor (pausa e segue degradado) em vez de manada de retentativas; resiliência é decidida por quem conhece horários e picos do sistema. — _por quê:_ o agente nunca sugere disjuntor porque não conhece o tráfego. _(cap. 7)_
- **OPS-12** [A · C8 C9] Tarefas automáticas são idempotentes (rodar duas vezes não duplica) e têm fonte reserva. _(cap. 7)_
- **OPS-13** [A · C8] Confira os limites do destino antes de publicar (tamanho de e-mail que o cliente corta, formato aceito pela loja). — _por quê:_ leitores perderam o fim de uma edição. _(cap. 7)_
- **OPS-14** [A+H · C8] Software nunca está pronto: depois do deploy espere dezenas de decisões novas, trate como 0.1 até ter usuários reais e não lance com qualidade de descartável. — _por quê:_ mais de cem commits vieram depois do "pronto". _(caps. 7, 10)_
- **OPS-15** [H · C8] Configure alertas de saúde de infraestrutura (discos, serviços), acompanhe-os e planeje compra e recuperação antes do desastre; a reconstrução de disco é o momento de maior risco. — _por quê:_ o aviso existia havia mais de um mês; compra sob urgência saiu três vezes mais cara. _(cap. 16)_
- **OPS-16** [A+H · C9] Tenha plano B para recusa por política de conteúdo (modelo local para texto sensível legítimo); retentar em contexto limpo não resolve. — _por quê:_ filtros comerciais usam régua grossa e barram tema legítimo; perde-se controle. _(interlúdio 1)_
- **OPS-17** [A · C8 C10] Não deixe saldo pré-pago ou cota acabar no meio de execução longa. — _por quê:_ uma prova parou sozinha de madrugada. _(cap. 11)_
