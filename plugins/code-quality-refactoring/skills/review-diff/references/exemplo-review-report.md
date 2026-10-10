# Exemplo: relatório de revisão preenchido

Molde ilustrativo. Nada foi executado: o pedido trouxe só o diff e uma frase de contexto, então tudo é revisão por leitura (Inferido). Os números de linha são relativos ao hunk, porque o diff colado não tem numeração absoluta.

## Pedido do usuário

"Pode mergear esse PR?" com o diff de `app/users.py`:

```diff
-def get_user_email(user_id):
-    user = db.get(user_id)
-    return user.email
+import os
+def get_user_email(user_id):
+    u = db.get(user_id)
+    return u.profile.email.lower()
```

Contexto informado: `db.get` devolve `None` quando o usuário não existe e `profile` é opcional no modelo.

## Como a skill chega ao relatório

1. Triagem: há diff, não é trivial. Segue.
2. Regras do projeto: nenhum `CLAUDE.md` citável foi colado; sem checagem de conformidade.
3. Escopo: a função agora devolve o e-mail em minúsculas via `profile`; sem plano ou requisito, não há como achar requisito faltante.
4. Ferramentas: nenhuma informada; "não rodei linter/typechecker".
5. Um `code-reviewer` recebe o diff e o contexto. Candidatos: (a) `u.profile.email.lower()` sem tratar `None`; (b) `import os` sem uso; (c) nome `u`.
6. Validação: o `finding-validator` procura guarda anterior no trecho; não há (o diff é o corpo inteiro da função). (a) CONFIRMADO. (b) o linter do projeto tipicamente pega import não usado (F401 no Ruff, `no-unused-vars` no ESLint), então sai do relatório do agente e vai para "o que foi checado". (c) preferência de nome: descartado no modo agente.

## Relatório

**Resumo.** A mudança troca `user.email` por `u.profile.email.lower()` e introduz dereferência de `None` em dois pontos (usuário inexistente e perfil ausente), ambos descritos no contexto do pedido. Veredito: bloquear até tratar os dois casos.

**Escopo.** Alvo: diff colado de `app/users.py`. Modo: agente. Lido: o diff e o contexto informado. Não lido: chamadores de `get_user_email`, testes, `CLAUDE.md`.

| # | Severidade | Categoria | Onde | Por que importa | Correção sugerida | Evidência | Rótulo | Confiança |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CRÍTICO | correção | `app/users.py`, linha 4 do hunk: `return u.profile.email.lower()` | `db.get` devolve `None` para usuário inexistente (`u.profile` levanta `AttributeError`) e `profile` é opcional (`None.email` levanta `AttributeError`) | Ver diff abaixo | O contexto do pedido descreve os dois casos; o corpo da função não tem guarda | Inferido (não executei) | 92 |

Correção sugerida (proposta em texto, nada foi aplicado):

```diff
 def get_user_email(user_id):
     u = db.get(user_id)
-    return u.profile.email.lower()
+    if u is None or u.profile is None or u.profile.email is None:
+        return None
+    return u.profile.email.lower()
```

A linha `email is None` depende de o campo aceitar `None`: **Suposição** (o contexto não diz). Se o contrato do chamador preferir exceção a `None`, a escolha é do autor; o ponto é tratar o caso de forma explícita.

**Dúvidas (não verificadas, sem confiança alta).**

- O chamador espera `str` ou aceita `None`? Sem ler os chamadores, não dá para saber se devolver `None` quebra outro ponto (Não verificado).
- O PR inclui teste para usuário inexistente e perfil ausente? Não está no diff colado.

**O que foi checado.** Desreferência de `None` em `u` e `u.profile`; mudança de contrato do retorno (`.lower()` altera o valor devolvido: antes preservava a caixa); import novo. **Não foi checado.** Chamadores, testes existentes, comportamento em execução, desempenho.

**Fora do relatório por regra.** `import os` sem uso e o nome `u`: linter e preferência de estilo (no modo humano entrariam como `nitpick (non-blocking)`).

**Observação de contrato.** O retorno passou a vir em minúsculas; se algum chamador compara com o e-mail original, o resultado muda. Isso é IMPORTANTE e depende dos chamadores (Não verificado): vale conferir no PR.

**Veredito.** Bloquear (1 achado CRÍTICO). Status: DONE_WITH_CONCERNS (sem execução; chamadores não lidos).

**Independência.** Revisor e autor podem ser o mesmo modelo e compartilhar pontos cegos; leia o diff também como humano.

## O que este molde mostra

- Um achado forte com linha, texto, impacto e correção; ruído de estilo fora.
- Rótulo honesto: sem execução, tudo é Inferido; a Suposição sobre `email` está marcada.
- Dúvidas separadas, em vez de achados com confiança inflada.
- Nenhum arquivo editado, nenhum comentário publicado.
