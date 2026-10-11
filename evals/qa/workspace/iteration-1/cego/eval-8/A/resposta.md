## Veredito: não publique como está

O formulário tem falhas que impedem totalmente o uso por quem navega só com teclado ou usa leitor de tela. Para uma prefeitura, isso também é risco legal: a Lei Brasileira de Inclusão (Lei 13.146/2015, art. 63) exige acessibilidade nos sites de órgãos públicos. Confirme com o jurídico ou com o edital qual referência o contrato cobra (WCAG 2.2 nível AA, ABNT NBR 17060 ou eMAG). Eu usei WCAG 2.2 AA como régua.

**Como auditei:** li o código de `cadastro.html`, calculei os contrastes e testei no navegador a versão corrigida que estou entregando. **Não testei com leitor de tela real, nem em celular, nem com zoom de 200% e 400%.** Isso precisa ser feito antes do lançamento (lista no fim).

### Bloqueadores (corrigir antes de qualquer lançamento)

| # | Problema | Critério WCAG | Correção |
|---|---|---|---|
| 1 | O botão "Enviar" é uma `<div onclick>`. Não recebe foco do teclado, não é anunciado como botão e não dá para enviar sem mouse. | 2.1.1, 4.1.2 | `<button type="submit">` e tratar o evento `submit` do formulário. |
| 2 | Nenhum campo tem `<label>`; só há `placeholder`. O leitor de tela não sabe o que cada campo pede, e o texto some ao digitar. | 1.3.1, 3.3.2, 4.1.2 | `<label for="...">` visível em cada campo. |
| 3 | `input:focus { outline: none }` remove o indicador de foco, então quem usa teclado não vê onde está. | 2.4.7 | Remover a regra e definir `:focus-visible` com contorno de 3px. |
| 4 | O erro do CPF é só uma borda vermelha. Não há texto, não é anunciado, o foco não vai ao campo e a classe nunca é removida. | 1.4.1, 3.3.1, 3.3.3, 4.1.3 | Mensagem em texto ("Erro: ..."), `aria-invalid`, `aria-describedby`, resumo de erros com foco e links para os campos. |
| 5 | "Cadastro realizado!" aparece sem `role="status"` (leitor de tela não anuncia) e some sozinho em 2 segundos. | 4.1.3, 2.2.1 | Região `role="status"` com a mensagem fixa, sem `setTimeout`. |
| 6 | Contraste insuficiente (medido sobre branco): texto do corpo `#999` = **2,85:1** (mínimo 4,5); ajuda `#bbb` = **1,92:1**; botão branco sobre `#6cf` = **1,80:1**; borda dos campos `#ddd` = **1,36:1** (mínimo 3:1). | 1.4.3, 1.4.11 | Texto `#1f1f1f` (16,5:1), ajuda `#595959` (7:1), borda `#767676` (4,5:1), botão `#0b4f8a` com texto branco (8,4:1). |
| 7 | `<img>` do logo sem `alt`. | 1.1.1 | `alt="Prefeitura de [nome do município]"`. |
| 8 | `<html>` sem `lang`. O leitor de tela lê português com sotaque de inglês. | 3.1.1 | `<html lang="pt-BR">`. |

### Importantes

| # | Problema | Critério | Correção |
|---|---|---|---|
| 9 | Falta `autocomplete` e os tipos de campo estão errados: e-mail como `text`, CPF e nascimento sem teclado numérico. | 1.3.5 | `name`, `email`, `bday`, `new-password`. E-mail com `type="email"`. CPF com `inputmode="numeric"`. Nascimento com `type="date"`. |
| 10 | O texto de ajuda da senha não está ligado ao campo. "Deve ter 8 caracteres" é ambíguo: mínimo ou exatamente 8? | 1.3.1, 3.3.2 | `aria-describedby` e texto claro. Confirmar a regra com o negócio. |
| 11 | O checkbox não tem `label`. Clicar no texto não marca, o alvo é de 13px e o "termos" é um link para `#` (nada abre). | 1.3.1, 2.5.8 | `<label for="termos">`, caixa de 24px, link real para os termos. |
| 12 | Campos obrigatórios não são indicados. | 3.3.2 | "Todos os campos são obrigatórios" e atributo `required`. |
| 13 | Sem `<meta name="viewport">`: no celular a página abre em escala de desktop. | 1.4.10 | Adicionar o viewport e usar largura fluida. |
| 14 | Sem `<main>`, sem `<header>`, sem link "pular para o conteúdo" e sem `<h1>` (só `<h3>`). Título da aba genérico ("Cadastro"). | 1.3.1, 2.4.1, 2.4.2, 2.4.6 | Landmarks, `h1` e título descritivo com o nome da prefeitura. |
| 15 | Fonte de 13px e de 11px (ajuda), fixa em `px`. | 1.4.4 (boa prática) | `rem`, mínimo 16px no corpo e 15px na ajuda. |

