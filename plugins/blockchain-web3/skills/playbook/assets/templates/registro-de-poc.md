# Registro de PoC

Adaptado do registro de evidências do brain-of-agent (MIT). PoC só em fork local, RPC por variável de ambiente (cite o nome, nunca o valor), sem chave real e sem transmitir transação. O PoC vale apenas para contratos autorizados do usuário.

| ID | Achado | Estado | Ambiente | Arquivo de teste | Limitação |
| --- | --- | --- | --- | --- | --- |
| POC-01 | [W3-… · arquivo:linha] | [PoC-passed / PoC-failed / apenas-rastro-de-código / needs-execution] | [fork local de [rede] no bloco [n]; `forge --version`: ] | [test/poc/…] | [ ] |

## Execução

ID: [POC-nn] · Achado: [ID] · Tentativa: [n] · Data: [ ]

- Método: [`forge test --match-path …` em fork local | teste diferencial | análise de código]
- Pré-condições montadas: [saldos, papéis, estado do fork]
- Esperado e fonte: [resultado observável e de onde vem o oráculo]
- Comando: `[ ]`
- Saída: [trecho real, incluindo linhas de aprovação/falha e gás se relevante]
- Obtido: [resultado]
- Estado: [um dos estados acima]
- Verificação de `ffi` antes de rodar: [`ffi` ausente/false em `foundry.toml` e sem `vm.ffi` | confirmado pelo usuário]
- Alcance da conclusão: [o que a execução prova e o que não prova]

## Descarte

Se `PoC-failed` e o achado for descartado: nome do teste que refutou, motivo e rodada. Vai para o Apêndice A.

## Mudança e revalidação

- Achado original: [ID]
- Correção e revisão: [arquivos/commit]
- Revalidação: [mesmo teste, antes falhava e agora passa; comando e saída]
- Regressões: [testes adicionais]
- Pendências: [ ]
