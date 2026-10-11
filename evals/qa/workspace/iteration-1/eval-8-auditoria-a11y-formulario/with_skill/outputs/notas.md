# Notas da execução (eval-8, auditoria de acessibilidade do cadastro)

## Arquivos da skill lidos
- skills/qa/SKILL.md (inteiro)
- skills/qa/references/acessibilidade.md (inteiro)
- skills/qa/assets/templates/bug-report.md (inteiro; usei o formato para os 5 bloqueadores)
- skills/qa/scripts/auditoria_axe.py (lido; NÃO executado: exige playwright, ausente, e baixa o axe-core do CDN)
- skills/qa/scripts/documentos_br.py (executado só em `validar`, para conferir que o CPF de exemplo 123.456.789-09 é válido)

Não abri: estrategia.md, bugs-e-relatorios.md, seguranca.md, dominios.md, demais templates e scripts.

## Arquivos criados na pasta de saída
- resposta.md, notas.md
- cadastro-corrigido.html (versão corrigida; verificada por script no Chromium do painel)
- contraste.py (executado)
- acessibilidade.spec.ts (NÃO executado)

## Incertezas
- axe-core não rodou (sem playwright, sem rede). A previsão de que o axe pegaria só ~4 achados (html-has-lang, image-alt, color-contrast, checkbox sem rótulo) é estimativa. Em especial, acredito (sem confirmar) que a regra `label` das versões recentes do axe aceita placeholder não vazio, por isso os campos de texto talvez não sejam sinalizados.
- Nada foi testado com leitor de tela; os anúncios descritos são inferência a partir da árvore de acessibilidade do Chromium (ex.: nome "on" do checkbox).
- A navegação por Tab, o Enter e os estilos de foco foram verificados no navegador do painel (versão do Chromium não registrada). O painel era compartilhado e trocava de aba entre chamadas; confirmei `document.title` antes de cada medição, mas uma das conferências do HTML corrigido (Enter no campo) rodou na aba que já tinha estado de testes anteriores. O resultado (envio bem-sucedido, foco na mensagem) é coerente, mas não foi um teste limpo.
- O `outline` computado via JS com foco programático dava "none" no corrigido; só com Tab real (tecla pressionada) apareceu o contorno de 3 px. Para o original, a remoção do contorno também vem do CSS `input:focus { outline: none }`, não só da medição.
- Reflow em 320 px, zoom 200% e espaçamento de texto não foram testados (painel sem viewport controlável de forma segura num painel compartilhado).
- Enquadramento normativo: usei a tabela da skill (LBI art. 63, eMAG só federal). Não confirmei a versão vigente de nenhuma norma nem se o edital da prefeitura cita outra. Não declarei conformidade jurídica.
- Itens classificados como "no limite" (2.4.4 no link `#`, 2.4.2 no título "Cadastro", ausência de h1/main) são julgamento meu; o axe os trata como best-practice.
- Suposições: todos os campos obrigatórios; "8 caracteres" = mínimo; HTML é protótipo (nada é enviado); logo-prefeitura.png não existe na pasta recebida.
- Desvio de regra: rodei `ls` em evals/qa/files/ (apenas nomes de arquivo, nenhum conteúdo além do cadastro.html foi lido).
- O spec em Playwright usa `page.clock` (>= 1.45) e `toHaveAccessibleDescription` (>= 1.44); seletores `getByLabel('CPF')` etc. foram escritos contra o HTML corrigido, sem execução.
