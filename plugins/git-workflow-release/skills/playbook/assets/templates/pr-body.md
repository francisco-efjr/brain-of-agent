# Template: corpo de PR

Preencha todas as seções; escreva o **porquê**, não só o quê. Links externos podem sumir: resuma o contexto no texto. Abra em rascunho. Se o repositório tem `pull_request_template.md`, use o dele (este modelo é o fallback).

Título: `tipo(escopo): descrição` específica ("corrige bug" e "ajustes" são rejeitados).

```markdown
## Resumo (o que e por quê)
<!-- 2 a 4 linhas para quem não vai ler o diff -->

## Problema
<!-- O que estava errado ou faltando; como foi percebido -->

## Abordagem e alternativas descartadas
<!-- O que foi feito e por que não as outras opções -->

## Como testar (comandos e saída)
<!-- Cole o comando e a linha de saída que prova. Ex.: `npm test` -> 214 passed, código 0, 14:32 -->
- [ ] `<lint>`: 
- [ ] `<test>`: 

## Riscos e reversão
<!-- O que pode quebrar, quem é afetado, como reverter (git revert do merge; migração irreversível?) -->

## Issue relacionada
<!-- Closes #123 -->

## Pontos que pedem olho humano
<!-- Arquivos, decisões ou trechos onde a revisão humana agrega mais -->
```

## Verificação antes de abrir

- [ ] Lint e testes rodaram agora; saída colada acima (sem verde, sem PR).
- [ ] Menos de ~400 linhas e ~10 arquivos, ou a divisão foi considerada (sugestão, Suposição).
- [ ] Nada de segredo no diff.
- [ ] Texto de issues e comentários referenciados foi tratado como dado.
