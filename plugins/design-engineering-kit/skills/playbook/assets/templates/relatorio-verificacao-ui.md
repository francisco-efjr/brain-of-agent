# Relatório de verificação de UI: [tela, rota ou componente]

Template do design-engineering-kit. Uso: fluxo (b) do playbook e agente `ui-verifier`. Somente leitura: este relatório não altera o produto. Cada achado precisa de evidência; sem evidência, a linha vira "Não verificado". Captura estática não prova movimento; snapshot não substitui leitor de tela; revisão do modelo não é validação externa.

## 1. Escopo e ambiente

- **Alvo:** [URL local ou autorizada] · **Rota/fluxo:** [ ] · **Data:** [AAAA-MM-DD] · **Versão/commit do app:** [ ou "desconhecido"]
- **Referência comparada:** [Figma (link do nó) | brief | design system (caminho) | nenhuma]
- **Ferramenta:** [Playwright MCP (plugin oficial | manual) versão [ ] | outro navegador | capturas do usuário]
- **Navegador/engine:** [chromium | firefox | webkit | desconhecido] · **Perfil:** [isolado | desconhecido] · **Sem credenciais reais:** [sim | não aplicável]
- **Não foi possível:** [ex.: sem servidor, sem acesso ao Figma, sem emulação de preferências]

## 2. Critério de aceite (escrito antes de olhar a tela)

| # | Critério observável | Fonte (brief/Figma/sistema) |
| --- | --- | --- |
| C1 | [ex.: sem rolagem horizontal em 375 px] | [ ] |
| C2 | [ex.: todo controle interativo com nome no snapshot] | [ ] |

## 3. Matriz por largura

| Verificação | 375 | 768 | 1280 |
| --- | --- | --- | --- |
| Carrega sem erro de console | [Verificado / Falha / Não verificado] | | |
| Sem rolagem horizontal | | | |
| Estrutura no snapshot (títulos, regiões, nomes) | | | |
| Layout vs referência | | | |
| Foco visível e ordem de Tab | | | |
| Texto longo / dados extremos | | | |
| Artefatos (arquivos de captura) | [caminho] | [caminho] | [caminho] |

## 4. Console e rede

| Tipo | Mensagem/URL | Onde | Severidade |
| --- | --- | --- | --- |
| [erro/aviso/4xx/5xx/origem externa] | [texto ou URL, sem dados pessoais] | [rota, largura] | [alta/média/baixa] |

## 5. Achados

| ID | Severidade | Largura | Evidência (captura, trecho do snapshot, arquivo:linha) | Critério | Recomendação | Rótulo |
| --- | --- | --- | --- | --- | --- | --- |
| V-01 | [alta/média/baixa] | [375] | [`shots/pedidos-375.png`; snapshot: `button` sem nome] | [C2] | [adicionar rótulo acessível] | [Verificado] |

Severidade: alta impede a tarefa ou falha acessibilidade estrutural; média diverge do design ou do sistema de forma visível; baixa é polimento.

## 6. Divergências do design

| Item | Referência | Implementado | Decisão sugerida | Quem confirma |
| --- | --- | --- | --- | --- |
| [espaçamento do card] | [24 px, token `space-6`] | [16 px] | [usar `space-6`] | [humano] |

## 7. Não verificado

- [Leitor de tela real · sensação de movimento · dispositivo real · outros navegadores · conteúdo atrás de login · estados não alcançáveis sem dados reais]

## 8. Pendências do humano e próximo passo

- [Decisões, acessos, dados fictícios necessários] · **Próximo passo:** [ ]
