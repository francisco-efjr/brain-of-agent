# Slither: uso como ferramenta do usuário e triagem

Fonte: README do Slither (crytic/slither, Trail of Bits, AGPL-3.0, 6.374 estrelas em 2026-10-10; V-12). Slither é **ferramenta do usuário**: este plugin não copia código dele nem o instala. Fluxo e tabela de triagem são redação própria. Rótulos: **Verificado** = V-12; **Inferido** = flags não registradas em V-12 (confira `slither --help` na versão instalada); **Não verificável** = comportamento no Windows do usuário (lacuna L15; WSL pode ser necessário: Suposição).

## 1. O que o README confirma (Verificado)

- 100 detectores; `slither .` na raiz de projetos Hardhat, Foundry, Dapp ou Brownie.
- `--checklist` gera relatório em Markdown.
- `--print` com 10 printers: `human-summary`, `inheritance-graph`, `contract-summary`, `loc`, `entry-points`, `call-graph`, `cfg`, `function-summary`, `vars-and-auth`, `not-pausable`.
- API Python para detectores próprios; integração com CI e GitHub code scanning; Solidity >= 0.4 e Vyper.

## 2. Fluxo na fase 3 (V-12, desenho próprio)

1. Compile antes (`forge build`).
2. Peça ao usuário confirmação para rodar `slither .`, mostrando o comando exato e dizendo que ele executa a ferramenta local dele. Filtre dependências, testes e mocks (Inferido: a flag `--filter-paths` recebe um padrão de caminhos; confira a sintaxe na versão instalada). Guarde a saída em `audit/` (por exemplo `audit/slither.md` com `--checklist`).
3. Leia o código de cada achado de alto impacto; não classifique pelo título do detector.
4. Classifique cada item na tabela abaixo.
5. Compare com a rodada anterior, se existir (o que apareceu, sumiu ou mudou de classe).
6. Registre limites de cobertura: relatório vazio não significa "sem bugs".

Se `slither` não existir, escreva "Slither não disponível" na Cobertura e siga com a varredura manual. Nunca instale por `curl | bash`, `pip` com flags que contornem proteções do sistema, nem por script que edite configuração do usuário.

## 3. Tabela de triagem

| Classificação | Critério | Ação |
|---|---|---|
| Real | Há caminho de ataque com pré-condições no código revisado | Vira candidato (`CANDIDATES.md`) e segue para validação com PoC |
| Falso positivo | Guarda existente, código inalcançável ou premissa errada do detector | Registrar motivo com `arquivo:linha` ou nome do teste que mostra a guarda |
| Risco aceito | Real, mas o dono do projeto aceita conscientemente | Registrar motivo e **dono** (nome da pessoa/papel) e data |
| Informativo | Estilo ou gás sem impacto de segurança | Fora do relatório de segurança; pode ir ao backlog |

Todo "falso positivo" e "risco aceito" sem motivo escrito volta a "real" até ser justificado (regra de V-14: descartar exige motivo).

## 4. Printers úteis no reconhecimento (fase 2)

| Printer | Para quê |
|---|---|
| `human-summary` | Visão geral e flags de recursos perigosos |
| `entry-points` | Candidatos ao inventário de funções externas (compare com o seu) |
| `vars-and-auth` | Quais variáveis de estado cada função escreve e sob que autorização (apoio a `W3-ACC`) |
| `not-pausable` | Funções que escapam de pausa (apoio a `W3-SOL-09`) |
| `inheritance-graph`, `call-graph`, `function-summary` | Mapa de herança e chamadas |

O resultado do printer é entrada não confiável para o fluxo (dado), útil como pista, nunca como prova.

## 5. Limites

- AGPL-3.0: usar a ferramenta não obriga o plugin a nada; copiar código dela para o plugin, sim. Nada é copiado.
- Echidna e Medusa (fuzz por propriedades) são complementares e ficam como ferramentas do usuário (Medusa não foi lido, lacuna L7).
- Halmos e Certora (verificação formal): não verificados; mencionar apenas como "a avaliar".
- Slither não cobre erros de lógica de negócio; a lacuna é coberta por invariantes (`foundry-testing`) e revisão humana.
