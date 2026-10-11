# Acessibilidade, performance e conformidade BR do checkout

Modelo-alvo e data de validação: Claude 4.x/5.x, 2026-10-10. Nada aqui é parecer jurídico ou certificação de acessibilidade. Fontes: WCAG 2.2 Quick Reference e Understanding 3.3.7 (V-16, V-53), web.dev Core Web Vitals (V-15), Decreto 7.962/2013 e LGPD (V-32), CDC art. 49 (V-55), página da ANPD sobre comunicação de incidentes (V-54).

## 1. WCAG 2.2 no formulário de checkout

Grau de evidência por achado (vale o menor): **Verificado** (reproduzido com ferramenta ou código lido), **Sinalizado** (varredura automática ou leitura indica, sem confirmação), **Requer humano** (teste com leitor de tela, teclado, zoom). "Não determinado" é resposta válida e deve aparecer no relatório.

| Critério | Nível | O que verificar no checkout | Evidência típica |
|---|---|---|---|
| 3.3.1 Identificação do erro | A* | Erro descrito em texto e associado ao campo (`aria-describedby`, `aria-invalid`) | Código lido + teste manual |
| 3.3.2 Rótulos ou instruções | A* | Rótulo visível por campo; placeholder não é rótulo | Código lido (`<label for>`) |
| 3.3.3 Sugestão de erro | AA* | "CEP deve ter 8 dígitos" em vez de "inválido" | Código lido |
| 3.3.4 Prevenção de erros (financeiro) | AA* | Revisão e confirmação do pedido antes de pagar; correção possível | Fluxo percorrido |
| 3.3.7 Entrada redundante | A (Verificado em V-53) | Dado já informado é preenchido ou selecionável; erro de validação não apaga o digitado | Fluxo percorrido + código |
| 3.3.8 Autenticação acessível (mínimo) | AA (V-16, arquivo awesome-copilot) | Login/OTP sem teste cognitivo; colar e autofill liberados (`autocomplete`, sem `onpaste="return false"`) | Código lido + manual |
| 1.3.5 Identificar a finalidade da entrada | AA* | `autocomplete="postal-code"`, `"street-address"`, `"cc-number"` e afins | Código lido; varredura |
| 2.4.7 Foco visível | AA* | Outline não removido (`outline: none` sem substituto) | CSS lido + teclado |
| 2.5.8 Tamanho do alvo (mínimo) | AA (V-16) | Alvos >= 24 x 24 px CSS (ou espaçamento equivalente) | Medição |
| 1.4.3 Contraste (mínimo) | AA (V-16) | Texto 4,5:1; texto grande e componentes 3:1 | Ferramenta de contraste |
| Reflow | AA (1.4.10)* | Sem rolagem horizontal em 320 px de largura | Redimensionar |

\* Níveis marcados com asterisco: **Inferido** (conhecimento da norma); a página lida em V-16 foi truncada nesses critérios. Confira no Quick Reference antes de citar o nível em relatório formal. `prefers-reduced-motion` é boa prática ligada a 2.3.3, que é **AAA**, não AA (V-16).

Regras de método (V-16, padrão de `ecom-a11y-audit`, MIT, só o padrão): severidade P0 (impede concluir a compra), P1 (dificulta), P2 (incômodo); nunca afirmar conformidade a partir de varredura limpa; o que a automação não testou fica "não determinado". Teste de leitor de tela e de teclado completo é manual e deve constar como pendência quando não foi feito. A estimativa popular de que "automação cobre 20 a 40%" não foi confirmada em V-16: não cite.

### Checklist 3.3.7 (V-53)

1. "Cobrança igual à entrega" disponível; marcada por padrão é boa prática (**Inferido**: a página só exige poder evitar a digitação).
2. CEP, telefone e nome não pedidos de novo em outra etapa.
3. Erro de validação (por exemplo, cartão recusado, CEP inválido) não apaga o que o usuário digitou, incluindo o formulário do cartão quando o provedor permitir.
4. Reentrada só nas exceções previstas (essencial, segurança, dado que deixou de valer), com justificativa registrada.
5. Autocomplete do navegador sozinho não basta como cumprimento.

## 2. Core Web Vitals como critério de aprovação (V-15)

| Métrica | Bom (p75) | Observação |
|---|---|---|
| LCP | <= 2,5 s | Imagem principal da PDP, banner do carrinho |
| INP | <= 200 ms | Cliques em "Aplicar cupom", "Pagar" |
| CLS | <= 0,1 | Total/frete que muda de altura, banners tardios |

Aprovação exige as três metas no percentil 75, mobile e desktop separados. Fonte de campo (CrUX, PageSpeed, Search Console) é a principal; laboratório serve para regressão. Lighthouse não mede INP; Total Blocking Time é proxy. Limites "ruim" (4 s, 500 ms, 0,25) vêm de um arquivo da comunidade, não da página web.dev (V-15). Relate sempre a fonte do número: "campo" ou "laboratório". Página web.dev com última atualização de 31/10/2024: confira se as metas mudaram.

