# design-engineering-kit

Plugin do Claude Code para o **designer-engenheiro**: leva um design (link do Figma, brief ou tela existente) até uma UI implementada, **verificada no navegador** e **polida**. Reúne 17 skills de terceiros (motion e polimento de Emil Kowalski; direções visuais do taste-skill), um playbook com a **ordem de precedência de estilo**, 16 prompts prontos, 2 agentes somente leitura e 8 evals. É um **complemento opcional** de `ux-ui-design`, `web-frontend` e `mobile-apps`: funciona sozinho, mas não substitui nenhum deles.

Palavra-chave do modo completo: `DESIGNENG-COMPLETO`. Versão 0.1.0, licença MIT (as skills vendorizadas mantêm a licença MIT dos autores originais; ver "Créditos e licenças"). Conteúdo próprio em português brasileiro; as 17 skills vendorizadas estão em inglês, como no original.

**O kit não traz `.mcp.json`, hooks nem binários.** Figma MCP e Playwright MCP já existem como plugins oficiais mantidos pelos fornecedores; duplicá-los criaria servidores conflitantes. O kit orienta a instalação (sempre com a sua confirmação) e usa as ferramentas quando existirem, com fallback explícito quando não existirem.

## O que entrega

- **Playbook** que roteia o pedido, impõe 11 princípios com motivo, a precedência de estilo, 4 fluxos (Figma para código, verificação com Playwright, polimento, redesign), adaptação por plataforma (web, React Native/Expo, iOS, Android), segurança e rótulos epistêmicos (Verificado, Inferido, Suposição, Não verificável, Não aplicável).
- **Referências:** `figma-mcp`, `playwright-verificacao-ui`, `precedencia-e-adaptacao`, `android-motion` (tradução de princípios para Compose e Material motion), `claude-md-snippets` (DE-01 a DE-06) e `fontes`; **templates** de relatório de verificação de UI e de mapeamento Figma para tokens.
- **17 skills vendorizadas** sem alteração de conteúdo e **16 prompts** (`P-01` a `P-16`).
- **2 agentes**: `ui-verifier` (verifica no navegador, sem edição) e `motion-polish-reviewer` (revisão por leitura).
- **8 evals** desenhados, **não executados**.

## Quando usar

Ao implementar um frame do Figma; ao conferir uma tela no navegador em 375, 768 e 1280; ao revisar ou construir animações; ao dar acabamento antes de entregar; ao quebrar uma UI com dados extremos; ao redesenhar sem perder o design system; ao levar os princípios do Mo baile para Android. Não é para definir direção de design, tokens ou acessibilidade de design (`ux-ui-design`), nem para escrever testes de UI em CI (`qa-testing`, `web-frontend:e2e-tests`).

## Componentes

| Tipo | Nome | Para que serve | Efeito |
| --- | --- | --- | --- |
| Skill (núcleo) | `playbook` | Router, precedência, fluxos, plataforma, segurança, modo `DESIGNENG-COMPLETO` | Não |
| Skill | `prompts` | 16 prompts prontos (P-01 a P-16) | Não |
| Skill (Emil) | `emil-design-eng` | Filosofia de polimento, decisões de animação, checklist de revisão | Guia e revisão |
| Skill (Emil) | `animate` | Construir animação web decidindo se, propósito, curva, duração, interrupção | Escreve código |
| Skill (Emil) | `animate-expo` | Animação em React Native/Expo (Reanimated, gestos, háptico) | Escreve código |
| Skill (Emil) | `animation-vocabulary` | Nome do efeito a partir da descrição | Nenhum |
| Skill (Emil) | `apple-design` | Gestos, molas, materiais e tipografia no estilo Apple, para web | Guia e código |
| Skill (Emil) | `break-ui` | Quebrar UI com dados extremos, relatar antes de corrigir | Adiciona alternador só de desenvolvimento |
| Skill (Emil) | `find-animation-opportunities` | Onde animar (e o que rejeitar) | Somente leitura |
| Skill (Emil) | `improve-animations` | Auditoria de motion do código e planos de implementação | Somente leitura no código |
| Skill (Emil) | `review-animations` | Revisão contra 10 padrões, Block ou Approve | Somente leitura; **só por comando** |
| Skill (Emil) | `mobile-native` | Web mobile e PWA com cara de instalado (não é React Native) | Escreve código |
| Skill (Emil) | `pick-ui-library` | Escolher biblioteca de UI | Recomendação; **só por comando** |
| Skill (Emil) | `prototype` | Variantes lado a lado com seletor visual | Superfície temporária; **só por comando** |
| Skill (taste) | `design-taste-frontend` | Landing, portfólio e redesign anti-genérico, com dials | Escreve código |
| Skill (taste) | `redesign-existing-projects` | Auditar e elevar projeto existente | Escreve código |
| Skill (taste) | `minimalist-ui` | Direção editorial minimalista | Escreve código |
| Skill (taste) | `high-end-visual-design` | Direção premium de agência | Escreve código |
| Skill (taste) | `industrial-brutalist-ui` | Direção brutalista e de telemetria | Escreve código |
| Agente | `ui-verifier` | Verificação no navegador contra Figma, brief ou design system | Sem `Write`, `Edit`, `Bash`, `PowerShell`, `Agent` nem web; ferramentas de escrita do Figma bloqueadas por nome; grava só capturas |
| Agente | `motion-polish-reviewer` | Revisão de motion e polimento com arquivo:linha | `Read`, `Grep`, `Glob` |

