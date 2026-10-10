# Relatório de revisão: CLI, TUI ou script

Preencha apenas o que foi lido ou executado. Rótulos: Verificado (arquivo lido ou saída colada pelo usuário), Inferido (dedução), Suposição, Não verificável, Não aplicável (com motivo). Este relatório é de leitura: o alvo não foi executado, salvo onde a seção "Comandos executados" disser o contrário.

## Cabeçalho

- Alvo: [NOME E CAMINHO]
- Tipo: [CLI | TUI (Textual, Ratatui, Bubble Tea) | PowerShell | bash/sh]
- Versão da ferramenta e do runtime: [VERSÃO] (de onde veio: [comando ou arquivo])
- Público: [humano | agente | ambos] · Versão publicada com compromisso de compatibilidade: [sim/não]
- Escopo lido: [ARQUIVOS] · Fora do escopo: [LISTA]
- Data: [AAAA-MM-DD] · Revisor: [modelo ou pessoa]; autoavaliação do mesmo modelo que escreveu o código não é validação independente.

## Resumo (3 a 5 linhas)

[Resultado primeiro: veredito, número de achados por severidade, o risco principal.]

## Achados

| ID | Severidade | Confiança | Evidência (arquivo:linha ou saída) | Fonte V | Correção mínima | Rótulo |
| --- | --- | --- | --- | --- | --- | --- |
| CLI-04 | Alta | Alta | `src/cli.py:41` `input()` sem teste de TTY | V-13, V-12 | `--no-input`; falhar listando flags | Inferido |

Severidade: Crítica, Alta, Média, Baixa, Info. Confiança: Alta, Média, Baixa. Em dúvida, não reporte (confiança Baixa só com cenário concreto). A linha de exemplo acima ilustra o formato; apague-a.

## Pontos fortes

- [O que já atende o contrato, com evidência.]

## Contrato proposto (opcional)

| Código | Significado | Quando |
| --- | --- | --- |
| 0 | Sucesso | [ ] |
| 2 | Uso inválido | [ ] |
| 3 | Não encontrado | [ ] |

Esquema `--json` (objeto): [CAMPOS]. Regra de estabilidade: [NOTA DE MIGRAÇÃO].

## Não sinalizado de propósito

[Preferências de nome onde o repositório tem convenção, estilo de cor se `NO_COLOR` e TTY são respeitados, recursos fora do escopo.]

## Não verificável

- [Itens sem acesso: acessibilidade de TUI (sem fonte), comportamento em runtime, resize no Windows (Bubble Tea), cobertura de distribuição de CLI.]

## Comandos executados

- [Comando, versão, saída essencial] ou "nenhum; revisão somente por leitura".

## Veredito

[SHIP | FIX FIRST | REWORK]: [motivo em uma linha]. Falha crítica impede SHIP; "sem lacunas" é um resultado válido.

## Próximo passo

[Ação concreta e quem executa.]
