# Relatório de auditoria de vazamento

Escopo: [código/notebook/SQL auditado]. Modo: somente leitura. Rótulos: Verificado (lido em arquivo:linha), Inferido, Não verificável. Fontes: V-12, V-13.

- **Instante da decisão:** [..]  **Instante do rótulo:** [..]
- Tabela de disponibilidade: ver `tabela-disponibilidade-features.md`

## Achados
Formato: `[blocker/high/medium] título | classe | arquivo:linha | frase de ordem temporal | direção do viés | correção`.
Achado sem frase de ordem temporal vira **"high + pergunta"**, nunca blocker.

| ID | Sev | Título | Classe | arquivo:linha | Frase de ordem temporal | Viés (infla/deflaciona) | Correção |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L-01 | [sev] | [..] | [alvo / temporal / pré-processamento / grupo / duplicatas / derivado do futuro] | [..] | ["escrito em X; decisão em Y"] | [..] | [..] |

## Quatro checagens de split
| Checagem | Passa/Falha | Evidência (arquivo:linha) |
| --- | --- | --- |
| Pré-processamento (`fit`) só no treino, dentro de Pipeline/fold | [..] | [..] |
| Grupo/entidade: nenhuma entidade em treino e teste | [..] | [..] |
| Tempo: treino anterior ao teste | [..] | [..] |
| Teste intocado: sem uso em escolha de modelo, limiar ou hiperparâmetro | [..] | [..] |

## Evidência empírica (só corrobora)
[ablação da feature suspeita, concentração de importância, queda no hold-out temporal] -> resultado e limite da interpretação.

## Não verificado
[arquivos sem acesso, execuções não feitas]

## Próximo passo
[correção prioritária e como verificar (comando)]
