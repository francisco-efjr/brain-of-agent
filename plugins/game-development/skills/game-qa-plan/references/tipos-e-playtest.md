# Tipos de teste de jogo e playtest: detalhes e exemplos

Sumário: [Classificação com sinais](#classificação-com-sinais) · [Testes de lógica: exemplo](#testes-de-lógica-exemplo) · [Smoke](#smoke) · [Plano de playtest preenchido](#plano-de-playtest-preenchido) · [Relatório de playtest preenchido](#relatório-de-playtest-preenchido) · [Charter exploratório](#charter-exploratório) · [Fontes](#fontes)

Rótulos: Verificado (na fonte citada), Inferido, Suposição, Não verificável, NÃO AVALIADO. Os exemplos são ilustrativos e redação própria; os números são fictícios e nunca devem ser copiados como resultado.

## Classificação com sinais

| Se a história fala de... | Tipo | Por quê |
| --- | --- | --- |
| fórmula, limiar, dano, custo, cooldown, probabilidade, transição de estado | Logic | saída determinística dado o input; automatizável |
| gravar/carregar, rede, troca de cena, persistência, ordem de inicialização | Integration | cruza sistemas; falha aparece na junção |
| "sensação", "responsivo", animação, impacto, câmera, som, juice | Visual/Feel | só um humano julga; captura documenta |
| menu, HUD, legenda, foco, remapeamento, tela de carregamento | UI | checklist visual e de navegação |
| arquivo de bindings, tabela de itens, Resource de balanceamento | Config/Data | validar esquema, faixas, referências cruzadas |

Regras (V-26): `Type:` declarado é autoritativo; inferido vira lacuna a confirmar com o dono; empate entre Logic e Integration vira Integration; história sem escopo = NÃO AVALIADO. A mesma história pode ter dois tipos (ex.: UI + Config/Data no remapeamento): liste os dois.

## Testes de lógica: exemplo

Regra (fictícia, a confirmar no GDD): `dano = max(ataque - defesa, 0)`; crítico dobra o dano; chance de crítico 10%.

| Caso | Entrada | Esperado | Classe |
| --- | --- | --- | --- |
| abaixo do limiar | ataque 4, defesa 10 | 0 | limite |
| no limiar | ataque 10, defesa 10 | 0 | limite |
| acima do limiar | ataque 11, defesa 10 | 1 | limite |
| crítico | ataque 20, defesa 10, crítico forçado | 20 | regra |
| arredondamento | ataque 15, defesa 10, multiplicador 0,5 | conforme a regra de arredondamento do GDD | decisão |
| aleatoriedade | semente fixa 42, 1000 golpes | taxa de crítico dentro da tolerância do GDD | estatístico |

Princípios: oráculo independente da implementação (valor escrito à mão, não calculado pela mesma função); semente fixa para aleatoriedade; um teste por regra, nome descritivo; o bug vira teste antes do conserto. Teste que só verifica "a função foi chamada" não protege a regra (brain `testes-e-debugging`).

GDScript com GUT, esqueleto (o projeto deve ter adotado GUT; V-12):

```gdscript
extends GutTest

func test_dano_no_limiar_e_zero() -> void:
	assert_eq(Combat.compute_damage(10, 10), 0)

func test_dano_acima_do_limiar() -> void:
	assert_eq(Combat.compute_damage(11, 10), 1)
```

`Combat.compute_damage` é um nome ilustrativo; adapte à API real do projeto e confirme a sintaxe de asserção na versão do GUT instalada. No Unity, o equivalente é um teste NUnit em EditMode (Unity Test Framework 1.4.6, V-21).

## Smoke

Passos curtos que respondem "o build vive". Cada um com resultado esperado:

1. Abrir o build -> menu principal aparece sem erro no log.
2. Novo jogo -> cena principal carrega em tempo razoável (limite do projeto; sem orçamento, NÃO AVALIADO).
3. Mover, pular e atacar por 30 s -> sem crash nem softlock.
4. Salvar, sair, carregar -> estado igual (posição, itens).
5. Abrir opções, remapear uma tecla, voltar -> tecla nova funciona.
6. Sair -> processo encerra, sem processo fantasma.

Execução por humano ou por script de sonda (`game-verify-by-running`); o resultado entra no relatório com evidência.

## Plano de playtest preenchido

```markdown
# Plano de playtest: nível 1 (build a1b2c3d)
Objetivo: descobrir onde jogadores novos se perdem.
Hipótese: 8 em 10 encontram a saída em até 2 minutos sem dica.   (a razão 8/10 é ilustrativa)
Público: pessoas que nunca viram o jogo; perfil de jogo de plataforma casual.
Método: presencial, moderado; moderador M1, anotador A1.
Roteiro: briefing de 1 min (sem explicar controles); sessão de 15 min; entrevista de 5 min.
Avisos e consentimento: gravação de tela e voz, uso interno, pode parar a qualquer momento.
Dados: tempo até a saída, mortes por área, onde pausa/abandona (eventos: level_start, death, exit_reached).
Critério de leitura: comparar o que a pessoa diz com o que faz.
Fora do escopo: balanceamento fino de dano.
```

Quantidade de jogadores: decisão do usuário. O número "5 a 8 por sessão" aparece no FAQ do IXDF e é referência comercial; Meta e Level Design Book não trazem cifra (V-28).

## Relatório de playtest preenchido

```markdown
# Relatório de playtest: nível 1 (build a1b2c3d)
Sessão: 4 participantes (P1 a P4), foco no início do nível. Hipótese: ver plano.
Primeiras impressões: P1 "claro"; P2 "perdido na sala 3"; ...
## Bugs
| # | Tipo | Passos | Frequência | Evidência |
| B1 | softlock | sala 3, empurrar caixa na porta | 2/4 | clipe P2, log linha 880 |
## Pain points (sensação, sem defeito)
- Salto parece "pesado" (P1, P3). Rotear: design.
- Não fica claro que a alavanca é interativa (P2, P4). Rotear: polish.
## Dados
- Tempo até a saída: P1 1m40, P2 sem concluir, ... (coletado por log). Taxa de vitória: 3/4.
- Telemetria de mortes: NÃO AVALIADO (evento não implementado).
## Roteamento
| Item | Destino | Próximo passo | Dono |
## Pilares
- "Leitura clara": parcialmente atendido (ver pain point 2).
```

Regras do relatório: bug exige passos e evidência; pain point é opinião de jogador, registrada com quantos relataram; nunca transforme "gostei" em dado quantitativo; dado faltante vira "não avaliado".

## Charter exploratório

Sessão de busca livre por risco, com missão (brain-of-agent QA `charter-exploratorio`, texto próprio adaptado):

```markdown
Explorar: save/load durante troca de cena
Com: save no meio do dash, no menu de pausa, e em transição de nível
Para descobrir: perda de estado ou softlock
Tempo: 30 min   Build: a1b2c3d
Oráculos: GDD seção "persistência"; saída do log
Achados: [bugs com evidência, dúvidas, ideias] separados
Cobertura efetiva: [o que foi exercitado]
Não exercitado / risco residual: [o que ficou de fora]
```

## Fontes

- V-26: tipos de teste (Donchitos/Claude-Code-Game-Studios, classe B, MIT; padrão destilado).
- V-28: playtest (Level Design Book, Meta, IXDF; classe B; sem texto copiado).
- V-12: GUT (MIT) e limites do headless; V-21: Unity Test Framework.
- Brain-of-agent do usuário (MIT): `bug-report.md`, `charter-exploratorio.md`, `testes-e-debugging.md`.
