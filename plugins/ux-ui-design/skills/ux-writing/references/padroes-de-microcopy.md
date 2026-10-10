# Padrões de microcopy por elemento (PT-BR e EN)

Os exemplos são do plugin, em redação própria, para ilustrar a forma; os fatos (prazos, nomes, valores) são fictícios. Tom, tratamento "você" e sentence case em PT-BR são Suposição até haver guia de voz do projeto (lacuna: sem fonte PT-BR de nível A ou B lida). Princípios de base: ux-copy da Anthropic (Apache-2.0, V-13), GOV.UK e Microsoft Writing Style Guide (V-14).

## Sumário

- [Botões e links](#botões-e-links)
- [Erros](#erros)
- [Estados vazios](#estados-vazios)
- [Confirmações destrutivas](#confirmações-destrutivas)
- [Carregando e sucesso](#carregando-e-sucesso)
- [Campos, rótulos e ajuda](#campos-rótulos-e-ajuda)
- [Tom](#tom)
- [Localização e tradução](#localização-e-tradução)
- [Lista de revisão rápida](#lista-de-revisão-rápida)

## Botões e links

Regra: verbo no infinitivo ou imperativo (escolha um e mantenha) + objeto específico. O rótulo deve fazer sentido sozinho, fora de contexto (leitor de tela lista botões e links).

| Ruim | Melhor | Motivo |
| --- | --- | --- |
| Enviar | Criar conta | nomeia o resultado |
| OK | Entendi | o botão responde à mensagem |
| Clique aqui | Ver tabela de preços | link descritivo (WCAG 2.4.4) |
| Submit | Save API key | EN: nomeia a ação e o objeto |
| Sim / Não em confirmação | Excluir projeto / Manter projeto | evita erro de leitura apressada |

A ação primária e o título da tela usam o mesmo verbo ("Criar conta" no título e no botão). O nome acessível deve conter o texto visível (WCAG 2.5.3).

## Erros

Modelo: o que aconteceu, por quê (só se o sistema sabe), o que fazer agora.

| Situação | PT-BR | EN |
| --- | --- | --- |
| Campo obrigatório | Informe seu e-mail para continuar. | Enter your email to continue. |
| Formato | Use o formato nome@exemplo.com. | Use the format name@example.com. |
| Sessão expirada | Sua sessão terminou por inatividade. Entre de novo para continuar. Suas alterações não salvas foram mantidas neste formulário. | Your session timed out. Sign in again to continue. |
| Rede | Não conseguimos conectar. Confira sua internet e tente de novo. | We couldn't connect. Check your internet connection and try again. |
| Permissão | Você não tem acesso a este relatório. Peça acesso a quem administra a conta. | You don't have access to this report. Ask your account admin for access. |
| Login | E-mail ou senha incorretos. | Incorrect email or password. |

Notas:

- No login, não revele qual dos dois está errado (requisito de segurança; coordene com `security-appsec`).
- "Suas alterações foram mantidas" só se o produto realmente as mantém. Confirme com o desenvolvedor.
- Códigos técnicos vão em "detalhes" opcional (diretriz 12), não no texto principal.

## Estados vazios

Modelo: por que está vazio + ação principal + (opcional) ajuda ou exemplo.

| Contexto | PT-BR | EN |
| --- | --- | --- |
| Primeiro uso | Você ainda não criou nenhum projeto. Crie o primeiro para organizar suas tarefas. [Criar projeto] | You haven't created a project yet. Create your first to organize your tasks. [Create project] |
| Busca sem resultado | Nenhum resultado para "balcão". Tente outra palavra ou limpe os filtros. [Limpar filtros] | No results for "counter". Try another word or clear the filters. [Clear filters] |
| Tudo concluído | Nada pendente por aqui. | Nothing pending here. |

Diferencie "ainda não há dados" de "filtros esconderam tudo" e de "erro ao carregar": cada um tem texto e ação próprios.

## Confirmações destrutivas

```text
Título:  Excluir o projeto "Loja Centro"?
Corpo:   Serão apagados 14 relatórios e 3 convites. Esta ação não pode ser desfeita.
Ações:   [Manter projeto] (primária, foco inicial)   [Excluir projeto] (destrutiva)
```

O corpo nomeia o que será perdido, com contagens reais do sistema (no exemplo, fictícias). Se existe desfazer, prefira "Projeto excluído. Desfazer" a um diálogo. Para ações financeiras ou legais, WCAG 3.3.4 pede verificação, confirmação ou reversão.

## Carregando e sucesso

| Momento | PT-BR | Observação |
| --- | --- | --- |
| Em andamento | Salvando… | caractere `…`, não três pontos; anunciado por região de status |
| Concluído | Alterações salvas. | sem exclamação; some sozinho só se não for informação necessária |
| Demora longa | Isso está levando mais que o normal. Você pode continuar, avisamos quando terminar. | só se o produto realmente avisa |

## Campos, rótulos e ajuda

- Rótulo visível e curto ("Data de nascimento"); dica abaixo do campo ("Dia, mês e ano"); placeholder só como exemplo ("12/03/1990"), nunca como rótulo.
- Marque opcional ou obrigatório em texto, não só com asterisco sem legenda.
- Instrução de mais de uma frase costuma compensar uma interação ruim: corrija a interação e corte a instrução.

## Tom

- Direto e caloroso, sem excesso de informalidade; sem viés de gênero, idade ou capacidade; sem humor em erro, pagamento ou dado sensível.
- A marca define a voz. Sem guia, ofereça duas alternativas de tom (neutro e acolhedor) e peça a escolha.
- Evite conversa fiada ("Bem-vindo ao nosso incrível…"): texto que o usuário ignora gasta atenção.

## Localização e tradução

Rotule estas notas no campo "nota de localização" da saída:

- **Expansão:** textos em português costumam ocupar mais espaço que os equivalentes em inglês; reserve folga nos limites de caracteres (Inferido; meça no seu conjunto de textos).
- **Plural e gênero:** use mensagens completas com plural do framework (ICU MessageFormat ou equivalente); não concatene fragmentos ("Você tem " + n + " itens").
- **Variáveis:** deixe o tradutor mover a variável; descreva o que ela contém ("{nome}: primeiro nome do usuário").
- **Formatos:** datas, números e moedas pelo recurso de localização (por exemplo `Intl`), nunca no texto fixo.
- **Sem texto em imagem**; sem trocadilhos e metáforas que não viajam.
- **Gênero gramatical:** prefira formulações neutras quando existirem ("Boas-vindas" em vez de "Bem-vindo(a)").

## Lista de revisão rápida

- O texto funciona sozinho, sem a tela ao redor?
- Diz o que fazer a seguir?
- Tem fato inventado? (prazo, valor, política)
- O verbo da ação é o mesmo em título, botão e mensagem de sucesso?
- Cabe nos limites e sobrevive à tradução?
- O tom vem de um guia ou está marcado Suposição?
