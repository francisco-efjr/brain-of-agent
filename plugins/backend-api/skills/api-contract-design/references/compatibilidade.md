# Compatibilidade de contrato: breaking x compatível, por protocolo

Uso: classificar cada mudança de contrato antes de publicar. Base: conteúdo próprio do brain-of-agent (`backend-e-contratos`, `automacao-api`, MIT), V-30 (GraphQL), V-34/V-35 (paginação e versionamento), V-17 (gRPC). Itens que dependem de fato externo não reverificado estão rotulados Inferido.

## Sumário

1. Princípio
2. REST/HTTP: tabela de classificação
3. Proto/gRPC
4. GraphQL
5. Eventos e schemas de mensagem
6. Deprecar e remover
7. Procedimento de revisão (diff de spec)

## 1. Princípio

Compatível é o que **todo consumidor existente continua tratando corretamente sem mudar**, não o que o schema aceita. Duas perguntas por mudança: (1) quem lê este campo ou depende deste comportamento? (2) o que acontece com o cliente mais antigo que ainda está em uso? Consumidores desconhecidos (API pública) tornam toda dúvida um breaking.

Regra de leitura/escrita (robustez): produtor de **resposta** só acrescenta; consumidor de resposta ignora campo desconhecido e tolera valor novo de enum aberto. Receptor de **entrada** que rejeita ou ignora campo desconhecido documenta qual dos dois.

## 2. REST/HTTP: tabela de classificação

| Mudança | Classe | Por quê / mitigação |
| --- | --- | --- |
| Campo opcional novo na resposta | compatível | clientes tolerantes ignoram; confira clientes com deserialização estrita (`additionalProperties` fechado, DTO que falha em campo extra) |
| Campo opcional novo na entrada | compatível | valor padrão deve preservar o comportamento antigo |
| Campo **obrigatório** novo na entrada | breaking | quem não envia passa a receber 400/422; torne opcional com padrão ou crie versão nova |
| Remover ou renomear campo (entrada ou saída) | breaking | mantenha o antigo `deprecated: true` até o `Sunset`; duplique o campo na transição |
| Mudar tipo, formato, unidade, escala ou fuso (`"49.90"` para número; segundos para ms) | breaking | crie campo novo com nome novo |
| Valor novo em enum de **resposta** | breaking para consumidor com `switch` exaustivo | documente enum aberto desde o início; anuncie antes; exponha só a clientes que optaram |
| Valor novo em enum de **entrada** | compatível | clientes antigos simplesmente não o enviam |
| Restringir enum/limite de entrada (menor máximo, `pattern` mais estrito) | breaking | valores antes válidos passam a falhar |
| Afrouxar limite de entrada | compatível | confira limites de armazenamento e de segurança |
| Mudar ordenação padrão ou critério de desempate | breaking | paginação e telas dependem da ordem; só com parâmetro novo |
| Mudar significado de campo ou regra de negócio (arredondamento, o que `status=PAID` quer dizer) | breaking | schema válido não prova compatibilidade; versione ou crie campo novo |
| Mudar o status de um cenário (200 para 202; 404 para 403; 400 para 422) | breaking | clientes ramificam por status |
| Novo código de erro/`type` em cenário já existente | geralmente compatível | cliente deve ter caminho genérico por classe de status |
| Remover endpoint ou método | breaking | deprecar, sinalizar, aguardar `Sunset`, medir tráfego restante |
| Tornar autenticação/escopo mais restrito | breaking | clientes com token antigo passam a receber 401/403 |
| Passar a exigir `Idempotency-Key` ou `If-Match` | breaking | torne opcional primeiro, meça a adoção, depois exija em versão nova |
| Adicionar paginação a lista que era completa | breaking | AIP-158: adicionar depois quebra clientes (V-34); nasça paginada |
| Mudar formato do `page_token` | compatível se opaco | quebra quem o decodificava; por isso é opaco e sem garantia de formato |
| Trocar offset por cursor | breaking | aceite os dois por um período e deprecie o antigo |
| Mudar formato de erro (fora de RFC 9457 para RFC 9457) | breaking | clientes leem `error.message`; coexistência por versão |
| Novo header de resposta | compatível | |
| Mudar `Cache-Control`/ETag de modo a servir dado mais velho | pode quebrar | avalie frescor esperado por consumidores |

## 3. Proto/gRPC

