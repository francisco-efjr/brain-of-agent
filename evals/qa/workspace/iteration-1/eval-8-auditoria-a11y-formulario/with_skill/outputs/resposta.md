**Não está pronto para lançar.** Testando só com o teclado, o formulário já impede um cadastro completo: o botão "Enviar" não recebe foco e Enter nos campos não envia. Encontrei 13 problemas, 7 deles em critérios de nível A da WCAG, o piso da norma. Sem corrigir pelo menos os 5 bloqueadores abaixo, pessoas que usam teclado, leitor de tela, comando por voz ou ampliação não conseguem se cadastrar com autonomia. Isso pesa num programa de benefícios.

Alvo que usei: **WCAG 2.2 nível AA**, que é a base técnica do art. 63 da LBI (Lei 13.146/2015) para sites de órgãos de governo. A eMAG 3.1 só é obrigatória na administração federal; se o edital ou contrato da prefeitura citar eMAG ou outra norma, confirme. Isto é uma auditoria técnica: não declara conformidade jurídica.

## O que foi verificado e o que não foi

- **Executado e observado** (Chromium do painel de pré-visualização, página local, sem rede): ordem de Tab, Enter nos campos, estilos de foco, árvore de acessibilidade, rótulos, `lang`, comportamento do script de validação e da mensagem de sucesso, razão de contraste calculada por script (`contraste.py`).
- **Inferido pela leitura do código** (marcado como "inferido"): o que um leitor de tela falaria e o comportamento em celular.
- **Não executado:** axe-core (o ambiente não tinha Playwright nem rede), NVDA, JAWS, VoiceOver, TalkBack, zoom de 200% e 400%, reflow em 320 px, espaçamento de texto (1.4.12) e teste com pessoas do público.
- Estimativa, não medida: o axe provavelmente pegaria só 4 destes problemas (`html-has-lang`, `image-alt`, `color-contrast` e o checkbox sem rótulo). O resto exige teclado e leitor de tela. Por isso, axe zerado depois da correção não bastaria para aprovar.

## Bloqueadores (impedem concluir o cadastro)

**1. O botão "Enviar" é um `<div onclick>`. Critérios 2.1.1 e 4.1.2 (A).**
- Observado: com 9 Tabs seguidos, o foco passou por CPF, nascimento, e-mail, senha, termos e o link "termos", e nunca parou no "Enviar". Na árvore de acessibilidade ele aparece como "generic", não "button". Depois do link "termos", o Tab volta ao início da página. Digitei um CPF e apertei Enter no campo: zero eventos `submit`, nada acontece.
- Quem é afetado: quem usa só teclado, leitor de tela e controle por voz. Não há contorno.
- Esperado: "Enviar cadastro, botão", alcançável por Tab, ativado por Enter e Espaço.
- Correção: `<button type="submit">Enviar cadastro</button>` e tratar o evento `submit` do formulário, não o clique.

**2. Os campos não têm rótulo, só placeholder. Critérios 1.3.1, 3.3.2 e 4.1.2 (A).**
- Observado: 6 controles e 0 `<label>`. O checkbox "Li e aceito os termos" tem nome acessível "on" na árvore de acessibilidade, e o texto ao lado não está dentro de um label, então clicar nele não marca a caixa.
- Efeito: o placeholder some ao digitar, e quem tem memória curta ou baixa visão perde a referência do que o campo pede. Inferido: um leitor de tela anunciaria só "on, caixa de seleção" para aceitar os termos.
- Correção: `<label for>` visível em cada campo, e `<label>` envolvendo o checkbox e o texto dos termos. A versão corrigida está anexa.

**3. O contorno de foco foi removido. Critério 2.4.7 (AA).**
- Observado: `input:focus { outline: none }` sem substituto. No Tab, os 5 campos e o checkbox ficaram sem indicação de foco; só o link "termos" mostra contorno.
- Efeito: quem navega por teclado não sabe onde está.
- Correção: `:focus-visible { outline: 3px solid #005fcc; outline-offset: 2px }`. O contorno tem 5,98:1 sobre branco, acima do mínimo de 3:1.

