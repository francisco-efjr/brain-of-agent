# Qualidade de produto com referência Apple

Consulta: 09/10/2026. Apple é a preferência de acabamento deste projeto,
não um ranking comprovado de todos os design systems. Adote integração,
consistência e cuidado com interação, preservando a identidade e plataforma
do produto. Não imponha migração nativa apenas para obter uma aparência.

## Fundamento confirmado e alcance

O HIG da Apple organiza orientações por plataforma e componentes. Use as
convenções do ambiente alvo para que controles familiares façam o que o usuário
espera. O princípio se aplica à seleção de componentes, sem transformar HIG
em norma universal para sistemas web.
Fonte: [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/).

No Mac, janelas ajustáveis, menus e teclado participam de tarefas de trabalho
prolongadas. Planeje comandos e contexto da janela junto à interface, em vez
de desenhar uma moldura que apenas simule o sistema.
Fonte: [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos/).

O material Liquid Glass é orientado a controles e navegação; aplicação extensa
na camada de conteúdo pode prejudicar hierarquia. Componentes do sistema
já oferecem comportamentos apropriados; efeitos personalizados pedem contenção
e legibilidade com fundos reais e preferências de acessibilidade.
Fonte: [Materials](https://developer.apple.com/design/human-interface-guidelines/materials).

As métricas e nomes de versões do arquivo de inspiração não foram confirmados
como contratos oficiais. Não copie automaticamente 13 pt, margens de 20 pt,
20×20 pt de alvo ou nomes de releases para outro projeto. Confirme SDK, versão
mínima e documentação aplicável antes de selecionar APIs e medidas.

## Critérios de engenharia definidos neste projeto

Os itens seguintes são critérios locais de revisão, não citações normativas.

1. Inventário original mapeado ao novo fluxo: nenhuma função desaparece por
   estética e propostas novas permanecem identificadas.
2. Toda ação possui comportamento, feedback, estado e recuperação definidos.
3. Tokens semânticos expressam função, variantes e consistência; cores
   literais espalhadas não são um design system.
4. Protótipo e aplicação implementada são diferenciados. Botão navegável
   não comprova salvamento, permissão ou integração.
5. Acessibilidade é comportamento verificável, não apenas acabamento.
6. Movimento explica mudança e admite interrupção e redução.
7. Tela contém dados reais/sintéticos plausíveis, extremos e falhas, sem
   usar lorem ipsum para mascarar overflow ou hierarquia.

## Transferência para web, mobile e sistemas existentes

| Intenção | macOS | Web/mobile/outra stack |
| --- | --- | --- |
| Comandos familiares | Menus, janela e teclado nativos | HTML/controles do sistema, rotas e gestos esperados |
| Hierarquia | Navegação e conteúdo distintos | Estrutura semântica e responsiva, sem obrigar moldura Mac |
| Acabamento | Materiais compatíveis com SDK | Tokens e componentes existentes; efeito não é requisito |
| Recuperação | Undo quando aplicável | Reversão/confirmar conforme operação, contrato e risco |
| Acesso assistivo | Árvore e recursos nativos | Semântica HTML e padrões ARIA quando necessários |

Na web, consulte os padrões WAI-ARIA para widgets personalizados; escolha
semântica e interação correspondentes, em vez de somente aplicar um papel.
Fonte: [W3C APG — Patterns](https://www.w3.org/WAI/ARIA/apg/patterns/).

### Exemplo: lista de clientes

Pedido: tornar a lista consistente e acessível em um sistema web existente.
Não substitua a stack por SwiftUI nem adicione botões de janela do macOS.
Inventarie busca, filtro, ordenação, seleção e ações. Implemente semântica,
estados vazio/carregando/erro, foco ao fechar diálogo e tratamento de resposta
obsoleta. Teste a jornada por teclado, viewport estreito e nomes longos.
Registre persistência e autorização na API separadamente da avaliação visual.

### Exemplo: app Mac existente

Confirme SDK e versão mínima antes de usar API nova de material. Avalie
compatibilidade e comportamento alternativo. Valide comando na janela ativa,
seleção, fechar/reabrir e redimensionamento. Não declare recurso suportado
porque o nome da API apareceu em uma geração de código.

## Matriz de componente e roteiro

| Elemento | Estados/verificações |
| --- | --- |
| Campo | Vazio, foco, preenchido, inválido, readonly, desabilitado, longo |
| Ação | Normal, foco, pressionado, processando, indisponível, erro |
| Lista | Vazia, carregando, resultados, seleção, erro, volume/paginação |
| Diálogo | Foco inicial, tabulação, validação, fechar e devolver foco |
| Navegação | Atual, teclado, back/deep link, painel e overflow quando aplicáveis |

Roteiro: concluir tarefa principal com entrada pertinente; repetir por teclado;
usar dados extremos; interromper requisição/transição; provocar erro e recuperar;
confirmar persistência; avaliar tema/preferências suportadas. Registre medição
de contraste no estado/fundo real e não estime números pela imagem.

## Checklist de aceite

- [ ] Plataforma, stack e versão mínima confirmadas.
- [ ] Funções originais preservadas e mapa de alterações disponível.
- [ ] Comandos e atalhos implementados, não apenas desenhados.
- [ ] Todos os estados relevantes têm comportamento e teste.
- [ ] Tokens, tipografia e densidade seguem o produto/plataforma.
- [ ] Navegação por teclado e foco avaliados no fluxo.
- [ ] Preferências e tecnologias assistivas pertinentes verificadas.
- [ ] Temas e fundos reais não destroem legibilidade.
- [ ] Redimensionamento/overflow e dados extremos não quebram a tarefa.
- [ ] Falha e recuperação preservam informações e evitam ação duplicada.
- [ ] Persistência, segurança e performance não foram inferidas de screenshots.
- [ ] Limitações de protótipo e medições não realizadas estão explícitas.

## Fontes adicionais a confirmar na tarefa

As páginas Apple de Accessibility, Typography, Motion e Windows exigiram
JavaScript na leitura direta desta pesquisa; não declaramos seu conteúdo como
lido. Consulte-as no host ou SDK quando a tarefa depender desses detalhes.
