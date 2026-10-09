# Frontend, estado, interação e desempenho

Aplicar em interfaces web; adaptar conceitos à plataforma nativa e consultar apple-design.md quando pertinente. Preservar stack e design system existentes antes de propor troca.

## Estado como contrato

Classificar: estado de domínio recebido do servidor, navegação (URL), rascunho do usuário, estado efêmero de interação e dados derivados. Evitar duas fontes de verdade. A URL deve representar filtros compartilháveis quando o produto pede retorno, bookmarking ou navegação; não expor dados sensíveis nela.

Descrever o componente por estados `inicial/carregando/sucesso/vazio/erro/atualizando` e transições. Erro após dados carregados não necessariamente apaga os dados; deve indicar que podem estar desatualizados. Salvar exige distinguir “enviando”, “aceito” e “resultado desconhecido”.

No React, valores deriváveis podem ser calculados durante renderização e eventos tratam ações do usuário; effects destinam-se principalmente à sincronização externa. Confirmar a versão e convenções do projeto. [Fonte: You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect).

## Concorrência na interface

Exemplo: busca por “a” inicia requisição A; busca por “ab” inicia B; B chega primeiro e A depois. Antes: última resposta recebida substitui resultado mesmo sendo de consulta antiga. Depois: associar resultado à identidade da consulta e ignorar resposta obsoleta, ou cancelar quando possível; cancelamento não garante que servidor não executou.

Mutação otimista exige: identificador temporário, rollback ou reconciliação, tratamento de conflito e mensagens compreensíveis. Não incrementar saldo financeiro no cliente e apresentá-lo como confirmado sem regra explícita. Bloquear duplo clique melhora UX, mas a garantia contra duplicação pertence também ao servidor.

## Componentes e semântica

Preferir controles nativos e semânticos. Botão executa ação; link navega. Label não pode ser substituída apenas por placeholder. Foco deve seguir uma ordem útil; modal precisa reter foco enquanto aberto, permitir saída adequada e restaurar foco. Mensagens de validação precisam identificar campo e como corrigir. Avaliar teclado, leitor de tela e ampliação em jornadas reais. WCAG 2.2 fornece critérios web, mas não comprova conformidade legal ou de software nativo. [Fonte: WCAG 2.2](https://www.w3.org/TR/WCAG22/).

## Desempenho e limites

Medir carregamento e interação em aparelho/rede representativos. Investigar bundle, imagens, fontes, hidratação, re-renderização e requisições em cascata antes de otimizar. Definir orçamento ligado à experiência e capturar antes/depois nas mesmas condições. Virtualização de listas deve preservar navegação assistiva e procura quando elas fazem parte do uso.

SSR/hidratação exigem valores iniciais consistentes: tempo, locale, armazenamento local e aleatoriedade podem produzir divergência. Nunca acessar segredo no bundle; variáveis “de ambiente” injetadas no cliente são públicas.

## Exemplo de aceitação

Lista de propostas: filtros sobrevivem a voltar/avançar; seleção não muda ao ordenar; erro de atualização preserva conteúdo anterior com aviso; teclado alcança detalhes; usuário com permissão removida recebe tratamento da resposta do servidor; resultado de consulta antiga não substitui atual.

## Checklist

- [ ] Mapear estado, fonte de verdade, URL e transições.
- [ ] Cobrir vazio, carregamento, falha, recuperação, sessão expirada e conteúdo longo.
- [ ] Proteger resposta obsoleta, duplo envio e perda de rascunho.
- [ ] Implementar semântica, foco, nomes acessíveis e feedback de operação.
- [ ] Confirmar regras no servidor; UI não é fronteira de autorização.
- [ ] Revisar componentes compartilhados e tokens antes de introduzir variação.
- [ ] Verificar responsividade, zoom, temas e preferência de movimento quando aplicável.
- [ ] Medir interação e carregamento com condições registradas.
- [ ] Revalidar contrato real e jornada após alteração de estado/endpoint.

Falhas comuns: screenshot bonita sem fluxo; toast como único registro de erro; skeleton infinito; índice de array como identidade de entidade mutável; cache de usuário anterior reaproveitado após logout.

Fontes consultadas em 2026-10-09. Exemplos são cenários próprios, não snippets universais de framework.
