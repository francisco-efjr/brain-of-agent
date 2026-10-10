# Tabela de riscos: <sistema ou mudança>

Como usar: escreva cada risco como **falha → efeito**. P (probabilidade) e I (impacto) de 1 a 3 com as âncoras abaixo; nível = P × I (6–9 Alto, 3–4 Médio, 1–2 Baixo); **impacto 3 nunca fica abaixo de Médio**. Ordene do maior ao menor. Probabilidade vem de quem conhece o código; impacto, de quem conhece o negócio. Reavalie quando o escopo mudar e após incidente. Fonte: brain-of-agent (MIT), `references/estrategia-e-risco.md`.

| Nota | Probabilidade | Impacto |
| --- | --- | --- |
| 1 | código estável, simples, já coberto | incômodo com contorno fácil, poucos usuários |
| 2 | mudança moderada ou integração conhecida | função importante degradada, contorno existe |
| 3 | código novo ou complexo, integração nova, histórico de defeitos | dinheiro ou dados, violação legal ou de segurança, fluxo principal parado, efeito irreversível |

| ID | Risco (falha → efeito) | Característica (ISO 25010) | P | I | Nível | Mitigação executável | Evidência prevista | Dono |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | <cupom aplicado duas vezes no clique duplo → perda de margem> | <Adequação funcional> | <3> | <3> | <9 Alto> | <teste de integração com mesma chave de idempotência> | <saída do teste + consulta ao registro> | <time> |

Checklist: [ ] ao menos uma linha não funcional (desempenho, segurança, acessibilidade) ou motivo para não ter · [ ] mais de um terço "alto"? force um ranking · [ ] riscos do projeto (ambiente, prazo) ficam no plano, não aqui · [ ] "fora do plano" e risco residual declarados.
