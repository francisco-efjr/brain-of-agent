# Formatos de critério, EARS, Gherkin em português e exemplo resolvido

Fontes: V-16 e V-17 (Cucumber, destilado), V-20 (EARS, síntese da Wikipedia sobre Mavin et al., 2009; o artigo original não foi lido), V-36 (product-on-purpose, Apache-2.0, destilado), V-42 (base própria MIT, Francisco Edson). Redação própria; o exemplo é original deste plugin.

## Sumário

- [Escolha do formato](#escolha-do-formato)
- [EARS em português](#ears-em-português)
- [Gherkin em português](#gherkin-em-português)
- [Exemplo resolvido: exportar relatórios](#exemplo-resolvido-exportar-relatórios)
- [Quando não usar Gherkin](#quando-não-usar-gherkin)

## Escolha do formato

Um padrão principal por spec (V-20). Decida por quem lê e pelo tipo de comportamento.

| Formato | Use quando | Cuidado |
| --- | --- | --- |
| Regra + exemplo | padrão para quase tudo | todo exemplo com dado concreto |
| Given/When/Then (Gherkin) | negócio lê e discute; há contexto e estados; o time automatiza BDD | declarativo; um comportamento por cenário |
| EARS | comportamento de sistema, regulado, embarcado | mais de 3 pré-condições fica pesado; requisito sem condição encaixa mal |
| Checklist | verificações simples e independentes (campos, textos, layout) | cada item verificável sozinho |

## EARS em português

Modelos de frase (tradução própria dos padrões de V-20). Ordem: pré-condições (ENQUANTO), gatilho (QUANDO), sistema, resposta. Zero ou mais pré-condições, zero ou um gatilho, um nome de sistema, uma ou mais respostas.

| Tipo | Modelo | Exemplo |
| --- | --- | --- |
| Ubíquo | O `<sistema>` DEVE `<resposta>`. | O sistema DEVE registrar cada exportação em auditoria. |
| Evento | QUANDO `<gatilho>`, o `<sistema>` DEVE `<resposta>`. | QUANDO o gerente solicitar a exportação, o sistema DEVE gerar o arquivo com as linhas do filtro aplicado. |
| Estado | ENQUANTO `<estado>`, o `<sistema>` DEVE `<resposta>`. | ENQUANTO uma exportação estiver em andamento, o sistema DEVE exibir o progresso. |
| Opcional | ONDE `<funcionalidade presente>`, o `<sistema>` DEVE `<resposta>`. | ONDE o plano incluir XLSX, o sistema DEVE oferecer o formato XLSX. |
| Indesejado | SE `<condição indesejada>`, ENTÃO o `<sistema>` DEVE `<resposta>`. | SE a geração do arquivo falhar, ENTÃO o sistema DEVE informar o erro e NÃO DEVE disponibilizar arquivo parcial. |
| Complexo | combinação | ENQUANTO o mês estiver fechado, QUANDO o gerente solicitar exportação, o sistema DEVE incluir só vendas conciliadas. |

## Gherkin em português

Primeira linha do arquivo: `# language: pt`.

| Inglês | Português |
| --- | --- |
| Feature | Funcionalidade (Característica) |
| Rule | Regra |
| Background | Contexto (Cenário de Fundo, Fundo) |
| Scenario / Example | Cenário (Exemplo) |
| Scenario Outline | Esquema do Cenário |
| Examples | Exemplos (Cenários) |
| Given / When / Then | Dado (Dada, Dados, Dadas) / Quando / Então |
| And / But | E / Mas |

Armadilhas de tradução: `Exemplo:` é sinônimo de `Cenário`, e `Cenários:` é sinônimo de `Exemplos`; a palavra-chave não faz parte do texto casado pela step definition. Papel das palavras (V-16): `Dado` descreve estado conhecido; `Quando`, ação ou evento; `Então`, resultado observável em saída (não leia o banco direto). Um `Contexto` por Funcionalidade ou Regra. `Rule` existe desde o Gherkin 6; ferramentas antigas podem não reconhecer a palavra: confirme na versão do time.

Regra de uso: regra de negócio -> `Regra`; mesma lógica com dados variados -> `Esquema do Cenário` com linhas em partições e limites distintos; contexto comum e curto -> `Contexto`.

## Exemplo resolvido: exportar relatórios

Entrada, como o usuário colou:

> História: "Como gerente quero exportar relatórios para analisar dados." Critérios: o export deve ser rápido, suportar vários formatos etc. e ser seguro.

### 1. Palavras vagas

| Trecho | Problema | Pergunta |
| --- | --- | --- |
| "relatórios" | quais? todos? | Quais relatórios entram? (vendas, estoque, outros) |
| "rápido" | sem número | Em quanto tempo, para quantas linhas, medido onde? |
| "vários formatos" | quantos? quais? | Quais formatos, exatamente? |
| "etc." | lista aberta | Qual é a lista completa? |
| "seguro" | genérico | Quem pode exportar? O que fica registrado? Há dado pessoal no arquivo? |

### 2. Regras implícitas e não funcionais que se aplicam

| Categoria | Pergunta |
| --- | --- |
| Permissão | Só gerente? Gerente de outra loja vê dados da loja dele? |
| Limites | Há máximo de linhas? O que acontece acima dele? |
| Falhas | O que ocorre se a geração falhar no meio? |
| Concorrência | Duas exportações ao mesmo tempo do mesmo usuário? |
| Efeitos em volta | A exportação deve ficar em auditoria? |
| LGPD | O arquivo traz dado pessoal (CPF, e-mail)? Mascarar? (conferir com jurídico) |

### 3. Critérios propostos (regra + exemplo), ordem feliz -> falhas -> não funcionais

Nenhum número abaixo veio do usuário: onde há limite, ele está como pergunta aberta ou Suposição.

| # | Critério | Oráculo | Ambiguidade/risco |
| --- | --- | --- | --- |
| C1 | A exportação reflete o filtro: vendas de 01/09 a 30/09 (120 vendas; há 30 de agosto) geram arquivo com 120 linhas e nenhuma de agosto | contagem de linhas e datas | formato ainda não definido (Q1) |
| C2 (negativo) | Atendente não exporta: tentativa recusada com mensagem de permissão e nenhum arquivo gerado | resposta e ausência de arquivo | quem tem permissão? (Q2) |
| C3 (negativo) | Falha na geração informa o erro e não deixa arquivo parcial disponível | ausência de arquivo; mensagem | texto da mensagem (Q4) |
| C4 | Acima de `TBD` linhas, o comportamento é `TBD` (recusar, enviar por e-mail, paginar) | depende de Q3 | pendente |
| C5 | Cada exportação gera registro de auditoria com quem, quando, qual relatório e filtro, sem o conteúdo | registro consultável | política de retenção (Q5); Suposição de que auditoria é desejada |
| C6 (não funcional) | Tempo de geração: p95 de `TBD` s para até `TBD` linhas, medido em `TBD` | teste de carga no ambiente definido | números dependem de Q3 e de infraestrutura |

### 4. Perguntas abertas

| ID | Pergunta | Dono |
| --- | --- | --- |
| Q1 | Quais formatos? (Suposição de partida: CSV; confirmar outros) | produto |
| Q2 | Quais perfis podem exportar? | produto/segurança |
| Q3 | Limite de linhas e comportamento acima dele | produto/engenharia |
| Q4 | Texto das mensagens de erro | produto |
| Q5 | Auditoria e retenção; mascaramento de dado pessoal | jurídico/segurança |

### 5. Gherkin (declarativo, sem passos de interface)

```gherkin
# language: pt
Funcionalidade: Exportação de relatório de vendas
  Para analisar as vendas fora do sistema,
  a gerente exporta o relatório do período filtrado.

  Regra: A exportação reflete exatamente o filtro aplicado

    Cenário: Exporta as vendas do período filtrado
      Dado que a loja teve 120 vendas em setembro de 2026 e 30 em agosto de 2026
      Quando a gerente Ana exporta as vendas de 01/09/2026 a 30/09/2026
      Então o arquivo contém 120 linhas de venda
      E nenhuma venda de agosto aparece no arquivo

  Regra: Só quem tem permissão exporta

    Cenário: Atendente não consegue exportar
      Dado que Bia tem perfil de atendente
      Quando Bia tenta exportar as vendas de setembro de 2026
      Então a exportação é recusada com "Você não tem permissão para exportar relatórios."
      E nenhum arquivo é gerado

  Regra: Falha na geração não deixa arquivo parcial

    Cenário: Erro durante a geração
      Dado que a geração do arquivo vai falhar para as vendas de setembro de 2026
      Quando a gerente Ana exporta as vendas de 01/09/2026 a 30/09/2026
      Então Ana vê a mensagem de erro de exportação
      E nenhum arquivo fica disponível para download

  @pendente
  Regra: Relatórios acima do limite (limite e comportamento aguardam a resposta Q3)
```

Fora do Gherkin: tempo de geração (C6) e auditoria (C5) ficam como critérios técnicos ou checklist, porque são verificações de sistema, não regras que o negócio discute cenário a cenário. Verbos de interface ("clico", "seleciono") aparecem zero vezes; trocar o desenho da tela não altera nenhum cenário.

Os nomes (Ana, Bia) são dados concretos de exemplo. Passos como "a geração do arquivo vai falhar" exigem que a automação consiga simular a falha; quem implementa isso é a camada de testes (`qa-testing`).

## Quando não usar Gherkin

BDD é conversa (descoberta), formulação e automação; Gherkin é só a formulação. Evite quando: ninguém de negócio lê os `.feature` (vira camada de tradução a manter); o alvo é cálculo com muitas variações (teste parametrizado é mais direto); o teste é técnico (performance, segurança, contrato, layout); o QA escreve sozinho depois do código; o trabalho é exploratório. Example Mapping e três amigos valem mesmo sem Gherkin (V-42); a skill `refine-backlog` cobre isso.
