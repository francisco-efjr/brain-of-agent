# Plano de teste: <funcionalidade ou release>

Como usar: plano enxuto para apoiar decisões (2 a 4 páginas), inspirado em documentação de teste no estilo ISO/IEC/IEEE 29119-3 (norma não lida nesta pesquisa). Preencha o que muda uma decisão; seção sem efeito fica "N/A: motivo". Apague as instruções ao preencher. Como pensar risco, níveis e go/no-go: `references/estrategia-e-risco.md`. Adaptado do template do brain-of-agent (MIT).

| Campo | Valor |
| --- | --- |
| Versão do plano / data / autor(a) | <0.1 · AAAA-MM-DD · nome> |
| Status | <Rascunho / Em revisão / Aprovado> |
| Aprovadores | <PO, líder técnico, QA> |
| Referências | <épico, histórias, contrato de API, protótipo> |

## 1. Contexto e suposições

<O que muda e por quê; quem usa; pior efeito realista; prazo e o que é imóvel; como se publica e se desfaz. Liste suposições como "Supondo que…". 5 a 10 linhas.>

## 2. Escopo

**Em escopo:** <funcionalidades, plataformas, integrações, ligadas a IDs do backlog>

**Fora de escopo** (o trecho que mais evita mal-entendido):

| Item | Motivo | Risco residual |
| --- | --- | --- |
| <item> | <motivo> | <o que pode acontecer> |

## 3. Riscos do produto

<Use `tabela-de-riscos.md`: falha → efeito, P e I de 1 a 3, impacto máximo nunca abaixo de Médio, mitigação executável, evidência prevista. Inclua ao menos uma linha não funcional ou diga por que não.>

## 4. Abordagem por camada e técnica

| Nível / tipo | O que cobre | Técnica | Automação | Riscos | Responsável |
| --- | --- | --- | --- | --- | --- |
| <Unitário> | <regra> | <valor-limite, tabela de decisão> | <sim, todo PR> | <R1> | <dev> |

Regra: cada risco no nível mais barato que o prova; E2E só para o que depende da integração. **Exploratório:** <charters previstos com duração>. **Não funcional:** <meta mensurável e como medir>. **Liberação:** <flag, etapas, métricas e limiares de aborto definidos antes>.

## 5. Ambientes e dados

| Ambiente | Uso | Dependências (real/sandbox/simulado) | Observações |
| --- | --- | --- | --- |
| <CI / homologação> | <níveis> | <PSP virtualizado> | <banco descartável por execução> |

Dados: <origem sintética, como reiniciar; nenhum dado de produção sem autorização e anonimização>.

## 6. Critérios de entrada, saída, suspensão e retomada

- **Entrada:** <build com smoke verde; critérios de aceite com exemplos; acessos prontos>
- **Saída:** <riscos altos com mitigação e evidência ou aceite formal; nenhum crítico aberto; regressão crítica verde; metas não funcionais medidas>
- **Suspensão / retomada:** <quando parar porque continuar desperdiça esforço; o que precisa acontecer para retomar>

## 7. Cronograma, papéis e entregáveis

| Marco | Data | Depende de |
| --- | --- | --- |
| <análise de risco com dev e PO> | <data> | <histórias refinadas> |

Papéis: <QA: estratégia, exploratório, parecer · Devs: unitário, integração, correções · PO: aceite de risco residual>. Entregáveis (só o que alguém vai usar): <testes no repositório, notas de sessões, relatório, parecer>.

## 8. Riscos do projeto (não do produto) e contingência

| Risco | P | I | Contingência | Dono |
| --- | --- | --- | --- | --- |
| <sandbox indisponível> | <1-3> | <1-3> | <virtualização cobre erros; E2E em janela reservada> | <nome> |

## 9. Risco residual e rótulos

Risco residual: <se evento, então efeito; probabilidade; detecção; quem aceita>. Rotule o conteúdo: Verificado · Inferido · Suposição · Não verificável.
