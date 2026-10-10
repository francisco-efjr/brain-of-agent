# Rubrica de GDD: critérios, sinais de ambiguidade e revisão de exemplo

Sumário: [Critérios por dimensão](#critérios-por-dimensão) · [Sinais de ambiguidade](#sinais-de-ambiguidade) · [Grafo de dependências](#grafo-de-dependências) · [Revisão de exemplo](#revisão-de-exemplo) · [Limites](#limites)

Fonte da rubrica: V-27 (design-review do Donchitos/Claude-Code-Game-Studios, classe B, MIT; padrão destilado, redação própria). Padrão de documento longo: V-09. Os exemplos são fictícios e servem de formato; rótulos: Verificado (trecho citado), Inferido (interpretação), Suposição, NOT ASSESSED.

## Critérios por dimensão

### Completude
- Cada seção esperada existe e tem conteúdo (não "TBD").
- Todo termo de jogo usado tem definição (glossário ou primeira menção).
- Toda referência a outro documento resolve a um arquivo existente.
- Há seção de "fora do escopo" e de questões abertas; ausência dela indica que o autor não separou o que sabe do que falta.

### Consistência
- Fórmula x texto: o exemplo numérico do texto bate com a fórmula? (Recalcule a conta do exemplo.)
- Regra x caso de borda: o caso de borda respeita a regra geral ou a contradiz?
- Números repetidos em seções diferentes (vida, custo, cooldown) coincidem?
- Dependências nos dois sentidos: se A diz "usa stamina de B", B lista A como consumidor?
- Terminologia: o mesmo conceito com dois nomes ("energia" e "stamina") ou dois conceitos com o mesmo nome.

### Implementabilidade
- Cada regra é um trio condição -> efeito -> valor.
- Estados têm tabela de transições; estados inválidos são declarados inalcançáveis.
- Critérios de aceite são observáveis ("stamina cai 25 ao usar dash") e não adjetivos ("dash satisfatório").
- Valores ajustáveis apontam onde moram (arquivo de dados), para não ficarem fixos no código.
- Ordem de operações definida quando há simultaneidade (dois danos no mesmo quadro).
- Dependência de plataforma e de entrada (teclado, gamepad, toque) declarada quando muda a regra.

### Encaixe
- Conflito entre mecânicas (ex.: invulnerabilidade do dash x armadilhas de dano contínuo).
- Cada sistema serve a pelo menos um pilar; sistema que não serve nenhum é candidato a corte ou a pergunta ao designer.
- Grafo de dependências sem ciclo não resolvido; ordem de implementação possível.
- Escopo total compatível com o que o projeto declara (equipe, prazo): isso é Suposição se o GDD não informa capacidade.

## Sinais de ambiguidade

| Sinal no texto | Por que atrapalha | Pergunta que resolve |
| --- | --- | --- |
| "rápido", "forte", "pouco" sem número | cada programador escolhe um valor | qual valor e unidade? |
| "o inimigo reage" | reação indefinida | qual estado, gatilho e duração? |
| "a definir", "TBD", seção vazia | lacuna disfarçada de plano | quem decide e até quando? |
| "como em [outro jogo]" | referência não é especificação | quais comportamentos exatos? |
| "quando apropriado" | condição ausente | qual condição? |
| exemplo numérico sem fórmula | não generaliza | qual é a fórmula? |
| regra sem caso de borda | zero, máximo e simultâneo ficam sem decisão | o que acontece em cada extremo? |
| sistema citado sem documento | dependência fantasma | existe ou será escrito? por quem? |

## Grafo de dependências

Monte uma lista simples `A -> B` (A depende de B). Verifique:

1. Todo nó existe como documento ou está marcado como a ser escrito.
2. Não há ciclo sem decisão (A depende de B que depende de A).
3. A ordem de implementação segue as dependências: o que não depende de ninguém vem primeiro.
4. Conflitos entre nós vizinhos estão listados na dimensão Encaixe.

Exemplo: `Crafting -> Forja -> Economia`; Economia vazia e Forja inexistente significam que Crafting não é implementável: vereditos `NOT ASSESSED` (Encaixe) e `MAJOR REVISION NEEDED` para o conjunto.

## Revisão de exemplo

Documento fictício:

> §1 Pilares: ritmo e leitura clara.
> §2 Combate: dano = ataque - defesa; crítico 10%; dash consome stamina.
> §3 Stamina: não afeta o movimento.
> §4 Economia: (vazio)
> §5 Crafting: depende do Sistema de Forja (a definir).

| Dimensão | Veredito | Achados (seção) |
| --- | --- | --- |
| Completude | NEEDS REVISION | §4 vazia; sem critérios de aceite em nenhuma seção; sem "fora do escopo" |
| Consistência | MAJOR REVISION NEEDED | §2 "dash consome stamina" x §3 "stamina não afeta movimento": dash é movimento; ou a stamina afeta, ou o dash não a consome |
| Implementabilidade | NEEDS REVISION | §2 "dano = ataque - defesa" sem piso (dano negativo?); "crítico 10%" sem multiplicador, sem semente, sem arredondamento |
| Encaixe | NOT ASSESSED | §5 referencia documento inexistente; sem como avaliar conflito com Economia |

Agregado: MAJOR REVISION NEEDED (a contradição de §2/§3 sozinha impede implementar o dash).

Perguntas abertas:
1. Dash consome stamina? Se sim, §3 deve declarar que a stamina afeta o movimento. Opção A: dash bloqueado a zero; opção B: dash curto a zero.
2. Qual o piso do dano? (zero, mínimo 1?)
3. Multiplicador e arredondamento do crítico; a aleatoriedade usa semente?
4. Quem escreve o Sistema de Forja e quando? Crafting fica bloqueado até então.
5. Critérios de aceite do combate: quais comportamentos devem ser testáveis?

Não avaliado: balanceamento numérico (fora do escopo), economia (vazia).

Nenhum valor foi sugerido para Economia, e nenhum arquivo foi escrito.

## Limites

- A rubrica avalia a estrutura do documento. Se os números estão bons depende de playtest e de modelagem, sem fonte validada aqui.
- Criação de GDD, design de nível, narrativa e economia estão fora deste plugin (lacuna declarada).
- Revisão por agente da mesma família de modelo que escreveu o GDD não é validação independente.
