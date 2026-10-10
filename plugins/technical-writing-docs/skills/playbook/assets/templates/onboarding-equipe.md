# Template: onboarding de equipe (novo integrante)

**Suposição de adequação.** Não há fonte validada para onboarding de equipe (novo funcionário, primeiro dia); esta estrutura combina as camadas do onboarding de contribuidor do Kubernetes (V-47, só a estrutura) com o esqueleto de README (V-23). Adapte à sua organização e peça a um integrante recente que a teste (o agente `revisor-de-leitor` também serve). Sem segredos: nunca cole senhas, tokens ou hostnames internos sensíveis; descreva como obter acesso.

````markdown
# Onboarding: [EQUIPE OU PROJETO]

**Para quem:** [CARGO E NÍVEL]. **Tempo estimado do primeiro dia:** [HORAS]. **Responsável por receber você:** [NOME E CANAL].

## 1. Orientação

- O que a equipe faz e para quem: [DUAS FRASES].
- Onde pedir ajuda: [CANAIS, horários, contato de quem desbloqueia].

## 2. Acessos (primeiro dia)

| Acesso | Como pedir | Quem aprova | Como saber que funcionou |
| --- | --- | --- | --- |
| [SISTEMA] | [PROCESSO] | [PESSOA OU GRUPO] | [rode X e veja Y] |

## 3. Ambiente de desenvolvimento

1. [PASSO COM COMANDO EXATO].
   Verificação: rode `[COMANDO]` e veja `[SAÍDA ESPERADA]`.
2. [...]

## 4. Fluxo de trabalho

[Issues, branches, PRs, revisão, testes: links para os documentos reais. Uma linha por item.]

## 5. Primeira entrega

Tarefa pequena e revisável: [LINK PARA A ISSUE]. Revisor nomeado: [NOME]. Critério de pronto: [OBSERVÁVEL].

## 6. Arquitetura e onde a documentação mora

[Link para a visão geral, ADRs, runbooks; como corrigir documentação errada.]

## 7. Contatos

| Assunto | Pessoa ou canal |
| --- | --- |
| [ASSUNTO] | [CONTATO] |
````

## Revisão

- [ ] Cada camada tem um passo verificável ("rode X e veja Y").
- [ ] Todo link existe; todo comando foi executado por alguém ou está marcado "não executado".
- [ ] Nenhum segredo nem host interno sensível.
- [ ] Teste de leitor limpo antes de entregar.
