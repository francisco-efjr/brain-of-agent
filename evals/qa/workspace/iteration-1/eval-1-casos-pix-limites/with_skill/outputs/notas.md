# Notas da execução (eval-1, casos PIX limites, with_skill)

## Arquivos da skill lidos

- `skills/qa/SKILL.md` (inteiro)
- `skills/qa/references/design-de-testes.md` (inteiro; valor-limite com 3 valores para dinheiro, tabela de decisão, partição, exemplo trabalhado, "quantos testes bastam")
- `skills/qa/references/dominios.md` (inteiro; seções Pagamentos e fintech e PIX: limites, virada do limite, limite noturno, concorrência de saldo, dispositivo novo, EndToEndId)
- `skills/qa/assets/templates/caso-de-teste.md` (colunas da tabela, formato para importar em Xray)
- `skills/qa/scripts/valores_limite.py` (li o cabeçalho e rodei `numero --min 0.01 --max 5000 --passo 0.01`, `--max 1000` e `--self-test`)

Não li: estrategia.md, requisitos-e-bdd.md, bugs-e-relatorios.md, automacao-api.md, dados-ambientes-ci.md, seguranca.md e os demais scripts. Não usei a ferramenta Skill nem a pasta evals/ (exceto a pasta de saída).

## Arquivos produzidos (todos na pasta outputs)

- `resposta.md`: texto final ao usuário
- `casos_pix_limites_xray.csv`: 43 testes, 8 colunas, 1 passo por teste, UTF-8 sem BOM, todos os campos entre aspas
- `gerar_casos.py`: fonte única dos casos; gera o CSV e `tabela_chat.md`
- `tabela_chat.md`: fragmento de tabela embutido na resposta (apoio)

## Incertezas

- **Formato do importador do Xray.** Não validei o CSV contra um Xray real. Cloud e Server/DC diferem; usei um passo único por teste (passos numerados dentro da célula) para evitar a convenção de várias linhas por teste, que não confirmei. Priority em High/Medium (nomes padrão do Jira); Labels separadas por espaço; pré-condição dentro de Description. A resposta avisa para testar com 2 ou 3 linhas.
- **Semântica do "limite diário".** A regra do usuário é ambígua em quatro pontos, tratados como suposições declaradas e marcadas "depende de Pn": contador por janela contra contador único (P1), janela noturna contínua atravessando a meia-noite (P1), instante de referência (P2) e fuso do cliente (P3). A escolha mais arriscada é a suposição de janelas independentes (CT-PIX-034 e 035) e a de noturno contínuo (CT-PIX-032).
- **Inclusivo ou exclusivo.** Assumi limites inclusivos (R$ 5.000,00 aceito), apoiado no exemplo de `dominios.md` ("aceita até 5.000,00 exatos; recusa 5.000,01"); não está dito na regra do usuário.
- **Texto das mensagens e códigos HTTP.** Não há contrato; os esperados dizem "mensagem de limite que cita R$ X" e "4xx (400 ou 422)". Na resposta peço o texto literal (P4).
- **Contexto de execução.** Os passos assumem app com Pix > Transferir, autenticação no app, API de transferência com chave de idempotência, extrato e consulta de acumulado. Nada disso foi informado; é inferência do domínio. Pode não bater com o produto real.
- **Regulamentação.** Os números vêm da regra do usuário. `dominios.md` cita o limite noturno padrão e a regra de dispositivo novo (R$ 200 por transação e R$ 1.000 por dia), mas manda confirmar na norma vigente. Não conferi (sem rede) e a resposta diz isso. A regra de dispositivo novo ficou como fora de escopo, e as pré-condições exigem dispositivo cadastrado para não contaminar os limites.
- **Quantidade e prioridade.** 43 casos (28 Alta, 15 Média, 10 smoke). Priorizei por risco, mas o domínio é dinheiro e a maioria saiu Alta; a resposta indica quais cortar primeiro. Não executei nenhum caso (não há sistema), e a resposta não afirma ter executado.
- **Contas.** Os saldos e acumulados esperados foram conferidos com `Decimal` em um script de verificação rápido (não salvo na pasta).
