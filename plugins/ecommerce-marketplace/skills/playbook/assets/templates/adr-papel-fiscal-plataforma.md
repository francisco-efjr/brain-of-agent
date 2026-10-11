# ADR: papel fiscal da plataforma

Uso: marketplace que decide entre exigir NF-e do vendedor e atuar como substituta tributária por opção (LC 214/2025, art. 22). **Requer revisão tributária**; este documento não é parecer. Base: V-33, V-34, V-57. Leitura da norma em 2026-10-10; releia o texto compilado e os atos conjuntos antes de decidir.

- Status: [proposto | aprovado] · Data: [AAAA-MM-DD] · Decisores: [PRODUTO, JURÍDICO, CONTADOR] · Data de leitura da norma: [AAAA-MM-DD]

## 1. Contexto
- Perfil dos vendedores: [MEI | PJ | mistos] · Volume: [X] · Regimes: [Simples | Lucro Presumido | Lucro Real] · Operações: [B2C | B2B] · Interestaduais: [SIM/NÃO]

## 2. O que a norma lida diz (parafraseado)
- Art. 22: plataformas digitais respondem pelo pagamento de IBS e CBS das operações feitas por seu intermédio, solidariamente com o adquirente e, para fornecedor no País, solidariamente em hipóteses que incluem a plataforma não fornecer as informações exigidas ou o fornecedor não emitir documento fiscal eletrônico; a plataforma pode optar, com anuência do fornecedor, por ser substituta tributária (emite documentos fiscais eletrônicos, apura e paga). **Verificado** (V-33).
- 2026: IBS 0,1% e CBS 0,9%, compensáveis; 2027–2028: arts. 344 e 347. Demais anos e alíquotas finais: **Não verificável**.
- Split payment (arts. 31–35): PSPs segregam e recolhem na liquidação e não são responsáveis tributários; calendário e campos: **Não verificável**.

## 3. Alternativas
| Opção | O que a plataforma assume | Dados exigidos do vendedor | Risco | Custo operacional |
| --- | --- | --- | --- | --- |
| A. Exigir NF-e do vendedor e validar | Verificação do documento por operação | Chave da NF-e, CNPJ/CPF, regime | Responsabilidade solidária se o vendedor não emitir | [X] |
| B. Substituta tributária por opção | Emissão de documentos, apuração e pagamento | Dados fiscais do produto/operação, anuência | Complexidade fiscal e de sistema | [X] |
| C. Alternativa mais simples: [EX.: só vendedores PJ com emissor integrado] | | | | |

## 4. Decisão
- Escolha: [OPÇÃO] · Motivo: [UMA FRASE] · Condições: [EX.: contrato de adesão com cláusula de anuência]

## 5. Dados exigidos do vendedor
| Dado | Obrigatório | Validação | Onde guardar |
| --- | --- | --- | --- |
| CNPJ/CPF (incl. CNPJ alfanumérico) | sim | DV (ASCII − 48) | cadastro (texto) |
| Regime tributário | [sim] | declaração + contador | [X] |
| Inscrição estadual / ISENTO | [sim] | regra da UF | [X] |
| Chave de acesso da NF-e por pedido | [conforme opção] | 44 posições, DV módulo 11 | pedido |

## 6. Implementação (sem emissão real)
- Homologação apenas; alíquotas e NTs em tabela versionada ([ficha-nt-fiscal-versionada.md](ficha-nt-fiscal-versionada.md)); teste de data 31/12/2026 × 01/01/2027; nenhum valor fixo no código.

## 7. Não verificável
- [Campos IBS/CBS na NF-e; MOC; calendário do split; regras estaduais; DIFAL do caso] · Revisão fiscal: [PENDENTE/FEITA por NOME em DATA]
