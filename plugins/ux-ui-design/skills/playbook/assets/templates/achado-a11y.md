# Achado de acessibilidade: [título curto com tela e sintoma]

Template T-09. Uso: `a11y-checklist` e `a11y-reviewer`. Um arquivo ou bloco por achado. Severidade pelo efeito na tarefa, não só pelo `impact` do axe. Status epistêmico obrigatório: o que foi **anunciado** só é Verificado se um leitor de tela real foi usado.

- **ID:** [ACH-01] · **Data:** [AAAA-MM-DD]
- **Critério WCAG:** [número, nome, nível. Ex.: 4.1.2 Nome, função, valor (A)]
- **Quem é afetado:** [leitor de tela, controle por voz, teclado, baixa visão, daltonismo, deficiência motora, cognição]
- **Tecnologia assistiva e navegador:** [ex.: Windows 11, Firefox + NVDA] · **Reproduz em:** [outras combinações testadas, ou "não testado"]
- **Local:** [arquivo:linha ou seletor, rota e estado]
- **Passos para reproduzir:**
  1. [___]
  2. [___]
- **Esperado:** [o que o usuário deveria ouvir ou conseguir fazer]
- **Obtido:** [o que foi anunciado ou aconteceu]
- **Evidência:** [saída do axe com regra e seletor, captura, gravação com áudio do leitor, trecho de código]
- **Status:** [Verificado | Inferido (li o código) | Não testado]
- **Severidade:** [crítico (antes do merge) | importante (na sprint) | sugestão], mapeada para [alta | média | baixa] pelo efeito na tarefa: [impede sem contorno → alta]
- **Correção:** [mudança específica; elemento nativo antes de ARIA]
- **Verificação da correção:** [como reconfirmar: teclado, leitor de tela, axe]

## Exemplo preenchido (formato adaptado do brain-of-agent, MIT)

- **ACH-01 · Carrinho: botão de remover item é anunciado só como "botão"**
- **Critério:** 4.1.2 Nome, função, valor (A). **Afeta:** quem usa leitor de tela e controle por voz.
- **Ambiente:** homologação, build [x.y.z]; Windows 11, Firefox + NVDA; [reproduz ou não em iOS, Safari + VoiceOver: não testado].
- **Passos:** 1. Adicionar dois produtos ao carrinho. 2. Abrir `/carrinho`. 3. Com NVDA ligado, Tab até o primeiro item.
- **Esperado:** "Remover Camiseta azul M do carrinho, botão". **Obtido:** "botão".
- **Evidência:** axe `button-name` (critical) em `.cart-item:nth-child(1) .icon-btn`; gravação com áudio do leitor.
- **Status:** Verificado. **Severidade:** importante, alta (impede revisar o carrinho com autonomia, sem contorno).
- **Correção:** `<button type="button" aria-label="Remover Camiseta azul M do carrinho">` com o ícone em `<svg aria-hidden="true">`; depois de remover, foco no próximo item e aviso em `role="status"` ("Camiseta azul M removida").
