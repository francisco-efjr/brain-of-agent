# Protocolo de feature list para execução longa

Para trabalho que atravessa várias sessões (um agente implementando e verificando uma lista grande de funcionalidades). Base: "Effective harnesses for long-running agents" (Anthropic Engineering, 26/11/2025; V-06), destilado. **Exige sandbox e revisão humana.** Este plugin não implementa loop autônomo e não define teto de custo por você: defina um teto de iterações e de custo antes de começar (V-05) e pare ao atingi-lo. Autoverificação do mesmo agente não é validação independente (a fonte mostra um único agente verificando o próprio trabalho).

## Registro: `feature-list.json`

Cada item tem `id`, `category`, `description`, `steps[]` e `passes` (booleano, **começa falso**). JSON em vez de Markdown, porque o modelo o altera com menos acidentes (V-06). Modelo: `feature-list.json` nesta pasta.

## Regras

1. Altere **somente** o campo `passes`. Nunca remova nem edite `steps` ou `description`: a fonte chama de inaceitável remover ou editar testes. Se um passo está errado, peça decisão ao usuário.
2. Marque `passes: true` só após verificação **ponta a ponta como usuário** (navegador ou fluxo real), não só unitário ou `curl`, com a evidência registrada (comando e saída, ou screenshot) no arquivo de progresso.
3. Uma feature por sessão; deixe o repositório em estado limpo e funcional ao terminar.
4. Alerta nativo do navegador é invisível à automação com Puppeteer MCP (V-06): registre como limitação e peça verificação humana.

## Início de sessão (rotina)

`pwd` · log do git recente · arquivo de progresso (`progress.md`) · `feature-list.json` · `init.sh` (se existir; leia antes de executar) · E2E básico de sanidade para confirmar que o estado anterior ainda funciona. Se a sanidade falha, conserte isso antes de qualquer funcionalidade nova.

## Fim de sessão

Atualize `passes` apenas do item verificado; escreva no `progress.md` o que foi feito, a evidência, o que ficou pendente e o próximo passo; commit descritivo **somente se o usuário autorizou commits** (sem push).

## Riscos e salvaguardas

Execução autônoma sem sandbox pode quebrar a base (a fonte do loop Ralph, V-30, avisa que o autor pode "acordar com a base quebrada" e não traz aviso de sandbox). Use ambiente isolado, credenciais de teste, permissões mínimas, revisão humana dos diffs e interrupção ao primeiro sinal de enfraquecimento de teste (S-02).
