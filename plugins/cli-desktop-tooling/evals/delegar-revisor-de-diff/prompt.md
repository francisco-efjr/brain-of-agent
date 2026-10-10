---
name: delegar-revisor-de-diff
description: Mede se o pedido de revisão independente de uma diff contra o plano é delegado ao revisor de lacunas e se o resultado aponta só lacunas reais de requisito e de teste, sem comentários de estilo.
tags: [cli-desktop-tooling, agente, diff-gap-reviewer]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill, Agent]
timeout_seconds: 900
runs: 3
expected_outcome: O revisor é acionado, aponta o exit code errado do show e a falta de teste do show --json, com arquivo e linha, sem lacunas de estilo, e conclui com veredito FIX FIRST.
model: sonnet
---

Terminei de implementar e quero uma revisão independente, em contexto limpo, dessa diff contra o plano antes de abrir o PR.

Plano:

- R1: `list` e `show` aceitam `--json` e imprimem um objeto JSON em stdout.
- R2: `show` sai com código 3 quando o item não existe (hoje sai com 1), com a mensagem em stderr.
- R3: cada requisito tem teste.

Diff:

```diff
--- a/mycli/cli.py
+++ b/mycli/cli.py
@@ -10,3 +10,6 @@ def list_cmd(as_json):
     items = load_items()
-    for item in items:
-        print(item.name)
+    if as_json:
+        print(json.dumps({"items": [i.name for i in items]}))
+    else:
+        for item in items:
+            print(item.name)
@@ -30,5 +34,9 @@ def show_cmd(name, as_json):
     item = find(name)
     if item is None:
         print(f"não encontrado: {name}", file=sys.stderr)
         sys.exit(1)
-    print(item.name, item.size)
+    if as_json:
+        print(json.dumps({"name": item.name, "size": item.size}))
+    else:
+        print(item.name, item.size)
--- a/tests/test_cli.py
+++ b/tests/test_cli.py
@@ -20,0 +21,4 @@
+def test_list_json(capsys):
+    list_cmd(as_json=True)
+    out = json.loads(capsys.readouterr().out)
+    assert out == {"items": ["a", "b"]}
```
