# Critérios por quadrante Diátaxis

Conteúdo: 1 classificador · 2 matriz entidade → quadrantes · 3 critérios e esqueletos · 4 mapa de cobertura · 5 onboarding · 6 migração · 7 antipadrões.

Origem: Diátaxis, de Daniele Procida (https://diataxis.fr/; README do repositório do autor declara CC BY-SA 4.0), destilado em redação própria (V-11, V-46); matriz, ordem de escrita e portões adaptados do `document-generate` do gstack (Garry Tan, MIT); camadas de onboarding de V-47 (estrutura apenas). Rótulo: Verificado nas fontes; adaptações para PT-BR são Suposição.

## 1. Classificador de duas perguntas

| O leitor está... | Aprendendo (estudo) | Aplicando (trabalho) |
| --- | --- | --- |
| **Agindo** | Tutorial | How-to |
| **Entendendo** | Explicação | Referência |

Um pedido como "documente o comando `sync`" costuma gerar dois ou três arquivos: referência das flags, how-to de uma tarefa comum, talvez explicação do modelo de sincronização. Pergunte "o que o leitor quer fazer depois de ler?" para decidir.

## 2. Matriz entidade → quadrantes (ponto de partida; adapte)

| Entidade | Tutorial | How-to | Referência | Explicação |
| --- | --- | --- | --- | --- |
| Funcionalidade com que o usuário interage | sim | sim | sim | talvez |
| Comando ou flag de CLI | talvez | sim | sim | não |
| Módulo interno ou arquitetura | não | não | sim | sim |
| Opção de configuração | não | sim | sim | não |
| Padrão de projeto ou filosofia | não | não | não | sim |
| Endpoint de API | talvez | sim | sim | não |
| Fluxo de várias etapas | sim | sim | não | talvez |

Plano de saída (formato): uma linha por entidade e, por quadrante, `novo`, `inline` (coberto dentro de outro arquivo) ou `não`.

## 3. Critérios e esqueletos

### Referência (consulta)

- Neutra e factual; espelha a estrutura do produto (mesma ordem de módulos, comandos, campos).
- Cobre 100% da superfície pública; cada item com tipo, padrão, restrições, erro possível.
- Exemplos curtos que ilustram sem instruir; sem "por quê" (link para a explicação).

```markdown
# Comando `sync`
Sincroniza a pasta local com o destino.

## Uso
`tool sync [opções] <origem> <destino>`

## Opções
| Opção | Tipo | Padrão | Descrição |
| --- | --- | --- | --- |

## Saída e códigos de retorno
## Exemplos
## Veja também (how-to e explicação)
```

### Explicação (compreensão)

- Responde "por quê" e "como isto se encaixa"; apresenta o problema antes da solução.
- Nomeia alternativas e trade-offs (o que ganhamos, o que pagamos); escopo delimitado.
- Sem passos nem comandos para executar. Título "Sobre X" ou "Por que X".

```markdown
# Por que o `sync` usa hashes e não datas
## O problema
## Como funciona (modelo mental)
## Alternativas consideradas e trade-offs
## Limites conhecidos
## Leitura relacionada (referência)
```

### How-to (aplicação)

- Orientado a objetivo; supõe que o leitor sabe o básico; só ações.
- Título diz o que resolve ("Sincronizar duas pastas sem apagar arquivos").
- Pode ramificar ("se X, faça A; se Y, faça B"); termina com verificação e, se a tarefa falha de modo previsível, solução de problemas.

```markdown
# Sincronizar duas pastas sem apagar arquivos
Pré-requisitos: ...
1. Faça X: `comando`
   Você deve ver: ...
2. ...
## Verificar
## Solução de problemas
## Veja também (referência)
```

### Tutorial (aprendizado)

- Mostra o destino no início ("ao final você terá..."); uma trilha, sem opções laterais.
- Primeiro resultado visível até o passo 3; cada passo termina com "o que você deve ver"; avisa erros comuns no passo onde ocorrem.
- Sem explicação no corpo: link. Confiável para qualquer leitor do nível declarado (teste de leitor limpo).

```markdown
# Seu primeiro sync em 10 minutos
O que você vai construir: ...  | O que você precisa: ...
## Passo 1: ...  (você deve ver: ...)
## Passo 2: ...
## O que você construiu (links para how-to, referência e explicação)
```

## 4. Mapa de cobertura (usado por `auditor-de-docs` e para o fim do trabalho)

| Item da superfície pública | Referência | How-to | Tutorial | Explicação | Classificação |
| --- | --- | --- | --- | --- | --- |
| `sync --dry-run` | sim | não | não | não | comum (só referência) |
| `sync --delete` | não | não | não | não | crítica (zero cobertura) |

Regra: zero cobertura = lacuna crítica; só referência = lacuna comum. O mapa informa; quem decide o que escrever é o usuário.

## 5. Onboarding (Suposição de adequação)

Camadas inspiradas no curso de contribuidores do Kubernetes (V-47, estrutura apenas; o texto do site tem termo de reuso ambíguo, então nada foi copiado): orientação (o que é e onde pedir ajuda) · fluxo de contribuição (issues, PRs, revisão) · ambiente reproduzível · testes · comunidade e canais · onde a documentação mora e como corrigi-la · visão da arquitetura. Para equipe: acrescente primeiro dia, acessos (sem credenciais no texto), contatos e primeira entrega. Cada camada: um passo verificável ("rode X e veja Y").

## 6. Guia de migração

How-to com: versões de origem e destino; pré-requisitos (backup, versão mínima); passos na ordem; como verificar; como reverter; tabela "o que mudou" com link para a entrada de quebra no CHANGELOG. Não decida o que conta como quebra: isso vem do contrato (`backend-api`) ou do changelog existente.

## 7. Antipadrões

| Antipadrão | Sinal | Correção |
| --- | --- | --- |
| How-to que ensina | Parágrafos de contexto antes dos passos | Mover para explicação e linkar |
| Tutorial que explica | "Isso funciona porque..." no meio dos passos | Uma frase de expectativa e link |
| Referência com opinião | "Recomendamos usar..." | Mover para how-to ou explicação |
| Explicação com passos | Lista numerada de comandos | Mover para how-to |
| Página-tudo | Título genérico como "Guia do X" | Dividir por quadrante, ligar por links |
| Documento órfão | Ninguém linka para ele | Ligar do README ou do índice |