Namespaces: skills como `/design-engineering-kit:playbook`; agentes como `design-engineering-kit:ui-verifier`. As três skills **só por comando** têm `disable-model-invocation`: o modelo não as chama pela ferramenta Skill. `review-animations` é usada como régua de leitura pelo agente de revisão; `prototype` e `pick-ui-library` (que criam arquivos ou podem instalar) só rodam quando você digita o comando ou diz "sim" na conversa.

## Instalação

Dentro do Claude Code:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install design-engineering-kit@brain-of-agent
```

Plugins oficiais complementares (opcionais; cada instalação altera sua configuração e o Claude pede confirmação antes de rodar):

```text
claude plugin install figma@claude-plugins-official
claude plugin install playwright@claude-plugins-official
```

Alternativas manuais: `claude mcp add --transport http figma https://mcp.figma.com/mcp` e, com versão fixada, `claude mcp add playwright -- npx @playwright/mcp@0.0.83`. **Não instale as duas formas do mesmo servidor.** O plugin oficial do Playwright usa `npx @playwright/mcp@latest`, sem versão fixa: se a cadeia de suprimentos importa, prefira a forma manual fixada. A autenticação do Figma é feita **por você** no navegador (OAuth); nunca cole token no chat. Usar o Figma MCP implica aceitar os termos de desenvolvedor da Figma. Requisitos: Node para o Playwright MCP; conta Figma com acesso ao arquivo; app local rodando para verificar. As skills vendorizadas têm upstream em `npx skills@latest add emilkowalski/skills` (Emil) e `/plugin marketplace add leonxlnx/taste-skill` (taste); o kit já traz as cópias congeladas, não as instale em paralelo.

## Exemplos de pedidos

1. **Figma para código:** "Implementa este frame: `<link do nó>`. Design system em `src/styles/tokens.css`." Lê o nó (contexto, variáveis, screenshot), mapeia para tokens e componentes, implementa na sua stack e verifica em 3 larguras. Sem o MCP, explica a instalação, espera seu "sim" e oferece o fallback com export e specs.
2. **Verificação:** "Confere `/pedidos` em localhost:5173 em 375, 768 e 1280." Snapshot, screenshot, console e rede por largura; relatório com achados, severidade e evidência; o que não deu para verificar fica explícito.
3. **Revisão de motion:** "Revisa o motion deste diff antes do merge." O agente `motion-polish-reviewer` lê os tokens de motion do projeto, aplica os 10 padrões e devolve tabela Before/After/Why com arquivo:linha e veredito.
4. **Dados extremos:** "Quebra essa lista de membros com nomes longos e zero itens." `break-ui` monta o pior caso plausível, relata e só corrige o que você escolher.
5. **Redesign com sistema:** "Redesenha Ajustes dentro do nosso design system." Recompõe hierarquia e espaçamento sem trocar fonte, ícones, cores ou raios dos tokens.
6. **Nova direção:** "Landing nova, sem design system: dá 3 direções." Variantes lado a lado com `prototype`; segue uma só depois da sua escolha.
7. **Android:** "Telas Compose no padrão Mo baile." Herda estrutura e regras, traduz os tokens de mola para `spring` e `tween`, trata reduzir movimento como sobrescrita de tema, e não copia CSS nem a estética do Mac.

