# README por tipo de projeto

Conteúdo: tabela de tipos, perguntas por tarefa, checklist de aceite e erros de abertura. Origem: tabela por tipo e tarefas de V-45 (redação própria, com a lacuna de aprovação corrigida), modelo de seis blocos de V-23 (Write the Docs), regras de landing page de V-25 (CC0-1.0, destiladas). Rótulo geral: Verificado nas fontes; a adaptação para PT-BR é Suposição.

## Tabela por tipo

| Tipo | Leitor e decisão que ele toma | Blocos obrigatórios | Tom | O que não incluir |
| --- | --- | --- | --- | --- |
| `aberto` | Desconhecido que decide em 3 a 5 segundos se usa o projeto | Frase de valor, exemplo funcional, funcionalidades (tabela de 2 colunas), Quick Start, instalação, uso, contribuição e suporte, licença | Venda moderada: fatos mensuráveis, sem adjetivos vazios | FAQ extenso, roadmap especulativo, badges sem origem |
| `pessoal` | Você no futuro ou quem tropeça no repositório | O que é, por que existe, como rodar, o que está incompleto | Direto, curto | Seção de contribuição formal se não aceita PRs; diga isso em uma linha |
| `interno` | Colega de equipe que precisa rodar ou operar | Propósito, dono (time e canal), como rodar localmente, onde está a documentação, como pedir ajuda | Neutro, sem venda | Descrição de mercado; duplicar o wiki (aponte para ele) |
| `configuração` (dotfiles, infra, valores de Helm, repositório de CI) | Quem aplica a configuração em uma máquina ou ambiente | O que configura, pré-requisitos, como aplicar, variáveis e valores que mudam por ambiente, como reverter, como validar | Procedimental, segunda pessoa | Segredos, hostnames internos sensíveis, valores reais de produção |

## Perguntas por tarefa (faça uma só, cobrindo o que falta)

- `criar`: qual o propósito em uma frase, quem é o leitor, qual a primeira coisa que ele quer fazer?
- `adicionar seção X`: a seção responde a qual pergunta do leitor? Ela já existe em outro documento (então vira link)?
- `atualizar`: o que mudou no código desde o README? Se o usuário não souber, compare o README com o manifesto e os scripts (passo 2 do SKILL.md).
- `revisar`: qual o critério de sucesso (menos perguntas de novatos, adoção, onboarding mais rápido)?

## Checklist de aceite (todos verificáveis)

- [ ] A primeira frase diz o valor para o leitor; não começa com "A tool that", "Uma ferramenta que" nem com o nome repetido.
- [ ] Existe exemplo funcional nas primeiras 5 linhas de conteúdo.
- [ ] Quick Start copia e cola: sem `$`, sem placeholders ocultos, uma saída esperada descrita.
- [ ] Cada comando existe no manifesto, `Makefile` ou código (`Grep`).
- [ ] Instalação cita a versão mínima do manifesto (`engines`, `requires-python`, `rust-version`, `go`).
- [ ] Licença confere com `LICENSE`.
- [ ] Toda imagem e todo link relativo existem (`Glob`).
- [ ] Nenhuma palavra da lista de enchimento sem fato que a sustente.
- [ ] Documentos novos ou existentes relevantes são alcançáveis do README.
- [ ] Marcado "não executado" onde nada foi rodado.

## Erros de abertura (antes e depois)

| Antes | Problema | Depois (padrão) |
| --- | --- | --- |
| "Uma ferramenta robusta e poderosa para gerenciar tarefas." | Adjetivos sem fato; não diz o que faz | "Cria, agenda e repete tarefas pelo terminal, sem servidor: `tarefa add 'Pagar luz' --toda-segunda`." |
| "Bem-vindo ao projeto X!" | Não informa nada | Frase de valor + exemplo |
| Quick Start com 12 passos | Não é Quick Start | 3 a 5 linhas; o resto vai para um how-to ligado |

O exemplo da última coluna é ilustrativo (comando fictício); no README real, use somente comandos lidos no repositório.

## Por que tom de venda só aqui

O README de entrada compete por atenção; referência e how-to atendem quem já decidiu usar o projeto e precisa de precisão. Misturar os dois tons deixa a referência imprecisa e o README sem apelo. Quando o guia de estilo do projeto discordar, ele vence.