**4. O erro só existe para o CPF e só como borda vermelha. Critérios 1.4.1, 3.3.1 (A) e 3.3.3 (AA).**
- Observado: sem texto de erro, sem `aria-invalid`, sem mover o foco, sem anúncio. A borda tem 1 px e nunca sai depois que o CPF é corrigido (testei: continua `erro` com CPF de 11 dígitos).
- Efeito: quem não distingue o vermelho ou usa leitor de tela não sabe que houve erro nem onde.
- Correção: mensagem de texto que diz como corrigir, ligada ao campo por `aria-describedby`, `aria-invalid="true"`, resumo de erros com links e foco no resumo. Os erros devem sumir quando o campo for corrigido.

**5. A confirmação "Cadastro realizado!" some em 2 s e não é anunciada. Critérios 2.2.1 (A) e 4.1.3 (AA).**
- Observado: o `#msg` não tem `role="status"` nem `aria-live`; o `setTimeout` limpa o texto em 2 segundos.
- Efeito: quem lê devagar, usa ampliador ou leitor de tela não fica sabendo se o cadastro foi feito, e provavelmente vai reenviar ou ligar para a prefeitura.
- Correção: região `role="status"` presente (vazia) desde o carregamento, mensagem que permanece, foco nela e, em produção, número de protocolo.

## Demais achados

| # | Sev. | Problema | Critério | Correção |
| --- | --- | --- | --- | --- |
| 6 | Alta | Contraste: texto `#999` sobre branco é 2,85:1; ajuda da senha `#bbb` é 1,92:1; "Enviar" branco sobre `#6cf` é 1,80:1; borda dos campos `#ddd` é 1,36:1. Mínimos: 4,5:1 para texto e 3:1 para borda | 1.4.3 (AA), 1.4.11 (AA) | texto `#1f1f1f`, ajuda `#595959` (7,0:1), borda `#767676` (4,54:1), botão branco sobre `#00539b` (7,75:1) |
| 7 | Alta | `<html>` sem `lang` (verificado: vazio). Leitor de tela pode ler o português com a pronúncia errada | 3.1.1 (A) | `<html lang="pt-BR">` |
| 8 | Alta | Logo sem `alt`. Além disso, `logo-prefeitura.png` não existe na pasta recebida | 1.1.1 (A) | `alt` com o nome oficial do município |
| 9 | Média | Sem `autocomplete` em nome, nascimento, e-mail e senha (verificado: nenhum). E-mail é `type="text"` | 1.3.5 (AA) | `name`, `bday`, `email`, `new-password`, e `type="email"` |
| 10 | Média | Instruções ausentes ou ambíguas: o formato de data não é informado; "A senha deve ter 8 caracteres" não diz se é mínimo ou exato e não está ligada ao campo; não há marcação de obrigatórios. Inferido: `maxlength="11"` corta CPF colado com pontos e traço ("123.456.789-09" vira "123.456.789"), e o erro não explica por quê | 3.3.2 (A), 1.3.1 (A) | dica visível ligada por `aria-describedby`, aceitar CPF com ou sem máscara e normalizar no envio |
| 11 | Média | Sem `<main>` nem `<h1>` (o título é um `h3`), e o título da aba é só "Cadastro". Não reprova um critério com certeza; é prática recomendada (o axe trata como `best-practice`) e atrapalha quem navega por títulos e marcos | 1.3.1, 2.4.6, 2.4.2 (limite) | `main`, `h1`, título descritivo |
| 12 | Média | Sem `<meta name="viewport">` e fonte de 13 px (ajuda 11 px). Inferido: no celular a página aparece miniaturizada. Alvos de 29 px nos campos e 31 px no botão passam o mínimo de 24 px do 2.5.8, mas ficam pequenos para o público idoso (referência: 44 px; corpo de 16 px) | boa prática; relacionado a 1.4.4 e 1.4.10; 2.5.8 passa | viewport sem `user-scalable=no`, 16 px, alvos de 44 px |
| 13 | Média | O link "termos" aponta para `#` (leva ao topo da página). Mais que acessibilidade, é problema de conteúdo e de negócio: a pessoa aceita um texto que não existe | 2.4.4 (no limite) | link com texto "termos de uso" e destino real |