### Bugs funcionais que apareceram na leitura (não são de acessibilidade, mas afetam o mesmo público)

- **Só o CPF é validado, e só pelo tamanho.** Um formulário vazio com 11 caracteres no CPF mostra "Cadastro realizado!".
- **`maxlength="11"` corta CPF colado com máscara.** `123.456.789-09` vira `123.456.789`, que tem 11 caracteres e **passa na validação**. O dígito verificador também não é conferido.
- Nada é enviado a lugar nenhum: `enviar()` só mostra a mensagem.
- O link dos termos não leva a nada. Como o formulário coleta CPF e data de nascimento, vale revisar com o jurídico a base legal e o aviso de privacidade (LGPD).

### O que está certo

`DOCTYPE` e `charset` presentes, uso de elementos nativos de formulário, ordem do DOM coerente com a ordem visual, e a senha não bloqueia colar nem gerenciador de senhas (bom para o critério 3.3.8).

### O que entreguei

`cadastro-corrigido.html` (na mesma pasta desta resposta) corrige todos os itens acima. Resumo do que mudou:

- Rótulos visíveis, `lang`, `viewport`, landmarks e `h1`.
- Botão nativo.
- Foco visível.
- Cores e tamanhos novos.
- Validação de todos os campos no envio, com a regra do CPF incluindo dígitos verificadores e aceitando máscara.
- Mensagens de erro em texto, resumo de erros que recebe o foco, e sucesso fixo na tela.
- Opção "Mostrar senha".

Executei o arquivo no navegador: o envio vazio lista os 6 erros e leva o foco ao resumo. Um preenchimento válido mostra o sucesso. A função de CPF aceitou `123.456.789-09` e rejeitou `111.111.111-11` e `123.456.789`.

Ficam como **TODO** no código: o nome do município no logo e no título, o link real dos termos, o envio ao back-end (hoje só mostra a mensagem) e a regra final da senha.

### Antes de lançar: testes manuais que faltam

1. **Só teclado:** Tab, Shift+Tab, Enter e Espaço. Dá para preencher e enviar sem mouse, e o foco aparece sempre?
2. **Leitor de tela:** NVDA + Firefox ou Chrome no Windows, VoiceOver no iPhone e TalkBack no Android. Os campos são anunciados com nome, obrigatoriedade e erro? O resumo de erros e o sucesso são lidos uma vez só? O ponto que mais me preocupa é um possível anúncio duplicado no sucesso, porque o foco vai para uma região `role="status"`.
3. **Zoom de 200% e 400%** (e janela de 320px): sem rolagem horizontal e sem perda de conteúdo.
4. **Celular real:** teclado numérico no CPF, seletor de data, tamanho dos alvos de toque.
5. **Ferramentas automáticas** (axe DevTools ou Lighthouse) como complemento. Elas pegam só uma parte dos problemas; o que está acima veio da leitura do código.
6. Se o público incluir pessoas idosas ou com baixa escolaridade digital, vale um teste com usuários reais, principalmente no campo de data de nascimento.

Decisões para você: a regra da senha (mínimo 8 ou exatamente 8), se o `type="date"` serve ou se prefere campo de texto com máscara dd/mm/aaaa, e se o cadastro realmente precisa de senha.
