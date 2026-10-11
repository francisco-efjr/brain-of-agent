# Notas

## Arquivos da skill lidos
- skills/qa/SKILL.md (inteiro)
- skills/qa/references/design-de-testes.md (seção "Pairwise e combinatório", linhas 180-229)
- skills/qa/scripts/pairwise.py (inteiro) e executado: `--self-test` (OK) e geração da matriz com exclusões
- skills/qa/references/estrategia.md (linhas 1-160: perguntas de contexto, análise de risco)
- skills/qa/references/automacao-web.md (linhas 36-47 e 666-690: WebKit do Playwright vs Safari, matriz de navegadores, ritmo PR/noturno/release)
- skills/qa/references/dominios.md (linhas 166-206: SaaS multi-tenant, linha de SSO e downgrade)

Não li: mobile.md, seguranca.md, templates (grep apenas para localizar trechos relevantes).

## Execução local
- `pairwise.py` com 5 parâmetros e exclusões (SSO só Enterprise; Safari só macOS/iOS): 17 casos, 111/111 pares possíveis cobertos.
- Conferência independente (script em scratchpad) por força bruta: 294 combinações válidas, 111 pares possíveis, nenhum descoberto; 42 triplas navegador×SO×login possíveis, 17 cobertas.
- Variante com Chrome/Firefox/Edge no iOS excluídos também deu 17 casos (não ajudou a reduzir; não mencionei no texto).

## Incertezas
- Safari só em macOS/iOS é suposição minha (estado atual do mercado), declarada na resposta.
- As 3 linhas extras (E1 a E3) são julgamento meu, não saída do gerador; idioma/plano delas são preenchimento.
- Afirmação "no Brasil todo navegador de iOS usa WebKit" vem de automacao-web.md; não verifiquei fora da skill.
- Código HTTP 403 na tabela de decisão é ponto de partida (a resposta diz "ou o código do seu contrato").
- Não sei se Enterprise com SSO obrigatório ainda aceita senha, nem se há mais de um IdP: listei como perguntas.
- Não estimei esforço em horas por falta de dado sobre a jornada crítica.
