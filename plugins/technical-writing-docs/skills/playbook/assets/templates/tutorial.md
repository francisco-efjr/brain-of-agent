# Template: tutorial (quadrante: aprendizado)

Fontes: V-46 (critérios), GS-gen Step 6 (processo adaptado de garrytan/gstack, MIT), V-11 (Diátaxis, CC BY-SA 4.0, destilado). O leitor aprende fazendo. **Sem explicação no corpo**: uma linha de "o que você deve ver" por passo; o "por quê" vira link para uma página de explicação. Primeiro resultado visível até o passo 3. Uma trilha só, sem "escolha A ou B". Todo comando abaixo deve ser executado por você (com autorização) ou marcado "não executado".

````markdown
# [TÍTULO QUE DESCREVE O QUE SERÁ CONSTRUÍDO]

[Parágrafo de abertura: "Você vai construir [X] que faz [Y]." Concreto, sem "este tutorial aborda".]

**Destino:** [IMAGEM, SAÍDA OU RESULTADO FINAL, para o leitor ver aonde vai.]

## O que você vai precisar

- [FERRAMENTA E VERSÃO MÍNIMA] (link para instalação)
- [CONHECIMENTO PRÉVIO, se houver]

## Passo 1: [partir de um estado limpo]

```bash
[COMANDO EXATO]
```

Você deve ver: [SAÍDA OU MUDANÇA VISÍVEL].

## Passo 2: [primeira peça funcionando]

```bash
[COMANDO EXATO]
```

Você deve ver: [RESULTADO VISÍVEL].

Se aparecer `[ERRO COMUM]`: [CORREÇÃO EM UMA LINHA].

## Passo 3: [resultado visível do objetivo principal]

[...]

## Passo N: [último passo]

[...]

## O que você construiu

[Recapitule o que o leitor tem agora e o que ele consegue fazer.] Próximos passos: [how-to relacionado], [referência], [explicação: por que é assim].
````

## Revisão

- [ ] Primeiro resultado visível até o passo 3.
- [ ] Cada passo termina com "Você deve ver".
- [ ] Comandos exatos; nenhuma abstração ("execute o comando apropriado").
- [ ] Erros comuns avisados no passo, vindos de testes ou tratamento de erro.
- [ ] Nenhum parágrafo explicativo longo; links para explicação e referência.
- [ ] Teste de leitor limpo com `revisor-de-leitor` (tutorial e onboarding).
