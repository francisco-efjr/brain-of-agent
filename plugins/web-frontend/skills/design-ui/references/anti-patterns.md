# Anti-padrões visuais de saída de IA (lista configurável)

Calibração de saída de IA em 2026-10-10: o brief do usuário e os tokens do projeto sempre vencem, inclusive quando pedem um visual desta lista. A lista envelhece (relatos de comunidade, Não verificado por mim, dizem que o visual volta a convergir com o tempo); revise-a a cada trimestre ou quando o plano começar a parecer com ela.

Fontes (redação própria, sem texto copiado): skill `frontend-design` da Anthropic (V-01, Apache-2.0), `impeccable` de Paul Bakaus (V-35, Apache-2.0; o instalador `npx` não é adotado), processo de `design-html` do gstack (brain-of-agent, inspiração de processo). Efeito real de qualquer lista sobre qualidade visual: Não verificável.

## Como usar

1. Na revisão do plano (fase 2 de `design-ui`), percorra a tabela. Para cada linha que o plano reproduz, escreva a pergunta de substituição e responda com algo derivado do assunto.
2. Se o brief ou o `DESIGN.md` pede o item, mantenha e registre "mantido a pedido".
3. Uma linha que o plano reproduz sem justificativa vira linha "mudei X porque Y" ou é cortada.
4. Detector limpo, lista limpa ou captura bonita não provam qualidade visual nem acessibilidade: inspecione em 320 px e em desktop.

## Tabela

| Sinal de saída genérica | Por que é um sinal | Pergunta que força uma escolha do assunto |
| --- | --- | --- |
| Fonte padrão (Arial, Inter) sem motivo registrado | É o valor para o qual o modelo converge; tipografia é o sinal mais barato de identidade | Que objeto físico ou texto real deste assunto tem uma letra característica (placa, etiqueta, manual)? |
| Gradiente roxo-azul sobre branco | Escolha estatisticamente segura repetida em páginas de produto | Que cor este público já associa ao assunto? Que cor ele nunca vê nesse mercado? |
| Creme com serifa e acento terracota | Calibração de 2026 do que a IA faz quando "foge" do azul | A paleta nasce de materiais do assunto (papel, aço, tinta) ou de um padrão de moda? |
| Quase-preto com um único acento neon | Estética "dev tool" aplicada a qualquer assunto | Este público trabalha à noite em tela escura ou à luz do dia? |
| Layout de jornal (colunas com filetes e caixa alta) | Segundo padrão de fuga mais comum | A hierarquia de leitura do assunto é a de uma notícia? |
| Kit de cartões SaaS idênticos (ícone, título, duas linhas) | Estrutura intercambiável: qualquer texto cabe | Que informação do assunto tem forma própria (tabela de preços, mapa, linha do tempo)? |
| Cartão dentro de cartão | Borda e sombra no lugar de hierarquia | O que muda se o container interno virar só espaçamento e peso tipográfico? |
| Cinza sobre fundo colorido | Contraste baixo; costuma falhar 4,5:1 | Medido, o texto passa? Use tom do próprio fundo em vez de cinza |
| Preto e cinza puros sem tom | Frio e sem relação com a paleta | Qual matiz da paleta pode tingir os neutros? |
| Easing com bounce em tudo | Movimento decorativo sem função | Que mudança de estado esse movimento explica? Se nenhuma, corte |
| Numeração 01/02/03 sem sequência real | Estrutura visual é informação; número sem ordem engana | Existe ordem de passos de verdade? Se não, tire os números |
| Hero com métricas genéricas ("10k+ usuários") | Conteúdo inventado que parece prova | Há um número real do cliente? Sem dado verdadeiro, não invente |
| CTA "Começar agora" sem origem | O texto não vem da tarefa | Qual verbo e objeto da tarefa principal do brief ("Agendar revisão")? |
| Emoji como elemento visual de interface | Substitui ícone ou ilustração por conveniência; leitor de tela anuncia o nome | Um ícone com nome acessível ou uma imagem do assunto serve melhor? |
| Seção de depoimentos genérica | Foto de banco e frase intercambiável | Existe depoimento real, com nome e contexto? Sem, omita a seção |
| Barra de recursos com grade 3x2 de ícones | Preenche espaço, não responde a tarefa | Qual dessas informações a pessoa precisa antes de decidir? |

## Itens que não são anti-padrões (não corte por reflexo)

- Fonte do sistema (`ui-sans-serif, system-ui`) em produto utilitário: pode ser a escolha certa se o plano disser por quê.
- Cartões quando cada item é um objeto independente com ações próprias.
- Gradiente quando a marca o define nos tokens.
- Tema escuro quando o público ou o `DESIGN.md` o exige.

## Manutenção

Quando uma linha deixar de aparecer em saídas reais por seis meses, remova-a; quando surgir um padrão novo repetido em três telas, acrescente com a pergunta de substituição. Registre a data da revisão no cabeçalho.
