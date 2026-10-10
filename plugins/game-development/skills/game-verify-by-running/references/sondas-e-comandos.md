# Sondas, contrato de pronto e check curto

Sumário: [Contrato de pronto](#contrato-de-pronto) · [Sondas](#sondas) · [Sonda em Godot (exemplo)](#sonda-em-godot-exemplo) · [Check curto](#check-curto) · [features.json](#featuresjson) · [Relatório preenchido](#relatório-preenchido)

Rótulos: Verificado = visto na documentação oficial ou em execução; Inferido = leitura ou conhecimento estável a conferir na versão; Suposição; Não verificável. Fontes: V-01, V-04, V-05, V-10, V-12, V-30 do `VALIDATED.md`. O código abaixo é redação própria (licença MIT do plugin) e não foi executado pelo autor do plugin: rode-o no projeto do usuário e leia a saída real.

## Contrato de pronto

Escreva antes de codar. Cada linha precisa de um comando, log ou captura que a prove.

```markdown
# Contrato: [funcionalidade]   Build/commit: [hash]   Engine: [nome + versão]
## Comportamentos (limiar mínimo; abaixo reprova)
1. [ação] produz [valor/estado observável] -> evidência: [linha de log | valor da sonda | contagem de nós]
2. [caso de borda] -> [resultado esperado]
## Regressão
- [comportamento antigo que segue igual] -> evidência: [mesmo check de antes]
## Orçamento (se relevante)
- [sistema] <= [N] ms/quadro no perfil [cena] em [hardware]; sem orçamento no projeto = NÃO AVALIADO
## Humano (NÃO AVALIADO pelo agente)
- sensação de [controle/impacto], áudio, legibilidade do feedback visual
## Fora do escopo
- [o que não será tocado]
```

Regras: limiar numérico quando houver número (ex.: "10 inimigos", "stamina cai 25"); "funciona bem" não é critério. Reduzir critério depois para a falha passar é proibido; se o critério estava errado, diga e peça decisão.

## Sondas

Sondas são flags do próprio jogo que permitem testar sem humano (caso Amiga para Godot, V-30; classe B, relato de praticante). Proponha como tarefa pequena e aprovada, antes de mecânicas novas.

| Flag | Efeito | Saída esperada |
| --- | --- | --- |
| `--level=<id ou cena>` | carrega direto a cena de teste | `PROBE level=<id> loaded` |
| `--drive=<arquivo>` | reproduz um script de input (ação, quadro) | `PROBE drive done frames=<n>` |
| `--probe` | imprime estado interno em texto e encerra | `PROBE key=value ...` (uma linha por consulta) |
| `--screenshot=<arquivo>` | salva captura do viewport (precisa de janela, não de `--headless`) | `PROBE screenshot=<arquivo>` |

Duas verificações headless fixas (V-30): compilar todos os scripts e carregar todos os níveis, relatando falhas. Com referência (build antigo, captura aprovada, saída esperada), compare em vez de olhar; sem referência (jogo novo), só há sondas. Registre constantes ajustadas à mão para sensação.

Convenção de log: prefixo fixo para busca (`PROBE`), erros como `ERROR[probe]`, valores em `chave=valor`. O agente lê com Grep; o humano lê o arquivo de log.

## Sonda em Godot (exemplo)

Autoload `Probe` (Godot 4.x). Argumentos do jogo vão depois de `--` na linha de comando; `OS.get_cmdline_user_args()` os devolve (Inferido: confirme na referência da sua versão).

```gdscript
# res://tools/probe.gd  (Projeto > Configurações > Autoload, nome "Probe")
extends Node

var _args: Dictionary = {}


func _ready() -> void:
	_args = _parse(OS.get_cmdline_user_args())
	if _args.has("level"):
		get_tree().change_scene_to_file.call_deferred(str(_args["level"]))
		await get_tree().process_frame
	if _args.has("probe"):
		for i in 3:
			await get_tree().physics_frame
		_report()


func _parse(raw: PackedStringArray) -> Dictionary:
	var out: Dictionary = {}
	for token in raw:
		if token.begins_with("--"):
			var kv := token.substr(2).split("=", true, 1)
			out[kv[0]] = kv[1] if kv.size() > 1 else "true"
	return out


func _report() -> void:
	var player := get_tree().get_first_node_in_group("player") as Node2D
	if player == null:
		print("ERROR[probe] grupo 'player' vazio")
		get_tree().quit(1)
		return
	print("PROBE player_pos=%s enemies=%d" % [player.global_position, get_tree().get_nodes_in_group("enemy").size()])
	get_tree().quit(0)
```

Uso: `godot --headless --path . -- --level=res://test/spawner_test.tscn --probe`. A troca de cena é diferida, por isso o `await` antes de consultar; se o nó ainda não existir, aumente os quadros de espera em vez de remover a checagem de `null`. O `as` devolve `null` em tipo incompatível, e a checagem trata isso (V-11). Sonda não substitui teste de lógica; ela dá ao agente um jeito de observar.

## Check curto

Desenho do comando `check` (V-10, analogia a jogos: Inferido). Exemplo de saída aceitável:

```
CHECK quick: import ok | scripts 41/41 ok | scenes 3/3 loaded | errors 0 | warnings 1
detalhe: build/check.log   falhas por sistema: grep "ERROR\[" build/check.log
```

Quando falha:

```
CHECK quick: scripts 41/41 ok | scenes 2/3 loaded | errors 2
ERROR[spawner] res://scenes/enemy.tscn: script ausente
ERROR[level] res://levels/l2.tscn: falha ao instanciar
detalhe: build/check.log
```

`--quick` roda uma amostra determinística de cenas (por exemplo, as 3 primeiras em ordem alfabética); `--full` roda todas. Detalhe longo vai para arquivo, nunca para o console do agente.

## features.json

Para projeto longo (V-04, artigo da Anthropic Engineering de 26/11/2025; transposição a jogos é Inferido). JSON, porque o modelo o sobrescreve menos que Markdown.

```json
{"id": "dash-01", "categoria": "gameplay",
 "descricao": "Dash consome stamina e respeita colisão com paredes",
 "passos": ["abrir a cena de teste", "acionar dash via sonda de input", "ler stamina e posição no log"],
 "passes": false}
```

Regras: só `passes` muda, e só depois de rodar os `passos`; nunca apagar nem editar passos; um item por sessão; início de sessão = `git log`, arquivo de progresso, primeiro `passes: false`, init (abre o jogo e roda o check), teste mínimo antes de codar; fim = commit descritivo (só se o usuário pedir) e progresso atualizado com o que ficou quebrado.

## Relatório preenchido

```markdown
# Verificação: spawner de inimigos (Godot 4.3, commit a1b2c3d)
Veredito: parcial. Lógica verificada; sensação NÃO AVALIADA.

| # | Contrato | Comando | Resultado | Evidência |
| --- | --- | --- | --- | --- |
| 1 | 10 inimigos após 1 s | `godot --headless --path . -- --level=res://test/spawner_test.tscn --probe` | passou | `PROBE enemies=10`, exit 0 |
| 2 | 11º spawn recusado | idem com `--drive=spawn11.txt` | passou | `spawn_cap` no log |
| 3 | Sem ERROR | `grep "ERROR\[" build/check.log` | passou | 0 linhas |
| 4 | Ritmo do spawn | - | NÃO AVALIADO | humano deve jogar |

Pendências humanas: ritmo, feedback visual do spawn, áudio.
Próximo passo: playtest curto na cena real; depois marcar `passes: true` em `spawn-01`.
```

Este exemplo mostra o formato; os números dependem da execução real e nunca devem ser copiados sem rodar.
