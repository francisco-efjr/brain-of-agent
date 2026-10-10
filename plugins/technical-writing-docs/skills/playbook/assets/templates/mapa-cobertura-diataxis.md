# Template: mapa de cobertura Diátaxis contra o diff

Fontes: GS-rel Step 1.5 (processo adaptado de garrytan/gstack, MIT), V-11, V-28. O mapa **informa**, não gera páginas. Zero cobertura = lacuna **crítica**; só referência = lacuna **comum**. Base do diff: `[BASE]..[HEAD]` (peça ao usuário se não houver; comandos de leitura: `git diff --name-status`, `git log`).

## Superfície pública alterada

Liste o que o diff adiciona, altera ou remove: funções e classes exportadas, comandos e flags, opções de configuração, endpoints, variáveis de ambiente, skills.

| Item | Mudança | Evidência (arquivo:linha) | Tutorial | How-to | Referência | Explicação | Classe da lacuna |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [ITEM] | nova/alterada/removida | [caminho:linha] | [doc ou —] | [doc ou —] | [doc ou —] | [doc ou —] | crítica/comum/nenhuma |

## Correções factuais derivadas do diff (aplicáveis com diff listado)

| Documento | Trecho | Fato correto | Evidência |
| --- | --- | --- | --- |
| [CAMINHO:LINHA] | [TEXTO ATUAL] | [CAMINHO, CONTAGEM, NOME, VERSÃO] | [arquivo:linha] |

## Decisões pendentes (perguntar antes de agir)

Remoções, mudança de narrativa, segurança, reescrita grande, CHANGELOG, ADR: [LISTA].

## Deriva de diagrama (só sinalizar)

| Diagrama | Entidade renomeada/removida | Arquivo |
| --- | --- | --- |

## Navegação

- Documentos alcançáveis do README em até dois cliques: [sim/não; exceções]
- Links relativos quebrados (Grep): [lista ou nenhum]
- Linters de docs configurados (`.vale.ini`, `.markdownlint*`, config do lychee): [lista] (registrados, não executados)

## Dívida de documentação (colar no corpo do PR)

```markdown
## Dívida de documentação
- [ITEM] sem [QUADRANTE]: [AÇÃO SUGERIDA]
```

Rótulos: Verificado (lido, com arquivo) · Inferido · Não verificável.