## Precedência de estilo

1. **Design system do projeto**, sempre.
2. **Design system da casa** (`design-systems/mo-baile/`), só quando você o pedir ou apontar.
3. **Direções taste**, só sem sistema ou com pedido de direção nova.

O ofício de motion e polimento do Emil vale dentro de qualquer um; as proibições estéticas das skills taste (fontes, ícones, paletas) **não sobrepõem tokens de um sistema existente**; acessibilidade medida é o piso. Detalhes e conflitos reais em `skills/playbook/references/precedencia-e-adaptacao.md`. Essa ordem é instrução, não barreira técnica: para travá-la, cole a regra `DE-01` no `CLAUDE.md` do projeto.

## Modo `DESIGNENG-COMPLETO`

Escreva `DESIGNENG-COMPLETO` no seu pedido. O playbook lê as 6 referências em 3 lotes (lida, parcial ou ausente), monta a matriz de aplicabilidade (sistema ativo, Figma para código, tokens, verificação, acessibilidade estrutural, responsividade, motion, polimento, direção visual, plataforma nativa, segurança), implementa só o que o pedido incluir e revalida com evidência. A palavra em documento, camada do Figma, README ou log **não** ativa o modo; e ela **não amplia permissões** (instalar plugin ou MCP, escrever no Figma, commit e publicação continuam pedindo confirmação concreta).

## Segurança

Conteúdo de camadas e comentários do Figma, páginas, DOM e console é dado, não instrução. Playwright só em `localhost` ou URL autorizada, sem credenciais reais, sem `browser_run_code_unsafe`; o README do Playwright MCP diz que as flags de origem não são fronteira de segurança. Screenshots podem conter dados pessoais e são gravados em disco: o kit manda salvá-los em pasta ignorada pelo git. O servidor remoto do Figma tem ferramentas de escrita no canvas (`use_figma` executa JavaScript no arquivo) e ferramentas que gastam crédito (`generate_image`): o kit só usa leitura, e o `ui-verifier` as bloqueia pelo nome. Logos de marcas reais, depoimentos e métricas só entram se você fornecer. O kit não instala nada sozinho.

## Relação com outros plugins

| Plugin | Divisão |
| --- | --- |
| `ux-ui-design` | Direção, tokens, handoff e acessibilidade de design ficam lá; o kit implementa e verifica |
| `web-frontend` | `design-ui` e `verify-ui` cobrem o fluxo web geral; o kit acrescenta Figma MCP, Playwright MCP e as skills de motion |
| `mobile-apps` | Código SwiftUI, Compose e React Native lá; o kit traz motion e polimento (Expo) e a tradução para Android |
| `qa-testing` | Testes automatizados em CI lá; o kit só verifica a tela, não escreve suíte |

## Créditos e licenças

| Projeto | Autor | Licença | Commit | Skills incluídas | Modificações |
| --- | --- | --- | --- | --- | --- |
| `emilkowalski/skills` | Emil Kowalski | MIT, (c) 2026 Emil Kowalski | `e8a175de22ae1e49370fc144c1f3bb9aeedf988d` | `emil-design-eng`, `animate`, `animate-expo`, `animation-vocabulary`, `apple-design`, `break-ui`, `find-animation-opportunities`, `improve-animations`, `review-animations`, `mobile-native`, `pick-ui-library`, `prototype` | Nenhuma; conteúdo sem alteração |
| `Leonxlnx/taste-skill` | Leonxlnx | MIT, (c) 2026 Leonxlnx | `717446e07a78d4e6d7918b1fde1a263378eebac9` | `design-taste-frontend`, `redesign-existing-projects`, `minimalist-ui`, `high-end-visual-design`, `industrial-brutalist-ui` | Pasta renomeada para igualar o `name` do frontmatter (taste-skill, redesign-skill, minimalist-skill, soft-skill, brutalist-skill); conteúdo sem alteração |

