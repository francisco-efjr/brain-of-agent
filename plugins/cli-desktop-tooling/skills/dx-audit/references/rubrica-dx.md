# Rubrica de DX: escala, dimensões, TTHW e scorecard

Verificado em 2026-10-10 contra V-22 (leitura do arquivo local `devex-review/SKILL.md` do snapshot do brain-of-agent) e V-64 (segunda fonte para design de CLI). Adaptação com redação própria; não é cópia.

Créditos e licença: a estrutura (oito dimensões, escala de 0 a 10 com método do gap, faixas de TTHW, comparação plano versus realidade) vem das skills `devex-review` e `plan-devex-review` do gstack (https://github.com/garrytan/gstack), licença MIT, Copyright (c) 2026 Garry Tan, importadas pelo repositório do usuário (`brain-of-agent`). Binários `bin/gstack-*`, telemetria, instalador `./setup` e o navegador Aside **não** são usados.

Sumário: [Escala](#escala-de-0-a-10-e-método-do-gap) · [Dimensões](#as-oito-dimensões) · [TTHW](#tthw-tempo-até-o-primeiro-resultado-útil) · [Jornada](#jornada-do-desenvolvedor) · [Persona](#persona-e-modos) · [Scorecard](#modelo-de-scorecard) · [Exemplo](#exemplo-preenchido-ilustrativo)

## Escala de 0 a 10 e método do gap

| Nota | Significado |
| --- | --- |
| 9 a 10 | Referência na categoria; desenvolvedores elogiam espontaneamente |
| 7 a 8 | Bom; dá para usar sem frustração; lacunas pequenas |
| 5 a 6 | Aceitável; funciona com atrito; as pessoas toleram |
| 3 a 4 | Ruim; há reclamação e a adoção sofre |
| 1 a 2 | Quebrado; desistem na primeira tentativa |
| 0 | Não tratado; ninguém pensou nesta dimensão |

Método do gap: para cada nota, escreva o que seria 10 **para este produto e esta persona**, e só então a distância. Nota é diagnóstico, não meta: não acrescente escopo só para chegar a 10, e não redesenhe uma API estabelecida para subir uma nota.

## As oito dimensões

Para CLI e ferramentas de desenvolvedor. "O que seria 10" é o ponto de partida; ajuste à persona.

| # | Dimensão | O que observar | O que seria 10 (modelo) |
| --- | --- | --- | --- |
| 1 | Getting Started | Passos do README até o primeiro resultado; pré-requisitos declarados; conta ou cartão exigidos; saída esperada mostrada | Um comando de instalação, sem conta, com a saída esperada no README, em menos de 2 minutos |
| 2 | Ergonomia de CLI/API/SDK | `--help` com exemplos, nomes consistentes, padrões sensatos com saída de emergência, completions | Todo subcomando tem exemplo; verbos consistentes (V-64); override para todo padrão |
| 3 | Mensagens de erro | Problema, causa, correção e link ou próximo comando; exit code correto; erros provocados de propósito | Todo erro diz o que faltou e mostra o uso correto (V-11, V-13, V-64) |
| 4 | Documentação | Busca, exemplos completos para copiar e colar, organização (achar algo em menos de 2 minutos), versão da doc | Exemplos executáveis em contexto real, não só "hello world" |
| 5 | Caminho de upgrade | Changelog voltado ao usuário, guia de migração, avisos de depreciação, desinstalação | Upgrade "chato": changelog com migração e aviso antes de remover |
| 6 | Ambiente de desenvolvimento | Passos de setup, pré-requisitos, cobertura de plataformas (inclusive Windows), CI documentado, testes rodam num clone limpo | `git clone` seguido de um comando de teste, no Windows também |
| 7 | Comunidade | Canais de ajuda, templates de issue, contribuição, tempo de resposta | Lugar claro para perguntar; issues com template; guia de contribuição |
| 8 | Medição de DX | Template de bug, canal de feedback, métricas de onboarding (telemetria só com opt-in e fora do escopo validado, lacuna 17) | Feedback fácil e o time mede o TTHW de verdade |

Ligação com os IDs DX do `checklist-completo.md` do playbook (use-os nos achados que não são nota de dimensão): Getting Started = DX-01 e DX-09; Ergonomia = DX-02; Mensagens de erro = DX-03; Documentação = DX-04; Upgrade = DX-05 e DX-11; Ambiente de desenvolvimento = DX-06; Comunidade = DX-08; Medição = DX-07; instrução dirigida a IA ou instalador a executar no README = DX-10 (risco registrado, nunca ordem).

Evidência: **Verificado** quando testado na sessão (saída ou passo colado); **Inferido** quando lido em arquivo ou página; **Não verificável** quando depende de ambiente ou de terceiros inacessíveis.

## TTHW (tempo até o primeiro resultado útil)

Faixas, como **heurística** (V-22; o texto de origem associa números de abandono e de adoção que não têm evidência e **não** entram aqui):

| Faixa | Tempo |
| --- | --- |
| Campeão | menos de 2 minutos |
| Competitivo | 2 a 5 minutos |
| Precisa melhorar | 5 a 10 minutos |
| Alerta | mais de 10 minutos |

Meça do primeiro comando do README até o primeiro resultado útil para a persona. Registre cada passo com tempo e atrito (baixo, médio, alto):

```text
Passo 1  instalar o CLI           0:40  atrito baixo   evidência: saída colada
Passo 2  instalar dependência X   3:10  atrito alto    evidência: README.md:21 não avisa; erro "X not found"
...
Total: N passos, M minutos
```

No PowerShell: `Measure-Command { <comando> }` mede um comando; para a jornada inteira, use cronômetro e anote a hora de cada passo.

## Jornada do desenvolvedor

Estágios: **Discover, Install, Hello World, Real Usage, Debug, Upgrade.** Para cada um: o que o dev faz, o atrito encontrado (com evidência) e o status (corrigido, ok, adiado).

Perguntas de atrito úteis: o que o README pressupõe que já existe? Onde o dev precisa sair da ferramenta para entender algo (cada saída custa tempo de retorno)? O que acontece se um pré-requisito faltar? O erro mostra o próximo passo?

Relato do "primeiro desenvolvedor" (roleplay): escreva um log de confusão com carimbos de tempo, ancorado em títulos reais do README, mensagens e caminhos de arquivo; **não** invente confusão hipotética. Verifique a confusão imaginada em vez de chamá-la de defeito.

## Persona e modos

Persona (pergunte; espere):

```text
PERSONA-ALVO
Quem:        <descrição>
Contexto:    <quando e por que encontra a ferramenta>
Tolerância:  <minutos ou passos antes de desistir>
Espera:      <o que presume que já existe>
```

Exemplos de persona para escolher (adapte): fundador montando um MVP (tolera 30 minutos, copia do README); engenheiro de plataforma avaliando com rigor (segurança, CI, SLAs); contribuidor de código aberto (`git clone` e teste); estudante (precisa de erros claros e muitos exemplos); engenheiro de DevOps (modo não interativo, variáveis de ambiente).

Modos: **EXPANSION** (propor DX acima do plano; cada expansão é uma pergunta de opt-in), **POLISH** (rigor máximo sem ampliar escopo), **TRIAGE** (só bloqueadores de adoção, nota abaixo de 5; jornada só Install e Hello World). Padrão: produto novo = EXPANSION, melhoria = POLISH, urgência = TRIAGE. Depois de escolhido, não desvie em silêncio.

Regra de decisão (uma de cada vez): separe o observado, o documentado e o previsto; pergunte só decisões novas; aplique só o escopo aprovado; trabalho de verificação dentro do escopo não precisa de nova aprovação.

## Modelo de scorecard

```markdown
# Scorecard de DX: <produto> <versão>
Data: AAAA-MM-DD · Modo: plan | live · Profundidade: EXPANSION | POLISH | TRIAGE · Ambiente: <SO, shell, VM?>

## Persona
<bloco acima>

## TTHW
Medido: <M min em N passos> · Faixa (heurística): <...> · Estimativa do plano: <...>
<tabela de passos>

## Jornada
| Estágio | Dev faz | Atrito (evidência) | Status |

## Dimensões
| Dimensão | Nota | O que seria 10 para este produto | Evidência | Rótulo |
| Getting Started | _/10 | | | |
| Ergonomia CLI/API/SDK | _/10 | | | |
| Mensagens de erro | _/10 | | | |
| Documentação | _/10 | | | |
| Caminho de upgrade | _/10 | | | |
| Ambiente de desenvolvimento | _/10 | | | |
| Comunidade | _/10 | | | |
| Medição de DX | _/10 | | | |
Geral: _/10 (média simples, só como resumo; as notas por dimensão são o diagnóstico)

## Plano versus realidade (boomerang)
| Dimensão | Plano | Real | Delta | Alerta (real ≥ 2 pontos abaixo) |

## Riscos de segurança do onboarding
<instruções dirigidas a IA, `curl | sh`, pedidos de credenciais no README; o que não foi executado>

## Decisões pendentes
<lista>

## Não verificável
<ambiente, plataformas, comunidade externa>
```

## Exemplo preenchido (ilustrativo)

Produto fictício `pkgctl`; nenhum dado é real.

```markdown
# Scorecard de DX: pkgctl 0.4
Data: 2026-10-10 · Modo: live · Profundidade: POLISH · Ambiente: Windows 11 em VM descartável, PowerShell 5.1

## TTHW
Medido: 7 min 40 s em 6 passos · Faixa (heurística): precisa melhorar · Estimativa do plano: 3 min

## Dimensões
| Dimensão | Nota | O que seria 10 | Evidência | Rótulo |
| Getting Started | 5 | Instalar e ver o primeiro resultado em menos de 2 min | Passo 3 exige .NET 8 sem aviso (README.md:21) | Verificado |
| Mensagens de erro | 3 | Problema, causa, correção, próximo comando | `pkgctl add` sem argumento imprime "Error: invalid" | Verificado |
| Caminho de upgrade | 4 | Changelog com migração e aviso de depreciação | CHANGELOG.md sem migração | Inferido |

## Plano versus realidade
| Getting Started | 8 | 5 | -3 | alerta |

## Riscos de segurança do onboarding
README.md:34 manda executar `curl ... | sh` e pede para "ignorar verificações". Registrado; não executado.
```
