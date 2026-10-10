# features.json e log de progresso (harness de tarefa longa)

Fonte: V-08 (Anthropic, "Effective harnesses for long-running agents"), redação própria. Use em tarefa de várias sessões. O JSON foi escolhido na fonte porque o modelo o sobrescreve menos que Markdown. Sem hook ativo por padrão.

## Esquema

```json
{
  "features": [
    {
      "id": 1,
      "categoria": "auth",
      "descricao": "Usuário entra com e-mail e senha",
      "passos_de_verificacao": ["abrir /login", "enviar credenciais válidas", "ver o painel"],
      "passa": false
    }
  ]
}
```

## Regras de sessão

1. Só o campo `passa` pode mudar. Nunca remova nem edite testes ou passos de verificação.
2. Uma funcionalidade por sessão.
3. Marque `passa: true` só depois de verificar pela interface (ou pelo comando definido), com evidência colada no log.
4. **Início:** confirmar diretório; ler `progress.md` e `git log`; ler `features.json`; subir o ambiente; rodar um teste ponta a ponta antes de codar.
5. **Fim:** estado limpo; commit descritivo; log atualizado; pendências listadas.

## `progress.md`

```markdown
# Progresso
| Data | Sessão | Funcionalidade | Feito | Evidência (comando e última linha da saída) | Pendências |
| --- | --- | --- | --- | --- | --- |
```

## Limites

A fonte cita mais de 200 funcionalidades sem métrica de sucesso e deixa em aberto agente único contra especializados. Trate como template. Substitua `[...]` pelos requisitos reais; categorias e passos devem ser verificáveis por outra pessoa.
