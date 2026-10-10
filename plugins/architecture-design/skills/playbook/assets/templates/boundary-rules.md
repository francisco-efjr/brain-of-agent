<!-- Regras de fronteira verificáveis. Sem verificador executável, a regra é só uma frase. -->
# Regras de dependência: [sistema]

Revisão: [AAAA-MM-DD] · Dono: [nome]

## Tabela camada ou módulo para imports
| Camada / módulo | Pode importar | Não pode importar |
| --- | --- | --- |
| [api] | [services, schemas] | [repositories, db] |
| [services] | [repositories (por interface), domain] | [api, db] |
| [domain] | [biblioteca padrão] | [tudo o mais do projeto] |

## Regras de módulo
- Contrato por módulo: [fachada, API ou evento].
- Nenhum acesso direto a tabela de outro módulo (propriedade de esquema).
- Código compartilhado entra se houver comportamento comum e dono.

## Verificador
- Comando: `[comando que roda no CI]`
- Cobre: [imports textuais]. Não cobre: [DI, reflexão, config por ambiente: Inferido].
- Falha o build? [sim | não]

## Caso de violação documentado (prova de que o verificador funciona)
| arquivo:linha | Importação | Regra violada | Correção aplicada |
| --- | --- | --- | --- |

## Regra para o CLAUDE.md (forma positiva, com gatilho de parada)
"[Módulo A] não importa [Módulo B]. Verificação: `[comando]`. Se parecer necessário importar, pare e registre a dúvida."

## Métrica de acoplamento de mudança (Suposição)
Limiar acordado: [x% de commits tocando A e B juntos]; consulta: `git log --name-only` por período.
