# Bugs, evidência e relatórios

Como registrar, reduzir, classificar, triar, verificar e analisar defeitos; como registrar evidência do que foi testado; como relatar o resultado a quem decide. Base: `bugs-e-relatorios.md` do brain-of-agent (MIT, conteúdo próprio, condensado) cruzado com V-27 (Mozilla), V-39, V-34, V-40, V-28, V-07, V-06 (ver `fontes.md`). Rótulo geral: conhecimento próprio Inferido; leis e artigos citados do brain (CDC, LGPD) são pontos de partida, confirme com o jurídico. Validado em 2026-10-10.

## Sumário

- [Anatomia de um bug report](#anatomia-de-um-bug-report)
- [Título e redução ao mínimo](#título-e-redução-ao-mínimo)
- [Evidências e dados pessoais](#evidências-e-dados-pessoais)
- [Severidade e prioridade](#severidade-e-prioridade)
- [Triagem](#triagem)
- [Ciclo de vida e verificação da correção](#ciclo-de-vida-e-verificação-da-correção)
- [Causa raiz e escape analysis](#causa-raiz-e-escape-analysis)
- [Comunicação e bug advocacy](#comunicação-e-bug-advocacy)
- [Relatório de teste](#relatório-de-teste)
- [Defeito em produção](#defeito-em-produção)
- [Evidência do que foi testado: TESTING.md](#evidência-do-que-foi-testado)
- [Protocolo de feature list para execução longa](#protocolo-de-feature-list)
- [Diagnóstico em 6 fases](#diagnóstico-em-6-fases)

## Anatomia de um bug report

Um bug report é bom quando **quem não estava presente reproduz, entende o impacto e decide sem perguntar nada**. Cada pergunta de volta custa horas ou dias. A Mozilla (V-27) pede: resumo curto e único sem a solução; passos numerados e precisos com frequência; esperado separado do obtido; observação separada de palpite; um bug por relatório; pesquisar duplicata; testar build mais novo; caso mínimo; janela de regressão.

| Campo | Por que existe | Armadilha |
| --- | --- | --- |
| Título | aparece na lista, na triagem e na busca de duplicados | descrever a causa suposta ("NullPointer no CupomService") em vez do sintoma |
| Ambiente e versão | o defeito pode existir só em um build, navegador, dispositivo | "última versão"; informe build, commit ou release |
| Pré-condições | estado antes do passo 1: perfil, dados, flag | omitir o que você já tinha configurado |
| Passos | caminho mínimo e numerado | 15 passos, 10 irrelevantes |
| Esperado | define o oráculo: por que isso é defeito | "deveria funcionar", ou valor copiado da tela; cite a regra, o cálculo, a fonte |
| Obtido | o que aconteceu, com valores | "deu erro" sem mensagem, código ou valor |
| Frequência | separa determinístico de intermitente | "às vezes" sem número |
| Evidência | prova e atalho para o diagnóstico | vídeo de 5 minutos; print sem destaque; dado pessoal exposto |
| Impacto | traduz para quem prioriza | deixar o PO deduzir |
| Severidade e prioridade sugeridas | ponto de partida da triagem | inflar para chamar atenção |
| Adicionais | contorno, primeira versão afetada, bugs relacionados, hipótese | misturar hipótese com fato; rotule a hipótese (Suposição) |

O mesmo defeito, ruim e bom (dados fictícios):

| Campo | Ruim | Bom |
| --- | --- | --- |
| Título | Erro no cupom | Checkout: total ignora cupom quando o frete é grátis |
| Ambiente | homolog | Homologação, build 3.8.0-rc2 (commit `3f9c1a2`), Chrome 141, Windows 11 |
| Pré-condições | — | usuário `cliente.qa01@exemplo.test`; cupom `PRIMEIRA10` (10%, válido até 31/12/2026); frete grátis a partir de R$ 199,00 |
| Passos | Coloquei uns produtos, apliquei o cupom e o valor ficou errado | 1. Adicionar "Fone XZ" (R$ 250,00). 2. Ir ao checkout com CEP 01310-100. 3. Aplicar `PRIMEIRA10`. |
| Esperado | O valor certo | Total R$ 225,00 = R$ 250,00 − 10% (R$ 25,00) + frete R$ 0,00 (regra RN-12, história CHK-431) |
| Obtido | Valor errado | Total R$ 250,00; o resumo lista "Cupom −R$ 25,00", mas não subtrai |
| Frequência | — | 5 de 5 com subtotal ≥ R$ 199,00; 0 de 5 com R$ 150,00 |
| Evidência | print da tela inteira | print com o total destacado; resposta de `POST /api/checkout/totais` (request id `req-7f3a91`) com `desconto: 25.00` e `total: 250.00` |
| Impacto | — | cliente paga R$ 25,00 a mais em todo pedido com cupom e frete grátis; possível devolução em dobro (CDC art. 42, parágrafo único: Inferido, confirme) |
| Sev./Prior. | URGENTE!!! | Severidade Crítica (valor cobrado errado, sem contorno); prioridade sugerida P1 (campanha em 10/10) |

O bom é **reproduzível** (dados concretos), **verificável** (esperado vindo de regra) e **decidível** (impacto em reais e clientes). Template: `assets/templates/bug-report.md`. **Não preencha o que não foi informado**: marque "Não informado" e pergunte só o que muda a decisão; nunca invente passos, versões, horários nem IDs.

## Título e redução ao mínimo

**Título = onde + o que acontece + em que condição**, com os termos que alguém usaria para buscar duplicados; verbo observável ("ignora", "duplica", "retorna 500"); sintoma no título e hipótese no corpo; até ~100 caracteres. Evite "Bug no login", "Tela quebrada", "Erro 500", "Não funciona no iPhone"; prefira "Login: conta bloqueada após 3 tentativas mesmo com a senha correta na 3ª" ou "Cadastro (iOS 18, Safari): botão 'Continuar' não responde com o teclado aberto".

**Reduza até o mínimo:**

1. **Corte passos**, um por vez, e veja se o defeito continua.
2. **Isole a variável**: mude uma condição por vez e registre. A coluna "reproduz?" é o dado mais útil para o dev:

   | Variação | Reproduz? |
   | --- | --- |
   | Subtotal R$ 250,00, frete grátis | sim (5/5) |
   | Subtotal R$ 150,00, frete pago | não (0/5) |
   | Subtotal exato R$ 199,00 (limite) | sim (3/3) |
   | Cupom de valor fixo (`MENOS20`) | não |
   | Firefox e app Android | sim: não depende do cliente |

3. **Desça de camada**: se passa pela API, reproduza com `curl` e tire a interface da equação:

   ```bash
   curl -s -X POST "$BASE_URL/api/checkout/totais" \
     -H "Authorization: Bearer $TOKEN_QA" -H "Content-Type: application/json" \
     -d '{"itens":[{"sku":"FONE-XZ","qtd":1}],"cep":"01310-100","cupom":"PRIMEIRA10"}'
   ```

   Contra servidor de dev ou staging, com token de teste vindo de variável de ambiente; nunca produção sem autorização.
4. **Ache o commit com `git bisect`** quando há versão boa e ruim. Salvaguardas (V-34, brain): exige **árvore limpa**, **muda o checkout** (confirme com o usuário antes), deixe o teste reprodutor **sem commit** (arquivos não rastreados sobrevivem), restaure no fim:

   ```bash
   git bisect start && git bisect bad && git bisect good v3.7.0
   git bisect run sh -c 'npm ci --silent || exit 125; npx vitest run cupom-frete'
   git bisect reset
   ```

   Código de saída do `run`: 0 = bom, 125 = não testável (pula), 1 a 127 = ruim.

**Intermitente não é "não reproduz"**: é frequência menor que 100%, e frequência é dado. Registre a frequência medida ("3 de 20"), condições de cada ocorrência (horário em UTC, usuário, dados, instância, carga, rede, outra aba), timestamp e correlation/request id de cada falha, o que as falhas têm em comum e as passagens não, e hipóteses por categoria (tempo, concorrência, dados, ambiente, ordem). Skill: `flaky-triage`.

## Evidências e dados pessoais

| Evidência | Use quando | Como fazer bem |
| --- | --- | --- |
| Print anotado | defeito visual ou valor errado | destaque a área, mostre URL e horário, corte o resto |
| Vídeo curto | sequência, animação, timing | até ~1 min, começando perto do defeito; diga o segundo |
| Console do navegador | tela quebra ou não reage | copie o erro com stack trace como texto |
| HAR | requisição errada, lentidão | grave só a sessão do defeito; revise antes de anexar |
| Logs do servidor | 5xx, processamento assíncrono | trecho com timestamp e correlation id, não o arquivo |
| Request id / trace id | todo defeito que passa pelo servidor | o elo mais barato entre relato e log |
| Trace do Playwright | falha de teste automatizado | anexe o `trace.zip` (ações, DOM, rede, console), após revisar |
| Registro afetado | dado gravado errado | ID e a consulta usada para conferir |

**Dado pessoal em evidência é tratamento de dado pessoal** (LGPD; princípio da necessidade, art. 6º III: Inferido, confirme). Use usuários e dados de teste; mascare CPF (`***.456.789-**`), e-mail, telefone, endereço, nome; nunca exponha cartão completo, senha, token ou cookie de sessão (`<REDACTED>`). HAR e trace contêm cabeçalhos, cookies e corpos de requisição: revise antes de anexar (versões recentes do Chrome exportam HAR "sanitized" por padrão, mas corpos e URLs continuam: Inferido). Em automação, mascare na origem (`screenshot` com máscara sobre o campo). Defeito de produção com dado real: referencie o ID do registro, não copie o dado; se o anexo for indispensável, área restrita e apagar após a correção.

## Severidade e prioridade

Severidade mede o **estrago**; prioridade mede a **urgência**. QA propõe a severidade (técnica); o PO decide a prioridade (negócio), com o dev informando custo e risco.

| Severidade | Critério objetivo (basta um) | Exemplos |
| --- | --- | --- |
| Bloqueador | impede usar ou testar um fluxo principal inteiro, sem contorno; ou impede a release | login falha para todos; checkout retorna 500 em qualquer pedido |
| Crítica | dinheiro errado; perda ou corrupção de dados; falha de segurança explorável; violação legal; função principal quebrada para um grupo sem contorno | cobrança em duplicidade; usuário vê pedido de outro (IDOR); "Pagar" inacessível por teclado e leitor de tela |
| Alta | função importante errada com contorno difícil ou caro; regra violada sem perda direta | upload falha acima de 2 MB (contorno: comprimir); filtro ignora a categoria |
| Média | função secundária errada, ou principal com contorno simples; mensagem confusa | ordenação errada a partir da 2ª página; erro sem dizer qual campo |
| Baixa | cosmético ou de texto, sem efeito na decisão do usuário | ícone desalinhado |

Prioridade: **P1** corrigir agora (hotfix; muitos usuários, dinheiro ou dados, prazo legal); **P2** antes da release ou nesta sprint; **P3** backlog; **P4** se sobrar tempo (candidato a risco aceito). Divergem de propósito: alta severidade com baixa prioridade (fechamento anual trava acima de 50 mil linhas, próximo uso em março, CSV serve de contorno); baixa severidade com alta prioridade (nome do parceiro errado no banner no dia do lançamento da parceria). Corrija quando vir: tudo crítico (peça o critério da tabela); severidade pelo cargo de quem reportou ("o diretor viu" muda a prioridade, não a severidade); severidade rebaixada porque o conserto é difícil (custo afeta prioridade, nunca severidade); ênfase ("urgente!!!") não é critério; campo único "criticidade" que esconde as duas dimensões.

## Triagem

Objetivo: sair de cada defeito novo com **decisão, dono e prazo**. Quem: QA (fato e impacto), dev da área (custo, risco, causa provável), PO (prioridade); em produção, suporte ou SRE. Cadência: diária de 15 min na reta final; fora disso, assíncrona com prazo (ex.: bug novo triado em 1 dia útil). Perguntas, em ordem: é defeito (diverge de requisito, regra, lei ou expectativa razoável)? reproduz, com que frequência? já existe? qual o impacto real? severidade e prioridade? quem corrige e até quando? que teste de regressão nasce daqui?

| Resolução | Legítima quando | Resposta sem atrito | Depois |
| --- | --- | --- | --- |
| Não é bug | ambiente fora do ar, massa errada, engano de quem testou | "Era a massa do ambiente; anotei no guia para não repetir." | se confundiu quem testa, pode confundir o usuário |
| Funciona como projetado | segue regra explícita e aceita | "Confere com a RN-12. Se o efeito para o cliente não for o desejado, abro como melhoria." | regra que produz resultado ruim é defeito de requisito |
| Duplicado | mesma causa e sintoma de bug aberto | "Duplicado do CHK-512; levei evidência nova para lá." | sintoma igual não prova causa igual: se as condições diferem, mantenha e vincule |
| Não reproduz | após tentativa honesta com mesmos dados, versão, ambiente | "Podemos reproduzir juntos 15 min? Mando o HAR e o horário das falhas." | nunca feche se há ocorrências no log de produção |
| Adiado / não corrigir | impacto baixo ou custo desproporcional, decidido pelo dono do risco | "Registro como risco aceito por [nome], revisão em [data]." | continua visível como risco conhecido |

QA não "ganha" a triagem: se o defeito foi adiado e o risco ficou registrado com dono e data, o trabalho foi bem feito.

## Ciclo de vida e verificação da correção

Novo → Triado → Em correção → Corrigido → Em verificação → Fechado; Reaberto (verificação falhou); Adiado (risco aceito, com data); Rejeitado (não é bug, duplicado, não reproduz, como projetado). Os nomes variam; o essencial é existir um estado entre "corrigido" e "fechado": o dev marca corrigido, **quem verifica fecha**.

Verificação: (1) **confirme o build** (hash ou versão exposta; muitas reaberturas falsas nascem aqui); (2) repita os passos originais com os mesmos dados e as variações da tabela, inclusive as que não reproduziam; (3) regressão ao redor (o que mais usa o código: percentual e fixo, com e sem frete grátis, 198,99 / 199,00 / 199,01, cupom expirado, dois cupons, sem cupom); (4) **automatize** no nível mais barato um teste que falharia sem a correção e rode-o contra o código antigo. **Reabrir ou abrir novo?** Reabra quando o mesmo sintoma persiste nas mesmas condições (informe a versão testada e a evidência nova); abra novo, vinculado, quando a correção resolveu o original mas causou outro efeito ou o sintoma ocorre em outra condição. Reabertura alta indica correção sem teste ou definição de pronto fraca: sinal de processo, não de pessoa.

## Causa raiz e escape analysis

Faça para defeitos críticos, escapes e padrões repetidos, não para todo bug. O produto é **uma ação com dono e prazo que impede a classe de defeito**.

**5 porquês** (caso do cupom): o total ignorou o cupom porque, com frete grátis, o serviço de frete recalcula a partir do subtotal bruto → a regra fica no serviço de frete, que não recebe os descontos → o contrato carrinho→frete não tem campo de desconto e ninguém o revisou → nenhum teste pegou porque testes de cupom usam frete pago e os de frete grátis não têm cupom (a combinação não estava na tabela de decisão) → o refinamento não incluiu o time de frete nem QA. Ações: tabela de decisão cupom × frete na história e nos unitários (QA e dev, esta sprint); teste de contrato carrinho→frete com desconto (dev do frete, próxima sprint); dono de cada serviço tocado no refinamento (PO). Armadilhas: parar em "o dev errou"; seguir uma só cadeia quando há várias causas; preencher porquê com palpite em vez de evidência. **Ishikawa** quando há muitas causas candidatas: pessoas, processo, ferramentas, requisitos, ambiente, dados.

| Origem | Sinal típico | Prevenção que funciona |
| --- | --- | --- |
| Requisito | regra ambígua, ausente ou contraditória | exemplos concretos no refinamento, critérios de aceite com dados |
| Design | a solução não comporta o caso | revisão de design com casos de borda |
| Código | lógica, limite, nulo, tipo, concorrência | unitário, revisão, análise estática |
| Ambiente | só acontece em um ambiente | paridade entre ambientes, infra como código |
| Dados | registro legado, migração, massa inexistente em teste | teste de migração, dados realistas anonimizados |
| Configuração | flag, variável, permissão errada | config versionada e validada na subida |
| Integração | contrato divergente com terceiro | teste de contrato, virtualização fiel, monitoramento |

Registre também **em que fase o defeito entrou** e **em que fase foi achado**: a distância é o custo.

| Por que escapou | Ação concreta |
| --- | --- |
| Não havia teste para esse risco | adicionar o caso e revisar a análise de risco da área |
| Havia teste, com dado ou ambiente diferente | incluir o dado que dispara; reduzir a diferença de ambiente |
| Havia teste, mas a asserção não verificava o efeito | fortalecer a asserção (valor, não só 200) e procurar o padrão em outros testes |
| O teste falhou e foi ignorado (flaky, quarentena) | corrigir o teste; rever a política de quarentena |
| Só aparece com volume, concorrência ou tempo de produção | teste de carga ou concorrência direcionado; alerta |
| Quem detectou foi o cliente | monitoramento sintético ou alerta de métrica de negócio |
| Risco conhecido e aceito | confirmar que a aceitação foi consciente e por quem |

"Testar mais" e "ter mais atenção" não são ações. Ação tem verbo, artefato, dono e prazo: "Adicionar à suíte de contrato o caso desconto + frete grátis (Ana, até 17/10)". Acompanhe o DDP por área e período para decidir onde investir, nunca para comparar pessoas.

## Comunicação e bug advocacy

O objetivo é **levar à decisão certa**, não vencer discussão. RIMGEA (BBST Bug Advocacy, Kaner; Inferido do brain): **R**eplicate, **I**solate, **M**aximize (busque a pior consequência), **G**eneralize (onde mais aparece), **E**xternalize (impacto no mundo real) e **A**nd say it clearly and dispassionately.

| Evite | Prefira |
| --- | --- |
| "Você esqueceu de aplicar o desconto" | "O total não aplica o desconto quando o frete é grátis" |
| "Como isso passou?" | "Esse caso não estava nos critérios; sugiro incluí-lo" |
| "URGENTE!!! Tudo quebrado" | "Checkout cobra R$ 25,00 a mais em pedidos com cupom e frete grátis" |
| "Não fecho enquanto não corrigir" | "Se for adiado, registro como risco aceito por quem decidir" |

Com dev: chegue com reprodução mínima e request id, ofereça 15 min de pareamento, discuta o comportamento esperado. Com PO: fale em impacto de negócio e apresente opções com custo (corrigir agora, desligar por flag, contornar com comunicação, adiar com risco registrado). Debug de causa raiz **no código** é do plugin `code-quality-refactoring`; esta área vai até reprodução mínima, evidência, relatório, triagem e verificação.

## Relatório de teste

Existe para apoiar uma decisão (quase sempre "liberar ou não"). Ordem em que o gestor lê: (1) recomendação em uma linha; (2) riscos abertos (3 a 5) em linguagem de negócio, com a decisão que cada um pede; (3) escopo testado e **não** testado e o risco que isso deixa; (4) números (planejados, executados, aprovados, com falha, não executados; defeitos abertos por severidade); (5) tendência; (6) condições do teste (ambiente fora do ar, dados faltando); (7) decisões pedidas e próximos passos, com dono e data. Template: `relatorio-de-teste.md`.

Em vez de "92% dos casos passaram": "Compra, pagamento e cadastro passaram; as falhas restantes são de relatórios administrativos, com 2 defeitos de severidade média". Em vez de "Não deu tempo de testar o app iOS": "O app iOS não foi testado nesta versão; uma falha no checkout atingiria clientes iOS. Opções: adiar o iOS 2 dias ou liberar com smoke e monitoramento reforçado". Armadilhas: relatório melancia (verde por fora, "100% de aprovação" com 40% dos casos não executados); contar casos em vez de pesar riscos; misturar verificado com inferido; esconder bloqueios de ambiente.

Versão curta (cabe numa mensagem; dados fictícios): "Release 3.8.0, recomendação: LIBERAR COM RESSALVA. Ressalva: a correção do CHK-512 precisa estar no build final. Testado: compra, pagamento, cadastro e busca, 212 de 220 casos executados, 205 aprovados, 7 com falha. Não testado: regressão do app iOS (8 casos; dispositivo indisponível). Risco: falha no checkout iOS; mitigação: smoke no iOS após a publicação + alerta de erro. Defeitos abertos: 0 bloqueadores, 1 crítico, 3 médios, 5 baixos. Decisão pedida (PO, até 08/10): aceitar o iOS sem a regressão completa?"

## Defeito em produção

**Mitigar antes de corrigir.** (1) classificar pelo impacto (usuários, dinheiro, dados, segurança); (2) mitigar: rollback, desligar a flag, contorno operacional; (3) comunicar o status com a próxima atualização em horário marcado; (4) corrigir e verificar: hotfix de escopo mínimo, teste de confirmação, regressão focada no diff, smoke pós-deploy (hotfix que pula todos os testes é a origem do segundo incidente); (5) postmortem sem culpados em poucos dias (resumo e impacto, linha do tempo, causas contribuintes, escape analysis, o que funcionou, ações com dono e prazo; pergunte "como o sistema permitiu", não "quem errou"). Papel do QA: reproduzir fora de produção com dados no formato dos reais anonimizados; medir a extensão; definir os testes do hotfix; levar a escape analysis ao postmortem. **Todo defeito de produção vira ao menos um teste automatizado que falha sem a correção**, no nível mais barato, com o ID do incidente no nome (`test('INC-2026-031: desconto percentual com frete grátis', ...)`). Não aplique rollback, deploy ou restauração por conta própria: recomende e peça autorização.

## Evidência do que foi testado

Relatório de evidência (`TESTING.md`; V-40 sustenta a ideia de pedir ao agente que registre como testou, para o humano revisar o documento e não todo o código; os campos "comando executado", "saída" e "NÃO testado" são acréscimo deste plugin, Suposição apoiada em V-01 e V-28). Template `evidencia-de-teste.md`, a preencher à mão ou com o comando `/qa-testing:qa-evidence`:

```markdown
# Evidência de teste: <mudança>
- Escopo: <o que foi alterado>
- Comando executado: `<comando>`
- Saída relevante: <colar; truncar o resto e apontar para o log>
- Verificado: <comportamentos confirmados, por teste ou execução manual>
- NÃO testado: <lacunas, motivo>
- Riscos residuais: <...>
```

Regra: só comandos e saídas **desta sessão**; o que não foi rodado vai para "NÃO testado". A ferramenta Showboat citada por Willison (V-28) registra `note`, `image` e `exec` e desencoraja o agente de escrever o que esperava em vez do que ocorreu; o princípio vale sem a ferramenta (não validada aqui). **Saída de teste desenhada para o agente** (V-07): console com poucas linhas; `ERROR <arquivo>:<teste> - <motivo curto>` em uma linha (para `grep`); sumário final de 3 linhas (total, falhas, caminho do log); log completo em arquivo; progresso impresso raramente; opção `--fast` com amostra determinística quando a suíte é longa; verificador de testes quase perfeito, senão o agente resolve o problema errado.

## Protocolo de feature list

Para execução longa em sandbox, com revisão humana (V-06; o plugin não implementa loop autônomo, K8). Registro JSON (modelo em `assets/templates/feature-list.json`): `id`, `category`, `description`, `steps[]`, `passes` (booleano, inicia falso). Regras: altere **somente** `passes`; nunca remova nem edite passos (a fonte chama inaceitável); marque verdadeiro só após verificação ponta a ponta como usuário (navegador, não só unitário ou `curl`); uma feature por sessão. Início de sessão: `pwd`, log do git, arquivo de progresso, lista de features, `init.sh`, E2E básico de sanidade; fim: commit descritivo (com autorização do usuário) e log de progresso. Limitação a registrar: alertas nativos do navegador são invisíveis à automação com Puppeteer MCP (V-06). Detalhes: `protocolo-feature-list.md`.

## Diagnóstico em 6 fases

Para bug difícil (V-34, destilado; MIT). (1) **Loop de feedback rápido que falha**, determinístico, antes de teorizar; (2) reproduzir e minimizar; (3) 3 a 5 hipóteses falsificáveis e ranqueadas, cada uma com previsão; (4) instrumentar **uma variável por vez**, com logs de prefixo único; (5) correção e teste de regressão em um seam que exercite o padrão real do bug (se não existir, registre como achado de arquitetura); (6) limpeza (remova logs marcados, registre a hipótese correta). Redija segredos. **Salvaguardas que a fonte não traz:** confirme o ambiente-alvo antes de executar estresse, fuzz (1.000 entradas) ou `git bisect run`; nunca instrumente produção sem autorização; mutação de código para forçar falha só em cópia/árvore limpa. Escalada: após 3 hipóteses refutadas, pare, resuma o que foi descartado e peça decisão.
