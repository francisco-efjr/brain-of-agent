# Relatório de revisão de prompt

Base: checklist de 12 itens (V-01) e poda para modelos Claude 5 (V-03). Revisão feita pelo mesmo modelo que escreveu o prompt não é validação independente: declare. Nada aqui foi executado, salvo o que a seção de verificação listar.

- **Artefato revisado:** [arquivo ou trecho] · **Modelo-alvo e data:** [...] · **Falhas observadas:** [...]
- **Lido por inteiro:** [sim/não; o que não foi aberto]

## Veredito

[aprovado / aprovado com mudanças / reescrever] em uma ou duas frases.

## Achados

| # | Trecho citado | Item do checklist | Problema | Severidade (bloqueante / melhoria / opcional) | Correção |
| --- | --- | --- | --- | --- | --- |
| 1 | "[...]" | 3 (tom) | CAPS e "CRITICAL" tendem a causar excesso de uso de ferramenta | melhoria | Motivo + linguagem calma |

## Poda (V-03)

| Pergunta | Resposta | Ação |
| --- | --- | --- |
| Cada regra "sempre/nunca" ainda é necessária? | | |
| Exemplos que travam a exploração viram enum ou parâmetro? | | |
| Instrução de tool mora na tool? | | |
| Conhecimento ocasional virou skill? | | |
| Só o que o código não revela? | | |
| Referência executável substitui prosa? | | |

## Versão proposta (menor versão que preserva o contrato)

```text
[...]
```

## Plano de teste

3 tarefas reais com e sem a mudança; critério por tarefa; modelo e data; resultado esperado. Status: **projetado, não executado**.

## Suposições, riscos e próximo passo

[...]
