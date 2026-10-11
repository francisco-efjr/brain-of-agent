# Notas e incertezas

Auditoria feita só com conhecimento próprio, sem usar a skill nem consultar a pasta evals (exceto `cadastro.html`).

## O que verifiquei de fato
- Contrastes calculados com script Python (fórmula WCAG de luminância relativa): #999/#fff = 2,85; #bbb/#fff = 1,92; #fff/#6cf = 1,80; #ddd/#fff = 1,36; vermelho/branco = 4,00; verde/branco = 5,14. Valores propostos também calculados.
- `cadastro-corrigido.html` foi aberto no painel do navegador (arquivo local): árvore de acessibilidade mostra labels, landmarks e botão corretos. Envio vazio gera 6 erros, foco vai ao resumo e sucesso foi exibido com dados válidos.
- Função `cpfValido` testada em Node com 6 casos.
- O logo `logo-prefeitura.png` não existe na pasta `evals/qa/files`. Não sei se existe no projeto real; mencionei só o `alt`.

## O que NÃO verifiquei (incertezas)
- Nenhum leitor de tela real (NVDA, JAWS, VoiceOver, TalkBack). Comportamentos como duplo anúncio ao mover o foco para `role="alert"` e `role="status"` são previsões baseadas em padrões conhecidos (por exemplo, o resumo de erros do GOV.UK), não testes meus.
- Nada de zoom 400%, celular real, modo de alto contraste do Windows (`forced-colors`) nem axe/Lighthouse (não instalei pacotes). A afirmação "borda mantém o botão visível em alto contraste" é teoria.
- Não sei qual referência o contrato exige. Citei a LBI art. 63 de memória; eMAG é obrigatório para o governo federal e para municípios depende de norma local. Não tenho certeza de qual versão das WCAG a NBR 17060 adota. Por isso usei WCAG 2.2 AA como régua e pedi confirmação ao jurídico/edital.
- Alguns critérios são discutíveis:
  - 2.2.1 (a mensagem de 2 s é uma "limitação de tempo"?) é interpretável, mas o problema prático existe de qualquer forma.
  - 2.5.8 (tamanho de alvo) tem exceções de espaçamento; no código original o checkbox de 13px talvez passasse por espaçamento, mas a falta de label já o torna um alvo ruim.
  - 1.4.4 com fonte em px não é falha formal, pois o zoom do navegador funciona; tratei como boa prática.
- Classifiquei CPF `maxlength` + máscara como bug funcional/usabilidade, não como falha WCAG.

## Escolhas de design no arquivo corrigido que podem ser discutidas
- `type="date"` para nascimento: simples e validado pelo navegador, mas a experiência varia entre navegadores e leitores de tela. A alternativa é campo de texto com dica dd/mm/aaaa e `inputmode="numeric"`. Deixei `type="date"` e pedi decisão. O `autocomplete="bday"` em campo de texto também varia entre navegadores.
- "Nome completo" só exige não vazio (não obriga sobrenome), para não excluir pessoas com nome único.
- Validação só no envio (não no `blur`), para não interromper quem digita.
- Regra da senha assumida como "mínimo de 8". O original era ambíguo. Não adicionei exigência de complexidade.
- Após sucesso o formulário não é limpo nem bloqueado. Com back-end real, o ideal é redirecionar para uma página de confirmação ou desabilitar o reenvio.
- CPF validado também com dígitos verificadores no cliente. A validação no servidor continua obrigatória.
- Adicionei "Mostrar senha" (extra, não exigido por WCAG); pode ser removido.
- O link dos termos aponta para `termos.html`, um placeholder que não existe.
- Não avaliei LGPD a fundo, só sinalizei.
