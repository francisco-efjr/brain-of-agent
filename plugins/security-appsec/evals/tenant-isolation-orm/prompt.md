---
name: tenant-isolation-orm
description: Mede se a revisão de autorização acha a ausência de filtro de tenant em listagem e detalhe, não aceita login como autorização, e propõe filtro no servidor e teste de negação entre empresas que relê o estado.
tags: [security-appsec, access-control-review, multi-tenant, idor, django]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta que listar e detalhe não filtram por empresa, explica o vazamento entre tenants com cenário, propõe filtro derivado de request.user no servidor e teste de negação entre empresas que relê o recurso, sem tratar login_required como autorização."
model: sonnet
---
Essas views Django listam e mostram faturas. Cada usuário pertence a uma empresa (`request.user.org_id`) e o modelo `Fatura` tem o campo `org` (chave estrangeira para a empresa). Pode ter vazamento de dados entre empresas? Estamos em produção com 40 clientes.

```python
# faturas/views.py
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import Fatura


@login_required
def listar(request):
    status = request.GET.get("status", "aberta")
    faturas = Fatura.objects.filter(status=status).values("id", "numero", "valor", "status")
    return JsonResponse(list(faturas), safe=False)


@login_required
def detalhe(request, pk):
    try:
        fatura = Fatura.objects.get(pk=pk)
    except Fatura.DoesNotExist:
        raise Http404
    return JsonResponse({"id": fatura.pk, "numero": fatura.numero, "valor": str(fatura.valor), "org_id": fatura.org_id})
```
