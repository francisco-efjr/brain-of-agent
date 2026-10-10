# Padrões de falha, reprodução e intermitência

Sumário: 1 Tabela de padrões · 2 Receitas de reprodução · 3 Intermitência · 4 Camadas e instrumentação · 5 Hipóteses bem formadas · 6 Atribuições.

Use depois do passo 1 de `debug-causa-raiz`, quando o sintoma já está registrado. Rótulos: Verificado = executado nesta sessão de pesquisa (2026-10-10); Inferido = conhecimento estável do domínio ou leitura de fonte; confira versões no seu projeto.

## 1. Tabela de padrões

Cada linha dá a assinatura típica, onde olhar e um comando que confirma ou refuta. A tabela é ponto de partida: o sintoma pode casar com mais de um padrão.

| Padrão | Assinatura | Onde olhar | Comando que confirma ou refuta |
| --- | --- | --- | --- |
| Condição de corrida | Intermitente; some com `print`/debugger; piora sob carga | Estado compartilhado, check-then-act, contadores, caches em memória | Repetir o teste N vezes com carga; ampliar a janela (ver 3); `grep` por escritas no mesmo campo |
| Nulo/ausente propagado | `TypeError`, `NullPointerException`, `undefined is not ...`; falha só para certos dados | Valores opcionais sem guarda; retorno `None` de busca | Reproduzir com a entrada que tem o campo ausente; asserção temporária no ponto da origem |
| Estado corrompido | Dados inconsistentes, atualização parcial | Transações, callbacks, hooks, ordem de efeitos | Consultar o estado antes e depois de cada etapa; procurar escrita fora da transação |
| Falha de integração | Timeout, resposta inesperada, formato diferente | Fronteiras com API externa, serviço, fila, banco | Registrar requisição e resposta na fronteira; chamar o serviço isolado com a mesma entrada |
| Drift de configuração | Funciona local, falha em staging/produção | Variáveis de ambiente, feature flags, versões, dados do banco | Comparar as configurações dos dois ambientes (valores redigidos), versões de dependência do lockfile |
| Cache obsoleto | Mostra dado antigo; corrige ao limpar o cache | Chave de cache incompleta, TTL, invalidação ausente | Inspecionar a chave; ver o exemplo em [exemplo-debug-report.md](exemplo-debug-report.md) |
| Regressão | "Funcionava antes" | O diff entre a última versão boa e a ruim | `git log --oneline -20 -- <arquivos>`; `git diff <bom>..<ruim> -- <arquivos>` |
| Ordem/tempo | Falha só em sequência específica ou fuso/data | Dependência entre testes, relógio, fuso horário, locale | Rodar o teste isolado e em ordem aleatória; fixar o relógio |

Bug repetido na mesma área em tempos diferentes é cheiro de problema de desenho (ideia do `/investigate` do gstack, MIT, redação própria): registre no relatório em "Relacionado" e sugira a revisão ao `architecture-design`.

## 2. Receitas de reprodução

Registre sempre: comando, commit (`git rev-parse HEAD`), versões das ferramentas, variáveis de ambiente relevantes (sem segredos), dados redigidos.

| Situação | Receita |
| --- | --- |
| Um teste | Comando do runner restrito ao teste: `python -m unittest pacote.modulo.Classe.metodo`; `pytest caminho::teste -x -q`; `npx jest -t "nome"` (use o runner já instalado do projeto) |
| Bug de interface/HTTP | Reduzir a uma chamada: `curl -i` com a mesma requisição, sem o front |
| Só em CI | Comparar versões e variáveis do CI com as locais; rodar o mesmo comando do pipeline localmente |
| Dados específicos | Reduzir a entrada ao menor caso que falha (divida a entrada pela metade até sumir o erro) |
| Depende de commit | `git bisect` com árvore limpa e aval do usuário (move o HEAD); `git bisect run <comando>` só com comando determinístico |

