# Biblioteca de prompts do orquestrador

Autoria própria (MIT). As variáveis aparecem como `[EM_COLCHETES]`.

## O-01: link em outro chat

```text
Use https://github.com/francisco-efjr/brain-of-agent como orquestrador (siga o ORCHESTRATOR.md da raiz).
Demanda: [O QUE QUERO]. Projeto: [CAMINHO LOCAL OU LINK]. Escopo: [auditar | implementar].
Entrega: [relatórios por papel | correções em branch local | ambos]. Restrições: [o que não mexer, prazo, stack].
Antes de executar, mostre o plano (especialistas, ordem e validadores).
```

**Por que funciona.** Aponta o protocolo explicitamente, define escopo e entrega e pede o plano antes de executar. Assim nenhuma permissão é presumida.

## O-02: revisão completa com relatórios e commit

```text
Orquestre uma rodada completa no projeto [CAMINHO OU LINK] usando os especialistas do brain-of-agent:
arquiteto (antes e depois detalhado, diagramas, ADRs), designer (telas novas aplicando o design system do plugin ux-ui-design),
QA (bugs reproduzíveis com evidência), segurança, qualidade de código e o plugin da plataforma detectada.
Cada relatório passa por um validador independente. Em seguida, o dev implementa as correções aprovadas em uma branch local nova,
roda os testes e o QA revalida. Entregue os relatórios em docs/revisao/ e deixe um commit pronto, sem push.
```

## O-03: feature nova

```text
Orquestre a feature [DESCRIÇÃO] no projeto [CAMINHO]: spec com critérios de aceite (product-discovery-specs),
plano de arquitetura em fatias (architecture-design), implementação (plugin da plataforma), testes (qa-testing)
e revisão de código (code-quality-refactoring). Mostre a spec e o plano antes de implementar. Commit local sem push.
```

## O-04: bug ou incidente

```text
Orquestre a investigação do bug: [SINTOMA, PASSOS, LOGS]. Projeto: [CAMINHO].
Debug sistemático (code-quality-refactoring), teste de regressão que falha antes e passa depois (qa-testing)
e, se for produção, análise com sre-observability. Não altere nada fora da correção mínima.
```

## O-05: telas novas

```text
Proponha telas novas para [OBJETIVO] no projeto [CAMINHO], aplicando o design system do plugin ux-ui-design
(tokens, acessibilidade, estados vazio/erro/carregando) e as convenções da plataforma (mobile-apps ou web-frontend).
Entregue fluxo, wireframes descritos ou protótipo, especificação de componentes e critérios de aceite. Não implemente sem eu aprovar.
```

## O-06: segurança e LGPD

```text
Orquestre uma auditoria de segurança e privacidade em [CAMINHO OU LINK], somente leitura: security-appsec
(modelo de ameaças, OWASP, segredos, dependências), dados pessoais (cite a chave e o local, nunca o valor) e o histórico do git.
Entregue os achados com severidade e evidência, e as ações que só eu posso tomar.
```

## O-07: só planejar

```text
Use o brain-of-agent só para PLANEJAR a demanda [DEMANDA] no projeto [CAMINHO]: classifique, escolha os especialistas
e devolva o plano (tabela trabalho, agente, skills, validador), riscos e decisões pendentes. Não execute nada.
```
