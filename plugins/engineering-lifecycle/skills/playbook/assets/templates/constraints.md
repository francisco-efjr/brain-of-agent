# Modelo: CONSTRAINTS.md (contrato de qualidade com catraca)

Use com a skill [constraint-driven-development](../../../constraint-driven-development/SKILL.md) e o comando `/engineering-lifecycle:constraints`. Copie o bloco abaixo para a raiz do repositório alvo e preencha o que estiver entre colchetes. Adaptado do esqueleto do agent-skills (Addy Osmani, MIT), com a precedência do brain.

## Como preencher

1. **Detecte antes de perguntar** (stack, runner de teste, lint, cobertura de hoje, CI, harness do agente) e relate em duas linhas. Nunca pergunte o que dá para ler.
2. **No máximo quatro perguntas**, uma por vez, cada uma com palpite e padrão; "não sei" também gera uma configuração que funciona.
3. **Sem número em mente, meça o de hoje e segure a linha** (catraca). Não invente meta que o código já falha.
4. **Cada número tem motivo e comando.** Dimensão com número e sem comando é aspiração: marque "proposta" ou remova.
5. **Pelo menos uma checagem externa** (axe, osv-scanner, Lighthouse), para o contrato não depender só dos testes que o agente escreveu.
6. **Ferramenta nova é proposta.** Instalar exige confirmação do usuário e versão fixada; veja [ferramentas-e-hooks.md](../../references/ferramentas-e-hooks.md). Não grave `check:*` no `package.json` sem mostrar o diff.
7. **Em CI ou loop sem usuário, vale só o piso.** Registre que o resto ficou para um humano.
8. Aponte o agente para o arquivo com a regra EL-01 de [claude-md-snippets.md](../../references/claude-md-snippets.md).

Valores padrão do autor, **Suposição** até medir no projeto: cobertura das linhas alteradas ≥ 80%; mutação ≥ 60% para começar; dependências sem severidade alta ou crítica; LCP ≤ 2500 ms; CLS ≤ 0,1; exceção com no máximo 90 dias; tolerância da catraca 0,5%. Acessibilidade: **WCAG 2.2 AA** (precedência do brain).

O upstream menciona um `.constraintsignore` na guarda de diff, mas a implementação de referência não o lê: não prometa esse arquivo.

## O arquivo

```markdown
# Constraints

Última revisão: [AAAA-MM-DD] por [responsável]
Leia este arquivo antes de escrever código. Não o enfraqueça para fazer uma mudança passar.

## Piso (sempre vale, sem instalar nada)

- Nenhuma supressão nova: `@ts-ignore`, `eslint-disable`, `# noqa`, `# type: ignore`, `nosemgrep`, `istanbul ignore`, `gitleaks:allow`
- Nenhum stub inacabado: `throw new Error("Not implemented")`, `catch` vazio, TODO no lugar da implementação
- Nenhum teste pulado ou apagado, nem asserção removida, sem motivo na mensagem do commit
- Nenhum segredo no código
- Limiar, regra ou exceção deste arquivo só mudam em commit próprio, com aprovação humana

## Limites em três camadas

- **Sempre:** [rodar os testes antes de commitar; validar entrada na fronteira; seguir as convenções do projeto]
- **Perguntar antes:** [mudar schema; adicionar dependência; mexer em CI; novo fluxo de autenticação; integração externa]
- **Nunca:** [commitar segredo; remover teste que falha sem aprovação; logar dado pessoal; editar `vendor/`]

## Aplicado com número

| Dimensão | Regra | Motivo | Checado por (comando exato) | Roda em |
| --- | --- | --- | --- | --- |
| Tipos | Zero erros de tipo | [o build já exige] | [`tsc --noEmit`] | cada edição |
| Lint | Zero erros na config do projeto | [convenção do time] | [`eslint .` ou `biome check` ou `ruff check`] | cada edição |
| Segredos | Nenhum segredo no código | [vazamento é irreversível] | [comando do scanner de segredos, com opção de ocultar o valor] | cada edição |
| Cobertura | Linhas alteradas ≥ [80%] | [alto o bastante para exigir teste] | [`vitest run --coverage` ou equivalente] | fim da tarefa e CI |
| Segurança: código | Nenhum achado alto | [fronteiras de confiança] | [comando do analisador] | CI |
| Segurança: dependências | Nada alto ou crítico alcançável | [advisories conhecidos] | [comando do scanner de dependências] | CI |
| Acessibilidade | Zero violações críticas ou sérias, WCAG 2.2 AA | [norma do brain] | [comando do axe com as tags 2.2 da versão fixada; URL local 127.0.0.1] | preview ou local |
| Performance | LCP ≤ [2500 ms]; CLS ≤ [0,1] | [metas de Core Web Vitals do texto do upstream] | [comando do Lighthouse; mediana de repetições] | preview |

## Medido, ainda não aplicado (catraca)

| Métrica | Hoje | Direção | Medida em |
| --- | --- | --- | --- |
| Cobertura do projeto | [62,4%] | não cair (tolerância 0,5%) | [AAAA-MM-DD, comando] |
| Bundle principal | [184 kB] | não crescer | [AAAA-MM-DD, comando] |

Piorar além da tolerância é achado. Melhorar: atualize o valor aqui, em commit próprio.

## Exceções

| ID | Regra | Caminho | Motivo | Dono | Expira |
| --- | --- | --- | --- | --- | --- |
| [E1] | [`no-explicit-any`] | [`src/legacy/**`] | [reescrita em ISSUE-123] | [@pessoa] | [AAAA-MM-DD, até 90 dias] |

## Onde cada checagem roda

| Estágio | Orçamento | O quê |
| --- | --- | --- |
| Edição | Segundos, só o arquivo alterado | Tipos, lint, segredos, piso |
| Fim da tarefa | Menos de 90 s | Testes relacionados, cobertura das linhas alteradas |
| Revisão | Minutos | Tudo, mais a guarda de enfraquecimento (limiar movido, teste mais fácil, checador silenciado, trabalho inacabado, exceção nova) |
| CI | Sem limite | Direção das métricas, sem regressão |
```

## Verificação do modelo preenchido

- [ ] O arquivo existe na raiz e cada número tem motivo.
- [ ] O piso passa hoje, sem mudar código.
- [ ] Cada dimensão escolhida tem comando que roda hoje.
- [ ] Há ao menos uma checagem externa.
- [ ] Exceções têm dono e data de expiração.
- [ ] O `CLAUDE.md` ou `AGENTS.md` aponta para o arquivo.
