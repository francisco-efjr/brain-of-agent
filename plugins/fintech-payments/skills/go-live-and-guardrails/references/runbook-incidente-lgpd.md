# Runbook de incidente de dados (chave, PAN, PII) com comunicação à ANPD

Sumário: 1. Aviso · 2. Visão geral e prazos · 3. Passo a passo · 4. Os sete itens da comunicação · 5. Modelo de linha do tempo · 6. Rotação de chave · 7. Lições aprendidas · 8. O que está verificado e o que não está

## 1. Aviso

Este runbook organiza a resposta; **não é aconselhamento jurídico**. Quem decide se o incidente exige comunicação, o conteúdo final e o envio são o encarregado de dados (DPO) e o jurídico. O plugin não envia comunicação, não gira chaves e não acessa sistemas: prepara rascunhos e listas para as pessoas responsáveis.

Origem: ANPD, página "Comunicação de Incidente de Segurança" (publicada em 23/12/2022, modificada em 26/08/2026) e Resolução CD/ANPD nº 15/2024 (V-30, V-42); LGPD arts. 46 a 49 (V-42); resposta a chave exposta da Stripe (V-41). Conferido em 2026-10-10. Os artigos 6, 7 e 46 a 49 da lei foram lidos por resumo da ferramenta sobre o texto atualizado da Câmara: **abra o artigo antes de citar literal**. A Lei 9.613/1998 (AML) e KYC não foram lidas e não entram aqui.

## 2. Visão geral e prazos

| Item | Regra (fonte) |
| --- | --- |
| Quando comunicar | incidente de segurança confirmado, que envolve dados pessoais da LGPD e pode causar risco ou dano relevante aos titulares (V-30) |
| Prazo | **3 dias úteis** para comunicar a ANPD e os titulares, citando os arts. 6º e 9º da Resolução CD/ANPD nº 15/2024; lei específica pode fixar outro prazo (V-30, V-42) |
| Comunicação preliminar | permitida com justificativa; complementada em **20 dias úteis** por petição intercorrente no mesmo processo (art. 6º, § 3º) (V-42) |
| Operador | informa o controlador sem demora (V-30) |
| Canal | SEI!ANPD, pelo encarregado ou representante (V-30) |
| Sigilo empresarial | pedido previsto no art. 7º da resolução (V-42) |
| Início da contagem | a partir do conhecimento do incidente pelo controlador (**Inferido**: a página lida pede a data em que se soube, mas o ponto exato de início está no art. 6º da resolução, que deve ser aberto); registre data e hora com a fonte |

A afirmação circulante de que a ANPD "pode pedir cópia da comunicação aos titulares e não exige a lista de afetados" **não foi reconferida**: não a use.

## 3. Passo a passo

1. **Conter (humano, imediato):** se há chave de API, token ou segredo exposto, **girar na hora, antes de investigar** (seção 6). Se há PAN ou PII em log ou repositório, isolar o acesso e preservar evidência (cópia protegida, não apagar antes de registrar).
2. **Classificar:** que dados (PAN, CVV, token, documento, e-mail, dados bancários), quantos titulares (estimativa), por quanto tempo estiveram expostos, quem pode ter acessado. O risco ou dano relevante é avaliado com o encarregado.
3. **Acionar o encarregado e o jurídico**; se houver operador ou provedor envolvido, avisar sem demora (operador informa o controlador).
4. **Abrir a linha do tempo** (seção 5) e manter atualizada; cada entrada com quem, quando e fonte.
5. **Decidir sobre a comunicação** (encarregado): se necessária, preparar o texto com os sete itens (seção 4) e contar os 3 dias úteis a partir do conhecimento. Em dúvida sobre o prazo, o encarregado considera a comunicação preliminar com justificativa.
6. **Contratos e bandeiras:** verifique no contrato com adquirente e provedor se há obrigação própria de notificação e em quanto tempo (**Não verificado** neste plugin; PCI DSS: nenhum requisito numerado foi lido).
7. **Mitigar:** rotação de credenciais, revogação de tokens, bloqueio de contas afetadas, monitoramento de uso indevido (cobranças suspeitas, card testing), orientação aos titulares quando indicado.
8. **Complemento:** reunir o que faltou e enviar em até 20 dias úteis se a comunicação inicial foi preliminar.
9. **Encerrar com lições aprendidas** (seção 7).