- Número de campo **nunca** é reutilizado. Campo removido vira `reserved` (número e nome). Mudar o número é remover e criar outro campo.
- Mudar o tipo de um campo existente é breaking, salvo conjuntos de tipos compatíveis no formato de fio (confira a documentação do Protobuf; Inferido).
- Renomear serviço, método ou pacote é breaking para o cliente gerado; renomear só o nome do campo quebra JSON mapeado e código gerado, mas não o formato binário.
- Enum: mantenha o valor zero como `UNSPECIFIED`; valor novo exige que consumidores tratem desconhecidos.
- CI: `buf breaking --against '.git#branch=main'` (brain; confira sintaxe na versão instalada). Rodar contra a branch correta.
- Códigos de status e política de retry: `UNAVAILABLE` pode repetir (com idempotência quando houver efeito); `ABORTED` repete em nível superior; `FAILED_PRECONDITION` não repete até o estado mudar (V-17). A página oficial não mapeia para HTTP; qualquer tabela gRPC para HTTP é convenção do projeto.
- Deadlines: toda chamada tem deadline e o servidor propaga o prazo restante (brain).

## 4. GraphQL

Regras de V-30 (Apollo, MIT; redação própria) e do brain:

- Depreciar com `@deprecated(reason: "...")` antes de remover; meça uso do campo pelo registro de operações antes de remover.
- Argumento novo precisa de valor padrão ou ser anulável; senão quebra queries existentes.
- Mudar nulabilidade de campo de saída de `T` para `T!` é breaking para quem trata `null`; de `T!` para `T` quebra clientes tipados que assumiam não nulo (inverter requer cuidado nos dois sentidos).
- Valor novo em `enum` de saída: mesma regra do REST (consumidor com `switch` exaustivo). Remover valor é breaking.
- Mutation com um único argumento `input`, retorno do objeto afetado, por ação de negócio: adicionar campo opcional ao input é compatível.
- Erros chegam em `errors` com HTTP 200: não confie em status para detectar falha de contrato nos testes.

## 5. Eventos e schemas de mensagem

- Registro de schemas (Confluent usa o modo padrão `BACKWARD`: o schema novo lê dados gravados com o anterior). Verificado em 2026-10-10 na doc de schema evolution da Confluent; confira o modo configurado do seu registry.
- Campo opcional novo com padrão: compatível; remover campo obrigatório: breaking para consumidor antigo e novo conforme o modo.
- Evento é contrato com consumidores desconhecidos no tempo (replay): prefira acrescentar a alterar, e versione o tipo do evento (`pedido.pago.v2`) quando o significado muda.

## 6. Deprecar e remover

Sequência: (1) anunciar com data; (2) marcar na spec (`deprecated: true`); (3) sinalizar em tempo de execução; (4) medir tráfego do recurso antigo por consumidor; (5) remover só após o `Sunset` e com tráfego residual conhecido.

Sinalização por cabeçalhos: RFC 9745 (`Deprecation`, valor `@<segundos desde a época Unix>`, mais `Link` com `rel="deprecation"` para o guia) e RFC 8594 (`Sunset`, HTTP-date, não anterior ao `Deprecation`) (**Verificado** em 2026-10-10 em rfc-editor.org):

```http
Deprecation: @1788912000
Sunset: Wed, 31 Mar 2027 23:59:59 GMT
Link: <https://api.exemplo.com.br/docs/migracao-v2>; rel="deprecation"; type="text/html"
```

(Valores ilustrativos: `Deprecation` em data de Structured Fields; `Sunset` em HTTP-date.) Modelo de aviso: `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/aviso-de-deprecacao.md`.

Versionamento por caminho, header ou query é decisão do projeto. A regra "sem versão no caminho, `api-version` na query" é convenção da Azure (V-35); a regra transversal é: nenhuma quebra dentro de uma versão, uma estratégia por API, deprecar antes de remover (V-30, V-35).

## 7. Procedimento de revisão (diff de spec)

1. Obtenha a spec publicada (`git show <tag>:openapi.yaml`) e a nova.
2. Rode o diff do projeto (ex.: `oasdiff breaking base.yaml nova.yaml`); cole a saída. Sem ferramenta, compare por leitura e rotule **Inferido**.
3. Para cada mudança, aplique a tabela da seção 2 e preencha `mudança · classe · quem quebra · mitigação · consumidores afetados`.
4. Ferramenta não vê o que o schema não expressa (significado, ordenação, efeito colateral): faça a leitura dirigida dos itens de comportamento (enum, ordenação, regra de negócio, status).
5. Resultado: compatível, compatível com deprecação, ou exige versão nova; liste o plano para consumidores.