O que **não** reprovou: contraste da mensagem verde (5,14:1), do link (9,4:1) e do placeholder na cor padrão (4,61:1, `#757575` medido no navegador).

## Fora da acessibilidade, mas bloqueia o lançamento

Verificado rodando o script do arquivo: o cadastro aparece como "realizado" com CPF `aaaaaaaaaaa` e com `12345678901` (dígitos verificadores inválidos). Também aparece com nome, e-mail e senha vazios e termos desmarcados, porque só o tamanho do CPF é validado. Nada é enviado (sem `action`, sem `fetch`, sem `name` nos campos). Presumo que seja protótipo. Se for o código final, isso vem antes de qualquer acabamento.

## O que entreguei

- `cadastro-corrigido.html`: versão que corrige os pontos 1 a 12 (rótulos, botão real, foco visível, erros em texto com resumo, status persistente, contraste, `lang`, `autocomplete`, validação de CPF por dígito verificador e de data). Rodei no Chromium do painel:
  - envio vazio gera 6 erros, o resumo recebe o foco e cada campo fica com `aria-invalid`;
  - `aaaaaaaaaaa` e `12345678901` são recusados e `123.456.789-09` é aceito;
  - `31/02/2000` e `25/12/2999` são recusados;
  - a mensagem de sucesso não some após 2,5 s;
  - Tab mostra contorno de 3 px azul;
  - Enter no campo envia;
  - sem ids duplicados e com `aria-describedby` resolvendo.
  Não foi testada com leitor de tela real nem em 320 px. O ponto 13 e o `alt` do logo ficaram como `TROCAR` no HTML, porque dependem de dado da prefeitura (nome oficial e endereço dos termos).
- `contraste.py`: calcula os contrastes do original e do corrigido (executado; 4 falhas no original, 0 no corrigido).
- `acessibilidade.spec.ts`: regressão em Playwright + axe (varredura inicial e em estado de erro, teclado, foco, status, 320 px). **Não executado**: adapte seletores e versão do Playwright (precisa de 1.45 ou mais).

## Risco que sobra e próximos passos

1. Passar o `cadastro-corrigido.html` por NVDA + Firefox (ou Chrome) e por VoiceOver no iPhone, nas tarefas "preencher com erro" e "concluir o cadastro". Teste também zoom de 200%, largura de 320 px e TalkBack no Android, porque o público de benefício social costuma usar celular.
2. Se possível, observar 3 a 5 pessoas do público real (incluindo idosos) fazendo o cadastro.
3. Rodar o spec no pipeline e acrescentar as demais telas do fluxo (login, recuperação de senha, consulta de protocolo). Eu auditei só esta tela, e o login precisa atender também ao 3.3.8 (autenticação acessível).

## Suposições e perguntas que mudariam o resultado

- Supus que **todos os campos são obrigatórios** e que "8 caracteres" significa **no mínimo 8**. Confirme com o PO.
- Há norma citada em edital ou contrato (eMAG, NBR 17060 se houver app)? Isso muda o alvo.
- Este HTML é o definitivo ou um protótipo de um componente do framework? Se for protótipo, os achados 1 a 5 devem virar critérios de aceite do componente.
- Os termos de uso e a finalidade do tratamento de CPF e data de nascimento (LGPD) já existem? O link atual não leva a nada.