## 4. Os sete itens da comunicação ao titular (V-42, Verificado)

1. Natureza e categorias dos dados afetados. 2. Medidas técnicas e de segurança adotadas. 3. Riscos e impactos. 4. Motivo do atraso, se houver. 5. Medidas de mitigação. 6. Data em que se soube do incidente. 7. Contato (encarregado ou canal). Linguagem simples; quando possível, direta e individualizada.

Esqueleto de rascunho (para revisão do encarregado; sem dados reais):

```text
Assunto: Comunicado de incidente de segurança envolvendo seus dados
1) O que aconteceu e quais dados: [descrição curta; categorias de dados, ex.: nome, e-mail, últimos 4 dígitos do cartão].
2) Medidas de segurança adotadas: [contenção, rotação de credenciais, correção].
3) Riscos e impactos possíveis para você: [ex.: tentativa de fraude, phishing].
4) Motivo do atraso, se houver: [ ].
5) O que estamos fazendo para reduzir os riscos: [ ].
6) Quando tomamos conhecimento: [data e hora].
7) Contato: [encarregado / canal].
```

## 5. Modelo de linha do tempo

| Data/hora (fuso) | Evento | Quem | Fonte ou evidência | Prazo derivado |
| --- | --- | --- | --- | --- |
| [conhecimento] | incidente identificado | | | início dos 3 dias úteis |
| | chave girada / acesso isolado | | | |
| | encarregado e jurídico acionados | | | |
| | decisão sobre comunicação | | | |
| | comunicação à ANPD e aos titulares (ou justificativa) | | | 3 dias úteis |
| | complemento | | | 20 dias úteis |

## 6. Rotação de chave exposta (V-41)

1. **Gire agora**, antes de investigar o alcance: gere nova chave no painel do provedor, atualize o cofre ou a variável de ambiente, faça deploy, revogue a antiga. Sequência exata depende do provedor: siga a documentação dele.
2. **Audite** os logs do provedor (uso da chave antiga, IPs, operações de escrita) e os seus logs de aplicação.
3. **Acione o suporte do provedor** se houver uso indevido.
4. Se a chave estava no histórico do Git, a rotação continua obrigatória (reescrever o histórico não revoga a chave).
5. Para segredo de webhook: gere o novo, mantenha o anterior aceito durante a janela do provedor (Stripe: até 24 h com dois segredos ativos; Adyen: aceitar a chave anterior por um tempo) e depois remova (V-03, V-47).
6. Registre na linha do tempo; verifique que nenhum valor de segredo foi copiado para o relatório.

## 7. Lições aprendidas (modelo)

Causa raiz; por que o controle existente não pegou (logging, revisão, permissões); ação corretiva com dono e data (por exemplo `permissions.deny`, varredura de segredos no CI, remoção de PAN dos logs, CSP); teste de regressão que reproduz o defeito; mudança de processo; revisão da matriz de perigos.

## 8. O que está verificado e o que não está

- **Verificado (fonte oficial lida):** prazo de 3 dias úteis, complemento em 20 dias úteis, sete itens, canal SEI!ANPD, papel do operador (ANPD, V-30, V-42).
- **Inferido:** tabela de bases legais prováveis para uma fintech (execução de contrato, obrigação legal ou regulatória, proteção do crédito, legítimo interesse), sujeita ao encarregado.
- **Não verificado:** obrigações de notificação a adquirentes, bandeiras e BCB; requisitos do PCI DSS; texto literal dos arts. 6, 7 e 46 a 49; prazos de retenção de logs.