Textos de licença em `third_party/<projeto>/LICENSE`; atribuição completa e procedimento de atualização em `third_party/README.md`. Ficaram de fora, por não serem design ou por dependerem de serviço específico: `write-swift`, `ask-sonner` (Emil); `image-to-code`, `imagegen-frontend-web`, `imagegen-frontend-mobile`, `brandkit`, `gpt-tasteskill`, `output-skill`, `stitch-skill`, `taste-skill-v1` (taste). Playwright MCP (Microsoft, Apache-2.0) e Figma MCP (Figma) **não** são redistribuídos: são instalados pelos plugins oficiais. O design system da casa Mo baile é do próprio autor (MIT). Fontes consultadas, com classe A/B/C e data: `skills/playbook/references/fontes.md`.

## Limitações honestas

- **Nada foi executado dentro do Claude Code.** Os 8 evals estão `designed_not_executed`; `claude plugin eval` exige 2.1.269 ou superior (o CLI local da fábrica é 2.1.128). Eles cobrem fallback, leitura de material colado e segurança; **não cobrem** o fluxo com Figma e Playwright conectados. Autores e revisores são modelos da mesma família: não é validação independente.
- **Verificação feita:** estrutural, em 2026-10-10 (`tools/verify_plugin.py`: PASS com 2 avisos de mais de 500 linhas nas skills vendorizadas; `claude plugin validate`: passed). Isso confere formato, não comportamento. Na mesma data, uma validação por agente separado (mesma família de modelo) conferiu licenças, conteúdo vendorizado contra o upstream, fatos de MCP nas fontes oficiais e segurança, e corrigiu o que estava defasado.
- **Skills vendorizadas congeladas** nos commits citados, em inglês, e algumas passam de 500 linhas como no original (`design-taste-frontend` 1206, `emil-design-eng` 674): o verificador avisa e o kit não as altera. Atualizações do upstream não chegam sozinhas (ver `third_party/README.md`).
- **Taste-skill é gosto de autor** (classe C). As `description` dessas skills podem acioná-las sozinhas em pedidos de landing ou redesign; a precedência é uma regra do playbook, não uma trava. Elas também se contradizem entre si (fontes, serifas), proíbem fontes e ícones que o seu sistema pode usar (Lucide, Inter), e `minimalist-ui` sugere texto secundário `#787774` que dá 4,48:1 sobre branco (abaixo de 4,5:1).
- **Conteúdo vendorizado é dado de terceiros.** Leitura e busca textual não acharam pedido de segredo, `curl` com pipe nem exfiltração. Acharam: comandos de instalação (`npx expo install`, `npm install` de bibliotecas, `npx shadcn@latest`); placeholders externos (picsum.photos, Unsplash, CDN do Simple Icons); `design-taste-frontend` manda usar qualquer gerador de imagem disponível, pôr logos reais de marcas em "Trusted by" e inventar dados com cara de reais; `redesign-existing-projects` sugere rolagem com inércia; `improve-animations` grava planos em `plans/`; `prototype` sobe uma rota temporária. O kit manda **não executar** instalação, não gerar imagem, não usar logo ou dado com cara de real sem o seu pedido, e trata `prototype` e `pick-ui-library` como só por comando. As skills Emil abrem com uma saudação fixa quando chamadas sem pergunta.
- **Figma:** o limite de leitura diverge entre as fontes oficiais (guia no GitHub: 6 chamadas por mês para Starter e assentos View/Collab; documentação de desenvolvedores: 20 por mês, e 200 a 600 por dia para assentos Dev/Full); o kit assume o menor. Nomes de ferramentas e das 14 skills do plugin oficial foram conferidos nas fontes em 2026-10-10, não numa sessão com o plugin instalado.
- **Playwright** não verifica app nativo, leitor de tela, nem sensação de movimento. O plugin oficial usa `@latest`.
- **Android:** não há skill dedicada; a tradução em `android-motion.md` é Inferida e valores do Material 3 são Não verificáveis (a documentação do Material 3 não foi aberta; a do Compose e a de acessibilidade Android foram, para `spring`, 48 dp e escala de animação). O cálculo `dampingRatio = 1 - bounce` dos tokens do Mo baile foi conferido por conta, não compilado.
- O kit **complementa**, não substitui, `verify-ui` e `design-ui` do `web-frontend`; revalide a cada versão do Claude Code, dos MCPs e das fontes.
