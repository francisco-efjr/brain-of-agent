# Relatório de acessibilidade do checkout com grau de evidência

Uso: auditoria WCAG 2.2 de formulários de endereço, frete, pagamento e erro. Base: V-16, V-53 (padrão de evidência do `ecom-a11y-audit`, MIT). Varredura limpa **não prova** conformidade; o que a automação não testou fica "não determinado"; leitor de tela é teste manual.

## 1. Escopo
- Páginas e fluxos: [LISTA] · Componentes hospedados por terceiros (fora do controle): [LISTA] · Ferramentas usadas: [NOME E VERSÃO | nenhuma] · Data: [AAAA-MM-DD]

## 2. Graus de evidência
**Verificado** (testado, evidência anexa) · **Sinalizado** (detectado automaticamente, sem confirmação) · **Requer humano** (leitor de tela, foco, linguagem). Prevalece o **menor** grau. Severidade: P0 bloqueia a compra, P1 dificulta, P2 melhoria.

## 3. Critérios
| Critério | Nível | Resultado | Grau | Sev. | Evidência (tela, trecho, comando) | Correção |
| --- | --- | --- | --- | --- | --- | --- |
| 3.3.2 Rótulos ou instruções | A | [ok/falha/não determinado] | [grau] | | | |
| 3.3.1 Identificação do erro | A | | | | | |
| 3.3.3 Sugestão de erro | AA | | | | | |
| 3.3.4 Prevenção de erros (financeiro) | AA | | | | | |
| 3.3.7 Entrada redundante | A | | | | "cobrança igual à entrega"; erro não apaga o digitado | |
| 3.3.8 Autenticação acessível (mínimo) | AA | | | | colar e autofill liberados | |
| 1.3.5 Finalidade da entrada | AA | | | | `autocomplete` | |
| 2.4.7 Foco visível | AA | | | | | |
| 2.5.8 Tamanho do alvo (mínimo) | AA | | | | alvos ≥ 24×24 px | |
| 1.4.3 Contraste (mínimo) | AA | | | | 4,5:1 e 3:1 | |
| 1.4.10 Reflow | AA | | | | 320 px | |

Níveis A/AA de 3.3.1, 3.3.2, 3.3.3, 3.3.4, 2.4.7, 1.3.5 e 1.4.10 foram dados como conhecimento da norma (Inferido); 3.3.7, 3.3.8 e 2.5.8 foram lidos na documentação. `prefers-reduced-motion` é 2.3.3 (AAA): boa prática, não requisito AA.

## 4. Não determinado
- [O QUE A AUTOMAÇÃO NÃO TESTOU: leitor de tela, ordem de foco em modal de 3DS, mensagens dinâmicas]

## 5. Conclusão
- P0: [N] · P1: [N] · P2: [N]. Nenhuma afirmação de "conforme" sem teste manual. Próximo passo: [AÇÃO]
