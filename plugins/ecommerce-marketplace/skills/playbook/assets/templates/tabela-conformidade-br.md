# Tabela de conformidade do checkout BR

Uso: mapa de requisitos legais do checkout, com onde está implementado e a evidência. **Não é parecer jurídico**: toda linha leva "Requer revisão jurídica". Textos lidos em planalto.gov.br e gov.br/anpd em 2026-10-10 e **parafraseados**; releia a versão vigente e registre a data. Base: V-32, V-53, V-54, V-55.

- Data da leitura da norma: [AAAA-MM-DD] · Revisor jurídico: [NOME | pendente] · Loja/versão: [X]

| # | Requisito (paráfrase) | Artigo | Onde está implementado (arquivo/tela) | Status (atende / parcial / não / a verificar) | Evidência | Rótulo | Revisão |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Identificação do fornecedor em local de destaque: nome empresarial, CPF/CNPJ, endereços físico e eletrônico | Decreto 7.962 art. 2º | [rodapé/oferta] | | | Verificado (norma) | Requer revisão jurídica |
| 2 | Preço com despesas adicionais (entrega, seguros) discriminadas antes do pagamento | Decreto 7.962 art. 2º, IV | [carrinho/revisão] | | | Verificado | Requer revisão jurídica |
| 3 | Características essenciais, condições da oferta (pagamento, disponibilidade, prazo de entrega) e restrições | Decreto 7.962 art. 2º | [página do produto] | | | Verificado | Requer revisão jurídica |
| 4 | Sumário do contrato antes de contratar; ferramentas para identificar e corrigir erros antes de finalizar | Decreto 7.962 art. 4º | [etapa de revisão] | | | Verificado | Requer revisão jurídica |
| 5 | Confirmação imediata do recebimento da aceitação; contrato em meio que permita conservação | Decreto 7.962 art. 4º | [e-mail/conta] | | | Verificado | Requer revisão jurídica |
| 6 | Atendimento eletrônico eficaz, resposta em até 5 dias | Decreto 7.962 art. 4º | [canal] | | | Verificado | Requer revisão jurídica |
| 7 | Mecanismos de segurança eficazes para pagamento e dados | Decreto 7.962 art. 4º | [PSP, TLS] | | | Verificado | Requer revisão jurídica |
| 8 | Informar os meios do direito de arrependimento; exercício pela mesma ferramenta da contratação; comunicação à administradora do cartão; confirmação imediata | Decreto 7.962 art. 5º (não relido) | [conta do cliente] | | | Inferido (artigo não relido) | Requer revisão jurídica |
| 9 | Desistência em 7 dias do recebimento em contratação fora do estabelecimento; devolução imediata dos valores pagos a qualquer título | CDC art. 49 | [política] | | | Verificado (texto); "dias corridos" e "frete devolvido" = Inferido | Requer revisão jurídica |
| 10 | Cumprir as condições da oferta (prazos, quantidade, qualidade) | Decreto 7.962 art. 6º | [logística] | | | Verificado | Requer revisão jurídica |
| 11 | Mapa de dados pessoais do checkout com base legal por finalidade (execução de contrato; consentimento separado para marketing) | LGPD arts. 6º, 7º | [inventário] | | | Verificado | Requer revisão jurídica |
| 12 | Canal do titular (confirmação, acesso, correção, eliminação, portabilidade, revogação) | LGPD art. 18 | [canal] | | | Verificado | Requer revisão jurídica |
| 13 | Registro das operações de tratamento; encarregado indicado e contato divulgado | LGPD arts. 37, 41 | [documento] | | | Verificado | Requer revisão jurídica |
| 14 | Plano de incidente: comunicação à ANPD e aos titulares (3 dias úteis; complemento em 20 dias úteis) | LGPD art. 48; Res. CD/ANPD 15/2024 (página de tópico) | [runbook] | | | Verificado (página); gatilho e registro: Não verificado | Requer revisão jurídica |
| 15 | Entrada redundante: dado já informado não é pedido de novo ("cobrança igual à entrega"; erro não apaga o digitado) | WCAG 3.3.7 (nível A) | [formulário] | | | Verificado | n/a (norma técnica) |
| 16 | Cartão: número, CVV e trilha fora do backend da loja; escopo de PCI decidido com o adquirente | PCI DSS (versão não lida) | [campos hospedados] | | | Inferido (redução de escopo); versão Não verificada | Requer revisão especializada |

## Pendências e limites
- Regulamentos da ANPD além da página de tópico e CDC além do art. 49: **não lidos**.
- Multa da LGPD (art. 52: até 2% do faturamento, limitada a R$ 50 milhões por infração) é referência de risco, não cálculo.
- Próximo passo: [AÇÃO] · Responsável: [NOME]
