# Notas

## Arquivos da skill lidos

Em /Users/francisco.junior/novo projeto/brain-of-agent/skills/qa/:

- SKILL.md
- references/estrategia.md
- references/dominios.md (pagamentos, cartão, PIX/boleto, e-commerce, SaaS multi-tenant)
- references/dados-ambientes-ci.md
- references/processo-e-gestao.md
- references/seguranca.md
- references/design-de-testes.md
- references/automacao-api.md
- assets/templates/plano-de-teste.md
- assets/templates/checklist-release.md
- assets/templates/charter-exploratorio.md

Não li: scripts/ (não executei nenhum), outras referências (web, mobile, performance, acessibilidade, ia-e-llm, unitarios-e-integracao) nem a pasta evals/ do repositório, exceto para escrever nesta pasta de saída.

## Incertezas e decisões

- O pedido não informa: quem emite/processa o cartão, se há sandbox, stack, existência de CI, se há flag. Declarei como suposições e listei 5 perguntas que mudariam o plano.
- Datas: usei D1 a D10 e só mencionei o feriado de 12/10/2026 (segunda, nacional, conforme dominios.md) de forma condicional. A data de hoje vem do ambiente, não do usuário.
- Os critérios de aborto (erro de geração de cartão acima de 1%, qualquer divergência de conciliação) são exemplos inspirados nos da skill; marquei "ajuste ao produto".
- Itens do domínio de cartão que a skill cobre sob a ótica de lojista/gateway (PCI, 3DS, CVV): adaptei para o ponto de vista de emissor sem afirmar regra de escopo PCI. Disse apenas "número completo e CVV fora de log" e deixei conformidade com compliance/jurídico.
- Regras do Banco Central e de crédito (limites, encargos, prazo de fechamento, direito de revisão de decisão automatizada na LGPD) não estão na skill e não citei números nem artigos. Pedi que venham do produto e das normas.
- Tabela de riscos sem P×I numérico: todos os "Alto" justificados por dinheiro, dado do cartão, obrigação legal ou efeito irreversível (critério da skill). R7 classificado como Alto por falha aberta de crédito; R8 como Médio.
- O calendário (alocação de dias, 2 rodadas de correção, congelamento no D8) é minha estimativa, não medida; declarei a suposição das 2 rodadas.
- Nada foi executado (nenhum script, nenhum teste); a resposta diz isso.
- Tamanho da resposta: longa (plano com tabelas), proporcional a um lançamento financeiro com prazo curto, mas no limite do que ainda é escaneável.
