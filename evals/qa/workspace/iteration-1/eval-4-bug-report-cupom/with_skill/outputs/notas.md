# Notas

## Arquivos da skill lidos

- skills/qa/SKILL.md
- skills/qa/references/bugs-e-relatorios.md (anatomia do bug, título, redução, intermitente, evidências/LGPD, severidade x prioridade, bug advocacy)
- skills/qa/assets/templates/bug-report.md (estrutura do relatório e exemplo preenchido)
- skills/qa/references/mobile.md (resposta antiga após consulta nova, matriz de dispositivos, evidências de falha)
- skills/qa/references/dominios.md (seção e-commerce: cupons, frete por CEP, checkout)
- Só um grep em references/dados-ambientes-ci.md para achar a taxonomia de flaky citada em bugs-e-relatorios.md; não encontrei e não li o arquivo.
- Nenhum script executado (a probabilidade 0,6^3 ≈ 22% e 0,6^5 ≈ 8% foi calculada à mão).

## Incertezas e decisões

- Valores, CEPs, itens do carrinho, build, versão do Android, ambiente, horários e request ids não foram informados; deixei como **[preencher]** em vez de inventar.
- Tipo e regra do BLACK10 (percentual ou fixo, restrição por região/frete) são desconhecidos. Não assumi 10%.
- Resultado esperado: a regra de negócio (cupom vale ou não para o novo CEP) não é conhecida. Usei como oráculo a consistência tela x cobrança e deixei os dois desfechos válidos, marcando a regra para confirmação com dev/PO.
- Severidade Crítica (dinheiro cobrado errado, sem contorno) segue a tabela da skill. A prioridade depende de o BLACK10 estar ativo para clientes reais e da campanha; deixei condicional e atribuí a decisão ao PO.
- Não ficou claro se o pedido 88123 é de cliente real ou de teste, nem se o ambiente é produção; tratei a correção do valor cobrado do cliente como ação à parte, condicional.
- Hipóteses de causa (recálculo no servidor descartando cupom, corrida entre respostas) são inferências a partir da intermitência e do padrão de mobile.md; marcadas como não confirmadas.
- O cálculo sobre tentativas no iPhone assume a mesma taxa de 40% do Android e tentativas independentes; é uma ordem de grandeza para orientar o relato, não um teste estatístico.
- "Total continua com desconto na tela" foi lido como: o total exibido segue o valor com desconto, e a linha de desconto some. Se o relato for outro (por exemplo, o total já aparece sem desconto na tela), o título e o resultado obtido mudam.
