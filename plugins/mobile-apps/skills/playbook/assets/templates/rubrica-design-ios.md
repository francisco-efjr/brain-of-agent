# Rubrica de design iOS (10 dimensões, 0 a 10)

Atribuição: a estrutura "pontuar 0 a 10 com o que levaria a 10" é destilada do skill `ios-design-review` do gstack (MIT, Copyright (c) 2026 Garry Tan), com redação própria; combinada com critérios do brain-of-agent `apple-design.md` (MIT, Francisco Edson) e números oficiais da HIG (V-18). Nenhum comando, binário ou texto em bloco do gstack foi copiado, e o fluxo dele (ponte de depuração, daemon, Tailscale) não é usado aqui.

**Somente leitura.** A rubrica avalia telas fornecidas pelo usuário (capturas ou código); não altera o produto. Capturas e logs com dados reais devem ser redigidos antes de anexar.

Valores oficiais (V-18, Verificado): Dynamic Type até 200%; texto padrão 17 pt, mínimo 11 pt; alvo 44x44 pt, mínimo 28 pt; contraste 4,5:1 até 17 pt e 3:1 a partir de 18 pt ou negrito. Valores do autor do gstack (grade de 4 e 8 pt, 200 a 300 ms em feedback, no máximo duas animações simultâneas, "texto tocável abaixo de 24 pt") são **Suposição/preferência**, não HIG. "Cargo-cult de Material Design" é opinião. Apple é preferência de acabamento, não imposição de stack.

App: [nome] · Telas avaliadas: [lista] · iOS mínimo: [versão] · Data: [AAAA-MM-DD]
Limites: avaliação por captura ou código não prova comportamento, persistência nem acessibilidade com leitor de tela.

## Dimensões

| # | Dimensão | O que avaliar | Base |
| --- | --- | --- | --- |
| 1 | Hierarquia tipográfica | Tamanhos consistentes por papel (título, corpo, legenda), estilos de texto do sistema escaláveis, entrelinha coerente | V-18 (escala), preferência do autor para o resto |
| 2 | Ritmo de espaçamento | Espaçamento consistente, safe areas respeitadas, sem valores "mágicos" soltos | Preferência (grade de 4/8 pt é Suposição) |
| 3 | Hierarquia de cor | Ação primária em maior destaque, destrutiva distinta, modo escuro correto, contraste 4,5:1 e 3:1 | V-18 |
| 4 | Alvos de toque | Todo elemento interativo com 44x44 pt (mínimo absoluto 28 pt) | V-18 |
| 5 | Estados de carregando, vazio e erro | Cada um presente e intencional; vazio explica o próximo passo; sem tela em branco durante trabalho assíncrono | brain `apple-design.md` (critério 2) |
| 6 | Acessibilidade | Rótulos em todo controle, Dynamic Type no maior tamanho sem quebrar layout, Reduce Motion, não depender só de cor | V-18, V-19, V-48 |
| 7 | Disciplina de animação | Movimento explica a mudança, é interrompível e reduzível; duração coerente | brain (critério 6); números do autor são Suposição |
| 8 | Idioma da plataforma | Componentes do sistema (`NavigationStack`, `List`, `Form`, sheets) onde cabem; sem reinventar navegação | brain `apple-design.md` |
| 9 | Densidade de informação | Conteúdo cabe sem rolagem horizontal; listas com padrões do sistema (deslizar para agir, menus de contexto) | Preferência |
| 10 | Sinais de conteúdo genérico | Dados fictícios deixados (lorem ipsum), layouts de catálogo, efeitos decorativos sem função | Preferência do autor |

## Pontuação por tela

| Tela | Dim. 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | O que levaria a 10 (maior alavanca) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Login] | | | | | | | | | | | |

Pergunte ao usuário apenas quando uma nota ficar abaixo de 7 e a correção tiver trade-off. Registre, por dimensão, a única mudança de maior alavanca.

## Modos de falha comuns

| Sintoma | Ação |
| --- | --- |
| Captura preta ou em branco | Confirmar com o usuário se o app estava renderizando; não pontuar |
| Número de telas diferente da lista do usuário | Perguntar se há telas atrás de estado ainda não alcançado |
| Fundo ou tema diferente do real | Pontuar contraste só com o fundo real; não estimar números pela imagem |

## Checklist de aceite (brain `apple-design.md`, adaptado)

- [ ] Plataforma e versão mínima confirmadas.
- [ ] Funções originais preservadas.
- [ ] Todos os estados relevantes têm comportamento e teste.
- [ ] Tokens, tipografia e densidade seguem o produto e a plataforma.
- [ ] Preferências de acessibilidade verificadas (texto maior, Reduce Motion).
- [ ] Temas e fundos reais não destroem a legibilidade.
- [ ] Dados extremos e falhas não quebram a tarefa.
- [ ] Persistência, segurança e performance não foram inferidas de capturas.
- [ ] Limitações e medições não realizadas estão explícitas.
