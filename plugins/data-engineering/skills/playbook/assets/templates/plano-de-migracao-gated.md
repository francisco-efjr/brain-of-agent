# Plano de migração com gates: [TECNOLOGIA] [VERSÃO ORIGEM] → [VERSÃO DESTINO]

Uso: skill `gated-pipeline-migration` (invocação explícita). Base: V-11 (`upgrading-dbt`, dbt Labs, Apache-2.0, adaptado) e "Migração e liberação" do brain-of-agent (MIT, do autor). Tipo: [UPGRADE DE VERSÃO|TROCA DE PLATAFORMA|MUDANÇA ESTRUTURAL].
Regras do plano: cada fase só começa quando o gate da anterior passa; mudanças fora do repositório são relatadas, não editadas; nenhuma instalação de pacote (`uv`, `uvx`, `dbt deps`, `npx`) sem decisão revisada do usuário; nenhuma execução em produção.

## Fases
| Fase | O que fazer | Gate | Preenchimento |
| --- | --- | --- | --- |
| 0 | Preflight de git: árvore limpa e fora de `main`/`master` | Falhou: parar | Branch: [NOME] · `git status`: [RESULTADO] |
| 1 | Listar o que muda a partir de fonte verificável (changelog oficial fornecido ou lido com autorização); nunca de memória | Sem fonte: parar | Fonte: [URL/ARQUIVO] · data: [DATA] |
| 2 | Ler o projeto sem editar | | Arquivos lidos: [N] |
| 3 | Detectar ocorrências sem editar | | Ocorrências por tipo: [TABELA] |
| 4 | Aplicar correções determinísticas em lote | | Arquivos alterados: [LISTA] |
| 5 | Correções que exigem julgamento | | Itens: [LISTA] |
| 6 | Mostrar diff e pedir confirmação do ambíguo | Sem confirmação: não editar | Confirmado por [NOME] em [DATA] |
| 7 | Verificação mínima: parse/compilação primeiro | Tetos abaixo | Comando: `[COMANDO]` · resultado: [SAÍDA] |
| 8 | Re-detectar | Ocorrências restantes: 0 ou listadas | [RESULTADO] |
| 9 | Relatório final | | Ver seção "Relatório" |

Tetos (V-11): `dbt parse` com no máximo 5 tentativas no projeto todo; qualquer outro laço de verificação, até 3 repetições; três falhas seguidas do mesmo comando encerram a verificação; `compile`/`test`/`build` só com perfil definido e aprovação. Confirmar na versão instalada se o parse exige perfil válido e conexão; se exigir, tratar como comando com efeito. Em outras tecnologias, o teto é 3 ciclos de correção.

## Oráculo antes/depois (obrigatório em troca de plataforma)
| Verificação | Antes | Depois | Igual? |
| --- | --- | --- | --- |
| Contagem por tabela | [N] | [N] | [S/N] |
| Chaves únicas/nulas | [N] | [N] | [S/N] |
| Totais por métrica | [VALOR] | [VALOR] | [S/N] |
| Relações (FK) | [N ÓRFÃOS] | [N ÓRFÃOS] | [S/N] |
| Casos especiais (nulos históricos, encoding, duplicatas válidas) | [LISTA] | [LISTA] | [S/N] |
| Invariantes por entidade (amostra por cliente/conta) | [AMOSTRA] | [AMOSTRA] | [S/N] |
Contagens iguais não impedem valores trocados entre entidades; por isso a amostra e as invariantes por entidade.

## Ensaios
- Falha parcial: [COMO SIMULAR E RESULTADO]
- Retomada: [COMO RETOMAR]
- Execução repetida (idempotência): [RESULTADO]
- Convivência de versões durante a migração (expandir, migrar, remover): [PLANO]

## Rollback
Rollback de código não restaura dado destruído. Backup/restauração validado em [DATA] ou "não validado".

## Fora do repositório (relatar, não editar)
[CI, imagens, adapters instalados, permissões, conexões]

## Relatório
- Até onde a verificação chegou: [FASE]
- O que ficou para o usuário: [LISTA]
- Não verificado: [LISTA]
- Revisão: feita pelo mesmo modelo = autoavaliação, não validação externa.