## 3. Conformidade BR de checkout (tabela; cada linha "Requer revisão jurídica")

Textos legais lidos em 2026-10-10 no Planalto (V-32, V-55). Paráfrase; não cite como texto literal. Use o modelo `tabela-conformidade-br.md` (colunas: requisito, artigo, onde está implementado, status, evidência).

| # | Requisito | Base | Onde verificar | Status inicial |
|---|---|---|---|---|
| 1 | Nome empresarial, CPF/CNPJ, endereço físico e eletrônico em destaque | Decreto 7.962/2013, art. 2º | Rodapé, página de oferta | Não determinado |
| 2 | Preço final com despesas adicionais (entrega, seguros) discriminadas | art. 2º, IV | Carrinho, resumo, e-mail | Não determinado |
| 3 | Condições integrais da oferta (pagamento, disponibilidade, prazo de entrega) e restrições | art. 2º | PDP, checkout | Não determinado |
| 4 | Sumário do contrato antes da contratação; ferramenta para identificar e corrigir erros antes de finalizar | art. 4º | Etapa de revisão (3.3.4 também) | Não determinado |
| 5 | Confirmação imediata do recebimento do pedido; contrato em meio que permita conservação | art. 4º | E-mail/página de confirmação | Não determinado |
| 6 | Atendimento eletrônico eficaz com resposta em até 5 dias | art. 4º | Canal, SLA interno | Não determinado |
| 7 | Mecanismos de segurança eficazes para pagamento e dados | art. 4º | Esta skill, passos 2 a 4 | Parcial por revisão técnica |
| 8 | Meios do direito de arrependimento informados e exercíveis pela mesma ferramenta da contratação; confirmação imediata; comunicação à administradora do cartão para não lançar ou estornar | art. 5º | Área do cliente, política | Não determinado |
| 9 | Mapa de dados pessoais, base legal por finalidade (execução de contrato para entrega/pagamento; consentimento separado para marketing), retenção | LGPD arts. 6º, 7º | Registro de tratamento | Não determinado |
| 10 | Canal do titular (art. 18), contato do encarregado (art. 41) | LGPD | Política de privacidade | Não determinado |
| 11 | Plano de incidente com comunicação à autoridade e ao titular | LGPD art. 48; Res. CD/ANPD 15/2024 | Runbook (seção 5) | Não determinado |

Multa LGPD do art. 52 (até 2% do faturamento no Brasil, limitada a R$ 50 milhões por infração) é Verificada em V-32 e serve de contexto de risco, não de cálculo.

## 4. Arrependimento e devolução (V-55)

- CDC art. 49 (texto compilado do Planalto, lido): 7 dias contados da assinatura ou do recebimento do produto ou serviço, quando a contratação ocorre **fora do estabelecimento comercial**, "especialmente por telefone ou a domicílio". O caput **não cita a internet**. O parágrafo único manda devolver de imediato, com atualização monetária, os valores pagos "a qualquer título" durante o prazo de reflexão.
- A aplicação ao comércio eletrônico se apoia na leitura de "fora do estabelecimento" e no Decreto 7.962/2013, art. 5º (V-32).
- **Inferido**: contagem em dias corridos; devolução do frete. **Suposição/Não verificado**: "sem exigir motivo" e "política interna não restringe o direito" (não constam do art. 49).
- Regra do plugin: o prazo e a contagem seguem a decisão registrada com o jurídico; o reembolso ao PSP exige aprovação humana e chave de idempotência própria (skill `estoque-reserva-pedido`).

## 5. Relógio de incidente de dados pessoais (V-54; Requer revisão jurídica)

Fonte: página da ANPD sobre comunicação de incidentes (resumo da Resolução CD/ANPD nº 15/2024); a resolução integral não foi lida.

| Passo | Ação | Rótulo |
|---|---|---|
| 1 | Marcar data e hora da ciência do incidente | Verificado (o prazo depende dela; gatilho exato no texto integral: Não verificado) |
| 2 | Registrar o incidente | Boa prática; obrigação de registrar e reter: **Não verificada** (rejeitada como fato em V-54) |
| 3 | Avaliar risco ou dano relevante | LGPD art. 48 (Verificado em V-32) |
| 4 | Comunicar ANPD e titulares em 3 dias úteis, salvo prazo previsto em lei específica | Verificado na página; Requer revisão jurídica |
| 5 | Faltando informação: comunicação preliminar e complemento em até 20 dias úteis, no mesmo processo; a preliminar sozinha não cumpre o art. 48 | Verificado na página |
| 6 | Conteúdo ao titular: linguagem simples, natureza e categorias dos dados, medidas técnicas e de segurança, riscos e impactos, motivo de atraso, mitigação, data de ciência, contato (e do encarregado) | Verificado na página (art. 9º da resolução, segundo a página) |

A decisão de comunicar é do controlador com o jurídico, nunca do agente; o envio real exige aprovação humana. Modelo: `runbook-incidente-dados-pessoais.md` em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/`.
