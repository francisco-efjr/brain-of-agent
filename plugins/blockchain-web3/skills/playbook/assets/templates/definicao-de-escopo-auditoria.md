# Definição de escopo da auditoria

Fase 1 do `audit-contracts`. Preencha com o usuário antes de qualquer varredura; a fase 2 só começa quando este arquivo termina com o marcador. Sem dado, escreva "Não informado" e registre a suposição. Não inclua chaves, seeds nem valores de `.env`: cite só nomes de variáveis.

## Escopo e autorização

- Modo: [diff | full] (diff só por opt-in; restringe a varredura ao que o diff altera ou torna alcançável)
- Contratos no escopo (caminho, linhas, commit/tag): [lista]
- Fora de escopo (bibliotecas em `lib/`, testes, mocks, contratos de terceiros): [lista]
- O que o agente pode alterar: [nada (auditoria) | arquivos X em `test/` | ...]
- Ações com efeito externo autorizadas: [nenhuma por padrão; deploy, assinatura e transmissão são do usuário]

## Sistema

- Cadeia(s) alvo e L2: [ex.: Ethereum, Base]
- Linguagem e compilador (pragma e versão instalada): [ ]
- Framework e versão (`forge --version`): [ ]
- Bibliotecas e versões (OpenZeppelin, tag; plugin de upgrades): [ ]
- Padrões implementados/consumidos (ERC-20/721/1155/4626, EIP-712...): [ ]
- Proxies e papéis privilegiados (quem atualiza, quem pausa): [ ]
- Dependências externas (oráculos, DEX, pontes, tokens aceitos): [ ]
- Documentação e propriedades esperadas (NatSpec, spec, invariantes conhecidas): [ ]

## Regras

- Severidade (Alta/Média/Baixa) e critério: [padrão do plugin ou o do usuário]
- Limiar de relato: confiança ≥ 0,8; Alta exige PoC ou "Verificação pendente"
- Restrições (prazo, custo de tokens, ferramentas permitidas): [ ]
- Aprovação de custo antes de subagentes em paralelo: [sim/não; limite]

## Ambiente de execução

| Ferramenta | Disponível? | Versão | Observação |
| --- | --- | --- | --- |
| forge | | | sem ele, PoC fica `needs-execution` |
| slither | | | só se o usuário já o tem; confirmação na fase 3 |
| RPC de fork (nome da variável) | | | nunca o valor |
| `ffi` em `foundry.toml` | | | se `true`, pedir confirmação antes de rodar testes |

## Áreas aplicáveis

SOL · ACC · UPG · VLT · ERC · ORA · L2 · HOOK · SCN · SIG · SVM · TST · GAS · AGT (marque as que se aplicam e o motivo das demais: veja `matriz-aplicabilidade-web3.md`).

Ao concluir esta fase, acrescente ao final do arquivo a linha `<!-- W3_STATUS: COMPLETE -->` (o próprio passo escreve o marcador; sem ele a fase 2 não começa).