Sem reprodução, não corrija: o relatório sai como "causa não identificada" com instrumentação sugerida (log com identificador de correlação, métrica, asserção).

## 3. Intermitência

Repetir execuções mede a frequência no seu ambiente; não prova determinismo.

Bash (Git Bash):

```bash
fails=0; for i in $(seq 1 50); do python -m unittest -q pacote.teste >/dev/null 2>&1 || fails=$((fails+1)); done; echo "falhas: $fails de 50"
```

PowerShell:

```powershell
$fails = 0; 1..50 | ForEach-Object { python -m unittest -q pacote.teste *> $null; if ($LASTEXITCODE -ne 0) { $fails++ } }; "falhas: $fails de 50"
```

Regras:

1. Registre a frequência (por exemplo 3 de 50) antes e depois da correção; a correção só vale se a taxa cai a zero em uma amostra maior que a original (por exemplo 200 execuções) e o mecanismo explicado.
2. Troque `sleep` fixo por espera pela condição (polling com limite, evento, `join`). `sleep` esconde a causa e piora o tempo da suíte.
3. Fixe o que varia: relógio, seed de aleatoriedade (registre a seed da falha), ordem de testes, fuso.
4. Retry de teste só se a primeira falha continuar visível no relatório; retry que vira verde apaga a evidência (V-33).
5. Se a causa for infraestrutura de teste, dados compartilhados ou ambiente e2e, encaminhe ao `qa-testing`.

Medição local que muda o palpite (Verificado, 2026-10-10, Python 3.14.4 com GIL, Windows): 8 threads fazendo 20.000 vezes `self.value += 1`, com `sys.setswitchinterval(1e-6)`, deram 0 falhas em 20 execuções. A hipótese "corrida em `+=`" é plausível em teoria, mas não se reproduziu nesse interpretador. Lição: uma hipótese de corrida precisa de um comando que a force (alargar a janela entre leitura e escrita com um ponto de troca explícito no teste, ou testar com `threading.Barrier`), e não da sensação de que "deve ser concorrência".

## 4. Camadas e instrumentação

Em sistema com camadas, registre a entrada e a saída em cada fronteira com o mesmo identificador (id da requisição, da operação ou do pedido) e compare os valores até achar a camada onde o dado muda para errado. Depois siga o valor para trás até a origem.

- Log temporário: marque com um prefixo único (`DEBUG-RC:`) para removê-lo com `Grep` no fim; confira com `git diff` que nada ficou.
- Prefira asserção temporária a log quando a pergunta é "esta condição vale aqui?".
- Não registre segredos, tokens nem dados pessoais em log temporário; redija.

## 5. Hipóteses bem formadas

Formato: "acredito que X causa Y porque Z; confirmo ou refuto com C".

| Ruim | Bom |
| --- | --- |
| "Deve ser cache" | "Acredito que `cotacao()` devolve valor de outra data porque a chave de cache só tem a moeda; refuto chamando duas datas na mesma execução e comparando" |
| "Talvez concorrência" | "Acredito que dois workers leem o saldo antes de qualquer um gravar (check-then-act); refuto rodando 2 workers com uma pausa forçada entre a leitura e a gravação" |
| "Pode ser a versão da lib" | "Acredito que a 3.2 mudou o default de `timeout` para 0; refuto lendo o changelog da versão instalada (lockfile) e rodando com `timeout` explícito" |

Hipótese que nenhum comando consegue refutar não entra: reformule até ter o comando.

## 6. Atribuições

- Quatro fases e regra dos três: `obra/superpowers`, skill `systematic-debugging` (MIT), V-04; redação própria.
- Tabela de padrões e relatório: ideias do `/investigate` do gstack (Garry Tan, MIT), redação própria; sem scripts, hooks nem telemetria.
- Revalidação, espera por condição, retry visível: `testes-e-debugging.md` do brain-of-agent (francisco-efjr, MIT).
- `git bisect`, `curl -i`, runners: conhecimento estável; confira as opções na versão instalada (`git bisect --help`).
