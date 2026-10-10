---
name: review-pr-null-deref
description: "Mede se a revisão de um diff reporta o defeito real (desreferência de None) com arquivo:linha e evidência, ignora ruído de estilo, não edita nada e admite que foi revisão por leitura."
tags: [code-quality-refactoring, review-diff, high-signal]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta que u ou u.profile pode ser None em app/users.py:13 com severidade alta e correção em diff de texto, trata o import não usado e o nome u como ruído, não edita arquivos, não afirma ter rodado testes e dá veredito."
model: sonnet
---
Pode mergear esse PR? Foi a Camila que abriu e ela disse que é só um "ajuste pequeno" no e-mail do usuário. Segue o diff do arquivo `app/users.py`:

```diff
--- a/app/users.py
+++ b/app/users.py
@@ -10,3 +10,4 @@
-def get_user_email(user_id):
-    user = db.get(user_id)
-    return user.email
+import os
+def get_user_email(user_id):
+    u = db.get(user_id)
+    return u.profile.email.lower()
```

Contexto: `db.get` devolve `None` quando o usuário não existe e `profile` é opcional no modelo (muitos usuários antigos não têm perfil). O endpoint que chama essa função devolve 500 em qualquer exceção. Não tenho como rodar a suíte agora.
