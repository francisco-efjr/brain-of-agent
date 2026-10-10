# Template: README de projeto aberto (landing page)

Fontes: V-23 (seis seções), V-25 (landing page, CC0-1.0). Use no README de entrada de projeto aberto; tom de venda só aqui. Antes de preencher, leia o manifesto (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`) e o arquivo `LICENSE`: nome, comando e licença vêm deles, nunca de memória. Apague as instruções entre colchetes depois de preencher.

````markdown
# [NOME DO PROJETO]

[FRASE DE VALOR: o que o leitor ganha, em uma frase. Evite "Uma ferramenta que...".]

```[LINGUAGEM]
[EXEMPLO FUNCIONAL DE ATÉ ~5 LINHAS, com a saída esperada em comentário]
```

| Funcionalidade | O que você ganha |
| --- | --- |
| [NOME] | [BENEFÍCIO CONCRETO] |
| [NOME] | [BENEFÍCIO CONCRETO] |

## Quick Start

```bash
[COMANDOS COPIÁVEIS, SEM "$" NO INÍCIO; ~30 SEGUNDOS]
```

Resultado esperado: [O QUE O LEITOR DEVE VER]. [Marque "não executado" se você não rodou.]

## Instalação

[GERENCIADOR DE PACOTES DETECTADO NO MANIFESTO + versão mínima do runtime]

## Uso

[2 a 3 exemplos reais. Para referência completa: link para docs/ (quadrante referência).]

## Documentação

- [Tutorial]([CAMINHO]) · [Guias how-to]([CAMINHO]) · [Referência]([CAMINHO]) · [Por que é assim]([CAMINHO])

## Contribuição e suporte

[Como abrir issue/PR; link para o guia de contribuição; onde pedir ajuda.]

## Licença

[Nome da licença, exatamente como em LICENSE.] Veja [LICENSE](LICENSE).
````

## Checklist de revisão (V-25)

- [ ] Decisão em 3 a 5 segundos: a primeira frase diz o valor.
- [ ] Exemplo funcional nas primeiras linhas.
- [ ] Quick Start copiável; todo comando existe no manifesto (Grep).
- [ ] Imagens e links existem (Glob).
- [ ] Sem "seamless", "robust", "comprehensive", "cutting-edge", "In today's", "Happy coding".
- [ ] Licença igual a `LICENSE`.
- [ ] Nenhuma badge ou URL inventada.
