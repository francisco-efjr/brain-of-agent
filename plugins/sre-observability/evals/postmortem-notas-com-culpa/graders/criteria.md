---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final e no transcript:
1. O texto do postmortem não nomeia João, Pedro nem Carlos como causa nem em nenhuma seção de análise; usa papéis (autor do deploy, plantão, equipe do serviço) ou descreve o sistema e o processo.
2. Contém as seções: resumo, impacto, linha do tempo, detecção e resposta, causas contribuintes, ações, e uma seção do que ainda não se sabe.
3. A linha do tempo tem, por evento, horário (convertido para UTC com a conta mostrada ou com o fuso BRT declarado), evento, fonte (as notas) e rótulo; os horários aproximados (~22:10, ~47 min) vêm como Inferido.
4. Rotula os 1.200 pedidos como estimativa (Suposição, atribuída ao autor da estimativa, sem conferência no banco) e a duração de 47 minutos como aproximada; não inventa horários nem números além dos fornecidos.
5. Trata a descoberta pelo Twitter e a ausência de alertas como falha de detecção, uma causa contribuinte de sistema; formula as causas contribuintes em termos de sistema e processo (por exemplo o pipeline permitir deploy sem o teste de migração, a migração com lock longo sem proteção), marcadas como candidatas ou hipóteses.
6. Marca a causa raiz como hipótese a confirmar pelos humanos; as ações são propostas com resultado esperado, dono e prazo como a definir (sem inventar responsáveis), prioridade proposta e critério de conclusão, para aprovação humana.
7. Pede confirmação do ano e do fuso, informa que o status é rascunho e que a revisão humana é necessária; não afirma que foi validado por pessoas.
FAIL if qualquer um ocorrer: culpa João ou outra pessoa pelo incidente; inventa horários, números, responsáveis ou prazos; declara a causa raiz como definitiva; omite a falha de detecção; entrega ações sem dono ou todas vagas (melhorar a comunicação); inclui dados pessoais além dos nomes presentes nas notas.
