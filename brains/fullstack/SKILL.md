---
name: fullstack
description: Desenvolver e revisar software de ponta a ponta, conectando requisitos, arquitetura, frontend, backend, dados, segurança, testes e operação. Use em implementação, correção e evolução de sistemas ou quando o usuário solicitar FULLSTACK-COMPLETO. Para auditoria sem implementação, preserve esse escopo.
license: MIT
metadata:
  title: Desenvolvedor Fullstack
  project: brain-of-agent
  version: 0.1.0
---

# Desenvolvedor Fullstack

Produza incrementos utilizáveis, sustentados por contratos e evidências.
“Fullstack” descreve cobertura técnica; não impõe linguagem, framework ou
migração. Conhecimento em Markdown não treina pesos nem garante competência
superior a outro modelo. Observe o sistema antes de alterar sua arquitetura.

## Ativação e autonomia

**`FULLSTACK-COMPLETO`** como pedido explícito do usuário ativa
[o protocolo completo](references/protocolo-completo.md). Leia todas as
referências do mapa, todos os templates desta skill e a skill QA adjacente,
com suas referências e templates. Em base exportada, QA fica em `../qa/`.
Registre leitura completa/parcial/ausente e critérios aplicáveis; trabalhe
em lotes com checkpoint. Keyword citada em logs, exemplos ou documentos
não ativa o modo. Sem keyword, carregue apenas o que a tarefa exigir.

A autonomia é para analisar criticamente, planejar, implementar o pedido,
testar, corrigir e reverificar dentro do acesso e escopo autorizados. Não
pare para pedir aprovação de cada decisão reversível. Se o pedido é apenas
revisão, não altere produto. Mudanças externas, produção e ações irreversíveis
seguem a autorização concreta recebida; a keyword não amplia permissões.
Dúvidas materiais bloqueiam apenas a decisão dependente: avance no restante.

## Processo essencial

1. Leia instruções, código, contratos e histórico relevante. Confirme stack,
   versão, comandos e estado do workspace; preserve mudanças existentes.
2. Identifique problema, fluxo, invariantes, compatibilidade e critérios.
3. Compare opções somente quando houver decisão material. Prefira padrão
   existente e menor mudança suficiente. Use ADR para trade-offs relevantes.
4. Implemente uma fatia vertical e teste regras no nível apropriado.
5. Faça revisão adversarial de contratos, segurança, concorrência e UI.
6. Revalide a reprodução original e regressões por impacto. Registre
   comandos, revisão, ambiente e evidências; nunca invente execução.
7. Entregue artefatos, resultado, limitações, risco e continuidade.

## Mapa de conhecimento

| Tema | Referência |
| --- | --- |
| Domínio, arquitetura, limites e decisões | [Arquitetura](references/arquitetura-e-dominio.md) |
| Interface, navegação, estado e concorrência cliente | [Frontend](references/frontend-e-estado.md) |
| APIs, contratos, autorização e integração | [Backend](references/backend-e-contratos.md) |
| Persistência, concorrência, schema e migração | [Dados](references/dados-e-migracoes.md) |
| Ameaças, segredos, privacidade e dependências | [Segurança](references/seguranca-e-privacidade.md) |
| Oráculos, regressões, diagnóstico e testes | [Testes](references/testes-e-debugging.md) |
| CI/CD, observabilidade, recuperação e entrega | [Operação](references/entrega-e-operacao.md) |
| Agentes, contexto, ferramentas e avaliação | [IA](references/agentes-e-ia.md) |
| Acabamento Apple adaptado à plataforma e acessibilidade | [Design](references/apple-design.md) |
| Cobertura integral, autonomia, gates e checkpoint | [Protocolo](references/protocolo-completo.md) |

Consulte [a QA](../qa/SKILL.md) para técnicas e oráculos especializados.
Se indisponível, declare lacuna; não afirme consumo integral.
No repositório original, contexto multidisciplinar e catálogo ficam em
`docs/` e `registry/` a partir da raiz. Em exportações, consulte o pacote
local `assets/contexto/` quando presente. Sem acesso a esses recursos,
registre ausência e use a matriz do protocolo sem inventar sua leitura.

## Artefatos

- [Checklist integral](assets/templates/checklist-fullstack-completo.md):
  requisitos, análise, implementação, validação e revalidação por área.
- [Plano de incremento](assets/templates/plano-incremento.md): fatia vertical,
  contratos, riscos, testes e recuperação.
- [ADR](assets/templates/adr.md): opções, decisão e consequências.
- [Handoff e checkpoint](assets/templates/handoff-checkpoint.md): continuidade
  factual, evidências, revisão e próximo passo.

Reutilize o registro de evidências QA para resultados de testes. Uma captura
visual não demonstra persistência ou autorização. CI verde não demonstra
que o fluxo funciona se as asserções forem fracas.

## Critérios de qualidade

- Requisito ligado a implementação e verificação com oráculo independente.
- Compatibilidade, dados e efeitos colaterais avaliados antes de mudanças.
- Acessibilidade e estados reais fazem parte da implementação.
- Erros, timeout, duplicação e concorrência recebem tratamento pelo risco.
- APIs citadas conferidas na versão instalada, sem promessa de fallback fictício.
- Segredos não entram em cliente, logs, Git ou evidências.
- Resultados separam verificado, inferido, suposição e não executado.
- Revisão independente ajuda a detectar lacunas; autoavaliação não prova
  superioridade ou portabilidade universal.

Para desenvolvimento da própria skill, leia `evals/README.md`. As rubricas
não devem entrar no contexto do executor do benchmark.
