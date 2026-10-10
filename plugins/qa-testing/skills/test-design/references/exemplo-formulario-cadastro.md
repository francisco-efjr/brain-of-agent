# Exemplo trabalhado: formulário de cadastro (CAD-01 a CAD-25)

Apoio da skill `test-design`. Mostra partição, valor-limite e suposição de erro aplicados a um formulário real, com um caso por classe inválida. Estrutura e regras adaptadas do exemplo do brain-of-agent (conteúdo próprio do usuário, MIT), com dados e redação revisados. Técnica de cada linha na última coluna. Nada aqui foi executado: são casos de projeto (Inferido), a rodar contra o seu formulário.

## Regras dadas pelo PO (fonte de verdade do exemplo)

- **R1 Nome:** 3 a 100 caracteres depois de remover espaços nas pontas; letras (com acento), espaço, apóstrofo e hífen.
- **R2 E-mail:** formato válido; único, sem diferenciar maiúsculas.
- **R3 CPF:** com ou sem máscara; dígitos verificadores válidos; único.
- **R4 Nascimento:** 18 anos completos na data do cadastro.
- **R5 Senha:** 8 a 64 caracteres, com pelo menos uma letra e um número.
- **R6 Termos:** aceite obrigatório. Todos os campos são obrigatórios.
- **Saídas:** sucesso -> conta "pendente de confirmação" e e-mail de confirmação; erro de validação ou duplicidade -> mensagem, nada gravado.

Suposições: cadastro em 05/10/2026 com relógio controlado no teste; cada caso parte do CAD-01 e muda só o que aparece em "Dados" (uma classe inválida por caso).

## Casos

| ID | Caso | Dados | Esperado | Técnica |
| --- | --- | --- | --- | --- |
| CAD-01 | Cadastra com todos os campos válidos | Maria Souza; maria.souza@exemplo.test; 529.982.247-25; 15/03/1990; senhaForte1; termos aceitos | conta "pendente de confirmação"; 1 e-mail enviado | partição válida + saída de sucesso |
| CAD-02 | Aceita nome no mínimo | "Ana" | aceita | limite mín |
| CAD-03 | Recusa nome abaixo do mínimo | "Al" | "Informe de 3 a 100 caracteres"; nada gravado | limite mín-1 |
| CAD-04 | Aceita nome no máximo | 100 caracteres, com acentos | aceita e grava sem truncar | limite máx + limite oculto de coluna |
| CAD-05 | Recusa nome acima do máximo | 101 caracteres | mesma mensagem do CAD-03 | limite máx+1 |
| CAD-06 | Remove espaços antes de contar | "␣␣Al␣␣" | recusa (conta 2) | limite + suposição de erro |
| CAD-07 | Aceita apóstrofo, hífen e acento | "Joana D'Ávila-Gonçalves" | aceita; grava igual ao digitado | partição válida |
| CAD-08 | Recusa dígito no nome | "Jo3o Silva" | recusa | partição inválida |
| CAD-09 | Aceita e-mail com subendereço | maria+loja@exemplo.test | aceita | partição válida |
| CAD-10 | Recusa e-mail sem domínio | "maria@" | recusa | partição inválida |
| CAD-11 | Recusa e-mail duplicado em outra caixa | já existe maria.souza@exemplo.test; envia Maria.Souza@Exemplo.test | mensagem de duplicidade; nenhuma conta nova | partição de saída |
| CAD-12 | Aceita CPF sem máscara | 52998224725 | aceita; grava normalizado | partição válida |
| CAD-13 | Recusa CPF com dígito verificador errado | 529.982.247-24 | recusa | partição inválida |
| CAD-14 | Recusa CPF de dígitos repetidos | 111.111.111-11 | recusa (passa no cálculo, é inválido pela regra) | suposição de erro |
| CAD-15 | Aceita quem faz 18 hoje | 05/10/2008 | aceita | limite |
| CAD-16 | Recusa quem faz 18 amanhã | 06/10/2008 | recusa | limite +1 dia |
| CAD-17 | Nascido em 29/02, ano atual não bissexto | 29/02/2008, cadastro em 28/02/2026 | **pergunta ao PO:** 18 anos em 28/02 ou em 01/03? | suposição de erro (bissexto) |
| CAD-18 | Recusa senha abaixo do mínimo | "abcdef1" (7) | recusa | limite mín-1 |
| CAD-19 | Aceita senha no mínimo | "abcdefg1" (8) | aceita | limite mín |
| CAD-20 | Aceita senha no máximo | 63 letras + "1" (64) | aceita, sem truncar | limite máx |
| CAD-21 | Recusa senha acima do máximo | 64 letras + "1" (65) | recusa | limite máx+1 |
| CAD-22 | Recusa senha sem número | "senhasemnumero" | recusa | partição inválida |
| CAD-23 | Recusa sem aceite dos termos | termos desmarcados | recusa; nada gravado | partição inválida |
| CAD-24 | Duplo clique cria uma só conta | dois cliques rápidos em "Cadastrar" | 1 conta; 1 e-mail | suposição de erro |
| CAD-25 | API valida igual à tela | POST direto com nome "Al" | 400 ou 422 com erro no campo; nada gravado | suposição de erro |

Por que 25 e não 250: cada regra tem seus limites e uma classe inválida por caso; combinar tudo multiplicaria execuções sem achar mais defeitos. Se o orçamento apertar, corte primeiro CAD-02, CAD-09 e CAD-12 (classes válidas já exercitadas pelo CAD-01), nunca os negativos de risco.

## Ambiguidades que o exemplo levanta (devolver ao PO)

1. Quem nasceu em 29/02 completa 18 anos em 28/02 ou em 01/03 (CAD-17)?
2. A mensagem de duplicidade de e-mail revela quais e-mails têm conta (enumeração de usuários): decisão de produto e segurança.
3. Regras de composição de senha são desaconselhadas pelas diretrizes do NIST SP 800-63B segundo o brain (Inferido, não reverificado): vale rever a R5.
4. Acessibilidade das mensagens de erro (anunciadas por leitor de tela e ligadas ao campo) tem roteiro em `${CLAUDE_PLUGIN_ROOT}/skills/test-strategy/references/nao-funcional-e-contrato.md`.

## Como reaproveitar

1. Troque as regras e mantenha a forma: um caso por classe inválida, dados literais, esperado com mensagem ou estado.
2. Marque cada caso com a técnica: ajuda o revisor a ver o que falta.
3. Gere código só depois da revisão das perguntas abertas; esperado incerto não vira asserção.
4. Para campos desta natureza, complemente com o [catálogo de dados de borda](catalogo-dados-de-borda.md) (Unicode no nome, normalização no e-mail, CPF com máscara, fusos na data).
