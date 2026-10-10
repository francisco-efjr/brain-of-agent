# Reproduzir e minimizar

Apoio da skill `bug-report`. Leia quando precisar construir o loop de feedback, reduzir um defeito ao caso mínimo, usar `curl` para descer de camada, localizar o commit com `git bisect` sem riscos ou registrar um defeito intermitente.

Base: loop de feedback e fases 1 e 2 do diagnóstico de V-34 (Matt Pocock, MIT, destilado); Mozilla Bug Writing Guidelines (V-27: caso mínimo, build novo, frequência); conteúdo próprio do brain-of-agent (MIT) sobre isolamento, `curl` e bisect, com redação revisada. Comandos de Git e curl são estáveis; confirme flags com `--help`. Itens não lidos em fonte externa estão marcados Inferido.

## Sumário

- [Loop de feedback primeiro](#loop-de-feedback-primeiro)
- [Reduzir até o mínimo](#reduzir-até-o-mínimo)
- [Descer de camada com curl](#descer-de-camada-com-curl)
- [Hipóteses falsificáveis](#hipóteses-falsificáveis)
- [git bisect com salvaguardas](#git-bisect-com-salvaguardas)
- [Defeito intermitente](#defeito-intermitente)
- [Limites desta skill](#limites-desta-skill)

## Loop de feedback primeiro

Antes de teorizar sobre a causa, construa um comando que reproduz o sintoma de forma rápida, determinística e que **falha** quando o defeito está presente (V-34, Verificado). Opções, da mais barata à mais cara:

1. Teste automatizado que falha (unitário ou de integração) com os dados do relato.
2. Script de uma linha (`python -c`, `node -e`) chamando a função suspeita.
3. `curl` contra servidor de desenvolvimento ou staging.
4. Navegador controlado (Playwright) com o passo a passo mínimo.

Critério de saída: você roda o loop duas vezes seguidas e obtém o mesmo vermelho, em segundos. Se o defeito é intermitente, o "loop" é uma repetição com contagem (seção abaixo). Sem loop, o relatório diz "não reproduzido" e lista o que foi tentado; não conclui causa.

## Reduzir até o mínimo

1. **Corte passos.** Tire um passo por vez e veja se o defeito continua. O que sobra é o caminho necessário.
2. **Isole a variável.** Mude uma condição por vez e registre. A coluna "reproduz?" é o dado mais útil ao desenvolvedor:

| Variação | Reproduz? |
| --- | --- |
| Subtotal R$ 250,00, frete grátis | sim (5/5) |
| Subtotal R$ 150,00, frete pago | não (0/5) |
| Subtotal exato R$ 199,00 (limite do frete grátis) | sim (3/3) |
| Cupom percentual (`VOLTA15`) | sim |
| Cupom de valor fixo (`MENOS20`) | não |
| Firefox e app Android | sim (não depende do cliente) |

A tabela já aponta onde olhar: desconto percentual combinado com frete grátis, no servidor.

3. **Troque a configuração** uma vez: perfil/usuário novo, navegador limpo, build mais novo (V-27: testar build mais novo e perfil novo antes de relatar).
4. **Janela de regressão:** se existe uma versão boa conhecida, registre a última versão que funcionava e a primeira que falha (V-27); `git bisect` automatiza isso.
5. **Procure o dado que dispara:** o menor valor, a menor lista, o menor payload que ainda reproduz.

## Descer de camada com curl

Se o defeito passa por API, reproduza com `curl` e tire a interface da equação. Exemplo (variáveis de ambiente de teste; token de teste, nunca real; `jq` opcional):

```bash
curl -s -X POST "$BASE_URL/api/checkout/totais" \
  -H "Authorization: Bearer $TOKEN_QA" -H "Content-Type: application/json" \
  -d '{"itens":[{"sku":"FONE-XZ","qtd":1}],"cep":"01310-100","cupom":"PRIMEIRA10"}' \
  | jq '{subtotal, desconto, frete, total}'
```

Registre no relatório o comando com o token substituído por `<TOKEN>`. No PowerShell use `curl.exe` (o alias `curl` chama `Invoke-WebRequest`). Copie o `request id` do cabeçalho da resposta: é o elo mais barato entre o relato e o log do servidor.

## Hipóteses falsificáveis

Depois de ter o loop (V-34, fase 3 de 6, Verificado), liste 3 a 5 hipóteses ranqueadas, cada uma com uma **previsão** que a refuta: "se a causa for o arredondamento por item, o total de 3 itens de R$ 0,10 com 10% de desconto deve diferir do total do pedido inteiro". Teste uma hipótese por vez, alterando uma variável por rodada. Instrumentação (logs com prefixo único, depuração) é permitida só em ambiente de desenvolvimento ou teste confirmado com o usuário, e é removida no fim; instrumentar produção exige autorização. Registre a hipótese correta e as descartadas.

Agentes costumam errar ao explicar quando um bug entrou; exigir que a hipótese seja testada executando código removeu a maioria dos erros no relato de V-29 (anedótico). Rotule qualquer hipótese não testada como Suposição.

## git bisect com salvaguardas

Use quando há um commit bom e um ruim e um teste que reproduz o defeito. O Git faz busca binária: cerca de 10 passos para 1.000 commits (conta de log2).

Riscos e salvaguardas:

1. `git bisect` muda o checkout. Árvore de trabalho com alterações não commitadas atrapalha. Prefira um **worktree** separado:

```bash
git worktree add "$TMPDIR/bisect" HEAD     # cópia limpa
cd "$TMPDIR/bisect"
git bisect start
git bisect bad                             # o commit atual tem o defeito
git bisect good v3.7.0                     # última release em que funcionava (confira com git tag)
git bisect run sh -c 'npm ci --silent || exit 125; npx vitest run cupom-frete'
git bisect reset                           # volta ao ponto de partida
cd - && git worktree remove --force "$TMPDIR/bisect"
```

2. Código de saída do comando de `run`: 0 = commit bom; 125 = não dá para testar (o Git pula o commit); 1 a 127 exceto 125 = commit ruim. Confirme na documentação do Git instalado.
3. O teste reprodutor deve ficar **fora do controle de versão** (arquivo não rastreado) para sobreviver aos checkouts; no worktree, copie-o para dentro.
4. `npm ci` ou instalações por commit executam scripts do projeto (`postinstall`): só em repositório confiável e ambiente descartável.
5. Peça confirmação ao usuário antes de iniciar (gate da skill): o comando roda código de vários commits.
6. Registre no relatório o commit encontrado e o comando usado; o commit culpado é pista, não veredito de causa.

## Defeito intermitente

Intermitente não é "não reproduz": é um defeito com frequência abaixo de 100%, e frequência é dado.

- **Frequência medida:** "falhou 3 de 20 tentativas". Para repetir de forma controlada use um laço (`for i in $(seq 1 20); do <comando-que-reproduz> || echo "falha $i"; done`).
- **Condições de cada ocorrência:** horário em UTC, usuário, dados, instância ou pod, carga, rede, outra aba aberta.
- **Timestamp e correlation id** de cada falha: acham a linha certa entre milhões de linhas de log.
- **O que as falhas têm em comum e as passagens não.** Se todas ocorreram com duas abas abertas, o próximo passo é testar isso de propósito.
- **Hipóteses por categoria:** tempo, concorrência, dados, ambiente, ordem (taxonomia completa na skill `flaky-triage` quando o intermitente é um teste automatizado).

## Limites desta skill

- Esta skill não corrige o produto. Quando a redução aponta o módulo e a condição, entregue o relatório com a tabela de isolamento e indique o handoff ao segmento de qualidade de código.
- Não fuzze, estresse nem mutile código para forçar falha sem delimitar o ambiente-alvo e sem autorização (V-34 sugere essas técnicas sem limites; este plugin exige confirmação).
- Nunca cole segredos: substitua tokens, cookies e dados pessoais por `<REDACTED>` antes de qualquer registro.
