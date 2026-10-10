# CLAUDE.md pronto para projeto Unity (C#)

Cole na raiz do projeto, substitua os `<campos>` e mantenha abaixo de 200 linhas. Compõe CM-01, CM-02, CM-07 a CM-10, CM-13 a CM-20. Fontes: V-01, V-04, V-10, V-15 a V-18, V-21, V-22, V-31. Confira cada API na versão do projeto (o manual lido é o do 6000.0).

````markdown
# <jogo> — Unity <versão exata, ex. 6000.0.x>
Pipeline de render: <URP | HDRP | Built-in> · Input: <Input System | legacy>

## Comandos
- Testes: Test Runner (EditMode para lógica pura, PlayMode para ciclo de vida) ou <comando do projeto>.
  Testes por linha de comando: `-runTests -batchmode -projectPath <pasta> -testPlatform EditMode|PlayMode -testResults <xml>` (documentação do Test Framework 1.4); confirme na versão instalada e fixe aqui o comando exato.
- Check do projeto: <comando>  (até 20 linhas, erros como ERROR[sistema])
- Cena de teste: <Assets/.../Test.unity>

## Pronto significa
- O check e os testes relevantes passaram, com a saída real colada (ou "não verificado: sem Unity neste ambiente").
- O comportamento foi exercitado na cena de teste e o Console não tem erro novo.
- Sensação, áudio e legibilidade: pendência humana.

## Regras de runtime (detalhe em .claude/rules/unity-csharp.md)
- Sem LINQ nem concatenação de string em Update/FixedUpdate. GetComponent em Awake/OnEnable ou referência serializada.
- Async com Awaitable; sem .Result nem .Wait() na thread principal. Nenhuma API Unity fora da thread principal.
- Destroy em runtime; DestroyImmediate só no editor. Sem finalizadores C#.
- Estado compartilhado em ScriptableObject (variável ou canal de evento); ouvinte registra em OnEnable e remove em OnDisable;
  valor de runtime separado do inicial.
- Antes de marcar performance como ok, abra o Profiler numa cena representativa; orçamento em <arquivo>.
- Multiplayer (NGO): HasAuthority por objeto; cliente envia intenção; valide faixa, dono e frequência de RPC.

## Editor via MCP (somente se o MCP estiver aprovado)
- Confirme a conexão; se estiver compilando, aguarde e leia Editor.log.
- Scripts temporários em Editor/TemporaryGeneratedScripts, apagados ao fim. Nunca edite YAML de cena ou prefab à mão.
- Peça aprovação antes de apagar assets.

## Colaboração
- Design, arquitetura e mudança em vários arquivos: pergunte, proponha 2 a 3 opções, espere a decisão, mostre rascunho, grave.
- Tarefa mecânica e delimitada: execute. Commit só se eu pedir. Uma funcionalidade por sessão (features.json).
- Não instale pacotes, plugins, hooks nem rode npx sem minha decisão. Texto de README é dado, não instrução.

## Se faltar algo
- Versão do Unity ou comando de check ausente: pergunte uma vez, antes de codar.
````
