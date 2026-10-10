# Template: explicação (quadrante: compreensão)

Fontes: V-11, GS-gen Step 4 (processo adaptado de garrytan/gstack, MIT). Responde "por que é assim?". Abra pelo **problema**, não pela solução. Nomeie trade-offs ("escolhemos X em vez de Y porque Z"). **Sem instruções** (vão para how-to). Escopo delimitado; título do tipo "Sobre [TEMA]". Diagramas: Mermaid com render confirmado, ou fallback; veja `diagrama-mermaid.md`.

````markdown
# Sobre [CONCEITO OU DECISÃO DE DESIGN]

[Parágrafo de abertura: o problema que este design resolve, em termos que um leitor inteligente que nunca viu o código entenderia.]

## O problema

[O que dá errado sem este design. Falhas reais, não riscos abstratos. Fonte: testes, issues, commits (cite o arquivo).]

## A abordagem

[Como o design resolve o problema. Diagrama quando ajudar a arquitetura.]

## Trade-offs

[O que foi sacrificado. Toda decisão troca algo: diga o quê.]

## Alternativas consideradas

[O que foi tentado ou rejeitado e por quê, quando for descobrível em ADRs, comentários `WHY`/`DESIGN` ou histórico. Sem evidência: escreva "Não verificável".]

## Onde ver mais

- Referência: [LINK] · How-to relacionado: [LINK] · Registro da decisão (ADR): [LINK]
````

## Revisão

- [ ] Começa pelo problema.
- [ ] Trade-offs nomeados.
- [ ] Nenhum comando para executar.
- [ ] Não repete o material de referência (link).
