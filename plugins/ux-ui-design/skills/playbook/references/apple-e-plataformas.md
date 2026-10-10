# Convenções de plataforma: Apple HIG, web e lacuna de Material 3

Quando o alvo é iOS, iPadOS ou macOS, estes números e critérios valem como fato; em web ou Android servem só de comparação. Base: critérios locais e matriz de componente do brain-of-agent (`apple-design.md`, MIT, do autor do plugin, adaptado; consulta de 2026-10-09 pelo brain) e tamanhos da HIG lidos em 2026-10-10 (V-39, © Apple: só destilado, sem texto copiado). Implementação nativa (SwiftUI, Compose, React Native, Flutter) é de `/mobile-apps:playbook`.

## Sumário

- [Alcance e postura](#alcance-e-postura)
- [Tamanhos e acessibilidade Apple (V-39)](#tamanhos-e-acessibilidade-apple-v-39)
- [Conflito de tamanhos de alvo](#conflito-de-tamanhos-de-alvo)
- [Critérios locais de qualidade](#critérios-locais-de-qualidade)
- [Transferência macOS para web e mobile](#transferência-macos-para-web-e-mobile)
- [Matriz de componente e roteiro](#matriz-de-componente-e-roteiro)
- [Checklist de aceite](#checklist-de-aceite)
- [Exemplos](#exemplos)
- [Lacunas: Material 3 e páginas Apple não lidas](#lacunas-material-3-e-páginas-apple-não-lidas)

## Alcance e postura

Apple é a preferência de acabamento desta fábrica, não um ranking comprovado de todos os design systems. Adote integração, consistência e cuidado com a interação, preservando a identidade e a plataforma do produto. Não imponha migração nativa para obter uma aparência. A HIG organiza orientações por plataforma e componente; use as convenções do ambiente-alvo para que controles familiares façam o que o usuário espera. O princípio vale para a escolha de componentes e não vira norma universal para web.

- No Mac, janelas ajustáveis, menus e teclado fazem parte de tarefas longas: planeje comandos e contexto de janela junto da interface, em vez de desenhar uma moldura que só simule o sistema (HIG, Designing for macOS).
- Liquid Glass e materiais são orientados a controles e navegação; aplicar em excesso na camada de conteúdo prejudica a hierarquia. Componentes do sistema já trazem os comportamentos apropriados; efeito personalizado pede contenção e legibilidade sobre fundos reais e com as preferências de acessibilidade ligadas (HIG, Materials; citadas pelo brain, não reabertas aqui).
- Confirme SDK, versão mínima e documentação aplicável antes de escolher APIs e medidas. Não declare recurso suportado porque o nome da API apareceu em código gerado.

## Tamanhos e acessibilidade Apple (V-39)

Verificado em 2026-10-10 pelo endpoint de dados da página de Accessibility (a página HTML devolve só o título; o endpoint não é documentado e pode mudar).

| Plataforma | Alvo padrão | Alvo mínimo |
| --- | --- | --- |
| iOS e iPadOS | 44×44 pt | 28×28 pt |
| macOS | 28×28 pt | 20×20 pt |
| watchOS | 44×44 pt | 28×28 pt |
| visionOS | 60×60 pt | 28×28 pt |
| tvOS | 66×66 pt | 56×56 pt |

- Espaçamento entre alvos: cerca de 12 pt em elementos com bezel e cerca de 24 pt em elementos sem bezel.
- Texto: permitir ampliação de pelo menos 200% (140% no watchOS); tamanho de texto padrão e mínimo no iOS: 17 pt e 11 pt.
- Contraste: o Accessibility Inspector avalia no nível AA (4,5:1 até 17 pt; 3:1 para texto de 18 pt ou em negrito). Ofereça esquema de maior contraste quando Increase Contrast estiver ligado, verifique claro e escuro e prefira cores do sistema.
- O piso de 28 pt contradiz a regra popular "44 pt sempre": 44 pt é o padrão; 28 pt, o mínimo. Cite os dois.
- Números do arquivo de inspiração do brain (13 pt, margens de 20 pt, alvo de 20×20 pt, nomes de releases) **não** foram confirmados como contratos oficiais: não os copie.

## Conflito de tamanhos de alvo

| Referência | Valor | Status |
| --- | --- | --- |
| WCAG 2.5.8 (AA), piso normativo web | 24×24 px CSS | Verificado (V-08) |
| WCAG 2.5.5 (AAA) | 44×44 px CSS | Verificado (brain) |
| Meta de toque em web mobile | 44 px | convenção (V-27); iOS padrão 44 pt |
| HIG iOS mínimo | 28×28 pt | Verificado (V-39) |
| Android (Material) | 48×48 dp | **Não verificável** aqui (páginas do Material 3 não renderizam sem JavaScript) |

Resolução do plugin: piso normativo 24×24 px CSS; meta de toque 44; Apple 44 pt padrão e 28 pt mínimo; 48 dp só como comparação rotulada Não verificável.

## Critérios locais de qualidade

Critérios de revisão deste projeto, não citações normativas (origem: brain-of-agent).

1. Inventário original mapeado ao novo fluxo: nenhuma função desaparece por estética; propostas novas ficam identificadas.
2. Toda ação tem comportamento, feedback, estado e recuperação definidos.
3. Tokens semânticos expressam função, variantes e consistência; cor literal espalhada não é design system (ver `design-tokens.md`).
4. Protótipo e aplicação implementada são diferenciados: botão navegável não comprova salvamento, permissão ou integração.
5. Acessibilidade é comportamento verificável, não acabamento.
6. Movimento explica mudança e admite interrupção e redução.
7. A tela tem dados reais ou sintéticos plausíveis, extremos e falhas; sem lorem ipsum para mascarar overflow ou hierarquia.

## Transferência macOS para web e mobile

| Intenção | macOS | Web, mobile ou outra stack |
| --- | --- | --- |
| Comandos familiares | Menus, janela e teclado nativos | HTML e controles do sistema, rotas e gestos esperados |
| Hierarquia | Navegação e conteúdo distintos | Estrutura semântica e responsiva, sem obrigar moldura de Mac |
| Acabamento | Materiais compatíveis com o SDK | Tokens e componentes existentes; efeito não é requisito |
| Recuperação | Undo quando aplicável | Reversão ou confirmação conforme operação, contrato e risco |
| Acesso assistivo | Árvore e recursos nativos | Semântica HTML e padrões ARIA quando necessários |

Na web, consulte os padrões WAI-ARIA (APG) para widgets personalizados: escolha a semântica e a interação correspondentes, em vez de aplicar só um papel.

## Matriz de componente e roteiro

| Elemento | Estados e verificações |
| --- | --- |
| Campo | Vazio, foco, preenchido, inválido, somente leitura, desabilitado, texto longo |
| Ação | Normal, foco, pressionada, processando, indisponível, erro |
| Lista | Vazia, carregando, resultados, seleção, erro, volume e paginação |
| Diálogo | Foco inicial, tabulação, validação, fechar e devolver o foco |
| Navegação | Atual, teclado, voltar e deep link, painel e overflow quando aplicáveis |

Roteiro: concluir a tarefa principal com entrada pertinente; repetir por teclado; usar dados extremos; interromper requisição ou transição; provocar erro e recuperar; confirmar persistência; avaliar tema e preferências suportadas. Registre a medição de contraste no estado e no fundo reais e não estime números pela imagem.

## Checklist de aceite

- [ ] Plataforma, stack e versão mínima confirmadas.
- [ ] Funções originais preservadas e mapa de alterações disponível.
- [ ] Comandos e atalhos implementados, não apenas desenhados.
- [ ] Todos os estados relevantes têm comportamento e teste.
- [ ] Tokens, tipografia e densidade seguem o produto e a plataforma.
- [ ] Navegação por teclado e foco avaliados no fluxo.
- [ ] Preferências e tecnologias assistivas pertinentes verificadas.
- [ ] Temas e fundos reais não destroem a legibilidade.
- [ ] Redimensionamento, overflow e dados extremos não quebram a tarefa.
- [ ] Falha e recuperação preservam informações e evitam ação duplicada.
- [ ] Persistência, segurança e performance não foram inferidas de screenshots.
- [ ] Limitações de protótipo e medições não realizadas estão explícitas.

## Exemplos

**Lista de clientes em sistema web existente.** Pedido: tornar a lista consistente e acessível. Não substitua a stack por SwiftUI nem adicione botões de janela do macOS. Inventarie busca, filtro, ordenação, seleção e ações. Especifique semântica, estados vazio, carregando e erro, foco ao fechar diálogo e tratamento de resposta obsoleta. Teste por teclado, em viewport estreito e com nomes longos. Registre persistência e autorização da API à parte da avaliação visual.

**App Mac existente.** Confirme SDK e versão mínima antes de usar API nova de material. Avalie compatibilidade e comportamento alternativo. Valide comando na janela ativa, seleção, fechar e reabrir, redimensionamento. Não declare suporte só porque o nome da API apareceu num trecho gerado.

## Lacunas: Material 3 e páginas Apple não lidas

- **Material Design 3: Não verificável.** As páginas `m3.material.io` devolvem só o título sem JavaScript; a regra de 48 dp só aparece em trechos de busca. Para obter: `developer.android.com` (acessibilidade em Compose), repositório `material-components/material-web` ou documentação de tokens `md.sys`. Até lá, o plugin só declara a lacuna.
- As páginas Apple de Typography, Motion e Windows não foram lidas (exigem JavaScript na leitura direta); consulte-as no host ou no SDK quando a tarefa depender desses detalhes. Os tamanhos acima vêm só da página de Accessibility.
- Motion (duração, easing, hierarquia de movimento): sem diretriz oficial lida; use apenas `prefers-reduced-motion` (ver `wcag-aa.md`) e as regras de polegar de `padroes-e-antipadroes.md`, rotuladas Inferido.
