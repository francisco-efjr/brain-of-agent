# Brief de design system

Template T-10. Uso: `design-brief` (modo `brief-ds`). Formato inspirado no template de brief por setor de ui-ux-pro-max-skill (V-30, MIT), em redação própria. Nenhum script externo é executado; a quantidade de dados de uma ferramenta não prova a qualidade das recomendações.

## 1. Entradas

| Campo | Valor |
| --- | --- |
| Produto e setor | [___] |
| Público e contexto de uso | [___] |
| Plataformas e stack | [web | iOS | Android; framework; biblioteca de componentes existente] |
| Requisitos de acessibilidade | [WCAG 2.2 AA; requisito contratual: ___] |
| Idiomas (e RTL?) | [pt-BR | en | ___] |
| Marca existente | [logo, cores, tipografia, DESIGN.md, tokens] ou "inexistente" |
| Superfícies | [Persuade | Operate | Read | Experience, por parte do produto] |
| Restrições | [prazo, equipe, licenças de fontes] |

## 2. Saídas

1. **Tokens de cor:** 4 a 6 cores nomeadas com papel; pares de contraste calculados; modo escuro como modo da coleção semântica.
2. **Tokens de tipografia:** 1 ou 2 famílias, escala, medida de linha < 80 caracteres, corpo ≥ 16 px.
3. **Tokens de espaçamento e forma:** escala base 4 ou 8; hierarquia de raios; elevação.
4. **Padrão de layout** para cada superfície (ver Padrões e anti-padrões do playbook).
5. **Cinco anti-padrões a evitar neste produto:** [cinco itens da lista de visual genérico que mais ameaçam este setor, cada um com o motivo]
6. **Inventário de componentes** necessários, com estados obrigatórios e dono.
7. **Checklist de entrega** (abaixo).

## 3. Checklist de entrega

- [ ] Três camadas de tokens com fonte única (`tokens.json`) e nomes por função.
- [ ] Todos os componentes com estados (hover, foco, desabilitado, carregando, erro), teclado e nota de acessibilidade.
- [ ] Contraste calculado em todos os pares semânticos nos dois temas.
- [ ] Plano de versionamento: quebra de API ⇒ major.
- [ ] Documentação de uso e do que não fazer (Do's and Don'ts).
- [ ] Lacunas declaradas: [Material 3, motion, i18n/RTL, Figma Dev Mode].

## 4. Decisões em aberto e suposições

[___]
